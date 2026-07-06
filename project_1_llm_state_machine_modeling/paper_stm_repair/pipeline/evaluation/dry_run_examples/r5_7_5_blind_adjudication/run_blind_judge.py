#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, shutil, subprocess, sys, os, tempfile
from pathlib import Path
from datetime import datetime

ROOT=Path(__file__).resolve().parent
REPO=ROOT.parents[5]
PROMPT_TEMPLATE=REPO/'project_1_llm_state_machine_modeling/paper_stm_repair/experiment_design/protocols/better_adjudication_blind_prompt_v0.md'
SCHEMA=REPO/'project_1_llm_state_machine_modeling/paper_stm_repair/experiment_design/protocols/better_adjudication_blind_output_schema_v0.json'

def read(p): return Path(p).read_text(encoding='utf-8')
def load(p): return json.loads(read(p))
def sha256_text(text:str)->str: return hashlib.sha256(text.encode('utf-8')).hexdigest()
def validate_schema(obj):
    try:
        import jsonschema  # type: ignore
    except Exception as exc:
        raise RuntimeError(f'jsonschema is required for blind judge output validation: {exc}')
    jsonschema.validate(obj, load(SCHEMA))
def resolve_bin(name:str)->str:
    path=shutil.which(name)
    if not path:
        raise SystemExit(f"required CLI not found on PATH: {name}")
    return path

def build_prompt(bid:str, judge_id:str)->str:
    inpdir=ROOT/'blind_inputs'/bid
    packet=load(inpdir/'input_packet.json')
    return f"""{read(PROMPT_TEMPLATE)}

# Blind case input

judge_id: {judge_id}
blind_case_id: {bid}

## input_packet.json
```json
{json.dumps(packet, ensure_ascii=False, indent=2)}
```

## NL
```text
{read(inpdir/'nl.txt')}
```

## raw STM_0
```plantuml
{read(inpdir/'raw_stm0.plantuml')}
```

## canonical STM_0
```fcstm
{read(inpdir/'canonical_stm0.fcstm')}
```

## candidate STM_k
```fcstm
{read(inpdir/'candidate_stmk.fcstm')}
```

请只输出 JSON。不要访问任何其他文件。不要使用 PR comment 或上下文记忆。不要猜测隐藏 answer key。
"""

def extract_json(text:str):
    text=text.strip()
    dec=json.JSONDecoder()
    candidates=[]
    for i,ch in enumerate(text):
        if ch!='{':
            continue
        try:
            obj,end=dec.raw_decode(text[i:])
        except Exception:
            continue
        if isinstance(obj, dict):
            candidates.append(obj)
    for obj in reversed(candidates):
        if obj.get('schema_version') == 'r5_7_5.better_adjudication_blind_output.v0':
            return obj
    if candidates:
        return candidates[-1]
    raise ValueError('no JSON object found')

def extract_identity_json(text:str, *, blind_case_id:str, judge_id:str):
    """Extract only an actual judge output object from a CLI transcript.

    Codex-family CLIs may print a transcript to stderr and write a later
    natural-language summary to last_message.txt even when an earlier assistant
    turn satisfied the JSON schema.  Blind safety still forbids parsing arbitrary
    prompt echo.  This fallback therefore accepts only JSON objects that carry
    the exact output schema version plus the exact blind_case_id and judge_id.
    The prompt skeleton uses placeholder values, and blind input packets do not
    contain this output schema version, so prompt echo is rejected.
    """
    dec=json.JSONDecoder()
    matches=[]
    for i,ch in enumerate(text):
        if ch!='{':
            continue
        try:
            obj,end=dec.raw_decode(text[i:])
        except Exception:
            continue
        if not isinstance(obj, dict):
            continue
        if (
            obj.get('schema_version') == 'r5_7_5.better_adjudication_blind_output.v0'
            and obj.get('blind_case_id') == blind_case_id
            and obj.get('judge_id') == judge_id
        ):
            matches.append(obj)
    if matches:
        return matches[-1]
    raise ValueError('no identity-matching judge JSON object found in combined transcript')

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--judge', required=True, choices=['codex','deepseek','claude'])
    ap.add_argument('--case', required=True)
    ap.add_argument('--timeout', type=int, default=600)
    args=ap.parse_args()
    judge_id={'codex':'codex-blind-judge','deepseek':'deepseek-blind-judge','claude':'claude-blind-judge'}[args.judge]
    od=ROOT/'judge_outputs'/judge_id/args.case
    od.mkdir(parents=True, exist_ok=True)
    for name in ['last_message.txt','stdout.txt','stderr.txt','raw_output.txt','combined_output_for_parse.txt','parsed_output.json','parsed_output.invalid.json','run_meta_start.json','run_meta_end.json']:
        old=od/name
        if old.exists():
            old.unlink()
    prompt=build_prompt(args.case, judge_id)
    (od/'prompt.txt').write_text(prompt, encoding='utf-8')
    env=os.environ.copy()
    isolated_dir=Path(tempfile.mkdtemp(prefix=f'r575_{judge_id}_{args.case}_'))
    isolated_prompt=isolated_dir/'prompt.txt'
    isolated_schema=isolated_dir/'output_schema.json'
    isolated_last_message=isolated_dir/'last_message.txt'
    isolated_prompt.write_text(prompt, encoding='utf-8')
    isolated_schema.write_text(read(SCHEMA), encoding='utf-8')
    cli_output_schema_mode='provider_cli_structured_output'
    if args.judge=='codex':
        exe=resolve_bin('codex')
        codex_cli_output_schema=os.environ.get('R575_CODEX_CLI_OUTPUT_SCHEMA', '0').strip().lower() not in {'0','false','no','off','local','none'}
        cmd=[exe,'exec','--ephemeral','--skip-git-repo-check','--ignore-rules','--sandbox','read-only','-C',str(isolated_dir),'-o',str(isolated_last_message),'-']
        if codex_cli_output_schema:
            cmd[cmd.index('-o'):cmd.index('-o')]=['--output-schema', str(isolated_schema)]
        else:
            cli_output_schema_mode='local_jsonschema_validation_no_cli_output_schema'
        codex_provider=os.environ.get('R575_CODEX_MODEL_PROVIDER')
        if codex_provider:
            cmd[1:1]=['-c', f'model_provider="{codex_provider}"']
        codex_model=os.environ.get('R575_CODEX_MODEL')
        if codex_model:
            cmd[1:1]=['--model', codex_model]
        codex_reasoning_effort=os.environ.get('R575_CODEX_REASONING_EFFORT')
        if codex_reasoning_effort:
            cmd[1:1]=['-c', f'model_reasoning_effort="{codex_reasoning_effort}"']
        archived_cmd=cmd
    elif args.judge=='deepseek':
        exe=resolve_bin('codex-deepseek')
        cmd=[exe,'exec','--ephemeral','--skip-git-repo-check','--ignore-rules','--sandbox','read-only','-C',str(isolated_dir),'--output-schema',str(isolated_schema),'-o',str(isolated_last_message),'-']
        archived_cmd=cmd
    else:
        # Claude JSON schema expects inline schema string.  Run in an out-of-repo
        # cwd so any accidental tool/file access cannot see oracle or PR context.
        exe=resolve_bin('claude')
        cmd=[exe,'-p','--no-session-persistence','--bare','--model','sonnet','--json-schema',read(SCHEMA)]
        archived_cmd=[exe,'-p','--no-session-persistence','--bare','--model','sonnet','--json-schema',f'<schema-content-redacted; see {SCHEMA}>']
    meta={'judge':args.judge,'judge_id':judge_id,'blind_case_id':args.case,'started_at':datetime.now().isoformat(timespec='seconds'),'schema_path':str(SCHEMA),'prompt_path':str(od/'prompt.txt'),'prompt_sha256':sha256_text(prompt),'protocol_prompt_template_sha256':sha256_text(read(PROMPT_TEMPLATE)),'cwd':str(isolated_dir),'isolated_run_dir':str(isolated_dir),'isolated_prompt_path':str(isolated_prompt),'isolated_schema_path':str(isolated_schema),'cli_output_schema_mode':cli_output_schema_mode,'timeout_seconds':args.timeout,'command_argv_archived':archived_cmd,'context_isolation_claim':'fresh external CLI subprocess with no session persistence where supported; process cwd is an out-of-repository temporary directory containing only prompt.txt and output_schema.json; oracle_answer_key.json, PR comments, score summaries, and repository files are not present in the run cwd; the only adjudication context is prompt.txt via stdin; when cli_output_schema_mode is local_jsonschema_validation_no_cli_output_schema, the provider CLI is not asked to enforce structured output but the archived last_message/stdout is still parsed and validated against isolated_schema_path before becoming eligible'}
    (od/'run_meta_start.json').write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding='utf-8')
    try:
        res=subprocess.run(cmd, input=prompt, text=True, cwd=isolated_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=args.timeout, env=env)
        rc=res.returncode
    except subprocess.TimeoutExpired as e:
        rc=124; res=e
    stdout=getattr(res,'stdout','') or ''
    stderr=getattr(res,'stderr','') or ''
    (od/'stdout.txt').write_text(stdout, encoding='utf-8')
    (od/'stderr.txt').write_text(stderr, encoding='utf-8')
    if isolated_last_message.exists():
        shutil.copy2(isolated_last_message, od/'last_message.txt')
    raw=''
    lm=od/'last_message.txt'
    last_message = lm.read_text(encoding='utf-8') if lm.exists() else ''
    if last_message.strip():
        raw=last_message
    elif stdout.strip():
        raw=stdout
    combined_for_parse='\n'.join([last_message, stdout, stderr])
    # Important blind-safety rule: stderr often contains CLI transcript / prompt echo.
    # The normal parse path is last_message/stdout only.  A combined transcript
    # fallback is allowed below only when it contains an exact schema-version +
    # blind_case_id + judge_id matching JSON object; otherwise the combined
    # transcript remains audit-only.
    (od/'raw_output.txt').write_text(raw, encoding='utf-8')
    (od/'combined_output_for_parse.txt').write_text(combined_for_parse, encoding='utf-8')
    meta.update({'completed_at':datetime.now().isoformat(timespec='seconds'),'exit_code':rc})
    parse_error=None
    schema_error=None
    parse_source=None
    if raw.strip():
        try:
            obj=extract_json(raw)
            validate_schema(obj)
            parse_source='raw_output'
            # ensure judge id and blind id if model omitted/wrong? Do not correct, archive parsed as-is.
            (od/'parsed_output.json').write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding='utf-8')
        except Exception as exc:
            parse_error=str(exc)
            try:
                obj=extract_json(raw)
                (od/'parsed_output.invalid.json').write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding='utf-8')
                schema_error=str(exc)
            except Exception:
                pass
    else:
        parse_error='no model output in last_message/stdout; stderr/combined transcript intentionally not parsed'
    if parse_error is not None:
        try:
            obj=extract_identity_json(combined_for_parse, blind_case_id=args.case, judge_id=judge_id)
            validate_schema(obj)
            parse_source='combined_transcript_identity_fallback'
            parse_error=None
            schema_error=None
            (od/'parsed_output.json').write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding='utf-8')
        except Exception:
            # Preserve the original parse_error.  combined transcript remains
            # audit-only unless it contains an exact identity-matching JSON
            # output object.
            pass
    meta['parse_error']=parse_error
    meta['schema_error']=schema_error
    meta['parse_source']=parse_source
    meta['provider_or_cli_nonzero_with_parsed_output'] = bool(rc != 0 and parse_error is None and (od/'parsed_output.json').exists())
    (od/'run_meta_end.json').write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(meta, ensure_ascii=False, indent=2))
    raise SystemExit(0 if rc==0 and parse_error is None else 1)
if __name__=='__main__': main()
