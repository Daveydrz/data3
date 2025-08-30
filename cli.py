import argparse
import json
import random
import hashlib
import csv
from validator import validate_record, compute_counts, compute_axis_distribution


def transform_record(rec, seed):
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
    return {
        'id': rec['id'],
        'mode': {'turns': 'single', 'updates': False, 'quality': 'clean', 'perspective': 'third'},
        'text': text,
        'turns': [],
        'entities': entities,
        'relations': relations,
        'meta': {
            'seed': seed,
            'entity_types_covered': sorted({e['type'] for e in entities}),
            'relation_types_covered': sorted({r['type'] for r in relations}),
            'final_state_only': True
        }
    }


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
    sample = data[:args.records]

    records = [transform_record(r, args.seed) for r in sample]

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
