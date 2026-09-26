# Nonconformity classification, deadlines and closure

Applies to DOA findings (P3 第5.3节) and POA findings (P4 第5.5节).
Classify first: the class determines the deadline.

## DOA findings

| Class | Meaning | Deadline |
| --- | --- | --- |
| 一类问题 | 可能导致失控状态并可能造成潜在不安全状态；以及书面要求 2 次以上仍不让局方接近设施、伪造文件证据、违规使用或冒用 DOA、未任命或任命不合格的责任经理 | 措施落实不超过 21 个工作日 |
| 二类问题 | 不属于一类问题的其他不符合项 | 措施落实不超过 3 个月，可提前申请延期 |
| 观察项 | 未达预期表现、可能导致一/二类问题的潜在情况、改进建议 | 沟通后记录在审定信函中 |

依据 P3 第5.3.2条。局方在审查后 5 个工作日内以审定信函告知，附不符合项记录表。
一类问题未按要求提交或落实的，局方可暂停体系权利；二类问题未落实的上升为一类问题。

## POA findings

| Class | Answer due | Corrective action |
| --- | --- | --- |
| 涉及安全 | 5 个工作日 | 20 个工作日，或局方要求的更短期限 |
| 系统性 — 严重 | 5 个工作日 | 一般不超过 3 个月 |
| 系统性 — 一般 | 20 个工作日 | 一般不超过 3 个月 |
| 孤立 | 30 个工作日 | — |

依据 P4 第5.5.2条。涉及安全的不符合项须立即消除不安全因素、立即停止相关产品的放行和交付，
必要时通报受影响的用户或运营人，并提供受影响清单。

## Closure is three things, not one

1. 纠正 — the specific item is fixed.
2. 纠正措施 — recurrence is prevented, addressed at root cause rather than symptom.
3. 回归检查 — the fix did not break something else.

The authority verifies and closes. Until then the item is open. For a POA finding that
is still open, and where the system cannot be shown to guarantee the airworthiness of
what is being produced, release and delivery are affected.

## Regression sweep, concretely

- Re-read the whole affected section, not only the corrected line.
- Compare against the previous version wherever the fix touched shared numbers, references or structure.
- Anything changed outside the stated scope is a regression until explained.
- Confirm cross-references still resolve, and that the manual still agrees with the procedure files and checklists.
- Report a failed round as failed: closing one finding while opening two is a failed round, not progress.

## Ledger

Use the nonconformity ledger shape in the phase-① contracts file, and put every deadline
into the state ledger the moment the finding is recorded. Record the dispatch date:
deadlines run from the authority's dispatch, not from when we noticed the finding.

## Answer content

The 纠正措施答复 is read by a reviewer, so it carries evidence rather than intention:

- the finding as classified, quoted from the record table
- what was done, with the objective evidence and where it lives
- root cause
- preventive effect and how it is verified
- completion date per item
- what remains open, if anything, and when it closes

Do not describe a fix that has not been made. A statement of intent in place of a
completed action is itself a finding.
