# Security & SELinux Runbooks

Recovery guides for auth issues, SELinux blocks, and related security tooling.

[⬅ Back to Main Index](README.md)

## Scenario: Reset forgotten root password via GRUB (`rd.break`)

**Symptoms:** Root password unknown, console access available, need to regain control.  
**Applies to:** RHEL/CentOS 6–8 with GRUB access (physical or virtual).

### Investigation
1. Reboot and interrupt GRUB by tapping the arrow keys so the countdown pauses.
2. Highlight the desired kernel and press `e` to edit the boot entry.
3. Find the kernel line (starts with `linux16` on RHEL7, `linux` on RHEL8) and append `rd.break` to the end.
4. Press `Ctrl+X` to boot into the temporary rescue prompt (`switch_root:/#`).

### Resolution
- Remount the real root filesystem read/write and chroot into it:

```bash
mount -o remount,rw /sysroot
chroot /sysroot
```

- Reset the password, then flag SELinux to relabel on reboot:

```bash
passwd root
touch /.autorelabel
```

- Type `exit` to leave the chroot, then run `reboot`. SELinux relabeling may take several minutes on large filesystems; let it finish before logging back in.

## Scenario: SSSD PAM module not installed for smart card authentication

**Symptoms:** Error "SSSD PAM module is not installed" when attempting YubiKey/smart card login, despite having YubiKey software installed.
**Applies to:** Ubuntu with YubiKey PIV/CAC authentication (not U2F/FIDO).

### Investigation
1. YubiKey packages handle U2F/FIDO; SSSD smart card (PIV) requires separate modules.
2. Verify SSSD and PAM packages: `dpkg -l | grep -E 'libpam-sss|opensc|pcscd'`.
3. Check SSSD configuration: `cat /etc/sssd/sssd.conf`.

### Resolution
- Install required packages:

```bash
sudo apt update
sudo apt install libpam-sss opensc-pkcs11 pcscd
```

- Configure SSSD for certificate authentication:

```bash
sudo nano /etc/sssd/sssd.conf
```

- Ensure the `[pam]` section enables certificate auth:

```ini
[sssd]
services = pam, nss

[pam]
pam_cert_auth = True
```

- Set correct permissions on sssd.conf (required for SSSD to load):

```bash
sudo chown root:root /etc/sssd/sssd.conf
sudo chmod 600 /etc/sssd/sssd.conf
```

- Add CA certificates for the YubiKey:

```bash
sudo mkdir -p /etc/sssd/pki
sudo chmod 600 /etc/sssd/pki
sudo cat ca_chain.pem >> /etc/sssd/pki/sssd_auth_ca_db.pem
```

- Restart services and enable pcscd on boot:

```bash
sudo systemctl restart sssd
sudo systemctl enable pcscd.service
```

- Run `sudo pam-auth-update` and enable the SSSD smart card option.

## Scenario: USBGuard blocking keyboard and mouse after boot

**Symptoms:** Keyboard/mouse work at BIOS but stop responding after Linux boots. Devices are connected via USB-C hub or docking station.
**Applies to:** Systems with USBGuard enabled (common on enterprise Linux deployments).

### Investigation
1. If keyboard works at BIOS, hardware is fine—USBGuard is blocking devices post-boot.
2. User needs sudo access to fix; grant it first if not available.

### Resolution
- First, grant sudo access if needed:

```bash
sudo usermod -aG sudo username
# User must log out and back in for group membership to take effect
```

- List currently connected USB devices to find blocked ones:

```bash
sudo usbguard list-devices
```

- Allow specific blocked devices (keyboard, mouse, hub):

```bash
sudo usbguard allow-device <device-id>
```

- Make the allowance permanent by appending to policy:

```bash
sudo usbguard allow-device <device-id> -p
```

- Alternative: regenerate policy from all currently connected devices:

```bash
sudo usbguard generate-policy > /etc/usbguard/rules.conf
sudo systemctl restart usbguard
```

- Temporary workaround (not for production): stop USBGuard entirely:

```bash
sudo systemctl stop usbguard
```
