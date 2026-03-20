# Eval Guide

How to write evaluation criteria that actually work. This guide helps you create Yes/No checklists that produce reliable, meaningful scores.

## The Golden Rule

**Every eval must be a Yes/No question.**

Not a scale. Not a feeling judgment. Binary.

Why? Scales add variance. If you have 4 evals each scored 1–7, the total score swings wildly between runs — same output, different scores. Binary evals give you a stable signal: either the condition is met or it isn't.

## Good vs Bad Evals

### Text / Content Skills

| Bad | Good | Why |
|-----|------|-----|
| "Is the writing good?" | "Does the output avoid these phrases: [game-changer, here's the kicker, level up]?" | "Good" is subjective; phrase presence is binary |
| "Rate attractiveness 1-10" | "Is the output between 150–400 words?" | Scale = unreliable; word count = measurable |
| "Does it sound human?" | "Does the first sentence mention a specific time, place, or sensory detail?" | "Human" is vague; structural features are checkable |
| "Is the CTA effective?" | "Does the ending contain a specific action the reader should take next?" | "Effective" is subjective; presence of action is binary |

### Visual / Design Skills

| Bad | Good | Why |
|-----|------|-----|
| "Does it look professional?" | "Is all text legible with no truncation, overlap, or cutoff?" | "Professional" is subjective; legibility is observable |
| "Rate visual quality 1-5" | "Does the color scheme use only muted/pastel tones, no neon or high-saturation?" | Scale; vs specific checkable constraint |
| "Is the layout good?" | "Does the layout flow linearly (left-to-right or top-to-bottom) with no scattered elements?" | "Good" is vague; flow direction is structural |

### Code / Technical Skills

| Bad | Good | Why |
|-----|------|-----|
| "Is the code clean?" | "Does the code run without errors?" | Subjective; vs actually testable |
| "Does it follow best practices?" | "Are there no TODO or placeholder comments?" | Vague; vs grep-able |
| "Is it well-structured?" | "Do all functions have descriptive names (no single-letter vars except loop counters)?" | Subjective; vs inspectable |

### Document Skills

| Bad | Good | Why |
|-----|------|-----|
| "Is it comprehensive enough?" | "Does the document contain all required sections: [list them]?" | Relative; vs checkable against a list |
| "Does it meet client needs?" | "Is every conclusion supported by a specific number, date, or source?" | Vague; vs verifiable |
| "Is it the right length?" | "Is the document under 10 pages / 3000 words?" | Ambiguous; vs measurable |

## Common Mistakes

### 1. Too Many Evals (>6)
After 6 checklist items, the skill starts "gaming" the checklist — optimizing to pass each check rather than genuinely producing good output. Like a student memorizing answers instead of understanding the material.

**Fix:** Choose the 3–6 checks that matter most. If those all pass, the output is almost certainly good.

### 2. Too Narrow / Too Rigid
"Must contain exactly 3 bullet points" or "must use the word 'because' at least twice." These produce technically passing but weird, stilted output.

**Fix:** Test quality characteristics, not arbitrary structural constraints.

### 3. Overlapping Evals
"Is the grammar correct?" + "Are there any typos?" — these overlap. Grammar failures often include typos. You're double-counting the same issue.

**Fix:** Each eval should test one independent dimension.

### 4. Unmeasurable by AI
"Would a human find this engaging?" — the AI grader can't reliably answer this. It will almost always say "yes."

**Fix:** Translate subjective feelings into observable signals. "Engaging" → "Does the first sentence contain a specific claim, story, or question rather than a generic statement?"

## Pre-Flight Check

Before finalizing any checklist item, ask yourself:

1. **Reliability:** Would two different AI graders, looking at the same output, give the same answer? If not → too subjective, rewrite.

2. **Gaming resistance:** Could a skill produce bad output that still passes this check? If yes → too narrow, broaden.

3. **Relevance:** Does this test something the user actually cares about? If not → remove it. Every irrelevant eval dilutes the signal from the ones that matter.

## Quick Reference

```
✓ Binary (Yes/No)
✓ Observable (can be checked by reading the output)
✓ Independent (doesn't overlap with other items)
✓ Meaningful (user cares about this)
✓ Resistant to gaming (can't pass without being genuinely good)

✗ Scales (1-10)
✗ Subjective ("is it good?")
✗ Overlapping with other items
✗ Unmeasurable by AI
✗ Overly rigid structural constraints
```
