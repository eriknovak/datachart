# Domain Docs

How the engineering skills should consume this repo's domain documentation when exploring the codebase.

## Before exploring, read these

- **`CONTEXT.md`** at the repo root, or
- **`CONTEXT-MAP.md`** at the repo root if it exists — it points at one `CONTEXT.md` per context. Read each one relevant to the topic.
- **`docs/adr/`** — read ADRs that touch the area you're about to work in. `docs/adr/README.md` indexes them by subsystem; start there to find every record on one area. In multi-context repos, also check `src/<context>/docs/adr/` for context-scoped decisions.

An ADR whose frontmatter carries `amended-by: [NNNN]` still governs, but a later record changed part of it — read both. `status: superseded by ADR NNNN` means read the successor instead.

If any of these files don't exist, **proceed silently**. Don't flag their absence; don't suggest creating them upfront. The `/dev-tools:domain-modeling` skill (reached via `/dev-tools:grill-with-docs` and `/dev-tools:improve-codebase-architecture`) creates them lazily when terms or decisions actually get resolved.

## File structure

Single-context repo (most repos):

```
/
├── CONTEXT.md
├── docs/adr/
│   ├── 0001-event-sourced-orders.md
│   └── 0002-postgres-for-write-model.md
└── src/
```

Multi-context repo (presence of `CONTEXT-MAP.md` at the root):

```
/
├── CONTEXT-MAP.md
├── docs/adr/                          ← system-wide decisions
└── src/
    ├── ordering/
    │   ├── CONTEXT.md
    │   └── docs/adr/                  ← context-specific decisions
    └── billing/
        ├── CONTEXT.md
        └── docs/adr/
```

## Use the glossary's vocabulary

When your output names a domain concept (in an issue title, a refactor proposal, a hypothesis, a test name), use the term as defined in `CONTEXT.md`. Don't drift to synonyms the glossary explicitly avoids.

If the concept you need isn't in the glossary yet, that's a signal — either you're inventing language the project doesn't use (reconsider) or there's a real gap (note it for `/dev-tools:domain-modeling`).

## Flag ADR conflicts

If your output contradicts an existing ADR, surface it explicitly rather than silently overriding:

> _Contradicts ADR-0007 (event-sourced orders) — but worth reopening because…_

When a new ADR does change an earlier one's commitment, tag the earlier file with `amended-by: [NNNN]` and add the new one to `docs/adr/README.md` (ADR 0064). Never renumber or delete an ADR to resolve a contradiction — its number is cited from code comments, issues, and merged PRs.
