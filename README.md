## Local File Transfer

Simple local file transfer web app (Flask) — run the server on one device and open the app from other devices on the same LAN (or via a public tunnel) to upload/download files. 
Supports multiple files per transfer and provides download-as-zip.

## Features
- Web UI (responsive for mobile & desktop)
- Multiple-file uploads per transfer code
- Download individual files or all as a zip
- In-memory mapping of transfer codes -> files
- Saves uploaded files to `uploads/`

## Requirements
- macOS / Linux / Windows with Python 3.8+
- Virtualenv recommended
- Dependencies listed in `requirements.txt`

## Quick start (macOS)
1. Create and activate a venv: 
   python3 -m venv env
   source env/bin/activate
2. Install deps: pip install -r requirements.txt
3. Run the app: python3 main.py
4. Open the app in a browser on the same machine: `http://192.168.1.5:5050/`
5. From another device on the same LAN, use the host machine's LAN IP, e.g.: `http://192.168.1.5:5050/`
