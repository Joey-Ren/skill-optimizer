# Case Extractor

Extract real test cases from historical usage data. Real test cases are more valuable than synthetic ones because they represent what users actually ask the skill to do, including the messy edge cases that are hard to invent.

## Role

Search available historical data for real uses of the target skill, extract them as structured test cases, and present them to the user for confirmation.

## Inputs

You receive:
- **skill_name**: Name of the target skill to find cases for
- **skill_description**: Brief description of what the skill does (for context when generating fallback cases)

## Sources (Search in This Order)

Try each source in order. Skip any that don't exist in the current environment — this skill is designed to work across different setups.

### 1. Project-Local Logs

Search for log files, daily notes, or history files in the current project that might mention the target skill.

**How to search:**
- Use `Grep` tool to search the project directory for the skill name
- Common locations to check: `.memory/`, `daily-report/`, `logs/`, `notes/`, or any directory that looks like it contains usage history
- Also search for related keywords (e.g., for "deep-research" also search "调研", "research")
- If no log directories exist, skip to Source 2

### 2. Session History (if available)

Some environments provide tools to search past conversation history.

**How to search:**
- If `session_search` tool is available, use it with the skill name as query
- If `grep` can search a sessions directory, try that
- If neither is available, skip to Source 3
- Look for messages where the user triggered the skill, and any follow-up feedback

### 3. AI-Generated Cases (Fallback)

If fewer than 3 real cases are found from the above sources, generate synthetic cases based on the skill's SKILL.md. This is the fallback, not the preferred path.

**When generating:**
- Read the skill's SKILL.md to understand its intended use cases
- Create prompts that a real user would actually type — casual, with context, sometimes messy
- Include at least one edge case or unusual input
- Mark these clearly as `"source": "generated"` so the user knows they're synthetic

## Process

### Step 1: Search for Historical Usage

1. Check what history sources are available in the current environment
2. Search each available source for the skill name and related keywords
3. For each match, extract:
   - The date (if available)
   - The user's original request/prompt
   - Any input files mentioned
   - Whether the result was noted as good or bad
4. Record as candidate test cases

### Step 2: Select and Diversify

From all candidates, select 3–5 cases that maximize diversity:
- Different types of inputs (short vs long, simple vs complex)
- Different use scenarios (if the skill serves multiple purposes)
- At least 1 case that previously failed (if found), because failure cases are the most valuable for optimization
- Avoid multiple cases that test essentially the same thing

### Step 3: Generate Fallbacks (If Needed)

If fewer than 3 real cases found:
1. Read the skill's SKILL.md
2. Generate cases covering different aspects of the skill
3. Make prompts realistic — include context, file paths, casual language
4. Mark as `"source": "generated"`

### Step 4: Write Expected Behavior

For each test case, write a brief `expected_behavior` description:
- What the output should contain
- What format it should be in
- Any specific quality markers

### Step 5: Present to User

Show all extracted cases to the user. For each case, show:
- The prompt
- Where it came from (source)
- Expected behavior
- Whether it was a known success or failure

Ask the user to confirm, modify, add, or remove cases.

## Output Format

```json
{
  "skill_name": "target-skill",
  "test_cases": [
    {
      "id": 1,
      "prompt": "Help me compare shadcn-vue and Element Plus",
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
      "expected_behavior": "Report with dated findings from 2026, source links, and technical analysis",
      "historical_result": "partial_failure"
    },
    {
      "id": 3,
      "prompt": "Deep dive comparison of CrewAI vs AutoGen multi-agent frameworks",
      "source": "generated",
      "context_files": [],
      "expected_behavior": "Multi-section comparison with architecture analysis, code examples, and clear recommendation",
      "historical_result": null
    }
  ],
  "extraction_notes": "Found 8 historical uses in project logs. Selected 2 real cases + 1 generated. Case #2 had partial failure: missing source links in conclusion."
}
```

## Rules

- **Minimum 3 cases, ideally 5.** Fewer than 3 doesn't give enough signal. More than 7 makes each optimization loop too slow.
- **Diversity over quantity.** 3 diverse cases beat 5 similar ones.
- **Failure cases are gold.** If a case previously failed, always include it — that's exactly what the optimizer needs to fix.
- **Always confirm with user.** Never skip the confirmation step. The user knows their use cases better than the logs do.
- **Honest about sources.** Mark generated cases as generated. Don't pretend synthetic cases are real.
- **Graceful degradation.** If no history sources exist, don't error out — fall back to AI-generated cases and tell the user why.
