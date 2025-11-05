# clipsync

`clipsync` is a versatile, cross-platform clipboard synchronization tool designed to seamlessly share clipboard content across multiple devices. It operates with a client-server architecture, allowing various clients to connect to a central server and exchange clipboard data securely using cryptography. Beyond standard text and image clipboard functionalities, `clipsync` also supports advanced features like audio input processing (ASRClip).

## Features

*   **Cross-Platform Compatibility**: Works on Windows, Linux, and macOS.
*   **Client-Server Architecture**: Synchronize clipboards between multiple devices.
*   **Secure Communication**: Encrypts clipboard data using cryptography.
*   **Multiple Clipboard Modes**: Supports native clipboard access, terminal-based operations, and audio input.
*   **Audio Input (ASRClip)**: Integrates speech-to-text functionality for clipboard content.
*   **Standalone Installer**: Easily generate executables for distribution.

## Usage

### Installation & Setup

To set up the necessary Python dependencies (e.g., `clipboard`, `pyinstaller`, `cryptography`):

```bash
./setup.sh -s
```

### Generating Standalone Installer (Windows)

To generate a standalone Windows executable using PyInstaller:

```bash
./setup.sh -w -i
```

This will create an executable in the `dist` directory.
