# Design & Audit Report

## Issues Identified

- **Span mismatch**: entities in the original `demonstration_dataset_10k.json` used precomputed `text` fields that did not always match the substring defined by their `span` offsets, leading to validation failures.
- **Lack of validation tooling**: no programmatic checks existed to verify entity spans, deduplicate records, or compute coverage statistics.
- **Relation typing errors**: relations sometimes pointed to entity IDs of incompatible types (e.g., `WORKS_FOR` with non-person heads), allowing logically invalid triples to pass through.

## Fixes Implemented

- **Deterministic sampling & transformation**: `cli.py` samples records from the demonstration dataset and rewrites them into the required schema. Entity texts are regenerated from the main text to guarantee offset alignment【F:cli.py†L11-L59】.
- **Relation constraint enforcement**: A single source of truth mapping relation types to allowed head/tail entity types was introduced. The validator now rejects records where relations violate these constraints【F:validator/__init__.py†L11-L93】【F:validator/__init__.py†L100-L159】.
- **Preflight normalisation & blocking**: Records are normalised for common mismatches (business-as-place, activity time heads, ownables) and validated before inclusion, preventing bad samples from being written【F:cli.py†L62-L88】【F:cli.py†L117-L126】.
- **Artifact generation**: `cli.py` produces per-type counts, axis balance tables, a hash-based deduplication index, an empty violations log, and a validation report summarising any error categories【F:cli.py†L133-L190】.
- **Axis balancing**: Conversation style flags (`turns`, `updates`, `quality`, `perspective`) cycle evenly across records via an infinite mode generator【F:cli.py†L91-L101】【F:cli.py†L117-L126】.

- **Template enforcement**: Validator detects and rejects records for the `role at org`, `skill via method`, and `attendance + industry + connection` templates unless all required entities and relations are present, preventing under‑extracted or miswired samples【F:validator/__init__.py†L168-L241】.

- **Pronoun policy**: The pipeline currently omits explicit `PRONOUN` entities for anaphora; this policy is documented and applied consistently across records.

## Balance & Quality Assurance

- Span integrity and relation typing are validated for every record before inclusion, ensuring only logically consistent examples are written.
- Deduplication uses SHA-256 hashes of text, entities, and relations to prevent duplicate training items.
- Counts, axis summaries, and an explicit violations CSV are exported to enable manual inspection of coverage and error rates.

The pipeline now guarantees that each relation connects compatible entity types and that any constraint violations are surfaced by the validator, laying the groundwork for further balancing work.
