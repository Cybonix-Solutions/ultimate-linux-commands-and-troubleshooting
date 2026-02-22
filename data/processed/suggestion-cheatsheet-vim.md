# Vim Cheatsheet - Suggested Addition

**Target:** cheatsheets/vim-cheatsheet.md (new file)
**Priority:** High (essential for remote server work)

---

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
| `H M L` | Top/middle/bottom of screen |
| `%` | Jump to matching bracket |

---

## Topic: Editing (Insert Mode)

| Key | Description |
|-----|-------------|
| `i` | Insert before cursor |
| `I` | Insert at beginning of line |
| `a` | Append after cursor |
| `A` | Append at end of line |
| `o` | Open new line below |
| `O` | Open new line above |
| `Esc` | Exit insert mode |
| `Ctrl+[` | Exit insert mode (alternative) |

---

## Topic: Editing (Normal Mode)

| Key | Description |
|-----|-------------|
| `x` | Delete character |
| `dd` | Delete line |
| `dw` | Delete word |
| `d$` or `D` | Delete to end of line |
| `d0` | Delete to beginning of line |
| `yy` | Yank (copy) line |
| `yw` | Yank word |
| `p` | Paste after cursor |
| `P` | Paste before cursor |
| `u` | Undo |
| `Ctrl+R` | Redo |
| `r<char>` | Replace single character |
| `R` | Replace mode (overwrite) |
| `cw` | Change word |
| `cc` | Change entire line |
| `c$` or `C` | Change to end of line |
| `~` | Toggle case |
| `>>` | Indent line |
| `<<` | Unindent line |
| `.` | Repeat last command |
| `J` | Join lines |

---

## Topic: Visual Mode (Selection)

| Key | Description |
|-----|-------------|
| `v` | Character visual mode |
| `V` | Line visual mode |
| `Ctrl+V` | Block visual mode |
| `gv` | Reselect last selection |

After selecting:
| Key | Description |
|-----|-------------|
| `d` | Delete selection |
| `y` | Yank selection |
| `c` | Change selection |
| `>` | Indent selection |
| `<` | Unindent selection |
| `=` | Auto-indent selection |

---

## Topic: Search and Replace

| Key | Description |
|-----|-------------|
| `/pattern` | Search forward |
| `?pattern` | Search backward |
| `n` | Next match |
| `N` | Previous match |
| `*` | Search word under cursor (forward) |
| `#` | Search word under cursor (backward) |
| `:noh` | Clear search highlighting |

**Replace (in command mode):**

| Command | Description |
|---------|-------------|
| `:s/old/new/` | Replace first on current line |
| `:s/old/new/g` | Replace all on current line |
| `:%s/old/new/g` | Replace all in file |
| `:%s/old/new/gc` | Replace all with confirmation |
| `:5,10s/old/new/g` | Replace in lines 5-10 |
| `:'<,'>s/old/new/g` | Replace in visual selection |

---

## Topic: Files and Buffers

| Command | Description |
|---------|-------------|
| `:w` | Save |
| `:w filename` | Save as |
| `:q` | Quit |
| `:q!` | Quit without saving |
| `:wq` or `:x` or `ZZ` | Save and quit |
| `:e filename` | Open file |
| `:e!` | Reload file (discard changes) |
| `:bn` | Next buffer |
| `:bp` | Previous buffer |
| `:bd` | Close buffer |
| `:ls` | List buffers |
| `:sp filename` | Horizontal split |
| `:vsp filename` | Vertical split |
| `Ctrl+W h/j/k/l` | Navigate splits |
| `Ctrl+W =` | Equal size splits |
| `Ctrl+W _` | Maximize current split |
| `Ctrl+W c` | Close split |

---

## Topic: Useful Commands

| Command | Description |
|---------|-------------|
| `:set number` | Show line numbers |
| `:set nonumber` | Hide line numbers |
| `:set paste` | Paste mode (disable auto-indent) |
| `:set nopaste` | Normal mode |
| `:set ignorecase` | Case-insensitive search |
| `:set hlsearch` | Highlight search matches |
| `:syntax on` | Enable syntax highlighting |
| `:set tabstop=4` | Tab width |
| `:set expandtab` | Use spaces instead of tabs |
| `:!command` | Run shell command |
| `:r !command` | Insert command output |
| `:r filename` | Insert file contents |
| `ga` | Show ASCII code of character |
| `g Ctrl+G` | Show cursor position info |
| `:earlier 5m` | Revert to 5 minutes ago |
| `:later 5m` | Go forward 5 minutes |

---

## Topic: Text Objects

Use with operators (d, c, y, v) for powerful editing.

| Object | Description |
|--------|-------------|
| `iw` / `aw` | Inner/around word |
| `is` / `as` | Inner/around sentence |
| `ip` / `ap` | Inner/around paragraph |
| `i"` / `a"` | Inner/around double quotes |
| `i'` / `a'` | Inner/around single quotes |
| `i)` / `a)` | Inner/around parentheses |
| `i]` / `a]` | Inner/around brackets |
| `i}` / `a}` | Inner/around braces |
| `it` / `at` | Inner/around HTML tag |

**Examples:**
```
ci"    Change inside quotes
da)    Delete around parentheses (including parens)
yip    Yank inner paragraph
vat    Select around HTML tag
```

---

## Topic: Macros

Record and replay keystrokes.

| Key | Description |
|-----|-------------|
| `qa` | Start recording to register 'a' |
| `q` | Stop recording |
| `@a` | Play macro 'a' |
| `@@` | Repeat last macro |
| `10@a` | Play macro 10 times |

**Example workflow:**
```
qa           Start recording to 'a'
0            Go to line start
f"           Find quote
ci"          Change inside quotes
NEW TEXT     Type new text
Esc          Exit insert
j            Next line
q            Stop recording
10@a         Apply to next 10 lines
```
