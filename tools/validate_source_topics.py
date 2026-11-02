#!/usr/bin/env python3
"""Validate source/topic traceability without treating inventory counts as completion."""
from pathlib import Path
import re
import sys
import yaml

ROOT = Path(__file__).resolve().parents[1]


def validate(data, canonical, registered, questions, planned):
    errors = []
    policy = data.get('policy', {})
    for key in ('count_floors_are_completion_criteria', 'preferred_counts_are_caps'):
        if policy.get(key) is not False:
            errors.append(f'policy.{key} must be false')
    snapshots = {}
    for s in data.get('source_snapshots', []):
        sid = s['source_id']
        if sid in snapshots:
            errors.append(f'duplicate source snapshot {sid}')
        snapshots[sid] = s
        if sid not in registered:
            errors.append(f'unregistered source {sid}')
        if not re.fullmatch(r'[0-9a-f]{40}', s.get('commit', '')):
            errors.append(f'{sid}: immutable commit required')
        if s.get('reuse') != 'topic-discovery-only':
            errors.append(f'{sid}: topic inventory must not grant question reuse rights')
        files = s.get('files', [])
        if len({f['path'] for f in files}) != len(files):
            errors.append(f'{sid}: duplicate file snapshot')
        for f in files:
            if not re.fullmatch(r'[0-9a-f]{40}', f.get('blob_sha', '')):
                errors.append(f'{sid}:{f["path"]}: file blob SHA required')
    seen = set()
    mapped = set()
    for topic in data.get('topics', []):
        tid = topic['id']
        if tid in seen:
            errors.append(f'duplicate topic {tid}')
        seen.add(tid)
        comps = set(topic.get('competencies', [])); mapped |= comps
        if not comps or comps - canonical:
            errors.append(f'{tid}: missing or unknown canonical competency')
        if topic.get('scope') not in {'general', 'specialist'}:
            errors.append(f'{tid}: invalid scope')
        if topic.get('status') not in {'gap', 'partial', 'covered', 'deferred'}:
            errors.append(f'{tid}: invalid status')
        origin = topic.get('origin')
        if origin not in {'source-discovery', 'existing-role-profile'}:
            errors.append(f'{tid}: invalid origin')
        refs = topic.get('sources', [])
        if origin == 'source-discovery' and not refs:
            errors.append(f'{tid}: source-discovery topic needs evidence')
        if origin == 'existing-role-profile' and topic.get('profile_path') != 'evidence/role-profiles/swe.yaml':
            errors.append(f'{tid}: baseline origin needs the SWE role profile')
        for ref in refs:
            snapshot = snapshots.get(ref['source_id'])
            if not snapshot or ref.get('path') not in {f['path'] for f in snapshot['files']}:
                errors.append(f'{tid}: source path was not inspected')
            if not ref.get('locator'):
                errors.append(f'{tid}: source locator required')
        evidence = topic.get('question_evidence', [])
        assessed = set()
        for ev in evidence:
            q = questions.get(ev.get('question_id'))
            if not q or 'swe' not in q['classification']['roles'] or q['status'] == 'deprecated':
                errors.append(f'{tid}: unknown, deprecated or non-SWE question'); continue
            qc = q['classification']['competencies']
            overlap = comps & {qc['primary'], *qc['secondary']}
            if not overlap:
                errors.append(f'{tid}: question has no shared canonical competency')
            a = q['assessment']; field = ev.get('field'); valid = False
            if field == 'rubric':
                valid = ev.get('criterion_id') in {r['id'] for r in a.get('rubric', [])}
            elif field in {'must_surface', 'strong_signals'}:
                index = ev.get('index')
                valid = type(index) is int and 0 <= index < len(a.get(field, []))
            if not valid:
                errors.append(f'{tid}: assessment anchor does not resolve')
            if topic.get('status') == 'covered':
                if q['status'] != 'reviewed' or any(q['review'][k] != 'approved' for k in ('technical', 'taxonomy', 'provenance')):
                    errors.append(f'{tid}: covered evidence must be reviewed and fully approved')
                if not ev.get('topic_rationale'):
                    errors.append(f'{tid}: covered evidence needs a topic-specific assessment rationale')
                assessed |= overlap if valid else set()
        if topic.get('status') == 'covered' and (not evidence or comps - assessed):
            errors.append(f'{tid}: covered status requires evidence for every mapped competency')
        if topic.get('status') == 'partial' and not evidence:
            errors.append(f'{tid}: partial status requires anchored question evidence')
        if topic.get('status') == 'deferred' and not topic.get('deferral_reason'):
            errors.append(f'{tid}: deferral needs a reason')
        if not topic.get('assessment_focus') or not topic.get('next_action'):
            errors.append(f'{tid}: assessment focus and next action required')
    if planned - mapped:
        errors.append(f'planned competencies absent from topic inventory: {sorted(planned-mapped)}')
    return errors


def main():
    load = lambda p: yaml.safe_load(p.read_text())
    data = load(ROOT / 'coverage/topics/swe.yaml')
    canonical = {c['id'] for c in load(ROOT / 'taxonomy/competencies.yaml')['competencies']}
    registered = {s['id'] for s in load(ROOT / 'sources/source-register.yaml')['sources']}
    questions = {q['id']: q for p in (ROOT/'questions').rglob('*.yaml') if (q := load(p))}
    plan = load(ROOT / 'coverage/swe.yaml')
    planned = {c for b in plan['coverage_targets'].values() for c in b['competencies']}
    errors = validate(data, canonical, registered, questions, planned)
    if plan['policy'].get('topic_inventory') != 'coverage/topics/swe.yaml':
        errors.append('SWE coverage plan must reference the source-topic inventory')
    completion = plan['policy'].get('generation_completion', {})
    for key in ('count_floors_are_completion_criteria', 'preferred_counts_are_caps'):
        if completion.get(key) is not False:
            errors.append(f'SWE generation_completion.{key} must be false')
    if errors:
        print('\n'.join(errors)); return 1
    from collections import Counter
    print(f"Validated {len(data['topics'])} source/baseline topics; status counts: {dict(Counter(t['status'] for t in data['topics']))}.")
    print('Structural traceability passed. Source-topic coverage and technical approval remain open; counts do not complete the pass.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
