# NVIDIA Driver Troubleshooting Runbooks

Investigations for NVIDIA driver installation, GPU detection, and graphics issues.

[⬅ Back to Main Index](README.md)

## Scenario: NVIDIA Driver Won't Install

**Symptoms:** Installation fails with "unable to find kernel source tree"; `nvidia-smi` not found after install; `modprobe: FATAL: Module nvidia not found`.
**Applies to:** Ubuntu, RHEL, Debian.

### Investigation

1. Check current driver state:

```bash
# Is NVIDIA driver loaded?
lsmod | grep nvidia

# What GPU is detected?
lspci | grep -i nvidia

# Current driver in use
lspci -k | grep -A 3 -i nvidia
# Look for "Kernel driver in use:" line

# Check for nouveau (open source driver)
lsmod | grep nouveau
```

2. Check if nouveau is blocking:

```bash
cat /etc/modprobe.d/blacklist-nouveau.conf
# Should contain:
# blacklist nouveau
# options nouveau modeset=0
```

3. Check kernel headers (required to build NVIDIA module):

```bash
uname -r

# RHEL
rpm -qa | grep kernel-devel
rpm -qa | grep kernel-headers

# Ubuntu
dpkg -l | grep linux-headers
```

### Resolution

**Install kernel headers:**

```bash
# RHEL
sudo dnf install kernel-devel kernel-headers

# Ubuntu
sudo apt install linux-headers-$(uname -r)
```

**Blacklist nouveau:**

```bash
cat << 'EOF' | sudo tee /etc/modprobe.d/blacklist-nouveau.conf
blacklist nouveau
options nouveau modeset=0
EOF

# Regenerate initramfs
# RHEL:
sudo dracut --force

# Ubuntu:
sudo update-initramfs -u

sudo reboot
```

## Scenario: Installing NVIDIA Drivers

**Applies to:** Ubuntu, RHEL.

### Ubuntu - Recommended Method

```bash
# Check available drivers
ubuntu-drivers devices

# Auto-install recommended driver
sudo ubuntu-drivers autoinstall

# Or install specific version
sudo apt install nvidia-driver-535

sudo reboot
```

### Ubuntu - PPA Method (Latest Drivers)

```bash
sudo add-apt-repository ppa:graphics-drivers/ppa
sudo apt update

# List available
apt search nvidia-driver | grep ^nvidia-driver

# Install
sudo apt install nvidia-driver-545

sudo reboot
```

### RHEL - Using RPM Fusion

```bash
# Enable EPEL and RPM Fusion
sudo dnf install epel-release
sudo dnf install https://download1.rpmfusion.org/free/el/rpmfusion-free-release-$(rpm -E %rhel).noarch.rpm
sudo dnf install https://download1.rpmfusion.org/nonfree/el/rpmfusion-nonfree-release-$(rpm -E %rhel).noarch.rpm

# Install driver (builds kernel module automatically)
sudo dnf install akmod-nvidia xorg-x11-drv-nvidia-cuda

# Wait for kernel module to build
sudo akmods --force

sudo reboot
```

### RHEL - From NVIDIA Runfile

```bash
# Download from nvidia.com
# Install dependencies
sudo dnf install gcc make kernel-devel kernel-headers

# Switch to text mode (X must not be running)
sudo systemctl set-default multi-user.target
sudo reboot

# Run installer
sudo bash NVIDIA-Linux-x86_64-535.xx.run

# Return to graphical mode
sudo systemctl set-default graphical.target
sudo reboot
```

## Scenario: nvidia-smi Shows No Devices

**Symptoms:** `nvidia-smi` shows "No devices were found"; GPU not detected after boot.
**Applies to:** All distros.

### Investigation

```bash
# Is the kernel module loaded?
lsmod | grep nvidia
# Should show nvidia, nvidia_modeset, nvidia_uvm, etc.

# Check dmesg for errors
dmesg | grep -i nvidia
dmesg | grep -i nvrm

# Check if GPU is visible to system
lspci | grep -i nvidia

# Check module loading errors
journalctl -b | grep -i nvidia
```

### Resolution

**Module not loaded:**

```bash
# Try loading manually
sudo modprobe nvidia

# Check for errors
dmesg | tail -20
```

**Secure Boot blocking:**

```bash
# Check if Secure Boot is on
mokutil --sb-state

# Options:
# 1. Disable Secure Boot in BIOS
# 2. Use distro packages that handle signing (Ubuntu nvidia-driver-*)
```

**Version mismatch:**

```bash
# Check driver version
cat /proc/driver/nvidia/version
modinfo nvidia | grep version

# Rebuild if needed
# Ubuntu:
sudo dkms autoinstall

# RHEL (akmods):
sudo akmods --force
```

## Scenario: Black Screen After Driver Install

**Symptoms:** System boots to black screen; no display output; can SSH but no GUI.
**Applies to:** All distros.

### Recovery

1. Boot to recovery/safe mode (add `nomodeset` to kernel line at GRUB).

2. Remove NVIDIA driver:

```bash
# Ubuntu
sudo apt purge 'nvidia-*'
sudo apt autoremove

# RHEL (RPM Fusion)
sudo dnf remove 'nvidia-*' 'kmod-nvidia*'

# RHEL (runfile install)
sudo /usr/bin/nvidia-uninstall
```

3. Restore nouveau:

```bash
sudo rm /etc/modprobe.d/blacklist-nouveau.conf

# Ubuntu
sudo update-initramfs -u

# RHEL
sudo dracut --force

sudo reboot
```

4. Fix Xorg configuration:

```bash
sudo rm /etc/X11/xorg.conf
sudo rm -rf /etc/X11/xorg.conf.d/*nvidia*
```

## Scenario: Driver Breaks After Kernel Update

**Symptoms:** `nvidia-smi` fails after kernel update; black screen after kernel update.
**Applies to:** All distros.

### Investigation

```bash
uname -r

# Check if module exists for this kernel
ls /lib/modules/$(uname -r)/kernel/drivers/video/nvidia* 2>/dev/null
ls /lib/modules/$(uname -r)/extra/nvidia* 2>/dev/null
```

### Resolution

**Ubuntu (DKMS should auto-rebuild):**

```bash
dkms status | grep nvidia
sudo dkms autoinstall
sudo update-initramfs -u
sudo reboot
```

**RHEL (akmod should auto-rebuild):**

```bash
rpm -qa | grep akmod-nvidia
sudo akmods --force
sudo reboot
```

**Runfile installs (manual rebuild):**

```bash
sudo bash NVIDIA-Linux-x86_64-535.xx.run
sudo reboot
```

## Scenario: CUDA Not Working

**Symptoms:** `nvcc` not found; CUDA programs fail; `libcuda.so` not found.
**Applies to:** All distros.

### Investigation

```bash
ls /usr/local/cuda*
echo $PATH | grep cuda
echo $LD_LIBRARY_PATH | grep cuda
which nvcc
nvcc --version
```

### Resolution

**Add to ~/.bashrc:**

```bash
export PATH=/usr/local/cuda/bin:$PATH
export LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH
```

**Ubuntu CUDA install:**

```bash
# With nvidia-driver already installed
sudo apt install nvidia-cuda-toolkit

# Or from NVIDIA repo for latest version
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-keyring_1.0-1_all.deb
sudo dpkg -i cuda-keyring_1.0-1_all.deb
sudo apt update
sudo apt install cuda
```

## Useful NVIDIA Commands Reference

```bash
# Driver and GPU info
nvidia-smi                         # GPU status, memory, processes
nvidia-smi -L                      # List GPUs
nvidia-smi -q                      # Detailed info
nvidia-smi -q -d TEMPERATURE       # Temperature info
nvidia-smi dmon                    # Monitor mode

# Process management
nvidia-smi --query-compute-apps=pid,process_name,used_memory --format=csv
fuser -v /dev/nvidia*              # Processes using GPU

# Driver version
cat /proc/driver/nvidia/version
modinfo nvidia | grep version

# Monitor in real-time
watch -n 1 nvidia-smi
```
