---
inclusion: always
---

# Product

ESP32-S3 climate node for Home Assistant: SHT40 + ST7789, ESPHome native API.

It onboards like a consumer device: no home Wi‑Fi in the firmware; tutorial setup is QR on the screen (SoftAP + captive portal). Firmware also enables Improv BLE/serial but the docs do not walk those paths. Credentials persist in NVS across reboots. Factory reset (BOOT held 5 s, or the HA button) clears prefs only, so the same binary stays on the device.

Tutorial: walk through the code → build image → wire and validate → flash → configure and test. Host: Ubuntu 24.04.
