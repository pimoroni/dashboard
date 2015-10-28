#Pimstaller

A Python-based library and example installer for Raspberry Pi add-on boards.

#How to use

Just type:

```bash
./pimstaller
```

To see a list of available boards. And:

```bash
./pimstaller board_name
```

To install!

#Reinstalling

If you need to reinstall the Python libraries, you can use:

```bash
./pimstaller board_name --reinstall
```

#Adding your boards

Board files are retrieved from GitHub: https://github.com/gadgetoid/Pinout2

Example: https://raw.githubusercontent.com/Gadgetoid/Pinout2/master/src/en-GB/overlay/display-o-tron.md

```yaml
---
name: Display-o-Tron 3000
manufacturer: Pimoroni
github: https://github.com/pimoroni/dot3k
url: https://github.com/pimoroni/dot3k
description: A 3-line character LCD with an RGB backlight and joystick
install:
  'devices':
    - 'i2c'
    - 'spi'
  'apt':
    - 'python-smbus'
    - 'python3-smbus'
    - 'python-dev'
    - 'python3-dev'
  'python':
    - 'dot3k'
  'examples': 'python/examples/'
```

The `name`, `github` and `install` data is required to make a valid, installable file, but everything else should be specified in order to make a pretty board definition for Pinout: http://pi.gadgetoid.com/pinout
