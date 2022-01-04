# ArPiRobot-CameraStreaming

Low latency, real-time camera streaming using a Raspberry Pi.

## Dependencies

- Raspberry Pi OS Buster (32-bit)
- Pi Camera or USB webcam
- Install gstreamer

```sh
sudo apt install libgstreamer1.0-0 gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly gstreamer1.0-libav gstreamer1.0-doc gstreamer1.0-tools gstreamer1.0-x gstreamer1.0-alsa gstreamer1.0-gl gstreamer1.0-omx-rpi-config gstreamer1.0-omx-rpi gstreamer1.0-omx
```

libcamera buster: config.txt (after installing)

```
# In [all] section
dtoverlay=vc4-fkms-v3d
camera_auto_detect=1
```

Otherwise, must use old stack (raspicam). Recommended to increase gpu memory (should be at least 128, but 256 better, but don't use 256 on Pi 3A+)

```
gpu_mem=256
```


## Scripts
TODO

## Playing Stream

- Playing with [mpv](https://mpv.io/) (recommended). Make sure to change the fps argument to match your stream if needed.

```sh
mpv --no-cache --untimed --profile=low-latency -no-correct-pts --fps=30 --osc=no tcp://remote_host:5008
```

- Using ffplay (part of [ffmpeg](https://ffmpeg.org/)). This method may have latency issues (depends on the OS you are using and how the stream from the Pi is created). It is recommended to use this as a fallback if mpv does not work or has latency issues.

```sh
ffplay -probesize 32 -framerate 30 -fflags nobuffer -flags low_delay -framedrop -sync ext tcp://remote_host:5008
```


TODO: mplayer and vlc
