# Bash Cheatsheet Expansion - Suggested Addition

**Target:** cheatsheets/bash-shortcuts.md (expand existing)
**Priority:** High (current coverage is minimal)

---

## Topic: Readline Keyboard Shortcuts

Essential shortcuts for command-line editing (work in bash, zsh, and most readline apps).

| Shortcut | Description |
|----------|-------------|
| `Ctrl+A` | Move cursor to beginning of line |
| `Ctrl+E` | Move cursor to end of line |
| `Ctrl+B` | Move back one character |
| `Ctrl+F` | Move forward one character |
| `Alt+B` | Move back one word |
| `Alt+F` | Move forward one word |
| `Ctrl+U` | Cut from cursor to beginning of line |
| `Ctrl+K` | Cut from cursor to end of line |
| `Ctrl+W` | Cut word before cursor |
| `Alt+D` | Cut word after cursor |
| `Ctrl+Y` | Paste (yank) last cut text |
| `Ctrl+L` | Clear screen (keep current line) |
| `Ctrl+R` | Reverse search history |
| `Ctrl+S` | Forward search history (may need `stty -ixon`) |
| `Ctrl+G` | Cancel search/escape |
| `Ctrl+C` | Cancel current command |
| `Ctrl+D` | Delete character / EOF (exit shell if empty) |
| `Ctrl+_` | Undo last edit |
| `Alt+.` | Insert last argument from previous command |
| `Ctrl+X Ctrl+E` | Open command in $EDITOR |

---

## Topic: History Expansion

Quickly reference and modify previous commands.

| Syntax | Description |
|--------|-------------|
| `!!` | Last command |
| `!$` | Last argument of previous command |
| `!^` | First argument of previous command |
| `!*` | All arguments of previous command |
| `!n` | Command number n from history |
| `!-n` | nth previous command |
| `!string` | Most recent command starting with "string" |
| `!?string` | Most recent command containing "string" |
| `^old^new` | Replace "old" with "new" in last command |
| `!!:s/old/new` | Same as above |
| `!$:h` | Last arg, remove filename (head = dirname) |
| `!$:t` | Last arg, remove directory (tail = filename) |
| `!$:r` | Last arg, remove extension |
| `!$:e` | Last arg, keep only extension |

**Examples:**
```bash
$ cat /var/log/syslog
$ less !$              # less /var/log/syslog
$ vim !$:h/auth.log    # vim /var/log/auth.log

$ mkdir -p /path/to/new/dir
$ cd !$                # cd /path/to/new/dir

$ ./configure && make && sudo make install
$ sudo !!              # sudo ./configure... (repeat with sudo)
```

---

## Topic: Parameter Expansion

Powerful variable manipulation inside `${...}`.

| Syntax | Description |
|--------|-------------|
| `${var:-default}` | Use default if var is unset/empty |
| `${var:=default}` | Set and use default if var is unset/empty |
| `${var:+alternate}` | Use alternate if var IS set |
| `${var:?error msg}` | Exit with error if var is unset |
| `${#var}` | Length of string |
| `${var#pattern}` | Remove shortest prefix match |
| `${var##pattern}` | Remove longest prefix match |
| `${var%pattern}` | Remove shortest suffix match |
| `${var%%pattern}` | Remove longest suffix match |
| `${var/old/new}` | Replace first occurrence |
| `${var//old/new}` | Replace all occurrences |
| `${var^}` | Uppercase first character |
| `${var^^}` | Uppercase all |
| `${var,}` | Lowercase first character |
| `${var,,}` | Lowercase all |
| `${var:offset:length}` | Substring |

**Examples:**
```bash
file="/path/to/script.sh"
echo ${file##*/}      # script.sh (basename)
echo ${file%/*}       # /path/to (dirname)
echo ${file%.sh}      # /path/to/script (remove extension)
echo ${file##*.}      # sh (get extension)

name="john"
echo ${name^}         # John
echo ${name^^}        # JOHN
```

---

## Topic: Brace Expansion

Generate sequences and combinations.

| Syntax | Description |
|--------|-------------|
| `{a,b,c}` | Comma list |
| `{1..10}` | Numeric range |
| `{a..z}` | Alphabetic range |
| `{01..10}` | Zero-padded range |
| `{1..10..2}` | Range with step |
| `pre{a,b}post` | Combine with strings |

**Examples:**
```bash
mkdir -p project/{src,lib,bin,docs}
touch file{1..5}.txt
cp config.yml{,.bak}                    # config.yml → config.yml.bak
mv photo.{jpg,png}                      # rename jpg to png
echo {A..Z}{0..9}                       # A0 A1 ... Z9
```

---

## Topic: Process Substitution

Use command output as a file.

| Syntax | Description |
|--------|-------------|
| `<(command)` | Command output as readable file |
| `>(command)` | Writable file that pipes to command |

**Examples:**
```bash
# Compare two command outputs
diff <(ls dir1) <(ls dir2)

# Process sorted output
join <(sort file1) <(sort file2)

# Tee to multiple commands
command | tee >(gzip > out.gz) >(wc -l)
```

---

## Topic: Conditionals and Tests

Test expressions in scripts.

| Test | Description |
|------|-------------|
| `-f file` | File exists and is regular file |
| `-d file` | Directory exists |
| `-e file` | File exists (any type) |
| `-r file` | File is readable |
| `-w file` | File is writable |
| `-x file` | File is executable |
| `-s file` | File exists and is not empty |
| `-z string` | String is empty |
| `-n string` | String is not empty |
| `str1 = str2` | Strings are equal |
| `str1 != str2` | Strings are not equal |
| `n1 -eq n2` | Numbers are equal |
| `n1 -ne n2` | Numbers are not equal |
| `n1 -lt n2` | n1 less than n2 |
| `n1 -gt n2` | n1 greater than n2 |

**Examples:**
```bash
[[ -f "$file" ]] && echo "exists"
[[ -z "$var" ]] && var="default"
[[ "$str" == *pattern* ]] && echo "matches"  # glob in [[
[[ "$str" =~ ^[0-9]+$ ]] && echo "is number" # regex in [[
```

---

## Topic: Useful One-Liners

Quick recipes for common tasks.

```bash
# Find and replace in multiple files
find . -name "*.py" -exec sed -i 's/old/new/g' {} +

# Count lines of code
find . -name "*.py" | xargs wc -l

# Watch command output
watch -n 1 'command'

# Parallel execution
cat hosts.txt | xargs -P 4 -I {} ssh {} 'uptime'

# Loop over files safely (handles spaces)
while IFS= read -r -d '' file; do
  echo "$file"
done < <(find . -name "*.txt" -print0)

# Quick HTTP server
python3 -m http.server 8080

# Generate random password
openssl rand -base64 24

# Date math
date -d "yesterday"
date -d "+7 days"
date -d "next monday"
```
