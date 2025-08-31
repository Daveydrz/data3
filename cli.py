import argparse
import json
import random
import hashlib
import csv
import itertools
from collections import Counter
from validator import validate_record, compute_counts, compute_axis_distribution


def transform_record(rec, seed, mode):
    """Rewrite a raw record into the target schema and attach mode info."""
    text = rec["text"]
    entities = []
    for ent in rec.get("entities", []):
        start, end = ent["span"]
        span_text = text[start:end]
        entities.append(
            {
                "id": ent["id"],
                "type": ent["type"],
                "text": span_text,
                "start": start,
                "end": end,
                "coref_key": f"E{ent['id']}",
            }
        )
    relations = []
    for i, rel in enumerate(rec.get("relations", [])):
        relations.append({"id": i, "type": rel["type"], "head": rel["head"], "tail": rel["tail"]})

    # Assemble turns based on conversation style. We keep original text so
    # entity offsets remain valid; for multi-turn we append a simple AI
    # acknowledgement after the source text.
    if mode["turns"] == "multi":
        turns = [
            {"speaker": "human", "text": text, "ts": None},
            {"speaker": "ai", "text": "Acknowledged.", "ts": None},
        ]
        text = text + "\nAI: Acknowledged."
    else:
        turns = [{"speaker": "human", "text": text, "ts": None}]

    record = {
        "id": rec["id"],
        "mode": mode,
        "text": text,
        "turns": turns,
        "entities": entities,
        "relations": relations,
        "meta": {
            "seed": seed,
            "entity_types_covered": sorted({e["type"] for e in entities}),
            "relation_types_covered": sorted({r["type"] for r in relations}),
            "final_state_only": True,
        },
    }

    return normalize_record(record)


def normalize_record(record):
    """Apply light normalisation to entities based on relation context."""
    text = record["text"]
    entity_map = {e["id"]: e for e in record.get("entities", [])}

    # Realign spans if text doesn't match
    for ent in record.get("entities", []):
        if text[ent["start"] : ent["end"]] != ent["text"]:
            idx = text.find(ent["text"])
            if idx != -1:
                ent["start"] = idx
                ent["end"] = idx + len(ent["text"])

    for rel in record.get("relations", []):
        head = entity_map.get(rel["head"])
        tail = entity_map.get(rel["tail"])
        if not head or not tail:
            continue

        if rel["type"] == "AT_LOCATION" and tail["type"] == "BUSINESS":
            tail["type"] = "PLACE"
        if rel["type"] in {"OCCURS_AT", "ON_DATE", "FOR_DURATION"} and head["type"] == "ACTIVITY":
            head["type"] = "EVENT"
        if rel["type"] == "OWNS" and tail["type"] not in {"PRODUCT", "ITEM", "OBJECT", "ASSET", "PET", "VEHICLE"}:
            tail["type"] = "OBJECT"

    return record


def mode_generator():
    """Infinite generator cycling evenly through conversation mode axes."""
    axes = {
        "turns": ["single", "multi"],
        "updates": [False, True],
        "quality": ["clean", "asr"],
        "perspective": ["first", "third"],
    }
    cycles = {axis: itertools.cycle(opts) for axis, opts in axes.items()}
    while True:
        yield {axis: next(cycle) for axis, cycle in cycles.items()}


def main():
    parser = argparse.ArgumentParser(description='Sample and validate records')
    parser.add_argument('--out', default='sample_records.jsonl')
    parser.add_argument('--records', type=int, default=1000)
    parser.add_argument('--seed', type=int, default=42)
    args = parser.parse_args()

    with open('demonstration_dataset_10k.json') as f:
        data = json.load(f)['dataset']

    rnd = random.Random(args.seed)
    rnd.shuffle(data)

    records = []
    mode_iter = mode_generator()
    for rec in data:
        mode = next(mode_iter)
        transformed = transform_record(rec, args.seed, mode)
        vres = validate_record(transformed)
        if vres["is_valid"]:
            records.append(transformed)
        if len(records) >= args.records:
            break

    with open(args.out, "w") as f:
        for r in records:
            json.dump(r, f)
            f.write("\n")

    # Validate and deduplicate
    dedup_index = []
    seen = set()
    error_totals = Counter()
    violations = []
    for r in records:
        res = validate_record(r)
        error_totals.update(res["errors"])
        if res["errors"]:
            for err in res["errors"]:
                violations.append({"id": r["id"], "error": err})

        record_hash = hashlib.sha256(
            (r["text"] + json.dumps(r["entities"]) + json.dumps(r["relations"]))
            .encode("utf-8")
        ).hexdigest()
        dedup_index.append({"id": r["id"], "hash": record_hash})
        if record_hash in seen:
            raise ValueError("Duplicate record detected")
        seen.add(record_hash)

    with open("hash_dedup_index.csv", "w") as f:
        writer = csv.DictWriter(f, ["id", "hash"])
        writer.writeheader()
        writer.writerows(dedup_index)

    entity_counts, relation_counts = compute_counts(records)
    with open("counts_entities.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerow(["type", "count"])
        for t, c in entity_counts.items():
            writer.writerow([t, c])
    with open("counts_relations.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerow(["type", "count"])
        for t, c in relation_counts.items():
            writer.writerow([t, c])

    axes = compute_axis_distribution(records)
    with open("axis_balance.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerow(["axis", "bucket", "count", "percentage"])
        for axis, counter in axes.items():
            total = sum(counter.values()) or 1
            for bucket, count in counter.items():
                writer.writerow([axis, bucket, count, count / total])

    with open("violations.csv", "w") as f:
        writer = csv.DictWriter(f, ["id", "error"])
        writer.writeheader()
        writer.writerows(violations)

    with open("validation_report.md", "w") as f:
        f.write("# Validation Report\n\n")
        f.write(f"Total records: {len(records)}\n")
        for err, count in error_totals.items():
            f.write(f"{err}: {count}\n")



if __name__ == '__main__':
    main()
