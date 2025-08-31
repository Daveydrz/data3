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
    text = rec['text']
    entities = []
    for ent in rec.get('entities', []):
        start, end = ent['span']
        span_text = text[start:end]
        entities.append({
            'id': ent['id'],
            'type': ent['type'],
            'text': span_text,
            'start': start,
            'end': end,
            'coref_key': f"E{ent['id']}"
        })
    relations = []
    for i, rel in enumerate(rec.get('relations', [])):
        relations.append({'id': i, 'type': rel['type'], 'head': rel['head'], 'tail': rel['tail']})

    # Assemble turns based on conversation style. We keep original text so
    # entity offsets remain valid; for multi-turn we append a simple AI
    # acknowledgement after the source text.
    if mode['turns'] == 'multi':
        turns = [
            {'speaker': 'human', 'text': text, 'ts': None},
            {'speaker': 'ai', 'text': 'Acknowledged.', 'ts': None},
        ]
        text = text + '\nAI: Acknowledged.'
    else:
        turns = [{'speaker': 'human', 'text': text, 'ts': None}]

    return {
        'id': rec['id'],
        'mode': mode,
        'text': text,
        'turns': turns,
        'entities': entities,
        'relations': relations,
        'meta': {
            'seed': seed,
            'entity_types_covered': sorted({e['type'] for e in entities}),
            'relation_types_covered': sorted({r['type'] for r in relations}),
            'final_state_only': True
        }
    }


def generate_balanced_modes(n):
    """Produce a list of mode dicts balanced across conversation axes."""
    axes = {
        'turns': ['single', 'multi'],
        'updates': [False, True],
        'quality': ['clean', 'asr'],
        'perspective': ['first', 'third'],
    }
    cycles = {axis: itertools.cycle(opts) for axis, opts in axes.items()}
    modes = []
    for _ in range(n):
        modes.append({axis: next(cycle) for axis, cycle in cycles.items()})
    return modes


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

    # Determine coverage targets across full dataset
    all_entity_types = {e['type'] for rec in data for e in rec.get('entities', [])}
    all_relation_types = {r['type'] for rec in data for r in rec.get('relations', [])}

    selected = []
    ent_counter = Counter()
    rel_counter = Counter()
    for rec in data:
        selected.append(rec)
        ent_counter.update(e['type'] for e in rec.get('entities', []))
        rel_counter.update(r['type'] for r in rec.get('relations', []))
        if len(selected) >= args.records and all_entity_types <= set(ent_counter) and all_relation_types <= set(rel_counter):
            break

    selected = selected[:args.records]
    modes = generate_balanced_modes(len(selected))
    records = [transform_record(r, args.seed, m) for r, m in zip(selected, modes)]

    with open(args.out, 'w') as f:
        for r in records:
            json.dump(r, f)
            f.write('\n')

    # Validate and deduplicate
    dedup_index = []
    seen = set()
    all_valid = True
    for r in records:
        res = validate_record(r)
        all_valid &= res['span_integrity']
        record_hash = hashlib.sha256((r['text'] + json.dumps(r['entities']) + json.dumps(r['relations'])).encode('utf-8')).hexdigest()
        dedup_index.append({'id': r['id'], 'hash': record_hash})
        if record_hash in seen:
            raise ValueError('Duplicate record detected')
        seen.add(record_hash)

    with open('hash_dedup_index.csv', 'w') as f:
        writer = csv.DictWriter(f, ['id', 'hash'])
        writer.writeheader()
        writer.writerows(dedup_index)

    entity_counts, relation_counts = compute_counts(records)
    with open('counts_entities.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['type', 'count'])
        for t, c in entity_counts.items():
            writer.writerow([t, c])
    with open('counts_relations.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['type', 'count'])
        for t, c in relation_counts.items():
            writer.writerow([t, c])

    axes = compute_axis_distribution(records)
    with open('axis_balance.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['axis', 'bucket', 'count', 'percentage'])
        for axis, counter in axes.items():
            total = sum(counter.values()) or 1
            for bucket, count in counter.items():
                writer.writerow([axis, bucket, count, count / total])

    with open('validation_report.md', 'w') as f:
        f.write('# Validation Report\n\n')
        f.write(f'Span integrity: {"PASS" if all_valid else "FAIL"}\n')
        f.write(f'Total records: {len(records)}\n')


if __name__ == '__main__':
    main()
