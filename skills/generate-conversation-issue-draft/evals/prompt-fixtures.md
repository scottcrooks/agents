# Prompt evaluation fixtures

Use the skill's normal Sonata invocation frontmatter for each fixture. Evaluate only the issue sections.

## One cross-layer behavior stays vertical

Conversation: The operator requests a user-visible notification preference that requires a UI control, an API update, and persistence.

Expected: One end-to-end issue covering the observable preference behavior and all required layers; no frontend/backend/database split.

## Independent outcomes stay separate

Conversation: The operator independently requests notification preferences and an unrelated audit-log export, with both fully decided.

Expected: Two issues because each delivers an independent outcome.

## Operator feedback consolidates horizontal drafts

Conversation: An assistant proposes separate UI, API, and schema tickets. The operator replies, “Make this one end-to-end issue.”

Expected: One vertical issue; the assistant's horizontal proposal is superseded.

## Later operator decision wins

Conversation: The assistant proposes email delivery. The operator first accepts, then later says delivery must be in-app only.

Expected: The issue specifies in-app delivery and does not require email.

## Previous bundles are not requirements

Conversation: A previous generated bundle includes analytics. The operator requests regeneration and states analytics is out of scope.

Expected: No analytics requirement or issue appears in the regenerated bundle.

## Materially unresolved decisions block generation

Conversation: The operator wants notifications but has not decided whether delivery is email or in-app, and that choice changes implementation and acceptance.

Expected: Exactly one blocked issue naming the delivery-channel decision; no speculative implementation issues.
