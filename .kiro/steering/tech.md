---
inclusion: always
---

# Tech

Ubuntu 24.04, Python 3.14 (`/usr/bin/python3.14`; ESPHome supports 3.12–3.14). Docs: Zensical + patina. Firmware: ESPHome for ESP32-S3 N16R8 (16 MB flash, 8 MB octal PSRAM).

Flash through the **COM** USB-C port (CH343 → `/dev/ttyACM0`).

Pins:

- I2C: SDA **8**, SCL **18** (SHT40 at **0x44**)
- SPI display: SCK **12**, MOSI **11**, CS **10**, DC **9**, RST **7**, backlight **21**
- GPIO0 (BOOT): factory reset long-press, so don't wire anything to it
- Avoid 19/20 (native USB), 35–37 (PSRAM), 45/46 (strapping)

```bash
.venv/bin/esphome compile firmware/climate.yaml
.venv/bin/esphome upload firmware/climate.yaml --device /dev/ttyACM0
```
