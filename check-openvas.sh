#!/bin/bash
## Script by AfterBurn @ NetSecNow GNU License
echo -e "Script by AfterBurn @ NetSecNow.\n"
##Setting up nvt sync
echo "Syncing NVT Database..."
openvas-nvt-sync
echo "Updating SCAP Data Feed"
openvas-scapdata-sync
echo "Updating CERT Feed.."
openvas-certdata-sync
## Starting Services
echo "Starting OpenVAS Services..."
/etc/init.d/./greenbone-security-assistant start
/etc/init.d/./openvas-scanner start
/etc/init.d/./openvas-administrator start
/etc/init.d/./openvas-manager start
openvas-start
openvassd
openvasmd
gsad