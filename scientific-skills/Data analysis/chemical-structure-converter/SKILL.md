---
name: chemical-structure-converter
description: Convert between IUPAC names, SMILES strings, and molecular formulas for chemical compounds. Supports structure validation, identifier interconversion, and cheminformatics data preparation for drug discovery and chemical research workflows.
license: MIT
skill-author: AIPOCH
---
# Chemical Structure Converter

Interconvert between different chemical structure representations including IUPAC names, SMILES strings, molecular formulas, and common names. Essential for cheminformatics workflows, database standardization, and compound registration in drug discovery and chemical research.

**Key Capabilities:**
- **Multi-Format Conversion**: Convert between IUPAC names, SMILES, InChI, and molecular formulas
- **SMILES Validation**: Validate SMILES syntax for structural correctness
- **Batch Processing**: Process multiple compounds for database standardization
- **Identifier Lookup**: Retrieve all available identifiers for known compounds
- **Structure Standardization**: Normalize chemical representations for consistency

---

## When to Use

- Use this skill when the task is to Convert between IUPAC names, SMILES strings, and molecular formulas for chemical compounds. Supports structure validation, identifier interconversion, and cheminformatics data preparation for drug discovery and chemical research workflows.
- Use this skill for data analysis tasks that require explicit assumptions, bounded scope, and a reproducible output format.
- Use this skill when you need a documented fallback path for missing inputs, execution errors, or partial evidence.

## Key Features

- Scope-focused workflow aligned to: Convert between IUPAC names, SMILES strings, and molecular formulas for chemical compounds. Supports structure validation, identifier interconversion, and cheminformatics data preparation for drug discovery and chemical research workflows.
- Packaged executable path(s): `scripts/main.py`.
- Reference material available in `references/` for task-specific guidance.
- Structured execution path designed to keep outputs consistent and reviewable.

## Dependencies

See `## Prerequisites` above for related details.

- `Python`: `3.10+`. Repository baseline for current packaged skills.
- `Third-party packages`: `not explicitly version-pinned in this skill package`. Add pinned versions if this skill needs stricter environment control.

## Example Usage

converter = ChemicalStructureConverter()
entry = standardize_compound_entry("aspirin", converter)

if entry:
    print("Standardized Entry:")
    for key, value in entry.items():
        print(f"  {key}: {value}")
```

**Standardization Rules:**

| Rule | Standard Form | Example |
|------|--------------|---------|
| **Common names** | Lowercase | "aspirin" not "Aspirin" |
| **IUPAC** | Full systematic name | "2-acetoxybenzoic acid" |
| **SMILES** | Canonical | No stereochemistry if unspecified |
| **Formula** | Hill system | C, H, then alphabetical |

**Best Practices:**
- ✅ **Use consistent naming** across entire database
- ✅ **Include CAS numbers** when available
- ✅ **Track version history** of structure assignments
- ✅ **Validate against PubChem** for known compounds

**Common Issues and Solutions:**

**Issue: Multiple valid representations**
- Symptom: Same compound has different standard forms
- Solution: Define canonicalization rules; use chemical validation

## Implementation Details

See `## Workflow` above for related details.

- Execution model: validate the request, choose the packaged workflow, and produce a bounded deliverable.
- Input controls: confirm the source files, scope limits, output format, and acceptance criteria before running any script.
- Primary implementation surface: `scripts/main.py`.
- Reference guidance: `references/` contains supporting rules, prompts, or checklists.
- Parameters to clarify first: input path, output path, scope filters, thresholds, and any domain-specific constraints.
- Output discipline: keep results reproducible, identify assumptions explicitly, and avoid undocumented side effects.

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

## Workflow

1. Confirm the user objective, required inputs, and non-negotiable constraints before doing detailed work.
2. Validate that the request matches the documented scope and stop early if the task would require unsupported assumptions.
3. Use the packaged script path or the documented reasoning path with only the inputs that are actually available.
4. Return a structured result that separates assumptions, deliverables, risks, and unresolved items.
5. If execution fails or inputs are incomplete, switch to the fallback path and state exactly what blocked full completion.

## Integration with Other Skills

**Upstream Skills:**
- `chemical-storage-sorter`: Classify chemicals by hazard group before storage registration
- `adme-property-predictor`: Convert structures to standardized formats before ADME prediction
- `safety-data-sheet-reader`: Extract chemical names from SDS for structure lookup

**Downstream Skills:**
- `molecular-docking-predictor`: Convert compound libraries to 3D structures for docking
- `bio-ontology-mapper`: Map chemical structures to standardized ontologies (ChEBI, PubChem)
- `lab-inventory-tracker`: Register standardized chemical identifiers in inventory

**Complete Workflow:**
```
Literature/Patent → chemical-structure-converter → adme-property-predictor → molecular-docking-predictor → Hit Selection
```

---

## Core Capabilities

### 1. Multi-Format Chemical Identifier Conversion

Convert chemical structures between different representation formats for database interoperability.

```python
from scripts.main import ChemicalStructureConverter

converter = ChemicalStructureConverter()

# Convert compound name to all available identifiers
chemical_name = "aspirin"
data = converter.name_to_identifiers(chemical_name)

if data:
    print(f"Compound: {chemical_name}")
    print(f"IUPAC Name: {data['iupac']}")
    print(f"SMILES: {data['smiles']}")
    print(f"Formula: {data['formula']}")
    print(f"Molecular Weight: {data['mw']} g/mol")

# Output:

# Compound: aspirin

# IUPAC Name: 2-acetoxybenzoic acid

# SMILES: CC(=O)Oc1ccccc1C(=O)O

# Formula: C9H8O4

# Molecular Weight: 180.16 g/mol
```

**Supported Conversions:**

| From → To | Method | Use Case |
|-----------|--------|----------|
| **Name → SMILES** | Database lookup | Literature to database |
| **SMILES → IUPAC** | Structure recognition | Machine to human readable |
| **IUPAC → SMILES** | Name parsing | Chemical registration |
| **SMILES → Formula** | Atom counting | Quick MW calculation |

**Best Practices:**
- ✅ **Use canonical SMILES** for database storage (ensures uniqueness)
- ✅ **Validate conversions** with known reference compounds
- ✅ **Preserve stereochemistry** during conversions (use @/@@ in SMILES)
- ✅ **Check tautomeric forms** - different representations may exist

**Common Issues and Solutions:**

**Issue: Compound not in local database**
- Symptom: Returns "Unknown structure" for valid compounds
- Solution: Use external databases (PubChem, ChemSpider APIs) for lookup; add common compounds to local database

**Issue: Multiple valid SMILES for same compound**
- Symptom: Different SMILES strings represent same molecule
- Solution: Use canonical SMILES generation (requires RDKit or similar)

### 2. SMILES String Validation

Validate SMILES syntax to ensure structural integrity before computational processing.

```python
from scripts.main import ChemicalStructureConverter

converter = ChemicalStructureConverter()

# Validate SMILES strings
smiles_examples = [
    "CC(=O)Oc1ccccc1C(=O)O",  # Aspirin - valid
    "CCO",                     # Ethanol - valid
    "C(=O",                    # Invalid - unclosed parenthesis
    "C1CCCCC",                 # Invalid - unclosed ring
]

for smiles in smiles_examples:
    is_valid, message = converter.validate_smiles(smiles)
    status = "✅ Valid" if is_valid else "❌ Invalid"
    print(f"{smiles:<30} {status}: {message}")

# Output:

# CC(=O)Oc1ccccc1C(=O)O        ✅ Valid: Valid SMILES syntax

# CCO                          ✅ Valid: Valid SMILES syntax

# C(=O                         ❌ Invalid: Mismatched parentheses

# C1CCCCC                      ❌ Invalid: Ring closure error
```

**Validation Checks:**

| Check | Description | Example Error |
|-------|-------------|---------------|
| **Parentheses** | Matching ( and ) | `C(=O` - missing closing |
| **Brackets** | Matching [ and ] | `[Na+` - missing closing |
| **Ring closures** | Matching digits | `C1CC` - ring not closed |
| **Atom validity** | Recognized elements | `@` - invalid character |
| **Valence** | Chemical validity | `C(C)(C)(C)(C)C` - 5 bonds to C |

**Best Practices:**
- ✅ **Always validate** SMILES before using in downstream tools
- ✅ **Check for aromaticity** (lowercase c,n,o in SMILES)
- ✅ **Verify stereochemistry** (@ symbols for chirality)
- ✅ **Use explicit hydrogens** when ambiguity exists

**Common Issues and Solutions:**

**Issue: Valid syntax but chemically impossible**
- Symptom: SMILES passes validation but structure is unrealistic
- Solution: Use chemical validation tools (RDKit SanitizeMol) for deeper checks

**Issue: Tautomeric ambiguity**
- Symptom: Keto/enol forms represented differently
- Solution: Use tautomer canonicalization if consistency required

### 3. Batch Structure Processing

Process multiple chemical structures simultaneously for database standardization.

```python
from scripts.main import ChemicalStructureConverter

converter = ChemicalStructureConverter()

# Batch process compound list
compound_list = [
    "aspirin",
    "caffeine", 
    "glucose",
    "ethanol",
    "unknown_compound"
]

results = []
for compound in compound_list:
    data = converter.name_to_identifiers(compound)
    if data:
        results.append({
            'name': compound,
            'iupac': data['iupac'],
            'smiles': data['smiles'],
            'formula': data['formula'],
            'mw': data['mw']
        })
    else:
        print(f"⚠️  Warning: '{compound}' not found in database")

# Display results table
print("\n" + "="*80)
print(f"{'Name':<20} {'Formula':<15} {'MW':<10} {'SMILES'}")
print("="*80)
for r in results:
    print(f"{r['name']:<20} {r['formula']:<15} {r['mw']:<10.2f} {r['smiles'][:40]}")
```

**Best Practices:**
- ✅ **Process in batches** of 100-1000 for large databases
- ✅ **Log missing compounds** for manual review
- ✅ **Export to CSV** for Excel/chemoinformatics tools
- ✅ **Include CAS numbers** when available for verification

**Common Issues and Solutions:**

**Issue: Synonym confusion**
- Symptom: Same compound listed multiple times with different names
- Solution: Use SMILES as unique key; deduplicate by structure

**Issue: Mixture or salt forms**
- Symptom: Structures with counterions or multiple components
- Solution: Process main component; flag mixtures for special handling

### 4. Molecular Formula and Properties

Extract molecular formulas and calculate basic properties from SMILES or names.

```python
from scripts.main import ChemicalStructureConverter

converter = ChemicalStructureConverter()

# Analyze compound properties
compounds = ["aspirin", "caffeine", "glucose"]

print("Molecular Properties:")
print("-" * 70)
print(f"{'Compound':<15} {'Formula':<12} {'MW (g/mol)':<12} {'Heavy Atoms'}")
print("-" * 70)

for name in compounds:
    data = converter.name_to_identifiers(name)
    if data:
        # Count heavy atoms (non-hydrogen) from formula
        formula = data['formula']
        heavy_atoms = sum(int(c) for c in formula if c.isdigit())
        if heavy_atoms == 0:  # Single atoms like C, O
            heavy_atoms = len([c for c in formula if c.isupper()])
        
        print(f"{name:<15} {data['formula']:<12} {data['mw']:<12.2f} {heavy_atoms}")
```

**Calculated Properties:**

| Property | Calculation | Use Case |
|----------|-------------|----------|
| **Molecular Weight** | Sum of atomic weights | Dosing, filtering |
| **Heavy Atoms** | Non-hydrogen atoms | Size estimation |
| **Formula** | Atom count from structure | Database indexing |
| **Rotatable Bonds** | Count rotatable bonds | Flexibility index |

**Best Practices:**
- ✅ **Include salt forms** in MW calculation if relevant
- ✅ **Check isotopic labeling** for specialized applications
- ✅ **Calculate elemental composition** for combustion analysis
- ✅ **Use exact mass** for mass spectrometry applications

**Common Issues and Solutions:**

**Issue: Hydrates and solvates**
- Symptom: Different MW for hydrate vs anhydrous forms
- Solution: Always specify form (e.g., "caffeine anhydrous")

### 5. Structure Standardization

Standardize chemical representations for database consistency.

```python
from scripts.main import ChemicalStructureConverter

def standardize_compound_entry(name: str, converter) -> dict:
    """
    Standardize compound entry with all identifiers.
    
    Returns standardized entry or None if not found.
    """
    data = converter.name_to_identifiers(name)
    
    if not data:
        return None
    
    # Create standardized entry
    standardized = {
        'common_name': name.lower(),
        'iupac_name': data['iupac'],
        'smiles': data['smiles'],
        'inchi': f"InChI=1S/{data['formula']}",  # Placeholder
        'molecular_formula': data['formula'],
        'molecular_weight': data['mw'],
        'standardized_date': '2026-02-09',
        'source': 'local_database'
    }
    
    return standardized

### 6. Chemical Database Integration

Prepare chemical data for import into cheminformatics databases.

```python
import json
from scripts.main import ChemicalStructureConverter

def prepare_database_import(compound_names: list, converter) -> list:
    """
    Prepare compound list for database import.
    
    Returns list of standardized database records.
    """
    records = []
    
    for name in compound_names:
        data = converter.name_to_identifiers(name)
        
        if data:
            record = {
                'compound_id': f"CMPD_{len(records)+1:04d}",
                'common_name': name,
                'iupac_name': data['iupac'],
                'smiles': data['smiles'],
                'molecular_formula': data['formula'],
                'molecular_weight': data['mw'],
                'status': 'active'
            }
            records.append(record)
        else:
            print(f"⚠️  Skipped: {name} (not in database)")
    
    return records

# Generate database import file
converter = ChemicalStructureConverter()
compounds = ["aspirin", "caffeine", "glucose", "ethanol"]

db_records = prepare_database_import(compounds, converter)

# Export to JSON for database import
with open('chemical_database_import.json', 'w') as f:
    json.dump(db_records, f, indent=2)

print(f"\nExported {len(db_records)} compounds to database import file")
```

**Database Schema Example:**

```sql
CREATE TABLE compounds (
    compound_id VARCHAR(20) PRIMARY KEY,
    common_name VARCHAR(255),
    iupac_name VARCHAR(500),
    smiles VARCHAR(1000),
    molecular_formula VARCHAR(50),
    molecular_weight DECIMAL(10,4),
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Best Practices:**
- ✅ **Use unique compound IDs** for internal tracking
- ✅ **Index SMILES column** for substructure searching
- ✅ **Include source information** for data provenance
- ✅ **Validate before import** to prevent duplicates

**Common Issues and Solutions:**

**Issue: Character encoding problems**
- Symptom: Special characters in IUPAC names corrupted
- Solution: Use UTF-8 encoding; escape special characters

---

## Complete Workflow Example

**From compound names to standardized database:**

```text

# Step 1: Convert single compound
python scripts/main.py --name aspirin

# Step 2: Validate SMILES
python scripts/main.py --smiles "CC(=O)Oc1ccccc1C(=O)O" --validate

# Step 3: Convert IUPAC to SMILES
python scripts/main.py --iupac "ethanol"

# Step 4: List available compounds
python scripts/main.py --list
```

**Python API Usage:**

```python
from scripts.main import ChemicalStructureConverter
import pandas as pd

def process_compound_library(
    compound_list: list,
    output_file: str = "compound_library.csv"
) -> pd.DataFrame:
    """
    Process compound library for cheminformatics analysis.
    
    Args:
        compound_list: List of compound names
        output_file: Output CSV filename
        
    Returns:
        DataFrame with standardized compound data
    """
    converter = ChemicalStructureConverter()
    
    records = []
    not_found = []
    
    print("Processing compound library...")
    print("="*60)
    
    for compound in compound_list:
        data = converter.name_to_identifiers(compound)
        
        if data:
            records.append({
                'name': compound,
                'iupac': data['iupac'],
                'smiles': data['smiles'],
                'formula': data['formula'],
                'mw': data['mw']
            })
            print(f"✅ {compound}")
        else:
            not_found.append(compound)
            print(f"❌ {compound} - not found")
    
    print("="*60)
    
    # Create DataFrame
    df = pd.DataFrame(records)
    
    # Export to CSV
    df.to_csv(output_file, index=False)
    print(f"\nExported {len(df)} compounds to {output_file}")
    
    if not_found:
        print(f"\n⚠️  {len(not_found)} compounds not found:")
        for comp in not_found:
            print(f"  - {comp}")
    
    return df

# Process library
library = ["aspirin", "caffeine", "glucose", "ethanol", "unknown_drug"]
df = process_compound_library(library, "my_library.csv")

print("\nLibrary Summary:")
print(f"Total compounds: {len(df)}")
print(f"Average MW: {df['mw'].mean():.2f} g/mol")
print(f"MW range: {df['mw'].min():.2f} - {df['mw'].max():.2f} g/mol")
```

**Expected Output Files:**

```
chemical_data/
├── compound_library.csv       # Standardized compound data
├── missing_compounds.txt      # List of compounds not found
├── database_import.json       # JSON format for database import
└── validation_report.txt      # SMILES validation results
```

---

## Common Patterns

### Pattern 1: Literature to Database Conversion

**Scenario**: Converting compound names from publications to SMILES for database entry.

```json
{
  "task": "literature_to_database",
  "source": "Journal article compound list",
  "input_format": "Common names and IUPAC",
  "output_format": "SMILES for database",
  "volume": "50 compounds",
  "quality_check": "Validate all SMILES"
}
```

**Workflow:**
1. Extract compound names from publication
2. Look up each compound in converter
3. Validate generated SMILES
4. Check for missing compounds
5. Manual lookup for missing entries
6. Export to database import format
7. Review and correct any errors

**Output Example:**
```
Literature Conversion Results:
  Total compounds: 50
  Successfully converted: 47 (94%)
  Manual review needed: 3
    - Compound_23: ambiguous name
    - Compound_31: salt form unclear
    - Compound_45: stereochemistry unspecified
  
Database ready: 47 compounds exported
```

### Pattern 2: Cheminformatics Pipeline Preparation

**Scenario**: Preparing compound library for virtual screening pipeline.

```json
{
  "task": "virtual_screening_prep",
  "library_size": "10,000 compounds",
  "source_formats": ["SDF", "SMILES", "MOL"],
  "target_format": "Canonical SMILES",
  "requirements": [
    "Validate all structures",
    "Remove duplicates",
    "Calculate properties",
    "Flag reactive groups"
  ]
}
```

**Workflow:**
1. Load compound library from various sources
2. Convert all to SMILES format
3. Validate SMILES syntax
4. Remove duplicates by canonical SMILES
5. Calculate molecular properties (MW, formula)
6. Filter by drug-like properties if needed
7. Export standardized library

**Output Example:**
```
Virtual Screening Library Preparation:
  Input: 10,000 compounds
  After validation: 9,847 (153 invalid SMILES removed)
  After deduplication: 9,520 (327 duplicates removed)
  
Property Distribution:
  MW range: 150-650 Da
  Average MW: 387.5 Da
  MW < 500: 8,234 compounds (86%)
  
Ready for docking: 9,520 compounds
```

### Pattern 3: Patent Compound Extraction

**Scenario**: Extracting and standardizing compounds from patent text.

```json
{
  "task": "patent_extraction",
  "source": "US Patent with IUPAC names",
  "compounds": "25 specific compounds",
  "challenge": "Complex IUPAC names",
  "output": "SMILES for SAR analysis"
}
```

**Workflow:**
1. Extract IUPAC names from patent text
2. Parse names using converter
3. Generate SMILES for each
4. Validate structures
5. Create SAR table with consistent formatting
6. Compare with known compounds
7. Flag novel structures

**Output Example:**
```
Patent Compound Extraction:
  Patent: US10,XXX,XXX
  Compounds extracted: 25
  Successfully converted: 22 (88%)
  
Novel compounds identified: 3
  - Compound A: New scaffold
  - Compound B: Known scaffold, new substitution
  - Compound C: Prodrug of known compound
  
SAR Table Generated: 22 compounds × 5 properties
```

### Pattern 4: Inventory Database Cleanup

**Scenario**: Standardizing existing chemical inventory with mixed naming.

```json
{
  "task": "inventory_cleanup",
  "current_state": "Mixed naming conventions",
  "compounds": "500 chemicals",
  "issues": [
    "Inconsistent naming",
    "Missing SMILES",
    "Duplicate entries"
  ]
}
```

**Workflow:**
1. Export current inventory to CSV
2. Parse compound names
3. Convert all to standard format
4. Identify duplicates by SMILES
5. Merge duplicate records
6. Add missing SMILES
7. Import cleaned data back

**Output Example:**
```
Inventory Cleanup Results:
  Original entries: 500
  Unique compounds: 487 (13 duplicates removed)
  
Standardization:
  - Common names standardized: 487
  - SMILES added: 423
  - IUPAC names added: 487
  - MW calculated: 487
  
Data Quality Improvement:
  Completeness: 65% → 100%
  Consistency: 40% → 98%
```

---

## Quality Checklist

**Pre-Conversion:**
- [ ] Verify compound names are spelled correctly
- [ ] Check for stereochemical information (R/S, E/Z)
- [ ] Note salt forms and hydrates
- [ ] Identify any ambiguous or generic names
- [ ] Prepare list of expected compounds for validation

**During Conversion:**
- [ ] Validate all generated SMILES
- [ ] Check stereochemistry preservation
- [ ] Verify molecular formulas match expected
- [ ] Confirm molecular weights reasonable
- [ ] Flag any compounds not found in database

**Post-Conversion:**
- [ ] Review all conversions for accuracy
- [ ] Manually verify random sample (5-10%)
- [ ] Check for duplicate structures
- [ ] Validate unique compound IDs
- [ ] Export in required format

**Database Import:**
- [ ] Test import with small subset first
- [ ] Verify foreign key constraints
- [ ] Check character encoding (UTF-8)
- [ ] Validate required fields populated
- [ ] Create backup before bulk import

---

## Common Pitfalls

**Input Data Issues:**
- ❌ **Ambiguous names** → Multiple compounds match name
  - ✅ Use CAS numbers or specific synonyms
  
- ❌ **Mixtures and salts** → Complex structures unclear
  - ✅ Specify components or use main active compound
  
- ❌ **Stereochemistry omitted** → Racemic vs pure unclear
  - ✅ Specify stereochemistry explicitly
  
- ❌ **Hydrates vs anhydrous** → Different molecular weights
  - ✅ Always specify form in compound name

**Conversion Errors:**
- ❌ **Invalid SMILES** → Unbalanced parentheses or brackets
  - ✅ Always validate SMILES after generation
  
- ❌ **Loss of stereochemistry** → Chiral centers become racemic
  - ✅ Check @ symbols preserved in SMILES
  
- ❌ **Tautomeric ambiguity** → Keto/enol forms differ
  - ✅ Use canonical tautomers for consistency
  
- ❌ **Aromaticity errors** → Kekulé vs aromatic forms
  - ✅ Use consistent aromatic representation

**Database Issues:**
- ❌ **Duplicate entries** → Same compound multiple times
  - ✅ Deduplicate by canonical SMILES
  
- ❌ **Character encoding** → Special characters corrupted
  - ✅ Use UTF-8 encoding throughout
  
- ❌ **Missing fields** → Required data not populated
  - ✅ Validate all required fields present
  
- ❌ **Inconsistent formatting** → Mixed naming conventions
  - ✅ Apply standardization rules uniformly

---

## Troubleshooting

**Problem: Compound not found in database**
- Symptoms: Returns None for valid compound name
- Causes:
  - Database limited to common compounds
  - Name variation not recognized
  - Very new or obscure compound
- Solutions:
  - Try alternative names or synonyms
  - Use external database (PubChem API)
  - Manually create entry for novel compounds

**Problem: SMILES validation fails**
- Symptoms: Valid-looking SMILES rejected
- Causes:
  - Unbalanced brackets/parentheses
  - Invalid atom symbols
  - Ring closure errors
- Solutions:
  - Check for typos in SMILES
  - Use SMILES visualization tool to debug
  - Generate SMILES from structure drawing

**Problem: Stereochemistry lost in conversion**
- Symptoms: Chiral compound becomes achiral
- Causes:
  - Stereochemistry not specified in input
  - Conversion tool ignores stereochemistry
  - Wrong SMILES format used
- Solutions:
  - Use isomeric SMILES with @ symbols
  - Check input has stereochemical info
  - Use tools that preserve stereochemistry

**Problem: Multiple SMILES for same compound**
- Symptoms: Same compound has different SMILES strings
- Causes:
  - Different tautomeric forms
  - Different aromatic representations
  - Different starting atoms
- Solutions:
  - Use canonical SMILES generation
  - Normalize tautomers
  - Use InChI for unique identification

**Problem: Molecular weight mismatch**
- Symptoms: Calculated MW differs from expected
- Causes:
  - Salt form included/excluded
  - Isotopic composition different
  - Hydrate form
- Solutions:
  - Specify exact compound form
  - Check formula calculation
  - Use exact mass for precision work

---

## References

Available in `references/` directory:

- (No reference files currently available for this skill)

**External Resources:**
- PubChem: https://pubchem.ncbi.nlm.nih.gov
- ChemSpider: http://www.chemspider.com
- SMILES Specification: http://opensmiles.org
- InChI Standard: https://www.inchi-trust.org
- RDKit Documentation: https://www.rdkit.org/docs/

---

## Scripts

Located in `scripts/` directory:

- `main.py` - Chemical structure conversion and validation engine

---

## Chemical Identifier Quick Reference

**SMILES Notation:**
- `C` = aliphatic carbon
- `c` = aromatic carbon
- `=` = double bond
- `#` = triple bond
- `()` = branching
- `[]` = explicit valence/charge
- `@` = anticlockwise (S)
- `@@` = clockwise (R)

**IUPAC Naming:**
- Use systematic nomenclature
- Specify stereochemistry (R/S, E/Z)
- Include salt forms when relevant
- Indicate hydration state

**Molecular Formula (Hill System):**
- C first, then H, then alphabetical
- Example: C6H12O6 (glucose)

## Parameters

| Parameter | Type | Default | Required | Description |
|-----------|------|---------|----------|-------------|
| `--name`, `-n` | string | - | No | Compound name |
| `--smiles`, `-s` | string | - | No | SMILES string |
| `--iupac`, `-i` | string | - | No | IUPAC name |
| `--validate` | flag | - | No | Validate SMILES syntax |
| `--list`, `-l` | flag | - | No | List available compounds |

## Usage

### Basic Usage

```text

# Convert by compound name
python scripts/main.py --name aspirin

# Convert SMILES to IUPAC
python scripts/main.py --smiles "CC(=O)Oc1ccccc1C(=O)O"

# Validate SMILES
python scripts/main.py --smiles "CCO" --validate

# List all compounds
python scripts/main.py --list
```

## Risk Assessment

| Risk Indicator | Assessment | Level |
|----------------|------------|-------|
| Code Execution | Python script executed locally | Low |
| Network Access | No external API calls | Low |
| File System Access | No file access | Low |
| Data Exposure | No sensitive data | Low |

## Security Checklist

- [x] No hardcoded credentials or API keys
- [x] No file system access
- [x] Input validation for chemical identifiers
- [x] Output does not expose sensitive information
- [x] Error messages sanitized
- [x] Script execution in sandboxed environment

## Prerequisites

```text

# Python 3.7+

# No additional packages required (uses standard library)
```

## Evaluation Criteria

### Success Metrics
- [x] Successfully converts between chemical formats
- [x] Validates SMILES syntax
- [x] Retrieves compound information by name
- [x] Lists available compounds

### Test Cases
1. **Name Lookup**: Aspirin → Returns SMILES, IUPAC, formula
2. **SMILES Conversion**: Valid SMILES → IUPAC name
3. **Validation**: Invalid SMILES → Error message

## Lifecycle Status

- **Current Stage**: Active
- **Next Review Date**: 2026-03-09
- **Known Issues**: Limited compound database (mock data)
- **Planned Improvements**:
  - Integrate with PubChem API
  - Add 2D/3D structure generation
  - Expand compound database

---

**Last Updated**: 2026-02-09  
**Skill ID**: 185  
**Version**: 2.0 (K-Dense Standard)

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

This skill accepts requests that match the documented purpose of `chemical-structure-converter` and include enough context to complete the workflow safely.

Do not continue the workflow when the request is out of scope, missing a critical input, or would require unsupported assumptions. Instead respond:

> `chemical-structure-converter` only handles its documented workflow. Please provide the missing required inputs or switch to a more suitable skill.

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

## Inputs to Collect

- Required inputs: the user goal, the primary data or source file, and the requested output format.
- Optional inputs: output directory, formatting preferences, and validation constraints.
- If a required input is unavailable, return a short clarification request before continuing.

## Output Contract

- Return a short summary, the main deliverables, and any assumptions that materially affect interpretation.
- If execution is partial, label what succeeded, what failed, and the next safe recovery step.
- Keep the final answer within the documented scope of the skill.

## Validation and Safety Rules

- Validate identifiers, file paths, and user-provided parameters before execution.
- Do not fabricate results, metrics, citations, or downstream conclusions.
- Use safe fallback behavior when dependencies, credentials, or required inputs are missing.
- Surface any execution failure with a concise diagnosis and recovery path.
