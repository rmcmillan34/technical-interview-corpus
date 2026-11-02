#!/usr/bin/env python3
"""Report inventory separately from assessment quality and release readiness.

Run after the schema, provenance and progression validators. Counts are advisory;
secondary tags do not establish separately assessed competence.
"""
from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

import yaml

DIFFICULTIES = ('D1', 'D2', 'D3', 'D4', 'D5')


def summarize(questions: list[dict], plan: dict, graph: dict, role: str) -> dict:
    selected = {q['id']: q for q in questions
                if role in q['classification']['roles'] and q['status'] != 'deprecated'}
    edges = [e for e in graph['edges'] if e['from'] in selected and e['to'] in selected]
    connected = {e[k] for e in edges for k in ('from', 'to')}
    overall = Counter(q['classification']['difficulty']['level'] for q in selected.values())
    rows = []
    for tier, block in plan['coverage_targets'].items():
        for competency in block['competencies']:
            tagged = {i: q for i, q in selected.items() if competency in {
                q['classification']['competencies']['primary'],
                *q['classification']['competencies']['secondary']}}
            primary = [q for q in tagged.values()
                       if q['classification']['competencies']['primary'] == competency]
            counts = Counter(q['classification']['difficulty']['level'] for q in tagged.values())
            primary_counts = Counter(q['classification']['difficulty']['level'] for q in primary)
            relevant_edges = [e for e in edges if e['from'] in tagged and e['to'] in tagged]
            entry_edges = [e for e in relevant_edges if e['relation'] == 'escalate'
                           and selected[e['from']]['classification']['difficulty']['level'] == 'D1']
            recovery_pairs = {(e['from'], e['to']) for e in relevant_edges if e['relation'] == 'recover'}
            rows.append(dict(competency=competency, tier=tier,
                tagged={d: counts[d] for d in DIFFICULTIES},
                primary={d: primary_counts[d] for d in DIFFICULTIES},
                below_floor=[d for d in DIFFICULTIES if counts[d] < block['default'][d]['min']],
                d1_entry_with_recovery=any((e['to'], e['from']) in recovery_pairs for e in entry_edges)))
    return dict(role=role, question_count=len(selected),
        difficulty={d: overall[d] for d in DIFFICULTIES},
        reviewed_count=sum(q['status'] == 'reviewed' for q in selected.values()),
        fully_approved_count=sum(q['status'] == 'reviewed' and all(
            q['review'][k] == 'approved' for k in ('technical', 'taxonomy', 'provenance'))
            for q in selected.values()),
        with_rubric=sum(bool(q['assessment'].get('rubric')) for q in selected.values()),
        with_followups=sum(bool(q.get('followups')) for q in selected.values()),
        response_modes=dict(sorted(Counter(m for q in selected.values()
                                          for m in q['question']['response_modes']).items())),
        edges=dict(sorted(Counter(e['relation'] for e in edges).items())),
        isolated_by_difficulty={d: sum(i not in connected and
            q['classification']['difficulty']['level'] == d for i, q in selected.items())
            for d in DIFFICULTIES}, competencies=rows)


def markdown(data: dict) -> str:
    lines = [f"# {data['role'].upper()} coverage inventory", '',
        'Counts include active draft and reviewed questions. Tagged coverage includes secondary labels; it is not evidence of separately assessed competence.', '',
        f"Questions: {data['question_count']}; reviewed: {data['reviewed_count']}; fully approved: {data['fully_approved_count']}.",
        f"With explicit rubric: {data['with_rubric']}; with embedded follow-ups: {data['with_followups']}.",
        'Difficulty: ' + ', '.join(f'{d}={n}' for d, n in data['difficulty'].items()) + '.',
        'Graph: ' + ', '.join(f'{k}={v}' for k, v in data['edges'].items()) + '.',
        'Isolated nodes: ' + ', '.join(f'{d}={n}' for d, n in data['isolated_by_difficulty'].items()) + '.', '',
        'Counts in each cell follow D1 / D2 / D3 / D4 / D5. A route means at least one shared-competency D1 escalation with its recovery edge, not full graph coverage.', '',
        '| Tier | Competency | Tagged | Primary | Below floor | D1 route + recovery |',
        '|---|---|---|---|---|---|']
    for r in data['competencies']:
        tagged = ' / '.join(str(n) for n in r['tagged'].values())
        primary = ' / '.join(str(n) for n in r['primary'].values())
        gaps = ', '.join(r['below_floor']) or '—'
        route = 'yes' if r['d1_entry_with_recovery'] else 'no'
        lines.append(f"| {r['tier']} | {r['competency']} | {tagged} | {primary} | {gaps} | {route} |")
    return '\n'.join(lines) + '\n'


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--role', default='swe')
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args()
    load = lambda p: yaml.safe_load(p.read_text(encoding='utf-8'))
    questions = [load(p) for p in sorted((args.root / 'questions').rglob('*.yaml'))]
    data = summarize(questions, load(args.root / 'coverage' / f'{args.role}.yaml'),
                     load(args.root / 'paths' / f'{args.role}.yaml'), args.role)
    print(json.dumps(data, indent=2) if args.json else markdown(data), end='\n' if args.json else '')


if __name__ == '__main__':
    main()
