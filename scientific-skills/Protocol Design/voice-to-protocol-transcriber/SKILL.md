---
name: voice-to-protocol-transcriber
description: Record experimental procedures and observations via voice commands during.
license: MIT
skill-author: AIPOCH
---
# Voice-to-Protocol Transcriber

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
```

## When to Use

- Use this skill when the task needs Record experimental procedures and observations via voice commands during.
- Use this skill for protocol design tasks that require explicit assumptions, bounded scope, and a reproducible output format.
- Use this skill when you need a documented fallback path for missing inputs, execution errors, or partial evidence.

## Workflow

1. Confirm the user objective, required inputs, and non-negotiable constraints before doing detailed work.
2. Validate that the request matches the documented scope and stop early if the task would require unsupported assumptions.
3. Use the packaged script path or the documented reasoning path with only the inputs that are actually available.
4. Return a structured result that separates assumptions, deliverables, risks, and unresolved items.
5. If execution fails or inputs are incomplete, switch to the fallback path and state exactly what blocked full completion.

## Description

Record operation steps and observations via voice commands during experiments. Suitable for laboratory environments, helping researchers transcribe experimental operations in real-time and generate structured experiment records.

## Use Cases

- Chemistry experiment operation recording
- Biology experiment step tracking
- Physics experiment data recording
- Clinical experiment operation logging
- Any scenario requiring real-time step recording

## Dependencies

```text
pip install speechrecognition pyaudio pydub python-docx
```

## Configuration

Configure in `~/.openclaw/config/voice-to-protocol-transcriber.json`:

```json
{
  "language": "zh-CN",
  "output_format": "markdown",
  "auto_save_interval": 60,
  "save_directory": "~/Documents/Experiment-Protocols",
  "experiment_name": "default",
  "enable_timestamp": true,
  "voice_commands": {
    "start_recording": "开始记录",
    "stop_recording": "停止记录",
    "add_observation": "观察到",
    "add_step": "步骤",
    "save_protocol": "保存记录",
    "add_note": "备注"
  }
}
```

## Usage

### Basic Usage

```text
openclaw skill voice-to-protocol-transcriber --config config.json
```

### Quick Start

```text
# Start voice recording
openclaw skill voice-to-protocol-transcriber --experiment "Cell Culture Experiment-2024-02-06"

# Use specific language
openclaw skill voice-to-protocol-transcriber --lang en-US
```

### Voice Commands

| Command | Description |
|------|------|
| "Start Recording" | Start voice recognition and recording |
| "Step [content]" | Add an experiment step |
| "Observed [content]" | Add observation results |
| "Note [content]" | Add additional notes |
| "Save Record" | Save current experiment record |
| "Stop Recording" | End recording and save |

## Output Format

### Markdown Format

```markdown
# Experiment Record: [Experiment Name]

**Date**: 2024-02-06  
**Time**: 14:30:25  
**Recorder**: [User]

---

## Step 1
**Time**: 14:31:00  
**Operation**: [Voice transcription content]

## Observation 1
**Time**: 14:32:15  
**Content**: [Observation result]

## Note 1
**Time**: 14:35:00  
**Content**: [Note information]

---

*Experiment record ended at 14:45:00*
```

## API

### Python Call

```python
from skills.voice_to_protocol_transcriber import ProtocolTranscriber

# Initialize
transcriber = ProtocolTranscriber(
    experiment_name="My Experiment",
    language="zh-CN"
)

# Start listening
transcriber.start_listening()

# Add manual entry
transcriber.add_step("Prepare petri dish")
transcriber.add_observation("Culture medium became turbid")

# Save and stop
transcriber.save()
transcriber.stop()
```

## Features

- 🎙️ Real-time voice recognition
- 📝 Automatic classification (Step/Observation/Note)
- ⏱️ Automatic timestamps
- 💾 Auto-save
- 🌐 Multi-language support
- 📄 Multiple output formats (Markdown/Word/Plain Text)
- 🔇 Voice command control

## Notes

- First use requires microphone permission
- Recommended to use in quiet environments
- Chinese recognition requires good network connection
- Save regularly to avoid data loss

## Changelog

### 1.0.0
- Initial version release
- Support Chinese and English voice recognition
- Markdown and Word output formats
- Voice command control

## Risk Assessment

| Risk Indicator | Assessment | Level |
|----------------|------------|-------|
| Code Execution | Python/R scripts executed locally | Medium |
| Network Access | No external API calls | Low |
| File System Access | Read input files, write output files | Medium |
| Instruction Tampering | Standard prompt guidelines | Low |
| Data Exposure | Output files saved to workspace | Low |

## Security Checklist

- [ ] No hardcoded credentials or API keys
- [ ] No unauthorized file system access (../)
- [ ] Output does not expose sensitive information
- [ ] Prompt injection protections in place
- [ ] Input file paths validated (no ../ traversal)
- [ ] Output directory restricted to workspace
- [ ] Script execution in sandboxed environment
- [ ] Error messages sanitized (no stack traces exposed)
- [ ] Dependencies audited

## Prerequisites

```text
# Python dependencies
pip install -r requirements.txt
```

## Evaluation Criteria

### Success Metrics
- [ ] Successfully executes main functionality
- [ ] Output meets quality standards
- [ ] Handles edge cases gracefully
- [ ] Performance is acceptable

### Test Cases
1. **Basic Functionality**: Standard input → Expected output
2. **Edge Case**: Invalid input → Graceful error handling
3. **Performance**: Large dataset → Acceptable processing time

## Lifecycle Status

- **Current Stage**: Draft
- **Next Review Date**: 2026-03-06
- **Known Issues**: None
- **Planned Improvements**: 
  - Performance optimization
  - Additional feature support

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

This skill accepts requests that match the documented purpose of `voice-to-protocol-transcriber` and include enough context to complete the workflow safely.

Do not continue the workflow when the request is out of scope, missing a critical input, or would require unsupported assumptions. Instead respond:

> `voice-to-protocol-transcriber` only handles its documented workflow. Please provide the missing required inputs or switch to a more suitable skill.


## References

- [references/audit-reference.md](references/audit-reference.md) - Supported scope, audit commands, and fallback boundaries

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
