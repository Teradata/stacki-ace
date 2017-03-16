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

* Copy ISOs to the frontend:

  ```
  wget CentOS-7-7.x.armv7hl.disk1.iso
  wget CentOS-kernel-rpi2-7-7.x.armv7hl.disk1.iso
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

* Load host configuration spreadsheet.

---

# Build Backend

* Copy `stacki-centos.img` to a micro SD card.

* Boot the backend once.

** This will configure the boot loader to enable booting from the on-board
ethernet device

* Remove /boot/bootcode.bin

** This ensures that the Pi *won't* boot from the micro SD card and that it
will boot from the network.

* Reboot the backend Pi

