#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, subprocess, sys, os
from pathlib import Path
from datetime import datetime

ROOT=Path(__file__).resolve().parent
REPO=ROOT.parents[5]
PROMPT_TEMPLATE=REPO/'project_1_llm_state_machine_modeling/paper_stm_repair/experiment_design/protocols/better_adjudication_blind_prompt_v0.md'
SCHEMA=REPO/'project_1_llm_state_machine_modeling/paper_stm_repair/experiment_design/protocols/better_adjudication_blind_output_schema_v0.json'

def read(p): return Path(p).read_text(encoding='utf-8')
def load(p): return json.loads(read(p))

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

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--judge', required=True, choices=['codex','deepseek','claude'])
    ap.add_argument('--case', required=True)
    ap.add_argument('--timeout', type=int, default=600)
    args=ap.parse_args()
    judge_id={'codex':'codex-blind-judge','deepseek':'deepseek-blind-judge','claude':'claude-blind-judge'}[args.judge]
    od=ROOT/'judge_outputs'/judge_id/args.case
    od.mkdir(parents=True, exist_ok=True)
    prompt=build_prompt(args.case, judge_id)
    (od/'prompt.txt').write_text(prompt, encoding='utf-8')
    meta={'judge':args.judge,'judge_id':judge_id,'blind_case_id':args.case,'started_at':datetime.now().isoformat(timespec='seconds'),'schema_path':str(SCHEMA),'prompt_path':str(od/'prompt.txt')}
    (od/'run_meta_start.json').write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding='utf-8')
    env=os.environ.copy()
    if args.judge=='codex':
        cmd=['codex','exec','--ephemeral','--sandbox','read-only','-C',str(REPO),'--output-schema',str(SCHEMA),'-o',str(od/'last_message.txt'),'-']
    elif args.judge=='deepseek':
        cmd=['codex-deepseek','exec','--ephemeral','--sandbox','read-only','-C',str(REPO),'--output-schema',str(SCHEMA),'-o',str(od/'last_message.txt'),'-']
    else:
        # Claude JSON schema expects inline schema string.
        cmd=['claude','-p','--no-session-persistence','--bare','--model','sonnet','--json-schema',read(SCHEMA)]
    try:
        res=subprocess.run(cmd, input=prompt, text=True, cwd=REPO, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=args.timeout, env=env)
        rc=res.returncode
    except subprocess.TimeoutExpired as e:
        rc=124; res=e
    stdout=getattr(res,'stdout','') or ''
    stderr=getattr(res,'stderr','') or ''
    (od/'stdout.txt').write_text(stdout, encoding='utf-8')
    (od/'stderr.txt').write_text(stderr, encoding='utf-8')
    raw=''
    lm=od/'last_message.txt'
    last_message = lm.read_text(encoding='utf-8') if lm.exists() else ''
    if last_message.strip():
        raw=last_message
    elif stdout.strip():
        raw=stdout
    combined_for_parse='\n'.join([last_message, stdout, stderr])
    (od/'raw_output.txt').write_text(raw, encoding='utf-8')
    (od/'combined_output_for_parse.txt').write_text(combined_for_parse, encoding='utf-8')
    meta.update({'completed_at':datetime.now().isoformat(timespec='seconds'),'exit_code':rc})
    parse_error=None
    if raw.strip():
        try:
            obj=extract_json(combined_for_parse)
            # ensure judge id and blind id if model omitted/wrong? Do not correct, archive parsed as-is.
            (od/'parsed_output.json').write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding='utf-8')
        except Exception as exc:
            parse_error=str(exc)
    meta['parse_error']=parse_error
    (od/'run_meta_end.json').write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(meta, ensure_ascii=False, indent=2))
    raise SystemExit(0 if rc==0 and parse_error is None else 1)
if __name__=='__main__': main()
