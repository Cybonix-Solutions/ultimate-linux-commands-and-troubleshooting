# Miscellaneous Runbooks

One-off operational guides that do not fit other categories but recur often enough to deserve a home.

[⬅ Back to Main Index](README.md)

## Scenario: Deploy Xymon/BigBrother client from a tarball

**Symptoms:** New server must report into BigBrother/Xymon monitoring; no vendor package available.  
**Applies to:** RHEL hosts with console/SSH access.

### Investigation
1. Confirm build tools are present; `gmake` may be missing on minimal installs.
2. Verify you can reach the monitoring server over SSH to pull the tarball.

### Resolution
- Install prerequisites and create the service account:

```bash
sudo yum install -y libtirpc-devel.x86_64 make
sudo useradd -d /opt/xymon xymon
```

- Download and unpack the client source on the target host:

```bash
cd /tmp
scp admin@bigbrother:/tmp/xymon-4.3.30.tar.gz .
tar -xvzf xymon-4.3.30.tar.gz --directory /opt/
```

- Build and install the client:

```bash
cd /opt/xymon-4.3.30
./configure.client
# Answer prompts: [client side], user [xymon], install dir [/opt/xymon], server IP as provided.
make -s
make install
su - xymon -c "/opt/xymon/runclient.sh start"
```

- Clean up the installer artifacts when done:

```bash
rm -rf /opt/xymon-4.3.30 /tmp/xymon-4.3.30.tar.gz
```

- For freshly built servers, locate and run the site’s `Complete_Installation_<physical|virtual>.sh` bootstrap (typically staged in `/root` or the Satellite pub share) before adding monitoring.

## Scenario: APT repository "Skipping acquire" warning for unsupported architecture

**Symptoms:** Running `sudo apt update` shows `N: Skipping acquire of configured file 'main/binary-i386/Packages' as repository '...' doesn't support architecture 'i386'`.
**Applies to:** Ubuntu/Debian with third-party repositories that only provide amd64 packages.

### Investigation
1. Identify the repository triggering the warning from the apt update output.
2. Locate the corresponding `.list` file in `/etc/apt/sources.list.d/`.

### Resolution
- Edit the source file and add `[arch=amd64]` to the deb line:

```bash
sudo nano /etc/apt/sources.list.d/example-repo.list
```

- If the line has no existing options:

```
# Before
deb https://example.repo.com/... main

# After
deb [arch=amd64] https://example.repo.com/... main
```

- If the line already has options in brackets, add `arch=amd64` inside:

```
# Before
deb [signed-by=/etc/apt/keyrings/repo-key.gpg] https://example.repo.com/... main

# After
deb [arch=amd64 signed-by=/etc/apt/keyrings/repo-key.gpg] https://example.repo.com/... main
```

- Verify the fix with `sudo apt update`; the warning should be gone.

## Scenario: USB audio device not recognized by PipeWire

**Symptoms:** USB headset or audio device detected by `lsusb` but not appearing in sound settings or `wpctl status`.
**Applies to:** Ubuntu 24.04+ with PipeWire (default), or older systems using PulseAudio.

### Investigation
1. Confirm the device is detected at USB level: `lsusb`.
2. Check if PipeWire sees the device: `wpctl status`.
3. Review kernel messages for errors: `dmesg | tail -20`.

### Resolution
- Restart the audio services to re-scan devices:

```bash
# For PipeWire (Ubuntu 24.04+ default)
systemctl --user restart pipewire pipewire-pulse

# For PulseAudio (older systems)
pulseaudio -k
```

- Verify the device now appears:

```bash
wpctl status
```

- Set the device as default output/input:

```bash
wpctl set-default <sink-id>
```

- Alternatively, use the Ubuntu Sound Settings GUI to select the device.

## Scenario: Quick Solaris/UNIX system inventory

**Symptoms:** Need a fast snapshot of hardware, networking, and user state on a Solaris box.  
**Applies to:** Solaris 10+ hosts.

### Investigation
1. Host and hardware: `hostname`, `uname -i/-a/-r`, `prtdiag -v`, `prtconf -b`, `psrinfo -pv`.
2. Memory and swap: `prtconf | grep Memory`, `swap -l`.
3. Network: `ifconfig -a`, `netstat -rn`, `cat /etc/resolv.conf`, `svcs` and `zonename`.
4. Disks and filesystems: `df -h`, `format`.
5. Processes and logs: `ps -ef`, `prstat`, `tail /var/adm/messages`, `cat /var/log/syslog` (if present).
6. Users and packages: `who`, `cat /etc/passwd`, `pkginfo`.

### Resolution
- Capture command output into a ticket for audit trails, then prioritize remediation (patching, hardware swaps, or cleanup) based on what the inventory reveals.
