# Performance Troubleshooting Runbooks

Investigations for CPU, memory, disk I/O, and system performance issues.

[⬅ Back to Main Index](README.md)

## Scenario: High CPU Usage

**Symptoms:** System slow/unresponsive; load average higher than CPU count; `top` shows 100% CPU.
**Applies to:** All distros.

### Investigation

1. Identify the offending process:

```bash
# Real-time view
top -o %CPU
htop

# One-shot with sorting
ps aux --sort=-%cpu | head -20

# CPU usage per process over time
pidstat 1 5
```

2. Determine user vs system time:

```bash
# In top, check us% vs sy%
# High us% = user-space process (app problem)
# High sy% = kernel time (I/O, syscalls, drivers)

pidstat -u 1 | grep processname
```

3. If kernel time is high:

```bash
strace -c -p $(pgrep -o processname) -f
perf top
```

4. Check for runaway process:

```bash
ps -p PID -o pid,etime,cputime,%cpu,comm
# Compare etime (wall clock) vs cputime (CPU consumed)
```

### Resolution

**Limit CPU usage:**

```bash
# With cpulimit
cpulimit -p PID -l 50              # Limit to 50%

# With systemd
systemctl set-property myservice.service CPUQuota=50%

# Lower priority
renice 19 -p PID
```

**Kill runaway process:**

```bash
kill PID
kill -9 PID                        # If unresponsive
```

## Scenario: High Memory Usage / OOM Kills

**Symptoms:** System slow then processes killed; `dmesg | grep -i oom` shows kills; swap usage growing.
**Applies to:** All distros.

### Investigation

1. Check current memory state:

```bash
free -h
# Look at "available" not just "free"
# available = free + reclaimable cache

cat /proc/meminfo | head -10
```

2. Find memory hogs:

```bash
ps aux --sort=-%mem | head -20
top -o %MEM

# More accurate with shared memory
smem -rs pss | head -20            # If smem installed
```

3. Check for memory leaks:

```bash
# Watch process memory over time
watch -n 5 'ps -p PID -o pid,rss,vsz,comm'
```

4. Review OOM killer logs:

```bash
dmesg | grep -i "out of memory\|oom\|killed"
journalctl -k | grep -i oom

# Check OOM scores
cat /proc/PID/oom_score
```

5. Check swap usage per process:

```bash
# RHEL/Ubuntu
for f in /proc/*/status; do
  awk '/VmSwap|Name/{printf $2" "$3}END{print ""}' $f 2>/dev/null
done | sort -k 2 -n | tail -20
```

### Resolution

**Immediate relief:**

```bash
# Clear caches (safe operation)
sync; echo 3 > /proc/sys/vm/drop_caches

# Kill memory hog
kill PID
```

**Protect critical processes from OOM:**

```bash
# Lower OOM score (less likely to be killed)
echo -500 > /proc/PID/oom_score_adj

# For systemd services
systemctl set-property myservice.service OOMScoreAdjust=-500
```

**Add swap (emergency):**

```bash
fallocate -l 4G /swapfile
chmod 600 /swapfile
mkswap /swapfile
swapon /swapfile
```

**Limit memory per service:**

```bash
systemctl set-property myservice.service MemoryMax=2G
```

## Scenario: High Disk I/O / System Unresponsive

**Symptoms:** System very slow; high `wa%` in top; commands hang; disk light solid.
**Applies to:** All distros.

### Investigation

1. Confirm I/O is the bottleneck:

```bash
top
# Check wa% (I/O wait) - should be <10%

vmstat 1
# Check wa column and bi/bo (blocks in/out)

iostat -x 1
# Check %util and await
# %util near 100% = disk saturated
# await high = requests queuing
```

2. Find the process causing I/O:

```bash
iotop -o
# Shows processes with active I/O

pidstat -d 1
```

3. Check for processes in D state:

```bash
ps aux | awk '$8 ~ /D/'

# What are they waiting for?
cat /proc/PID/stack
```

4. Check disk health:

```bash
smartctl -a /dev/sda
smartctl -H /dev/sda

dmesg | grep -i "error\|fail\|i/o"
```

5. Check filesystem:

```bash
df -h                              # Space
df -i                              # Inodes

dmesg | grep -i "ext4\|xfs\|filesystem"
```

### Resolution

**Identify and address I/O source:**

```bash
# If runaway backup/sync, lower priority
ionice -c3 -p PID                  # Idle I/O class

# If swap thrashing, add memory or reduce usage
# If database, check slow queries and indexes
# If log files, check for log storms, rotate
```

**Tune I/O scheduler (for SSD):**

```bash
cat /sys/block/sda/queue/scheduler
echo none > /sys/block/sda/queue/scheduler
```

## Scenario: Load Average High But CPU/IO Normal

**Symptoms:** High load average (>CPU count); CPU% and I/O wait% are low; system feels slow.
**Applies to:** All distros.

### Investigation

```bash
# Check for processes in D (uninterruptible) state
ps aux | awk '$8 ~ /D/ {print $0}'

# What are they waiting on?
for p in $(ps aux | awk '$8 ~ /D/ {print $2}'); do
  echo "=== PID $p ==="
  cat /proc/$p/stack 2>/dev/null | head -5
done
```

Common causes: NFS mount issues, disk failure, kernel module problems.

### Resolution

- Check NFS mounts: `mount | grep nfs`, try `umount -f /mount`.
- Check disk health with SMART.
- Check dmesg for hardware errors.
