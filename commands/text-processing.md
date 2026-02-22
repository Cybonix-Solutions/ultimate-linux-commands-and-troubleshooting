# Text Processing Commands

Commands for transforming, filtering, and analyzing text data in streams and files.

[⬅ Back to Main Index](README.md)

## Command: awk

**Category:** Text processing
**Distros:** All
**Summary:** Pattern scanning and processing language for extracting and transforming columnar data.

### Common usages

```bash
awk '{print $1}' file              # Print first field
awk '{print $NF}' file             # Print last field
awk -F: '{print $1}' /etc/passwd   # Custom delimiter (colon)
awk '{print NR, $0}' file          # Add line numbers
awk 'NR==5' file                   # Print line 5
awk 'NR>=5 && NR<=10' file         # Print lines 5-10
awk '/pattern/' file               # Print matching lines (like grep)
awk '!/pattern/' file              # Print non-matching lines
awk '{sum+=$1} END {print sum}'    # Sum first column
awk 'BEGIN {OFS=","} {print $1,$2}' file  # CSV output
awk 'NF' file                      # Remove blank lines
awk '!seen[$0]++' file             # Remove duplicate lines (unsorted)
```

### Tips & troubleshooting

- `$0` = entire line, `$1` = first field, `NF` = number of fields, `NR` = line number.
- Use `BEGIN{}` for header output, `END{}` for summary calculations.
- Default field separator is whitespace; use `-F` to change it.

## Command: column

**Category:** Text formatting
**Distros:** All
**Summary:** Formats stdin or file input into aligned columns for readable output.

### Common usages

```bash
column -t file                     # Auto-align columns
column -t -s: /etc/passwd          # Custom delimiter
mount | column -t                  # Clean up mount output
cat data.csv | column -t -s,       # Format CSV as table
```

### Tips & troubleshooting

- Pipe messy command output through `column -t` for instant readability.
- The `-s` flag specifies the input delimiter.

## Command: comm

**Category:** File comparison
**Distros:** All
**Summary:** Compares two sorted files line by line, showing unique and common lines.

### Common usages

```bash
comm file1 file2                   # Three columns: only1, only2, both
comm -12 file1 file2               # Lines common to both files
comm -23 file1 file2               # Lines only in file1
comm -13 file1 file2               # Lines only in file2
```

### Tips & troubleshooting

- Files must be sorted first; use `sort file1 > file1.sorted` before comparing.
- Use `diff` for more detailed comparison with context.

## Command: cut

**Category:** Text extraction
**Distros:** All
**Summary:** Extracts sections from each line of input by delimiter or character position.

### Common usages

```bash
cut -d: -f1 /etc/passwd            # First field, colon delimiter
cut -d: -f1,3 /etc/passwd          # Fields 1 and 3
cut -d: -f1-3 /etc/passwd          # Fields 1 through 3
cut -c1-10 file                    # Characters 1-10
cut -c5- file                      # Character 5 to end
cut --complement -d: -f2 file      # All fields except 2
```

### Tips & troubleshooting

- Faster than awk for simple field extraction.
- Default delimiter is TAB; use `-d` to specify another.
- Cannot reorder fields; use awk if you need `$3,$1,$2` ordering.

## Command: head

**Category:** File viewing
**Distros:** All
**Summary:** Outputs the first part of files, defaulting to the first 10 lines.

### Common usages

```bash
head file                          # First 10 lines
head -n 20 file                    # First 20 lines
head -c 100 file                   # First 100 bytes
head -n -5 file                    # All but last 5 lines
```

### Tips & troubleshooting

- Combine with `tail` to extract middle sections: `head -n 20 file | tail -n 10` for lines 11-20.
- Use `-q` to suppress filename headers when processing multiple files.

## Command: paste

**Category:** File merging
**Distros:** All
**Summary:** Merges lines from multiple files side by side.

### Common usages

```bash
paste file1 file2                  # Side by side (tab separated)
paste -d, file1 file2              # Comma separated
paste -s file                      # Serial (join all lines into one)
paste - - < file                   # Two columns from one file
```

### Tips & troubleshooting

- Use `-d` to specify the delimiter between merged columns.
- `paste - - - -` creates four columns from a single-column input.

## Command: sed

**Category:** Stream editing
**Distros:** All
**Summary:** Stream editor for filtering and transforming text using regex patterns.

### Common usages

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
sed -E 's/([a-z]+)/\U\1/' file     # Uppercase first word (extended regex)
```

### Tips & troubleshooting

- Use `-E` for extended regex (groups with `()` instead of `\(\)`).
- On macOS, `-i` requires an argument: `sed -i '' 's/old/new/g' file`.
- Test without `-i` first, then add it once the pattern is correct.

## Command: sort

**Category:** Text sorting
**Distros:** All
**Summary:** Sorts lines of text files alphabetically, numerically, or by custom keys.

### Common usages

```bash
sort file                          # Alphabetical sort
sort -n file                       # Numeric sort
sort -r file                       # Reverse order
sort -u file                       # Unique lines only
sort -k2 file                      # Sort by field 2
sort -k2,2n file                   # Numeric sort on field 2 only
sort -t: -k3 -n /etc/passwd        # Sort passwd by UID (colon delimiter)
sort -h file                       # Human-readable sizes (1K, 2M, 1G)
sort -R file                       # Random shuffle
sort -c file                       # Check if sorted (exit code)
```

### Tips & troubleshooting

- `-k2,2` means only field 2; `-k2` means field 2 to end of line.
- Combine with `uniq`: `sort file | uniq -c | sort -rn` for frequency counts.
- Use `-S 50%` to allocate more memory for sorting large files.

## Command: tail

**Category:** File viewing
**Distros:** All
**Summary:** Outputs the last part of files, with optional live following.

### Common usages

```bash
tail file                          # Last 10 lines
tail -n 20 file                    # Last 20 lines
tail -f /var/log/syslog            # Follow file (live updates)
tail -F /var/log/syslog            # Follow through log rotation
tail -n +5 file                    # All lines starting from line 5
```

### Tips & troubleshooting

- `tail -f` is essential for log monitoring; use `Ctrl+C` to stop.
- Use `tail -F` for logs that rotate; it follows the filename, not the inode.
- On RHEL, logs are in `/var/log/messages`; on Ubuntu, `/var/log/syslog`.

## Command: tr

**Category:** Character translation
**Distros:** All
**Summary:** Translates or deletes characters from stdin.

### Common usages

```bash
tr 'a-z' 'A-Z' < file              # Lowercase to uppercase
tr 'A-Z' 'a-z' < file              # Uppercase to lowercase
tr -d '[:digit:]' < file           # Delete all digits
tr -d '\r' < file                  # Remove Windows line endings (CRLF → LF)
tr -s ' ' < file                   # Squeeze repeated spaces to single
tr ' ' '\n' < file                 # Spaces to newlines (one word per line)
tr -dc '[:print:]\n' < file        # Keep only printable chars
tr '\t' ',' < file                 # Tabs to commas
```

### Tips & troubleshooting

- Only reads from stdin; use `<` redirection or pipe into it.
- Character classes: `[:alpha:]`, `[:digit:]`, `[:space:]`, `[:punct:]`.
- Use `-c` to complement the set (operate on characters NOT in the set).

## Command: uniq

**Category:** Duplicate filtering
**Distros:** All
**Summary:** Reports or filters repeated lines (requires sorted input for full deduplication).

### Common usages

```bash
uniq file                          # Remove adjacent duplicates
sort file | uniq                   # Remove all duplicates
sort file | uniq -c                # Count occurrences
sort file | uniq -d                # Show only duplicates
sort file | uniq -u                # Show only unique lines
uniq -i file                       # Case-insensitive comparison
uniq -f1 file                      # Skip first field when comparing
```

### Tips & troubleshooting

- Must sort first; uniq only removes *adjacent* duplicates.
- For frequency counting: `sort file | uniq -c | sort -rn`.
- For unsorted unique lines, use `awk '!seen[$0]++'` instead.

## Command: wc

**Category:** Counting
**Distros:** All
**Summary:** Prints line, word, and character counts for files.

### Common usages

```bash
wc file                            # Lines, words, characters
wc -l file                         # Line count only
wc -w file                         # Word count only
wc -c file                         # Byte count
wc -m file                         # Character count (UTF-8 aware)
wc -L file                         # Length of longest line
find . -name "*.py" | wc -l        # Count files matching pattern
```

### Tips & troubleshooting

- `wc -l` is the standard way to count lines in scripts.
- For counting files: `find ... | wc -l` or `ls -1 | wc -l`.
