# Text Processing Commands - Suggested Addition

**Target:** commands/text-processing.md (new file)
**Priority:** Critical (foundational skill, currently absent)

---

## sed

Stream editor for transforming text.

```bash
sed 's/old/new/' file              # Replace first occurrence per line
sed 's/old/new/g' file             # Replace all occurrences
sed -i 's/old/new/g' file          # Edit in-place
sed -i.bak 's/old/new/g' file      # In-place with backup
sed -n '5p' file                   # Print line 5 only
sed -n '5,10p' file                # Print lines 5-10
sed '5d' file                      # Delete line 5
sed '/pattern/d' file              # Delete matching lines
sed '/pattern/!d' file             # Keep only matching lines
sed 's/^/prefix/' file             # Add prefix to each line
sed 's/$/ suffix/' file            # Add suffix to each line
sed '1i\Header line' file          # Insert line at beginning
sed 's/[0-9]\+/(&)/g' file         # Wrap numbers in parens
sed -E 's/([a-z]+)/\U\1/' file     # Uppercase first word (extended regex)
```

**Tips:**
- Use `-E` for extended regex (groups with `()` instead of `\(\)`)
- `-i` behaves differently on macOS (requires `''` argument)
- Test without `-i` first, then add it

---

## awk

Pattern scanning and processing language.

```bash
awk '{print $1}' file              # Print first field
awk '{print $NF}' file             # Print last field
awk -F: '{print $1}' /etc/passwd   # Custom delimiter
awk '{print NR, $0}' file          # Add line numbers
awk 'NR==5' file                   # Print line 5
awk 'NR>=5 && NR<=10' file         # Print lines 5-10
awk '/pattern/' file               # Print matching lines (like grep)
awk '!/pattern/' file              # Print non-matching lines
awk '{sum+=$1} END {print sum}'    # Sum first column
awk '{print length, $0}' file      # Print line length
awk 'BEGIN {OFS=","} {print $1,$2}' # CSV output
awk -F, '{print $1,$3}' file.csv   # Parse CSV
awk '{gsub(/old/,"new"); print}'   # Replace in awk
awk 'NF' file                      # Remove blank lines
awk '!seen[$0]++' file             # Remove duplicate lines
```

**Tips:**
- `$0` = entire line, `$1` = first field, `NF` = number of fields, `NR` = line number
- Use `BEGIN{}` for header output, `END{}` for summary
- `awk` is Turing-complete; complex logic is possible

---

## cut

Extract sections from lines.

```bash
cut -d: -f1 /etc/passwd            # First field, colon delimiter
cut -d: -f1,3 /etc/passwd          # Fields 1 and 3
cut -d: -f1-3 /etc/passwd          # Fields 1 through 3
cut -c1-10 file                    # Characters 1-10
cut -c5- file                      # Character 5 to end
cut --complement -f2 file          # All fields except 2
```

**Tips:**
- Faster than awk for simple field extraction
- Default delimiter is TAB
- Cannot reorder fields (use awk for that)

---

## tr

Translate or delete characters.

```bash
tr 'a-z' 'A-Z' < file              # Lowercase to uppercase
tr 'A-Z' 'a-z' < file              # Uppercase to lowercase
tr -d '[:digit:]' < file           # Delete all digits
tr -d '\r' < file                  # Remove Windows line endings
tr -s ' ' < file                   # Squeeze repeated spaces
tr ' ' '\n' < file                 # Spaces to newlines
tr -dc '[:print:]\n' < file        # Keep only printable chars
tr '\t' ',' < file                 # Tabs to commas
```

**Tips:**
- Only reads from stdin (use `<` redirection)
- Character classes: `[:alpha:]`, `[:digit:]`, `[:space:]`, `[:punct:]`
- Use `-c` to complement the set

---

## sort

Sort lines of text.

```bash
sort file                          # Alphabetical sort
sort -n file                       # Numeric sort
sort -r file                       # Reverse order
sort -u file                       # Unique lines only
sort -k2 file                      # Sort by field 2
sort -k2,2n file                   # Numeric sort on field 2 only
sort -t: -k3 -n /etc/passwd        # Sort passwd by UID
sort -h file                       # Human-readable sizes (1K, 2M)
sort -M file                       # Month name sort (Jan, Feb...)
sort -R file                       # Random shuffle
sort -c file                       # Check if sorted (exit code)
```

**Tips:**
- `-k2,2` means only field 2; `-k2` means field 2 to end
- Combine with `uniq` for counting: `sort | uniq -c`
- Use `-S 50%` for large files to use more memory

---

## uniq

Report or filter repeated lines (requires sorted input).

```bash
uniq file                          # Remove adjacent duplicates
sort file | uniq                   # Remove all duplicates
sort file | uniq -c                # Count occurrences
sort file | uniq -d                # Show only duplicates
sort file | uniq -u                # Show only unique lines
uniq -i file                       # Case-insensitive
uniq -f1 file                      # Skip first field when comparing
```

**Tips:**
- MUST sort first (uniq only removes adjacent duplicates)
- `sort | uniq -c | sort -rn` = frequency count
- For unsorted unique: `awk '!seen[$0]++'`

---

## wc

Word, line, character counts.

```bash
wc file                            # Lines, words, characters
wc -l file                         # Line count only
wc -w file                         # Word count only
wc -c file                         # Byte count
wc -m file                         # Character count (UTF-8 aware)
wc -L file                         # Length of longest line
find . -name "*.py" | wc -l        # Count files
```

---

## head / tail

View beginning or end of files.

```bash
head file                          # First 10 lines
head -n 20 file                    # First 20 lines
head -c 100 file                   # First 100 bytes
tail file                          # Last 10 lines
tail -n 20 file                    # Last 20 lines
tail -f /var/log/syslog            # Follow file (live updates)
tail -F /var/log/syslog            # Follow through rotation
tail -n +5 file                    # All lines starting from line 5
```

**Tips:**
- `tail -f` is essential for log monitoring
- Use `tail -F` for logs that rotate (follows the name, not inode)
- Combine: `head -n 20 | tail -n 10` = lines 11-20

---

## column

Format output into columns.

```bash
column -t file                     # Auto-align columns
column -t -s: /etc/passwd          # Custom delimiter
mount | column -t                  # Clean up mount output
cat data.csv | column -t -s,       # Format CSV as table
```

---

## paste

Merge lines from multiple files.

```bash
paste file1 file2                  # Side by side (tab separated)
paste -d, file1 file2              # Comma separated
paste -s file                      # Serial (join all lines)
paste - - < file                   # Two columns from one file
```

---

## comm

Compare two sorted files line by line.

```bash
comm file1 file2                   # Three columns: only1, only2, both
comm -12 file1 file2               # Lines common to both
comm -23 file1 file2               # Lines only in file1
comm -13 file1 file2               # Lines only in file2
```

**Tips:**
- Files must be sorted first
- Use `diff` for more detailed comparison
