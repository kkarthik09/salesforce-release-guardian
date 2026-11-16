"""Explainable release gates over a normalized Salesforce dependency inventory."""
from collections import deque
import json

def assess(inventory, changed, deleted=(), approvals=()):
    nodes=inventory['components']; changed=set(changed); deleted=set(deleted)
    if not changed and not deleted: raise ValueError('Empty release')
    if not (changed|deleted)<=nodes.keys(): raise ValueError('Unknown component')
    reverse={n:set() for n in nodes}
    for name,component in nodes.items():
        for dep in component['depends_on']:
            if dep not in nodes: raise ValueError('Incomplete dependency inventory')
            reverse[dep].add(name)
    seeds=changed|deleted; paths={n:[n] for n in sorted(seeds)}; queue=deque(sorted(seeds))
    while queue:
        dependency=queue.popleft()
        for consumer in sorted(reverse[dependency]):
            if consumer not in paths:
                paths[consumer]=paths[dependency]+[consumer]; queue.append(consumer)
    blockers=[]; tests=set(); owners=set()
    for node,path in sorted(paths.items()):
        component=nodes[node]
        if node not in deleted:
            tests.update(component.get('tests',[]))
            if not component.get('tests'): blockers.append({'code':'NO_TEST_MAPPING','component':node,'path':path})
        owner=component.get('owner')
        if owner: owners.add(owner)
        else: blockers.append({'code':'NO_OWNER','component':node,'path':path})
    for node in sorted(deleted):
        for consumer in sorted(reverse[node]-deleted):
            # A changed consumer still references the deleted node in this supplied inventory.
            blockers.append({'code':'LIVE_DEPENDENT','component':node,'consumer':consumer})
    missing=sorted(owners-set(approvals))
    blockers.extend({'code':'OWNER_APPROVAL_MISSING','owner':o} for o in missing)
    if inventory.get('coverage')!='complete_reviewed':
        blockers.append({'code':'INVENTORY_NOT_REVIEWED'})
    return {'decision':'blocked' if blockers else 'ready_for_sandbox_validation',
            'impacted':paths,'recommended_tests':sorted(tests),'required_owners':sorted(owners),
            'blockers':blockers}

def sample():
    return {'coverage':'complete_reviewed','components':{
      'CustomField:Account.Risk__c':{'depends_on':[],'owner':'data','tests':['RiskTest']},
      'ApexClass:RiskService':{'depends_on':['CustomField:Account.Risk__c'],'owner':'sales','tests':['RiskTest']},
      'Flow:RouteAccount':{'depends_on':['ApexClass:RiskService'],'owner':'sales','tests':['RouteFlowScenario']}}}

if __name__=='__main__': print(json.dumps(assess(sample(),['CustomField:Account.Risk__c']),indent=2))
