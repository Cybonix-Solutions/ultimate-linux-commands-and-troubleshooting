# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Repository Does

Transforms raw Linux/Unix notes into clean, searchable documentation. Raw notes live in `data/_raw/` and get processed into three destination types:

- **commands/** - Command references grouped by topic (filesystem, networking, etc.)
- **troubleshooting/** - Scenario-driven runbooks for diagnosing and fixing issues
- **cheatsheets/** - Quick reference tables for shortcuts and high-frequency tasks

## The Documentation Workflow

1. Open a file from `data/_raw/`
2. Determine destination(s): commands, troubleshooting, or cheatsheets
3. Apply the templates below (from `meta/STYLEGUIDE.md`)
4. Move the processed file to `data/processed/`
5. Log a brief summary in `meta/AGENT_NOTES.md`

## Content Templates

### Command Entry (for `commands/*.md`)

```markdown
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
```

Commands are ordered **alphabetically** within each file.

### Troubleshooting Entry (for `troubleshooting/*.md`)

```markdown
## Scenario: <problem statement>

**Symptoms:** Bullet concrete observations or error text.
**Applies to:** Distros, services, or environments.

### Investigation
1. Step-by-step checks with bash blocks for commands.
2. Note expected vs. abnormal output.

### Resolution
- Final fix, config changes, or escalation notes.
```

### Cheatsheet Entry (for `cheatsheets/*.md`)

```markdown
## Topic: <focus area>

| Shortcut | Description |
|----------|-------------|
| `command` | What it does |
```

Keep entries terse; use tables or bullet blocks.

## Formatting Rules

- Every content page starts with `#` H1 title + one-sentence summary + backlink: `[⬅ Back to Main Index](../README.md)`
- Fenced code blocks must declare language (usually `bash`)
- Keep distro-agnostic unless specific—mark exceptions with **Distros:** field
- Capture exact error strings verbatim (improves searchability)
- Wrap lines at ~100 characters, use plain ASCII

## Search

```bash
./search <keyword>              # CLI search across commands, cheatsheets, troubleshooting
python3 meta/generate_index.py  # Regenerate search index after adding content
```

Web interface at `site/index.html` (reads from `site/search_index.json`). The index is auto-regenerated on push to main via GitHub Actions.
