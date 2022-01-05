#!/usr/bin/env bash
#####################################################################################
#
# Copyright 2020 Marcus Behel
#
# This file is part of ArPiRobot-CameraStreaming.
# 
# ArPiRobot-CameraStreaming is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# ArPiRobot-CameraStreaming is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
# 
# You should have received a copy of the GNU Lesser General Public License
# along with ArPiRobot-CameraStreaming.  If not, see <https://www.gnu.org/licenses/>.
#####################################################################################
# script:      install.sh
# description: Install camera streaming service and scripts to the system.
# author:      Marcus Behel
# version:     v1.0.0
#####################################################################################

DIR=$(realpath $(dirname $0))

if ! [ $(id -u) = 0 ]; then
   echo "This script must be run as root."
   exit 1
fi

pushd $DIR > /dev/null


cp camstream-launch.sh /usr/local/bin/
cp camstream.py /usr/local/bin/
chmod 755 /usr/local/bin/camstream-launch.sh
chmod 755 /usr/local/bin/camstream.py

mkdir -p /home/pi/camstream
chown pi:pi /home/pi/camstream
cp default.txt /home/pi/camstream
chown pi:pi /home/pi/camstream/default.txt

systemctl stop camstream.service
rm /lib/systemd/system/camstream.service
cp camstream.service /lib/systemd/system/
systemctl daemon-reload


popd > /dev/null
