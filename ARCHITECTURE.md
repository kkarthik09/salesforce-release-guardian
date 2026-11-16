# Dependency release gates

Reviewed dependency inventory + change set -> reverse graph traversal -> shortest impact paths -> test/owner gates.
Edges point from consumer to dependency. Breadth-first traversal handles cycles and produces deterministic paths.
Deletion with surviving consumers blocks release even if those consumers are changed; supply a reviewed
post-change dependency inventory to demonstrate references were removed. The inventory must still include deleted
nodes so their historical edges can be assessed. Keep baseline and candidate artifacts separately for review.
Missing owner, test mapping, dependency nodes or inventory review blocks readiness. Approved owners are supplied
by the caller; this is a planning tool, not an authenticated approval system or a deployment authorization service.
READY means eligible for sandbox validation, never automatic production deployment.

Salesforce MetadataComponentDependency can seed inventory, but its coverage is incomplete and it is documented
as Beta. Dynamic Apex references, Flow behavior, integrations and data migrations need additional review.
No automatic metadata retrieval, rollback, Apex coverage calculation or Salesforce deployment is implemented.
Tests listed in output are mappings, not proof those tests ran or sufficiently cover the change.

Official reference:
https://developer.salesforce.com/docs/platform/api-tooling/references/tooling-objects/tooling-metadatacomponentdependency.html
