# Ultimate Linux Commands and Troubleshooting

A curated knowledge base that turns messy Linux notes into clean, searchable documentation for day-to-day administration and firefighting.

[Visit the commands index](commands/README.md) · [Visit the troubleshooting index](troubleshooting/README.md) · [Visit the cheatsheets index](cheatsheets/README.md)

## Repository Map

- `commands/` – task-focused command collections grouped by topic.
- `troubleshooting/` – scenario-driven runbooks for diagnosing and resolving issues.
- `cheatsheets/` – fast references for shortcuts, key combos, and high-frequency tasks.
- `data/_raw/` – unprocessed notes; each file gets cleaned and re-homed.
- `data/processed/` – archives of raw files that have been fully incorporated.
- `meta/` – style guide, contribution rules, TODOs, and agent notes.

## Documentation Workflow

1. Open a single raw file inside `data/_raw/`.
2. Decide which documentation file(s) should receive the cleaned content (commands, troubleshooting, cheatsheets).
3. Apply the templates defined in `meta/STYLEGUIDE.md` when adding material.
4. After integrating everything, move the raw file into `data/processed/` and optionally log the work inside `meta/AGENT_NOTES.md`.

## Contributing

- Follow the formatting requirements in `meta/STYLEGUIDE.md`.
- Check `meta/TODO.md` for outstanding tasks and `meta/CONTRIBUTING.md` for repo norms.
- Keep entries distro-agnostic unless the workaround is specific—call that out explicitly when needed.

Questions, ideas, or clarifications can live in `meta/AGENT_NOTES.md` so future contributors stay in sync.
