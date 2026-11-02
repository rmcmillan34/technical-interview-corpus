import unittest
from tools.audit_role_coverage import summarize


def question(qid, difficulty, primary='programming', secondary=None, role='swe', status='draft'):
    return dict(id=qid, status=status,
                classification=dict(roles=[role], difficulty=dict(level=difficulty),
                                    competencies=dict(primary=primary, secondary=secondary or [])),
                assessment=dict(intent='Fixture'), question=dict(response_modes=['discussion']),
                review=dict(technical='pending', taxonomy='pending', provenance='approved'))


class CoverageAuditTests(unittest.TestCase):
    def setUp(self):
        self.plan = dict(coverage_targets=dict(core=dict(competencies=['programming'],
            default={d: dict(min=1 if d == 'D1' else 0) for d in ('D1','D2','D3','D4','D5')})))

    def test_secondary_tags_do_not_become_primary_or_reviewed_evidence(self):
        q = question('a', 'D1', primary='testing', secondary=['programming'])
        result = summarize([q], self.plan, dict(edges=[]), 'swe')
        self.assertEqual(result['competencies'][0]['tagged']['D1'], 1)
        self.assertEqual(result['competencies'][0]['primary']['D1'], 0)
        self.assertEqual(result['fully_approved_count'], 0)

    def test_other_roles_and_deprecated_questions_do_not_inflate_coverage(self):
        qs = [question('a', 'D1', role='ai-eng'), question('b', 'D1', status='deprecated')]
        result = summarize(qs, self.plan, dict(edges=[]), 'swe')
        self.assertEqual(result['question_count'], 0)
        self.assertEqual(result['competencies'][0]['below_floor'], ['D1'])

    def test_route_requires_recovery_and_shared_competency(self):
        qs = [question('a','D1'), question('b','D2'), question('c','D2',primary='testing')]
        edges = [dict(**{'from':'a','to':'b'}, relation='escalate')]
        row = lambda: summarize(qs, self.plan, dict(edges=edges), 'swe')['competencies'][0]
        self.assertFalse(row()['d1_entry_with_recovery'])
        edges.append(dict(**{'from':'b','to':'a'}, relation='recover'))
        self.assertTrue(row()['d1_entry_with_recovery'])
        edges[:] = [dict(**{'from':'a','to':'c'}, relation='escalate'),
                    dict(**{'from':'c','to':'a'}, relation='recover')]
        self.assertFalse(row()['d1_entry_with_recovery'])


if __name__ == '__main__':
    unittest.main()
