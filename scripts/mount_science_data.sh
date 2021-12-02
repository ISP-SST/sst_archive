#!/usr/bin/env bash

function usage() {
  SCRIPT_NAME=`basename "$0"`
  echo "Usage: "
  echo "${SCRIPT_NAME} TARGET_DIRECTORY"
}

if [ $# -ne 1 ]; then
  usage
  exit 1
fi

MOUNT_DIR=$1

umount "${MOUNT_DIR}"
sshfs -o allow_other,ro,IdentityFile=~/.ssh/id_rsa dubshen:/storage/science_data "${MOUNT_DIR}"

