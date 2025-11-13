# Tmux Cheatsheet

Common prefix combos for navigating panes, windows, and sessions quickly.

[⬅ Back to Main Index](README.md)

## Topic: Session & Window Basics

| Shortcut | Description |
|----------|-------------|
| `tmux new -s <name>` | Create a named session. |
| `prefix` `d` | Detach from the current session. |
| `tmux attach -t <name>` | Reattach to a session. |
| `prefix` `c` | Create a new window. |
| `prefix` `,` | Rename the current window. |
| `prefix` `&` | Kill the current window (confirm). |

## Topic: Pane Management

| Shortcut | Description |
|----------|-------------|
| `prefix` `%` | Split window vertically (left/right). |
| `prefix` `"` | Split window horizontally (top/bottom). |
| `prefix` `o` | Cycle focus through panes. |
| `prefix` `{` / `}` | Move pane left/right. |
| `prefix` `arrow keys` | Resize panes one cell at a time. |
| `prefix` `Ctrl+o` | Rotate panes. |

## Topic: Copy & Scroll Mode

| Shortcut | Description |
|----------|-------------|
| `prefix` `[` | Enter copy mode (vi bindings by default). |
| `Space` / `Enter` | Start and finish selection inside copy mode. |
| `prefix` `]` | Paste the most recent selection. |
| `:capture-pane -S -` | Capture full scrollback. |
| `:save-buffer ~/tmux.log` | Save the paste buffer to a file. |

- Set `set -g mouse on` in `~/.tmux.conf` if you prefer scrolling/resizing with a mouse.
