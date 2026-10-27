# sabren/appengine-workshop

> A two-file extraction of workshop library code, adapted for Google
> App Engine, committed on a single day (2012-12-28). It is NOT
> just sabren/workshop repackaged — workshop is a much larger
> framework-plus-docs tree, while this repo carries only two adapted
> library modules and a three-line README.
> Repo: https://github.com/sabren/appengine-workshop — 4 files, git
> history in this clone entirely on 2012-12-28. **Keep — it is the
> App Engine adaptation record for two workshop modules, distinct
> from workshop itself.**

## Is it just workshop repackaged? No — explicitly checked

Compared file by file against
https://github.com/sabren/workshop (cloned for this check):

- **Scope:** workshop holds `code/` (27 modules: arlo, clerks,
  clockwork, sixthday, strongbox, zebra, weblib, handy, and more),
  `docs/` (Sphinx sources plus a large `drafts/` archive), `specs/`,
  and app scaffolding. appengine-workshop holds only `README.md`,
  `handy.py`, `weblib.py`, and `.gitignore`. A repackaging of
  workshop would carry the framework; this carries two modules.
- **`weblib.py` (978 lines):** closely related to workshop's
  `code/weblib.py` — "Classes for easy server-side web scripting in
  Python" — with small adaptations: it imports itself
  (`import weblib # yes, this very file`), raises `TypeError`
  instead of string exceptions in `urlEncode`/`urlDecode`, uses `+=`
  string building, and adds a `ResponseTest` unittest class (the
  final commit is "added missing 'class' line (ResponseTest was
  merged into class above)"). This is the workshop weblib lineage,
  touched up — not a fresh copy of the whole tree.
- **`handy.py` (318 lines):** "handy routines for python" with
  explicit App Engine guards in the optional imports
  (`except IOError: pass # app engine` on the genshi and
  `Ft.Xml.Domlette` imports) and a TODO to split it into
  submodules "so it doesn't import everything under the sun". It
  differs substantially from workshop's `code/handy.py` (different
  import set: `re`, `hashlib`, `htmlentitydefs`, `datetime`), so it
  reads as a divergent App Engine-targeted variant of the handy
  module, not a verbatim copy.
- **History:** all five commits are dated 2012-12-28 ("import of
  working versions", "make weblib import weblib for the time being",
  "old changes to handy for app engine"). The README is three
  lines: "workshop / ======== / webapp workshop libraries".

## Verdict

**Keep.** Small, distinct, and self-describing once the workshop
comparison is made: it is the App Engine snapshot of two modules,
not a duplicate of workshop, so there is no redundancy to clean up.
