# Request Monitor Chrome Extension

Monitors web requests to specified domains and sends them to a backend for analysis.

The extension runs in the background, automatically syncing monitored domains from your backend and capturing matching HTTP requests for security analysis.

## Installation

1. Open Chrome and go to `chrome://extensions/`
2. Enable "Developer mode"
3. Click "Load unpacked"
4. Select the `extension` folder

## Setup

1. Start your backend API on `http://localhost:8000`
2. Install the extension

The extension automatically fetches configuration from your backend and begins monitoring configured domains. 