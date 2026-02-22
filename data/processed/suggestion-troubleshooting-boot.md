# Boot and Kernel Troubleshooting - Suggested Addition

**Target:** troubleshooting/boot-and-kernel.md (new file)
**Priority:** High

---

## Scenario: System Won't Boot - Kernel Panic

**Symptoms:**
- Screen shows "Kernel panic - not syncing"
- System halts during boot
- May show "VFS: Unable to mount root fs"
- May show "not syncing: Attempted to kill init!"

**Applies to:** All distros

### Investigation

1. **Boot to previous kernel**

```bash
# At GRUB menu:
# - Press 'e' to edit boot entry
# - Or select "Advanced options" to pick older kernel
```

2. **Boot with verbose output**

```bash
# Remove 'quiet splash' from kernel command line
# Add: systemd.log_level=debug rd.debug
# Press Ctrl+X to boot
```

3. **Boot to rescue mode**

```bash
# At GRUB: select rescue mode
# Or add to kernel line: systemd.unit=rescue.target
```

### Resolution

**Kernel panic from bad kernel:**
```bash
# After booting to old kernel, remove bad kernel
dnf remove kernel-5.xx.bad
# OR
apt remove linux-image-5.xx-bad
```

**VFS mount failure (missing initramfs or wrong root):**
```bash
# Boot from live USB
mount /dev/sda2 /mnt
mount /dev/sda1 /mnt/boot
mount --bind /dev /mnt/dev
mount --bind /proc /mnt/proc
mount --bind /sys /mnt/sys
chroot /mnt

# Regenerate initramfs
# Debian/Ubuntu:
update-initramfs -u -k all

# RHEL/CentOS:
dracut --force
```

---

## Scenario: GRUB Bootloader Broken

**Symptoms:**
- "error: no such partition"
- "GRUB rescue>" prompt
- System boots directly to BIOS

**Applies to:** All distros

### Resolution from Live USB

```bash
# Identify partitions
lsblk
fdisk -l

# Mount system
mount /dev/sda2 /mnt        # root partition
mount /dev/sda1 /mnt/boot   # boot partition
mount --bind /dev /mnt/dev
mount --bind /proc /mnt/proc
mount --bind /sys /mnt/sys

# For EFI systems:
mount /dev/sda1 /mnt/boot/efi

# Chroot
chroot /mnt

# Reinstall GRUB (BIOS)
grub-install /dev/sda
grub-mkconfig -o /boot/grub/grub.cfg

# Reinstall GRUB (UEFI)
grub-install --target=x86_64-efi --efi-directory=/boot/efi
grub-mkconfig -o /boot/grub/grub.cfg

# Exit and reboot
exit
umount -R /mnt
reboot
```

### GRUB Rescue Quick Commands

```bash
# At grub rescue>
ls                              # List partitions
ls (hd0,gpt2)/                  # Check partition contents
set root=(hd0,gpt2)
set prefix=(hd0,gpt2)/boot/grub
insmod normal
normal                          # Boot normally
```

---

## Scenario: Boot Hangs at "Started Job"

**Symptoms:**
- Boot stops with "Started X service" or "A start job is running"
- Boot takes extremely long
- Progress bar stops

**Applies to:** All systemd distros

### Investigation

1. **See what's hanging**

```bash
# At boot, press Escape to see messages
# Or remove 'quiet splash' from kernel line

# After boot, check:
systemd-analyze blame
systemd-analyze critical-chain
```

2. **Common culprits:**
- Network wait services (waiting for DHCP)
- Mount units (waiting for network storage)
- fsck running on large filesystem

### Resolution

**Disable problematic service:**
```bash
systemctl mask slow-service.service
systemctl disable NetworkManager-wait-online.service
```

**Fix stuck mount:**
```bash
# Check /etc/fstab for bad entries
# Add 'nofail' option to non-critical mounts
# Add 'x-systemd.device-timeout=10s' for timeout
```

---

## Scenario: Emergency Mode / Read-Only Root

**Symptoms:**
- "Welcome to emergency mode!"
- "Cannot open access to console, the root account is locked"
- Root filesystem mounted read-only
- fsck failures

**Applies to:** All distros

### Investigation

```bash
# When in emergency mode:
journalctl -xb
# Look for mount failures, fsck errors

dmesg | grep -i error
```

### Resolution

**If root is read-only:**
```bash
mount -o remount,rw /
```

**If fsck needed:**
```bash
# Find root device
findmnt /

# Run fsck (requires unmount or read-only)
fsck -y /dev/sda2
```

**If /etc/fstab has errors:**
```bash
mount -o remount,rw /
nano /etc/fstab
# Fix bad entries (wrong UUID, missing disk, etc.)
reboot
```

---

## Scenario: Missing Kernel Modules After Update

**Symptoms:**
- Network doesn't work after kernel update
- Graphics issues after kernel update
- "modprobe: FATAL: Module X not found"

**Applies to:** All distros

### Investigation

```bash
# Check if module exists
modinfo module_name
find /lib/modules/$(uname -r) -name "*.ko*" | grep module_name

# Check if initramfs has needed modules
lsinitrd | grep module_name  # RHEL
lsinitramfs /boot/initrd.img-$(uname -r) | grep module  # Debian
```

### Resolution

**Rebuild initramfs:**
```bash
# Debian/Ubuntu
update-initramfs -u -k $(uname -r)

# RHEL/CentOS
dracut --force
```

**Install missing drivers:**
```bash
# DKMS modules need rebuild for new kernel
dkms status
dkms autoinstall

# Or reinstall driver package
apt install --reinstall nvidia-driver-xxx
```

---

## Scenario: Boot Loop After Failed Upgrade

**Symptoms:**
- System reboots repeatedly
- Gets partway through boot then restarts
- Upgrade was interrupted

**Applies to:** All distros

### Resolution

1. **Boot to recovery/rescue mode**

2. **Fix interrupted package operations:**
```bash
# Debian/Ubuntu
dpkg --configure -a
apt-get -f install

# RHEL
dnf distro-sync
rpm --rebuilddb
```

3. **If kernel is broken, boot old kernel and:**
```bash
# Remove broken kernel
apt remove linux-image-broken
# Or
dnf remove kernel-broken

# Reinstall
apt install linux-image-generic
# Or
dnf install kernel
```
