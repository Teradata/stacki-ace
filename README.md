The best ARM on the team is an ACE.

---

Requirements

# Frontend

* 16 GB of storage

# Backend

* 4 GB of storage

---

# Build Frontend

* Boot Raspberry Pi that will be the frontend with `stacki-centos.img`.

* Login as `root` with the password `stacki-centos`.

* Change your root password:

  ```
  passwd
  ```

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
  ntpdate -s 3.us.pool.ntp.org
  ```

* Copy ISOs to the frontend:

  ```
  wget CentOS-7-7.x.armv7hl.disk1.iso
  wget CentOS-kernel-rpi2-7-7.x.armv7hl.disk1.iso
  wget CentOS-updates-7-7.x.armv7hl.disk1.iso
  wget stacki-4.0_20170208-7.x.armv7hl.disk1.iso
  ```

* Apply the ``stacki`` ISO to the frontend.
** This will transform the Pi into a Stacki ACE frontend.

  ```
  cp frontend-install.py /tmp/ 
  ```

* Execute `frontend-install.py`:

  ```
  /tmp/frontend-install.py --stacki-iso=/export/stacki-4.0_20170208-7.x.armv7hl.disk1.iso --stacki-version=4.0 --stacki-name=stacki
  ```

* Reboot the frontend Pi

* Add/Enable the CentOS pallets:

  ```
  stack add pallet CentOS-7-7.x.armv7hl.disk1.iso
  stack add pallet CentOS-updates-7-7.x.armv7hl.disk1.iso
  stack add pallet CentOS-kernel-rpi2-7-7.x.armv7hl.disk1.iso
  stack enable pallet CentOS CentOS-updates CentOS-kernel-rpi2
  ```

* Add/Enable the `stacki-ace` pallet:

  ```
  stack add pallet stacki-ace-4.0_20170321-7.x.armv7hl.disk1.iso
  stack enable pallet stacki-ace
  ```

* Apply the `stacki-ace` pallet to the frontend:

  ```
  stack run pallet stacki-ace | bash -x
  ```

* Load host configuration spreadsheet.

  ```
  stack load hostfile file=hosts.csv
  ```

* Set `ace` nodes to install:

  ```
  stack set host boot ace action=install
  ```

---

# Build Backend(s)

* Copy `stacki-centos.img` to a micro SD card.

* Boot the backend Pi

