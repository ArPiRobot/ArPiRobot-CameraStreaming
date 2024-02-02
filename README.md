# ArPiRobot-CameraStreaming

Low latency, real-time camera streaming using a Raspberry Pi.


## Requirements & Setup

- Tested on raspberry Pi OS  (v4l2src and x264enc should work on any linux system)
- Pi Camera or USB webcam
- Install gstreamer
    - Run

        ```sh
        sudo apt install libgstreamer1.0-0 gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly gstreamer1.0-rtsp gstreamer1.0-libav gstreamer1.0-tools gstreamer1.0-x gstreamer1.0-alsa gstreamer1.0-gl
        ```

## Starting a Stream

All streams are started using the `camstream.py` script. This script can start a stream using one of several drivers and allows for many different configuration options. Many of these options are hardware specific and will not work with all cameras. The available options all work with the Pi camera modules when using `libcamera` (though not necessarily using `v4l2`).

The most commonly used options are used to adjust the video resolution and framerate, the format of the stream, or which camera stack is used. The camera stack is selected using the `--driver` flag, resolution is selected using the `--width` and `--height` flags, framerate is controlled using the `--framerate` flag, and the format is controlled using the `--format` flag. 

The driver can be one of `libcamera` or `v4l2`. The is a camera stacks specific to raspberry pi camera modules and do not support USB webcams. Video for Linux v2 (v4l2) supports USB webcams.

When setting the resolution and framerate, make sure you choose a resolution and framerate supported by your camera. Most cameras support a finite number of resolutions and the maximum supported framerate will depend on the resolution. These settings are camera specific and usually found in the device's datasheet. You can also use `v4l2-ctl -d /dev/video0 --list-formats-ext` for USB webcams. Most cameras will likely support 640x480 at 30FPS (often at 60FPS). An HD camera should support 1280x720 at 30FPS (often 60FPS) and a 1080P camera should support 1920x1080 at 30FPS. Choosing one of these modes will often work.

The format of the stream can either be `mjpeg` or `h264`. The `h264` codec encodes changes between frames, and thus often results in smaller sizes or lower bandwidth. When streaming from a camera, this means that you will often be able to reduce bandwidth usage compared to `mjpeg` (or you could have higher resolutions or framerates for the same bandwidth usage). In contrast, `mjpeg` is a stream of jpeg compressed images (each frame is one image). As such, more bandwidth is required, however encoding and decoding `mjpeg` streams is much simpler. As such, it can reduce latency in the stream compared to `h264`. In practice, however, this is often not an issue as many systems support hardware accelerated `h264` encoding and decoding now.

The following are a few examples of starting and customizing streams. Additional options are available. See the table below for details.

```sh
# Start a H.264 stream with a resolution of 640x480 at 30fps using the libcamera stack (pi camera only, no usb camera)
./camstream.py --driver libcamera --width 640 --height 480 --framerate 30 --format h264

# Adjust quality (and bandwidth usage) with the bandwidth flag (indicates a target bandwidth in bits/sec)
./camstream.py --driver libcamera --width 640 --heigh 480 --framerate 30 --format h264 --bitrate 2048000


# Start a MJPEG stream with a resolution of 1280x720 at 30fps using the raspicam stack (pi camera only, no usb camera)
./camstream.py --driver libcamera --width 1280 --height 720 --framerate 30 --format mjpeg

# To reduce bandwidth usage with MJPEG, use the quality flag (or with raspicam use bandwidth flag)
# Quality from 1 to 100. Also works for v4l2 driver.
./camstream.py --driver libcamera --width 1280 --height 720 --framerate 30 --format mjpeg --quality 30

# Use v4l2 driver with a USB webcam. libcamera only support Pi camera modules
# Also have to specify which device v4l2 should use (--device argument)
# If you have latency issues with a USB webcam, you can try --iomode dmabuf also (iomode only supported with v4l2)
# List v4l2 devices with "v4l2-ctl --list-devices"
./camstream.py --driver v4l2 --device /dev/video0 --width 1280 --height 720 --format h264


# Any settings you do not specify take default values. As such even something as simple as no argument is allowed
# However, there are some arguments you will typically want to provide
# Starts a 640x480 stream at 30FPS using libcamera. Format is h264 with a bitrate of 2048000
./camstream.py
```

Any stream can also be used with a different networking mode. Three networking modes are available: tcp, udp, and rtsp. TCP runs a TCP server on the Pi that clients connect to to play the stream. UDP mode sends the stream to a single, designated IP address and port. RTSP sends the stream to an RTSP server running on the Pi (this is not handled by this script, another piece of software such as [rtsp-simple-server](https://github.com/aler9/rtsp-simple-server)). Multiple clients can then connect to this server to play the stream.

In TCP mode, the IP address is the address (of the Pi) to run the server on. `0.0.0.0` can be used to run the server on all of the Pi's IP addresses. In UDP mode, the address is the IP address of the device to send the stream to. In RTSP mode, the address is the address of the rtsp server (typically, the rtsp server runs on the Pi, so the address is `localhost`). The port is either the port to run a TCP server on, the port to send UDP data to, or the port the RTSP server is running on.

TCP and UDP are easier to use than RTSP (as an rtsp server is not required), but each have drawbacks. TCP ensures packet delivery and order, which means that older frames must be sent before newer frames. This can cause significant latency with poor network connections. UDP does not ensure packet delivery or order, but the IP address of the client must be known by the Pi and only one client can play the stream easily. Because packet delivery is not gaurenteed, on low quality connections, the newest frame will always be displayed (but frames can be lost). RTSP can use either TCP or UDP as a transport and does not introduce much latency. Additionally, it acts as a server that allows clients to connect to the Pi. Either UDP or TCP can be used as a transport allowing the advantages of UDP on low quality connections.

The network mode is controlled with the `--netmode` flag and the address and port are adjusted using `--address` and `--port`. Any above example can be modified to use udp or rtsp using these options. For example, if you run `rtsp-simple-server` on the Pi use the following

```sh
# H.264
./camstream.py --driver libcamera --width 640 --height 480 --framerate 30 --format h264 --netmode rtsp --address localhost --port 8554

# MJPEG
./camstream.py --driver libcamera --width 640 --height 480 --framerate 30 --format mjpeg --netmode rtsp --address localhost --port 8554
```

With RTSP, you can also have multiple streams on the same server. Each stream has it's own path on the server, which can be set using the `--rtspkey` flag. For example, the following command results in a stream on the server at the path `rtsp://server_address:server_port/my_stream_key

```sh
./camstream.py --driver libcamera --width 640 --height 480 --framerate 30 --format mjpeg --netmode rtsp --address localhost --port 8554 --rtspkey my_stream_key
```

All Available options:


## Starting a Stream at Boot

This repo includes a service and install script that can be used to configure one or more streams to launch at boot. After running `sudo ./install.sh` the service will be installed and two scripts will be placed in `/usr/local/bin`. These scripts are `camstream-launch.sh`, which is used by the installed service, and the actual `camstream.py` script used to launch the camera streams. In addition, `default.txt` will be copied to the `/home/pi/camstream` folder. 

By default, the installed service is disabled (meaning it will not run at boot), but can be enabled with `sudo systemctl start camstream.service`. To enable the service so it starts automatically at boot, run `sudo systemctl enable camstream.service`. 

When the service starts, it will run `camstream-launch.sh`. This script will read any file in `/home/pi/camstream` ending in `.txt` and use it to launch a camera stream. As such, you should not place other files in `/home/pi/camstream` that end with `.txt`. You can, however, place multiple `.txt` files there to run multiple camera streams.

Each config file (`.txt` file in `/home/pi/camstream/`) is a set of arguments to be passed to the `camstream.py` script to start a stream. As with the command, you do not have to explicitly set every option. Any options not explicitly set will use their default values.


## Playing the Stream

#### Play Stream Script (recommended)

The `playstream.py` script can be used to launch one of the tools mentioned below to play a stream. The tools must be installed separately and be in the system path. On Linux systems, all three players should be available using the system's package manager. On Windows or macOS, they can be downloaded and installed (or sometimes you have to download a zip, and extract it), but you may have to add commands to your path. Alternatively, ffmpeg (includes ffplay) and mpv should be available using the [scoop](https://scoop.sh/) package manager for windows or the [homebrew](https://brew.sh/) package manager for macOS.

Once the player you will use is installed use the following command to play the stream (on windows, you cannot run the script directly, instead use `python playstream.py` or `python3 playstream.py` depending on how you installed python).

```sh
./playstream.py --player ffplay --netmode rtsp --address 192.168.10.1 --port 8554 --rtspkey stream
```

There are several options that can be changed to use different players or handle different types of streams.

| Option / flag | Default Value | Possible Values            | Description                                                               |
| ------------- | ------------- | -------------------------- | ------------------------------------------------------------------------- |
| --netmode     | tcp           | tcp, udp, rtsp             | Which network mode the stream is using. |
| --address     | 127.0.0.1 for udp, else 192.168.10.1 | strings | Address to stream from. For TCP and RTSP this is the address of the Pi (running a TCP or RTSP server). For UDP this is generally localhost or 127.0.0.1 |
| --port        | 8554 for rtsp, else 5008 | integers        | Which port to stream from. For TCP and RTSP this is the server's port. For UDP this is the port data is being sent to. |
| --rtspkey     | stream        | strings                    | Path on the RTSP server of the stream. Only applies in rtsp mode. |
| --format      | auto          | auto, h264, mjpeg          | Some players can detect the stream format. In these cases, auto can be used. Otherwise you can specify either h264 or mjpeg. |
| --player      | auto          | auto, ffplay, mpv, mplayer | Which player to use. If auto, the first detected player on the system is used. Players are searched for in the following order: ffplay, mpv, mplayer. |
| --framerate   | 60            | integers                   | Framerate of the stream. Generally, it is recommended to use twice the actual framerate of the stream to reduce latency. |


#### Manual Method

There are several tools that can be used for playing the stream. They are listed below with information about the tool and the pros and cons of the tool. Recommended commands with each tool are provided below the table. 

| Tool                    | Recommended For           | Notes (based on my testing)                                                                  |
| ----------------------- | ------------------------- | -------------------------------------------------------------------------------------------- |
| [ffmpeg](https://ffmpeg.org/)'s ffplay       | MJPEG or H.264            | Works well for either mjpeg or h264, but often less performant than mpv for h264. Consistent performance across platforms. |
| [mpv](https://mpv.io/)                 | H.264                     | Very performant player capable of using many different types of h264 hardware accelerated decoding. Unfortunately, seems to be incapable of playing mjpeg streams. |
| [mplayer](http://www.mplayerhq.hu/design7/dload.html)             |                           | Plays both h264 and mjpeg decently, but inconsistent at times across platforms. |

Custom gstreamer pipelines could also be setup, but it is generally more complex to actually setup.

The following are recommendations for using each tool to play streams from the Pi. These recommended commands include many flags to reduce playback latency. Specifically what is done depends on the tool, but generally speaking any form of buffering is disabled and the *playback framerate is set to a value higher than the stream's framerate*. Generally, when playing a video it should play at a constant rate to avoid having playback too fast or too slow however, in the case of a realtime stream the newest frame should always be displayed. Configuring the player to play the stream faster than the frames come from the stream help acheive this goal. Generally, using a playback framerate twice that of the stream framerate produces good results.

Additionally, there are other parts of many players that introduce latency. These have been disabled when possible in the commands given below the table.

In each command the IP address of the Pi must be specified. In the commands, `remote_host` is used. Replace this with the IP address of the Pi.

#### ffplay

```sh
# TCP MJPEG or H264
ffplay -probesize 32 -framerate 60 -fflags nobuffer -flags low_delay -framedrop -sync ext tcp://remote_host:5008

# UDP MJPEG or H264
ffplay -probesize 32 -framerate 60 -fflags nobuffer -flags low_delay -framedrop -sync ext udp://localhost:5008

# RTSP MJPEG or H264 (framerate option not needed)
ffplay -probesize 32 -fflags nobuffer -flags low_delay -framedrop -sync ext rtsp://remote_host:8554/stream
```

#### mpv

```sh
# TCP H264, MJPEG add --demuxer-lavf-probescore=10
mpv --no-cache --untimed --profile=low-latency -no-correct-pts --fps=60 --osc=no tcp://remote_host:5008

# UDP H264, MJPEG add --demuxer-lavf-probescore=10
mpv --no-cache --untimed --profile=low-latency -no-correct-pts --fps=60 --osc=no udp://localhost:5008

# RTSP H264 and MJPEG. Often don't need --demuxer-lavf-probescore=10 for MJPEG
mpv --no-cache --untimed --profile=low-latency -no-correct-pts --fps=60 --osc=no rtsp://remote_host:8554/stream
```


#### mplayer

```sh
# TCP, MJPEG
mplayer -benchmark -nocache -fps 60 -demuxer lavf ffmpeg://tcp://remote_host:5008

# UDP, MJPEG

mplayer -benchmark -nocache -fps 60 -demuxer lavf ffmpeg://udp://localhost:5008

# RTSP, MJPEG
mplayer -benchmark -nocache -fps 60 -demuxer lavf rtsp://remote_host:8554/stream

# TCP, H264
mplayer -benchmark -nocache -fps 60 -demuxer h264es ffmpeg://tcp://remote_host:5008

# UDP, H264

mplayer -benchmark -nocache -fps 60 -demuxer h264es ffmpeg://udp://localhost:5008

# RTSP, H264
mplayer -benchmark -nocache -fps 60 -demuxer h264es rtsp://remote_host:8554/stream
```
