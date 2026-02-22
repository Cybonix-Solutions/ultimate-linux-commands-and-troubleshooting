# Regular Expressions Cheatsheet - Suggested Addition

**Target:** cheatsheets/regex-cheatsheet.md (new file)
**Priority:** Medium (essential for grep, sed, awk usage)

---

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

**Note:** Basic regex (grep, sed) requires `\+`, `\?`, `\|`, `\(\)`. Extended regex (grep -E, sed -E, awk) uses `+`, `?`, `|`, `()`.

---

## Topic: Character Classes

| Pattern | Description |
|---------|-------------|
| `[abc]` | a, b, or c |
| `[^abc]` | Not a, b, or c |
| `[a-z]` | Lowercase letters |
| `[A-Z]` | Uppercase letters |
| `[0-9]` | Digits |
| `[a-zA-Z]` | All letters |
| `[a-zA-Z0-9]` | Alphanumeric |
| `[-abc]` | Dash must be first or last |
| `[]]` | Literal bracket |

---

## Topic: POSIX Character Classes

Use inside brackets: `[[:alpha:]]`

| Class | Description |
|-------|-------------|
| `[:alpha:]` | Letters |
| `[:digit:]` | Digits |
| `[:alnum:]` | Alphanumeric |
| `[:space:]` | Whitespace |
| `[:blank:]` | Space and tab |
| `[:upper:]` | Uppercase |
| `[:lower:]` | Lowercase |
| `[:punct:]` | Punctuation |
| `[:print:]` | Printable characters |
| `[:graph:]` | Printable (no space) |
| `[:cntrl:]` | Control characters |
| `[:xdigit:]` | Hexadecimal digits |

**Example:** `grep '[[:digit:]]' file`

---

## Topic: Quantifiers

| Pattern | Description |
|---------|-------------|
| `*` | Zero or more |
| `+` | One or more |
| `?` | Zero or one |
| `{n}` | Exactly n |
| `{n,}` | n or more |
| `{n,m}` | Between n and m |
| `{,m}` | Up to m |

**Basic regex escaping:** `\{n,m\}`, `\+`, `\?`

---

## Topic: Anchors and Boundaries

| Pattern | Description |
|---------|-------------|
| `^` | Start of line |
| `$` | End of line |
| `\b` | Word boundary |
| `\B` | Not word boundary |
| `\<` | Start of word |
| `\>` | End of word |

**Example:** `grep '\bword\b'` matches "word" but not "password"

---

## Topic: Shorthand Classes (Perl/PCRE)

Use with `grep -P` or languages like Python, JavaScript.

| Pattern | Description |
|---------|-------------|
| `\d` | Digit `[0-9]` |
| `\D` | Non-digit `[^0-9]` |
| `\w` | Word character `[a-zA-Z0-9_]` |
| `\W` | Non-word character |
| `\s` | Whitespace |
| `\S` | Non-whitespace |

---

## Topic: Groups and Backreferences

| Pattern | Description |
|---------|-------------|
| `(pattern)` | Capture group |
| `\1`, `\2` | Backreference to group 1, 2 |
| `(?:pattern)` | Non-capturing group (PCRE) |
| `(?=pattern)` | Positive lookahead (PCRE) |
| `(?!pattern)` | Negative lookahead (PCRE) |
| `(?<=pattern)` | Positive lookbehind (PCRE) |
| `(?<!pattern)` | Negative lookbehind (PCRE) |

**Example backreference:**
```bash
# Find repeated words
grep -E '\b(\w+)\s+\1\b' file

# sed replacement
echo "hello world" | sed 's/\(hello\) \(world\)/\2 \1/'
# output: world hello
```

---

## Topic: Common Patterns

| Pattern | Matches |
|---------|---------|
| `^$` | Empty line |
| `^\s*$` | Blank line (only whitespace) |
| `^#` | Comment lines |
| `^[^#]` | Non-comment lines |
| `\b[A-Z][a-z]*\b` | Capitalized word |
| `[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}` | IPv4 address (basic) |
| `[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}` | Email (basic) |
| `https?://[^\s]+` | URL (basic) |
| `^[[:space:]]*$` | Whitespace-only line |
| `[[:punct:]]` | Punctuation |
| `\b[0-9a-fA-F]+\b` | Hexadecimal |

---

## Topic: Tool-Specific Usage

**grep:**
```bash
grep 'pattern' file              # Basic regex
grep -E 'pattern' file           # Extended regex
grep -P 'pattern' file           # Perl regex (PCRE)
grep -i 'pattern' file           # Case insensitive
grep -v 'pattern' file           # Invert match
grep -o 'pattern' file           # Only matching part
grep -n 'pattern' file           # Show line numbers
```

**sed:**
```bash
sed 's/old/new/' file            # Basic regex
sed -E 's/old/new/' file         # Extended regex
sed 's/old/new/g' file           # Global replace
sed -n '/pattern/p' file         # Print matching lines
```

**awk:**
```bash
awk '/pattern/' file             # Print matching lines
awk '/pattern/ {print $1}' file  # Print field 1 of matches
awk '$1 ~ /pattern/' file        # Field 1 matches pattern
```

---

## Topic: Quick Examples

```bash
# Find lines with IP addresses
grep -E '[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}' file

# Find lines starting with date (2024-01-15)
grep -E '^[0-9]{4}-[0-9]{2}-[0-9]{2}' file

# Remove blank lines
sed '/^[[:space:]]*$/d' file

# Extract email addresses
grep -oE '[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}' file

# Find duplicate words
grep -E '\b(\w+)\s+\1\b' file

# Match either pattern
grep -E 'error|warning|fail' file

# Lines NOT containing pattern
grep -v 'DEBUG' file

# Case-insensitive word boundary
grep -iE '\berror\b' file

# Find lines with exactly 3 digits
grep -E '^[^0-9]*[0-9]{3}[^0-9]*$' file
```
