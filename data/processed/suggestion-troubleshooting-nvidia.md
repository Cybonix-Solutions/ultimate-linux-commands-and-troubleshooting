# NVIDIA Driver Troubleshooting - Suggested Addition

**Target:** troubleshooting/nvidia.md (new file)
**Priority:** High (common pain point on both RHEL and Ubuntu)

---

## Scenario: NVIDIA Driver Won't Install

**Symptoms:**
- Installation fails with "unable to find kernel source tree"
- `nvidia-smi` command not found after install
- `modprobe: FATAL: Module nvidia not found`
- Black screen after driver install

**Applies to:** RHEL, Ubuntu, Debian

### Investigation

1. **Check current driver state**

```bash
# Is NVIDIA driver loaded?
lsmod | grep nvidia

# What GPU is detected?
lspci | grep -i nvidia
lspci -vnn | grep -i nvidia

# Current driver in use
lspci -k | grep -A 3 -i nvidia
# Look for "Kernel driver in use:" line

# Check for nouveau (open source driver)
lsmod | grep nouveau
```

2. **Check if nouveau is blocking**

```bash
# Nouveau must be blacklisted
cat /etc/modprobe.d/blacklist-nouveau.conf
# Should contain:
# blacklist nouveau
# options nouveau modeset=0
```

3. **Check kernel headers**

```bash
# NVIDIA driver builds kernel modules
# Need headers matching running kernel
uname -r

# RHEL/CentOS
rpm -qa | grep kernel-devel
rpm -qa | grep kernel-headers

# Ubuntu/Debian
dpkg -l | grep linux-headers
```

### Resolution

**Install kernel headers:**
```bash
# RHEL/CentOS
sudo dnf install kernel-devel kernel-headers

# Ubuntu/Debian
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

---

## Scenario: Driver Installation Methods

**Applies to:** RHEL, Ubuntu

### Ubuntu - Recommended Method

```bash
# Check available drivers
ubuntu-drivers devices

# Auto-install recommended
sudo ubuntu-drivers autoinstall

# Or install specific version
sudo apt install nvidia-driver-535

# After install
sudo reboot
```

### Ubuntu - Manual/PPA Method

```bash
# Add graphics PPA for latest drivers
sudo add-apt-repository ppa:graphics-drivers/ppa
sudo apt update

# List available
apt search nvidia-driver | grep ^nvidia-driver

# Install
sudo apt install nvidia-driver-545

sudo reboot
```

### RHEL/CentOS - Using RPM Fusion

```bash
# Enable EPEL and RPM Fusion
sudo dnf install epel-release
sudo dnf install https://download1.rpmfusion.org/free/el/rpmfusion-free-release-$(rpm -E %rhel).noarch.rpm
sudo dnf install https://download1.rpmfusion.org/nonfree/el/rpmfusion-nonfree-release-$(rpm -E %rhel).noarch.rpm

# Install driver
sudo dnf install akmod-nvidia xorg-x11-drv-nvidia-cuda

# Wait for kernel module to build (can take several minutes)
sudo akmods --force

sudo reboot
```

### RHEL/CentOS - From NVIDIA Runfile

```bash
# Download from nvidia.com
# Install dependencies
sudo dnf install gcc make kernel-devel kernel-headers

# Disable nouveau, switch to text mode
sudo systemctl set-default multi-user.target
sudo reboot

# Run installer
sudo bash NVIDIA-Linux-x86_64-535.xx.run

# Return to graphical
sudo systemctl set-default graphical.target
sudo reboot
```

---

## Scenario: nvidia-smi Shows No Devices

**Symptoms:**
- `nvidia-smi` shows "No devices were found"
- `nvidia-smi` fails with error
- GPU not detected after boot

**Applies to:** All distros

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

# If "Key was rejected" → Secure Boot issue
```

**Secure Boot blocking:**
```bash
# Check if Secure Boot is on
mokutil --sb-state

# Options:
# 1. Disable Secure Boot in BIOS
# 2. Sign the NVIDIA module (complex)
# 3. Use distro packages that handle signing (Ubuntu nvidia-driver-*)
```

**Version mismatch:**
```bash
# Check driver version
cat /proc/driver/nvidia/version

# Check if matches kernel module
modinfo nvidia | grep version

# Rebuild if needed
# Ubuntu:
sudo dkms autoinstall

# RHEL (akmods):
sudo akmods --force
```

---

## Scenario: Black Screen After Driver Install

**Symptoms:**
- System boots to black screen
- No display output after NVIDIA install
- Can SSH but no GUI

**Applies to:** All distros

### Recovery

1. **Boot to recovery/safe mode**

```bash
# At GRUB, add to kernel line:
nomodeset

# Or select recovery mode
```

2. **Remove NVIDIA driver**

```bash
# Ubuntu
sudo apt purge 'nvidia-*'
sudo apt autoremove

# RHEL (RPM Fusion)
sudo dnf remove 'nvidia-*' 'kmod-nvidia*'

# RHEL (runfile install)
sudo /usr/bin/nvidia-uninstall

# Restore nouveau
sudo rm /etc/modprobe.d/blacklist-nouveau.conf
sudo update-initramfs -u  # Ubuntu
sudo dracut --force        # RHEL

sudo reboot
```

3. **Fix Xorg configuration**

```bash
# Remove NVIDIA Xorg config
sudo rm /etc/X11/xorg.conf
sudo rm -rf /etc/X11/xorg.conf.d/*nvidia*

# Let X auto-configure
```

---

## Scenario: Driver Breaks After Kernel Update

**Symptoms:**
- `nvidia-smi` fails after kernel update
- "NVIDIA kernel module not found"
- Black screen after kernel update

**Applies to:** All distros

### Investigation

```bash
# Check running kernel
uname -r

# Check if module exists for this kernel
ls /lib/modules/$(uname -r)/kernel/drivers/video/nvidia*
ls /lib/modules/$(uname -r)/extra/nvidia*
```

### Resolution

**Ubuntu (DKMS should auto-rebuild):**
```bash
# Check DKMS status
dkms status | grep nvidia

# Force rebuild
sudo dkms autoinstall
sudo update-initramfs -u
sudo reboot
```

**RHEL (akmod should auto-rebuild):**
```bash
# Check akmod status
rpm -qa | grep akmod-nvidia

# Force rebuild
sudo akmods --force
sudo reboot
```

**Runfile installs (manual rebuild):**
```bash
# Re-run the installer
sudo bash NVIDIA-Linux-x86_64-535.xx.run
sudo reboot
```

---

## Scenario: CUDA Not Working

**Symptoms:**
- `nvcc` not found
- CUDA programs fail to compile
- `libcuda.so` not found

**Applies to:** All distros

### Investigation

```bash
# Check CUDA installation
ls /usr/local/cuda*

# Check PATH
echo $PATH | grep cuda

# Check library path
echo $LD_LIBRARY_PATH | grep cuda

# Check nvcc
which nvcc
nvcc --version
```

### Resolution

**Add to ~/.bashrc:**
```bash
export PATH=/usr/local/cuda/bin:$PATH
export LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH
```

**Ubuntu install CUDA:**
```bash
# With nvidia-driver already installed
sudo apt install nvidia-cuda-toolkit

# Or from NVIDIA repo
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-keyring_1.0-1_all.deb
sudo dpkg -i cuda-keyring_1.0-1_all.deb
sudo apt update
sudo apt install cuda
```

---

## Scenario: Multi-GPU or Optimus (Laptop) Issues

**Symptoms:**
- Wrong GPU being used
- Laptop overheating (dedicated GPU always on)
- `prime-select` issues

**Applies to:** Ubuntu primarily, some RHEL

### Investigation

```bash
# Check which GPU is active
glxinfo | grep "OpenGL renderer"
__NV_PRIME_RENDER_OFFLOAD=1 glxinfo | grep "OpenGL renderer"

# Check prime-select (Ubuntu)
prime-select query
```

### Resolution

**Ubuntu with PRIME:**
```bash
# Switch to NVIDIA
sudo prime-select nvidia

# Switch to Intel (power save)
sudo prime-select intel

# On-demand (render offload)
sudo prime-select on-demand
```

**Run app on NVIDIA:**
```bash
__NV_PRIME_RENDER_OFFLOAD=1 __GLX_VENDOR_LIBRARY_NAME=nvidia application
```

---

## Useful NVIDIA Commands Reference

```bash
# Driver and GPU info
nvidia-smi                              # GPU status, memory, processes
nvidia-smi -L                           # List GPUs
nvidia-smi -q                           # Detailed info
nvidia-smi -q -d TEMPERATURE            # Temperature info
nvidia-smi dmon                         # Monitor mode

# Process management
nvidia-smi --query-compute-apps=pid,process_name,used_memory --format=csv
fuser -v /dev/nvidia*                   # Processes using GPU

# Driver version
cat /proc/driver/nvidia/version
modinfo nvidia | grep version

# Power management
nvidia-smi -pm 1                        # Persistence mode on
nvidia-smi -pl 200                      # Power limit to 200W

# Check ECC errors
nvidia-smi -q -d ECC

# Monitor in real-time
watch -n 1 nvidia-smi
```
