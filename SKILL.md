---
name: skill-optimizer
description: >
  Analyze and iteratively optimize any skill's quality. Two modes: (1) Analysis Only — read a
  skill and generate a diagnostic report with scores and suggestions, no modifications.
  (2) Full Optimization — automated testing loop with AI-driven improvements. Triggers on:
  analyze skill, diagnose skill, skill report, optimize skill, improve skill, tune skill,
  skill not working well, skill quality, run skill eval, benchmark skill, skill pass rate.
---

# Skill Optimizer

Two modes of operation:

- **Analysis Only (Phase 0):** Read a skill's SKILL.md → score it across 6 quality dimensions → output a diagnostic report with strengths, weaknesses, and improvement suggestions. No test cases needed, no modifications made. Fast and lightweight.
- **Full Optimization (Phase 1–4):** Provide test cases and a checklist → run automated eval loops → iteratively improve the skill one change at a time → output an improved skill + changelog. Thorough but slower.

Start with analysis to understand the current state. Then decide whether to optimize.

## Quick Start

### Analysis Only (no test cases needed)
1. **Choose the target skill** — identify which skill to analyze
2. **Run Phase 0** — get a diagnostic report with 6-dimension scores and suggestions
3. **Decide** — fix issues manually, enter full optimization, or stop here

### Full Optimization (needs test cases + checklist)
1. **Choose the target skill** — identify which skill to optimize
2. **Gather test cases** — provide 3–5 real prompts, or extract them from history
3. **Define the checklist** — write 3–6 Yes/No quality criteria, or generate them
4. **Run baseline** — evaluate current skill performance against the checklist
5. **Optimize** — enter the automated loop: analyze failures → change one thing → re-test → keep or revert
6. **Review and confirm** — inspect the optimization report and apply changes

## Full Workflow

### Phase 0: Analysis Only (no test cases required)

Use this when the user says "分析一下这个 skill", "diagnose", "review", or wants a quality report before committing to the full optimization loop.

1. **Read the target skill's SKILL.md.** Note the structure, instructions, error handling, and any referenced files. Also run frontmatter validation (`scripts/quick_validate.py`) to catch structural issues (missing name/description, invalid YAML, name format violations). Report any validation errors upfront.

2. **Run the static analyzer.** Read `agents/skill_analyzer.md` and follow its process to evaluate the skill across 6 dimensions:
   - Structural Clarity — is it well-organized and easy to follow?
   - Instruction Completeness — does it tell the agent everything it needs to do?
   - Edge Case Coverage — does it handle failures and unusual inputs?
   - Consistency — are the instructions internally coherent?
   - Actionability — can an AI agent execute the instructions without guessing?
   - Quality Assurance — does it include self-verification mechanisms?

3. **Generate the diagnostic report.** Save to `{skill-name}-workspace/analysis_report.md` (and optionally `analysis_report.json`). The report includes:
   - Overall score and rating (Excellent / Adequate / Needs Work / Critical)
   - Per-dimension scores with evidence
   - Strengths and weaknesses
   - Top improvement suggestions (max 5, prioritized by impact)
   - Recommended next steps

4. **Present the report to the user.** After presenting, offer the choice:
   - **"Want to optimize this skill?"** → Proceed to Phase 1 (Setup) to begin the full optimization loop with test cases and checklist.
   - **"That's enough for now"** → End here. The report stands as a standalone diagnostic.

   If the user chooses to optimize, the analysis report's suggestions can inform the checklist design in Phase 1.

---

### Phase 1: Setup

1. Read the target skill's SKILL.md to understand what it does and how it works.

2. **Gather test cases** — choose one approach:
   - **Extract from history**: Read `agents/case_extractor.md` and follow its process to find real usage from project logs and session history.
   - **User-provided**: Accept test cases directly from the user in the format below.
   - Minimum 3 test cases, ideally 5. Diverse inputs are more valuable than many similar ones.

3. **Define the checklist** — choose one approach:
   - **Generate with assistance**: Read `agents/eval_designer.md` to draft a checklist based on the skill type. Present to user for confirmation.
   - **User-provided**: Accept checklist items directly. Validate they are Yes/No questions.
   - See `references/eval_guide.md` for guidance on writing effective checklist items.

4. **Confirm with user** before proceeding. Show them the test cases and checklist. This is the last chance to adjust before the loop begins.

### Phase 2: Baseline Evaluation

1. Create a workspace directory: `{skill-name}-workspace/iteration-0/`

2. For each test case, **execute the target skill with the test prompt**:
   - If the environment supports subagents (e.g., OpenCode `task()`), spawn a subagent that loads the target skill and runs the prompt. This is the preferred approach for isolation.
   - If subagents are not available (e.g., Claude Code), execute the skill instructions directly in the current session: read the target SKILL.md, follow its instructions with the test prompt as input, and save outputs.
   - Either way, save all outputs to `iteration-0/eval-{id}/outputs/`
   - If `runs_per_case` > 1, repeat each test case that many times. Grade each run independently, then for each checklist item use **majority vote**: the item passes only if it passed in more than half the runs. This smooths out flaky results. Save individual run grades to `iteration-0/eval-{id}/run-{N}/grading.json` and the majority-vote summary to `iteration-0/eval-{id}/grading.json`.

3. Grade each output by reading `agents/quality_grader.md` and evaluating against the checklist. Save results to `iteration-0/eval-{id}/grading.json`.

4. Calculate and report the baseline score. Example: "Baseline: 3/5 test cases pass all checks (60%)".

5. If baseline is already ≥90%, inform the user the skill may not need optimization. Offer to proceed anyway or stop.

### Phase 3: Optimization Loop

Two execution modes, controlled by `auto_apply` (default: `true`):

- **Full-auto** (`auto_apply: true`): AI proposes, applies, tests, and keeps/reverts changes without interruption. Best when you trust the process and want speed.
- **Semi-auto** (`auto_apply: false`): AI proposes each change, then **pauses for user approval** before applying. You see every change before it touches the skill. Best for high-stakes skills or first-time use.

Repeat until exit condition is met:

1. **Analyze failures.** Collect all grading results where checklist items failed. Look for patterns: which items fail most? Is there a common root cause?

2. **Propose a change.** Read `agents/skill_improver.md` and provide it with:
   - Current SKILL.md content
   - All grading results (passed and failed)
   - The changelog so far (to avoid repeating failed changes)
   
   The improver proposes ONE minimal change with rationale and a human-readable summary.

3. **Approval gate** (behavior depends on mode):

   **If `auto_apply: false` (semi-auto):**
   Present the proposed change to the user before doing anything:
   ```
   Iteration {N} — Proposed Change:
   ┌─────────────────────────────────────
   │ Problem:  {failure_pattern}
   │ Root cause: {root_cause}
   │ Change:   {human_summary}
   │ Location: {location in SKILL.md}
   │ Expected: {expected_impact}
   └─────────────────────────────────────
   Apply this change? [Yes / No / Stop optimization]
   ```
   - User says **Yes** → apply the change and proceed to step 4
   - User says **No** → skip this change, record as `"verdict": "SKIPPED"` in changelog, return to step 1 with instruction to try a different approach
   - User says **Stop** → proceed directly to Phase 4

   **If `auto_apply: true` (full-auto):**
   Apply the change immediately and proceed to step 4.

4. **Re-run all test cases** into `iteration-{N}/`. Same process as baseline: execute the target skill with each test prompt and grade outputs.

5. **Compare scores:**
   - New pass rate > previous pass rate → **KEEP** the change. Record in changelog with the diff, reason, and score delta.
   - New pass rate ≤ previous pass rate → **REVERT** the change. Record the attempt as reverted. Restore previous SKILL.md.

6. **Report iteration summary.** After every iteration, output a one-line progress update regardless of mode:
   ```
   Iteration {N}: {change_summary} → {before}→{after} → {KEEP/REVERT}
   ```
   Example: `Iteration 3: Added min 3-source threshold to Step 2 → 60%→80% → KEEP`
   
   In semi-auto mode, also show the current grading breakdown (which checklist items passed/failed) so the user can see what's still failing.

7. **Check exit conditions:**
   - Pass rate ≥ `target_pass_rate` (default 0.9) → exit with success
   - `stall_limit` consecutive iterations with no improvement (default 3) → exit with stall
   - `max_iterations` reached (default 10) → exit with max iterations
   - **Consecutive revert warning**: if 2 changes in a row are reverted, **pause and ask the user** regardless of mode: "Two consecutive changes had no effect. Continue optimizing, adjust the checklist, or stop?" This prevents burning tokens on a direction that isn't working.
   - Any exit → proceed to Phase 4

### Phase 4: Results

1. **Generate the optimization report** saved to `{skill-name}-workspace/optimization_report.md`:
   - Skill name and optimization date
   - Baseline score vs final score
   - Each iteration: what changed, why, before/after score, kept or reverted
   - Final SKILL.md diff (cumulative changes from baseline)
   - Exit reason

2. **Save machine-readable changelog** to `{skill-name}-workspace/changelog.json`. See `references/schemas.md` for the format.

3. **Optionally launch the eval viewer** for human review:
   ```
   python eval-viewer/generate_review.py {skill-name}-workspace/iteration-{latest} --skill-name "{skill-name}"
   ```

4. **Present results to user.** Show the before/after score and key changes. Ask for confirmation before applying changes to the original skill file.

## Test Case Format

```json
{
  "skill_name": "target-skill",
  "test_cases": [
    {
      "id": 1,
      "prompt": "The actual user prompt to test with",
      "source": "Where this test case came from (e.g., project logs, session history, or 'generated')",
      "context_files": ["optional/input/files.txt"],
      "expected_behavior": "Human-readable description of what good output looks like"
    }
  ]
}
```

## Checklist Format

Each checklist item is a Yes/No question. Aim for 3–6 items. Examples by skill type:

**Research/Content skills:**
- "Does the output contain all required sections (findings, analysis, conclusion)?"
- "Is every conclusion backed by a specific source or link?"
- "Is the output under 5000 words?"
- "Does the output directly answer the user's core question?"

**Document processing skills:**
- "Can the output file be opened without errors?"
- "Does the output contain all key data from the input?"
- "Does the format match the skill's template requirements?"
- "Is there no garbled text, truncation, or data loss?"

**Code/Technical skills:**
- "Does the generated code run without errors?"
- "Are there no TODO or placeholder comments?"
- "Does the code use the specified tech stack/framework?"
- "Do critical functions have error handling?"

**Image/Media skills:**
- "Was an image successfully generated (not empty, not an error)?"
- "Does the image content match the prompt description?"
- "Is all text in the image legible and not truncated?"
- "Does the image meet size/ratio requirements?"

For detailed guidance on writing effective checklist items, read `references/eval_guide.md`.

## Configuration

| Parameter | Default | Description |
|-----------|---------|-------------|
| `auto_apply` | true | `true` = full-auto (AI applies changes without asking). `false` = semi-auto (pauses for user approval before each change). |
| `target_pass_rate` | 0.9 (90%) | Stop optimizing when this pass rate is reached |
| `max_iterations` | 10 | Maximum optimization rounds before stopping |
| `stall_limit` | 3 | Stop after this many consecutive no-improvement rounds |
| `runs_per_case` | 1 | Run each test case N times (set to 3 for flaky skills) |

## Agent Reference

| Agent | File | When to Read |
|-------|------|-------------|
| Skill Analyzer | `agents/skill_analyzer.md` | When running Phase 0 analysis (static diagnostic, no test cases) |
| Quality Grader | `agents/quality_grader.md` | When grading skill outputs against the checklist |
| Skill Improver | `agents/skill_improver.md` | When analyzing failures and proposing changes |
| Eval Designer | `agents/eval_designer.md` | When helping the user design a checklist |
| Case Extractor | `agents/case_extractor.md` | When extracting test cases from `.memory/` or session history |

## Output Files

| File | Description |
|------|-------------|
| `{skill-name}-workspace/analysis_report.md` | Phase 0 diagnostic report (scores, strengths, weaknesses, suggestions) |
| `{skill-name}-workspace/analysis_report.json` | Machine-readable Phase 0 report (see `references/schemas.md`) |
| `{skill-name}-workspace/optimization_report.md` | Human-readable report with before/after scores and change history |
| `{skill-name}-workspace/changelog.json` | Machine-readable iteration history (see `references/schemas.md`) |
| `{skill-name}-workspace/iteration-N/` | Per-iteration directories with test outputs and grading results |
| `{skill-name}-workspace/iteration-N/eval-{id}/outputs/` | Skill outputs for each test case |
| `{skill-name}-workspace/iteration-N/eval-{id}/grading.json` | Checklist grading results for each test case |
