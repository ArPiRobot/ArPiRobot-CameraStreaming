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


################################################################################
# Video Device Settings
# ------------------------------------------------------------------------------
# VIDEO_DEVICE    = Device to capture video from
#                
# VIDEO_WIDTH     = Width of frames (must be supported in the given input mode)
#                   v4l2-ctl -d /dev/video# --list-formats
# VIDEO_HEIGHT    = Height of frames (must be supported in the given input mode)
#                   v4l2-ctl -d /dev/video# --list-formats
# VIDEO_FRAMERATE = Capture framerate (must be supported in given input mode)
#                   v4l2-ctl -d /dev/video# --list-formats
# V4L2_IOMODE     = Usually, auto. If latency issues with USB camera try dmabuf
################################################################################

VIDEO_DEVICE=/dev/video0
VIDEO_WIDTH=640
VIDEO_HEIGHT=480
VIDEO_FRAMERATE=60

V4L2_IOMODE=auto

# All cameras should support these
BRIGHTNESS=50                   # 0 to 100
CONTRAST=0                      # -100 to 100
SATURATION=0                    # -100 to 100
VFLIP=1                         # 0 = false, 1 = true
HFLIP=0                         # 0 = false, 1 = true
ROTATION=0                      # 0, 90, 180, 270, 360

# Pi Camera specific
EXPOSURE_TIME=5000              # 1-10000
ISO_SENSITIVITY=0               # 0-4

################################################################################
# Network Settings
# ------------------------------------------------------------------------------
# TCP Mode (NET_MODE=tcp)
#     IP_ADDRESS = Which of this device's IP addresses the server should 
#                  be accessible on. 0.0.0.0 for all IP addresses.
#     PORT       = TCP port to use for the server
# 
# UDP Unicast Mode (NET_MODE=udp)
#     IP_ADDRESS = Address of the device to send UDP packets to.
#     PORT       = Port to send UDP packets to
# 
# UDP Multicast Mode (NET_MODE=udp-multicast)
#     IP_ADDRESS = Multicast IP address for the current network
#     PORT       = Port to send packets to
################################################################################

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


# Apply general camera settings using v4l2-ctl
{
    v4l2-ctl -d $VIDEO_DEVICE -c brightness=$BRIGHTNESS
    v4l2-ctl -d $VIDEO_DEVICE -c contrast=$CONTRAST
    v4l2-ctl -d $VIDEO_DEVICE -c saturation=$SATURATION
    v4l2-ctl -d $VIDEO_DEVICE -c vertical_flip=$VFLIP
    v4l2-ctl -d $VIDEO_DEVICE -c horizontal_flip=$HFLIP
    v4l2-ctl -d $VIDEO_DEVICE -c rotate=$ROTATION

    v4l2-ctl -d $VIDEO_DEVICE -c exposure_time_absolute=$EXPOSURE_TIME
    v4l2-ctl -d $VIDEO_DEVICE -c iso_sensitivity=$ISO_SENSITIVITY
} > /dev/null 2>&1