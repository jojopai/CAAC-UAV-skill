---
name: uav-cert-compliance
description: Phase 2 of CAAC UAV airworthiness certification — build the substantiation and the organisation systems (审定基础, 符合性方法, 设计保证系统 DOA, 生产质量系统 POA), the manuals and procedures behind them, and the closure of nonconformities. Use for 审定基础 / 符合性方法 / 试验大纲 / 设计保证手册 / 质量手册 / DOA / POA / QSAC / 不符合项整改 / 申报资料编写与完善 requests.
metadata:
  short-description: UAV certification substantiation, systems and manuals
---

# Phase ② — Compliance and Systems

Turn the route decided in phase ① into evidence the authority can accept, and into
the two organisation systems that let us keep producing that evidence ourselves.

## Foundation

Phase ① holds the shared assets. Read its instructions once, then call its scripts
by absolute path:

| Asset | Path |
| --- | --- |
| Rules, invariants, contracts, roles | `~/.agents/skills/uav-airworthiness-cert/` |
| Regulation corpus | `<workspace>/.uav-cert-corpus/` |
| Citation map, deliverables matrix, state ledger | `.../uav-airworthiness-cert/references/` |

If that path is missing, say so and stop — do not improvise a replacement corpus
or map. Every phase-① invariant still applies here, in particular: clauses are
cited by code and machine-checked, unknown values become `待确认`, and 局方 actions
are never presented as our deliverables.

## Modes

| Mode | Use when | Read |
| --- | --- | --- |
| `type-cert` | 审定基础、符合性方法 MC0~MC9、试验大纲、TIA、ICA/飞行手册 | [references/substantiation.md](references/substantiation.md) |
| `design-org` | DOA、设计保证手册、独立监督、符合性核查工程师 | [references/manual-blueprints.md](references/manual-blueprints.md) |
| `production-org` | POA、质量手册、QSAC、生产放行人员、权益转让协议 | [references/manual-blueprints.md](references/manual-blueprints.md) |
| `nonconformity` | 审查发现的不符合项、分类、整改、验证关闭 | [references/nonconformity-and-closure.md](references/nonconformity-and-closure.md) |
| `draft` | 起草或完善任一申报资料 | `<workspace>/适航审定执行/06_设计保证手册与质量手册框架.md`; deliverables matrix in the phase-① skill |

## How to do the work

1. **Gap analysis first.** Before drafting anything, run the gap analysis in the
   deliverables matrix. Most "we need a document" requests turn out to be "an
   existing document is missing three fields".
2. **Requirements, not memory.** Generate the requirement list with
   `extract_requirements.py` and disposition every row. A system that satisfies
   the chapters we happened to remember is not a system that satisfies the regulation.
3. **One artifact, many clauses.** Record which requirements each document serves
   in the reuse register. Re-deriving is the waste this phase is most prone to.
4. **Prefer the authority's own checklist.** P3 附录E (DOA 符合性检查单), P4 附录F
   (符合性检查清单) and the 符合性检查清单 of P2 are the closest thing to the
   reviewer's script. Self-assess against them, not against a summary of them.
5. **Machines check, humans decide.** Run the phase-① verifiers on every artifact
   you produce. Fix what they find; keep what they cannot decide for review.

## Nonconformity discipline

Applies here for initial review, and in phase ③ for surveillance findings.

- Classify before acting: the class fixes the deadline, not the other way round.
- A fix is not closed until the correction **and** its preventive effect are
  verified, and a regression sweep has been run on the affected area.
- A round that closes one finding and opens two is a failed round; report it as
  failed rather than looping.
- Deadlines come from the regulation text. Put them in the state ledger the moment
  the finding is recorded.

## Writing rules for anything submitted

- Chinese, formal, no marketing language.
- 每份文件写清 依据条款、编制/审核/批准、版次与日期；表格使用规定的附表编号。
- Do not state a number (time limit, threshold, mass, speed) that the corpus does
  not support. Mark it `待核实依据` instead.
- Anything published outside the company and approved under the DOA carries the
  statement required by P3 第7.2条(7).
- Sanitise before sharing externally: strip absolute paths, internal identifiers,
  supplier names not needed for the submission, and any real customer data.

## Outputs

Artifacts follow the contracts defined in the phase-① skill. Keep one run
directory with absolute paths, and register every artifact in the state ledger so
phase ③ can find it.
