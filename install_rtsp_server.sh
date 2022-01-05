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
# script:      install_rtsp_server.sh
# description: Install rtsp server for use with camera streaming. 
#              Includes installation of a service to start it.
#              ONLY WORKS ON 32-bit RPI IMAGES!!! CHANGE DOWNLOAD FOR OTHER SYSTEMS!
# author:      Marcus Behel
# version:     v1.0.0
#####################################################################################

DIR=$(realpath $(dirname $0))

if ! [ $(id -u) = 0 ]; then
   echo "This script must be run as root."
   exit 1
fi

pushd /home/pi > /dev/null

mkdir -p rtsp-simple-server/
chown pi:pi rtsp-simple-server/
cd rtsp-simple-server/

wget https://github.com/aler9/rtsp-simple-server/releases/download/v0.17.13/rtsp-simple-server_v0.17.13_linux_armv6.tar.gz
tar -xzvf rtsp-simple-server_v0.17.13_linux_armv6.tar.gz
rm rtsp-simple-server_v0.17.13_linux_armv6.tar.gz
chown pi:pi ./*


popd > /dev/null

pushd "$DIR" > /dev/null


systemctl stop rtsp-simple-server.service
rm /lib/systemd/system/rtsp-simple-server.service
cp rtsp-simple-server.service /lib/systemd/system/
systemctl daemon-reload
systemctl enable rtsp-simple-server.service
systemctl start rtsp-simple-server.service


popd > /dev/null
