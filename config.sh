#!/usr/bin/env bash
####################################################################################################
#
# Copyright 2022 Marcus Behel
#
# This file is part of ArPiRobot-ImageScripts.
# 
# ArPiRobot-ImageScripts is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# ArPiRobot-ImageScripts is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
# 
# You should have received a copy of the GNU Lesser General Public License
# along with ArPiRobot-ImageScripts.  If not, see <https://www.gnu.org/licenses/>.
####################################################################################################
# script:      config.sh
# description: Settings used by all start scripts for camera streaming
# author:      Marcus Behel
# date:        1-2-2022
# version:     v1.0.0
####################################################################################################

VIDEO_DEVICE=/dev/video0
VIDEO_WIDTH=640
VIDEO_HEIGHT=480
VIDEO_FRAMERATE=60

NET_MODE=tcp
IP_ADDRESS=0.0.0.0
PORT=5008


if [ "$NET_MODE" == "tcp" ]; then
    SINK="tcpserversink host=${IP_ADDRESS} port=${PORT}"
elif [ "$NET_MODE" == "udp" ]; then
    SINK="udpsink host=${IP_ADDRESS} port=${PORT}"
elif [ "$NET_MODE" == "udp-multicast" ]; then
    SINK="udpsink host=${IP_ADDRESS} auto-multicast=true port=${PORT}"
else
    echo "Invalid net mode!"
    exit 1
fi
