# Package Management Commands - Suggested Addition

**Target:** commands/packages-and-repos.md
**Priority:** Critical (core skill, currently minimal coverage)

---

## apt / apt-get (Debian/Ubuntu)

Primary package manager for Debian-based systems.

```bash
apt update                         # Refresh package index
apt upgrade                        # Upgrade installed packages
apt full-upgrade                   # Upgrade with dependency changes
apt install nginx                  # Install package
apt install ./package.deb          # Install local .deb
apt remove nginx                   # Remove package (keep config)
apt purge nginx                    # Remove package + config
apt autoremove                     # Remove orphaned dependencies
apt search "web server"            # Search packages
apt show nginx                     # Package details
apt list --installed               # All installed packages
apt list --upgradable              # Packages with updates
apt-mark hold nginx                # Prevent package upgrades
apt-mark unhold nginx              # Allow upgrades again
apt-cache policy nginx             # Show version and repo source
apt-cache depends nginx            # Show dependencies
```

**Tips:**
- `apt` is the modern frontend; `apt-get` still works and is preferred in scripts
- Use `apt-mark hold` before major upgrades to protect critical packages
- Check `/var/log/apt/history.log` for installation history

---

## dpkg (Debian/Ubuntu)

Low-level .deb package manager.

```bash
dpkg -i package.deb                # Install .deb file
dpkg -r package                    # Remove package
dpkg -P package                    # Purge (remove + config)
dpkg -l                            # List all packages
dpkg -l | grep nginx               # Search installed
dpkg -L nginx                      # List files owned by package
dpkg -S /usr/bin/nginx             # Find which package owns file
dpkg --configure -a                # Fix interrupted installs
dpkg -c package.deb                # List contents of .deb
dpkg --get-selections > list.txt   # Export installed packages
dpkg --set-selections < list.txt   # Import package selections
```

**Tips:**
- Use `dpkg -L` to find config file locations
- `dpkg --configure -a` fixes "dpkg was interrupted" errors
- Combine with `apt-get -f install` to resolve broken dependencies

---

## dnf (RHEL 8+/Fedora)

Next-generation yum replacement.

```bash
dnf check-update                   # Check for updates
dnf upgrade                        # Apply updates
dnf install httpd                  # Install package
dnf install ./package.rpm          # Install local RPM
dnf remove httpd                   # Remove package
dnf autoremove                     # Remove orphaned deps
dnf search "web server"            # Search packages
dnf info httpd                     # Package details
dnf list installed                 # All installed
dnf list available                 # Available packages
dnf provides /usr/sbin/httpd       # What provides this file?
dnf repolist                       # Show enabled repos
dnf history                        # Transaction history
dnf history undo 15                # Rollback transaction 15
dnf module list                    # List module streams
dnf module enable nodejs:18        # Enable module stream
dnf group list                     # List package groups
dnf group install "Development Tools"
```

**Tips:**
- `dnf history undo` is powerful for rollbacks
- Module streams let you pick software versions (PHP 7.4 vs 8.1)
- Use `dnf needs-restarting -r` to check if reboot needed after updates

---

## rpm (RHEL/CentOS/Fedora)

Low-level RPM package manager.

```bash
rpm -ivh package.rpm               # Install with verbose output
rpm -Uvh package.rpm               # Upgrade (or install if new)
rpm -e package                     # Remove package
rpm -qa                            # List all installed
rpm -qa | grep httpd               # Search installed
rpm -qi httpd                      # Package info
rpm -ql httpd                      # List files in package
rpm -qf /usr/sbin/httpd            # Which package owns file?
rpm -qc httpd                      # List config files only
rpm -qd httpd                      # List documentation files
rpm -V httpd                       # Verify package integrity
rpm -qp --scripts package.rpm      # View pre/post install scripts
rpm --import /path/to/RPM-GPG-KEY  # Import GPG key
rpm -K package.rpm                 # Verify package signature
```

**Tips:**
- `rpm -V` detects modified config files (shows 5 for MD5 change)
- Use `rpm -qa --last` to see recently installed packages
- `rpm2cpio package.rpm | cpio -idmv` extracts without installing

---

## snap (Ubuntu/cross-distro)

Universal package format with sandboxing.

```bash
snap find "text editor"            # Search snaps
snap install code --classic        # Install (classic = no sandbox)
snap install code --channel=edge   # Install from edge channel
snap remove code                   # Remove snap
snap list                          # List installed snaps
snap refresh                       # Update all snaps
snap refresh code                  # Update specific snap
snap revert code                   # Rollback to previous version
snap info code                     # Package details
snap connections code              # Show snap permissions
snap connect code:ssh-keys         # Grant permission
```

**Tips:**
- `--classic` snaps have full system access (like traditional packages)
- Snaps auto-update; use `snap refresh --hold` to pause
- Check `/var/lib/snapd/snaps/` for disk usage

---

## flatpak (cross-distro)

Desktop application packaging.

```bash
flatpak search firefox             # Search Flathub
flatpak install flathub org.mozilla.firefox
flatpak run org.mozilla.firefox    # Run app
flatpak list                       # List installed
flatpak update                     # Update all
flatpak uninstall org.mozilla.firefox
flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo
```

**Tips:**
- Primarily for desktop apps (not servers)
- Apps are sandboxed with Bubblewrap
- Use Flatseal GUI to manage permissions
