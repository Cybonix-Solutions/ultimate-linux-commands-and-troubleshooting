# Storage & RAID Runbooks

Investigations for flaky external media, LVM capacity expansions, and other storage maintenance chores.

[⬅ Back to Main Index](README.md)

## Scenario: External USB drive will not mount (DataLocker example)

**Symptoms:** Drive never appears under `/dev/sdX`, `mount` fails immediately, or dmesg shows usb-storage blocked.  
**Applies to:** RHEL, Ubuntu, Solaris systems with hardened `usb-storage` policies.

### Investigation
1. Inspect `/etc/modprobe.d/usb-storage.conf`; if you see `install usb-storage /bin/true`, usb mass storage is being blackholed.
2. Run `dmesg --follow` before attaching the drive to watch which `/dev/sdX` node appears or whether errors fire.
3. Once the kernel reports the device file, run `sudo fdisk -l /dev/sdX` to review or rebuild partitions (delete with `d`, recreate with `n`, write with `w`).

### Resolution
- Comment out or remove the `install usb-storage /bin/true` line, then `modprobe usb-storage` and reattach the device.
- Build a filesystem and mount workflow:

```bash
sudo mkfs -t ext4 /dev/sdX1
sudo mount /dev/sdX1 /mnt
# ... copy data ...
sudo umount /mnt
sudo mount -o ro /dev/sdX1 /mnt && cat /proc/mounts | grep mnt
```

- Keep `dmesg --follow` up to ensure the kernel logs healthy operations, and remount read-only before couriering the drive.

## Scenario: Extended LVM size not visible in `df`

**Symptoms:** `lvextend` reports success, `vgdisplay` shows free space consumed, but `df -h` still lists the old filesystem size.  
**Applies to:** RHEL 5–8, any LVM2-managed ext3/ext4/XFS filesystem.

### Investigation
1. Confirm the new LUN or partition exists: `sudo pvdisplay` should list the additional `/dev/sdc1` (create it with `pvcreate /dev/sdc1` if missing).
2. Verify the volume group grew: `sudo vgextend vgdata /dev/sdc1`.
3. Re-check the logical volume: `sudo lvs -a -o +devices` to ensure the LV saw the new PV.

### Resolution
- Extend and resize in one go where possible:

```bash
sudo lvextend -r -L +125G /dev/vgdata/lvdata
```

- If you already ran `lvextend` without `-r`, finish with the filesystem-specific tool:

```bash
sudo resize2fs /dev/vgdata/lvdata     # ext3/ext4
sudo xfs_growfs /mountpoint           # XFS
```

- Always take a tested backup (e.g., `rear -d -v mkbackup`) before manipulating storage layers, and document the change in your ticket with the exact commands run.

## Scenario: /var partition is full and needs more space

**Symptoms:** `/var` hits 100%, package installs fail, or services logging to `/var/log` crash.  
**Applies to:** Ubuntu/Debian systems using either LVM or single-disk root partitions.

### Investigation
1. Map current mounts with `df -h` and `lsblk`; note whether `/var` is a distinct device (e.g., `/dev/mapper/vgname-var`) or just part of `/`.
2. If `/var` is an LVM logical volume, check remaining volume group headroom with `sudo vgs` or `sudo vgdisplay <vgname>`.
3. If `/var` lives inside the root partition, confirm you have contiguous unallocated disk space or can reclaim space by moving swap/other partitions with a live environment.

### Resolution
- **When `/var` is its own LVM logical volume:**

```bash
sudo lvextend -L +5G /dev/mapper/vgname-var     # or: lvextend -l +100%FREE ...
sudo resize2fs /dev/mapper/vgname-var           # use xfs_growfs for XFS
df -h /var
```

  - Replace `vgname-var` with the actual LV name, and only run `xfs_growfs /var` if the filesystem is XFS. Keep the filesystem mounted; most ext4/xfs volumes grow online.

- **When `/var` is part of `/`:**
  - Boot from trusted live media (Ubuntu installer, GParted Live) so the root filesystem is unmounted.
  - Use `gparted`, `fdisk`, or `cfdisk` to extend the root partition into adjacent unallocated space (move swap if it blocks expansion).
  - Apply the changes, reboot normally, then grow the filesystem:

```bash
sudo resize2fs /dev/sdaX   # substitute the real root partition ID
df -h /
```

  - If resizing still fails, double-check for snapshots or filesystem errors (`sudo fsck -f /dev/sdaX`) before attempting again.

- In all cases, capture a verified backup before editing partitions and note the exact commands in the change record.
