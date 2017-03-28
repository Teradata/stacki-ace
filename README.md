The best ARM on the team is an ACE.

---

Requirements

# Frontend

* 16 GB of storage

# Backend

* 2 GB of storage

---

# Build Frontend

* Boot Raspberry Pi that will be the frontend with `stacki-centos.img`.

* Login as `root` with the password `stacki-centos`.
** You'll be asked to change your password.

* Increase storage to full capacity:

   ```
   look up command to do this
   ```

* Reboot.

* Set the time:

  ```
  timedatectl set-timezone America/Los_Angeles
  timedatectl set-time '2017-03-14 14:53:00'
  ```

or:

  ```
  timedatectl set-timezone America/Los_Angeles
  ntpdate -s pool.ntp.org
  ```

* Copy ISOs to the frontend:

  ```
  wget os-7.3-7.x.armv7hl.disk1.iso
  wget stacki-4.0_20170316-7.x.armv7hl.disk1.iso
  wget stacki-ace-4.0_20170323-7.x.armv7hl.disk1.iso
  ```

* Apply the ``stacki`` ISO to the frontend.
** This will transform the Pi into a Stacki ACE frontend.

  ```
  wget frontend-install.py
  ```

* Execute `frontend-install.py`:

  ```
  ./frontend-install.py --stacki-iso=stacki-4.0_20170316-7.x.armv7hl.disk1.iso --stacki-version=4.0 --stacki-name=stacki
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

* Reboot the frontend Pi

After `frontend-install.py` completes, reboot the frontend Pi to complete the
installation.

* Add/Enable the `os` pallet:

After the frontend Pi reboots, login as `root` and add/enable the `os` pallet:

  ```
  stack add pallet os-7.3-7.x.armv7hl.disk1.iso
  stack enable pallet os
  ```

* Add/Enable the `stacki-ace` pallet:

  ```
  stack add pallet stacki-ace-4.0_20170321-7.x.armv7hl.disk1.iso
  stack enable pallet stacki-ace
  ```

* Your pallet inventory should like this:

  ```
  # stack list pallet
  NAME       VERSION      RELEASE ARCH    OS     BOXES
  stacki     4.0_20170316 7.x     armv7hl redhat default
  os         7.3          7.x     armv7hl redhat default
  stacki-ace 4.0_20170324 7.x     armv7hl redhat default
  ```

* Apply the `stacki-ace` pallet to the frontend:

  ```
  stack run pallet stacki-ace | bash -x
  ```
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

* Load host configuration spreadsheet.

Copy the host csv file to your frontend Pi and execute:

  ```
  stack load hostfile file=hosts.csv
  ```

** To see the host information, execute:

  ```
  # stack list host
  HOST    RACK RANK CPUS APPLIANCE BOX     ENVIRONMENT RUNACTION INSTALLACTION
  rasp003 0    0    4    frontend  default ----------- os        install      
  rasp004 0    4    1    ace       default ----------- os        install
  ```

In the above output `rasp003` is the frontend Pi and `rasp004` is the
backend Pi.
The appliace type for `rasp004` is **ace** which is correct appliance type
for a Raspberry Pi backend host.

* Set all the `ace` backend nodes to install:

  ```
  stack set host boot ace action=install
  ```

* Copy `stacki-centos.img` to a MicroSD card.

* Boot the backend Pi

* Enjoy your $35 dollar / node cluster!!

