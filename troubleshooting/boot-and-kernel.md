# Boot & Kernel Troubleshooting Runbooks

Investigations for boot failures, kernel panics, and GRUB issues.

[⬅ Back to Main Index](README.md)

## Scenario: Kernel Panic - System Won't Boot

**Symptoms:** Screen shows "Kernel panic - not syncing"; system halts during boot; "VFS: Unable to mount root fs".
**Applies to:** All distros.

### Investigation

1. Boot to previous kernel:

At GRUB menu, press `e` to edit boot entry or select "Advanced options" to pick an older kernel.

2. Boot with verbose output:

Remove `quiet splash` from kernel command line and add: `systemd.log_level=debug rd.debug`. Press Ctrl+X to boot.

3. Boot to rescue mode:

At GRUB, select rescue mode or add to kernel line: `systemd.unit=rescue.target`.

### Resolution

**Kernel panic from bad kernel:**

```bash
# After booting to old kernel, remove bad kernel
# RHEL/CentOS
dnf remove kernel-5.xx.bad

# Ubuntu/Debian
apt remove linux-image-5.xx-bad
```

**VFS mount failure (missing initramfs or wrong root):**

```bash
# Boot from live USB
mount /dev/sda2 /mnt               # Root partition
mount /dev/sda1 /mnt/boot          # Boot partition (if separate)
mount --bind /dev /mnt/dev
mount --bind /proc /mnt/proc
mount --bind /sys /mnt/sys
chroot /mnt

# Regenerate initramfs
# Ubuntu/Debian:
update-initramfs -u -k all

# RHEL/CentOS:
dracut --force

exit
umount -R /mnt
reboot
```

## Scenario: GRUB Bootloader Broken

**Symptoms:** "error: no such partition"; "GRUB rescue>" prompt; system boots directly to BIOS.
**Applies to:** All distros.

### Resolution (from Live USB)

```bash
# Identify partitions
lsblk
fdisk -l

# Mount system (adjust device names as needed)
mount /dev/sda2 /mnt               # Root partition
mount /dev/sda1 /mnt/boot          # Boot partition
mount --bind /dev /mnt/dev
mount --bind /proc /mnt/proc
mount --bind /sys /mnt/sys

# For EFI systems also mount:
mount /dev/sda1 /mnt/boot/efi

# Chroot into system
chroot /mnt

# Reinstall GRUB (BIOS/Legacy)
grub-install /dev/sda
grub-mkconfig -o /boot/grub/grub.cfg           # Ubuntu/Debian
grub2-mkconfig -o /boot/grub2/grub.cfg         # RHEL

# Reinstall GRUB (UEFI)
grub-install --target=x86_64-efi --efi-directory=/boot/efi
grub-mkconfig -o /boot/grub/grub.cfg           # Ubuntu
grub2-mkconfig -o /boot/grub2/grub.cfg         # RHEL

exit
umount -R /mnt
reboot
```

### GRUB Rescue Quick Commands

```bash
# At grub rescue> prompt
ls                                 # List partitions
ls (hd0,gpt2)/                     # Check partition contents
set root=(hd0,gpt2)
set prefix=(hd0,gpt2)/boot/grub
insmod normal
normal                             # Boot normally
```

## Scenario: Boot Hangs at "A start job is running"

**Symptoms:** Boot stops with "Started X service" or "A start job is running"; boot takes extremely long.
**Applies to:** All systemd distros.

### Investigation

```bash
# At boot, press Escape to see messages
# Or remove 'quiet splash' from kernel line

# After boot, check what was slow:
systemd-analyze blame
systemd-analyze critical-chain
```

Common culprits: network wait services, mount units waiting for storage, fsck on large filesystem.

### Resolution

**Disable problematic service:**

```bash
systemctl mask slow-service.service
systemctl disable NetworkManager-wait-online.service
```

**Fix stuck mount:**

```bash
# Edit /etc/fstab
# Add 'nofail' option for non-critical mounts
# Add 'x-systemd.device-timeout=10s' for timeout

# Example:
UUID=xxx /mnt/backup ext4 defaults,nofail,x-systemd.device-timeout=10s 0 0
```

## Scenario: Emergency Mode / Read-Only Root

**Symptoms:** "Welcome to emergency mode!"; root filesystem mounted read-only; fsck failures.
**Applies to:** All distros.

### Investigation

```bash
# When in emergency mode
journalctl -xb
dmesg | grep -i error
```

### Resolution

**If root is read-only:**

```bash
mount -o remount,rw /
```

**If fsck needed:**

```bash
findmnt /                          # Find root device
fsck -y /dev/sda2                  # Run fsck (must be unmounted or read-only)
```

**If /etc/fstab has errors:**

```bash
mount -o remount,rw /
nano /etc/fstab                    # Fix bad entries (wrong UUID, missing disk)
reboot
```

## Scenario: Missing Kernel Modules After Update

**Symptoms:** Network doesn't work after kernel update; graphics issues; "modprobe: FATAL: Module not found".
**Applies to:** All distros.

### Investigation

```bash
# Check if module exists
modinfo module_name
find /lib/modules/$(uname -r) -name "*.ko*" | grep module_name

# Check if initramfs has needed modules
# RHEL:
lsinitrd | grep module_name

# Ubuntu:
lsinitramfs /boot/initrd.img-$(uname -r) | grep module
```

### Resolution

**Rebuild initramfs:**

```bash
# Ubuntu/Debian
update-initramfs -u -k $(uname -r)

# RHEL/CentOS
dracut --force
```

**DKMS modules need rebuild:**

```bash
dkms status
dkms autoinstall

# Or reinstall driver package
apt install --reinstall nvidia-driver-xxx      # Ubuntu
dnf reinstall kmod-nvidia                       # RHEL
```

## Scenario: Boot Loop After Failed Upgrade

**Symptoms:** System reboots repeatedly; gets partway through boot then restarts.
**Applies to:** All distros.

### Resolution

1. Boot to recovery/rescue mode.

2. Fix interrupted package operations:

```bash
# Ubuntu/Debian
dpkg --configure -a
apt-get -f install

# RHEL
dnf distro-sync
rpm --rebuilddb
```

3. If kernel is broken, boot old kernel and:

```bash
# Ubuntu
apt remove linux-image-broken
apt install linux-image-generic

# RHEL
dnf remove kernel-broken
dnf install kernel
```
