# Appendix

*The running record, filled from the first step. Everything a reviewer needs to check the report and that does not belong in it: where the material came from, what was decided and why, the workings, and what was tried and abandoned. Not published as part of the page.*

## Source Material

**The paper.** `Wordalisation.zip`, an Overleaf download placed in the workspace by David on 9 October 2026, now in `Attachments/` (SHA-256 `44a75df8117375cc5972a48afb277ae4978c128b46a646a96b7b4b77dbbcd115`). It holds four versions of the paper: `neurips_2026.tex`, `ACL_article.tex`, `nature submission/article_nature.tex` and the older `other/article_v2.tex`, plus a cover letter, a rebuttal and style files. The zip is kept out of git because of the cover letter and rebuttal.

**Version used: `neurips_2026.tex`.** Its words are the same as the ACL version's apart from figure layout; the Nature and `article_v2` versions have different section structures. Copied unchanged to `Attachments/wordalisation-paper/` with the BibTeX file and the five images the paper uses:

| File | SHA-256 |
| --- | --- |
| `neurips_2026.tex` | `bcd8b572e4169dd4f1f61db0389cb44348f86ed21d4eac8eae2b538d79d614ce` |
| `reference_nature.bib` | `63dbed03e98c4d21ab77ba1bec52919749d134c7ea885fb695722c25a608098d` |
| `Images/wordalisation_process.png` | `ce57e6a330d71efd53344b3ef9e6f0b4474338649fcc65d2cab1c65234a17949` |
| `Images/try1.png` | `c10b16262b1712f661d9694fdc3ac0319a80afc6948a3474aaa2f1129c2d7fd4` |
| `Images/try2.png` | `e57f8b6a222c174fbe559b4a5dd3ac32f354efbf02457d8eee75129f94675daa` |
| `Images/accuracy_plot.png` | `2feacc0bf6feeb835a953c6373e3ee1142e01469f44c814fecfc0ebd393b3186` |
| `Images/votes_percentage_per_metric2.png` | `f52cdc2dd872b4e16801b545be4f5581ba77a961ad05bb23cd1f701fe0ca8b0f` |

**Instruction.** "Make this a vivid insights report. Do not change any of the text." Taken to cover every word of the paper as it compiles: title, authors and affiliations, abstract, body, captions, boxes, table, footnotes and reference details. Not included, because they are not part of the paper as published: the NeurIPS checklist (`\input{checklist.tex}`) and every passage commented out with `%`.

## Framing

*Step 2. The reader, the kind of report (method, application, evaluation), the contributions and what will show each, and what was considered and set aside.*

## Method Facts

*Step 3. One row per fact the report states about the method, with the place in the code that makes it true. Re-checked in step 8 against the commit recorded here.*

| Fact | Where in the code | Commit |
| --- | --- | --- |

## Workings

*Steps 4 and 5. One sub-heading per example or evaluation: how each case was chosen, which outputs were generated with what model, prompt and configuration, the diagnostics, and anything made but not used.*

## Log

*A numbered row per step taken, added as the work happens: what was done, what it changed, and where the output is. Superseded decisions stay, marked as such. Review rounds, the disclaimer confirmation and publication are recorded here too.*

| # | What was done | Output |
| --- | --- | --- |
| 1 | Converted `neurips_2026.tex` to `Report.md` by hand, word for word. A `%` in the middle of an Introduction sentence comments out "our approach does not involve training a model.", so the compiled sentence reads "In contrast to automatic captioning methods [...], wordalisation aim to generate text directly from data"; the report follows the compiled text. Typos in the source are kept: "Amandine M.Caut" and "David J.T.Sumpter" (no space), "our method are based", "in come cases", "the model generate", "wordalisation aim", "and $18 \%$", "statistical vastly texts outperformed the statistical text", "texts form the wordalisation prompt", "wordalistations", "generate according to", "such that categorical variables", "The examples presented is". The duplicated affiliation (Uppsala, "Department" and "department") is kept as written. | `Report.md` |
| 2 | Layout decisions that change no words: Figure 1 and Figure 2 as panels (a), (b) as in the LaTeX subfigures; references to sub-figures print "1a"/"1b" as LaTeX does; the paper's own "Fig." and "Section" kept beside the numbers; "Figure\ref{…}" without a space kept as "Figure1b". The 1.4 cm the LaTeX trims from the top of `accuracy_plot.png` is blank margin, so the image is used untrimmed. The z-score equation is unnumbered, as in the paper. Table 1's caption sits above the table, which is the format's convention. Citations are author–date instead of numbered (unsrt). | `Report.md` |
| 3 | Found while converting, and left as they are: the text says "Figure 1b gives examples of visualisations and corresponding wordalisation for each application area", which probably means Figure 2; Figure 2 and Table 1 are never referred to in the text; the footnoted links are anonymised review links (anonymous.4open.science). | — |
| 4 | References: 49 cited keys, all found in `reference_nature.bib`. Converted by `Code/bib_to_yaml.py` with their words unchanged. 25 had no doi or url, which the format requires. Four carry their arXiv number in the venue field, which gives the link. 15 were matched on Crossref by exact title. Two Crossref matches were rejected as different works: a review of Cairo's book, and a 2026 reprint of Brown et al. The other six were checked by hand: NeurIPS proceedings pages (Brown, Lewis), the OpenAI PDF (Radford), Peachpit (Cairo), Open Library ISBN 9781803248226 (Richards; Packt and O'Reilly block scripts), and the OpenReview API (Vendrow, exact workshop title; the later arXiv version has a different title). Jia et al. and Crawford were matched on Crossref under shorter registered titles ("Visual Prompt Tuning", "Atlas of AI"). Every DOI was confirmed registered through the doi.org handle API; publisher pages answering 403 or 202 are bot blocks. `context_engineering`: BibTeX author "Langchain Blog" kept as a publication name, and its missing year shown as "n.d.". BibTeX "and others" is shown as "et al.". None of the 49 works was opened and read for this conversion; the reference details are the authors'. | `references.yaml` |
| 5 | Checked the built page against the LaTeX with `Code/check_against_source.py`: 4 986 words on each side, 0 differences, footnote links identical. A one-word change to a copy of the report was caught. The normative-model text, the wordalisation and both prompts are also checked by the build against `neurips_2026.tex`. | `build/representing-data-in-words/` |
| 6 | *Superseded by row 7.* Open for the authors: the licence for the page (front matter), whether and how agentic AI was used in writing the paper (Disclaimer), a report number, and whether to replace the anonymous review links before publication. Each is marked `[CHECK]` or empty, and the release build refuses to publish until they are resolved. | `Report.md` |
| 7 | David's decisions, 10 October 2026: "No licence page. Remove the disclaimer. Call it report 0001. Use real links. And correct all typos." Licence removed from the front matter; the page now states no licence (the build was changed so a licence is optional). Disclaimer section removed, with `disclaimer: false` in the front matter; the contract still requires one in every other report. Report number `0001`. The two anonymised links replaced by the public repository `BeimnetGirma/wordalisations`, identified because the anonymised repository has expired: it holds the three applications, the evaluation pipeline (`evaluation/`, including `human-evaluation`) and `prompt cards/prompt-cards.md`, the index of the three prompt cards; both links answer 200. | `Report.md` |
| 8 | Typos corrected, at David's request. In the text, 36 corrections, each listed before and after in `CORRECTIONS` in `Code/check_against_source.py`, which applies them to the LaTeX and confirms they are the only differences (4 992 words on each side, 0 differences). Among them, two that change meaning rather than spelling: "the wordalisation and statistical vastly texts outperformed the statistical text" now reads "…texts vastly outperformed the control text", since a text cannot outperform itself; and "He was average in [smart passes]" in the Figure 1b synthetic text now has the brackets the other phrases have, so that box is no longer checked against the LaTeX by the build. In the author block: "Amandine M. Caut", "David J. T. Sumpter", "INSA Toulouse", and the two Uppsala affiliations ("Department"/"department") merged into one. In the references, via `OVERRIDES` and `NAME_FIXES` in `Code/bib_to_yaml.py`: BibTeX's lost capitals (NLP, LLM, NeurIPS, LangChain, journal and proceedings names, "Roles"), "Daumé III, Hal", "Xu, Zhanchao", "van Haften, Nanette", and addresses removed from publishers. Not changed: the two prompts in Section 3, which quote prompts as used. | `Report.md`, `references.yaml` |
| 9 | *Resolved in row 10.* Raised with David, not changed: "Figure 1b gives examples of visualisations and corresponding wordalisations for each application area" probably means Figure 2, which is otherwise never referred to; "$\chi^2=40.50$ for engagement" sits where usefulness is being reported, and engagement is reported in the next sentence; 42 + 40 + 40 texts is 122, but the text reports 121 responses. | — |
| 10 | David confirmed all three, 10 October 2026 ("Yes. yes. 122."): the sentence on examples of visualisations now refers to Figure 2 (`@fig-data-visualisation`), "$\\chi^2=40.50$ for engagement" now reads "for usefulness", and the human evaluation has 122 responses. The two text changes are in `CORRECTIONS`; the figure number is a cross-reference, which the check leaves out. | `Report.md` |
| 11 | The workspace moved to one paper per folder (12 October 2026). Everything for this paper is now in `papers/0002-representing-data-in-words/`; `Report.md` stays at the top of the workspace while the paper is open and names this folder in its front matter (`folder:`). Paths inside the report did not change, since they were already relative to the paper's material. The content hash changed once, because of the added `folder:` line; no review round was open. Rebuilt and re-checked: 0 errors, 4 992 words on each side, 0 differences. | this folder |
| 12 | At David's request, 12 October 2026: Matthias Green's affiliation is now Twelve Football (shared with Ágúst Pálmason, so the two affiliations merge into one) and his email matthias@twelve.football, in place of INSA Toulouse and mgreen@insa-toulouse.fr. The author block is not covered by `check_against_source.py`; the text is unchanged. | `Report.md` |
| 13 | At David's request, 12 October 2026: affiliation 1 (David J. T. Sumpter and Amandine M. Caut) is now "Department of Information Technology, Uppsala University, Box 524, 751 20 Uppsala, Sweden", in place of "Information Technology Department, Uppsala University". | `Report.md` |

## Code Summary

| Script | What it does | Run |
| --- | --- | --- |
| `Code/bib_to_yaml.py` | Writes this paper's `references.yaml` from the keys cited in `neurips_2026.tex` and their entries in `reference_nature.bib`, adding the verified links in its `LINKS` table and the corrections in `OVERRIDES` and `NAME_FIXES`. `--list` shows the parsed entries without writing. | From the workspace's `Code/`: `uv run python ../papers/0002-representing-data-in-words/Code/bib_to_yaml.py` |
| `Code/check_against_source.py` | Compares the words of the built page with the words of the LaTeX source, in order, after applying the listed `CORRECTIONS`, and exits 1 on any other difference. Citations, cross-reference numbers and the format's labels are removed from both sides first. | From the workspace's `Code/`: `uv run python tools/build.py && uv run python ../papers/0002-representing-data-in-words/Code/check_against_source.py` |

## References

*Sources behind the material, as distinct from the works the report cites.*
