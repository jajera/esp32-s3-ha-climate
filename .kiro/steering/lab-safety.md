---
inclusion: always
---

# Lab safety

Don’t upload or erase flash unless John asked and a serial port is visible (`/dev/ttyACM*` or `/dev/ttyUSB*`). `esphome config` and `esphome compile` are fine anytime.

Power the sensor and display from **3V3**, never 5V. Unplug USB while rewiring.

No Wi‑Fi passwords, API keys, or HA tokens in git. `secrets.yaml` is gitignored.

Factory reset clears NVS prefs only; it does not reflash the binary.
