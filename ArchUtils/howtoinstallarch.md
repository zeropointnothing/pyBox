### i use arch btw.

(

To dual boot, simply shrink the current OS's partition and place ARCH in there.

)

### NOTE:
All steps marked with * are for dual booting Arch Linux. If you're just installing, ignore these steps.

```bash
# To make sure you are in UEFI mode (needed for dual boot with this guide), run

ls /sys/firmware/efi/efivars

# If you don't see anything, this guide wont work.
```

## STEP ONE : : NETWORK

- Use iwctl to connect to the internet.

```bash
iwctl

device list

# DEVICE will most likely be wlan0

station DEVICE scan

station DEVICE get-networks

station DEVICE connect NETWORK

exit
```

- Test your connection. You should see it start "pinging" archlinux.org multiple times.

```bash
ping archlinux.org
```

## STEP TWO : : SYSTEM TIME

- Update the system time.

```bash
timedatectl set-ntp true
```

- Confirm it was set correctly.

```bash
timedatectl status
```

## STEP THREE : : PARTITIONS

- Let's give Linux a place to live. Remember, if you are dual booting, you have to make some space in Windows for ARCH to borrow!

```bash
cfdisk

# You should see a 'gui' open up. What we're interested in is the 'Free space' (should be green) label(s).

# This should be the entire drive if it's empty, or the amount of space you made with the partition manager eariler.

# Use the arrow keys to move to the free space and then press enter. It will ask you how big you want to make the parition. Make it MOST of your free space, but not all! This is called your 'root' partition, AKA where the actual OS is.

# Now do the same for your 'swap' partition, but make this one at least 4GB's. More specific info on how big this should be is here: https://itsfoss.com/swap-size/ (Do note that this is a general recommendation. If you have a good amount of RAM, SWAP may never be used. So make it 4-2GB at least.)

# Almost done! First, verify that in the 'Type' tab, the new parition you made for Linux is of the type "Linux filesystem". If it isn't, set it to that. Next, navigate to your new swap partition. Then, select the '[   Type   ]' button on the bottom. This should open up a menu. In this menu, select Linux swap'

# Finally, select the '[   Write   ]' button and type in yes to confirm.

# Exit with the '[   Exit   ]' button. Make sure to remember the partition labels! (It might be something like /dev/sda1 or /dev/nvmeOn1). These are important.
```

- Now we need to format the drive. This part is easy.

```bash
# Replace PART with the respective partition.


# Format the 'root' partition (Linux filesystem)

mkfs.ext4 /dev/PART

# Format the 'swap' partition (Linux swap)

mkswap /dev/PART
```

- Finally, enable the swap partition.

```bash
swapon /dev/PART
```

- Now we need to mount the root partition so we can install to it.

```bash
mount /dev/PART /mnt
```

- *Create a place for the Windows EFI system.

```bash
mkdir /mnt/efi
```

- *Mount the Windows EFI system.

```bash
# Replace PART with the EFI System type partition. Most likely sda1.

mount /dev/PART /mnt/efi
```

## STEP FOUR : :  CORE LINUX SETUP

### Installing Linux

- Install linux itself.

```bash
pacstrap /mnt base linux linux-firmware
```
This could take a while, so go ahead and take a well deserved break.

- Now we need to generate the fstab file. This tells your computer how to mount all the partitions automatically at start up.
```bash
genfstab -U /mnt >> /mnt/etc/fstab
```

- Now we get to enter our freshly made Linux system! We're almost there!

```bash
arch-chroot /mnt
```

If you want to verify you're in the right place, you can use the `ls` command to see the current files in your directory.

### Making Linux work with where you live.

- Let's set our timezone for the system.

```bash
ln -sf /usr/share/zoneinfo/CODE/ZONE /etc/localtime

# Don't know what to fill in? run 
# ls /usr/share/zoneinfo
# to find your code, and then
# ls /usr/share/zoneinfo/CODE
# to figure out what you should replace CODE and ZONE with.
```
- Next, sync the hardware clock.

```bash
hwclock --systohc
```

- Now, we need to set our Locale. This is important because it controls system language, currency format, numbering, and date systems.

```bash
# Open the file with vim. If this isn't installed, run 'pacman -Sy vim'

vim /etc/locale.gen

# Find your locale and remove the # in front of it. Don't know how to use VIM? You'll have to find a tutorial for it.
```

- Generate the locale.

```bash
locale-gen
```

- Create a locale config.

```bash
# Replace LOCALE with the locale from before. (for example, EN_US.UTF-8)

echo "LANG=LOCALE" > /etc/locale.conf
```

- Now we need a host name for our system. This can be anything you want, but you should make it simple. Replace archpc with your desired host name.

### Networks

```bash
echo archpc > etc/hostname

# Check that you did it correctly. You should see your host name appear.

cat etc/hostname
```

- Now we need to modify the etc/hosts file to support this.

```bash

# Again, replace archpc with your actual host name.

echo "127.0.1.1 archpc" >> /etc/hosts
```

- Now let's install a network manager.

```bash
# Note, in some cases, you might still have to install NetworkManager and NetworkManager-applet for your internet to work properly. Though I have not tested this.

pacman -Sy netctl # Select the openresolv provider if prompted to choose.

# There are optional dependencies for netctl. These are:

# dhcpcd - For DHCP support
# wpa-supplicant - For wireless networking
# ifplugd - For wired connections networking

# To install them, run

pacman -Sy dhcpcd wpa-supplicant ifplugd
```

### Using NetworkManager (use me)

- Network manager is a much better way to manage networks.

```bash
pacman -S networkmanager

# Then, make sure to start NetworkManager up.

systemctl enable NetworkManager.service
```

### Adding a user

- Now we need to make ourselves a user to actually log into.

```bash
# Replace USERNAME with whatever you want.

useradd -G wheel -m USERNAME
```

- Now let's add a password.

```bash
passwd USERNAME
```

- If you would like to make this user a sudo user, (which you should have a least one that this is so for.) run the following command, replacing USERNAME with your username once again.

```bash
sudo visudo
# If that doesn't work, open it manually with sudo vim /etc/sudoers Be careful if doing this however as syntax errors can make sudo stop working entirely.

# You can set sudo to allow users of the wheel group to run sudo, which we added our main user to before.

# Locate this line and uncomment as it instructs.

## Uncomment to allow members of group wheel to execute any command
# %wheel ALL=(ALL:ALL) ALL
```

## STEP FIVE : : FINAL PRE-INSTALL STEPS

- This is the final stretch! First, we need to install GRUB, a bootloader. This will allow us to start Linux up when our computer boots to this drive.

```bash
pacman -S grub # also install efibootmgr if in UEFI mode.
```

- *Now we need to install os-prober. This will let GRUB find our Windows installation.

```bash
pacman -S os-prober
```

- Now we need to install GRUB.

```bash
grub-install --target=x86_64-efi --efi-directory=/efi --bootloader-id=GRUB
```

- Create the config for grub.

```bash
# Note, if you installed os-prober for a dual boot system, you should see a messaged indicating that it found the Windows Boot Manager. If you don't see this when you *should* be, make sure that GRUB_DISABLE_OS_PROBER is set to false in etc/default/grub and Secure Boot is set to Disabled in the UEFI Firmware settings.

grub-mkconfig -o /boot/grub/grub.cfg

# If you are unable to locate the Windows EFI system like this, you may run os-prober after booting into the Linux system and then grub-mkconfig -o /boot/grub/grub.cfg again. It should find it and update GRUB.
```

- This next part is optional, but recommended. You can do this later, however.

```bash
# Set the 'root' user's password. You can skip this step to have that password simply be your user password, however this is a security risk as root has all permissions.

passwd
```

- Finally, reboot the system.

```bash
exit

reboot
```

---

And you're done! 

Kind of.

If you did everything correctly, you have the very basic barebones version of Arch Linux running now. We still have some work to do.

## STEP SIX : : POST-INSTALL

- (YOU SHOULD IGNORE THIS) You might notice that internet isn't working quite right yet. That's because it isn't configured correctly by default. Let's figure out what our network device is.

```bash
# This will return a lot of stuff, but don't worry, we're only focusing on one part. You're looking for a device that will have a name that might be unique, or it could simply be wlan0. It will not be lo, however, so ignore that one.

ip link
```

- Switch to root.

```bash
su # or, if you have sudo installed, sudo su
```

- Copy the ethernet-dhcp file to /etc/netctl.

```bash
cp /etc/netctl/examples/ethernet-dhcp  /etc/netctl/custom-dhcp-profile
```

- Now navigate the there.

```bash
cd /etc/netctl
```

- Use vim to open up this file.

```bash
vim custom-dhcp-profile
```

- You should see a value called Interface. We need to set that to the device we located eariler. Also, uncomment the line `DHCPClient=dhcpcd`

- Save and exit the config (ESC, : + wq)

- Enable the profile.

```bash
netctl enable custom-dhcp-profile
```

- Finally, enable it.

```bash
systemctl enable dhcpcd.service
```

### Using NetworkManager

- Simply run nmtui to open the Curses based menu and login through there.

```bash
nmtui

# Or, use the other command, nmcli for full cmd prompt.
```

- Verify that you can connect to the internet by pinging a website.

```bash
ping archlinux.org
```
## STEP SEVEN :: DISPLAY MANAGERS

- This is the fun part! Now that Arch Linux, our backbone is set up, we can choose how we want it to look. For this example, I'm going to go with my personal favorite, KDE Plasma. However, you can choose whichever DE (Desktop Env) you like!

- Install KDE Plasma (optionally also install kde-applications. This is a good idea as it includes things like Konsole and Dolphin, which are essential.)

```bash
pacman -S xorg plasma plasma-wayland-session

# Another good option is Hyprland. Follow this tutorial to install: https://www.youtube.com/watch?v=8GmpCwBqHCA&t=0s

# Start it by running the Hyprland command.
```

- Install sddm if you haven't already.

```bash
sudo pacman -S sddm
```

- Start SDDM and if you havent already, NetworkManager

```bash
systemctl enable sddm.service
systemctl enable NetworkManager.service
```

Once your DE is installed, you can reboot your system to see if it was correctly installed!

```bash
reboot
```

## STEP EIGHT (FINAL) : : POST-POST-INSTALL

Now that we have a freshly baked copy of Arch Linux, there's some things we might need to fix.

### No Bluetooth

A common (and almost always existant) issue with Arch Linux is bluetooth. It simply just doesn't work!

Well, at least it seems like it. The real issue is that the service for managing bluetooth was never installed.

---

- First, we should check if we have the services installed.

```bash
pacman -Ss bluez-utils bluez
```
- If we don't, we'll have to install them.

```bash
sudo pacman -S bluez-utils bluez
```
- Next, start bluetooth up and set it to start on boot.

```bash
sudo systemctl start bluetooth
sudo systemctl enable bluetooth
```
- Finally, check if it started correctly.

```bash
systemctl status bluetooth
```

- If all went well, and maybe after a restart, bluetooth should now be working perfect.

### No Browser

Unlike most Operating Systems nowadays, Arch Linux comes with no browser built in, leaving you to be able to choose! Now, the easiest one to install is firefox, so I'm going to show you how.

```bash
sudo pacman -S firefox
```

Done! That's all you need to do.