# Artifact contracts

Pin the shape before the work starts. A subagent that receives a shape fills it;
a subagent that receives only a topic invents a structure and the result cannot
be diffed or audited. Every artifact below carries a `待确认` list — an artifact
with an empty list is suspicious, not perfect.

Write paths: put one run directory per project and pass its **absolute** path in
every subagent task.

## Classification report (`classify` mode)

Markdown, one file: `取证类别与路线判定报告.md`

| Field | Rule |
| --- | --- |
| 最大起飞重量 / 构型 / 最大使用限制速度 | Our data only. If unknown → `待确认`, stop. |
| 计算动能 | Show the calculation, cite the A1 §7.1 thresholds. |
| 危害严重性级别 Ⅰ~Ⅳ | Derived from the row above; state which threshold decided it. |
| 是否载人 / 是否融合飞行 / 是否在人口密集区域上方飞行 | Three separate answers, each with its evidence. |
| 运行风险等级 A~G | From the A1 §7.3 table; quote the cell used. |
| 结论类别 | 限用类 / 正常类 / 运输类, with the clause that decides it (P1 §1.4, L2 §92.343). |
| 建议取证路线 | TC + DOA + POA + which airworthiness certificate. |
| 待确认 | Everything that could flip the answer, ranked by how much it matters. |

## 审定基础 table (`type-cert` mode)

One row per applicable requirement. This table is the contract for the whole
certification project, so never leave a row without a source.

| 条款号 | 条款标题/摘要 | 来源 | 符合性方法 (MC0~MC9) | 符合性文件 | 局方审查方式 | 责任人 |
| --- | --- | --- | --- | --- | --- | --- |

- `来源` is either a standard clause (`A2 2.2.4`) or `专用条件（待制定）`.
- 符合性方法 must be one of MC0~MC9; an unfamiliar need becomes a question to
  raise, not a new code.
- 局方审查方式 is `资料审查` or `局方参与` (P2 附录H §3.2).

## Compliance checklist

Same as 审定基础 but with the closing fields added:

| 条款号 | 要求摘要 | 符合性文件编号及版次 | 提交时间计划 | 状态 | 证据位置 |
| --- | --- | --- | --- | --- | --- |

Allowed 状态 values only: `未开始` / `进行中` / `已提交` / `待局方确认` / `已关闭`.
`已关闭` requires a 证据位置.

## 问题纪要 ledger (`type-cert` mode)

| 编号 | 类型 (MC / ELOS / SC / 豁免 / G-1 / G-2 / G-3 / 不安全特征 / 其他) | 问题说明 | 审查组立场 | 申请人立场 | 结论 | 阶段 (1~4) | 状态 |
| --- | --- | --- | --- | --- | --- | --- | --- |

Nothing is delivered while any item is open: 颁证前所有问题纪要必须关闭 (P2 §3.10(3)).

## Nonconformity ledger (`design-org` / `production-org` / `post-cert`)

| 编号 | 发现活动 | 描述 | 客观证据 | 分类 | 答复时限 | 整改完成时限 | 答复文件 | 状态 | 回归检查 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

- 分类 for DOA: 一类问题 (21 个工作日) / 二类问题 (3 个月) / 观察项 — P3 §5.3.2.
- 分类 for POA: 涉及安全 (5 个工作日答复, 20 个工作日整改) / 严重系统性 (5 个工作日) / 一般系统性 (20 个工作日) / 孤立 (30 个工作日) — P4 §5.5.2.
- `回归检查` records whether the fix broke something else. Leave it blank only
  before the re-check runs — an empty regression column after a repair is a
  finding, not a pass.

## Review report (`review` mode)

One file with exactly these three sections, in this order:

1. **核对结果** — per check: what was checked, the command run, the count of
   items, hits and misses. Include the misses even when later explained.
2. **已修正的问题** — what was wrong, severity, what changed. A review that
   corrected nothing is possible, but say so explicitly rather than leaving the
   section out.
3. **无法核实的项** — what could not be verified and why (missing text layer,
   absent document, undetermined product parameter). Never let an unverifiable
   item quietly become an assumption.

Plus a short closing line stating whether the document passed, and any item that
must be confirmed by the authority.

## Design assurance / quality manuals (`design-org` / `production-org`)

Use the structure already prepared in the workspace rather than inventing one:
`适航审定执行/06_设计保证手册与质量手册框架.md`. The contract here is coverage:
every element in P3 附录D (DOA) or P4 附录D/E (POA) must map to a chapter, and the
mapping is itself an artifact.

| 要求来源 | 要求编号/名称 | 手册章节 | 程序文件编号 | 状态 |
| --- | --- | --- | --- | --- |

## Run directory

```
<run dir>/
|-- 00_brief.json                 project parameters, unknowns listed explicitly
|-- 01_classification.md          classify mode
|-- 02_审定基础.md                  type-cert mode
|-- 03_符合性检查清单.md
|-- 04_问题纪要台账.md
|-- 05_不符合项台账.md              DOA / POA / post-cert
|-- 06_review_report.md           review mode
`-- sources.md                    absolute paths of every input used
```

`sources.md` exists so a later reviewer can tell which corpus build a document
was written against. Update it whenever the corpus is rebuilt.
