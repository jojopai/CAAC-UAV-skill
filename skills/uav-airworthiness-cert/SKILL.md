---
name: uav-airworthiness-cert
description: Phase 1 of CAAC UAV airworthiness certification — decide the category and route, confirm eligibility and application timing, and hold the shared foundation (regulation corpus, citation traceability, requirement inventory, state ledger) used by all three phases. Use for 无人机适航取证入门 / 类别判定 / 取证路线 / 申请资格与时机 / 受理, and whenever a document's clause citations or timeline values must be traced to source text.
metadata:
  short-description: UAV airworthiness certification workflow and clause audit
---

# UAV Airworthiness Certification (CAAC)

Phase 1 of a three-skill family. This skill also holds the **shared foundation** —
the corpus, the citation map, the verifier scripts and the contracts — that
phases 2 and 3 call into.

| Skill | Phase | Covers |
| --- | --- | --- |
| **uav-airworthiness-cert** (this one) | ① 判定与准入 | 类别判定、取证路线、申请资格与时机、受理、过渡期；共享底座 |
| `uav-cert-compliance` | ② 符合性与体系 | 审定基础、符合性方法、DOA 设计保证系统、POA 生产质量系统、申报资料编写与完善、不符合项整改 |
| `uav-cert-sustain` | ③ 颁证与维持 | 颁证前置检查、适航证/特许飞行证、证后更改、监督、报告义务 |

Route to the phase the user is actually in. A request about writing a manual is
phase ②, not this one; a request about a post-certificate design change is phase ③.

The project's working assets live under the user's workspace:

| Asset | Role |
| --- | --- |
| `取证工作流程/` | The 1 master + 6 sub-processes. This is the procedure to follow, not to reinvent. |
| `适航审定程序源文件/` and `无人机法规与标准源文件/` | The regulation corpus (PDF). The only legitimate source of clause numbers. |
| `适航审定执行/` | Study notes and templates (运行场景说明书, 手册框架). |
| `.uav-cert-corpus/` | Extracted plain text + index, built by `scripts/build_corpus.py`. |

The process documents in the first three rows are generic templates; copies ship
with this skill set under `reference/` of the same repository, so a new project can
start from them or point at its own equivalents. Replace `<workspace>` with the
absolute path of the project you are working in.

Read the master process and the relevant sub-process before acting. If those files are absent, say so and work from the regulation corpus instead of inventing a procedure.

## Invariants

These override convenience. Each one exists because getting it wrong invalidates a submission.

1. **Every clause citation carries a document code and must be machine-checked.** Never cite a clause number from memory. Write citations in the form `<code> <clause>` (for example `P2 第3.9.1条`, `L2 第92.305(a)(5)条`), where codes are defined in [references/regulation-map.md](references/regulation-map.md). Run `scripts/verify_citations.py` before delivering; report every unresolved citation instead of quietly keeping it.
2. **Classify before anything else.** Until 最大起飞重量、是否载人、是否融合飞行、是否在人口密集区域上方飞行 are known, do not draft later-stage material. The weight threshold alone decides whether certification applies at all.
3. **Times and numbers are statutory values, not estimates.** Take them from source text. If a script cannot confirm one, mark it `待核实依据` rather than smoothing it over.
4. **Separate responsibilities.** Label each step 我方 or 局方. Never present a 局方 action (受理、审查、颁证、监督) as our deliverable.
5. **Never invent.** Missing facts become `待确认`, never a plausible value. A visible gap is always better than a confident guess.
6. **Audit before finalising, and re-audit after any repair.** Include a regression sweep, not just closure of the original findings. A round that closes one finding and opens two is a failed round and must be reported as such.
7. **No requirement may go un-dispositioned.** "Strictly follow the regulations" is only real if the requirement list comes from the text. Generate it with `scripts/extract_requirements.py`, then disposition every row as 适用 / 不适用+理由 / 由专用条件确定. An empty disposition cell is an open finding.
8. **One piece of evidence, many uses — register the reuse.** Before producing anything, check the ledger for an existing artifact that already covers the need. Record in the artifact which requirements it serves. Re-deriving a document that already exists is the main way this kind of project burns time.
9. **Track statutory deadlines in one ledger.** Every open item carries its deadline and its source clause. Long projects fail from losing state, not from lacking knowledge: keep `references/state-ledger.md` current, and surface anything due inside the next 10 working days at the start of a working session.

## Modes

Pick the mode from the request. Read only the references that mode needs.

| Mode | Use when | Read |
| --- | --- | --- |
| `classify` | 类别判定、取证路线、运行风险等级 | [references/regulation-map.md](references/regulation-map.md) |
| `qualify` | 申请资格、申请时机、过渡期、受理与缴费 | [references/regulation-map.md](references/regulation-map.md) |
| `requirements` | 生成或复核要求清单、逐条处置适用性 | [references/deliverables-matrix.md](references/deliverables-matrix.md) |
| `dossier` | 缺哪些资料、资料是否齐备、复用登记 | [references/deliverables-matrix.md](references/deliverables-matrix.md) |
| `ledger` | 进度、在办事项、法定截止日、待局方回复 | [references/state-ledger.md](references/state-ledger.md) |
| `review` | 复核流程/文件、条款溯源、跨文件一致性 | `scripts/` |

The certification-line modes (`type-cert`, `design-org`, `production-org`,
`airworthiness`, `post-cert`) now belong to phases ② and ③ — use
`uav-cert-compliance` and `uav-cert-sustain` for those, and keep this skill for
the foundation services they call.

Modes may chain, but never run a later mode as if classification were settled.

## Corpus setup

Build the searchable corpus once per machine before any clause work:

```bash
python3 scripts/build_corpus.py --src "<workspace>/适航审定程序源文件" --src "<workspace>/无人机法规与标准源文件" --out "<workspace>/.uav-cert-corpus"
```

It writes one text file per PDF plus `index.json`, and flags PDFs that yield almost no text as `needs OCR`. Never quote a clause from a `needs OCR` document without rendering and reading the page.

## Reviewing

Three checks, all mechanical, all required before you call a document reviewable.
Phases ② and ③ run these same commands against their own outputs.

```bash
python3 scripts/verify_citations.py --doc <file.md> --corpus "<workspace>/.uav-cert-corpus" --map references/regulation-map.md
python3 scripts/check_consistency.py --dir <folder> --expect <expectations file>
python3 scripts/extract_requirements.py --corpus "<workspace>/.uav-cert-corpus" --code P4 --out requirements-P4.md
```

`scripts/check_consistency.py` takes an expectations file; start from
`references/timeline-expectations.example.txt` and substitute your own file names.

Treat their output as evidence, not a verdict. They catch citations that do not
exist in the source, values that disagree across documents, and requirements with
no disposition; judgement about whether a cited clause actually governs the
situation stays with you. `extract_requirements.py` attributes a clause number on
a best-effort basis — the requirement text is verbatim, the clause label should be
confirmed before it is quoted in a submission.

Write findings into a review report with three sections: findings, corrections
made, and what you could not verify.

## Delegating

Use subagents when the work splits cleanly, and read [references/roles.md](references/roles.md) for role definitions and task templates.

- The main session owns every phase transition, the artifact directory, and the final deliverable. Subagents are leaves.
- Phases are sequential. Keep a **single fan-out point** per workflow; do not parallelise across phases.
- Put the **full absolute path** of every input and output in each subagent task. Subagents do not share the main session's memory of the run directory.
- Give each subagent the artifact contract it must fill. Do not give it the answer you expect.
- Statutory deadlines, not round counts, bound any repair loop.

## Confirmation gates

Ask the moment a gap changes feasibility or needs a human decision — do not bank questions for the final message. At most three questions at once, each as: question, why it matters, what you suggest. Record everything else in an open-items list.

Ask immediately when: classification parameters are unknown; a required clause cannot be traced; an inconsistency affects a statutory deadline; a document is missing for an in-flight review.

## Scope

This skill produces and audits internal deliverables and submission drafts. It never substitutes for a 局方 conclusion, and it does not decide airworthiness. When a question is genuinely for the authority, say so and frame it as a question to raise, rather than answering it ourselves.
