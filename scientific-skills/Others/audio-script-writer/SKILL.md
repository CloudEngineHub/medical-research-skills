---
name: audio-script-writer
description: Convert written medical content into podcast or video scripts optimized.
license: MIT
skill-author: AIPOCH
---
# Audio Script Writer

## Quick Check

Use this command to verify that the packaged script entry point can be parsed before deeper execution.

```bash
python -m py_compile scripts/main.py
```

## Audit-Ready Commands

Use these concrete commands for validation. They are intentionally self-contained and avoid placeholder paths.

```bash
python -m py_compile scripts/main.py
python scripts/main.py --help
python scripts/main.py --text "Audit validation sample with explicit methods, findings, and conclusion."
```

## Workflow

1. Confirm the user objective, required inputs, and non-negotiable constraints before doing detailed work.
2. Validate that the request matches the documented scope and stop early if the task would require unsupported assumptions.
3. Use the packaged script path or the documented reasoning path with only the inputs that are actually available.
4. Return a structured result that separates assumptions, deliverables, risks, and unresolved items.
5. If execution fails or inputs are incomplete, switch to the fallback path and state exactly what blocked full completion.

## Overview

Content transformation tool that converts written medical and scientific materials into professionally structured audio scripts suitable for podcasts, educational videos, audiobooks, and voiceover narration.

**Key Capabilities:**
- **Format Conversion**: Research papers → podcast scripts
- **Spoken Word Optimization**: Sentence restructuring for listening
- **Pronunciation Guides**: Medical terminology phonetic spelling
- **Timing Estimation**: Duration calculations for production planning
- **Multi-Format Output**: Podcast, video, lecture, audiobook templates
- **Voice Direction**: Tone, pace, and emphasis cues for narrators

## When to Use

- Use this skill when the task is to Convert written medical content into podcast or video scripts optimized.
- Use this skill for other tasks that require explicit assumptions, bounded scope, and a reproducible output format.
- Use this skill when the response must stay inside the documented task boundary instead of expanding into adjacent work.

## Core Capabilities

### 1. Spoken Word Transformation

Convert written text to conversational audio style:

```python
from scripts.audio_writer import AudioScriptWriter

writer = AudioScriptWriter()

# Transform written content
script = writer.convert_to_audio(
    source_text=research_paper,
    format="podcast",  # podcast, video, lecture, audiobook
    target_audience="medical_students",
    duration_minutes=15
)

print(script.spoken_text)
# Converts: "The pathophysiology of diabetes mellitus involves..."
# To: "So what exactly happens in diabetes? Well, it all starts when..."
```

**Transformation Rules:**
| Written Style | Audio Style | Example |
|---------------|-------------|---------|
| "Furthermore" | "Plus" | Less formal transitions |
| " et al." | "and their colleagues" | Expand abbreviations |
| Numbers in text | Spoken numbers | "15%" → "15 percent" |
| Long sentences | 15-20 word max | Break into digestible chunks |
| Passive voice | Active voice | "was observed" → "we saw" |
| Citations | Omit or footnote | "(Smith et al., 2024)" → [reference tone] |

### 2. Pronunciation Guide Generation

Create phonetic spelling for medical terms:

```python
# Generate pronunciation guide
pronunciation = writer.create_pronunciation_guide(
    text=script,
    include_phonetic=True,
    include_syllables=True
)

# Output:
# "Hyperlipidemia: hi-per-lip-i-DEE-mee-uh"
# "Metformin: met-FOR-min"
# "Atherosclerosis: ath-er-oh-skleh-ROH-sis"
```

**Guide Elements:**
- **Phonetic Spelling**: IPA or simplified phonetics
- **Syllable Breaks**: hy-per-ten-sion
- **Emphasis Marking**: Primary stress (CAPS), secondary stress
- **Alternative Pronunciations**: Regional variations (UK vs US)
- **Sound-Alikes**: "rhymes with..." for difficult terms

### 3. Timing and Pacing

Calculate speaking duration and mark pacing cues:

```python
# Analyze timing
timing = writer.calculate_timing(
    script=script,
    speaking_rate="conversational",  # slow, conversational, fast
    include_pauses=True
)

print(f"Estimated duration: {timing.duration_minutes} minutes")
print(f"Word count: {timing.word_count}")
print(f"Pace: {timing.words_per_minute} WPM")
```

**Speaking Rates:**
| Style | WPM | Use Case |
|-------|-----|----------|
| **Slow/Educational** | 120-130 | Patient education, complex topics |
| **Conversational** | 140-160 | Podcasts, general audience |
| **Fast/News** | 170-190 | Time-constrained content |
| **Variable** | Varies | Dynamic pacing with pauses |

**Pacing Cues:**
```
[BREATHE] - Brief pause for narrator
[PAUSE 2s] - Two-second pause for emphasis
[SLOW DOWN] - Reduce pace for key point
[SPEED UP] - Increase energy/excitement
[BEAT] - Dramatic pause
```

### 4. Multi-Format Templates

Generate scripts for different audio formats:

```python
# Podcast episode
podcast = writer.create_podcast_script(
    content=article,
    episode_format="interview",  # solo, interview, panel
    include_intro_music=True,
    ad_breaks=[5, 12]  # minutes
)

# Educational video
video = writer.create_video_script(
    content=lecture_slides,
    visual_cues=True,  # Mark where visuals change
    b_roll_notes=True  # Suggest supplemental footage
)
```

**Format Types:**
| Format | Characteristics | Best For |
|--------|-----------------|----------|
| **Podcast** | Conversational, segments, ads | Long-form content, interviews |
| **Video** | Visual cues, B-roll notes | YouTube, educational platforms |
| **Lecture** | Structured, Q&A breaks | Online courses, training |
| **Audiobook** | Chapter markers, consistent tone | Textbooks, memoirs |
| **News** | Tight, factual, quick | Research briefs, updates |

## Common Patterns

### Pattern 1: Research Paper to Podcast

**Scenario**: Convert published study to 15-minute podcast episode.

```text
# Convert paper to podcast script
python scripts/main.py \
  --input paper.pdf \
  --format podcast \
  --duration 15 \
  --style conversational \
  --include-intro-outro \
  --output podcast_script.txt

# Generate pronunciation guide
python scripts/main.py \
  --input podcast_script.txt \
  --generate-pronunciation \
  --output pronunciation_guide.txt
```

**Structure:**
```
[INTRO MUSIC 5s]

HOST: Welcome to Medical Research Today. I'm your host...

[BREATHE]

HOST: Today we're diving into a fascinating study about...

[PAUSE]

HOST: So what did the researchers find? Well...

[BREATHE]

HOST: Dr. Smith, one of the study authors, explains...

[SOUND BITE: Interview clip]

...

[OUTRO MUSIC]
```

### Pattern 2: Medical Lecture Recording

**Scenario**: Convert lecture notes to video script for online course.

```python
# Create lecture script
lecture = writer.create_lecture_script(
    notes=lecture_content,
    duration=45,  # minutes
    break_intervals=[15, 30],  # minutes for student breaks
    interaction_points=True  # "Pause and think..." prompts
)

# Add visual cues
script = writer.add_visual_cues(
    script=lecture,
    slide_transitions=True,
    animation_notes=True
)
```

**Lecture Elements:**
- Learning objectives at start
- Periodic comprehension checks
- Break reminders
- Transition phrases between topics
- Summary and key takeaways

### Pattern 3: Patient Education Audio

**Scenario**: Create audio guide for diabetes management.

```python
# Patient-friendly script
patient_script = writer.create_patient_script(
    medical_content=diabetes_guide,
    reading_level=6,  # 6th grade
    empathetic_tone=True,
    key_points_highlighted=True
)

# Slow, clear pacing
patient_script.adjust_pacing(
    wpm=130,
    pause_after_sentences=1.5  # seconds
)
```

**Patient Script Features:**
- Simple language (avoid medical jargon)
- Empathetic tone
- Clear action steps
- Reassuring statements
- Repetition of key points

### Pattern 4: Conference Presentation to Video

**Scenario**: Adapt live presentation to YouTube video format.

```text
# Convert presentation script
python scripts/main.py \
  --input presentation_transcript.txt \
  --format video \
  --platform youtube \
  --include-hooks true \
  --engagement-cues true \
  --output youtube_script.txt
```

**YouTube Optimization:**
- Hook in first 30 seconds
- Engagement questions for comments
- Call to action (subscribe, like)
- Timestamp markers for chapters
- B-roll suggestions for visual interest

## Complete Workflow Example

**From research paper to published podcast:**

```text
# Step 1: Extract and summarize content
python scripts/main.py \
  --input paper.pdf \
  --extract-key-points \
  --output key_points.txt

# Step 2: Convert to audio script
python scripts/main.py \
  --input key_points.txt \
  --format podcast \
  --duration 20 \
  --output raw_script.txt

# Step 3: Add production elements
python scripts/main.py \
  --input raw_script.txt \
  --add-music-cues \
  --add-sound-effects \
  --add-pacing-marks \
  --output production_script.txt

# Step 4: Generate pronunciation guide
python scripts/main.py \
  --input production_script.txt \
  --generate-pronunciation \
  --output pronunciations.txt

# Step 5: Create timing breakdown
python scripts/main.py \
  --input production_script.txt \
  --calculate-timing \
  --output timing_breakdown.txt
```

**Python API:**

```python
from scripts.audio_writer import AudioScriptWriter
from scripts.pronunciation import PronunciationGuide
from scripts.timing import TimingCalculator

# Initialize
writer = AudioScriptWriter()
pronouncer = PronunciationGuide()
timing = TimingCalculator()

# Read source material
with open("research_article.txt", "r") as f:
    content = f.read()

# Step 1: Convert to spoken format
script = writer.convert_to_audio(
    text=content,
    format="podcast",
    target_duration=15,  # minutes
    audience="general_medical"
)

# Step 2: Add production elements
script_with_cues = writer.add_production_cues(
    script=script,
    music_stings=True,
    transition_effects=True
)

# Step 3: Generate pronunciation guide
medical_terms = pronouncer.extract_terms(script_with_cues)
pronunciation_guide = pronouncer.create_guide(medical_terms)

# Step 4: Calculate timing
timing_analysis = timing.calculate(
    script=script_with_cues,
    speaking_rate=150  # WPM
)

# Export complete production package
writer.export_production_package(
    script=script_with_cues,
    pronunciation=pronunciation_guide,
    timing=timing_analysis,
    output_dir="podcast_production/"
)
```

## Quality Checklist

**Content Quality:**
- [ ] Written content accurate and current
- [ ] Sources cited (even if not spoken)
- [ ] Medical facts verified by expert
- [ ] Appropriate for target audience level
- [ ] No confidential patient information

**Audio Optimization:**
- [ ] Sentences 15-20 words maximum
- [ ] Abbreviations expanded on first use
- [ ] Complex terms have pronunciation guides
- [ ] Active voice preferred over passive
- [ ] Transitions smooth and conversational

**Production Quality:**
- [ ] Timing realistic for content density
- [ ] Pacing cues appropriate for subject
- [ ] Music/sound cues marked clearly
- [ ] Pronunciation guide comprehensive
- [ ] Script formatted for easy reading

**Before Recording:**
- [ ] **CRITICAL**: Script read aloud for flow
- [ ] Difficult pronunciations practiced
- [ ] Timing tested with stopwatch
- [ ] Technical terms confirmed with subject expert
- [ ] Copyright cleared for any quoted material

## Common Pitfalls

**Content Issues:**
- ❌ **Too dense** → Information overload for listeners
  - ✅ Break complex topics into multiple episodes

- ❌ **Visual dependencies** → "As shown in Figure 3..."
  - ✅ Describe visuals or omit visual-dependent content

- ❌ **Citation overload** → Every sentence has reference
  - ✅ Save citations for show notes, not narration

**Audio Issues:**
- ❌ **Written-style language** → "Furthermore, the aforementioned..."
  - ✅ Conversational: "Plus, this thing we talked about..."

- ❌ **No pauses** → Relentless information delivery
  - ✅ Build in breathing room; let points sink in

- ❌ **Ignoring pronunciation** → Mispronounced medical terms
  - ✅ Research and practice all technical terms

**Production Issues:**
- ❌ **Underestimating time** → 10 minutes of script takes 12+ to record
  - ✅ Add 20% buffer for retakes and natural pacing

- ❌ **Complex sentence structures** → Tongue twisters for narrator
  - ✅ Short sentences; avoid nested clauses

## References

Available in `references/` directory:

- `audio_writing_best_practices.md` - Broadcast writing guidelines
- `medical_pronunciation_guide.md` - Common terms phonetics
- `podcast_production_standards.md` - Industry format standards
- `accessibility_guidelines.md` - Inclusive audio content
- `platform_requirements.md` - YouTube, Spotify, Apple specs
- `voice_care_tips.md` - Narrator health and performance

## Scripts

Located in `scripts/` directory:

- `main.py` - CLI interface for script conversion
- `audio_writer.py` - Core text-to-audio transformation
- `pronunciation.py` - Medical terminology phonetics
- `timing.py` - Duration calculation and pacing
- `format_templates.py` - Podcast, video, lecture templates
- `voice_direction.py` - Narrator cues and direction
- `accessibility.py` - Alternative format generation

## Limitations

- **Voice Performance**: Script is text only; actual delivery varies by narrator
- **Accent Variations**: Pronunciation guides may not match all dialects
- **Cultural Context**: Humor and references may not translate across cultures
- **Copyright**: Cannot use copyrighted material without permission
- **Technical Accuracy**: Does not verify medical content (input-dependent)
- **Live Elements**: Cannot script unscripted interviews or Q&A

## Parameters

| Parameter | Type | Default | Required | Description |
|-----------|------|---------|----------|-------------|
| `--input`, `-i` | string | - | No | Input text file path |
| `--output`, `-o` | string | - | No | Output JSON file path (default: stdout) |
| `--text` | string | - | No | Direct text input (alternative to --input) |
| `--duration`, `-d` | int | 5 | No | Target duration in minutes |
| `--pace`, `-p` | string | normal | No | Speaking pace (slow, normal, fast) |
| `--style`, `-s` | string | conversational | No | Script style (conversational, formal, educational) |

## Usage

### Basic Usage

```text
# Convert from file
python scripts/main.py --input article.txt --duration 5 --output script.json

# Direct text input
python scripts/main.py --text "Medical research findings..." --duration 3

# From stdin
cat article.txt | python scripts/main.py --duration 5 --style conversational

# With specific style and pace
python scripts/main.py --input paper.txt --style educational --pace slow
```

## Risk Assessment

| Risk Indicator | Assessment | Level |
|----------------|------------|-------|
| Code Execution | Python script executed locally | Low |
| Network Access | No external API calls | Low |
| File System Access | Read input files, write output files | Low |
| Instruction Tampering | Standard prompt guidelines | Low |
| Data Exposure | Output saved only to specified location | Low |

## Security Checklist

- [x] No hardcoded credentials or API keys
- [x] No unauthorized file system access
- [x] Output does not expose sensitive information
- [x] Prompt injection protections in place
- [x] Input validation for file paths
- [x] Output directory restricted to workspace
- [x] Script execution in sandboxed environment

## Prerequisites

```text
# Python 3.7+
# No additional packages required (uses standard library)
```

## Evaluation Criteria

### Success Metrics
- [x] Successfully converts text to audio-optimized script
- [x] Expands abbreviations and converts numbers to words
- [x] Calculates estimated duration based on word count
- [x] Applies style-specific formatting
- [x] Provides pronunciation notes for medical terms

### Test Cases
1. **Basic Conversion**: Convert text file → Returns audio script with metadata
2. **Abbreviation Handling**: Text with "e.g., i.e., etc." → All expanded in output
3. **Number Conversion**: Input with "1 in 4" → Output with "one in four"

## Lifecycle Status

- **Current Stage**: Draft
- **Next Review Date**: 2026-03-06
- **Known Issues**: None
- **Planned Improvements**:
  - Add support for custom abbreviation dictionaries
  - Integrate with text-to-speech engines
  - Add multilingual support

---

**🎙️ Pro Tip: The best audio scripts sound natural when spoken. Always read your script aloud before finalizing—if you stumble over a sentence, your narrator will too. Revise for the ear, not the eye.**

## Output Requirements

Every final response should make these items explicit when they are relevant:

- Objective or requested deliverable
- Inputs used and assumptions introduced
- Workflow or decision path
- Core result, recommendation, or artifact
- Constraints, risks, caveats, or validation needs
- Unresolved items and next-step checks

## Error Handling

- If required inputs are missing, state exactly which fields are missing and request only the minimum additional information.
- If the task goes outside the documented scope, stop instead of guessing or silently widening the assignment.
- If `scripts/main.py` fails, report the failure point, summarize what still can be completed safely, and provide a manual fallback.
- Do not fabricate files, citations, data, search results, or execution outcomes.

## Input Validation

This skill accepts requests that match the documented purpose of `audio-script-writer` and include enough context to complete the workflow safely.

Do not continue the workflow when the request is out of scope, missing a critical input, or would require unsupported assumptions. Instead respond:

> `audio-script-writer` only handles its documented workflow. Please provide the missing required inputs or switch to a more suitable skill.

## Response Template

Use the following fixed structure for non-trivial requests:

1. Objective
2. Inputs Received
3. Assumptions
4. Workflow
5. Deliverable
6. Risks and Limits
7. Next Checks

If the request is simple, you may compress the structure, but still keep assumptions and limits explicit when they affect correctness.
