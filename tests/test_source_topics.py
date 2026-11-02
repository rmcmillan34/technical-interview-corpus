import unittest
from tools.validate_source_topics import validate


class SourceTopicTests(unittest.TestCase):
    def setUp(self):
        self.q = dict(id='q', status='draft', classification=dict(roles=['swe'],
            competencies=dict(primary='programming',secondary=[])), assessment=dict(rubric=[dict(id='contract')]),
            review=dict(technical='pending',taxonomy='pending',provenance='approved'))
        self.data = dict(policy=dict(count_floors_are_completion_criteria=False,preferred_counts_are_caps=False),
            source_snapshots=[dict(source_id='source',commit='a'*40,reuse='topic-discovery-only',files=[dict(path='README.md',blob_sha='b'*40)])],
            topics=[dict(id='topic',competencies=['programming'],scope='general',origin='source-discovery',
                sources=[dict(source_id='source',path='README.md',locator='functions')],status='partial',
                assessment_focus='Function contract',next_action='Review remaining subtopics',
                question_evidence=[dict(question_id='q',field='rubric',criterion_id='contract')])])

    def errors(self):
        return validate(self.data,{'programming'},{'source'},{'q':self.q},{'programming'})

    def test_partial_draft_evidence_is_valid_but_cannot_close_topic(self):
        self.assertEqual(self.errors(),[])
        self.data['topics'][0]['status']='covered'
        self.assertTrue(any('reviewed and fully approved' in e for e in self.errors()))

    def test_covered_requires_specific_evidence_for_every_mapped_competency(self):
        self.q['status']='reviewed'; self.q['review']={k:'approved' for k in self.q['review']}
        topic=self.data['topics'][0];topic['status']='covered'
        self.assertTrue(any('topic-specific' in e for e in self.errors()))
        topic['question_evidence'][0]['topic_rationale']='The criterion checks the function contract required here.'
        self.assertEqual(self.errors(),[])
        topic['question_evidence'][0]['criterion_id']='missing'
        self.assertTrue(any('anchor does not resolve' in e for e in self.errors()))

    def test_uninspected_source_and_count_stopping_are_rejected(self):
        self.data['topics'][0]['sources'][0]['path']='not-read.md'
        self.data['policy']['count_floors_are_completion_criteria']=True
        errors=self.errors()
        self.assertTrue(any('not inspected' in e for e in errors))
        self.assertTrue(any('must be false' in e for e in errors))

    def test_unmapped_planned_competency_is_detected(self):
        self.data['topics']=[]
        self.assertTrue(any('absent from topic inventory' in e for e in self.errors()))


if __name__=='__main__':
    unittest.main()
