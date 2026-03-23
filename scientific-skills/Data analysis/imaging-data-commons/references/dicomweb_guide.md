# IDC DICOMweb Guide

IDC provides DICOMweb access through the Google Cloud Healthcare API DICOM store. This guide covers specific implementation details and usage patterns.

## When to Use DICOMweb

Use DICOMweb when:
- Integrating with PACS systems or DICOMweb-compatible tools
- Streaming metadata without downloading complete files
- Building custom viewers or web applications
- Using existing DICOMweb client libraries (OHIF, dicomweb-client, etc.)

For most use cases, `idc-index` is simpler and recommended. Only use DICOMweb when you specifically need the DICOMweb protocol.

## Endpoints

### Public Proxy (No Authentication Required)

```
https://proxy.imaging.datacommons.cancer.gov/current/viewer-only-no-downloads-see-tinyurl-dot-com-slash-3j3d9jyp/dicomWeb
```

- **100% data coverage** - Contains all IDC data from all buckets
- Automatically points to latest IDC version
- **Updates immediately** when IDC releases new versions
- Per-IP daily quota (suitable for testing and moderate use)
- No authentication required
- Read-only access
- Note: "viewer-only-no-downloads" in URL is legacy naming with no functional significance

### Google Healthcare API (Requires Authentication)

```
https://healthcare.googleapis.com/v1/projects/nci-idc-data/locations/us-central1/datasets/idc/dicomStores/idc-store-v{VERSION}/dicomWeb
```

Replace `{VERSION}` with IDC version number. To find the current version:

```python
from idc_index import IDCClient
client = IDCClient()
print(client.get_idc_version())  # e.g., v23 returns "23"
```

- **~96% data coverage** - Only syncs data from `idc-open-data` bucket (~4% data from other buckets missing)
- Updates **within 1-2 weeks** after IDC releases new version
- Requires authentication with higher quotas
- Better performance (no proxy routing)
- Each version gets a new versioned repository

See [Content Coverage Differences](#content-coverage-differences) and [Authentication](#authentication) sections below.

## Content Coverage Differences

**Important:** The two DICOMweb endpoints have different data coverage. The IDC public proxy contains **more** data than the authenticated Google Healthcare endpoint.

### Coverage Summary

| Endpoint | Coverage | Missing Data |
|----------|----------|--------------|
| **IDC Public Proxy** | 100% | None |
| **Google Healthcare API** | ~96% | ~4% (two buckets not synced) |

### What Does Google Healthcare Miss?

Google Healthcare DICOM store **only syncs data from the `idc-open-data` S3 bucket**. It does not include data from the other two buckets:

- `idc-open-data-cr`
- `idc-open-data-two`

These missing buckets typically contain thousands of series each, accounting for ~4% of total IDC data. Exact numbers vary by IDC version.

See `cloud_storage_guide.md` for details on bucket organization, file structure, and direct access methods.

### Update Timing

- **IDC Public Proxy**: Updates immediately when IDC releases new versions.
- **Google Healthcare**: Updates within 1-2 weeks after each IDC version release.

Between releases, both endpoints remain current. The 1-2 week delay only occurs during the transition period after a new IDC version is released.

**Warning from IDC documentation:** *"The Google-hosted DICOM store may not contain the latest version of IDC data!"* — Please verify within a few weeks after a new version release.

### Choosing the Right Endpoint

**Use IDC public proxy when:**
- You need complete data coverage (100%)
- You need absolutely latest data immediately after version release
- You don't want to set up GCP authentication
- Your usage fits within per-IP quota (can request increases via support@canceridc.dev)
- You're accessing slide microscopy images frame-by-frame

**Use Google Healthcare API when:**
- The ~4% missing data doesn't affect your use case
- You need higher quotas for heavy usage
- You want better performance (direct access, no proxy routing)

### Checking Your Data Availability

Before choosing an endpoint, verify whether your data might be in the missing buckets:

```python
from idc_index import IDCClient

client = IDCClient()

# Check which buckets contain your collection data
results = client.sql_query("""
    SELECT series_aws_url, COUNT(*) as series_count
    FROM index
    WHERE collection_id = 'your_collection_id'
    GROUP BY series_aws_url
""")

print(results)

# Look for URLs containing 'idc-open-data-cr' or 'idc-open-data-two'
# If present, this data won't be available in Google Healthcare endpoint
```

## Implementation Details

IDC DICOMweb is provided through Google Cloud Healthcare API DICOM store. Its implementation follows DICOM PS3.18 Web Services, with specific features documented in [Google Healthcare DICOM Conformance Statement](https://docs.cloud.google.com/healthcare-api/docs/dicom).

### Supported Operations

| Service | Description | Supported |
|---------|-------------|-----------|
| QIDO-RS | Search DICOM objects | Yes |
| WADO-RS | Retrieve DICOM objects and metadata | Yes |
| STOW-RS | Store DICOM objects | No (IDC is read-only) |

**Not supported:** URI services, worklist services, non-patient instance services, capability transactions.

### Searchable DICOM Tags (QIDO-RS)

The implementation supports a limited set of searchable tags:

| Level | Searchable Tags |
|-------|-----------------|
| Study | StudyInstanceUID, PatientName, PatientID, AccessionNumber, ReferringPhysicianName, StudyDate |
| Series | All Study tags + SeriesInstanceUID, Modality |
| Instance | All Series tags + SOPInstanceUID |

**Important:** Only exact matching is supported, except:
- StudyDate: Supports range queries
- PatientName: Supports fuzzy matching

### Query Limits

- Maximum results: 5,000 for study/series search; 50,000 for instance search
- Maximum offset: 1,000,000
- DICOM sequence tags larger than ~1 MB will not be returned in metadata (BulkDataURI provided instead)

## Code Examples

All examples use the public proxy endpoint. For authenticated Google Healthcare access, see the [Authentication section](#authentication).

### Using idc-index to Find UIDs

Use `idc-index` to discover data, then use DICOMweb to access metadata:

```python
from idc_index import IDCClient

client = IDCClient()

# Find studies of interest
results = client.sql_query("""
    SELECT StudyInstanceUID, SeriesInstanceUID, PatientID, Modality
    FROM index
    WHERE collection_id = 'tcga_luad' AND Modality = 'CT'
    LIMIT 5
""")

# Use these UIDs for DICOMweb
study_uid = results.iloc[0]['StudyInstanceUID']
series_uid = results.iloc[0]['SeriesInstanceUID']
print(f"Study: {study_uid}")
print(f"Series: {series_uid}")
```

### QIDO-RS: Search by UID

```python
import requests

base_url = "https://proxy.imaging.datacommons.cancer.gov/current/viewer-only-no-downloads-see-tinyurl-dot-com-slash-3j3d9jyp/dicomWeb"

# Search for specific study
study_uid = "1.3.6.1.4.1.14519.5.2.1.6450.9002.307623500513044641407722230440"
response = requests.get(
    f"{base_url}/studies",
    params={"StudyInstanceUID": study_uid},
    headers={"Accept": "application/dicom+json"}
)

if response.status_code == 200:
    studies = response.json()
    print(f"Found {len(studies)} study")
```

### QIDO-RS: List Series in Study

```python
import requests

base_url = "https://proxy.imaging.datacommons.cancer.gov/current/viewer-only-no-downloads-see-tinyurl-dot-com-slash-3j3d9jyp/dicomWeb"
study_uid = "1.3.6.1.4.1.14519.5.2.1.6450.9002.307623500513044641407722230440"

response = requests.get(
    f"{base_url}/studies/{study_uid}/series",
    headers={"Accept": "application/dicom+json"}
)

if response.status_code == 200:
    series_list = response.json()
    for series in series_list:
        # DICOM tags returned as hex codes
        series_uid = series.get("0020000E", {}).get("Value", [None])[0]
        modality = series.get("00080060", {}).get("Value", [None])[0]
        description = series.get("0008103E", {}).get("Value", [""])[0]
        print(f"{modality}: {description}")
```

### QIDO-RS: List Instances in Series

```python
import requests

base_url = "https://proxy.imaging.datacommons.cancer.gov/current/viewer-only-no-downloads-see-tinyurl-dot-com-slash-3j3d9jyp/dicomWeb"
study_uid = "1.3.6.1.4.1.14519.5.2.1.6450.9002.307623500513044641407722230440"
series_uid = "1.3.6.1.4.1.14519.5.2.1.6450.9002.217441095430480124587725641302"

response = requests.get(
    f"{base_url}/studies/{study_uid}/series/{series_uid}/instances",
    params={"limit": 10},
    headers={"Accept": "application/dicom+json"}
)

if response.status_code == 200:
    instances = response.json()
    print(f"Found {len(instances)} instances")
    for inst in instances[:3]:
        sop_uid = inst.get("00080018", {}).get("Value", [None])[0]
        print(f"  SOPInstanceUID: {sop_uid}")
```

### WADO-RS: Retrieve Series Metadata

```python
import requests

base_url = "https://proxy.imaging.datacommons.cancer.gov/current/viewer-only-no-downloads-see-tinyurl-dot-com-slash-3j3d9jyp/dicomWeb"
study_uid = "1.3.6.1.4.1.14519.5.2.1.6450.9002.307623500513044641407722230440"
series_uid = "1.3.6.1.4.1.14519.5.2.1.6450.9002.217441095430480124587725641302"

response = requests.get(
    f"{base_url}/studies/{study_uid}/series/{series_uid}/metadata",
    headers={"Accept": "application/dicom+json"}
)

if response.status_code == 200:
    instances = response.json()
    print(f"Retrieved metadata for {len(instances)} instances")

    # Extract image dimensions from first instance
    if instances:
        inst = instances[0]
        rows = inst.get("00280010", {}).get("Value", [None])[0]
        cols = inst.get("00280011", {}).get("Value", [None])[0]
        print(f"Image dimensions: {rows} x {cols}")
```

### Combined Workflow: idc-index Discovery + DICOMweb Metadata

```python
from idc_index import IDCClient
import requests

# Use idc-index for efficient discovery
idc = IDCClient()
results = idc.sql_query("""
    SELECT StudyInstanceUID, SeriesInstanceUID, Modality, SeriesDescription
    FROM index
    WHERE collection_id = 'nlst' AND Modality = 'CT'
    LIMIT 1
""")

study_uid = results.iloc[0]['StudyInstanceUID']
series_uid = results.iloc[0]['SeriesInstanceUID']
print(f"Found: {results.iloc[0]['SeriesDescription']}")

# Use DICOMweb to stream metadata without downloading files
base_url = "https://proxy.imaging.datacommons.cancer.gov/current/viewer-only-no-downloads-see-tinyurl-dot-com-slash-3j3d9jyp/dicomWeb"

response = requests.get(
    f"{base_url}/studies/{study_uid}/series/{series_uid}/metadata",
    headers={"Accept": "application/dicom+json"}
)

if response.status_code == 200:
    metadata = response.json()
    print(f"Retrieved metadata for {len(metadata)} instances without downloading files")
```

## Common DICOM Tag Reference

DICOMweb returns tags as hex codes. Common tags include:

| Tag | Name | Description |
|-----|------|-------------|
| 00080018 | SOPInstanceUID | Unique instance identifier |
| 00080020 | StudyDate | Date study was performed |
| 00080060 | Modality | Imaging modality (CT, MR, PT, etc.) |
| 0008103E | SeriesDescription | Series description |
| 00100020 | PatientID | Patient identifier |
| 0020000D | StudyInstanceUID | Unique study identifier |
| 0020000E | SeriesInstanceUID | Unique series identifier |
| 00280010 | Rows | Image pixel height |
| 00280011 | Columns | Image pixel width |

## Google Healthcare API Authentication

To use Google Healthcare endpoint with higher quotas:

```python
from google.auth import default
from google.auth.transport.requests import Request
import requests

# Get credentials (requires gcloud authentication)
credentials, project = default()
credentials.refresh(Request())

# Build authenticated request
base_url = "https://healthcare.googleapis.com/v1/projects/nci-idc-data/locations/us-central1/datasets/idc/dicomStores/idc-store-v23/dicomWeb"

response = requests.get(
    f"{base_url}/studies",
    params={"limit": 5},
    headers={
        "Authorization": f"Bearer {credentials.token}",
        "Accept": "application/dicom+json"
    }
)
```

**Prerequisites:**
1. Google Cloud SDK installed (`gcloud`)
2. Authenticated: `gcloud auth application-default login`
3. Account has access to public Google Cloud datasets

## Troubleshooting

### Problem: Search query returns 400 Bad Request
- **Cause:** Unsupported search parameters used. The implementation only supports specific DICOM tags for filtering.
- **Solution:** Use UID-based queries (StudyInstanceUID, SeriesInstanceUID). To filter by Modality or other attributes, first use `idc-index` to discover UIDs, then query DICOMweb with specific UIDs.

### Problem: Google Healthcare endpoint returns 403 Forbidden
- **Cause:** Missing authentication or insufficient permissions.
- **Solution:** Run `gcloud auth application-default login` and ensure your account has access.

### Problem: 429 Too Many Requests
- **Cause:** Rate limit exceeded.
- **Solution:** Add delays between requests, reduce `limit` value, or use authenticated endpoint for higher quotas.

### Problem: Valid UID returns 204 No Content
- **Cause:** UID may be from older IDC version (doesn't exist in current data), or data is in buckets not synced by Google Healthcare.
- **Solution:**
  - First verify UID exists via `idc-index` query.
  - Check if data is in `idc-open-data-cr` or `idc-open-data-two` buckets (not available via Google Healthcare).
  - Switch to IDC public proxy for 100% coverage.
  - During new version releases, Google Healthcare may lag 1-2 weeks.

### Problem: Large metadata response parsing is slow
- **Cause:** Series with many instances return enormous JSON.
- **Solution:** Use `limit` parameter in instance query, or query specific instances via SOPInstanceUID.

### Problem: Expected attributes missing from response
- **Cause:** DICOM sequences larger than ~1 MB are excluded from metadata response.
- **Solution:** If you need all attributes, use WADO-RS instance retrieval to get complete DICOM instances.

## Resources

**IDC Documentation:**
- [IDC DICOM Stores](https://learn.canceridc.dev/data/organization-of-data/dicom-stores) - Data coverage and bucket details
- [IDC DICOMweb Access](https://learn.canceridc.dev/data/downloading-data/dicomweb-access) - Endpoint usage and differences
- [IDC Proxy Policy](https://learn.canceridc.dev/portal/proxy-policy) - Quota policy and usage limits
- [IDC User Guide](https://learn.canceridc.dev/) - Complete documentation

**DICOMweb Standards and Tools:**
- [Google Healthcare DICOM Conformance Statement](https://docs.cloud.google.com/healthcare-api/docs/dicom)
- [DICOMweb Standard](https://www.dicomstandard.org/using/dicomweb)
- [dicomweb-client Python Library](https://dicomweb-client.readthedocs.io/)

**Related Guides:**
- `cloud_storage_guide.md` - Direct bucket access, file organization, CRDC UUID, and versioning
- `bigquery_guide.md` - Advanced metadata queries with complete DICOM attributes
