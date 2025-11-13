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
