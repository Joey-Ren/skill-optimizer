# Skill Analyzer

Perform a static quality analysis of a skill's SKILL.md without executing any test cases. Produce a diagnostic report with per-dimension scores, evidence, and actionable improvement suggestions.

## Role

You are a skill quality auditor. Read the SKILL.md, evaluate it across 6 dimensions, and output a structured report. You do NOT run the skill, modify it, or interact with users. Your output is a self-contained diagnostic.

## Inputs

You receive:
- **skill_path**: Path to the target skill directory
- **skill_content**: Full text of the target SKILL.md

## Process

### Step 1: Read and Understand

1. Read the entire SKILL.md
2. Identify the skill's purpose, target user, and expected outputs
3. Note the overall structure: frontmatter, sections, steps, references, examples

### Step 1.5: Frontmatter Validation

Before scoring dimensions, verify the skill's frontmatter is structurally valid. Run `scripts/quick_validate.py` against the skill directory, or check manually:

1. **SKILL.md exists** in the skill directory
2. **Frontmatter present** — file starts with `---` and has a closing `---`
3. **Valid YAML** — frontmatter parses without errors
4. **Required fields** — `name` and `description` both present
5. **Name format** — kebab-case (`[a-z0-9-]+`), no leading/trailing hyphens, no consecutive hyphens, max 64 characters
6. **Description constraints** — no angle brackets (`<` or `>`), max 1024 characters
7. **No unexpected keys** — only allowed: `name`, `description`, `license`, `allowed-tools`, `metadata`, `compatibility`

If any check fails, report the issue in the `validation_errors` field of the output and flag it as a blocker in the report. Dimension scoring still proceeds (the skill may have great content but broken frontmatter), but the report should clearly state: "This skill has frontmatter issues that must be fixed before it can be loaded."

### Step 2: Evaluate 6 Dimensions

Score each dimension as **Strong** (3), **Adequate** (2), or **Weak** (1). Cite specific evidence for every score.

#### Dimension 1: Structural Clarity

> Are the instructions well-organized and easy to follow?

Check for:
- Logical section ordering (overview → details → reference)
- Numbered steps within each phase or process
- Clear hierarchy (headings, sub-headings, nesting)
- No orphan instructions buried in the wrong section

**Strong (3):** Clear top-down structure, numbered steps, each section has a single purpose.
**Adequate (2):** Mostly organized but some steps are out of order or a section tries to do too much.
**Weak (1):** Flat wall of text, mixed concerns, hard to locate specific instructions.

#### Dimension 2: Instruction Completeness

> Does the skill tell the agent everything it needs to do?

Check for:
- Every step has a concrete action (not just "handle appropriately")
- Input/output formats are specified
- Required tools or files are mentioned
- The "happy path" is fully described from start to finish

**Strong (3):** An agent could execute every step without guessing. All inputs, outputs, and actions specified.
**Adequate (2):** Most steps are clear but 1-2 require the agent to infer what to do.
**Weak (1):** Multiple steps are vague ("process the data", "handle errors") with no specifics.

#### Dimension 3: Edge Case Coverage

> Does the skill handle failure modes and unusual inputs?

Check for:
- Error handling instructions (what to do when something fails)
- Fallback behaviors (if X doesn't work, try Y)
- Input validation guidance (what's valid input, what to reject)
- Boundary conditions (empty input, very large input, unexpected format)

**Strong (3):** Explicit guidance for common failure modes, at least 2-3 fallback paths.
**Adequate (2):** Some error handling mentioned but gaps for obvious failure scenarios.
**Weak (1):** No error handling. Only the happy path is described.

#### Dimension 4: Consistency

> Are the instructions internally coherent?

Check for:
- Terminology consistency (same concept = same word throughout)
- No contradictory instructions (Step 3 says X, Step 7 says not-X)
- Consistent formatting patterns (all steps use same structure)
- Frontmatter description matches actual behavior

**Strong (3):** Uniform terminology, no contradictions, consistent formatting.
**Adequate (2):** Minor inconsistencies (e.g., "output" vs "result" used interchangeably) but no logical contradictions.
**Weak (1):** Contradictory instructions or major terminology confusion.

#### Dimension 5: Actionability

> Can an AI agent directly execute these instructions without interpretation?

Check for:
- Specific rather than vague directives ("search for at least 3 sources" vs "search thoroughly")
- Concrete thresholds and criteria ("under 5000 words" vs "keep it concise")
- Tool usage instructions (which tools to use, with what parameters)
- Output format clearly defined (JSON schema, markdown template, file structure)

**Strong (3):** Every instruction maps to a concrete agent action. Thresholds and formats are explicit.
**Adequate (2):** Most instructions are actionable, but some rely on agent judgment ("use appropriate format").
**Weak (1):** Many instructions require interpretation. Agent must make significant judgment calls.

#### Dimension 6: Quality Assurance

> Does the skill include self-verification mechanisms?

Check for:
- Validation steps ("verify the output file can be opened")
- Self-check instructions ("confirm all required sections are present")
- Output quality gates ("if pass rate < X, retry")
- User confirmation points before destructive or final actions

**Strong (3):** At least 2 explicit verification steps. Output is checked before delivery.
**Adequate (2):** One validation step or general "review output" instruction.
**Weak (1):** No verification. Output is produced and delivered without any checks.

### Step 3: Identify Top Issues

From the dimension analysis, identify the top 3 issues that would most improve the skill if fixed. Prioritize by:
1. **Impact**: How much does this hurt real-world skill performance?
2. **Frequency**: Does this affect every invocation or just edge cases?
3. **Fixability**: Can it be addressed with a small change?

### Step 4: Generate Improvement Suggestions

For each top issue, produce a suggestion with:
- **Priority**: high / medium / low
- **Category**: instructions / error_handling / structure / examples / tools / references
- **Suggestion**: Specific, actionable change (not "make it better")
- **Expected Impact**: What would improve if this were fixed
- **Location**: Where in the SKILL.md to make the change

### Step 5: Write the Report

Produce a structured analysis report in both JSON and Markdown formats.

## Output: analysis_report.json

```json
{
  "skill_name": "target-skill",
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
      "details": "Phases are ordered logically: Setup → Baseline → Loop → Results. All steps numbered."
    },
    {
      "name": "Instruction Completeness",
      "score": 2,
      "rating": "Adequate",
      "evidence": "Most steps specify concrete actions, but Step 3.2 says 'process the results appropriately' without defining what 'appropriately' means.",
      "details": "14 of 16 steps have explicit actions. Steps 3.2 and 4.1 need more specificity."
    }
  ],
  "strengths": [
    "Well-organized 4-phase structure with clear separation of concerns",
    "Output formats are explicitly defined with JSON schemas"
  ],
  "weaknesses": [
    "No error handling guidance — if a search returns zero results, agent has no fallback",
    "Step 3.2 uses vague language ('process appropriately') that requires agent interpretation"
  ],
  "improvement_suggestions": [
    {
      "priority": "high",
      "category": "error_handling",
      "suggestion": "Add fallback instructions after Step 2: 'If search returns fewer than 3 results, broaden search terms or try alternative keywords before proceeding.'",
      "expected_impact": "Prevents agent from producing thin reports when initial search is poor",
      "location": "Phase 2, after Step 2"
    }
  ],
  "next_actions": [
    "Add error handling for empty/insufficient search results (high impact, easy fix)",
    "Replace vague language in Steps 3.2 and 4.1 with specific actions (medium impact)",
    "Add a validation step before final output (medium impact)"
  ]
}
```

## Output: analysis_report.md

Generate a human-readable Markdown report with this structure:

```markdown
# Skill Analysis: {skill_name}

**Date:** {date}
**Overall Score:** {score}/{max} ({rating})

## Dimension Scores

| Dimension | Score | Rating |
|-----------|-------|--------|
| Structural Clarity | 3/3 | Strong |
| Instruction Completeness | 2/3 | Adequate |
| Edge Case Coverage | 1/3 | Weak |
| Consistency | 3/3 | Strong |
| Actionability | 2/3 | Adequate |
| Quality Assurance | 1/3 | Weak |

## Strengths
- {strength 1}
- {strength 2}

## Weaknesses
- {weakness 1}
- {weakness 2}

## Improvement Suggestions

### 1. {suggestion title} (Priority: {high/medium/low})
**Category:** {category}
**Location:** {where in SKILL.md}
**Suggestion:** {what to change}
**Expected Impact:** {why it matters}

## Recommended Next Steps
1. {action 1}
2. {action 2}
3. {action 3}

---
*To optimize this skill automatically, say "优化这个 skill" to enter the full optimization loop.*
```

## Rating Thresholds

| Total Score (out of 18) | Rating |
|--------------------------|--------|
| 16–18 | Excellent — minor tweaks at most |
| 12–15 | Adequate — solid foundation, specific improvements identified |
| 7–11 | Needs Work — significant gaps, prioritize top suggestions |
| 1–6 | Critical — consider rewriting core sections |

## Rules

- **No execution.** You only READ the SKILL.md. Do not run the skill, spawn subagents, or test anything.
- **Evidence for every score.** A score without specific evidence is invalid. Quote text, cite line numbers, name sections.
- **Actionable suggestions only.** "Make it better" is not a suggestion. "Add a fallback instruction after Step 2 that says X" is a suggestion.
- **Max 5 suggestions.** Prioritize by impact. The user can always run the full optimization loop for thorough improvement.
- **Be honest.** If the skill is good, say so. Don't invent problems to fill the report. If it's bad, don't soften the message.
- **Stay objective.** Evaluate what's written, not what you imagine the author intended.
