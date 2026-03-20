# skill-optimizer

The eval-driven optimizer for AI coding skills.

> *PromptFoo scores your prompts. This scores AND fixes your AI coding skills.*

Most AI skills work 70% of the time and fail unpredictably the other 30%. skill-optimizer measures that failure rate with Yes/No checklists, then automatically fixes it — one small change at a time, keeping what helps, reverting what doesn't.

## What It Does

Two modes of operation:

- **Analysis Only** — Read a skill's SKILL.md, score it across 6 quality dimensions, and output a diagnostic report with strengths, weaknesses, and improvement suggestions. No test cases needed, no modifications made.
- **Full Optimization** — Provide test cases and a Yes/No checklist, then run automated eval loops that make one small change at a time, keep what improves the score, and revert what doesn't.

## Quick Start

### Analyze a Skill (no setup needed)

Tell your AI assistant:

> "Analyze the deep-research skill"

The assistant reads the skill's SKILL.md, runs a 6-dimension quality audit, and produces a diagnostic report:

```
Overall: 14/18 (Adequate)

Structural Clarity    3/3  Strong
Instruction Complete  2/3  Adequate
Edge Case Coverage    1/3  Weak
Consistency           3/3  Strong
Actionability         2/3  Adequate
Quality Assurance     3/3  Strong

Top suggestion: Add fallback instructions when search returns fewer than 3 results.
```

### Optimize a Skill (needs test cases)

Tell your AI assistant:

> "Optimize the deep-research skill"

The assistant will:
1. Help you gather 3–5 test cases (extracted from history or provided by you)
2. Help you define 3–6 Yes/No quality criteria
3. Run a baseline evaluation
4. Enter an optimization loop: analyze failures → change one thing → re-test → keep or revert
5. Output an improved skill + changelog

## How It Works

The core idea comes from the autoresearch methodology: if something can be measured, it can be optimized.

```
Choose skill → Gather test cases → Define checklist → Run baseline
                                                          ↓
                                              Score < target?
                                              ↓ Yes         ↓ No → Done
                                    Analyze failures
                                              ↓
                                    Propose ONE change
                                              ↓
                                    Apply → Re-test → Better?
                                              ↓ Yes      ↓ No
                                            Keep       Revert
                                              ↓          ↓
                                              ← Loop ←←←←←
```

Key principles:
- **One change at a time** — isolate what helps
- **Yes/No checklist** — no vibes, binary signal
- **Bad changes get reverted** — no speculative accumulation
- **Real test cases** — from actual usage, not synthetic
- **3–6 checklist items** — more causes "teaching to the test"

## Configuration

| Parameter | Default | Description |
|-----------|---------|-------------|
| `auto_apply` | true | `true` = full-auto. `false` = pause for user approval before each change. |
| `target_pass_rate` | 0.9 | Stop when this pass rate is reached |
| `max_iterations` | 10 | Maximum optimization rounds |
| `stall_limit` | 3 | Stop after N consecutive no-improvement rounds |
| `runs_per_case` | 1 | Run each test case N times (set to 3 for flaky skills) |

## Directory Structure

```
skill-optimizer/
├── SKILL.md                          Main skill — workflow orchestration
├── agents/
│   ├── skill_analyzer.md             Phase 0: 6-dimension static analysis
│   ├── quality_grader.md             Scores outputs against Yes/No checklist
│   ├── skill_improver.md             Analyzes failures, proposes ONE change
│   ├── eval_designer.md              Helps design effective checklists
│   └── case_extractor.md             Extracts test cases from history
├── eval-viewer/
│   ├── generate_review.py            Generates interactive HTML review page
│   └── viewer.html                   Review page template
├── references/
│   ├── eval_guide.md                 Guide: how to write good Yes/No evals
│   └── schemas.md                    JSON schemas for all data formats
└── scripts/
    └── quick_validate.py             Frontmatter validation (zero dependencies)
```

## Compatibility

Designed to work with:
- **OpenCode** — full feature set including subagent-based parallel execution
- **Claude Code** — works with direct execution (no subagent requirement)
- **Any AI coding assistant** that can read markdown instructions and execute them

No external dependencies. Python scripts use only the standard library.

## Output Files

After optimization, the workspace contains:

```
{skill-name}-workspace/
├── analysis_report.md          Phase 0 diagnostic (if run)
├── analysis_report.json        Machine-readable diagnostic
├── optimization_report.md      Full optimization history
├── changelog.json              Machine-readable change log
└── iteration-N/                Per-iteration results
    └── eval-{id}/
        ├── outputs/            Skill outputs for this test case
        └── grading.json        Checklist results with evidence
```

## License

MIT — Ren Le (任乐)
