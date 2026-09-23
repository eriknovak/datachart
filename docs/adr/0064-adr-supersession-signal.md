---
status: accepted
---

# A superseded ADR says so in its frontmatter; the records are not merged

Issue #269 opened on a contradiction: 0061 said the basemap outlines ship in
the wheel, 0062 said they do not, and 0061 gave the reader no hint that it had
been overtaken. The `status:` field existed on all 61 ADRs and read `accepted`
on every one of them, so it carried no signal at all.

The obvious fix — merge a superseded ADR into its successor — is the wrong
operation almost everywhere here. The records are a dense web rather than a
stack of amendments: `datachart/*.py` cites ADRs by number 215 times across 50
of them, and 40-odd ADRs cite each other, some in both directions (0022↔0023,
0029↔0030). Renumbering or removing one rewrites all of that plus every
reference already fixed in git history, PR bodies and issue comments. The log
is also the artifact: 0042→0045→0049→0050 reads as a real evolution of the
emphasis rules, and flattened it would say only what the code already says.

The basemap pair was folded anyway (see 0062), for a reason that does not
recur: `BasemapChart` merged after 0.10.2, so the bundled map never reached a
user and there was no history to preserve — only two documents disagreeing
about a feature that has only ever existed one way. Every other pair documents
something that shipped.

## Commitments

- **A later ADR that changes an earlier one's commitment is recorded on the
  earlier ADR**, as `amended-by: [0045]` in its frontmatter, listing every
  later number in ascending order. The amended ADR still governs everything
  its successor did not touch, so its `status:` stays `accepted` — the key
  says "read 0045 too", not "stop reading this".
- **`status:` gains a superseding form for a whole-record reversal**:
  `superseded by ADR NNNN`, when a later ADR leaves nothing of the earlier one
  standing. No ADR carries it today, and the format is written down so the
  first one to need it does not invent a spelling.
- **Neither key ever moves a citation.** Code comments, ADR cross-references,
  issue threads and merged PRs keep pointing at the number they always did.
  The signal is added where the reader lands, and nothing that points at a
  record has to be rewritten to add it.
- **`docs/adr/README.md` is the index**, grouped by subsystem so "everything
  about the basemap" or "everything about emphasis" is one lookup even when it
  spans four records. Each line carries the number, the title, and the
  amendments. Gaps in the numbering are listed with the reason, so 0061's
  absence reads as a decision rather than a lost file.
- **An amendment is a changed commitment, not a citation.** An ADR that builds
  on, extends consistently with, or merely mentions an earlier one adds no
  tag; one that reverses, narrows, widens or replaces something the earlier
  one committed to does. 0021 fulfilling a reservation 0020 made is not an
  amendment; 0017 spelling its axes against 0012's rule is.
- **A follow-up the earlier ADR already named is not an amendment either.**
  0034 deferred a rename and said so in its own text, so 0043 carrying it out
  changes nothing a reader of 0034 would get wrong. The tag exists for the
  reader who would otherwise be surprised, and a deferral is not a surprise.
  0043 reversing 0035's silent alias is, and is tagged.

## Considered options

- **Merge every superseded ADR into its successor.** Rejected: see above — it
  rewrites the citation graph and destroys the record of how a decision was
  reached, to save a reader one hop.
- **Carry the signal in `status:` alone**, as `accepted, amended by ADR 0045`.
  Rejected: it overloads one field with two meanings and makes the common case
  (`accepted`) a prefix match rather than a value.
- **A `superseded-by:` key used for partial amendments too**, as issue #269
  first sketched it. Rejected: "superseded" tells the reader to stop, and an
  amended ADR is still the governing record for everything its successor left
  alone. The distinction is the whole point of tagging.
- **Nothing but the index.** Rejected: a reader arrives at an ADR through a
  code comment far more often than through the index, and the warning has to
  be where they land.
