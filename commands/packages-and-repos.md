# Package & Repository Commands

Commands that help locate packages, manage firmware updates, and keep systems in sync with upstream repositories.

[⬅ Back to Main Index](README.md)

## Command: apt-file

**Category:** Package search  
**Distros:** Debian/Ubuntu  
**Summary:** Searches the APT package index for the package providing a given file path or pattern.

### Common usages

```bash
sudo apt update && sudo apt install apt-file    # Install the search helper
sudo apt-file update                            # Sync its index (separate from apt)
apt-file search <filename_pattern>              # Find which package ships the file
```

### Tips & troubleshooting

- Run `apt-file update` after every `apt update`; it maintains its own cache.
- Use anchored patterns (`usr/bin/foo$`) to avoid noisy hits.

## Command: fwupdmgr

**Category:** Firmware updates  
**Distros:** All (fwupd-supported hardware)  
**Summary:** Queries the LVFS to see if the system firmware has updates queued.

### Common usages

```bash
fwupdmgr get-devices           # Inventory supported hardware
fwupdmgr get-updates           # Show pending updates
fwupdmgr update                # Apply all applicable updates
```

### Tips & troubleshooting

- Ensure `fwupd` service is running; on servers without GUI you may need to start it manually.
- Updates usually require a reboot; schedule maintenance windows accordingly.

## Command: subscription-manager

**Category:** Subscription/registration  
**Distros:** RHEL/CentOS  
**Summary:** Registers systems to Red Hat Customer Portal or Satellite, manages entitlement certificates, and imports offline subscriptions.

### Common usages

```bash
sudo subscription-manager clean                                       # Remove cached identity data
sudo yum -y remove katello-ca-consumer*                               # Drop stale Satellite certs
curl -o /var/tmp/katello-cert.rpm http://<satellite>/pub/katello-cert.rpm
sudo yum -y install /var/tmp/katello-cert.rpm --nogpgcheck             # Install the CA from Satellite
sudo subscription-manager register --org=<ORG> --activationkey=<KEY>   # Register with an activation key

sudo subscription-manager import --certificate=/tmp/<entitlement>.pem  # Offline import of a downloaded cert
```

### Tips & troubleshooting

- If DNS is missing, add the Satellite host to `/etc/hosts` before registering.
- For disconnected hosts, download the `consumer_export.zip` bundle from the Customer Portal, extract the PEM from `export/entitlement_certificates/`, copy it to `/tmp`, and import it with `subscription-manager import`.
- When manually seeding Satellite content from DVD ISOs, mount each ISO and copy into `/var/www/html/pub/sat-import/`:

```bash
for ISO in *.iso; do
  echo "Mounting $ISO"
  sudo mount -o loop "$ISO" /mnt/iso
  sudo cp -ru /mnt/iso/* /var/www/html/pub/sat-import/.
  sudo umount /mnt/iso
done
```
- After importing media, sync products (`Content -> Sync Status -> Expand All -> Synchronize Now`), then save and promote each Content View through successive environments.

## Command: yum

**Category:** Package management
**Distros:** RHEL/CentOS 7 (use dnf on RHEL 8+)
**Summary:** Installs, updates, or removes RPM packages while handling dependencies from configured repos.

### Common usages

```bash
sudo yum -y install net-tools                   # Pull in legacy toolkit (provides netstat, etc.)
sudo yum update                                 # Apply all available package updates
```

### Tips & troubleshooting

- Use `yum provides <file>` to discover which package ships a missing binary.
- `yum history undo <id>` quickly reverts a problematic transaction if a new package breaks workloads.

## Command: apt

**Category:** Package management
**Distros:** Ubuntu, Debian, Linux Mint
**Summary:** Modern package manager frontend for Debian-based systems with user-friendly output.

### Common usages

```bash
apt update                         # Refresh package index
apt upgrade                        # Upgrade installed packages
apt full-upgrade                   # Upgrade with dependency changes
apt install nginx                  # Install package
apt install ./package.deb          # Install local .deb file
apt remove nginx                   # Remove package (keep config)
apt purge nginx                    # Remove package and config
apt autoremove                     # Remove orphaned dependencies
apt search "web server"            # Search packages
apt show nginx                     # Package details
apt list --installed               # All installed packages
apt list --upgradable              # Packages with updates available
apt-mark hold nginx                # Prevent package from upgrading
apt-mark unhold nginx              # Allow upgrades again
apt-cache policy nginx             # Show version and repo source
apt-cache depends nginx            # Show dependencies
```

### Tips & troubleshooting

- `apt` is the modern frontend; `apt-get` still works and is preferred in scripts.
- Use `apt-mark hold` before major upgrades to protect critical packages.
- Check `/var/log/apt/history.log` for installation history.

## Command: dpkg

**Category:** Package management
**Distros:** Ubuntu, Debian, Linux Mint
**Summary:** Low-level .deb package manager for direct package manipulation.

### Common usages

```bash
dpkg -i package.deb                # Install .deb file
dpkg -r package                    # Remove package
dpkg -P package                    # Purge (remove + config)
dpkg -l                            # List all installed packages
dpkg -l | grep nginx               # Search installed packages
dpkg -L nginx                      # List files owned by package
dpkg -S /usr/bin/nginx             # Find which package owns a file
dpkg --configure -a                # Fix interrupted installs
dpkg -c package.deb                # List contents of .deb before install
dpkg --get-selections > list.txt   # Export installed packages
dpkg --set-selections < list.txt   # Import package selections
```

### Tips & troubleshooting

- Use `dpkg -L` to find config file locations for a package.
- `dpkg --configure -a` fixes "dpkg was interrupted" errors.
- Combine with `apt-get -f install` to resolve broken dependencies after dpkg errors.

## Command: dnf

**Category:** Package management
**Distros:** RHEL 8+, Fedora, Rocky, AlmaLinux
**Summary:** Next-generation package manager replacing yum with better dependency resolution and module support.

### Common usages

```bash
dnf check-update                   # Check for available updates
dnf upgrade                        # Apply all updates
dnf install httpd                  # Install package
dnf install ./package.rpm          # Install local RPM
dnf remove httpd                   # Remove package
dnf autoremove                     # Remove orphaned dependencies
dnf search "web server"            # Search packages
dnf info httpd                     # Package details
dnf list installed                 # All installed packages
dnf list available                 # Available packages
dnf provides /usr/sbin/httpd       # What package provides this file?
dnf repolist                       # Show enabled repos
dnf history                        # Transaction history
dnf history undo 15                # Rollback transaction 15
dnf module list                    # List module streams
dnf module enable nodejs:18        # Enable specific module stream
dnf group list                     # List package groups
dnf group install "Development Tools"  # Install package group
```

### Tips & troubleshooting

- `dnf history undo` is powerful for rollbacks after problematic updates.
- Module streams let you choose software versions (e.g., PHP 7.4 vs 8.1).
- Use `dnf needs-restarting -r` to check if reboot is required after updates.

## Command: rpm

**Category:** Package management
**Distros:** RHEL, CentOS, Fedora, Rocky, AlmaLinux
**Summary:** Low-level RPM package manager for direct package queries and manipulation.

### Common usages

```bash
rpm -ivh package.rpm               # Install with verbose output
rpm -Uvh package.rpm               # Upgrade (or install if new)
rpm -e package                     # Remove package
rpm -qa                            # List all installed packages
rpm -qa | grep httpd               # Search installed packages
rpm -qi httpd                      # Package info
rpm -ql httpd                      # List files in package
rpm -qf /usr/sbin/httpd            # Which package owns this file?
rpm -qc httpd                      # List config files only
rpm -qd httpd                      # List documentation files
rpm -V httpd                       # Verify package integrity
rpm -qp --scripts package.rpm      # View pre/post install scripts
rpm --import /path/to/RPM-GPG-KEY  # Import GPG key
rpm -K package.rpm                 # Verify package signature
```

### Tips & troubleshooting

- `rpm -V` detects modified config files (shows `5` for MD5 change, `S` for size).
- Use `rpm -qa --last` to see recently installed packages.
- `rpm2cpio package.rpm | cpio -idmv` extracts contents without installing.

## Command: snap

**Category:** Package management
**Distros:** Ubuntu (default), available on most distros
**Summary:** Universal package format with automatic updates and sandboxing.

### Common usages

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

### Tips & troubleshooting

- `--classic` snaps have full system access (like traditional packages).
- Snaps auto-update; use `snap refresh --hold` to pause updates.
- Check `/var/lib/snapd/snaps/` for disk usage.
- To disable snap on Ubuntu: remove snapd package and hold it.

## Command: flatpak

**Category:** Package management
**Distros:** All (primarily for desktop apps)
**Summary:** Sandboxed application distribution primarily for desktop software.

### Common usages

```bash
flatpak search firefox             # Search Flathub
flatpak install flathub org.mozilla.firefox  # Install from Flathub
flatpak run org.mozilla.firefox    # Run app
flatpak list                       # List installed apps
flatpak update                     # Update all apps
flatpak uninstall org.mozilla.firefox
flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo
```

### Tips & troubleshooting

- Primarily for desktop apps, not server software.
- Apps are sandboxed with Bubblewrap.
- Use Flatseal GUI to manage app permissions.
