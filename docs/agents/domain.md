# Domain docs

- Glossary: `docs/GLOSSARY.md`
- ADRs: `docs/adr/`

## Reading them

Before exploring an area, read the glossary and any ADR that touches it. Name domain concepts with the glossary's terms in titles, tests, and proposals. When your output contradicts an ADR, say so and name the ADR.

A missing glossary or ADR folder is normal: carry on without mentioning it. Create them at these paths the first time a term or decision is settled.

## Coverage

Many people maintain this repo, and most decisions are never written up as ADRs. A missing ADR does not mean no decision was made: the code, its tests, and merged PRs are the record of current behavior. When code and an ADR disagree, say so, but don't call the code wrong on that basis alone.

Write an ADR only when the user asks for one or agrees to one, for a decision made in the session. Never ask another contributor for an ADR, and never flag a PR or review for lacking one.
