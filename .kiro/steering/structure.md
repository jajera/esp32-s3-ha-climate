---
inclusion: always
---

# Structure

```text
docs/                 tutorial (01–05; code walkthrough under 01-walkthrough/, wiring under 03-wire/), overview
firmware/climate.yaml the only firmware config
scripts/              setup-linux-usb.sh + udev rules
requirements.txt      ESPHome (readers)
requirements-docs.txt Zensical (docs CI + authors)
zensical.toml         site nav
overrides/            theme override + copied brand icons (.icons/brands/, see SOURCE.txt)
.github/              pages + markdown-lint + commitmsg-conform + yaml-lint
```

The walkthrough pages quote `firmware/climate.yaml`. When the YAML changes, update the quoted excerpts too.
