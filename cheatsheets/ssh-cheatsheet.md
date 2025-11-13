# SSH Cheatsheet

Reusable patterns for secure shell connections, agent forwarding, and tunneling.

[⬅ Back to Main Index](README.md)

## Topic: Core Connections

| Command | Description |
|---------|-------------|
| `ssh user@host` | Basic login using default key or password. |
| `ssh -i ~/.ssh/id_work user@host` | Use a specific identity file. |
| `ssh -p 2222 user@host` | Connect on a non-standard port. |
| `ssh-copy-id user@host` | Install your public key on the remote host. |

## Topic: SSH Config Snippets

```sshconfig
Host jump-prod
  HostName bastion.example.com
  User ops
  Port 2222
  IdentityFile ~/.ssh/id_work
  ForwardAgent yes
```

- Drop snippets into `~/.ssh/config` so `ssh jump-prod` expands to the full command.

## Topic: Port Forwarding & Proxying

| Command | Description |
|---------|-------------|
| `ssh -L 8080:localhost:80 user@host` | Forward local 8080 to remote port 80. |
| `ssh -R 2222:localhost:22 user@host` | Expose your local SSH server on the remote host. |
| `ssh -D 1080 user@host` | Create a dynamic SOCKS proxy on localhost:1080. |
| `ssh -J bastion target` | Use OpenSSH ProxyJump through an intermediate host. |

## Topic: Multiplexing & ControlMaster

```sshconfig
Host work-bastion
  HostName bastion
  ControlMaster auto
  ControlPath ~/.ssh/cm-%r@%h:%p
  ControlPersist 10m
```

- With multiplexing enabled, subsequent `ssh work-bastion` sessions piggyback on the first connection, speeding up repeated commands and `scp`.
