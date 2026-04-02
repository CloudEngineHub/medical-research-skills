---
name: antibody-humanizer
description: Humanize murine antibody sequences using CDR grafting and framework.
license: MIT
skill-author: AIPOCH
---
# Antibody Humanizer

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
python scripts/main.py -h
```

## Workflow

1. Confirm the user objective, required inputs, and non-negotiable constraints before doing detailed work.
2. Validate that the request matches the documented scope and stop early if the task would require unsupported assumptions.
3. Use the packaged script path or the documented reasoning path with only the inputs that are actually available.
4. Return a structured result that separates assumptions, deliverables, risks, and unresolved items.
5. If execution fails or inputs are incomplete, switch to the fallback path and state exactly what blocked full completion.

## Overview

Bioinformatics platform for converting murine antibodies into humanized variants by grafting complementarity-determining regions (CDRs) onto human framework templates while preserving antigen-binding affinity and reducing immunogenicity risk.

**Key Capabilities:**
- **CDR Identification**: Automatic CDR boundary detection (Kabat/Chothia/IMGT schemes)
- **Framework Matching**: Database search for optimal human germline templates
- **Humanization Scoring**: Multi-parameter immunogenicity risk assessment
- **Back-Mutation Prediction**: Identify critical framework residues for retention
- **Batch Processing**: Humanize multiple antibody candidates efficiently
- **Immunogenicity Assessment**: T-cell epitope and humanness scoring

## When to Use

- Use this skill when the task needs Humanize murine antibody sequences using CDR grafting and framework.
- Use this skill for protocol design tasks that require explicit assumptions, bounded scope, and a reproducible output format.
- Use this skill when you need a documented fallback path for missing inputs, execution errors, or partial evidence.

## References

- [references/audit-reference.md](references/audit-reference.md) - Supported humanization scope, audit commands, and fallback boundaries

## Core Capabilities

### 1. CDR Region Identification

Parse antibody sequences and identify CDR boundaries:

```python
from scripts.humanizer import AntibodyHumanizer

humanizer = AntibodyHumanizer()

# Analyze antibody sequence
analysis = humanizer.analyze_sequence(
    vh_sequence="QVQLQQSGPELVKPGASVKISCKASGYTFTDYYMHWVKQSHGKSLEWIGYINPSTGYTEYNQKFKDKATLTVDKSSSTAYMQLSSLTSEDSAVYYCAR...",
    vl_sequence="DIQMTQSPSSLSASVGDRVTITCRASQGISSWLAWYQQKPGKAPKLLIYKASSLESGVPSRFSGSGSGTDFTLTISSLQPEDFATYYCQQYSSYPYT...",
    scheme="chothia"  # Options: kabat, chothia, imgt
)

# Output CDR locations
print(analysis.cdr_regions)
# {
#   "VH_CDR1": {"start": 26, "end": 32, "seq": "GYTFTDY"},
#   "VH_CDR2": {"start": 52, "end": 58, "seq": "INPSTGY"},
#   ...
# }
```

**Numbering Schemes:**
| Scheme | VH CDR1 | VH CDR2 | VH CDR3 | Best For |
|--------|---------|---------|---------|----------|
| **Chothia** | 26-32 | 52-56 | 95-102 | Structural analysis |
| **Kabat** | 31-35 | 50-65 | 95-102 | Sequence-based work |
| **IMGT** | 27-38 | 56-65 | 105-117 | Standardized analysis |

### 2. Human Framework Matching

Identify optimal human germline templates:

```python
# Match against human germline database
matches = humanizer.find_human_frameworks(
    vh_framework=analysis.vh_frameworks,
    vl_framework=analysis.vl_frameworks,
    top_n=5,
    criteria=["homology", "canonical_structure", "vernier_similarity"]
)

# Evaluate each candidate
for match in matches:
    print(f"Template: {match.germline_genes}")
    print(f"Homology: {match.homology:.2%}")
    print(f"Vernier Score: {match.vernier_score:.1f}")
    print(f"Risk Level: {match.immunogenicity_risk}")
```

**Matching Criteria:**
- **Sequence Homology**: Percent identity to human germline
- **Canonical Structure**: Loop conformation compatibility
- **Vernier Region**: Framework residues contacting CDRs
- **Interface Residues**: Packing interactions with CDRs

### 3. Humanization Scoring

Assess immunogenicity risk of candidates:

```python
# Score humanization candidates
scores = humanizer.score_candidates(
    murine_antibody=analysis,
    human_templates=matches,
    scoring_methods=["t20", "h_score", "germline_deviation", "paratope_diversity"]
)

# Rank by overall score
ranked = scores.rank_by_composite_score(
    weights={"humanness": 0.4, "binding_retention": 0.4, "developability": 0.2}
)
```

**Scoring Methods:**
| Method | Description | Target |
|--------|-------------|--------|
| **T20 Score** | 20-mer peptide humanization | >80% human |
| **H-Score** | Hummerblind germline distance | <15 mutations |
| **Paratope Diversity** | CDR germline gene diversity | Low diversity |
| **Developability** | Aggregation/pH stability prediction | High score |

### 4. Back-Mutation Prediction

Identify critical residues to retain from murine framework:

```python
# Predict back-mutations
back_mutations = humanizer.predict_back_mutations(
    murine_vh=analysis.vh_sequence,
    human_vh=matches[0].human_template,
    cdr_regions=analysis.cdr_regions,
    rationale_required=True
)

# Output shows position-specific recommendations
for mutation in back_mutations:
    print(f"Position {mutation.position}: {mutation.human_aa} → {mutation.murine_aa}")
    print(f"Rationale: {mutation.reason}")  # e.g., "Vernier region contact"
    print(f"Priority: {mutation.priority}")  # Critical/Important/Optional
```

**Critical Residue Classes:**
- **Vernier Positions**: Framework residues contacting CDRs (VH 24, 71, 94)
- **Interface Packs**: Residue packing between VH and VL
- **Canonical Anchors**: Cysteines and conserved framework positions
- ** Buried Positions**: Core packing residues affecting stability

## Quality Checklist

**Input Quality:**
- [ ] VH and VL sequences complete (110-130 aa typical)
- [ ] No ambiguous residues (B, Z, X)
- [ ] Signal peptide removed
- [ ] Constant region removed (variable region only)

**Humanization Assessment:**
- [ ] CDR boundaries correctly identified
- [ ] Human framework homology >80%
- [ ] T20 score >75 (high humanness)
- [ ] Vernier positions analyzed for back-mutations
- [ ] Interface residues checked for packing

**Output Validation:**
- [ ] Humanized sequence valid (no stop codons)
- [ ] CDRs preserved exactly
- [ ] Framework length conserved
- [ ] Back-mutations documented with rationale
- [ ] **CRITICAL**: Immunogenicity risk assessed

**Before Experimental Work:**
- [ ] **CRITICAL**: Top 2-3 candidates selected for expression
- [ ] Binding affinity to be tested (ELISA/Biacore)
- [ ] Stability assessed (thermal/aggregation)
- [ ] Immunogenicity in vitro assays planned

## Common Pitfalls

**Sequence Issues:**
- ❌ **Incomplete sequences** → Missing framework regions
  - ✅ Ensure full VH/VL variable domains provided
  
- ❌ **Wrong numbering scheme** → CDR boundaries incorrect
  - ✅ Verify scheme matches experimental data source

- ❌ **Non-standard residues** → Unusual amino acids
  - ✅ Clean sequences; remove signal peptides

**Design Issues:**
- ❌ **Over-humanization** → Losing antigen binding
  - ✅ Don't exceed 85-90% humanness; retain critical residues

- ❌ **Ignoring back-mutations** → Assuming 100% human framework works
  - ✅ Always predict and test back-mutations

- ❌ **Single candidate only** → No backup options
  - ✅ Generate 2-3 candidates with different frameworks

**Experimental Issues:**
- ❌ **Skipping binding validation** → Assuming in silico = in vivo
  - ✅ Always confirm antigen binding experimentally

- ❌ **Ignoring developability** → Aggregation or instability
  - ✅ Check for problematic residues (unpaired cysteines, hydrophobic patches)

## References

Available in `references/` directory:

- `imgt_germline_database.md` - Human germline gene reference sequences
- `cdr_numbering_schemes.md` - Kabat, Chothia, IMGT comparison
- `humanization_case_studies.md` - Successful therapeutic examples
- `vernier_positions_guide.md` - Critical framework residues
- `immunogenicity_assessment.md` - T-cell epitope prediction methods
- `patent_landscape.md` - Humanization IP considerations

## Scripts

Located in `scripts/` directory:

- `main.py` - CLI interface for humanization
- `humanizer.py` - Core humanization engine
- `cdr_parser.py` - CDR identification and numbering
- `framework_matcher.py` - Human germline database search
- `scoring.py` - Humanization quality assessment
- `backmutation.py` - Critical residue prediction
- `batch_processor.py` - Multiple antibody screening
- `structure_predictor.py` - CDR conformation analysis

## Limitations

- **Binding Prediction**: Cannot accurately predict impact on antigen affinity
- **Developability**: Limited prediction of aggregation or stability issues
- **Immunogenicity**: In silico T-cell epitope prediction has false positives
- **Non-Standard Antibodies**: May not handle camelid, shark, or engineered scaffolds
- **Experimental Validation Required**: All predictions must be confirmed in vitro/vivo
- **Intellectual Property**: Does not check for existing patent claims on sequences

## Parameters

| Parameter | Type | Default | Required | Description |
|-----------|------|---------|----------|-------------|
| `--vh` | string | - | No | Murine VH sequence (amino acids) |
| `--vl` | string | - | No | Murine VL sequence (amino acids) |
| `--input`, `-i` | string | - | No | Input JSON file path |
| `--name`, `-n` | string | "" | No | Antibody name |
| `--output`, `-o` | string | - | No | Output file path |
| `--format`, `-f` | string | json | No | Output format (json, fasta, csv) |
| `--scheme`, `-s` | string | chothia | No | Numbering scheme (kabat, chothia, imgt) |
| `--top-n` | int | 3 | No | Number of best candidates to return |

## Usage

### Basic Usage

```text
# Humanize with direct sequence input
python scripts/main.py --vh "QVQLQQSGPELVKPGASVKMSCKAS..." --vl "DIQMTQSPSSLSASVGDRVTITC..." --name "MyAntibody"

# Use JSON input file
python scripts/main.py --input antibody.json --output results.json

# Use IMGT numbering scheme
python scripts/main.py --vh "SEQUENCE" --vl "SEQUENCE" --scheme imgt
```

### Input JSON Format

```json
{
  "vh_sequence": "QVQLQQSGPELVKPGASVKMSCKAS...",
  "vl_sequence": "DIQMTQSPSSLSASVGDRVTITC...",
  "name": "MyAntibody",
  "scheme": "chothia"
}
```

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

This skill accepts requests that match the documented purpose of `antibody-humanizer` and include enough context to complete the workflow safely.

Do not continue the workflow when the request is out of scope, missing a critical input, or would require unsupported assumptions. Instead respond:

> `antibody-humanizer` only handles its documented workflow. Please provide the missing required inputs or switch to a more suitable skill.

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
