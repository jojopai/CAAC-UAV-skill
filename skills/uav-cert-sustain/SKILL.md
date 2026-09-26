---
name: uav-cert-sustain
description: Phase 3 of CAAC UAV airworthiness certification — the certificate issue gate, per-aircraft airworthiness approval (标准适航证 / 特殊适航证 / 特许飞行证 / 出口适航证), delivery release, and post-certificate sustainment (设计更改, surveillance, certificate validity, reporting duties). Use for 颁证前置检查 / 适航证申请 / 特许飞行证 / 制造符合性声明 / 批准放行证书 / 设计更改批准 / 证后监督 / 证件有效期 / 48 小时报告 requests.
metadata:
  short-description: UAV certificate issue, airworthiness approval and sustainment
---

# Phase ③ — Issue and Sustain

Two jobs with different rhythms: pass the issue gate once, then keep the
certificates and the airworthiness of each delivered aircraft valid for years.

## Foundation

Phase ① holds the shared assets. Its invariants apply here unchanged: clauses cited
by code and machine-checked, unknown values `待确认`, 局方 actions never presented as
ours, deadlines tracked in one ledger.

| Asset | Path |
| --- | --- |
| Rules, contracts, scripts | `~/.agents/skills/uav-airworthiness-cert/` |
| Regulation corpus | `<workspace>/.uav-cert-corpus/` |
| State ledger template | `.../uav-airworthiness-cert/references/state-ledger.md` |

If that path is missing, say so and stop rather than improvising.

## Modes

| Mode | Use when | Read |
| --- | --- | --- |
| `issue-gate` | 颁证前自查：TC / DOA / POA 颁证条件是否齐备 | [references/issue-gate.md](references/issue-gate.md) |
| `airworthiness` | 适航证、特殊适航证、特许飞行证、出口适航证 | [references/airworthiness-approval.md](references/airworthiness-approval.md) |
| `delivery` | 逐架机放行：制造符合性声明、批准放行证书 | [references/airworthiness-approval.md](references/airworthiness-approval.md) |
| `post-cert` | 设计更改、修理设计、监督配合、报告义务、证件有效期 | [references/post-cert-surveillance.md](references/post-cert-surveillance.md) |

## The issue gate — why this phase decides the pass rate

Almost every avoidable failure at this point is one of five things. Check all five
explicitly, in writing, before submitting:

1. **问题纪要没有全部关闭** — nothing is issued while any item is open; 依据 P2 第3.10条(3)。
2. **符合性检查清单没有逐条落实** — every applicable clause needs a disposition and a
   document; 依据 P2 第3.10条(2)。
3. **前置证件未取得** — TC 颁发以取得相应 DOA 为前提，依据 P2 第3.11条。生产交付以 POA 为前提。
4. **手册批准状态未确认** — 持续适航文件与飞行手册须在颁证前批准或已提交完成计划，
   依据 P2 第3.9.14条 与 P2 第3.9.16条。
5. **引用与数字不一致** — run the phase-① verifiers; a submission that contradicts
   itself invites a second review round, which costs more time than the check.

## Per-aircraft discipline

Airworthiness approval repeats for every aircraft, so make it a procedure rather
than an event:

- 登记先行: 申请适航批准前须完成实名登记或国籍登记，依据 P1 第四部分第3节(1) 与 P5。
- 交付航空器提交航空器制造符合性声明，须做实物检查并由责任经理或其授权人签署，依据 P4 第3.5条(2)。
- 交付发动机、螺旋桨、零部件、遥控台（站）由授权的 CS 签发批准放行证书，依据 P4 第3.5条(3)。
- 限用类的三条禁止随证生效：不得载人、不得融合飞行、不得在人口密集区域上方飞行，
  依据 P1 第4.2条。运行管控文件必须与此一致。

## Sustainment

The two ways a certificate is lost are forgetting a validity date and forgetting a
change reporting duty. Keep both in the state ledger:

| Item | Rule |
| --- | --- |
| DOA 有效期 | 2 年；届满前至少 3 个月提交延续申请；失效后再申请视为初次申请，依据 P3 第3.5条 |
| POA | 长期有效，但须持续符合 CCAR-21 适用要求并接受检查，依据 P4 第3.6条 |
| 生产状态 | 由活跃转非活跃应书面报告 PI；转回活跃须接受生产质量系统复查，依据 P4 第4.3.1条 |
| 故障、失效、缺陷报告 | 确认后 48 小时内，依据 L2 第92.311条 |
| 记录保存 | DOA 审查记录不少于 7 个日历年；POA 不少于 15 个日历年 |

## Escalation

Ask the user at most three questions when a gap changes whether we can issue or
deliver. Ask the authority — not the user, not the model — when two documents
conflict, a clause cannot be traced, or an interpretation changes a submission.
Frame those as questions with the conflicting citations attached.
