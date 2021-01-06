# HEOS-REMOTE 

`Heos-remote` is a hobby project aimed at building physical remote control for Denon's HEOS-powered multi-room speakers systems. This allows you to pass simple commands to your speaker system without having to go through the hassle of finding your phone and starting the app.

## Overall setup

The overall idea is to use a Bluetooth remote (such as https://satechi.net/products/satechi-bluetooth-multi-media-remote) to control our speaker system. We'll connect this remote to our speaker using a small computer such as the Raspberry PI Zero W. This Raspberry PI will then respond to key presses on the remote and relay the appropriate commands to the speaker(s).

As such, the overall setup is as follows:  

```
Bluetooth remote --> Raspberry PI -> HEOS speaker(s)
```

Although some guidelines are provided below, you'll be responsible for setting up + configuring the RaspberryPI yourself. Once this setup has been done, the Python library from this repository can be used for installing + running the remote software.

## Getting started

### Pairing the remote

To get started with Bluetooth in the terminal, access Bluetooth control:

```
sudo bluetoothctl
```

Next, turn Bluetooth on and scan for devices to pair with:

```
agent-on
default-agent
scan on
```

This will bring up a list of all of the detected Bluetooth devices with their ID codes (format: XX:XX:XX:XX:XX:XX).
 
If your device is discoverable or in pairing mode, you should see name of the device appear. To now pair with the device use:

```
pair XX:XX:XX:XX:XX:XX
```

Once paired, test the connection with the device using:

```
connect XX:XX:XX:XX:XX:XX
```

After connecting, you should see the Bluetooth device inputs show up under `/dev/input` (e.g. `/dev/input/event0`, `/dev/input/event1`).

### Installing the heos-remote library

Before installing the remote library, you need to install the supporting `heos` API library, which is used to relay commands to the speakers:

```
pip install git+https://github.com/jrderuiter/heos.git
```

Afterwards, you can install the `heos-remote` library using:

```
pip install git+https://github.com/jrderuiter/heos-remote.git
```

### Running the remote manually

The `heos-remote` command can be used to run the remote software for a specific HEOS player: 

```
heos-remote player --name Lounge --device /dev/input/event0 --device /dev/input/event1
```

or a specific player group:

```
heos-remote group --name Downstairs --device /dev/input/event0 --device /dev/input/event1
```

The `--name` argument should point to a player/group in your HEOS setup. Make sure to surround the name in quotes if the name contains spaces.

The `--device` argument specifies to which input devices the remote should be listening for events. You should have identified these device paths in the previous step.

### Running the remote on boot

You can automatically start the remote on boot by registering a systemd service. 

To do so:

1. Copy over the systemd/heos-remote.service file to `/etc/systemd/system/`.
2. Modify the service contents to point to the correct executable (if needed) and adjust the names of the speakers + devices.
3. Enable and start the service using:

```
sudo systemctl daemon-reload
sudo systemctl enable heos-remote
sudo service start heos-remote
```

You can check on the status of the service using:

```
sudo systemctl status heos-remote
```

If needed, you can check the logs of the service to diagnose any errors using:

```
sudo journalctl -u heos-remote
```

## Wishlist

* Make mappings of keycodes -> commands configurable.
* Add utility command for identifying keycodes corresponding to specific buttons.
* Add support for presets linking to playlists, radio stations etc.

## Contributing 

Contributions are welcome, and they are greatly appreciated! Every little bit helps, and credit will always be given.

You can contribute in many ways:

### Report Bugs

Report bugs at https://github.com/jrderuiter/heos-remote/issues.

If you are reporting a bug, please include:

* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

### Fix Bugs

Look through the GitHub issues for bugs. Anything tagged with "bug" and "help wanted" is open to whoever wants to implement it.

### Implement Features

Look through the GitHub issues for features. Anything tagged with "enhancement" and "help wanted" is open to whoever wants to implement it.

### Write Documentation

We  could always use more documentation, whether as part of the official docs, in docstrings, or even on the web in blog posts, articles, and such.

### Submit Feedback

The best way to send feedback is to file an issue at https://github.com/jrderuiter/heos-remote/issues.

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions
  are welcome :)
