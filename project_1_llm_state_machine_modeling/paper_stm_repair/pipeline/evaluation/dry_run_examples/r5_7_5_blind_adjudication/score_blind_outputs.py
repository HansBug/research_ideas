#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, re
from pathlib import Path

ROOT=Path(__file__).resolve().parent
SCHEMA=ROOT.parents[3]/'experiment_design/protocols/better_adjudication_blind_output_schema_v0.json'
GATES=[f'G{i}' for i in range(7)]

def load_json(p:Path): return json.loads(p.read_text(encoding='utf-8'))

def extract_json(text:str):
    text=text.strip()
    if text.startswith('{'):
        return json.loads(text)
    m=re.search(r'\{.*\}', text, flags=re.S)
    if not m: raise ValueError('no JSON object found')
    return json.loads(m.group(0))

def validate_schema(obj):
    try:
        import jsonschema # type: ignore
    except Exception:
        return None
    jsonschema.validate(obj, load_json(SCHEMA))

def normalize_run_validity(v):
    mapping={
        'valid_constructed_protocol_case':'valid',
        'valid_blind_protocol_case':'valid',
        'candidate_schema_or_parse_invalid':'candidate_invalid',
        'stmk_repair_failure':'candidate_invalid',
        'protocol_or_provenance_invalid':'protocol_or_provenance_invalid',
        'stress_only_not_headline':'stress_only_not_headline',
    }
    return mapping.get(v, v)

def gate_statuses(obj):
    gates=obj.get('gate_results') or {}
    return {g: (gates.get(g) or {}).get('status') for g in GATES}

def load_meta_end(od:Path):
    p=od/'run_meta_end.json'
    if not p.exists():
        return {}
    try:
        return load_json(p)
    except Exception:
        return {'meta_parse_error':'run_meta_end.json is not valid JSON'}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--judge', required=True)
    ap.add_argument('--outputs-dir', default=None)
    ap.add_argument('--require-all-valid', action='store_true')
    ap.add_argument('--require-all-core-match', action='store_true', help='Require verdict, scope, and run-validity match for every case.')
    ap.add_argument('--require-no-leakage', action='store_true')
    args=ap.parse_args()
    oracle={c['blind_case_id']:c for c in load_json(ROOT/'oracle_answer_key.json')['cases']}
    outroot=Path(args.outputs_dir) if args.outputs_dir else ROOT/'judge_outputs'/args.judge
    rows=[]
    for bid, ans in sorted(oracle.items()):
        od=outroot/bid
        parsed_path=od/'parsed_output.json'
        raw_path=od/'raw_output.txt'
        meta_end=load_meta_end(od)
        status='missing'
        obj=None
        err=None
        if parsed_path.exists():
            try:
                obj=load_json(parsed_path)
                validate_schema(obj)
                status='valid_json'
            except Exception as e:
                status='schema_or_json_error'; err=str(e)
        elif raw_path.exists():
            try:
                raw_text = raw_path.read_text(encoding='utf-8')
                if not raw_text.strip():
                    raise ValueError('raw_output.txt is empty; combined transcript is audit-only and is not parsed')
                obj=extract_json(raw_text)
                validate_schema(obj)
                status='valid_json_from_raw'
            except Exception as e:
                status='parse_error'; err=str(e)
        if obj:
            expected_judge_id=args.judge
            identity_errors=[]
            if obj.get('blind_case_id') != bid:
                identity_errors.append(f"blind_case_id mismatch: expected {bid}, observed {obj.get('blind_case_id')}")
            if obj.get('judge_id') != expected_judge_id:
                identity_errors.append(f"judge_id mismatch: expected {expected_judge_id}, observed {obj.get('judge_id')}")
            transport_ok = meta_end.get('exit_code') == 0 and meta_end.get('parse_error') in (None, '')
            schema_ok = status.startswith('valid_json')
            output_valid = schema_ok and transport_ok and not identity_errors
            if schema_ok and not transport_ok:
                status='transport_failed_with_parsed_output'
            elif schema_ok and identity_errors:
                status='schema_valid_identity_mismatch'
            expected_gates=ans.get('expected_gate_results', {}) or {}
            observed_gates=gate_statuses(obj)
            gate_matches={g: output_valid and observed_gates.get(g)==expected_gates.get(g) for g in GATES}
            gate_disagreements=[
                {'gate':g,'expected':expected_gates.get(g),'observed':observed_gates.get(g)}
                for g in GATES if not gate_matches.get(g)
            ]
            row={
                'blind_case_id':bid,
                'source_case_id':ans['source_case_id'],
                'judge_id':obj.get('judge_id'),
                'status':status,
                'schema_error': err,
                'eligible_output': output_valid,
                'exit_code': meta_end.get('exit_code'),
                'parse_error': meta_end.get('parse_error'),
                'provider_or_cli_nonzero_with_parsed_output': meta_end.get('provider_or_cli_nonzero_with_parsed_output'),
                'identity_errors': identity_errors,
                'expected_verdict':ans['primary_expected_verdict'],
                'observed_verdict':obj.get('primary_verdict'),
                'verdict_match': output_valid and obj.get('primary_verdict')==ans['primary_expected_verdict'],
                'expected_scope':ans['scope_routing_status'],
                'observed_scope':obj.get('scope_routing_status'),
                'scope_match': output_valid and obj.get('scope_routing_status')==ans['scope_routing_status'],
                'expected_run_validity':ans['run_validity_status'],
                'observed_run_validity':obj.get('run_validity_status'),
                'run_validity_match': output_valid and normalize_run_validity(obj.get('run_validity_status'))==normalize_run_validity(ans['run_validity_status']),
                'expected_gate_results': expected_gates,
                'observed_gate_results': observed_gates,
                'gate_matches': gate_matches,
                'gate_all_match': output_valid and all(gate_matches.values()),
                'gate_disagreements': gate_disagreements,
                'leakage_detected': obj.get('leakage_observation',{}).get('detected'),
                'confidence': obj.get('confidence'),
                'human_escalation_required': obj.get('human_escalation_required')
            }
        else:
            row={'blind_case_id':bid,'source_case_id':ans['source_case_id'],'status':status,'error':err,'eligible_output':False,'exit_code':meta_end.get('exit_code'),'parse_error':meta_end.get('parse_error'),'expected_verdict':ans['primary_expected_verdict'],'verdict_match':False,'scope_match':False,'run_validity_match':False,'gate_all_match':False}
        rows.append(row)
    summary={
        'schema_version':'r5_7_5.blind_score_summary.v1',
        'judge':args.judge,
        'run_validity_match_policy':'normalized_equivalence: valid_constructed_protocol_case and valid_blind_protocol_case are both counted as valid; candidate_schema_or_parse_invalid and stmk_repair_failure are both counted as candidate_invalid. This is not literal string equality.',
        'case_count':len(rows),
        'valid_output_count':sum(r.get('eligible_output') is True for r in rows),
        'verdict_match_count':sum(r.get('verdict_match') is True for r in rows),
        'scope_match_count':sum(r.get('scope_match') is True for r in rows),
        'run_validity_match_count':sum(r.get('run_validity_match') is True for r in rows),
        'gate_all_match_count':sum(r.get('gate_all_match') is True for r in rows),
        'gate_status_match_counts':{g:sum((r.get('gate_matches') or {}).get(g) is True for r in rows) for g in GATES},
        'gate_disagreement_count':sum(len(r.get('gate_disagreements') or []) for r in rows),
        'leakage_detected_count':sum(r.get('leakage_detected') is True for r in rows),
        'rows':rows
    }
    (outroot/'score_summary.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    failures=[]
    if args.require_all_valid and summary['valid_output_count'] != summary['case_count']:
        failures.append(f"valid_output_count {summary['valid_output_count']} != case_count {summary['case_count']}")
    if args.require_all_core_match:
        for k in ['verdict_match_count','scope_match_count','run_validity_match_count']:
            if summary[k] != summary['case_count']:
                failures.append(f"{k} {summary[k]} != case_count {summary['case_count']}")
    if args.require_no_leakage and summary['leakage_detected_count'] != 0:
        failures.append(f"leakage_detected_count {summary['leakage_detected_count']} != 0")
    if failures:
        raise SystemExit('blind-score-validation-failed: ' + '; '.join(failures))
if __name__=='__main__': main()
