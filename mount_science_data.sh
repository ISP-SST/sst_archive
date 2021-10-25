#!/usr/bin/env sh

MOUNT_DIR=/Users/dani2978/Mounted/science_data

umount "${MOUNT_DIR}"
sshfs -o allow_other,ro,IdentityFile=/Users/dani2978/.ssh/id_rsa dubshen:/storage/science_data "${MOUNT_DIR}"

