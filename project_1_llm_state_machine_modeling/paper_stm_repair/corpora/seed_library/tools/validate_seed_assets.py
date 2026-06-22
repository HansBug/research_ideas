#!/usr/bin/env python3
"""Validate seed_library first-source registry assets.

The repository intentionally keeps this validator dependency-light: it performs
JSON syntax checks, schema-lite required/enum checks, manifest raw hashes,
pairs.jsonl source_asset_id/source_sha256 consistency, and validation_summary
count consistency. If the optional jsonschema package is later installed, this
script can still be complemented by full JSON Schema validation.
"""
from __future__ import annotations
import argparse, hashlib, json, sys
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
ROLE_ENUM = {
    'final_pool_ready', 'conditional_final_pool', 'pipeline_only',
    'reference_only', 'paper_reconstructable', 'related_only', 'excluded'
}
ASSET_STATUS_ENUM = {'downloaded', 'partially_downloaded', 'metadata_only', 'blocked', 'not_applicable'}
STORAGE_ENUM = {'committed', 'local_only', 'metadata_only', 'skipped'}
DOWNLOAD_ENUM = {'downloaded', 'skipped', 'blocked', 'metadata_only', 'local_only'}


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def load_json(p: Path):
    return json.loads(p.read_text())


def iter_pairs(p: Path):
    if not p or str(p) == '.' or not p.exists():
        return []
    rows=[]
    with p.open() as f:
        for line in f:
            line=line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def require(obj: dict, keys: list[str], label: str, errors: list[str]):
    for key in keys:
        if key not in obj:
            errors.append(f'{label} missing required field {key}')


def validate_registry_shape(reg: dict, errors: list[str]):
    require(reg, ['schema_version','seed_id','source_work','asset_summary','pair_sets','reference_sets','extracted_summary','downstream_selection','recommended_role','blockers','legacy_audit_refs'], 'registry', errors)
    if reg.get('schema_version') != 'seed-resource-registry.v1':
        errors.append('registry schema_version must be seed-resource-registry.v1')
    if reg.get('recommended_role') not in ROLE_ENUM:
        errors.append(f'unknown recommended_role {reg.get("recommended_role")}')
    asset_summary = reg.get('asset_summary', {})
    require(asset_summary, ['manifest_path','first_source_status','license_status','redistribution_status','version_pin'], 'asset_summary', errors)
    if asset_summary.get('first_source_status') not in ASSET_STATUS_ENUM:
        errors.append(f'unknown first_source_status {asset_summary.get("first_source_status")}')
    ds = reg.get('downstream_selection', {})
    require(ds, ['r2_smoke_recommendation','source_coverage_class','input_format_class','conversion_pressure','defect_risk_class','selection_caveat'], 'downstream_selection', errors)
    for i, pair_set in enumerate(reg.get('pair_sets', [])):
        require(pair_set, ['pair_set_id','nl_role','stm0_role','raw_pair_count','eligible_pair_count','canonical_case_count','reference_pair_count','generation_actor','generation_model_or_method','stm_family','stm_time_level','eligibility_state','must_not_count_as_generated','excluded_outputs','extracted_pairs_path'], f'pair_sets[{i}]', errors)
        if pair_set.get('eligibility_state') not in ROLE_ENUM:
            errors.append(f'pair_sets[{i}] unknown eligibility_state {pair_set.get("eligibility_state")}')


def validate_manifest_shape(manifest: dict, errors: list[str]):
    require(manifest, ['schema_version','seed_id','source_work','manifest_created_at','first_source_policy','assets','derived_assets','skipped_assets'], 'manifest', errors)
    if manifest.get('schema_version') != 'seed-assets-manifest.v1':
        errors.append('manifest schema_version must be seed-assets-manifest.v1')
    for i, asset in enumerate(manifest.get('assets', [])):
        require(asset, ['asset_id','role','source_url','source_url_type','download_status','accessed_at','local_path','storage_mode','license_status','redistribution_status','version_pin','sha256','bytes','notes'], f'assets[{i}]', errors)
        if asset.get('download_status') not in DOWNLOAD_ENUM:
            errors.append(f'assets[{i}] unknown download_status {asset.get("download_status")}')
        if asset.get('storage_mode') not in STORAGE_ENUM:
            errors.append(f'assets[{i}] unknown storage_mode {asset.get("storage_mode")}')


def validate_seed(seed_id: str) -> int:
    seed_dir = BASE / seed_id
    reg_path = seed_dir / 'seed_resource_registry.json'
    errors=[]
    if not reg_path.exists():
        print(f'ERROR missing registry: {reg_path}', file=sys.stderr)
        return 1
    reg = load_json(reg_path)
    validate_registry_shape(reg, errors)
    manifest_rel = reg.get('asset_summary', {}).get('manifest_path', '')
    manifest_path = seed_dir / manifest_rel if manifest_rel else None
    if manifest_rel and (not manifest_path or not manifest_path.exists() or manifest_path.is_dir()):
        errors.append(f'manifest_path does not point to file: {manifest_rel}')
        manifest = {'assets': []}
    elif manifest_path:
        manifest = load_json(manifest_path)
        validate_manifest_shape(manifest, errors)
    else:
        manifest = {'assets': []}
    asset_by_id = {a['asset_id']: a for a in manifest.get('assets', []) if 'asset_id' in a}
    for asset in manifest.get('assets', []):
        if asset.get('storage_mode') == 'committed' and asset.get('download_status') == 'downloaded':
            p = seed_dir / 'assets' / asset.get('local_path', '')
            if not p.exists() or p.is_dir():
                errors.append(f'missing raw asset {asset.get("asset_id")}: {p}')
                continue
            actual = sha256_file(p)
            if actual != asset.get('sha256'):
                errors.append(f'asset hash mismatch {asset.get("asset_id")}: {actual} != {asset.get("sha256")}')
    pairs_rel = reg.get('extracted_summary', {}).get('pairs_jsonl', '')
    pairs_path = seed_dir / pairs_rel if pairs_rel else Path('')
    pairs = iter_pairs(pairs_path)
    trace_verified = 0
    eligible = 0
    for row in pairs:
        aid = row.get('source_asset_id')
        asset = asset_by_id.get(aid)
        if not asset:
            errors.append(f'pair {row.get("pair_id")} unknown source_asset_id {aid}')
            continue
        if asset.get('storage_mode') == 'committed' and asset.get('download_status') == 'downloaded':
            p = seed_dir / 'assets' / asset.get('local_path', '')
            if p.exists() and row.get('source_sha256') != sha256_file(p):
                errors.append(f'pair {row.get("pair_id")} source_sha256 mismatch')
        if row.get('trace_verified'):
            trace_verified += 1
        if row.get('trace_verified') and row.get('is_generated_stm0') and not row.get('is_reference') and not row.get('is_postprocessed'):
            eligible += 1
    vs_rel = reg.get('extracted_summary', {}).get('validation_summary', '')
    vs_path = seed_dir / vs_rel if vs_rel else Path('')
    if vs_path and str(vs_path) != '.' and vs_path.exists():
        vs = load_json(vs_path)
        if vs.get('trace_verified_pair_count') != trace_verified:
            errors.append(f'validation_summary trace count mismatch: {vs.get("trace_verified_pair_count")} != {trace_verified}')
        if vs.get('eligible_generated_pair_count') != eligible:
            errors.append(f'validation_summary eligible count mismatch: {vs.get("eligible_generated_pair_count")} != {eligible}')
    if reg.get('extracted_summary', {}).get('eligible_generated_pair_count') != eligible:
        errors.append(f'registry eligible count mismatch: {reg.get("extracted_summary", {}).get("eligible_generated_pair_count")} != {eligible}')
    if reg.get('recommended_role') == 'final_pool_ready':
        if eligible == 0:
            errors.append('final_pool_ready registry must have at least one eligible generated pair')
        if reg.get('asset_summary', {}).get('redistribution_status') in {'metadata_only','unknown','restricted'}:
            errors.append('final_pool_ready cannot use metadata_only/unknown/restricted redistribution status')
    if errors:
        for e in errors:
            print('ERROR', seed_id, e, file=sys.stderr)
        return 1
    print(json.dumps({'seed_id': seed_id, 'pair_count': len(pairs), 'trace_verified_pair_count': trace_verified, 'eligible_generated_pair_count': eligible}, ensure_ascii=False))
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('seed_id', nargs='+')
    args = ap.parse_args()
    code = 0
    for seed in args.seed_id:
        code |= validate_seed(seed)
    raise SystemExit(code)


if __name__ == '__main__':
    main()
