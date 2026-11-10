---
inclusion: fileMatch
fileMatchPattern: ["firmware/**", "docs/01-walkthrough/**"]
---

# Firmware

One config: `firmware/climate.yaml` (ESP-IDF framework, octal PSRAM, `mipi_spi` ST7789V display).

- No station Wi‑Fi in the YAML. Onboarding is `wifi.ap` + `captive_portal` + `improv_ble` + `improv_serial`.
- `api: encryption: {}` so Home Assistant sets the key on adopt.
- SoftAP SSID/password live in `substitutions` and feed both `wifi.ap` and the QR string.
- Keep the excerpts in `docs/01-walkthrough/` in sync with the YAML.

Validate with `.venv/bin/esphome config firmware/climate.yaml`; build with `compile`.
