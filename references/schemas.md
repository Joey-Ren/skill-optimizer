# JSON Schemas

Data format definitions for skill-optimizer. All JSON files follow these schemas.

---

## analysis_report.json

Output from Phase 0 (Analysis Only). Located at `{skill-name}-workspace/analysis_report.json`.

```json
{
  "skill_name": "deep-research",
  "analysis_date": "2026-03-20",
  "frontmatter_valid": true,
  "validation_errors": [],
  "overall_score": 14,
  "max_score": 18,
  "rating": "Adequate",
  "dimensions": [
    {
      "name": "Structural Clarity",
      "score": 3,
      "rating": "Strong",
      "evidence": "Clear 4-phase workflow with numbered steps. Each section has a single purpose.",
      "details": "Phases ordered logically: Setup → Baseline → Loop → Results. All steps numbered."
    },
    {
      "name": "Instruction Completeness",
      "score": 2,
      "rating": "Adequate",
      "evidence": "Most steps specify concrete actions, but Step 3.2 says 'process the results appropriately' without specifics.",
      "details": "14 of 16 steps have explicit actions. Steps 3.2 and 4.1 need more specificity."
    },
    {
      "name": "Edge Case Coverage",
      "score": 1,
      "rating": "Weak",
      "evidence": "No fallback instructions. If search returns zero results, agent has no guidance.",
      "details": "Only the happy path is described. No error handling or retry logic."
    },
    {
      "name": "Consistency",
      "score": 3,
      "rating": "Strong",
      "evidence": "Uniform terminology throughout. No contradictory instructions found.",
      "details": "Terms are consistent: 'test case' not mixed with 'eval case' or 'sample'."
    },
    {
      "name": "Actionability",
      "score": 2,
      "rating": "Adequate",
      "evidence": "Most instructions are concrete, but Step 5 says 'ensure quality' without measurable criteria.",
      "details": "12 of 16 instructions map to specific agent actions."
    },
    {
      "name": "Quality Assurance",
      "score": 3,
      "rating": "Strong",
      "evidence": "Includes validation step in Phase 4 and user confirmation before final output.",
      "details": "Two explicit verification points: output validation and user sign-off."
    }
  ],
  "strengths": [
    "Well-organized 4-phase structure with clear separation of concerns",
    "Consistent terminology and formatting throughout"
  ],
  "weaknesses": [
    "No error handling — if search returns zero results, agent has no fallback",
    "Step 3.2 uses vague language ('process appropriately') requiring interpretation"
  ],
  "improvement_suggestions": [
    {
      "priority": "high",
      "category": "error_handling",
      "suggestion": "Add fallback instructions after Step 2: 'If search returns fewer than 3 results, broaden search terms or try alternative keywords before proceeding.'",
      "expected_impact": "Prevents agent from producing thin reports when initial search is poor",
      "location": "Phase 2, after Step 2"
    },
    {
      "priority": "medium",
      "category": "instructions",
      "suggestion": "Replace 'process the results appropriately' in Step 3.2 with specific actions: 'Extract key claims, group by theme, and rank by source credibility.'",
      "expected_impact": "Removes ambiguity that causes inconsistent output structure",
      "location": "Phase 3, Step 3.2"
    }
  ],
  "next_actions": [
    "Add error handling for empty/insufficient search results (high impact, easy fix)",
    "Replace vague language in Steps 3.2 and 4.1 with specific actions (medium impact)",
    "Add a validation step before final output (medium impact)"
  ]
}
```

**Fields:**
- `skill_name`: Name of the analyzed skill
- `analysis_date`: Date of analysis (YYYY-MM-DD)
- `frontmatter_valid`: Boolean — whether frontmatter passes all structural checks
- `validation_errors`: Array of strings — empty if valid, otherwise lists each issue (e.g., "Missing 'name' in frontmatter", "Name should be kebab-case")
- `overall_score`: Sum of dimension scores (1–3 each, total 6–18)
- `max_score`: Always 18 (6 dimensions × 3 max)
- `rating`: "Excellent" (16–18), "Adequate" (12–15), "Needs Work" (7–11), "Critical" (1–6)
- `dimensions[]`: Per-dimension evaluation
  - `name`: Dimension name
  - `score`: 1 (Weak), 2 (Adequate), 3 (Strong)
  - `rating`: Human-readable score label
  - `evidence`: Primary evidence for the score (specific quotes or observations)
  - `details`: Additional context
- `strengths[]`: List of things the skill does well
- `weaknesses[]`: List of issues found
- `improvement_suggestions[]`: Prioritized, actionable suggestions
  - `priority`: high / medium / low
  - `category`: instructions / error_handling / structure / examples / tools / references
  - `suggestion`: Specific change to make
  - `expected_impact`: Why this change matters
  - `location`: Where in the SKILL.md to apply it
- `next_actions[]`: Top 3 recommended actions, ordered by priority

---

## test_cases.json

Defines the test cases for evaluating a skill. Created during Phase 1 (Setup).

```json
{
  "skill_name": "deep-research",
  "test_cases": [
    {
      "id": 1,
      "prompt": "帮我调研一下 shadcn-vue 和 Element Plus 的对比",
      "source": "project_logs",
      "context_files": [],
      "expected_behavior": "Structured comparison report with pros/cons table and recommendation",
      "historical_result": "success"
    },
    {
      "id": 2,
      "prompt": "Research the latest developments in WebGPU for 2026",
      "source": "session_history",
      "context_files": [],
      "expected_behavior": "Report with dated findings, source links, and technical analysis",
      "historical_result": "partial_failure"
    }
  ]
}
```

**Fields:**
- `skill_name`: Name of the skill being evaluated
- `test_cases[].id`: Unique integer identifier
- `test_cases[].prompt`: The user prompt to execute
- `test_cases[].source`: Where the test case came from (file path, "session_history", or "generated")
- `test_cases[].context_files`: Optional input files needed for the test
- `test_cases[].expected_behavior`: Human-readable description of good output
- `test_cases[].historical_result`: "success", "failure", "partial_failure", or null

---

## checklist.json

Defines the Yes/No evaluation criteria. Created during Phase 1 (Setup).

```json
{
  "skill_name": "deep-research",
  "items": [
    {
      "id": 1,
      "question": "Does the output contain all required sections (findings, analysis, conclusion)?",
      "dimension": "completeness"
    },
    {
      "id": 2,
      "question": "Is every conclusion backed by a specific source or link?",
      "dimension": "correctness"
    },
    {
      "id": 3,
      "question": "Is the output under 5000 words?",
      "dimension": "format"
    },
    {
      "id": 4,
      "question": "Does the output directly answer the user's core question?",
      "dimension": "relevance"
    }
  ]
}
```

**Fields:**
- `skill_name`: Name of the skill being evaluated
- `items[].id`: Unique integer identifier
- `items[].question`: The Yes/No evaluation question
- `items[].dimension`: Quality dimension (completeness, correctness, format, usability, relevance)

---

## grading.json

Output from the Quality Grader agent. One per test case per iteration. Located at `iteration-N/eval-{id}/grading.json`.

```json
{
  "test_case_id": 1,
  "test_prompt": "帮我调研一下 shadcn-vue 和 Element Plus 的对比",
  "checklist_results": [
    {
      "item": "Does the output contain all required sections (findings, analysis, conclusion)?",
      "passed": true,
      "evidence": "Found: '## Key Findings' (line 5), '## Detailed Analysis' (line 18), '## Conclusion' (line 45)"
    },
    {
      "item": "Is every conclusion backed by a specific source or link?",
      "passed": false,
      "evidence": "Conclusion has 3 claims. Claim 1 cites arxiv.org. Claims 2 and 3 have no source."
    },
    {
      "item": "Is the output under 5000 words?",
      "passed": true,
      "evidence": "Output is 2,847 words."
    },
    {
      "item": "Does the output directly answer the user's core question?",
      "passed": true,
      "evidence": "Output compares shadcn-vue and Element Plus across 5 dimensions with a recommendation."
    }
  ],
  "summary": {
    "passed": 3,
    "failed": 1,
    "total": 4,
    "pass_rate": 0.75
  }
}
```

**Fields:**
- `test_case_id`: Which test case this grades
- `test_prompt`: The prompt that was executed
- `checklist_results[].item`: The checklist question
- `checklist_results[].passed`: Boolean — true if condition is met
- `checklist_results[].evidence`: Specific evidence supporting the verdict
- `summary.passed`: Count of passed items
- `summary.failed`: Count of failed items
- `summary.total`: Total items evaluated
- `summary.pass_rate`: passed / total (0.0 to 1.0)

---

## changelog.json

Machine-readable history of all optimization iterations. Located at `{skill-name}-workspace/changelog.json`.

```json
{
  "skill_name": "deep-research",
  "baseline_score": "3/5 (60%)",
  "final_score": "5/5 (100%)",
  "exit_reason": "target_reached",
  "iterations": [
    {
      "iteration": 1,
      "timestamp": "2026-03-20T14:30:00",
      "change": "Added minimum source count threshold to research step",
      "human_summary": "Add a minimum 3-source threshold so the agent doesn't stop searching too early",
      "reason": "Agent stopped searching after 1-2 results; 2 of 5 test cases had conclusions without source links",
      "failure_pattern": "Conclusions missing source attribution",
      "before_score": "3/5 (60%)",
      "after_score": "4/5 (80%)",
      "verdict": "KEEP",
      "user_approved": true,
      "diff": {
        "old_text": "Search for relevant information on the topic.",
        "new_text": "Search for relevant information on the topic. If fewer than 3 distinct sources are found, try alternative search terms or broaden the query before proceeding."
      }
    },
    {
      "iteration": 2,
      "timestamp": "2026-03-20T14:45:00",
      "change": "Added explicit instruction to cite sources in conclusion",
      "human_summary": "Require every conclusion claim to reference a specific source",
      "reason": "Test case #4 still had uncited conclusion despite having sources in the body",
      "failure_pattern": "Sources found but not referenced in conclusion section",
      "before_score": "4/5 (80%)",
      "after_score": "4/5 (80%)",
      "verdict": "REVERT",
      "user_approved": true,
      "diff": {
        "old_text": "Write a conclusion summarizing key findings.",
        "new_text": "Write a conclusion summarizing key findings. Every claim in the conclusion must reference a specific source from the analysis above."
      }
    }
  ]
}
```

**Fields:**
- `skill_name`: Name of the skill being optimized
- `baseline_score`: Score before any changes
- `final_score`: Score at end of optimization
- `exit_reason`: "target_reached", "stall_limit", or "max_iterations"
- `iterations[].iteration`: Sequential number
- `iterations[].timestamp`: ISO 8601 timestamp
- `iterations[].change`: Human-readable description of what changed
- `iterations[].human_summary`: Plain-language one-liner for user approval in semi-auto mode
- `iterations[].reason`: Why this change was proposed
- `iterations[].failure_pattern`: The pattern that prompted this change
- `iterations[].before_score`: Pass rate before this change
- `iterations[].after_score`: Pass rate after this change
- `iterations[].verdict`: "KEEP", "REVERT", or "SKIPPED" (user declined in semi-auto mode)
- `iterations[].user_approved`: Boolean — `true` if user approved (or auto mode), `false` if user declined, `null` if auto mode
- `iterations[].diff.old_text`: Text that was replaced
- `iterations[].diff.new_text`: Text that replaced it

---

## optimization_report.json

Summary of the full optimization run. Located at `{skill-name}-workspace/optimization_report.json`.

```json
{
  "skill_name": "deep-research",
  "optimization_date": "2026-03-20",
  "baseline_score": 0.6,
  "final_score": 0.92,
  "total_iterations": 5,
  "changes_kept": 3,
  "changes_reverted": 2,
  "exit_reason": "target_reached",
  "test_cases_count": 5,
  "checklist_items_count": 4,
  "configuration": {
    "auto_apply": true,
    "target_pass_rate": 0.9,
    "max_iterations": 10,
    "stall_limit": 3,
    "runs_per_case": 1
  }
}
```

**Fields:**
- `skill_name`: Name of the optimized skill
- `optimization_date`: Date of the optimization run
- `baseline_score`: Initial pass rate (0.0–1.0)
- `final_score`: Final pass rate (0.0–1.0)
- `total_iterations`: Number of iterations run
- `changes_kept`: Number of changes that improved the score
- `changes_reverted`: Number of changes that were rolled back
- `exit_reason`: Why the loop stopped
- `test_cases_count`: Number of test cases used
- `checklist_items_count`: Number of checklist items
- `configuration`: The parameters used for this run
