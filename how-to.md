# Removing FRP lock

From: https://www.samsung.com/nz/support/mobile-devices/how-to-disable-google-factory-reset-protection/

To disable Factory Reset Protection, remove the Google account from the phone or
select to Reset device (wiping all data) while it's running.

# Flashing TWRP, LineageOS

Get your phone into download mode: `[Volume Down]+[Home]+[Power]`

And then flash TWRP:

```
heimdall flash --RECOVERY <twrp-image-name>.img
```

After the system reboots, power it off and then boot it again in recovery mode
with: `[Volume Up]+[Home]+[Power]`

Then wipe caches, system and data and start ADB sideload:

```
adb sideload <lineageos>.zip
adb sideload <gapps>.zip
```

# Restore original firmware

You need to download and unzip the firmware for your device. Some website that
can be used for this are:

  - samfw.com
  - samfrew.com

## Extracting the images

The firmware bundle is a zip file that contains tar files that contain
compressed images. All needs to be unpacked:

```
unzip <firmware>.zip
for file in *.tar.md5; do
  tar -xvf $file
done
unlz4 -m *.lz4
```

This produces a folder full of .bin and .img files:

```
$ ls -lh1 *bin *img
-rw-rw-r--. 1 slaanesh slaanesh  18M Dec 16 10:40 boot.img
-rw-r--r--. 1 slaanesh slaanesh  96M Dec 16 10:41 cache.img
-rw-rw-r--. 1 slaanesh slaanesh 2.4M Dec 16 10:39 cm.bin
-rw-r--r--. 1 slaanesh slaanesh 9.5M Dec 16 10:41 hidden.img
-r--r--r--. 1 slaanesh slaanesh 9.6K Dec 16 10:39 modem.bin
-rw-rw-r--. 1 slaanesh slaanesh 1.3M Dec 16 10:39 param.bin
-rw-rw-r--. 1 slaanesh slaanesh  23M Dec 16 10:40 recovery.img
-rw-rw-r--. 1 slaanesh slaanesh 1.7M Dec 16 10:40 sboot.bin
-rw-rw-r--. 1 slaanesh slaanesh 2.5G Dec 16 10:41 system.img
-rw-rw-r--. 1 slaanesh slaanesh 830M Dec 16 10:41 userdata.img
```

## Getting the PIT file

Get your phone into download mode: `[Volume Down]+[Home]+[Power]`

Then test that you can see the device:

```
heimdall detect
```

Discover which partitions exist on the phone:
```
heimdall print-pit --no-reboot | grep -E "Partition Name|Flash Filename"
```

If this works, it will print out all the partition names along with the file
names that match with those.

## Flashing

Once you have figured out which files go where, assemble your command line by
using the partition name (all capital) with the file name.

```
heimdall flash --<PARTITION1> <file1> --<PARTITION2> <file2> [...]
```

Simple example with the files above:

```
heimdall flash \
  --BOOT boot.img \
  --CACHE cache.img \
  --HIDDEN hidden.img \
  --MODEM modem.bin \
  --PARAM param.bin \
  --RECOVERY recovery.img \
  --SBOOT sboot.bin \
  --SYSTEM system.img \
  --USERDATA userdata.img
```

Pay attention to the partition names printed by the print-pit command as they
might not always match with the filename.
