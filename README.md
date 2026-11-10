# ESP32-S3 HA climate

A temperature and humidity sensor for Home Assistant, built from an ESP32-S3, an SHT40, and an ST7789 screen running ESPHome.

It sets up like a store-bought device: scan the QR code on its screen to connect it to Wi‑Fi, and Home Assistant finds it. Settings survive reboots, and holding **BOOT** for 5 seconds resets it to setup mode. No Wi‑Fi password is stored in the firmware or this repo.

Tutorial: [esp32-s3-ha-climate.johna.kiwi](https://esp32-s3-ha-climate.johna.kiwi/)

1. [Walk through the code](docs/01-walkthrough/index.md)
2. [Build the image](docs/02-build-image.md)
3. [Wire and validate](docs/03-wire/index.md)
4. [Flash the ESP32](docs/04-flash-esp32.md)
5. [Configure and test](docs/05-configure-and-test.md)

Wiring: [docs/03-wire/](docs/03-wire/index.md). Firmware: [`firmware/climate.yaml`](firmware/climate.yaml).

## Icons and logos

The docs use a few brand marks as inline icons. Copies live in `overrides/.icons/brands/`, with their source and terms in `SOURCE.txt` there. Home Assistant and ESPHome are trademarks of the Open Home Foundation, and Ubuntu is a trademark of Canonical Ltd. They are used here to identify the products, and are not relicensed under this repo's license.

## Social preview images

Link previews use `docs/assets/og-image.png` (default) and one card per tutorial section in `docs/assets/og/`. `overrides/main.html` picks the card from the page URL. To rebuild them after changing the firmware or the mock-ups:

```bash
.venv/bin/python -m pip install cairosvg pillow
.venv/bin/python docs/assets/render_og_image.py
```

The script checks that every firmware line quoted on a card is still in `firmware/climate.yaml`.

## Preview the docs

```bash
/usr/bin/python3.14 -m venv .venv
.venv/bin/python -m pip install -r requirements-docs.txt
.venv/bin/python -m zensical serve
```
