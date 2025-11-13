# FTP Command Reference

Common interactive FTP client commands for quickly moving files between hosts, including anonymous sessions.

[⬅ Back to Main Index](README.md)

## Topic: Session Management

| Command | Description |
|---------|-------------|
| `open <host>` | Connect to a remote FTP server (auth or anonymous). |
| `close` | Terminate the current connection but stay in the FTP client. |
| `bye` / `quit` | Exit the FTP client entirely. |
| `lcd <dir>` | Change the local working directory. |
| `cd <dir>` | Change directories on the remote host. |
| `pwd` | Print the current remote directory. |
| `mkdir <dir>` / `rmdir <dir>` | Create or remove remote directories. |

## Topic: Transfers

| Command | Description |
|---------|-------------|
| `ascii` / `binary` | Set transfer mode (7-bit text vs raw 8-bit binary). |
| `get <src> [dst]` | Download a single file. |
| `mget <pattern>` | Download multiple files; prompts per file. |
| `put <src> [dst]` | Upload a single file. |
| `mput <pattern>` | Upload multiple files with y/n confirmation. |
| `delete <file>` | Remove a remote file (`rm` equivalent). |
| `ls [path]` | List remote directory contents. |

## Topic: Help & Discovery

| Command | Description |
|---------|-------------|
| `?` / `help` | Show available FTP commands or help for a specific one. |

- Anonymous downloads typically use username `anonymous` with an email address as the password.
