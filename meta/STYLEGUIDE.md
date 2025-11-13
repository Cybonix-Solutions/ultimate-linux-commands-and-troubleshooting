# Ultimate Linux Documentation Style Guide

This guide defines how to turn the raw notes in `data/_raw/` into consistent, searchable Markdown pages across the repository.

## Voice & Editorial Rules

- Keep explanations short, direct, and distro-agnostic unless a scenario is clearly platform-specific (call that out with **Distros:**).
- Favor imperative language for steps (`Run`, `Verify`, `If it fails...`), and prefer present tense for descriptions.
- Capture exact error strings or quirky behaviors verbatim; they help searchability.
- Use plain ASCII, wrap lines at ~100 characters when possible, and avoid trailing whitespace.

## Shared Formatting Conventions

- Every content page starts with a single `#` H1 title followed by a one-sentence summary paragraph.
- Immediately after the summary, include a backlink to the relevant index using `[⬅ Back to Main Index](../README.md)` (adjust path as needed).
- Use H2/H3 headings to break down topics; do not skip heading levels.
- Fenced code blocks must declare a language (usually `bash`).
- List command flags inline (`\`--long-flag\``) and prefer tables only when they improve clarity.
- Link to upstream documentation or man pages when it materially helps.

## Command Pages (`commands/*.md`)

Add one section per command following this template:

````markdown
## Command: <name>

**Category:** <filesystems | networking | etc.>  
**Distros:** <All | Ubuntu | RHEL | ...>  
**Summary:** Single sentence describing what the command solves.

### Common usages

```bash
<command example #1>
<command example #2>
```

### Tips & troubleshooting

- Bullet key behaviors, gotchas, or follow-up commands.
- Quote error strings exactly when referencing them.
````

Order commands alphabetically inside each file. If a command fits multiple categories, pick the best home and cross-link elsewhere if truly necessary.

## Troubleshooting Pages (`troubleshooting/*.md`)

Organize by scenario:

````markdown
## Scenario: <problem statement>

**Symptoms:** Bullet concrete observations or error text.  
**Applies to:** Distros, services, or environments.

### Investigation
1. Step-by-step checks with `bash` blocks for commands.
2. Note expected vs. abnormal output.

### Resolution
- Final fix, config changes, or escalation notes.
````

Include escalation or rollback instructions when relevant.

## Cheatsheets (`cheatsheets/*.md`)

Structure entries as concise reference tables or bullet blocks:

````markdown
## Topic: <focus area>

| Shortcut | Description |
|----------|-------------|
| `tmux-prefix + c` | Create a window |
````

Keep items terse; link to deeper docs when needed.

## Working With Raw Notes

1. Read a single file from `data/_raw/`.
2. Decide whether the content belongs in commands, troubleshooting, cheatsheets, or multiple destinations.
3. Integrate the cleaned content into the target Markdown file(s) following the templates above.
4. Move the processed raw file into `data/processed/`.
5. Optionally record a short summary in `meta/AGENT_NOTES.md` (what file, where content went).

## File Hygiene

- Run spellcheck (or re-read) before saving; typos make searching harder.
- Never delete user-provided sections without replacing them.
- When adding TODOs or callouts, prefer `> **Note:** ...` blocks and explain why the note exists.

By following this guide, every contribution stays uniform and easy to search.
