"""Validation utilities for generated conversation records.

The validator enforces span integrity and relation argument typing
according to a constraint contract. Records failing any check are
considered invalid and should be dropped before writing to disk.
"""

from collections import Counter
import re


# ---------------------------------------------------------------------------
# Relation constraint contract
# ---------------------------------------------------------------------------

# Each entry maps a relation type to a tuple of allowed head types and tail
# types.  Types are expressed as strings matching the entity ``type`` field.
RELATION_CONSTRAINTS = {
    "ATTENDED": ({"PERSON", "PRONOUN"}, {"EVENT"}),
    "EVENT_IN_INDUSTRY": ({"EVENT"}, {"INDUSTRY", "DOMAIN", "SECTOR"}),
    "CONNECTED_WITH": ({"PERSON", "PRONOUN"}, {"PERSON", "PRONOUN"}),
    "AT_LOCATION": (
        {"PERSON", "PRONOUN", "EVENT", "ACTIVITY", "ORGANIZATION"},
        {"LOCATION", "PLACE", "VENUE", "ROOM", "ADDRESS", "CITY", "GPE", "COUNTRY", "BUSINESS"},
    ),
    "OCCURS_AT": (
        {"EVENT", "PLAN", "ACTIVITY"},
        {"DATE", "TIME", "TIME_OF_DAY", "TIMELINE", "DURATION", "DATE_TIME"},
    ),
    "ON_DATE": (
        {"EVENT", "PLAN", "ACTIVITY"},
        {"DATE", "TIME", "TIME_OF_DAY", "TIMELINE", "DURATION", "DATE_TIME"},
    ),
    "FOR_DURATION": (
        {"EVENT", "PLAN", "ACTIVITY"},
        {"DATE", "TIME", "TIME_OF_DAY", "TIMELINE", "DURATION", "DATE_TIME"},
    ),
    "HAS_FREQUENCY": ({"EVENT", "ACTIVITY", "HABIT"}, {"FREQUENCY"}),
    "DOES_ACTIVITY": ({"PERSON", "PRONOUN"}, {"ACTIVITY", "HOBBY"}),
    "HAS_ROLE": ({"PERSON", "PRONOUN"}, {"ROLE", "COMMUNITY_ROLE"}),
    "WORKS_FOR": ({"PERSON", "PRONOUN"}, {"ORGANIZATION", "BUSINESS", "COMPANY"}),
    "HAS_SKILL": ({"PERSON", "PRONOUN"}, {"SKILL", "TECHNOLOGY"}),
    "OWNS": (
        {"PERSON", "PRONOUN"},
        {"PRODUCT", "ITEM", "OBJECT", "ASSET", "PET", "VEHICLE"},
    ),
    "LIKES": (
        {"PERSON", "PRONOUN"},
        {
            "FOOD",
            "MUSIC",
            "MOVIE",
            "HOBBY",
            "BOOK",
            "SHOW",
            "GAME",
            "ITEM",
            "OBJECT",
            "ACTIVITY",
        },
    ),
    "PREFERS": (
        {"PERSON", "PRONOUN"},
        {
            "FOOD",
            "MUSIC",
            "MOVIE",
            "HOBBY",
            "BOOK",
            "SHOW",
            "GAME",
            "ITEM",
            "OBJECT",
            "ACTIVITY",
        },
    ),
    "DISLIKES": (
        {"PERSON", "PRONOUN"},
        {
            "FOOD",
            "MUSIC",
            "MOVIE",
            "HOBBY",
            "BOOK",
            "SHOW",
            "GAME",
            "ITEM",
            "OBJECT",
            "ACTIVITY",
        },
    ),
    "PLANS": ({"PERSON", "PRONOUN"}, {"PLAN", "GOAL", "EVENT", "ACTIVITY"}),
    # "CORRECTS" handled separately in validation logic
}


# ---------------------------------------------------------------------------
# Validation functions
# ---------------------------------------------------------------------------

def validate_record(record):
    """Validate a single record.

    Returns a dict ``{"is_valid": bool, "errors": Counter}`` where the
    counter tallies error categories such as ``RELATION_HEAD_TYPE``.
    """

    errors = Counter()
    text = record.get("text")

    # --- Text checks ----------------------------------------------------
    if not isinstance(text, str) or len(text) < 25:
        errors["TEXT_LENGTH"] += 1
        return {"is_valid": False, "errors": errors}

    # --- Entity checks --------------------------------------------------
    entity_map = {}
    for ent in record.get("entities", []):
        ent_id = ent.get("id")
        start, end = ent.get("start"), ent.get("end")
        ent_text = ent.get("text")
        ent_type = ent.get("type")

        if any(v is None for v in (ent_id, start, end, ent_text, ent_type)):
            errors["ENTITY_FORMAT"] += 1
            continue
        if not isinstance(start, int) or not isinstance(end, int) or start < 0 or end <= start or end > len(text):
            errors["SPAN_INVALID"] += 1
            continue

        span_text = text[start:end]
        if span_text != ent_text:
            errors["SPAN_MISMATCH"] += 1

        entity_map[ent_id] = ent

    # --- Relation checks -----------------------------------------------
    for rel in record.get("relations", []):
        head_id = rel.get("head")
        tail_id = rel.get("tail")
        rtype = rel.get("type")

        if head_id not in entity_map or tail_id not in entity_map:
            errors["RELATION_REF_INVALID"] += 1
            continue

        head_type = entity_map[head_id]["type"]
        tail_type = entity_map[tail_id]["type"]

        if rtype in RELATION_CONSTRAINTS:
            allowed_heads, allowed_tails = RELATION_CONSTRAINTS[rtype]
            if head_type not in allowed_heads:
                errors["RELATION_HEAD_TYPE"] += 1
            if tail_type not in allowed_tails:
                errors["RELATION_TAIL_TYPE"] += 1
        elif rtype == "CORRECTS":
            if head_type != tail_type:
                errors["RELATION_HEAD_TYPE"] += 1

    tmpl_errors, templates = _template_checks(record, entity_map)
    errors.update(tmpl_errors)

    return {"is_valid": not errors, "errors": errors, "templates": templates}


ROLE_AT_ORG_RE = re.compile(
    r"(?:in (?:their|his|her) role as|role as)\s+(?P<role>[^,]+?)\s+at\s+(?P<org>[^.,]+)",
    re.IGNORECASE,
)
SKILL_VIA_METHOD_RE = re.compile(
    r"(?:develops|masters|learns|builds|improves)\s+(?P<skill>[^,]+?)\s+(?:through|via|by)\s+(?P<method>[^.,]+)",
    re.IGNORECASE,
)
ATTENDANCE_RE = re.compile(
    r"attended a\s+(?P<event>[^,]+?)\s+in the\s+(?P<industry>[^,]+?)\s+industry and connected with\s+(?P<person>[^.,]+)",
    re.IGNORECASE,
)


def _template_checks(record, entity_map):
    errors = Counter()
    templates = {
        "role_at_org": False,
        "skill_via_method": False,
        "attendance_industry_connection": False,
    }

    text = record.get("text", "")
    entities = record.get("entities", [])
    relations = record.get("relations", [])

    m = ROLE_AT_ORG_RE.search(text)
    if m:
        templates["role_at_org"] = True
        role_txt = m.group("role").strip().lower()
        org_txt = m.group("org").strip().lower()
        role_ids = [e["id"] for e in entities if e["type"] == "ROLE" and e["text"].lower() == role_txt]
        org_ids = [e["id"] for e in entities if e["type"] == "ORGANIZATION" and e["text"].lower() == org_txt]
        has_role_heads = {r["head"] for r in relations if r["type"] == "HAS_ROLE" and r["tail"] in role_ids}
        works_for_heads = {r["head"] for r in relations if r["type"] == "WORKS_FOR" and r["tail"] in org_ids}
        if not role_ids or not org_ids or not (has_role_heads & works_for_heads):
            errors["UNDEREXTRACT_ROLE"] += 1

    m = SKILL_VIA_METHOD_RE.search(text)
    if m:
        templates["skill_via_method"] = True
        skill_txt = m.group("skill").strip().lower()
        method_txt = m.group("method").strip().lower()
        skill_ids = [e["id"] for e in entities if e["type"] == "SKILL" and e["text"].lower() == skill_txt]
        method_ids = [
            e["id"]
            for e in entities
            if e["type"] in {"METHOD", "APPROACH", "TECHNIQUE"} and e["text"].lower() == method_txt
        ]
        has_skill = any(
            r["type"] in {"HAS_SKILL", "LEARNS", "DEVELOPS"} and r["tail"] in skill_ids
            for r in relations
        )
        learned_via = any(
            r["type"] in {"LEARNED_VIA", "ACQUIRED_VIA", "BY_METHOD"}
            and r["head"] in skill_ids
            and r["tail"] in method_ids
            for r in relations
        )
        if not skill_ids or not method_ids or not has_skill or not learned_via:
            errors["MISSING_METHOD_EDGE"] += 1

    m = ATTENDANCE_RE.search(text)
    if m:
        templates["attendance_industry_connection"] = True
        event_txt = m.group("event").strip().lower()
        industry_txt = m.group("industry").strip().lower()
        person2_txt = m.group("person").strip().lower()
        event_ids = [e["id"] for e in entities if e["type"] == "EVENT" and e["text"].lower() == event_txt]
        industry_ids = [e["id"] for e in entities if e["type"] == "INDUSTRY" and e["text"].lower() == industry_txt]
        person2_ids = [
            e["id"]
            for e in entities
            if e["type"] in {"PERSON", "PRONOUN"} and e["text"].lower() == person2_txt
        ]
        attended = any(r["type"] == "ATTENDED" and r["tail"] in event_ids for r in relations)
        event_industry = any(
            r["type"] == "EVENT_IN_INDUSTRY" and r["head"] in event_ids and r["tail"] in industry_ids
            for r in relations
        )
        connected = any(
            r["type"] == "CONNECTED_WITH" and r["tail"] in person2_ids for r in relations
        )
        if not event_ids or not industry_ids or not person2_ids or not attended or not event_industry or not connected:
            errors["MISSING_ATTENDANCE_EDGE"] += 1
        for rel in relations:
            if rel["type"] == "AT_LOCATION":
                head = entity_map.get(rel["head"])
                tail = entity_map.get(rel["tail"])
                if head and tail and head["type"] in {"PERSON", "PRONOUN"} and tail["type"] in {"PERSON", "PRONOUN"}:
                    errors["AT_LOCATION_PERSON_PERSON"] += 1

    return errors, templates


def compute_counts(records):
    """Aggregate entity and relation type counts across records."""
    entity_counter = Counter()
    relation_counter = Counter()
    for rec in records:
        entity_counter.update(ent["type"] for ent in rec.get("entities", []))
        relation_counter.update(rel["type"] for rel in rec.get("relations", []))
    return entity_counter, relation_counter


def compute_axis_distribution(records):
    """Summarise how many records fall into each conversation mode bucket."""
    axes = {
        "turns": Counter(),
        "updates": Counter(),
        "quality": Counter(),
        "perspective": Counter(),
    }
    for rec in records:
        mode = rec.get("mode", {})
        axes["turns"][mode.get("turns", "single")] += 1
        axes["updates"][str(mode.get("updates", False))] += 1
        axes["quality"][mode.get("quality", "clean")] += 1
        axes["perspective"][mode.get("perspective", "first")] += 1
    return axes

