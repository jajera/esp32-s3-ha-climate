# 3. Wire and validate

Build the circuit on a breadboard, one step at a time. Each page ends with a **checkpoint**. Pass it before moving on, so a bad wire shows up early instead of after you flash.

!!! warning "3V3 only, and unplug while you wire"
    Power the SHT40 and the display from **3V3**. 5V on the logic pins can kill the modules. Unplug USB while you seat jumpers.

## The routine

Steps 2 to 4 all follow the same loop:

```mermaid
flowchart LR
  A[Unplug USB] --> B[Seat the jumpers] --> C[Plug into COM] --> D["Check: cool,<br/>about 3.3 V"] --> E[Checkpoint passed]
```

If anything is warm or the meter reads wrong, unplug and go back to the wires before you continue.

## Parts

| | Part | Notes |
|---|------|-------|
| :lucide-cpu: | ESP32-S3 DevKitC-1 class | Dual Type-C **N16R8** |
| :lucide-thermometer: | SHT40 breakout | I2C at `0x44` |
| :lucide-monitor: | ST7789 **240×240** SPI display | Square IPS, 8-pin header (`GND` to `BL`) |
| :lucide-grid-3x3: | Solderless breadboard | 400 or 830 holes, half or full size |
| :lucide-cable: | DuPont M–M jumpers | Board to rail, board to board |
| :lucide-usb: | USB-C **data** cable | Charge-only cables never show a serial port |

## Steps

<div class="grid cards" markdown>

- :lucide-grid-3x3: **[1. Breadboard](breadboard.md)**

    How the holes are already tied.

- :lucide-cpu: **[2. ESP32](esp32.md)**

    Board on the breadboard, 3V3 and GND on the rails.

- :lucide-thermometer: **[3. SHT40](sht40.md)**

    Power, then I2C.

- :lucide-monitor: **[4. Display](display.md)**

    Power, then SPI.

- :lucide-circle-check: **[5. Validate](validate.md)**

    The full pin map and a USB check.

</div>

The full pin map is on [Validate](validate.md) once everything is wired.
