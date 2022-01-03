# ArPiRobot-CameraStreaming

Low latency, real-time camera streaming using a Raspberry Pi.

## Dependencies

- Raspberry Pi OS Buster (32-bit)
- Pi Camera or USB webcam
- Install gstreamer

```sh
sudo apt install libgstreamer1.0-0 gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly gstreamer1.0-libav gstreamer1.0-doc gstreamer1.0-tools gstreamer1.0-x gstreamer1.0-alsa gstreamer1.0-gl gstreamer1.0-omx-rpi-config gstreamer1.0-omx-rpi gstreamer1.0-omx
```


## Scripts
TODO

## Playing Stream

- Install ffmpeg and run one of the following commands

```
ffplay -fflags nobuffer -flags low_delay -framedrop -sync ext tcp://remote_host:5008

ffplay -fflags nobuffer -flags low_delay -framedrop -sync ext udp://localhost:5008

# Add -probesize 32 to reduce startup time
```

TODO: mpv, mplayer, and vlc
