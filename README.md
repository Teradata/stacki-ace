The best ARM on the team is an ACE.

---

Requirements

# Frontend

* [Raspberry Pi 3 Model B](https://www.raspberrypi.org/products/raspberry-pi-3-model-b/)

* MicroSD card with at least 2 GB of storage

# Backend

* [Raspberry Pi 3 Model B](https://www.raspberrypi.org/products/raspberry-pi-3-model-b/)

* MicroSD card with at least 2 GB of storage

---

# Build Your Frontend

* On your Linux workstation, download `stacki-centos.img` and copy it onto
the MicroSD card that you will use to build your frontend Pi.

Most likely, you'll need to put your MicroSD card into an adapter in order
to insert it into your workstation.

After you insert your MicroSD card into your workstation, you should see
messages like this from `dmesg`:

   ```
[20630376.657782] sd 49:0:0:0: [sdd] 124735488 512-byte logical blocks: (63.8 GB/59.4 GiB)
[20630376.658370] sd 49:0:0:0: [sdd] Write Protect is off
[20630376.658374] sd 49:0:0:0: [sdd] Mode Sense: 03 00 00 00
[20630376.659016] sd 49:0:0:0: [sdd] No Caching mode page found
[20630376.660577] sd 49:0:0:0: [sdd] Assuming drive cache: write through
[20630376.665869]  sdd: sdd1 sdd2
[20630376.668636] sd 49:0:0:0: [sdd] Attached SCSI removable disk
   ```

The above indicates that *sdd* is the device name of the MicroSD card.
The device name on your system most likely will be different, but it will have
the format *sdX*.

Now let's copy *stacki-centos.img* to the MicroSD card.

  ```
  # wget http://stacki.s3.amazonaws.com/public/pallets/4.0/open-source/ace/stacki-centos.img

  # dd if=stacki-centos.img of=/dev/sdd
  ```

* Put the MicroSD card into the Raspberry Pi that will be the frontend and
power on the frontend Pi.

> The frontend Pi will reboot on the first boot, don't be alarmed.
The Pi is automatically resizing your '/' file system to take advantage of
all the free space on your MicroSD card.

* After the Pi boots, login as `root` with the password `stacki-centos`.

> You'll be asked to change your password.

* Copy the Stacki ACE ISOs to the frontend:

  ```
  # wget http://stacki.s3.amazonaws.com/public/pallets/4.0/open-source/ace/os-7.3-7.x.armv7hl.disk1.iso

  # wget http://stacki.s3.amazonaws.com/public/pallets/4.0/open-source/ace/stacki-4.0_20170316-7.x.armv7hl.disk1.iso

  # wget http://stacki.s3.amazonaws.com/public/pallets/4.0/open-source/ace/stacki-ace-4.0_20170328-7.x.armv7hl.disk1.iso
  ```

* Download and execute `frontend-install.py`.

> This will transform the Pi into a Stacki ACE frontend.

  ```
  # wget http://stacki.s3.amazonaws.com/public/pallets/4.0/open-source/ace/frontend-install.py

  # ./frontend-install.py --stacki-iso=stacki-4.0_20170316-7.x.armv7hl.disk1.iso --stacki-version=4.0 --stacki-name=stacki
  ```
The above step will run several commands and will eventually display
the Installation Wizard.

## Installation Wizard

### Timezone

The first screen will appear and you will be prompted to enter your timezone:

<img src="doc/screen-1.png" width="500">

### Network

The network configuration screen allows you to set up the network that will
be used by the frontend to install backend hosts.

1. _Fully Qualified Host Name_ - Input the FQDN for the frontend.
2. Choose from the network _Devices_ to select the frontend's network interface.
3. _IP_ address of the interface.
4. _Netmask_.
5. _Gateway_.
5. _DNS Servers_ - Enter *one* DNS server here.

Click _Continue_ to configure the network interface. 

<img src="doc/screen-2.png" width="500">

### Password

Enter the password for the **root** account on the frontend.  

<img src="doc/screen-3.png" width="500">

### Add Pallets

The `stacki` pallet that you provided as a parameter to `frontend-install.py`
will be automatically selected.

Just click _Continue_.

<img src="doc/screen-4.png" width="500">

### Review

Review the installation parameters and click _Continue_ to proceed.

<img src="doc/screen-5.png" width="500">

> The remainder of the install will take some time and will output a lot of
text.

* After `frontend-install.py` completes, reboot the frontend Pi to complete the
installation.

* After the frontend Pi reboots, login as `root` and add/enable the `os` pallet:

  ```
  # stack add pallet os-7.3-7.x.armv7hl.disk1.iso
  # stack enable pallet os
  ```

* Now add/enable the `stacki-ace` pallet:

  ```
  # stack add pallet stacki-ace-4.0_20170328-7.x.armv7hl.disk1.iso
  # stack enable pallet stacki-ace
  ```

* Your pallet inventory should like this:

  ```
  # stack list pallet
  NAME       VERSION      RELEASE ARCH    OS     BOXES
  stacki     4.0_20170316 7.x     armv7hl redhat default
  os         7.3          7.x     armv7hl redhat default
  stacki-ace 4.0_20170328 7.x     armv7hl redhat default
  ```

* Apply the `stacki-ace` pallet to the frontend:

  ```
  # stack run pallet stacki-ace | bash -x
  ```

* Reboot your frontend Pi 

* After the frontend reboots, your frontend Pi is ready to build backend Pis.

---

# Build Backend(s)

* Create a host configuration spreadsheet.

The spreadsheet will contain the basic networking information for your
backend Pis (known as `ace` appliances).

The Host CSV file needs to have the following columns:

1. **Name**. A hostname.
1. **Appliance**. The appliance name for the host (e.g. backend).
1. **Rack**. The rack number for the host.
1. **Rank**. The position in the rack for the host.
1. **IP**. Network address.
1. **MAC**. Ethernet address.
1. **Interface**. Ethernet device name (e.g. em1).
1. **Network**. Network name for the interface (e.g. private).

Here is a link to a 
[sample spreadsheet](https://docs.google.com/spreadsheets/d/1YC4tlmiMw2YUj3X-2Q47VnAwuyxg2d5zL6mmbBuA29k/edit?usp=sharing).

* Save the spreadsheet as a CSV file (comma-separated values).

* Load the host configuration spreadsheet into your frontend Pi.

Copy the host CSV file to your frontend Pi and execute:

  ```
  # stack load hostfile file=hosts.csv
  ```

* To see the host information, execute:

  ```
  # stack list host
  HOST    RACK RANK CPUS APPLIANCE BOX     ENVIRONMENT RUNACTION INSTALLACTION
  rasp003 0    0    4    frontend  default ----------- os        install      
  rasp004 0    4    1    ace       default ----------- os        install
  ```

In the above output `rasp003` is the frontend Pi and `rasp004` is the
backend Pi.
The appliace type for `rasp004` is **ace** which is th correct appliance type
for a Raspberry Pi backend host.

* Set all the `ace` backend hosts to install:

  ```
  # stack set host boot ace action=install
  ```

* Copy `stacki-centos.img` to the MicroSD card that will be used in the
backend Pi (use the same procedure you used to copy `stacki-centos.img` to
your frontend Pi's MicroSD card).

* Put the MicroSD card into your backend Pi and power it on.

* The frontend Pi will recognize the backend Pi and the frontend will instruct
the backend to install itself.

> This process will take approximately 10 minutes.
When complete, you'll be able to login to the backend via the console or via
*ssh* from the frontend.

* If you have multiple backend Pis, repeat the process of copying
`stacki-centos.img` to the respective backend Pis' MicroSD cards and booting
them -- the frontend Pi will install all backend Pis that are listed in
`stack list host`.

* Enjoy your $35 dollar / host cluster!!

