# Linux Command Library

Curated command references grouped by topic, focusing on practical usage, flags, and gotchas for daily administration tasks.

[⬅ Back to Main Index](../README.md)

## How This Section Is Organized

- Each topic file (e.g., `filesystem.md`, `networking.md`) contains multiple `## Command: <name>` entries sorted alphabetically.
- Entries include a summary, distro applicability, fenced `bash` examples, and any tips or troubleshooting notes.
- When content overlaps multiple categories, choose the best-fit file and add cross-links only if absolutely necessary.

## Topic Files

| File | Focus |
|------|-------|
| [`filesystem.md`](filesystem.md) | Disks, partitioning, mounts, quotas. |
| [`networking.md`](networking.md) | Interfaces, routing, diagnostics, VPN tooling. |
| [`processes-and-services.md`](processes-and-services.md) | Process inspection, systemd/service helpers. |
| [`packages-and-repos.md`](packages-and-repos.md) | Package managers, repositories, build/install helpers. |
| [`users-and-permissions.md`](users-and-permissions.md) | Accounts, groups, sudo, ACLs, SELinux helpers. |
| [`misc.md`](misc.md) | Commands that do not neatly fit other categories. |

## Adding New Content

1. Identify the best topic file and ensure it exists (create it using the style guide template if needed).
2. Insert a new `## Command:` block with alphabetic ordering.
3. Include at least one worked example; add tips for errors or distro quirks.
4. Link back to troubleshooting pages if the command is part of a larger fix.
