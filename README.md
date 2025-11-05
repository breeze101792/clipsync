# Clipsync - Cross-Platform Clipboard Synchronization Tool

## Description
Clipsync is a command-line utility designed to synchronize clipboard content across multiple devices over a network. It can operate as a server, broadcasting clipboard changes to connected clients, or as a client, sending its local clipboard content to the server and receiving updates from it. It supports various clipboard mechanisms and encrypts data for secure transmission.

## Features
*   Cross-platform clipboard synchronization.
*   Server and client modes of operation.
*   Support for multiple clipboard backends (macOS, Windows, Linux, Terminal, ASR for audio input).
*   Configurable server IP and port.
*   Debug logging levels.
*   Encryption of clipboard content during network transmission.
*   Automatic reconnection for clients.

## Usage

### To list available microphone devices (for ASRClip mode):
```bash
./clipsync.py --mic-list
```

### To start Clipsync as a server:
```bash
./clipsync.py --start-server [-i <server_ip>] [-p <server_port>] [-d]
```

### To start Clipsync as a client:
```bash
./clipsync.py [-i <server_ip>] [-p <server_port>] [-m <clip_mode>] [-a <audio_device_index>] [-d]
```

## Options
*   `-a, --audio-index <index>` : Specify the microphone device index for ASRClip mode.
*   `-l, --mic-list`            : List available microphone devices and exit.
*   `-t, --test`                : Run testing functions (currently not detailed).
*   `-d, --debug`               : Enable debug mode for more verbose logging.
*   `-i, --server-ip <ip>`      : Specify the server IP address (default: 0.0.0.0 for server, auto-discover for client).
*   `-p, --server-port <port>`  : Specify the server port (default: 11320).
*   `-s, --start-server`        : Start Clipsync in server mode.
*   `-m, --clip-mode <mode>`    : Choose the clipboard mode.
                                  Supported modes:
                                    - pyclip (Windows)
                                    - clipboard (Linux)
                                    - macclip (macOS)
                                    - terminal (for terminal-based clipboard)
                                    - asrclip (for audio-to-text clipboard)
*   `-c, --config-path <path>`  : Specify a custom path to the configuration file.

## Configuration
Clipsync uses a configuration file located at `~/.clipsync.json` by default.
This file stores settings such as server IP, port, and log level.
You can override these settings using command-line options.

## Example
1.  Start the server on a specific IP and port with debug logging:
    ```bash
    ./clipsync.py -s -i 192.168.1.100 -p 12345 -d
    ```

2.  Start a client connecting to the server, using macclip mode:
    ```bash
    ./clipsync.py -i 192.168.1.100 -p 12345 -m macclip
    ```

3.  List audio devices and then start a client using ASRClip with a specific device:
    ```bash
    ./clipsync.py -l
    # (After identifying the index, e.g., 0)
    ./clipsync.py -a 0 -m asrclip
    ```

