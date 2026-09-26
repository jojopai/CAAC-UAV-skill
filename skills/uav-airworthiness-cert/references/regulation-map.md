# Regulation map

Document codes used in citations. `scripts/verify_citations.py` reads the block
below to resolve a code to a corpus document, so keep the names aligned with the
actual PDF file names on disk.

<!-- citation-map
L1: 无人驾驶航空器飞行管理暂行条例
L2: 民用无人驾驶航空器运行安全管理规则（CCAR-92部）
P1: 民用无人驾驶航空器系统适航审定管理程序（AP-21-AA-2022-71）
P2: 型号合格审定程序_AP-21-11R2
P3: 设计机构审定和监督程序_AP-21-18
P4: 生产机构审定和监督程序_AP-21-31R3
P5: 民用航空器国籍登记和民用无人驾驶航空器实名登记管理程序
P6: 民用无人驾驶航空器事件信息管理办法
P7: 基于计算机的民用无人驾驶航空器运行控制系统管理办法
A1: 民用无人驾驶航空器系统适航审定分级分类和系统安全性分析指南（AC-21-AA-2022-40）
A2: 限用类无人驾驶航空器系统适航标准
A3: 正常类多旋翼无人驾驶航空器系统（不载人）适航标准
A4: 正常类动力提升无人驾驶航空器系统（不载人）适航标准
A5: 中型民用无人驾驶航空器系统适航标准及符合性指导材料（试行）
A6: 民用无人驾驶航空器系统适航安全评定指南
SC1: 翼龙-2气象型无人驾驶航空器系统专用条件
-->

## What each document decides

| Code | Document | Decides |
| --- | --- | --- |
| L1 | 无人驾驶航空器飞行管理暂行条例 | Whether certification is required at all. 第八条: 中型、大型 need 适航许可; 微型、轻型、小型 do not. 第六十二条: the category weight/speed definitions. |
| L2 | CCAR-92部 运行安全管理规则 | The UAV airworthiness chapter. 92.301 scope, 92.305 procedure and division of authority, 92.307 risk-based principle, 92.311 48-hour reporting, 92.323 applicant's design assurance system, 92.325 application documents, 92.327 专用条件, 92.329 applicable requirements and 3-year application validity, 92.343 category definitions, 92.347/92.349 design change. |
| P1 | AP-21-71 (UAV-specific) | The UAV route: 1.4 general principles (which category), 1.5 scope, design approval flow, and Part 4 airworthiness approval (标准适航证 / 特殊适航证 / 特许飞行证 / 出口适航证). |
| P2 | AP-21-11R2 | Type certification procedure: five stages, application, 审定基础, CP/PSCP, MC0~MC9, risk-based retention, manufacturing conformity, TIA, ICA and flight manual approval, issue, post-certificate changes in ch.8, and 附录H simplified procedure. |
| P3 | AP-21-18 | Design organisation approval (DOA): class 1/2 by the 1360 kg line, application,审查 activities, 2-year validity, 设计保证系统 requirements (附录D), personnel qualification (附录C), continued supervision, nonconformity deadlines. |
| P4 | AP-21-31R3 | Production organisation approval (POA): applicant eligibility, 权益转让协议, two-stage review, QSAC (附录D 20 quality elements, 附录E 4 safety elements), CS release, surveillance, nonconformity deadlines, records. |
| P5 | 实名登记管理程序 | Registration is a precondition for applying for airworthiness approval. |
| P6 | 事件信息管理办法 | Event reporting obligations beyond the 48-hour defect report. |
| P7 | 运行控制系统管理办法 | Computer-based control system (cloud) requirements. |
| A1 | AC-21-40 | Severity class Ⅰ~Ⅳ from MTOW and kinetic energy; operating risk level A~G; this drives category selection. |
| A2 | AC-21-AA-2026-44 | The airworthiness standard most likely to become our 审定基础 for a 限用类 UAV: 基本要求, 通用测试科目 (link and ground-station tests included), 特定测试科目 by configuration. |
| A3 / A4 | 正常类 standards (uncrewed) | For a 正常类 route. |
| A5 / A6 | 中型 standard (trial) and safety-assessment guide | Earlier reference material; useful for comparison, check validity before relying on it. |
| SC1 | 翼龙-2 专用条件 | Reference sample for how a UAV 专用条件 is written and numbered. |

## Not in the corpus

| Document | Why it matters | Rule |
| --- | --- | --- |
| CCAR-21（民用航空产品和零部件合格审定规定） | The parent regulation all three programs are made under | We hold no text copy. **Do not cite a CCAR-21 clause number directly.** Cite it indirectly through P2/P3/P4, or obtain the text and add it to the corpus first. |
| AP-21-17 / AP-21-21（专用条件与豁免程序） | The procedure for issuing 专用条件 | Not held. Refer to it by name only. |
| AP-21-32（轻小型航空器生产许可及适航批准审定程序） | Superseded for production licensing by P4 | Refer by name when explaining a conflict; do not cite clauses. |

When a code resolves to a document flagged `needs OCR`, render the page and read
it before quoting. L1 (the 条例) is the known case: its published PDF is a scan.

## Known conflicts between documents

Record these rather than silently picking one. Current handling:

1. 符合性核查工程师 experience: P1 says 3 years, P3 附录C says 5 years → prepare to the stricter 5 years and ask the authority.
2. Design assurance system roles: P1 lists 责任经理/适航经理/CVE; P3 adds 安全经理（如适用）and 独立监督负责人 → follow P3.
3. 限用类 production approval basis: P1 points at AP-21-32; P4 has absorbed that content → follow P4.
4. 专用条件 procedure number: P1 cites AP-21-21; P2 cites AP-21-17 → follow P2.
5. Issuing decision window: L2 92.305(a)(5) counts 20 working days from acceptance; P2 §3.11 counts from the review report → quote L2 for the outward commitment and ask which applies.
