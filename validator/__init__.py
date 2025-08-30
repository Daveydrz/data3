from collections import Counter


def validate_record(record):
    """Check span integrity for all entities."""
    text = record.get('text', '')
    span_ok = True
    for ent in record.get('entities', []):
        start, end = ent.get('start'), ent.get('end')
        span_text = text[start:end]
        if span_text != ent.get('text'):
            span_ok = False
            break
    return {'span_integrity': span_ok}


def compute_counts(records):
    entity_counter = Counter()
    relation_counter = Counter()
    for rec in records:
        entity_counter.update(ent['type'] for ent in rec.get('entities', []))
        relation_counter.update(rel['type'] for rel in rec.get('relations', []))
    return entity_counter, relation_counter


def compute_axis_distribution(records):
    axes = {
        'turns': Counter(),
        'updates': Counter(),
        'quality': Counter(),
        'perspective': Counter(),
    }
    for rec in records:
        mode = rec.get('mode', {})
        axes['turns'][mode.get('turns', 'single')] += 1
        axes['updates'][str(mode.get('updates', False))] += 1
        axes['quality'][mode.get('quality', 'clean')] += 1
        axes['perspective'][mode.get('perspective', 'first')] += 1
    return axes
