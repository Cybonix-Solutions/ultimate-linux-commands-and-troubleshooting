# Performance Troubleshooting - Suggested Addition

**Target:** troubleshooting/performance.md (new file)
**Priority:** Critical

---

## Scenario: High CPU Usage

**Symptoms:**
- System feels slow/unresponsive
- Load average higher than CPU count
- Fans running loud
- `top` shows 100% CPU

**Applies to:** All distros

### Investigation

1. **Identify the offending process**

```bash
# Real-time view
top -o %CPU
htop

# One-shot with sorting
ps aux --sort=-%cpu | head -20

# CPU usage per process over time
pidstat 1 5
```

2. **Determine if it's user or system time**

```bash
# In top, check us% vs sy%
# High us% = user-space process (app problem)
# High sy% = kernel time (I/O, syscalls, drivers)

# Per-process breakdown
pidstat -u 1 | grep processname
```

3. **If kernel time is high, check what syscalls**

```bash
strace -c -p $(pgrep -o processname) -f
# Shows syscall distribution

perf top
# Shows which kernel functions are hot
```

4. **Check if it's a runaway process**

```bash
# Is process accumulating CPU time?
ps -p PID -o pid,etime,cputime,%cpu,comm
# etime = real time elapsed
# cputime = CPU time consumed
```

### Resolution

**Limit CPU usage:**
```bash
# With cpulimit
cpulimit -p PID -l 50  # Limit to 50%

# With cgroups/systemd
systemctl set-property myservice.service CPUQuota=50%

# With nice (lower priority)
renice 19 -p PID
```

**Kill runaway process:**
```bash
kill PID
kill -9 PID  # If it doesn't respond
```

---

## Scenario: High Memory Usage / OOM Kills

**Symptoms:**
- System becomes slow then processes get killed
- `dmesg | grep -i "oom\|killed"`
- Swap usage growing
- `free` shows low available memory

**Applies to:** All distros

### Investigation

1. **Check current memory state**

```bash
free -h
# Look at "available" not just "free"
# free = truly unused
# available = free + reclaimable cache

cat /proc/meminfo | head -10
```

2. **Find memory hogs**

```bash
ps aux --sort=-%mem | head -20
top -o %MEM

# More accurate (includes shared memory properly)
smem -rs pss | head -20
```

3. **Check for memory leaks**

```bash
# Watch process memory over time
watch -n 5 'ps -p PID -o pid,rss,vsz,comm'

# Or with pmap
pmap -x PID | tail -1
```

4. **Review OOM killer logs**

```bash
dmesg | grep -i "out of memory\|oom\|killed"
journalctl -k | grep -i oom

# Check OOM scores
cat /proc/PID/oom_score
# Higher score = more likely to be killed
```

5. **Check swap usage**

```bash
# Per-process swap
for f in /proc/*/status; do
  awk '/VmSwap|Name/{printf $2" "$3}END{print ""}' $f;
done | sort -k 2 -n | tail -20

# Or
smem -s swap | tail -20
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

---

## Scenario: High Disk I/O / System Unresponsive

**Symptoms:**
- System very slow to respond
- High `wa%` in top
- Commands hang before executing
- SSD/HDD activity light solid

**Applies to:** All distros

### Investigation

1. **Confirm I/O is the bottleneck**

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

2. **Find the process causing I/O**

```bash
iotop -o
# Shows processes with active I/O
# DISK READ, DISK WRITE columns

pidstat -d 1
# Per-process I/O stats
```

3. **Check for iowait storms**

```bash
# Processes in D (uninterruptible) state
ps aux | awk '$8 ~ /D/'

# What are they waiting for?
cat /proc/PID/stack
```

4. **Check disk health**

```bash
# SMART status
smartctl -a /dev/sda
smartctl -H /dev/sda

# Disk errors
dmesg | grep -i "error\|fail\|i/o"
```

5. **Check filesystem**

```bash
# Filesystem almost full?
df -h
df -i  # inodes

# Filesystem issues?
dmesg | grep -i "ext4\|xfs\|filesystem"
```

### Resolution

**Identify and address the I/O source:**
```bash
# If it's a runaway backup/sync
ionice -c3 -p PID  # Idle I/O class

# If it's swap thrashing
# Add memory, or reduce memory usage

# If it's database
# Check slow queries, indexes, caching

# If it's log files
# Check for log storms, rotate logs
```

**Tune I/O scheduler:**
```bash
# Check current scheduler
cat /sys/block/sda/queue/scheduler

# For SSD, use none/mq-deadline
echo none > /sys/block/sda/queue/scheduler
```

---

## Scenario: Network Slow / High Latency

**Symptoms:**
- SSH feels laggy
- File transfers slow
- Packet loss

**Applies to:** All distros

### Investigation

```bash
# Check interface errors
ip -s link show eth0
# Look for errors, dropped, overruns

# Check network utilization
iftop -i eth0
nethogs

# Check connection quality
mtr -rw targethost

# Check socket buffers
netstat -s | grep -i buffer
ss -s
```

### Resolution

```bash
# Tune TCP buffer sizes
sysctl -w net.core.rmem_max=16777216
sysctl -w net.core.wmem_max=16777216

# Check for duplex mismatch
ethtool eth0 | grep -i duplex
```

---

## Scenario: Load Average High But CPU/IO Normal

**Symptoms:**
- High load average (>CPU count)
- CPU% and I/O wait% are low
- System still feels slow

**Applies to:** All distros

### Investigation

```bash
# Check for processes in D state
ps aux | awk '$8 ~ /D/ {print $0}'

# What are they waiting on?
for p in $(ps aux | awk '$8 ~ /D/ {print $2}'); do
  echo "=== PID $p ==="
  cat /proc/$p/stack 2>/dev/null | head -5
done

# Common causes:
# - NFS mount issues (stuck I/O)
# - Disk failure (stuck I/O)
# - Kernel module issues
```

### Resolution

- Check NFS mounts: `mount | grep nfs`, try `umount -f`
- Check disk health with SMART
- Check dmesg for hardware errors
