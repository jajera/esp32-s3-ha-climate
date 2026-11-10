# Sensors

The SHT40 reports temperature and humidity over I2C. Two more sensors watch the device itself.

```yaml
i2c:
  sda: GPIO8
  scl: GPIO18

sensor:
  - platform: sht4x
    address: 0x44
    update_interval: 10s
    temperature:
      name: Temperature
      id: temp_c
      accuracy_decimals: 1
    humidity:
      name: Humidity
      id: hum_pct
      accuracy_decimals: 0

  - platform: wifi_signal
    id: wifi_rssi_db
    name: WiFi Signal
    entity_category: diagnostic
    update_interval: 10s

  - platform: uptime
    name: Uptime
    entity_category: diagnostic

text_sensor:
  - platform: wifi_info
    ip_address:
      id: wifi_ip
      internal: true
    ssid:
      id: wifi_ssid_ts
      internal: true
```

## Pins

| Signal | Pin | Wired in |
|--------|-----|----------|
| SDA | **GPIO8** | [SHT40](../03-wire/sht40.md) (checkpoint 3) |
| SCL | **GPIO18** | [SHT40](../03-wire/sht40.md) (checkpoint 3) |

The sensor answers at `0x44` every 10 seconds. After flash, the boot log should show that address — see [Flash the ESP32](../04-flash-esp32.md).

## What appears in Home Assistant

| Entity | Where | Used on screen as |
|--------|-------|-------------------|
| Temperature | Main, 1 decimal | `temp_c` |
| Humidity | Main, whole % | `hum_pct` |
| WiFi Signal | **Diagnostic** | `wifi_rssi_db` (dBm + strength icon) |
| Uptime | **Diagnostic** | — |
| SSID / IP (`wifi_info`) | Internal only | `wifi_ssid_ts` / `wifi_ip` on the run page |

Each `name` becomes an entity. Each `id` lets other blocks (the [display](display.md)) read the value. `entity_category: diagnostic` keeps signal and uptime out of the main list. The `wifi_info` text sensors stay `internal` so they feed the screen without cluttering Home Assistant.

**Next:** [Display](display.md)
