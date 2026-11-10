# Agent notes

Climate tutorial: ESP32-S3 N16R8 + SHT40 + ST7789 → Home Assistant via ESPHome. Docs in Zensical. Firmware: `firmware/climate.yaml`. Demo host: Ubuntu 24.04.

Read `.kiro/steering/` first. Docs flow: walk through the code → build image → wire and validate → flash ESP32 → configure and test.

```bash
.venv/bin/esphome compile firmware/climate.yaml
.venv/bin/python -m zensical serve
```

`requirements.txt` is ESPHome (for readers); `requirements-docs.txt` is the docs site (for CI and authors).

Don’t flash unless asked and a serial port is there. No Wi‑Fi passwords, API keys, or HA tokens in git. Config persists in NVS across reboots; factory reset clears prefs only (same binary).
