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

*H.264 will be lower bandwidth streams (higher resolutions and FPS supported), but can be higher latency or require more CPU time to encoder the data (depends on the system). MJPEG is often lower latency and easier to encoder, but will require more bandwidth for the same resolution and framerate compared to H.264 encoded streams.*

- `start_h264_native.sh`: Starts an H.264 stream using H.264 frames directly from a camera that natively supports H.264 output. The Pi Camera supports H.264 natively, but many cameras do not.
- `start_h264_omx.sh`: Starts an H.264 stream using the hardware accelerated OpenMax encoder available on the Raspberry Pi. This will often be similar in performance to the "native" H.264 method.
- `start_h264_libx264.sh`: Starts an H.264 stream using software encoding (libx264 library). This script configures libx264 in such a way to minimize latency, however it will likely still be higher than a hardware accelerated method. This encoding method will also require a considerable amount of CPU time on lower power devices. Higher framerates and resolutions will require more CPU time and add more latency to the stream using this method.

- `start_mjpeg_native.sh`: Uses JPEG frames from the camera to create an MJPEG stream. The camera must support JPEG frames natively. It is often better to encode on the Pi, however, as it gives more control over quality / size and thus bandwidth.
- `start_mjpeg_jpegenc.sh`: Uses software JPEG encoder on the Pi to encode JPEG images to create an MJPEG stream. Gives control of image quality and often allows better latency and framerates on the streamed video.


## Playing Stream

- Install ffmpeg and run one of the following commands

```
ffplay -fflags nobuffer -flags low_delay -framedrop -sync ext tcp://remote_host:5008

ffplay -fflags nobuffer -flags low_delay -framedrop -sync ext udp://localhost:5008

# Add -probesize 32 to reduce startup time
```

TODO: mpv, mplayer, and vlc
