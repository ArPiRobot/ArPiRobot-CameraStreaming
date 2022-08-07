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
# script:      arpirobot-camerastream.sh
# description: Start camera streaming for one or more cameras by loading flags 
#              from a file
# author:      Marcus Behel
# version:     v1.0.0
#####################################################################################


# Kill forked processes on exit
trap 'kill $(jobs -p)' EXIT


CONFIGS=/home/USERNAME_HERE/camstream/*.txt
for c in $CONFIGS
do
    arguments=`cat $c | sed ':a;N;$!ba;s/\n/ /g'`
    /usr/local/bin/camstream.py $arguments &
done

echo "Streams running. Press Ctrl+C to kill all."

wait

