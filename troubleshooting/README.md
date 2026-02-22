# Troubleshooting Runbooks

Step-by-step investigations and fixes for recurring Linux issues, from boot failures to storage headaches.

[⬅ Back to Main Index](../README.md)

## Structure

- Each topic file collects multiple `## Scenario:` sections, each dedicated to a specific failure pattern or error string.
- Sections document symptoms, investigation steps, resolution, and any rollback or escalation guidance.
- Include distro or environment qualifiers near the top when a fix is not universal.

## Topic Files

| File | Focus |
|------|-------|
| [`logging.md`](logging.md) | Runaway syslog, rsyslog issues, log management. |
| [`storage-and-raid.md`](storage-and-raid.md) | Disk health, RAID rebuilds, filesystem errors. |
| [`security-and-selinux.md`](security-and-selinux.md) | Root password resets, SELinux AVCs, auth failures. |
| [`misc.md`](misc.md) | Edge cases that do not fit other categories. |

## Authoring Checklist

1. Capture exact error messages under **Symptoms** for easier searching.
2. Provide numbered investigation steps with expected vs. problematic output.
3. Offer at least one actionable resolution or mitigation; mention log locations touched.
4. Link to related command entries or cheatsheets when they give additional context.
