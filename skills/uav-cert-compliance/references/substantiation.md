# Substantiation: 审定基础 and 符合性

Phase-① codes apply. Cite as `CODE 条款`.

## 审定基础 — establish it before planning any test

| Component | Requirement source | Note |
| --- | --- | --- |
| 适用适航标准与环境保护要求 | L2 第92.329条(a)(1); P1 第3.6条 | 首次申请取申请之日有效版次 |
| 专用条件 | L2 第92.327条; P2 第3.7.2条 | 无现成标准或标准不覆盖时以此确定 |
| 等效安全水平结论 ELOS | P2 第3.7.4条 | 补偿措施等效时使用 |
| 豁免 | L2 第92.309条; P2 第3.7.5条 | 因技术原因 |

For a 限用类 UAV the sequence is fixed: 运行场景 → 运行风险 → 对已颁布标准的适用性评估
→ 增加遥控台（站）与数据链要求 → 以专用条件固化。依据 P1 第3.6条 与 L2 第92.327条(b)。
This is why the 运行场景说明书 is drafted before the 符合性计划.

## 审定计划 / 符合性计划表

Required content per P2 第3.8.1条: 项目与预期运行类别说明、建议的审定基础、符合性方法说明、
逐条款的符合性检查单、责任人、含重大里程碑的进度计划。

限用类 may use the simplified 符合性计划表 of P2 附录H 第3.2条。Per clause it also needs
局方审查方式（资料审查 / 局方参与）、符合性文件编号与版次、提交时间计划、双方责任人。

## 符合性方法

MC0~MC9 as defined in P2 第3.8.2条 and P1 第3.7.2条。

Two rules that are easy to get wrong:

- A new method is not invented by us; it is agreed with the review team and recorded in a 问题纪要。
- 局方只批准分析的结果数据，不批准分析用的手段，所以分析报告必须证明数据有效性，而不只是给出数字。依据 P2 第3.9.3条。

## Evidence chain per verification activity

```
试验大纲（11 项内容）—批准（型号资料批准表）—┐
                                             ▼
试验产品 100% 制造符合性确认 — 制造符合性声明 — 局方检查（制造符合性检查记录表）
                                             │
                                             ▼
        目击（试验观察问题记录单 / 试验观察报告）—► 试验报告（属符合性报告）
```

Skipping any link invalidates the evidence. The two links skipped most often:

- 制造符合性声明必须在局方检查**之前**提交，依据 P2 第3.9.1条(3)。
- 自提交声明的时点到开展试验的期间，不得对试验产品做影响声明有效性的更改。

## Risk-based 审查范围

We propose the 符合性表明项目 CDI split and the risk grading; the review team decides
the retention, 依据 P2 第5.1条。Useful consequence: 申请人能力评价越高、局方保留项目越少。
DOA maturity and CVE work records therefore reduce later verification effort directly,
which is a reason to build the system early rather than only for compliance.

## Flight test chain

| Step | Requirement |
| --- | --- |
| 研发与检查飞行试验 | 先取得试验类特许飞行证，依据 P2 第3.9.4条 与 P1 第5条 |
| 审定飞行试验 | 只有签发 TIA 后才能开始，依据 P2 第3.9.11条 |
| 限用类 | 可不开展局方审定飞行试验，依据 P2 附录H |
| 功能与可靠性试飞 | 限用类可免除，依据 P2 附录H 第3.4条 |

## Documents approved before the certificate is issued

| Document | Requirement |
| --- | --- |
| 适航性限制要求 ALI/CMR、SRM、EWIS ICA、WBM | P2 第3.9.14条; P1 第3.9.7条 |
| 民用无人驾驶航空器系统飞行手册 | P2 第3.9.16条; P1 第3.9.8条 |

The flight manual limitations section must include 运行场景限制（人口密集程度、隔离飞行）、
C2 链路使用限制与操作程序、遥控台（站）使用限制。缺这三项的飞行手册会被退回。
