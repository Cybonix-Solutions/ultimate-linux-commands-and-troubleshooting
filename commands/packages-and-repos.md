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
**Distros:** RHEL/CentOS/Fedora (DNF-compatible)  
**Summary:** Installs, updates, or removes RPM packages while handling dependencies from configured repos.

### Common usages

```bash
sudo yum -y install net-tools                   # Pull in legacy toolkit (provides netstat, etc.)
sudo yum update                                 # Apply all available package updates
```

### Tips & troubleshooting

- Use `yum provides <file>` to discover which package ships a missing binary.
- `yum history undo <id>` quickly reverts a problematic transaction if a new package breaks workloads.
