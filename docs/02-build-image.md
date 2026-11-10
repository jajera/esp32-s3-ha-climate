# 2. Build the image

Install ESPHome on Ubuntu 24.04 and compile `firmware/climate.yaml` into firmware the ESP32 can run. You don't need the board for this step.

## What you need

| | Need | Notes |
|---|------|-------|
| :brands-ubuntu: | Ubuntu 24.04 | The computer used in this tutorial |
| :lucide-terminal: | Python 3.12 to 3.14 | Ubuntu 24.04 ships 3.12. This page uses 3.14 |
| :lucide-git-branch: | git | To clone the repo |
| :lucide-globe: | An internet connection | The first build downloads the ESP-IDF framework, the compiler and the display fonts |
| :lucide-unplug: | No board yet | Building never touches the ESP32 |

## The steps

```mermaid
flowchart LR
  A[Python + git] --> B[Get the code] --> C[Get ESPHome] --> D[Check config] --> E[Compile] --> F[Firmware files]
```

## Install the tools

```bash
sudo add-apt-repository -y ppa:deadsnakes/ppa
sudo apt-get install -y git python3.14 python3.14-venv
```

The first line adds the [deadsnakes PPA](https://launchpad.net/~deadsnakes/+archive/ubuntu/ppa), which carries newer Python versions. The second installs git, Python 3.14 and its `venv` module. Check it worked:

<div class="run" markdown>

```bash
python3.14 --version
```

```text {.no-copy}
Python 3.14.6
```

</div>

Any 3.14.x is fine.

!!! tip "Prefer not to add a PPA?"
    Use the built-in Python 3.12. Install `python3.12` and `python3.12-venv` instead, and swap `python3.14` for `python3.12` in the commands on this page.

## Get the code

```bash
git clone https://github.com/jajera/esp32-s3-ha-climate.git
cd esp32-s3-ha-climate
```

Already have the repo checked out? Skip the clone and `cd` into it.

## Install ESPHome

ESPHome goes into a virtual environment (`.venv`) inside the repo, so it doesn't touch your system Python:

<div class="run" markdown>

```bash
/usr/bin/python3.14 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/esphome version
```

```text {.no-copy}
…
Successfully installed … esphome-2026.10.2 …
Version: 2026.10.2
```

</div>

## Check the config

`config` validates the YAML without building anything. It's a quick way to catch typos after you edit the file. The `grep` keeps just the status lines:

<div class="run" markdown>

```bash
.venv/bin/esphome config firmware/climate.yaml | grep INFO
```

```text {.no-copy}
INFO ESPHome 2026.10.2
INFO Reading configuration firmware/climate.yaml...
INFO Configuration is valid!
```

</div>

## Compile

<div class="run" markdown>

```bash
.venv/bin/esphome compile firmware/climate.yaml
```

```text {.no-copy}
INFO ESPHome 2026.10.2
INFO Reading configuration firmware/climate.yaml...
INFO Generating C++ source...
INFO Compiling app... Build path: …/firmware/.esphome/build/esp32-s3-ha-climate
…
RAM:   [====      ]  42.7% (used 145763 bytes from 341760 bytes)
Flash: [==        ]  16.2% (used 1319099 bytes from 8126464 bytes)
INFO Creating factory.bin...
INFO Created: …/build/firmware.factory.bin
INFO Created: …/build/firmware.ota.bin
INFO Created: …/build/firmware.elf
INFO Successfully compiled program.
```

</div>

!!! note "How long it takes"
    The first compile downloads the framework, compiler and fonts, so it takes several minutes. Later builds reuse what was downloaded. On the machine used for this page, a rebuild with nothing changed finished in about 1.4 seconds.

### Reading the result

| | Line | What it tells you |
|---|------|-------------------|
| :lucide-memory-stick: | `RAM` | Memory the running program uses: 145,763 of 341,760 bytes (42.7%). Over half is still free |
| :lucide-hard-drive: | `Flash` | Space the program takes in its flash partition: 1,319,099 of 8,126,464 bytes (16.2%). That is the app partition, not the whole 16 MB chip |

### What it builds

The files land in `firmware/.esphome/build/esp32-s3-ha-climate/build/`, which git ignores. Sizes from the compile above:

| | File | Size | What it is |
|---|------|------|------------|
| :lucide-zap: | `firmware.factory.bin` | 1.32 MB | The complete image (bootloader, partition table and app) for the first flash over USB |
| :lucide-refresh-cw: | `firmware.ota.bin` | 1.26 MB | The app on its own, for over-the-air updates later |
| :lucide-bug: | `firmware.elf` | 22.3 MB | Debug symbols. It is never flashed |

You don't need to copy anything. ESPHome finds these itself when you upload in the next step.

## If it fails

| Symptom | Fix |
|---------|-----|
| `python3.14: command not found` | The PPA step didn't run. Repeat the two `apt` commands |
| Creating `.venv` fails | Install the venv module: `sudo apt-get install -y python3.14-venv` |
| The compile stops while downloading | Check your internet connection and run the same command again |

!!! success "Done when"
    - `esphome version` prints a version
    - `esphome config` ends with **Configuration is valid!**
    - `esphome compile` ends with **Successfully compiled program.**

**Next:** [Wire and validate](03-wire/index.md)
