# Regular Expressions Cheatsheet

Quick reference for regex patterns used with grep, sed, awk, and other tools.

[⬅ Back to Main Index](README.md)

## Topic: Basic Metacharacters

| Pattern | Description |
|---------|-------------|
| `.` | Any single character (except newline) |
| `^` | Start of line |
| `$` | End of line |
| `*` | Zero or more of previous |
| `+` | One or more of previous (extended) |
| `?` | Zero or one of previous (extended) |
| `\` | Escape metacharacter |
| `\|` | Alternation (OR) |
| `()` | Grouping |
| `[]` | Character class |

Basic regex (grep, sed) requires `\+`, `\?`, `\|`, `\(\)`.
Extended regex (grep -E, sed -E, awk) uses `+`, `?`, `|`, `()`.

## Topic: Character Classes

| Pattern | Description |
|---------|-------------|
| `[abc]` | a, b, or c |
| `[^abc]` | Not a, b, or c |
| `[a-z]` | Lowercase letters |
| `[A-Z]` | Uppercase letters |
| `[0-9]` | Digits |
| `[a-zA-Z0-9]` | Alphanumeric |

## Topic: POSIX Character Classes

Use inside brackets: `[[:alpha:]]`

| Class | Description |
|-------|-------------|
| `[:alpha:]` | Letters |
| `[:digit:]` | Digits |
| `[:alnum:]` | Alphanumeric |
| `[:space:]` | Whitespace |
| `[:upper:]` | Uppercase |
| `[:lower:]` | Lowercase |
| `[:punct:]` | Punctuation |

## Topic: Quantifiers

| Pattern | Description |
|---------|-------------|
| `*` | Zero or more |
| `+` | One or more |
| `?` | Zero or one |
| `{n}` | Exactly n |
| `{n,}` | n or more |
| `{n,m}` | Between n and m |

Basic regex: `\{n,m\}`, `\+`, `\?`

## Topic: Anchors and Boundaries

| Pattern | Description |
|---------|-------------|
| `^` | Start of line |
| `$` | End of line |
| `\b` | Word boundary |
| `\B` | Not word boundary |
| `\<` | Start of word |
| `\>` | End of word |

`grep '\bword\b'` matches "word" but not "password".

## Topic: Shorthand Classes (Perl/PCRE)

Use with `grep -P` or languages like Python.

| Pattern | Description |
|---------|-------------|
| `\d` | Digit `[0-9]` |
| `\D` | Non-digit `[^0-9]` |
| `\w` | Word character `[a-zA-Z0-9_]` |
| `\W` | Non-word character |
| `\s` | Whitespace |
| `\S` | Non-whitespace |

## Topic: Groups and Backreferences

| Pattern | Description |
|---------|-------------|
| `(pattern)` | Capture group |
| `\1`, `\2` | Backreference to group 1, 2 |

```bash
# Find repeated words
grep -E '\b(\w+)\s+\1\b' file

# sed replacement with groups
echo "hello world" | sed 's/\(hello\) \(world\)/\2 \1/'
# Output: world hello
```

## Topic: Common Patterns

| Pattern | Matches |
|---------|---------|
| `^$` | Empty line |
| `^\s*$` | Blank line (whitespace only) |
| `^#` | Comment lines |
| `^[^#]` | Non-comment lines |
| `[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}` | IPv4 (basic) |
| `[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}` | Email (basic) |
| `https?://[^\s]+` | URL (basic) |

## Topic: Tool Usage

**grep:**

```bash
grep 'pattern' file              # Basic regex
grep -E 'pattern' file           # Extended regex
grep -P 'pattern' file           # Perl regex (PCRE)
grep -i 'pattern' file           # Case insensitive
grep -v 'pattern' file           # Invert match
grep -o 'pattern' file           # Only matching part
```

**sed:**

```bash
sed 's/old/new/' file            # Basic regex
sed -E 's/old/new/' file         # Extended regex
sed 's/old/new/g' file           # Global replace
sed -n '/pattern/p' file         # Print matches
```

**awk:**

```bash
awk '/pattern/' file             # Print matching lines
awk '/pattern/ {print $1}' file  # Field 1 of matches
awk '$1 ~ /pattern/' file        # Field 1 matches pattern
```

## Topic: Examples

```bash
# Find lines with IP addresses
grep -E '[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}' file

# Find lines starting with date (2024-01-15)
grep -E '^[0-9]{4}-[0-9]{2}-[0-9]{2}' file

# Remove blank lines
sed '/^[[:space:]]*$/d' file

# Extract email addresses
grep -oE '[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}' file

# Match error OR warning OR fail
grep -E 'error|warning|fail' file

# Case-insensitive word boundary
grep -iE '\berror\b' file
```
