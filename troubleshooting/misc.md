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
