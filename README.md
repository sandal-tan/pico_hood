# A Micropython Port of the `Fume_Hood` for the Raspberry Pi Pico

## Usage

Install the environment with [poetry][1]:

```bash
% poetry install
```

Once the Pico is plugged in and configured to run Micropython, you can install the `pico_hood` package with:

```bash
% DEVICE=... make install
```

`DEVICE` should refer to the USB device referencing the Pico. On Mac OS, this is something like `/dev/cu.usbmodemxxyyzz`
