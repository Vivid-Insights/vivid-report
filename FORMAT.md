# Report format

How to write `Report.md` so it builds into a Vivid Insights web paper. Ordinary Markdown works as usual; this file covers what is added. `papers/0000-specimen/Report.md` uses every part, and its built page shows the result.

Build with `cd Code && uv run python tools/build.py` (add `--open` to open it). The page goes to `build/<slug>/index.html`, a self-contained folder.

## Front matter

```yaml
---
title: "The title, plain and literal"
subtitle: ""                          # optional
slug: short-name                      # the page's address: reports/<slug>/
folder: papers/0002-short-name        # the paper's folder; every path in the file is relative to it
report-number: VI-2026-001            # the Vivid Insights series; ask before assigning
authors:
  - name: Ada Lovelace
    affiliation: [1]
    orcid: 0000-0000-0000-0000        # optional
    email: ada@example.org            # shown only for the corresponding author
    corresponding: true
    equal-contribution: true          # optional: marked * with "Equal contribution" under the affiliations
affiliations:
  1: Vivid Insights
date: 2026-10-09
version: "0.1"
keywords: [wordalisation, football]
licence: CC BY 4.0                    # optional: leave out and the page states no licence
disclaimer: false                     # only if the authors decide this report carries no Disclaimer section
repository: https://github.com/...    # optional: linked as the source and working record
references: references.yaml
---
```

## Sections

Every report has the same sections, in this order: `Abstract`, an optional `What We Have Built`, `Introduction`, `Methods`, `Results`, `Discussion`, `Data and code availability`, `Disclaimer`, `References`. The `Methods`, `Results` and `Discussion` share their `###` sub-headings, one per point of the paper; the `Discussion` ends with `### Limitations` and `### Looking ahead`. `instructions.md` (`The Structure of a Report`) says what goes in each.

`##` is a numbered section, `###` a numbered sub-section, `####` an unnumbered heading. These are never numbered: `Abstract`, `What We Have Built`, `Disclaimer`, `References`, `Acknowledgements`, `Appendix`, `Data and code availability`, `Funding`. Add `{-}` to the end of any other heading to leave it unnumbered, and `{#sec-name}` to give it an id for cross-references.

- `## Abstract` is lifted out of the body into the title block.
- `## Disclaimer` is required. The build fails without it.
- `## References` is filled in by the build from `references.yaml`. Write nothing under it.

## Figures, videos and interactive figures

All three are numbered as figures, in the order they appear. The block's text is the caption. Paths are relative to the paper's folder (`folder:` in the front matter), wherever the Markdown file happens to be.

In Obsidian a block shows only its caption, so its first line can be an embed of its file from the top of the vault, `![[papers/NNNN-slug/Code/outputs/figures/pipeline.png]]`: the image, the video, or an interactive's `fallback=` still. The page ignores the line, and the build warns when it no longer matches the block. `cd Code && uv run python tools/obsidian.py` writes and refreshes these lines for every figure, video, interactive and panel block, and touches nothing else.

```markdown
::: figure {#fig-pipeline src="Code/outputs/figures/pipeline.png" alt="What the image shows, for screen readers"}
Caption: what the figure shows and how to read it.
:::
```

- A dark-theme version is picked up automatically from `dark/` beside the image (`Code/outputs/figures/dark/pipeline.png`), which is where `viz_style.save` puts it. Or name it with `dark="…"`.
- PNGs made with `viz_style` are shown at the size that makes their 11 pt text match the body text. Add `width=wide` for a figure wider than the text column, `width=full` for the full window, `width=narrow` for a small one.

```markdown
::: video {#fig-demo src="Code/outputs/videos/demo.mp4" poster="Code/outputs/videos/demo-poster.png"}
Caption.
:::
```

- Add `loop` for a short silent animation that plays like a moving figure; without it the video has controls.
- `youtube="VIDEO_ID"` or `vimeo="VIDEO_ID"` instead of `src` for anything long. Keep video files under about 20 MB.
- A `dark/` version of the video and poster is picked up as for figures. A poster is required for print.

```markdown
::: interactive {#fig-explorer src="Code/interactives/explorer/index.html" height=480 fallback="Code/outputs/figures/explorer.png"}
Caption.
:::
```

- The whole folder of the `index.html` is published. It must be self-contained: no build step, no keys, no calls to an LLM or a paid API.
- `fallback=` is the still shown in print.
- To follow the page's light or dark theme, listen for the message the page sends: `window.addEventListener("message", e => { if (e.data && e.data.vividTheme) document.documentElement.dataset.theme = e.data.vividTheme; })`. `papers/0000-specimen/interactives/threshold-explorer/` does this.

### Figures with panels

A figure made of panels (a), (b), …, like LaTeX's subfigure. The outer block uses more colons than the panels inside it. Text outside the panels is the figure's caption.

```markdown
::::: figure {#fig-workflow cols=2 width=wide}
:::: panel {#fig-workflow-a src="Code/outputs/figures/a.png" alt="…"}
Caption of panel (a).
::::
:::: panel {#fig-workflow-b}
Any Markdown, boxes or tables. The last paragraph is the panel's caption.

Caption of panel (b).
::::
Caption of the whole figure.
:::::
```

`@fig-workflow-b` gives "Figure 1b". `cols=` sets panels side by side.

### Boxes

```markdown
::: box {label="Normative model:" source="Attachments/paper/main.tex"}
Text in a framed box, like LaTeX's tcolorbox. The label is set in bold at its start.
:::
```

Add `.rounded` for rounded corners. With `source=` the text is checked word for word against that file, as for quoted outputs; a `.tex` source is compared after LaTeX markup is removed.

## Generated text: outputs, prompts and conversations

Generated text is quoted, never written. Each block names the file it comes from, and the build fails if the text is not word for word what the file says.

```markdown
::: output {source="Attachments/cache.json" key="0.texts.2" model="gpt-4o, 2026-09-30"}
The text exactly as generated.
:::
```

- `key` points into a JSON file: dots between keys, numbers for list positions. The text must equal that value. Without `key`, the text must appear somewhere in the file.
- `prompt` is the same block for prompt text, shown in a monospaced face.
- `source="hand-written"` for an example written by a person. The page labels it "hand-written example". There is no other way to put text in one of these blocks.

```markdown
::: conversation {source="Attachments/transcripts/session-3.txt" assistant="Ask Afya"}
User: What does my blood pressure mean?
Ask Afya: Your systolic blood pressure of 110 is ...
:::
```

- One `Speaker: text` per turn. The speaker named in `assistant=` is drawn as the agent. Each turn must appear in the source file.
- Add `{#fig-name caption="…"}` to any of these blocks to number it as a figure with a caption.

`.obsidian/snippets/vivid-report.css` styles a report while it is being written: quoted blocks as blockquotes, figures centred and capped in height on a white ground so a black SVG survives a dark theme, and section headings marked. It is enabled in `.obsidian/appearance.json` and adds nothing to `Report.md`, so the build neither sees it nor depends on it. Obsidian still shows the `:::` fence lines themselves as plain text; they are the price of a build that checks every quote.

Obsidian shows one of these blocks as bare text, running it together with the prose around it. `cd Code && uv run python tools/obsidian.py` puts a `> ` on each line of every `output`, `prompt` and `conversation` block, which Obsidian renders as a blockquote; the build takes the prefix off again before it checks the text and before it publishes, so the quote stays word for word. Write the text either way and run the tool; it adds what is missing and leaves what is already right.

## Tables

```markdown
::: table {#tab-configs}
Caption, above the table as in a printed paper.
| Configuration | Scale | Threshold |
| --- | --- | ---: |
| A | log-odds | 0.45 |
:::
```

Tables are set in the booktabs style: rules above and below, one under the header, no vertical lines.

## Equations and definitions

```markdown
$$
z = \frac{x - \mu}{\sigma}
$$ {#eq-z}
```

Display equations are numbered on the right; leave off `{#eq-…}` and they are still numbered. Write `{-}` after the closing `$$` for an unnumbered one. Inline maths is `$x$`. LaTeX is rendered by KaTeX.

```markdown
::: definition {#def-wordalisation title="Wordalisation"}
The text of the definition.
:::
```

## Cross-references

| Write | Get |
| --- | --- |
| `@fig-pipeline` | Figure 1 |
| `@tab-configs` | Table 1 |
| `@eq-z` | (1) — write "equation @eq-z" |
| `@sec-method` | Section 2 |
| `@def-wordalisation` | Definition 1 |

Put `-` before the `@` for the number alone, when the text supplies its own word: `Fig.&nbsp;-@fig-pipeline` gives "Fig. 1", `[-@fig-pipeline]` likewise. A cross-reference to an id that does not exist is an error. A figure or table never referred to is a warning.

## Citations and references

| Write | Get |
| --- | --- |
| `[@caut2025]` | (Caut et al., 2025) |
| `[@caut2025, p. 4]` | (Caut et al., 2025, p. 4) |
| `[@caut2025; @sumpter2016]` | (Caut et al., 2025; Sumpter, 2016) |
| `@caut2025` | Caut et al. (2025) |
| `[-@caut2025]` | (2025) |

Hovering a citation shows the reference. Two works by the same authors in the same year become 2025a and 2025b automatically.

`references.yaml` holds the list. An author written "others" (BibTeX's "and others") is shown as "et al."; a work with no date takes `year: n.d.`.

```yaml
- id: caut2025
  type: preprint              # article, preprint, book, chapter, report, software, dataset, web
  author: ["Caut, Amandine M.", "Sumpter, David J. T."]   # "Family, Given"; a body as "World Health Organization"
  title: "Representing data in words: A context engineering approach"
  year: 2025
  container: arXiv            # journal, or the series or site
  number: "2503.15509"        # preprint number, report number
  volume: ""                  # issue, pages also accepted
  doi: ""                     # or url: every reference needs one
  url: https://arxiv.org/abs/2503.15509
  note: Preprint, not peer reviewed.
  version: ""                 # software and datasets
  publisher: ""               # books, reports, software
```

A reference without a `doi` or `url` is an error. A citation not in the file is an error. A reference never cited is a warning.

## Footnotes and other Markdown

Footnotes (`text[^1]` and `[^1]: the note`) are collected into a `Notes` section before the references. Tables, lists, block quotes and code blocks work as usual. HTML is allowed but should be rare: the build cannot check it.

## Unfinished work

`[TO WRITE: …]`, `[CHECK: …]` and `[PLACEHOLDER: …]` are highlighted on draft pages. So are the template notes that start `*Step N …*`. A release build — the one `review.py request` and `publish.py` make — treats every one of them as an error.

## What the page does

- A brand bar with Cite, Print / PDF and a light/dark switch. The reader's system setting chooses the theme first; their choice is remembered.
- A contents rail that follows the reader on wide screens.
- Draft and review-copy banners, which only an approved release build drops.
- `?embed` at the end of the address hides the brand bar, contents and footer, for showing a report inside another page in an `<iframe>`. `?theme=dark` or `?theme=light` forces a theme.
- Print gives an A4 paper: videos become their posters, interactives their fallbacks.
- Google Scholar `citation_*` tags, a BibTeX entry, and the review record at the foot.
