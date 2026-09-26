# The two organisation systems

The chapter structures already prepared for this project are authoritative in this workspace:

| Manual | Blueprint |
| --- | --- |
| 设计保证手册 | `<workspace>/适航审定执行/06_设计保证手册与质量手册框架.md` |
| 质量手册 | same file, second half |

Do not invent an alternative structure. Use these blueprints and check coverage
against the clauses below.

## DOA — what must be covered

依据 P3 附录D。

| Requirement | Where it lands |
| --- | --- |
| 责任经理及任命（适航经理、安全经理如适用、独立监督负责人） | 组织与职责章 |
| 独立监督职能对设计及适航职能的独立性 | 独立监督章；组织架构图须能看出这一点 |
| 一类系统：设计保证要素 + 完整安全管理要素 | 安全管理章 |
| 二类系统：5 类程序（取证流程、变更管理、持有责任、供应商控制、事件报告与资料保存） | 对应各章 |
| 手册须描述组织架构、政策流程程序、设计活动类型、许可项目单覆盖的产品与零部件类别、设计供应商接口与管控 | 总则与各章 |
| 开展试飞则须编制试飞管理手册 | 单独手册 |
| 管理人员资历和经验声明 | 提交件 |
| DOA 符合性检查单 | P3 附录E |

人员资质见 P3 附录C。当 P1 与 P3 的年限要求不一致时，按更严的一侧准备并向局方确认。

## POA — what must be covered

依据 P4 第5.1.3条 与 P4 附录D、附录E。

质量手册必备内容（十项）：

1. 责任经理声明，承诺持续符合包括质量手册在内的所有生产质量系统文件要求
2. 高级管理人员授权书，载明姓名、职务、职责、权限、与局方联络授权
3. 生产质量系统组织机构图及部门职责
4. 人力资源概况
5. 生产设施概况
6. 与生产机构许可项目单相关的工作范围说明
7. 生产质量系统及其文件的更改管理
8. 生产质量系统要素的管理要求
9. 授权的 CS 名单及管理要求
10. 与民用航空规章适用条款的符合性索引或矩阵图

Two structural requirements the reviewer tests first:

- 组织机构的设置应保证质量部门能够独立并不受干扰地开展工作。
- 手册应包括收集、调查和分析事件报告的要求，以识别不良趋势。

QSAC coverage: 20 项质量要素见 P4 附录D，4 项安全要素见 P4 附录E。
对限用类无人机，局方可只选取必要且适用的审查准则，见 P4 附录D 第1条。这一点应当先问，不要默认全套。

## Procedure-file set

The numbered procedure list (D-01~D-23 for DOA, P-01~P-33 for POA, plus eight shared
procedures) is in the workspace blueprint. Build the shared ones once and reference
them from both manuals: it halves the drafting and removes a class of inconsistency
between the two systems.

## Cross-checks that catch most problems

| Check | Why |
| --- | --- |
| 手册条款与 DOA 符合性检查单逐条对应 | 检查单就是审查员的脚本 |
| 手册引用的程序文件在清单中都存在且版次一致 | 悬空引用是最常见的退回原因 |
| 组织架构图与职责分配矩阵一致 | 独立性靠这两张图证明 |
| CVE / CS 名单与授权文件、培训记录一致 | 人员资质是最容易超期的项 |
| 手册内的时限与法规时限一致 | 用 check_consistency.py 核对 |
