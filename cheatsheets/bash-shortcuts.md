# Bash Shortcuts & Snippets

Quick references for interactive shell work, from readline tricks to lightweight scripting patterns.

[⬅ Back to Main Index](README.md)

## Topic: Array Basics

```bash
# Read a line of space-delimited values into an array
read line
list=(${line})

# Print elements one per line
for e in "${list[@]}"; do
  echo "$e"
done
```

- Always double-quote `"${list[@]}"` when echoing elements that may contain whitespace.

## Topic: Iterate Over Indices

```bash
for i in "${!myarray[@]}"; do
  printf '%s: %s\n' "$i" "${myarray[$i]}"
done
```

- `${!array[@]}` expands to the list of indexes, which is helpful when you must mutate array contents in place.

## Topic: Renumber Lines with `sed`

```bash
sed -E 's/(.*Disc )([0-9]+)(.*)/echo "\1$((\2+1))\3"/ge' sedthis.txt
```

- Useful when you need to bump a list numbered from 0..N up to 1..N. The `-E` regex captures the prefix and suffix, then `$(())` increments the middle number in place.
