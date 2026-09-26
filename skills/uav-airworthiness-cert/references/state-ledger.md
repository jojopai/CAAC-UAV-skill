# State ledger

Certification runs for years, across authorities, reviewer changes and staff
turnover. What fails over that horizon is not knowledge, it is **state**: which
gate we are at, what is pending with the authority, and which statutory clock is
running. Keep one ledger per project, update it in the same session as the event,
and read it before starting work.

## Template

```markdown
# <项目名> 适航取证状态台账
更新日期：YYYY-MM-DD ｜ 维护人：

## 1 当前阶段与控制门
| 项 | 值 |
| --- | --- |
| 类别与路线 | 限用类 / 正常类 / 运输类（依据：…） |
| 当前阶段 | ① 判定 / ② 符合性与体系 / ③ 颁证与维持 |
| 当前控制门 | G1 / G2 / G3 / G4 / G5 / G6（见 01 总流程） |
| 三条线状态 | TC：；DOA：；POA： |
| 下一里程碑 | |

## 2 在办事项（按截止日排序）
| 事项 | 依据条款 | 法定/约定截止 | 剩余工作日 | 责任人 | 状态 |
| --- | --- | --- | --- | --- | --- |
| | | | | | |

## 3 待局方事项（不由我们决定）
| 事项 | 送出口 | 送出口期 | 局方口径/编号 | 等待天数 | 跟进动作 |
| --- | --- | --- | --- | --- | --- |

## 4 已提交资料
| 交付物 | 提交日期 | 接收方 | 受理/回执编号 | 状态 |
| --- | --- | --- | --- | --- |

## 5 复用登记
| 交付物 | 覆盖条款 | 被哪些事项引用 |
| --- | --- | --- |

## 6 未决问题
| 编号 | 问题 | 影响 | 需谁决定 | 提出日期 |
| --- | --- | --- | --- | --- |

## 7 风险与提醒
| 风险 | 触发条件 | 应对 | 复核日期 |
| --- | --- | --- | --- |
```

## Rules

1. **Every open item carries a deadline and a source clause.** An item without a
   clause is a preference, not an obligation — say which it is.
2. **Deadlines are counted from the authority's dispatch date**, not from when we
   noticed. Record the dispatch date in section 3.
3. **Surface what is due inside the next 10 working days** at the start of every
   working session, before doing anything else.
4. **Section 3 is the honest one.** Long waits are normal; what damages a project
   is an item that was sent to the authority and then forgotten. If a send-out has
   no response after 20 working days, that is itself a follow-up item.
5. **Record the authority's own words** for any interpretation, with the date and
   who said it. A verbal ruling that changes the route must be written down here
   or it will be re-litigated later.
6. **Update the reuse register whenever a document is reused**, so the next person
   can see which requirement a file already serves.

## Statutory deadlines worth pre-loading

Pre-fill these when the corresponding event happens; they are the ones that
expire fastest.

| 事件 | 时限 | 依据 |
| --- | --- | --- |
| 申请材料补正通知 | 收到申请后 5 个工作日内一次性书面通知 | L2 第92.305条 |
| 颁发合格证件的决定 | 受理之日起 20 个工作日内 | L2 第92.305条 |
| 型号合格审定总结报告、型号检查报告 | 颁证后 3 个月内 | P2 第3.12条; P2 第3.13条 |
| DOA 一类问题整改 | 不超过 21 个工作日 | P3 第5.3.2条 |
| DOA 二类问题整改 | 不超过 3 个月 | P3 第5.3.2条 |
| POA 涉及安全不符项答复 / 整改 | 5 个工作日 / 20 个工作日 | P4 第5.5.2条 |
| POA 严重、一般系统性不符项答复 | 5 / 20 个工作日 | P4 第5.5.2条 |
| POA 孤立不符项答复 | 30 个工作日 | P4 第5.5.2条 |
| 故障、失效、缺陷报告 | 确认后 48 小时内 | L2 第92.311条 |
| DOA 有效期延续申请 | 届满前至少 3 个月 | P3 第3.5条 |
| 供应商控制审查通知 | 提前 20 天 | P4 第5.2.3条 |
| 过渡期截止（DOA 取得、PC 转 POA） | 2027-07-01 | P2、P3、P4 附则 |
