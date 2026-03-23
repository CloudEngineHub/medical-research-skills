# IDC Cloud Storage Guide

IDC stores all DICOM files in public cloud storage buckets, with synchronized mirrors between Google Cloud Storage (GCS) and AWS S3. This guide covers bucket organization, file structure, access methods, and versioning.

## When to Use Direct Cloud Storage Access

Use direct bucket access when you need:
- Maximum download performance through parallel transfer
- Integration with cloud-native workflows (e.g., running analysis on cloud VMs)
- Programmatic access via tools like `s5cmd` or `gsutil`
- Access to specific file versions for reproducibility

For most use cases, `idc-index` is simpler and recommended—it internally uses `s5cmd` to download from these S3 buckets and handles UUID lookup automatically. Use direct cloud storage when you need raw file access, custom parallelization, or building cloud-native pipelines.

## Buckets

IDC organizes data across multiple buckets based on license agreements and content type. All buckets are mirrored between AWS and GCS with identical content and file paths.

### Bucket Overview

| Purpose | AWS S3 Bucket | GCS Bucket | License | Content |
|---------|---------------|------------|---------|---------|
| Primary data | `idc-open-data` | `idc-open-data` | No commercial restrictions | >90% of IDC data |
| Head scans | `idc-open-data-two` | `idc-open-idc1` | No commercial restrictions | Collections that may contain head imaging |
| Commercial restricted | `idc-open-data-cr` | `idc-open-cr` | Commercial use restricted (CC BY-NC) | ~4% of data |

**Notes:**
- All AWS buckets are in AWS region `us-east-1`
- Before IDC v19, GCS used `public-datasets-idc` (now replaced by `idc-open-data`)
- Head scan buckets exist to comply with potential future policies regarding facial imaging data
- **Important:** Use `idc-index` to get license info—don't rely on bucket names!

### Why Multiple Buckets?

1. **License isolation:** Data with commercial use restrictions (CC BY-NC) is isolated in `idc-open-data-cr` / `idc-open-cr` to prevent accidental commercial use.
2. **Head scan handling:** Collections marked by TCIA as potentially containing head scans are stored in separate buckets (`idc-open-data-two` / `idc-open-idc1`) for potential future policy compliance.
3. **Historical reasons:** Bucket structure evolved as IDC grew and partnered with different cloud programs.

## File Organization Within Buckets

Files are organized by CRDC UUID, not DICOM UID. This enables versioning while maintaining consistent paths across cloud providers.

### Directory Structure

```
<bucket>/<crdc_series_uuid>/
├── <crdc_instance_uuid_1>.dcm
├── <crdc_instance_uuid_2>.dcm└── ...
```

**Example Path:**
```
s3://idc-open-data/7a6b2389-53c6-4c5b-b07f-6d1ed4a3eed9/0d73f84e-70ae-4eeb-96a0-1c613b5d9229.dcm
```

- `7a6b2389-53c6-4c5b-b07f-6d1ed4a3eed9` = Series UUID (folder)
- `0d73f84e-70ae-4eeb-96a0-1c613b5d9229.dcm` = Instance UUID (file)

### CRDC UUID vs DICOM UID

| Identifier Type | Format | When It Changes | Purpose |
|-----------------|--------|-----------------|---------|
| DICOM UID (e.g., SeriesInstanceUID) | Numeric (e.g., `1.3.6.1.4...`) | Never (embedded in DICOM metadata) | Clinical identification, DICOMweb queries |
| CRDC UUID (e.g., crdc_series_uuid) | UUID (e.g., `e127d258-37c2-...`) | When content changes | File paths, versioning, reproducibility |

**Key insight:** If series content changes (instances added/removed, metadata corrected), a single DICOM `SeriesInstanceUID` may map to multiple CRDC series UUIDs across different IDC versions. CRDC UUID uniquely identifies a specific version of the data.

### Mapping DICOM UID to File Paths

Use `idc-index` to get file URLs from DICOM identifiers:

```python
from idc_index import IDCClient
client = IDCClient()

# Get all file URLs for a series
series_uid = "1.3.6.1.4.1.14519.5.2.1.6450.9002.217441095430480124587725641302"
urls = client.get_series_file_URLs(seriesInstanceUID=series_uid)

for url in urls[:3]:
    print(url)
# Returns S3 URL like: s3://idc-open-data/<crdc_series_uuid>/<crdc_instance_uuid>.dcm
```

Or query URL columns directly in the index:

```python
# Get series-level URL (points to folder)
result = client.sql_query("""
    SELECT SeriesInstanceUID, series_aws_url
    FROM index
    WHERE collection_id = 'rider_pilot' AND Modality = 'CT'
    LIMIT 3
""")

print(result[['SeriesInstanceUID', 'series_aws_url']])
```

**Available URL columns in the index:**
- `series_aws_url`: S3 URL pointing to series folder (e.g., `s3://idc-open-data/uuid/*`)

GCS URLs follow the same path structure—just replace `s3://` with `gs://` (e.g., `gs://idc-open-data/uuid/*`). When using `idc-index` download methods, GCS access is handled internally.

## Accessing Cloud Storage

Through partnerships with AWS Open Data and Google Public Data programs, all IDC buckets support free egress (no download fees). No authentication required.

### AWS S3 Access

**Using AWS CLI (no account needed):**
```bash
# List bucket contents
aws s3 ls --no-sign-request s3://idc-open-data/

# List files in series folder
aws s3 ls --no-sign-request s3://idc-open-data/7a6b2389-53c6-4c5b-b07f-6d1ed4a3eed9/

# Download single file
aws s3 cp --no-sign-request \
    s3://idc-open-data/7a6b2389-53c6-4c5b-b07f-6d1ed4a3eed9/0d73f84e-70ae-4eeb-96a0-1c613b5d9229.dcm \
    ./local_file.dcm

# Download entire series folder
aws s3 cp --no-sign-request --recursive \
    s3://idc-open-data/7a6b2389-53c6-4c5b-b07f-6d1ed4a3eed9/ \
    ./series_folder/
```

**Using s5cmd (faster for batch downloads):**
```bash
# Install s5cmd
# macOS: brew install s5cmd
# Linux: Download from https://github.com/peak/s5cmd/releases

# Download specific series
s5cmd --no-sign-request cp 's3://idc-open-data/7a6b2389-53c6-4c5b-b07f-6d1ed4a3eed9/*' ./local_folder/

# Download from manifest file
s5cmd --no-sign-request run manifest.txt
```

**s5cmd manifest format:** `s5cmd run` requires one s5cmd command per line, not just URLs:
```
cp s3://idc-open-data/uuid1/instance1.dcm ./local_folder/
cp s3://idc-open-data/uuid1/instance2.dcm ./local_folder/
cp s3://idc-open-data/uuid2/instance3.dcm ./local_folder/
```

IDC Portal exports manifests in this format. When programmatically creating manifests, use `idc-index` download methods (which handle this internally) rather than building manifests manually.

### GCS Access

**Using gsutil:**
```bash
# List bucket contents
gsutil ls gs://idc-open-data/

# Download series folder
gsutil -m cp -r gs://idc-open-data/7a6b2389-53c6-4c5b-b07f-6d1ed4a3eed9/ ./local_folder/
```

**Using gcloud storage (newer CLI):**
```bash
gcloud storage cp -r gs://idc-open-data/7a6b2389-53c6-4c5b-b07f-6d1ed4a3eed9/ ./local_folder/
```

### Python Direct Access

```python
import s3fs
import gcsfs
from idc_index import IDCClient

# First, get file URLs from idc-index
client = IDCClient()
result = client.sql_query("""
    SELECT series_aws_url
    FROM index
    WHERE collection_id = 'rider_pilot' AND Modality = 'CT'
    LIMIT 1
""")
# series_aws_url is like: s3://idc-open-data/<uuid>/*
series_url = result['series_aws_url'].iloc[0]
series_path = series_url.replace('s3://', '').rstrip('/*')  # e.g., "idc-open-data/<uuid>"

# AWS S3 access
s3 = s3fs.S3FileSystem(anon=True)
files = s3.ls(series_path)
with s3.open(files[0], 'rb') as f:
    data = f.read()

# GCS access (uses same path structure as AWS)
gcs = gcsfs.GCSFileSystem(token='anon')
files = gcs.ls(series_path)
with gcs.open(files[0], 'rb') as f:
    data = f.read()
```

## Versioning and Reproducibility

IDC releases new data versions every 2-4 months. The versioning system ensures reproducibility by preserving all historical data.

### How Versioning Works

1. **Snapshots:** Each IDC version (v1, v2, ..., v23, etc.) represents a complete snapshot of all data at the time of release.
2. **UUID-based:** When data changes, new CRDC UUIDs are assigned; old UUIDs remain accessible.
3. **Cumulative buckets:** All versions coexist in the same buckets—old series folders remain.

**Version change scenarios:**
| Change Type | DICOM UID | CRDC UUID | Impact |
|-------------|-----------|-----------|--------|
| New series added | New | New | New folder appears in bucket |
| Instances added to series | Same | New series UUID | New folder, instances may repeat |
| Metadata correction | Same or new | New | New folder with updated files |
| Series removed | N/A | N/A | Old folder preserved but not in current index |

**Data removal warning:** In rare cases (e.g., data owner request, PHI breach), data may be completely removed from IDC, including all historical versions.

**BigQuery versioned datasets (metadata only, not file storage):**

For querying version-specific metadata, BigQuery provides versioned tables. See `bigquery_guide.md` for details.
- `bigquery-public-data.idc_current` — Alias for latest version
- `bigquery-public-data.idc_v23` — Specific version (replace 23 with desired version)

### Reproducing Previous Analyses

The simplest way to ensure reproducibility is to save the `crdc_series_uuid` values of the data you used in your analysis:

```python
from idc_index import IDCClient
import json

client = IDCClient()

# Select data for your analysis
selection = client.sql_query("""
    SELECT crdc_series_uuid
    FROM index
    WHERE collection_id = 'tcga_luad'
      AND Modality = 'CT'
    LIMIT 10
""")
series_uuids = list(selection['crdc_series_uuid'])

# Download data
client.download_from_selection(seriesInstanceUID=series_uuids, downloadDir="./data")

# Save manifest for reproducibility
manifest = {
    "crdc_series_uuids": series_uuids,
    "download_date": "2024-01-15",
    "idc_version": client.get_idc_version(),
    "description": "CT scans for lung cancer analysis"
}
with open("analysis_manifest.json", "w") as f:
    json.dump(manifest, f, indent=2)

# Later, reproduce exactly the same dataset:
with open("analysis_manifest.json") as f:
    manifest = json.load(f)
client.download_from_selection(
    seriesInstanceUID=manifest["crdc_series_uuids"],
    downloadDir="./reproduced_data"
)
```

Since `crdc_series_uuid` identifies an immutable version of each series, saving these UUIDs guarantees you can retrieve the exact same files later.

## Relationship Between Buckets, Versions, and Other Access Methods

### Data Coverage Comparison

| Access Method | Buckets Included | Coverage | Versions |
|---------------|------------------|----------|----------|
| Direct bucket access | All 3 buckets | 100% | All historical versions |
| `idc-index` download | All 3 buckets | 100% | Current version + prior_versions_index |
| IDC Portal | All 3 buckets | 100% | Current version only |
| DICOMweb public proxy | All 3 buckets | 100% | Current version only |
| Google Healthcare DICOM | Only `idc-open-data` | ~96% | Current version only |

**Important:** Google Healthcare API DICOM store only syncs data from `idc-open-data`. Data in `idc-open-data-two` and `idc-open-data-cr` (~4% of total) is not accessible via Google Healthcare DICOMweb endpoints.

## Best Practices

- **Use `idc-index` for discovery:** Query metadata first, then access buckets with known UUIDs.
- **Default to AWS buckets:** Request GCS only if needed.
- **Save manifests:** Store `series_aws_url` or `crdc_series_uuid` values for reproducibility.
- **Check license agreements:** Query `license_short_name` before commercial use; CC-NC data requires non-commercial use.
- **Use current version unless for reproducibility:** `index` table contains current data; use `prior_versions_index` only when exact reproducibility is needed.

## Troubleshooting

### Problem: "Access Denied" when accessing buckets
- **Cause:** Using signed requests or wrong bucket name.
- **Solution:** Use `--no-sign-request` flag in AWS CLI, or `anon=True` in Python libraries.

### Problem: File not found at expected path
- **Cause:** Using DICOM UID instead of CRDC UUID, or data changed in newer version.
- **Solution:** Query `idc-index` for current `series_aws_url`, or find historical paths in `prior_versions_index`.

### Problem: Downloaded files don't match expected series
- **Cause:** Series was revised in newer IDC version.
- **Solution:** Use `prior_versions_index` to find the exact version you need; compare `crdc_series_uuid` values.

### Problem: Google Healthcare DICOMweb missing data
- **Cause:** Google Healthcare only mirrors `idc-open-data` bucket (~96% of data).
- **Solution:** Use IDC public proxy for 100% coverage, or access buckets directly.

## Resources

**IDC Documentation:**
- [Files and Metadata](https://learn.canceridc.dev/data/organization-of-data/files-and-metadata) - Bucket organization details
- [Data Versioning](https://learn.canceridc.dev/data/data-versioning) - Version scheme explanation
- [Parsing GUIDs and UUIDs](https://learn.canceridc.dev/data/organization-of-data/guids-and-uuids) - CRDC UUID documentation
- [Loading Directly from Cloud](https://learn.canceridc.dev/data/downloading-data/direct-loading) - Python examples for cloud access

**AWS Resources:**
- [NCI IDC on AWS Open Data Registry](https://registry.opendata.aws/nci-imaging-data-commons/) - Bucket ARN and access info
- [s5cmd](https://github.com/peak/s5cmd) - High-performance S3 client (used internally by idc-index)
- [AWS CLI S3 Commands](https://docs.aws.amazon.com/cli/latest/reference/s3/) - Standard AWS CLI
- [Boto3 S3 Documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html) - AWS SDK for Python

**Google Cloud Resources:**
- [gsutil Tool](https://cloud.google.com/storage/docs/gsutil) - Google Cloud Storage CLI
- [gcloud storage Commands](https://cloud.google.com/sdk/gcloud/reference/storage) - Modern GCS CLI (recommended over gsutil)
- [Google Cloud Storage Python Client](https://cloud.google.com/python/docs/reference/storage/latest) - GCS SDK for Python

**Related Guides:**
- `dicomweb_guide.md` - DICOMweb API access (alternative to direct bucket access)
- `bigquery_guide.md` - Advanced metadata queries including versioned datasets
