# Vim Cheatsheet

Essential vim commands for editing files on remote servers and in terminal environments.

[⬅ Back to Main Index](README.md)

## Topic: Basic Navigation

| Key | Description |
|-----|-------------|
| `h j k l` | Left, down, up, right |
| `w` | Forward one word |
| `b` | Back one word |
| `e` | End of word |
| `0` | Beginning of line |
| `^` | First non-blank character |
| `$` | End of line |
| `gg` | First line of file |
| `G` | Last line of file |
| `42G` or `:42` | Go to line 42 |
| `Ctrl+F` | Page down |
| `Ctrl+B` | Page up |
| `Ctrl+D` | Half page down |
| `Ctrl+U` | Half page up |
| `%` | Jump to matching bracket |

## Topic: Entering Insert Mode

| Key | Description |
|-----|-------------|
| `i` | Insert before cursor |
| `I` | Insert at beginning of line |
| `a` | Append after cursor |
| `A` | Append at end of line |
| `o` | Open new line below |
| `O` | Open new line above |
| `Esc` | Exit insert mode |

## Topic: Editing in Normal Mode

| Key | Description |
|-----|-------------|
| `x` | Delete character |
| `dd` | Delete line |
| `dw` | Delete word |
| `d$` or `D` | Delete to end of line |
| `yy` | Yank (copy) line |
| `yw` | Yank word |
| `p` | Paste after cursor |
| `P` | Paste before cursor |
| `u` | Undo |
| `Ctrl+R` | Redo |
| `r<char>` | Replace single character |
| `cw` | Change word |
| `cc` | Change entire line |
| `>>` | Indent line |
| `<<` | Unindent line |
| `.` | Repeat last command |
| `J` | Join lines |

## Topic: Visual Mode (Selection)

| Key | Description |
|-----|-------------|
| `v` | Character visual mode |
| `V` | Line visual mode |
| `Ctrl+V` | Block visual mode |
| `gv` | Reselect last selection |

After selecting: `d` delete, `y` yank, `c` change, `>` indent, `<` unindent.

## Topic: Search and Replace

| Key/Command | Description |
|-------------|-------------|
| `/pattern` | Search forward |
| `?pattern` | Search backward |
| `n` | Next match |
| `N` | Previous match |
| `*` | Search word under cursor (forward) |
| `#` | Search word under cursor (backward) |
| `:noh` | Clear search highlighting |
| `:s/old/new/` | Replace first on current line |
| `:s/old/new/g` | Replace all on current line |
| `:%s/old/new/g` | Replace all in file |
| `:%s/old/new/gc` | Replace all with confirmation |

## Topic: Files and Buffers

| Command | Description |
|---------|-------------|
| `:w` | Save |
| `:w filename` | Save as |
| `:q` | Quit |
| `:q!` | Quit without saving |
| `:wq` or `ZZ` | Save and quit |
| `:e filename` | Open file |
| `:e!` | Reload file (discard changes) |
| `:bn` | Next buffer |
| `:bp` | Previous buffer |
| `:sp filename` | Horizontal split |
| `:vsp filename` | Vertical split |
| `Ctrl+W h/j/k/l` | Navigate splits |
| `Ctrl+W c` | Close split |

## Topic: Useful Commands

| Command | Description |
|---------|-------------|
| `:set number` | Show line numbers |
| `:set nonumber` | Hide line numbers |
| `:set paste` | Paste mode (disable auto-indent) |
| `:set nopaste` | Normal mode |
| `:syntax on` | Enable syntax highlighting |
| `:!command` | Run shell command |
| `:r !command` | Insert command output |
| `:r filename` | Insert file contents |

## Topic: Text Objects

Use with operators (d, c, y, v) for powerful editing.

| Object | Description |
|--------|-------------|
| `iw` / `aw` | Inner/around word |
| `i"` / `a"` | Inner/around double quotes |
| `i)` / `a)` | Inner/around parentheses |
| `i}` / `a}` | Inner/around braces |
| `it` / `at` | Inner/around HTML tag |

```
ci"    # Change inside quotes
da)    # Delete around parentheses
yip    # Yank inner paragraph
```

## Topic: Macros

| Key | Description |
|-----|-------------|
| `qa` | Start recording to register 'a' |
| `q` | Stop recording |
| `@a` | Play macro 'a' |
| `@@` | Repeat last macro |
| `10@a` | Play macro 10 times |
