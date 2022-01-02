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
# script:      start_h264_libx264.sh
# description: Starts an H.264 stream using the libx264 software encoder
#              Configured to minimize latency, however will not be as good as a hardware accelerated
#              method. Also requires considerable CPU time and may have issues with higher 
#              framerates.
# author:      Marcus Behel
# date:        1-2-2022
# version:     v1.0.0
####################################################################################################

DIR=$(realpath $(dirname $0))

source "$DIR"/config.sh

gst-launch-1.0 v4l2src device=${VIDEO_DEVICE} ! \
    video/x-raw,width=${VIDEO_WIDTH},height=${VIDEO_HEIGHT},framerate=${VIDEO_FRAMERATE}/1 ! \
    x264enc tune=zerolatency speed-preset=ultrafast ! mpegtsmux ! $SINK

exit $?