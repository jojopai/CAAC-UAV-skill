# Roles and delegation

The main session orchestrates. Subagents are leaves: they produce one artifact,
report, and stop. Keep one fan-out point per workflow and never parallelise
across phases — each phase consumes the previous phase's artifact.

## Choosing a role

| Role | Job | Suggested effort | Produces |
| --- | --- | --- | --- |
| `classifier` | Turn product parameters into a category and route | high | 取证类别与路线判定报告 |
| `clause-scout` | Locate the clauses that govern a described situation, from the corpus only | medium | clause list with source codes |
| `drafter` | Write one artifact against its contract | high | the artifact |
| `compliance-auditor` | Audit a draft against the regulation and the contract | medium | review report |
| `mechanical-verifier` | Run the scripts, report raw output | low | script output (no interpretation) |
| `doc-reviewer` | Read-scope check: does the document answer the clause it claims to? | medium | findings |

Effort is a suggestion. The one role that decides quality (classification,
drafting the 审定基础) deserves the highest level available; mechanical runs do
not.

## Task template

Every task carries all five parts. Omitting any of them is the usual cause of a
subagent inventing structure or a path.

```
Role: <role>
Run directory (absolute): <path>
Read: <absolute paths of every input>
Contract: <the artifact shape this must fill, from references/contracts.md>
Write: <absolute output path>
Return: <what to report back, in at most N characters>
Constraints:
- Cite clauses only in the form <code> <clause>; every citation must exist in the corpus text.
- Do not reproduce the input back; list what you changed or decided.
- Unknown values are 待确认, never a plausible guess.
```

## Worked example: classification

```
Role: classifier
Run directory (absolute): <workspace>/runs/<slug>
Read:
  <workspace>/reviews/product-params.md
  <corpus>/text/A1_....txt  (severity and risk tables)
  <corpus>/text/L1_....txt  (category definitions; scanned, render if needed)
Contract: classification report in references/contracts.md
Write: <run dir>/01_classification.md
Return: under 1500 characters — severity class, risk level, category, and every unknown.
Constraints:
- Show the kinetic-energy calculation.
- Quote the table cell used for the risk level.
- If 最大起飞重量 is unknown, stop and ask rather than assuming a class.
```

## Worked example: mechanical verification

```
Role: mechanical-verifier
Run directory (absolute): <path>
Run:
  python3 scripts/verify_citations.py --doc <path> --corpus <corpus>
  python3 scripts/check_consistency.py --dir <folder> --expect <rules>
Return: the raw output, plus one line stating how many items were checked.
Constraints:
- Do not fix anything and do not interpret. Report MISS and FAIL lines verbatim.
- Do not summarise away a miss because it "looks like a typo".
```

## Worked example: repair and re-audit

Repairs are bounded by statutory time, not by round count: a POA safety-related
nonconformity allows 5 working days to answer and 20 to correct; a DOA class-1
finding allows 21 working days. State the deadline in the repair task.

```
Role: drafter (repair)
Run directory (absolute): <path>
Read: <run dir>/06_review_report.md
Fix ONLY these findings: <list>
Do NOT change: <explicit list — sections, numbering, unaffected clauses>
Write: <same artifact paths>
Return: which items changed, and the smallest description of each change.
```

Then a separate re-audit task, which must do both jobs:

```
Role: compliance-auditor (re-audit)
Read: the previous findings, the repaired artifacts, the corpus
1) For each previous finding: CLOSED / PARTIAL / NOT FIXED, each with the number that proves it.
2) Hunt regressions: re-read the whole affected section, not just the fixed line;
   confirm every cross-reference and every number still agrees; report anything
   that changed outside the stated scope as a regression.
Append to the review report; never overwrite the first pass.
```

A round that closes one finding and opens two is a failed round. Report it as
failed, then escalate rather than looping.

## Escalation

Ask the user at the moment a gap changes feasibility, at most three questions,
each as: question / why it matters / what you suggest. Everything else goes into
the artifact's `待确认` list.

Ask the authority (not the user, and not the model) when: two documents conflict,
a clause cannot be traced, or an interpretation would change a submission.
Frame those as questions to raise, with the conflicting citations attached.

## What a subagent must never do

1. Quote a clause that is not in the corpus text.
2. Fill an unknown with a plausible number.
3. Present a 局方 action as something we produce.
4. Re-run a check with a different input to make it pass.
5. Edit an artifact outside its stated scope during a repair.
