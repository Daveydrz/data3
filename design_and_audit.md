# Design & Audit Report

## Issues Identified

- **Span mismatch**: entities in the original `demonstration_dataset_10k.json` used precomputed `text` fields that did not always match the substring defined by their `span` offsets, leading to validation failures.
- **Lack of validation tooling**: no programmatic checks existed to verify entity spans, deduplicate records, or compute coverage statistics.

## Fixes Implemented

- **Deterministic sampling & transformation**: Added `cli.py` which samples records from the demonstration dataset and rewrites them into the required schema. Entity texts are regenerated from the main text to guarantee offset alignment【F:cli.py†L9-L25】.
- **Validation utilities**: Introduced a lightweight `validator` module providing span integrity checks, count aggregation, and axis distribution summaries【F:validator/__init__.py†L1-L34】.
- **Artifact generation**: `cli.py` now produces per-type counts, axis balance tables, a hash-based deduplication index, and a validation report【F:cli.py†L101-L160】.
- **Axis balancing & coverage**: Conversation style flags (`turns`, `updates`, `quality`, `perspective`) are cycled to evenly cover all buckets, and sampling continues until every entity and relation type present in the source corpus is represented in the output set【F:cli.py†L64-L95】【F:cli.py†L97-L100】.

## Balance & Quality Assurance

- Span integrity is verified for every record before writing summaries; failures halt the pipeline.
- Deduplication uses SHA-256 hashes of text, entities, and relations to prevent duplicate training items.
- Counts and axis summaries are exported as CSV files to enable manual inspection of coverage.

Future improvements could expand axis variety and incorporate full relation-type validation, but the current pipeline establishes deterministic, validated sampling as a foundation for further balancing work.
