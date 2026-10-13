---
reviewer: {{reviewer}}
round: {{round}}
hash: {{hash}}
date: {{date}}
recommendation:          # accept | minor | major | reject
---

# Review by {{name}}, round {{round}}

I read the review copy of version `{{hash}}` (the first characters are in the banner at the top of the page). If the version you read is different, stop and tell the author.

## Summary

In two or three sentences: what the report claims, and whether it shows it.

## Checklist

Mark each `yes`, `no` or `n/a`, and explain every `no` under Comments. REVIEW.md says what each means.

- [ ] The report has the standard structure, and its three points run in the same order from the abstract through the Introduction (at least 20 works cited) to the Discussion, where each is answered.
- [ ] Every claim about the method is true of the code, and every number traces to a saved output.
- [ ] Every generated text, prompt and conversation is quoted from a file; hand-written examples are labelled; the model's errors are reported.
- [ ] The normative choices are named, with their alternatives.
- [ ] Any claim that the method works rests on a stated procedure, and the report says what it cannot show.
- [ ] Other people's methods are credited; client and partner material is published with permission; nothing personal, confidential or licensed is exposed.
- [ ] The references say what the report says they say, and the links resolve.
- [ ] The writing follows WRITING.md closely enough that nothing obscures the argument.
- [ ] The page works: figures in both themes, videos, interactives, a phone-width window, print preview.
- [ ] The disclaimer is present.

## Comments

Number each point so the author can answer it. Give the section, figure or quoted sentence it is about, say what is wrong, and say whether it must be fixed before you accept.

1.

## Recommendation

Set `recommendation:` above. `accept` means you would put Vivid Insights' name to this version as it stands. Then approve it with `cd Code && uv run python tools/review.py approve {{reviewer}}`, and commit both files yourself.
