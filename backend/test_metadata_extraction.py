from app.services.metadata_extraction_service import (
    extract_metadata,
)

sample = """
Document ID: CORP-HB-2026-v3.2
Department: Human Resources
Effective Date: 2026-04-01
Owner: Global HR Operations
Classification: Internal
This document describes the enterprise Leave Policy.
"""

metadata = extract_metadata(sample)

print("=" * 80)
print(metadata)
print("=" * 80)