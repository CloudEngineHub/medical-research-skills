# idc-index Command-Line Interface Guide

The command-line tools provided by the `idc-index` package allow you to download DICOM data from NCI Imaging Data Commons (IDC) without writing Python code.

## Installation

```bash
pip install --upgrade idc-index
```

After installation, you can use the `idc` command in your terminal.

## Available Commands

| Command | Purpose |
|---------|---------|
| `idc download` | General download command with auto-detect input type |
| `idc download-from-manifest` | Download from manifest file with validation and progress tracking |
| `idc download-from-selection` | Download based on filter criteria with multiple selection options |

---

## idc download

General download command that intelligently parses input. It automatically determines whether input is a manifest file path or an identifier list (collection_id, PatientID, StudyInstanceUID, SeriesInstanceUID, crdc_series_uuid).

### Usage

```bash
# Download entire collection
idc download rider_pilot --download-dir ./data

# Download specific series by UID
idc download "1.3.6.1.4.1.9328.50.1.69736" --download-dir ./data

# Download multiple items (comma-separated)
idc download "tcga_luad,tcga_lusc" --download-dir ./data

# Download from manifest file (auto-detected by file extension)
idc download manifest.txt --download-dir ./data
```

### Options

| Option | Description |
|--------|-------------|
| `--download-dir` | Target directory (default: current directory) |
| `--dir-template` | Directory hierarchy template (default: `%collection_id/%PatientID/%StudyInstanceUID/%Modality_%SeriesInstanceUID`) |
| `--log-level` | Log level: debug, info, warning, error, critical |

### Directory Template Variables

Use these variables in `--dir-template` to organize downloaded data:

- `%collection_id` - Collection identifier
- `%PatientID` - Patient identifier
- `%StudyInstanceUID` - Study UID
- `%SeriesInstanceUID` - Series UID
- `%Modality` - Imaging modality (CT, MR, PT, etc.)

**Examples:**

```bash
# Flat structure (all files in same directory)
idc download rider_pilot --download-dir ./data --dir-template ""

# Simplified hierarchy
idc download rider_pilot --download-dir ./data --dir-template "%collection_id/%PatientID/%Modality"
```

---

## idc download-from-manifest

Specialized command for downloading from manifest files, with built-in validation, progress tracking, and resume capability.

### Usage

```bash
# Basic download from manifest file
idc download-from-manifest --manifest-file cohort.txt --download-dir ./data

# Show progress bar and validate
idc download-from-manifest --manifest-file cohort.txt --download-dir ./data --show-progress-bar

# Resume interrupted download using s5cmd sync
idc download-from-manifest --manifest-file cohort.txt --download-dir ./data --use-s5cmd-sync
```

### Options

| Option | Description |
|--------|-------------|
| `--manifest-file` | **Required.** Path to manifest file containing S3 URLs |
| `--download-dir` | **Required.** Target directory |
| `--validate-manifest` | Validate manifest before download (enabled by default) |
| `--show-progress-bar` | Show download progress |
| `--use-s5cmd-sync` | Enable resume - skip already downloaded files |
| `--quiet` | Suppress subprocess output |
| `--dir-template` | Directory hierarchy template |
| `--log-level` | Log verbosity |

### Manifest File Format

Manifest files contain S3 URLs, one per line:

```
s3://idc-open-data/cb09464a-c5cc-4428-9339-d7fa87cfe837/*
s3://idc-open-data/88f3990d-bdef-49cd-9b2b-4787767240f2/*
```

**How to get manifest files:**

1. **IDC Portal**: Export selected cohort as manifest
2. **Python Query**: Generate from SQL results

```python
from idc_index import IDCClient

client = IDCClient()
# Execute SQL query to get S3 URLs
results = client.sql_query("""
    SELECT series_aws_url
    FROM index
    WHERE collection_id = 'rider_pilot' AND Modality = 'CT'
""")

with open('ct_manifest.txt', 'w') as f:
    for url in results['series_aws_url']:
        f.write(url + '\n')
```

---

## idc download-from-selection

Download data using filter criteria. Filters are applied in sequence.

### Usage

```bash
# Download by collection
idc download-from-selection --collection-id rider_pilot --download-dir ./data

# Download specific series
idc download-from-selection --series-instance-uid "1.3.6.1.4.1.9328.50.1.69736" --download-dir ./data

# Combine multiple filters
idc download-from-selection --collection-id nlst --patient-id "100004" --download-dir ./data

# Dry run - see what would be downloaded without actually downloading
idc download-from-selection --collection-id tcga_luad --dry-run --download-dir ./data
```

### Options

| Option | Description |
|--------|-------------|
| `--download-dir` | **Required.** Target directory |
| `--collection-id` | Filter by collection identifier |
| `--patient-id` | Filter by patient identifier |
| `--study-instance-uid` | Filter by study UID |
| `--series-instance-uid` | Filter by series UID |
| `--crdc-series-uuid` | Filter by CRDC UUID |
| `--dry-run` | Calculate cohort size without downloading |
| `--show-progress-bar` | Show download progress |
| `--use-s5cmd-sync` | Enable resume |
| `--dir-template` | Directory hierarchy template |

### Using Dry Run to Estimate Size

Before downloading, use `--dry-run` to estimate download size:

```bash
idc download-from-selection --collection-id nlst --dry-run --download-dir ./data
```

This will show:
- Number of series matching the filter criteria
- Total download size
- No files will be downloaded

---

## Common Workflows

### 1. Download Small Collection for Testing

```bash
# rider_pilot is ~1GB - perfect for testing
idc download rider_pilot --download-dir ./test_data
```

### 2. Large Dataset Download with Progress and Resume

```bash
# Use s5cmd sync for large downloads - can resume if interrupted
idc download-from-selection \
    --collection-id nlst \
    --download-dir ./nlst_data \
    --show-progress-bar \
    --use-s5cmd-sync
```

### 3. Estimate Size Before Downloading

```bash
# Check size first
idc download-from-selection --collection-id tcga_luad --dry-run --download-dir ./data

# If size is acceptable, proceed with download
idc download-from-selection --collection-id tcga_luad --download-dir ./data
```

### 4. Download Specific Modality Data via Python + CLI

```python
# First, query series UIDs in Python
from idc_index import IDCClient

client = IDCClient()
results = client.sql_query("""
    SELECT SeriesInstanceUID
    FROM index
    WHERE collection_id = 'nlst'
      AND Modality = 'CT'
      AND BodyPartExamined = 'CHEST'
    LIMIT 50
""")

# Save to manifest file
results['SeriesInstanceUID'].to_csv('my_series.csv', index=False, header=False)
```

```bash
# Then download via CLI
idc download my_series.csv --download-dir ./lung_ct
```

---

## Built-in Security Features

This CLI includes several security features:

- **Disk space check:** Verifies sufficient storage space before starting downloads.
- **Manifest validation:** Validates manifest file format by default.
- **Progress tracking:** Provides optional progress bars for monitoring large downloads.
- **Resume capability:** Use `--use-s5cmd-sync` to resume interrupted downloads.

---

## Troubleshooting

### Download Interrupted

Use `--use-s5cmd-sync` to resume:

```bash
idc download-from-manifest --manifest-file cohort.txt --download-dir ./data --use-s5cmd-sync
```

### Connection Timeout

For unstable networks, it is recommended to split the task into smaller batches using Python to generate multiple manifests, then download them sequentially.

---

## See Also

- [idc-index Documentation](https://idc-index.readthedocs.io/)
- [IDC Portal](https://portal.imaging.datacommons.cancer.gov/) - Interactive cohort building
- [IDC Tutorials](https://github.com/ImagingDataCommons/IDC-Tutorials)
