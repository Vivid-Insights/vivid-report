# Agents, models, instructions and dates

All runs happened on **2026-11-09** in Claude Code (VS Code extension, Windows 11), operated from
`K:\Vivid\Afya\Storyboard-Generator`, with the target project at `K:\Vivid\school_bot`.

## 1. Storyboard Generator (operator)

- **What:** the main Claude Code session, following `K:\Vivid\school_bot\CLAUDE.md` (a copy of the
  Storyboard Generator's converser instructions; its SHA-256 matches the tool's own `CLAUDE.md`,
  `ADA5762E…A406B1`).
- **Model:** Claude Opus 5.5 (`claude-opus-5-5`).
- **Tool path (`$TOOL_PATH`):** `K:\Vivid\Afya\Storyboard-Generator` (renderer `bin/render.py`,
  schema `schema/storyboard.schema.json`).
- **Instruction from the human (Sena), verbatim summary:** build a school chatbot through the
  storyboard, acting as both the generator and (via a subagent) the chatbot builder answering the
  questions; log every interaction; include areas such as "Processes" (registration, dropping
  courses, etc.); scope left to the operator. Sena then chose: fresh Claude subagent for the build,
  and **high school instead of college**.
- **Deviation from the normal flow:** every question the instructions say to ask "the person" via
  AskUserQuestion was instead sent to the builder subagent as a message, with the same option list
  (and previews for AF1). The subagent's reply is the answer of record.

## 2. Chatbot builder (answers the storyboard's questions)

- **Spawned:** 2026-11-09 ~03:52, Agent tool, `subagent_type: general-purpose`.
- **Model:** Claude Opus 5.5 (`claude-opus-5-5`), inherited from the operator session.
- **Persona:** "Jordan Hale", Data & Systems Coordinator at the fictional Ashbourne High School.
- **Its only context:** `builder-brief.md`. It was told not to read any other file, including the
  generator's `CLAUDE.md`, so it can't anticipate the questions.
- **Instruction, verbatim:** `builder-instruction.md`. Every later round was sent to the same agent
  as a follow-up message (so it kept its earlier answers in context) and is stored verbatim in
  `rounds/round-NN-question.md`, with its reply in `rounds/round-NN-answer.md`.

## 3. Build agent (builds the chatbot from the storyboard)

- **Spawned:** 2026-11-09 ~04:40, Agent tool, `subagent_type: general-purpose`, a **fresh** agent
  with no access to the storyboard session.
- **Model:** Claude Opus 5.5 (`claude-opus-5-5`), inherited.
- **Inputs allowed:** only `storyboard.json` (v3) and `data/few_shot_examples.csv`. It was
  explicitly forbidden from reading `log/`, `CLAUDE.md`, the config and the generator tool.
- **Output:** `K:\Vivid\school_bot\app\`, including `BUILD_NOTES.md` (its own record of every
  guess and gap).
- **Instruction, verbatim:** `build-agent-instruction.md`.
- **Why a fresh agent:** so the build shows what the storyboard *alone* communicates. The
  builder subagent knows the intent behind each answer, so it would silently fill gaps.
