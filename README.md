# Silver Solutions — Portfolio Site

Bilingual (English / Arabic RTL) one-page site for Silver Solutions, a remote Odoo
implementation, training, and support partner working worldwide with a focus on the
Saudi market.

## Structure

| Path | Purpose |
|---|---|
| `site.src.html` | **The file you edit.** Brand images are referenced as `__ASSET:name.png__` placeholders. |
| `assets/` | Brand PNGs (logo mark and horizontal logo, light and dark variants). |
| `build.py` | Inlines the assets as base64 data URIs and writes `index.html`. |
| `index.html` | **Generated — do not edit by hand.** This is the deployable page. |

## Build

```bash
python3 build.py
```

Requires Python 3 with no third-party packages. Edit `site.src.html`, run the build,
and `index.html` is regenerated.

## Why the build step

The page has to work as a single self-contained file (no external asset requests), so
the logos are embedded as data URIs. Keeping the source separate means `site.src.html`
stays readable and diffable instead of carrying 400 KB of base64.

## Local preview

```bash
python3 -m http.server 4321
```

Then open <http://localhost:4321/index.html>.

## Notes for future edits

- **Themes:** light and dark are both defined as CSS custom properties in three blocks —
  bare `:root` (light), `@media (prefers-color-scheme: dark)` guarded with
  `:root:not([data-theme="light"])`, and `:root[data-theme="dark"]`. Never define a
  color only inside a media or `[data-theme]` block. A sun/moon button in the nav sets
  `data-theme` and persists the choice to `localStorage`.
- **Languages:** every translatable string is two sibling spans, `.en` and `.ar`. CSS
  hides the inactive one and flips the document to RTL. The choice persists to
  `localStorage`.
- **Phone and email in Arabic:** these are wrapped with `direction:ltr` so digits and
  the leading `+` do not reorder in RTL context.
- **The hero mark animation:** the glow layer is deliberately *not* animated. A
  transform or opacity animation there gets promoted to a compositing layer that paints
  above its siblings and washes out the logo.
