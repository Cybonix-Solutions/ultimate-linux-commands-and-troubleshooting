# Miscellaneous Command References

Handy commands that do not warrant their own topical bucket but are still regular fixtures in day-to-day ops work.

[⬅ Back to Main Index](README.md)

## Command: && (AND operator)

**Category:** Shell chaining  
**Distros:** All  
**Summary:** Runs the next command only if the previous one exited with status 0, making quick mini-pipelines safer.

### Common usages

```bash
cd /etc && ls                                  # List /etc only if cd succeeded
dnf makecache && dnf upgrade                   # Skip the upgrade whenever metadata sync fails
```

### Tips & troubleshooting

- Contrast with `;`, which runs subsequent commands regardless of failure.
- In complex scripts, combine with `set -e` or explicit `if` blocks for clearer error handling.

## Command: clear

**Category:** Terminal UX  
**Distros:** All  
**Summary:** Resets the terminal display by sending ANSI escape sequences to redraw a blank screen.

### Common usages

```bash
clear                                          # Wipe the current terminal contents
printf '\033c'                                 # Alternative when `clear` is unavailable
```

### Tips & troubleshooting

- Use `Ctrl+L` (readline shortcut) for the same effect inside Bash without forking a process.
- `TERM=dumb clear` falls back to printing newlines when terminfo data cannot be loaded.

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

## Command: echo

**Category:** Shell helpers  
**Distros:** All  
**Summary:** Writes strings or variable values to stdout or redirects them into files.

### Common usages

```bash
echo "Hello World"                               # Print a literal string
echo "Hello World" > data.txt                    # Overwrite a file with new content
```

### Tips & troubleshooting

- Prefer `printf` when you need consistent escape handling across shells.
- Use `echo "$VAR"` (quoted) so spaces and wildcard characters are not reinterpreted.

## Command: env

**Category:** Environment inspection  
**Distros:** All  
**Summary:** Prints the current environment variables or runs a command with a modified environment.

### Common usages

```bash
env | more                                      # Review all exported variables
FOO=bar env bash -c 'echo $FOO'                 # Run a command with a temporary value
```

### Tips & troubleshooting

- Pipe into `grep` to locate a single variable quickly (`env | grep ^PATH=`).
- Remember `env -i` starts from a clean slate—great for debugging scripts that depend on inherited state.

## Command: export

**Category:** Environment management  
**Distros:** All  
**Summary:** Creates or updates environment variables so that child processes inherit the value.

### Common usages

```bash
export WEB_PAGE="https://www.redhat.com/en"     # Set a variable for the current session
export PATH="$HOME/.local/bin:$PATH"            # Prepend a directory to PATH
```

### Tips & troubleshooting

- Put persistent exports inside `~/.bash_profile` (login shells) or `~/.bashrc` (interactive shells).
- Use `unset VAR` to remove a value entirely rather than exporting an empty string.

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

## Command: man

**Category:** Documentation  
**Distros:** All  
**Summary:** Displays on-system manual pages, providing canonical syntax and flag descriptions for commands.

### Common usages

```bash
man cp                                           # Read the manual for cp
man 5 passwd                                     # Open a specific manual section
```

### Tips & troubleshooting

- Use `/pattern` inside `man` to search within the page; `n` jumps to the next match.
- `man -k keyword` (equivalent to `apropos`) searches page descriptions when you are unsure of the command name.

## Command: printenv

**Category:** Environment inspection  
**Distros:** All  
**Summary:** Outputs the value of specified environment variables without the extra formatting `env` provides.

### Common usages

```bash
printenv HOSTNAME                                # Display a single variable
printenv | sort                                  # Alphabetize the whole environment dump
```

### Tips & troubleshooting

- In scripts, guard against unset variables (`printenv VAR || echo "Missing VAR"`) so pipelines do not fail silently.
- Combine with `xargs` to pass values into other commands (`printenv HOME | xargs ls`).

## Command: source

**Category:** Shell helpers  
**Distros:** All  
**Summary:** Executes a script in the current shell so any exported variables or functions persist.

### Common usages

```bash
source ./new_vars.sh                             # Load environment tweaks without spawning a subshell
. /etc/profile                                   # POSIX-compatible shorthand for sourcing
```

### Tips & troubleshooting

- Remember that syntax errors in the sourced file abort your current shell when `set -e` is active—test in a subshell first.
- Use absolute paths in login scripts to avoid sourcing the wrong file when `pwd` changes mid-script.

## Command: which

**Category:** Path lookup  
**Distros:** All  
**Summary:** Shows the full path of the executable that the shell would run, honoring `$PATH` order.

### Common usages

```bash
which clear                                      # Reveal where a command lives on disk
which -a python3                                 # Display every matching executable in PATH order
```

### Tips & troubleshooting

- Alias-heavy environments may mask binaries; run `command -v <cmd>` for a POSIX-defined alternative.
- On hashed Bash commands, `hash -r` clears the cache so `which` reflects freshly installed executables.
