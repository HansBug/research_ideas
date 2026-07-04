#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, re
from pathlib import Path

ROOT=Path(__file__).resolve().parent
SCHEMA=ROOT.parents[3]/'experiment_design/protocols/better_adjudication_blind_output_schema_v0.json'

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

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--judge', required=True)
    ap.add_argument('--outputs-dir', default=None)
    args=ap.parse_args()
    oracle={c['blind_case_id']:c for c in load_json(ROOT/'oracle_answer_key.json')['cases']}
    outroot=Path(args.outputs_dir) if args.outputs_dir else ROOT/'judge_outputs'/args.judge
    rows=[]
    for bid, ans in sorted(oracle.items()):
        od=outroot/bid
        parsed_path=od/'parsed_output.json'
        raw_path=od/'raw_output.txt'
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
                obj=extract_json(raw_path.read_text(encoding='utf-8'))
                validate_schema(obj)
                status='valid_json_from_raw'
            except Exception as e:
                status='parse_error'; err=str(e)
        if obj:
            output_valid = status.startswith('valid_json')
            row={
                'blind_case_id':bid,
                'source_case_id':ans['source_case_id'],
                'judge_id':obj.get('judge_id'),
                'status':status,
                'schema_error': err,
                'expected_verdict':ans['primary_expected_verdict'],
                'observed_verdict':obj.get('primary_verdict'),
                'verdict_match': output_valid and obj.get('primary_verdict')==ans['primary_expected_verdict'],
                'expected_scope':ans['scope_routing_status'],
                'observed_scope':obj.get('scope_routing_status'),
                'scope_match': output_valid and obj.get('scope_routing_status')==ans['scope_routing_status'],
                'expected_run_validity':ans['run_validity_status'],
                'observed_run_validity':obj.get('run_validity_status'),
                'run_validity_match': output_valid and normalize_run_validity(obj.get('run_validity_status'))==normalize_run_validity(ans['run_validity_status']),
                'leakage_detected': obj.get('leakage_observation',{}).get('detected'),
                'confidence': obj.get('confidence'),
                'human_escalation_required': obj.get('human_escalation_required')
            }
        else:
            row={'blind_case_id':bid,'source_case_id':ans['source_case_id'],'status':status,'error':err,'expected_verdict':ans['primary_expected_verdict'],'verdict_match':False,'scope_match':False,'run_validity_match':False}
        rows.append(row)
    summary={
        'schema_version':'r5_7_5.blind_score_summary.v0',
        'judge':args.judge,
        'case_count':len(rows),
        'valid_output_count':sum(r['status'].startswith('valid_json') for r in rows),
        'verdict_match_count':sum(r.get('verdict_match') is True for r in rows),
        'scope_match_count':sum(r.get('scope_match') is True for r in rows),
        'run_validity_match_count':sum(r.get('run_validity_match') is True for r in rows),
        'leakage_detected_count':sum(r.get('leakage_detected') is True for r in rows),
        'rows':rows
    }
    (outroot/'score_summary.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(summary, ensure_ascii=False, indent=2))
if __name__=='__main__': main()
