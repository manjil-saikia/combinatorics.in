# combinatorics.in

Teaching site for Manjil P. Saikia. Jekyll, hosted on GitHub Pages.

Each course is one Markdown file in `_courses/`. Everything on the course page —
the metadata strip, the grading bar, the lecture log, the problem-set list, the
reading list, the diagram — is generated from that file's front matter. Adding a
lecture is a one-line edit.

---

## Running it locally

```bash
bundle install
bundle exec jekyll serve --livereload
# http://localhost:4000
```

The `Gemfile` pins `github-pages`, which is the exact gem set GitHub runs, so a
local preview cannot drift from production.

---

## Deploying

1. Create a repo (any name — `combinatorics-in` is fine) and push this tree to `main`.
2. **Settings → Pages → Source: Deploy from a branch**, branch `main`, folder `/ (root)`.
3. **Settings → Pages → Custom domain**: `www.combinatorics.in`. The `CNAME` file in
   this repo already contains that, so it should populate itself.
4. DNS at your registrar:
   - `CNAME` record, host `www`, value `<username>.github.io.`
   - For the bare domain, four `A` records for the apex pointing at
     `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`
     (and the `AAAA` equivalents if you want IPv6). GitHub redirects apex → www.
5. Tick **Enforce HTTPS** once the certificate is issued (usually under an hour).
6. Turn off the old Google Sites publication *after* DNS has cut over, not before.

---

## Adding a course

Copy an existing file in `_courses/` and edit it. The filename is the URL:
`_courses/mat631.md` → `/courses/mat631/`.

### Front matter reference

| Key | Required | What it does |
| --- | --- | --- |
| `code` | yes | Small label above the title (`MAT 631`, `Open online course`) |
| `title` | yes | Course title |
| `subtitle` | | Italic line under the title |
| `term` | yes | `Winter 2025`, `2026`, `TBC` |
| `status` | yes | `Current`, `Upcoming`, `Archive` — shown as a chip |
| `where` | | Institution, appended to `code` |
| `weight` | yes | Sort order on the index. Lower = nearer the top |
| `featured` | | `true` puts it on the home page |
| `card` | yes | One sentence, shown on the card |
| `chips` | yes | Short labels on the card |
| `graphic` | yes | Which diagram to use — see below |
| `caption` | | Caption under the diagram (HTML allowed) |
| `meta` | | List of `{label, value}`, the strip under the title (HTML allowed) |
| `grading` | | List of `{part, weight, note}`. Weights should total 100 |
| `grading_note` | | Paragraph under the grading bar |
| `lectures` | | List of `{date, topic, kind}`. Leave empty for an empty state |
| `lectures_note` | | What to show when `lectures` is empty |
| `sets` | | List of `{label, meta, url}` — problem sets, papers |
| `sets_note` | | Note under the problem-set list |
| `refs` | yes | List of `{title, meta, main, url}`. `main: true` tags it "Main text" |
| `policy` | | `au` pulls in the shared policy block from `_data/policies.yml` |
| `late_penalty` | if `policy` | e.g. `20% per day` — substituted into the shared text |
| `redirect_from` | | Old paths that should 301 here |

The body of the file, below the front matter, is the course description. Plain
Markdown.

### Adding a lecture

One line at the end of the `lectures:` list:

```yaml
  - { date: "Wed 12 Feb", topic: Jeu de taquin, RSK correspondence }
```

Add `kind: talk` for student presentations and guest lectures (renders italic and
muted), or `kind: exam` for exams. The numbering is automatic.

**YAML quoting.** Plain unquoted values are fine and handle apostrophes without
fuss (`Maschke's theorem`). Single-quote the value if it contains a colon
followed by a space:

```yaml
  - { date: "Tue 25 Mar", topic: 'Student presentations: determinant evaluations', kind: talk }
```

---

## Mathematics

KaTeX is loaded on every page. Write inline maths as `\( ... \)` and display maths
as `\[ ... \]`.

```yaml
  - { date: "Mon 29 Sep", topic: 'A basis for \(S^\lambda\)' }
```

Kramdown leaves both delimiters alone, so nothing needs escaping. `$...$` is
deliberately **not** a delimiter — it collides with kramdown's own maths handling.

---

## Diagrams

Every diagram is hand-written SVG in `_includes/gfx/`, using CSS custom properties
(`var(--facet-top)` and friends) for every colour. That means one copy of each
serves both the light and dark themes.

Currently:

| Name | What it shows | Used by |
| --- | --- | --- |
| `hooks` | Hook lengths of λ = (5,4,2,1) | MAT 631 |
| `younglattice` | Young's lattice up to n = 4 | MAT 730 |
| `qbinom` | A lattice path in a 3×5 box cutting out (5,3,2) | q-analysis |
| `catalan` | Dyck path, triangulated hexagon, binary tree | Cataland |
| `permplot` | σ = 351426 with a 231 pattern marked | Permutations |
| `chain` | The MAT 315 → 631 → 730 sequence | Home page |
| `tiling` | Plane partition in a 5×5×5 box (animated) | Home page hero |

To add one: drop `_includes/gfx/yourname.svg` in, add a `when 'yourname'` clause to
`_includes/graphic.html`, and set `graphic: yourname` on the course. Use
`var(--facet-top)`, `var(--facet-left)`, `var(--facet-right)`, `var(--accent)`,
`var(--line)`, `var(--muted)` and `var(--surface-2)` for fills so it themes itself.

`gen_svg.py` (kept outside this repo) generated the current set; the SVGs are
plain files now and can be edited by hand.

---

## Colours and type

The palette is in `assets/css/style.css`, at the top, in two blocks: `:root` for
light and `:root[data-theme="dark"]` for dark. The whole system is the three faces
of a cube — amber, teal, sage. `--accent` is whichever of the three has contrast
against the current background: teal on light, amber on dark. Change those two
blocks and the entire site, diagrams included, follows.

Type is Fraunces (display), Figtree (body), Azeret Mono (labels), from Google Fonts.

The theme toggle remembers the choice in `localStorage` and otherwise follows the
operating system. The set-before-paint script lives in `_includes/head.html`; keep
it inline, or the page will flash the wrong theme on load.

---

## Redirects

`jekyll-redirect-from` handles the old Google Sites paths on this domain:

| Old | New |
| --- | --- |
| `/home` | `/` |
| `/cataland` | `/courses/cataland/` |
| `/permutations` | `/courses/permutations/` |
| `/advanced-q-analysis` | `/courses/q-analysis/` |

**Still to do, in the other repo.** MAT 631 and MAT 730 currently live at
`manjilsaikia.in/teaching/AhdUni/MAT631/` and `.../MAT730/`. Those are a different
site, so this repo cannot redirect them. In `manjilsaikia.github.io`, add
`jekyll-redirect-from` and put this on each of those pages:

```yaml
redirect_to: https://www.combinatorics.in/courses/mat631/
```

---

## Known gaps

- **Problem-set PDFs are still hosted on `manjilsaikia.in` and Google Drive.**
  Worth moving them into this repo under `assets/pdf/<course>/` so the two sites
  are not coupled and the Drive links cannot rot.
- **Permutations has no term or venue** — currently `term: TBC`, no lecture log.
- **q-analysis is marked `Archive`** on the basis that registration closed in
  April 2025. If a second run or "Advanced q-analysis II" is coming, change
  `status` and add a new file.
- **Cataland's dates** are not published yet; only the daily time and venue are.

---

## Licence

Site code: do as you like with it. Course notes and problem sets: CC BY-SA 4.0.
