# Miscellaneous Command References

Handy commands that do not warrant their own topical bucket but are still regular fixtures in day-to-day ops work.

[⬅ Back to Main Index](README.md)

## Command: dmidecode

**Category:** Hardware info  
**Distros:** All  
**Summary:** Dumps SMBIOS data to reveal chassis make/model, serial numbers, and BIOS versions.

### Common usages

```bash
sudo dmidecode -t system            # Quick summary of vendor, product, serial, BIOS
sudo dmidecode -t memory            # Inspect DIMM population and speeds
```

### Tips & troubleshooting

- Requires root because it queries `/dev/mem`; run in change windows if production policies restrict it.
- Redirect output to a ticket for future audits (`sudo dmidecode -t system > /tmp/hw.txt`).

## Command: gh

**Category:** Developer tooling  
**Distros:** All  
**Summary:** GitHub CLI used to authenticate, create repos, and push existing projects without opening a browser.

### Common usages

```bash
sudo apt install gh git                      # Install requirements on Ubuntu/Debian
gh auth login                                # Interactive device or SSH auth
gh repo create --source=. --public --push    # Publish current repo and push with remote origin
```

### Tips & troubleshooting

- Run `git init && git add . && git commit -m "Initial commit"` before `gh repo create --source=. --push`.
- Use `gh repo create --private` (or `--public`) explicitly to avoid interactive prompts in scripts.
- Follow up with the standard flow: `git status`, `git add`, `git commit -m "...`, `git push -u <branch>` for ongoing work.

## Command: grep (PCRE)

**Category:** Text processing  
**Distros:** All (requires GNU grep with PCRE support)  
**Summary:** Uses the `-P` (PCRE) and `\K` features to drop the matched prefix and output only the desired suffix.

### Common usages

```bash
grep -oP 'pattern\K.*' file.txt        # Print everything after 'pattern' on each matching line
grep -oP '(?<=pattern).*' file.txt     # Equivalent when your grep supports lookbehind
```

### Tips & troubleshooting

- `\K` is faster than variable-length lookbehind and works even when lookbehind is unsupported.
- Validate your grep build (`grep --version`) because BusyBox and macOS/BSD `grep` lack `-P`.

## Command: lsb_release

**Category:** System info  
**Distros:** Debian/Ubuntu family  
**Summary:** Reports the distribution release name, description, and codename via the LSB database.

### Common usages

```bash
lsb_release -a           # Show distributor ID, description, release, codename
lsb_release -cs          # Output only the codename (useful for apt sources)
```

### Tips & troubleshooting

- Install `lsb-release` package if the utility is missing.
- Use in scripts to branch logic for `jammy`, `focal`, etc.
