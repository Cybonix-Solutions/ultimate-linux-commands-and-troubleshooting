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
| [`firewall.md`](firewall.md) | firewalld (RHEL), ufw (Ubuntu), iptables, nftables. |
| [`networking.md`](networking.md) | Interfaces, routing, DNS, diagnostics, VPN tooling. |
| [`packages-and-repos.md`](packages-and-repos.md) | apt, dnf, dpkg, rpm, snap, flatpak, repos. |
| [`processes-and-services.md`](processes-and-services.md) | systemctl, journalctl, process inspection, debugging. |
| [`text-processing.md`](text-processing.md) | sed, awk, cut, tr, sort, uniq, grep patterns. |
| [`users-and-permissions.md`](users-and-permissions.md) | Accounts, groups, sudo, ACLs, SELinux helpers. |
| [`misc.md`](misc.md) | System info, hardware, environment, and misc tools. |

## Adding New Content

1. Identify the best topic file and ensure it exists (create it using the style guide template if needed).
2. Insert a new `## Command:` block with alphabetic ordering.
3. Include at least one worked example; add tips for errors or distro quirks.
4. Link back to troubleshooting pages if the command is part of a larger fix.
