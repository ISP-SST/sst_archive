#!/usr/bin/env sh

sshfs -o allow_other,ro,IdentityFile=/Users/dani2978/.ssh/id_rsa dubshen:/storage/science_data /Users/dani2978/Mounted/science_data

