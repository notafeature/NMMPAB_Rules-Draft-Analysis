# Comment pages, withdrawn from the site

The comment page of each Part, as last published, withdrawn from the site on
October 22, 2026 at the owner's direction. Nothing here is served: GitHub Pages
publishes `docs/` only. Each address under `docs/` is now a redirect stub to its
Part's front page.

| Part | Page |
|---|---|
| 7.35.2 | `7.35.2/comment.html` |
| 7.35.3 | `7.35.3/comment.html` |
| 7.35.4 | `7.35.4/comment.html` |

To restore a page: move it back to `docs/<part>/comment.html` over its stub, put
`"comment": "Comment"` back in `NAMES`, its entry back in `GROUPS`, and
`CTA = ("comment.html", "Comment")` in `tools/parts/<part>/sync-nav.py`, restore
the footer link in `tools/build-rule-page.py` and on the hand pages, and run the
tools and `check-all.py`. The page's revision entries are in git history under
`tools/parts/<part>/sync-provenance.py`.

The input form on each page posts to the Formspree endpoint `mjgqnkvv`; withdrawing
the pages does not close that endpoint.
