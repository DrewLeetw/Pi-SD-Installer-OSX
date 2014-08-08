# PI SD Installer for OSX

PI SD Installer for OSX is using Python script to write image file to SD Card.

Also,you can use for any Open Hardware that need sd card to boot system

## Python Script for creating Raspberry PI SD card on OS X.

---

###Usage:

#### Simply execute the pisdinstaller.py script from Terminal and pass the image to write. (Image, not ZIP)

	eg.

```
sudo python ./pisdinstaller.py ~/Downloads/wheezy-raspbian.img
```

or

```
python ./pisdinstaller.py ~/Downloads/wheezy-raspbian.img
```

PI SD Installer uses  dd command, so it will request sudouser password.

#### Select the disk to write the image by selecting the disk number which is provided in the output.
```
+------------------------+
|No    disk       size   |
+------------------------+
| 1   disk0     121.30 GB|
+------------------------+
| 2   disk2     500.10 GB|
+------------------------+
| 3   disk3       4.00 GB|
--------------------------
Select the disk to use by enetering the number.
!!! MAKE SURE YOU SELECT THE CORRECT NUMBER FOR DISK !!!


enter number:[ 1,2,3 ] or [Q]uit:
```
#### Check your image file and disk

```
It will:
+---------------------------------------------------------------------------+
| Image File: arkos-rpi-20140718.img
| Write to  : disk3 4.0GB
+---------------------------------------------------------------------------+
Are you sure? [Y]es or [N]:n
```

#### Wait for disk to finish writing and You can check the write progress with `Ctrl+T` or `Ctrl-C` to Break.

```


Generate DD command:
+---------------------------------------------------------------------------+
[ dd bs=1024 of=/dev/rdisk3 if=arkos-rpi-20140718.img ]
+---------------------------------------------------------------------------+
Unmount of all volumes on disk3 was successful
+---------------------------------------------------------------------------+
Wait for disk to finish writing.
You can check the write progress with Ctrl+T or Ctrl-C to Break
+---------------------------------------------------------------------------+
```

When you press Ctrl + T to get DD Status

```
load: 1.14  cmd: dd 13365 uninterruptible 2.46u 71.92s
939964+0 records in
939963+0 records out
962522112 bytes transferred in 2823.141002 secs (340940 bytes/sec)
```


#### When you see the `All Done` ,it is Finished

```
+---------------------------------------------------------------------------+
Unmount Disk
+---------------------------------------------------------------------------+
Unmount failed for /dev/rdisk3
+---------------------------------------------------------------------------+
All Done!
```

---

##CAUTION:

** Make absolutely sure to select the correct disk from the list of mounted disks output by the Python script. **

**The selecting ,your system drive will `overwrite` it!**

If you are unsure which disk you need to select, you can remove the SD card and check the mounted disks by running `df -hl`, and then re-check after re-inserting the SD

eq.

```
$ df -hl
Filesystem     Size   Used  Avail Capacity  iused    ifree %iused  Mounted on
/dev/disk1s2  176Gi  104Gi   72Gi    60% 27197890 18817925   59%   /
/dev/disk0s2  112Gi  9.1Gi  103Gi     9%  2375032 27037336    8%   /Volumes/MacXD
/dev/disk2s2  465Gi   89Gi  377Gi    20% 23212533 98800133   19%   /Volumes/TM
/dev/disk3s1  100Mi   16Mi   84Mi    17%      512        0  100%   /Volumes/NO NAME
```
The disk name will likely be something similar to: `/dev/disk3s1`

---

## Download

[Pi SD Card Images](http://www.raspberrypi.org/downloads)