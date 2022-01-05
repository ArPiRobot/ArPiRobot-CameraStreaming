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


cp arpirobot-camstream.sh /usr/local/bin
cp stream.py /usr/local/bin/
chmod 755 /usr/local/bin/arpirobot-camerastream.sh
chmod 755 /usr/local/bin/stream.py

systemctl stop camerastream.service
cp camerastream.service /lib/systemd/system/
systemctl daemon-reload


popd > /dev/null
