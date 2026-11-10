# ESP32

The top of the file names the device and describes the board. A few variables are reused later for the setup hotspot and QR code.

## Name and substitutions

```yaml
substitutions:
  name: esp32-s3-ha-climate
  friendly_name: ESP32-S3 HA Climate
  ap_ssid: Climate Setup
  ap_password: setup1234

esphome:
  name: ${name}
  friendly_name: ${friendly_name}
  name_add_mac_suffix: true
  project:
    name: jajera.esp32-s3-ha-climate
    version: "1.0.0"
  on_boot:
    priority: -100
    then:
      - if:
          condition:
            lambda: return !wifi::global_wifi_component->has_sta();
          then:
            - display.page.show: page_setup
```

`${name}` and the other substitutions are filled in wherever they appear later in the file.

| Key | What it does |
|-----|--------------|
| `ap_ssid` / `ap_password` | Setup hotspot only (`Climate Setup` / `setup1234`). **Not** your home Wi‑Fi. Same values go into the QR code |
| `name_add_mac_suffix` | Appends the end of the MAC address, e.g. `esp32-s3-ha-climate-a1b2c3`, so several boards don't clash |
| `project` | Tags the binary so Home Assistant can show where the config came from |
| `on_boot` | After Wi‑Fi has loaded NVS: show the QR only when no home network is saved (see [Wi‑Fi setup](wifi.md)) |

!!! note "The hotspot password is not a secret"
    It is in the QR code and in this repo. It only opens the setup page while the device has no network.

## Board, memory and log

```yaml
esp32:
  board: esp32-s3-devkitc-1
  flash_size: 16MB

psram:
  mode: octal
  speed: 80MHz

logger:
  hardware_uart: UART0
```

| Key | What it does |
|-----|--------------|
| `esp32` | ESP32-S3 DevKitC-1 class board with 16 MB flash (the N16R8) |
| `psram` | 8 MB octal PSRAM at 80 MHz — needed for the display buffer and Bluetooth. Leave these unless you use a different board |
| `logger` | Serial log on **UART0** (the **COM** bridge). ESP32-S3 would otherwise log on native USB — you'll use COM in the [flash step](../04-flash-esp32.md) |

**Next:** [Home Assistant](home-assistant.md)
