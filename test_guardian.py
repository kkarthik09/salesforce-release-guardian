import unittest
from guardian import assess,sample
class GuardianTests(unittest.TestCase):
    def setUp(self): self.m=sample(); self.field='CustomField:Account.Risk__c'
    def test_transitive_path(self):
        r=assess(self.m,[self.field]); self.assertEqual(r['impacted']['Flow:RouteAccount'],[self.field,'ApexClass:RiskService','Flow:RouteAccount'])
    def test_missing_approvals_block(self): self.assertEqual(assess(self.m,[self.field])['decision'],'blocked')
    def test_approved_only_ready_for_sandbox(self):
        self.assertEqual(assess(self.m,[self.field],approvals=['data','sales'])['decision'],'ready_for_sandbox_validation')
    def test_delete_live_dependency_blocks(self):
        r=assess(self.m,[],deleted=[self.field],approvals=['data','sales'])
        self.assertIn('LIVE_DEPENDENT',[x['code'] for x in r['blockers']])
    def test_cycles_terminate(self):
        self.m['components'][self.field]['depends_on']=['Flow:RouteAccount']
        self.assertEqual(len(assess(self.m,[self.field])['impacted']),3)
    def test_unknown_component(self):
        with self.assertRaises(ValueError): assess(self.m,['unknown'])
    def test_incomplete_edge(self):
        self.m['components'][self.field]['depends_on']=['unknown']
        with self.assertRaises(ValueError): assess(self.m,[self.field])
    def test_missing_test_blocks(self):
        self.m['components']['Flow:RouteAccount']['tests']=[]
        self.assertIn('NO_TEST_MAPPING',[x['code'] for x in assess(self.m,[self.field])['blockers']])
    def test_unreviewed_inventory_blocks(self):
        self.m['coverage']='partial'
        self.assertIn('INVENTORY_NOT_REVIEWED',[x['code'] for x in assess(self.m,[self.field])['blockers']])
    def test_empty_change_rejected(self):
        with self.assertRaises(ValueError): assess(self.m,[])
if __name__=='__main__': unittest.main()
