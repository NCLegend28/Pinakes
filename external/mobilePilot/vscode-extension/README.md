# mobilePilot VSCode Extension

Control GitHub Copilot remotely from mobile devices through a REST API integration.

## Features

- **Remote Copilot Control**: Execute Copilot suggestions from your mobile device
- **Real-time Sync**: Live communication with the mobilePilot FastAPI server
- **Secure Authentication**: JWT-based authentication with automatic token refresh
- **Status Monitoring**: Real-time connection status in the status bar
- **Mobile Prompt Processing**: Handle prompts sent from mobile devices with interactive approval

## Installation

1. Install the extension from the VS Code marketplace (coming soon)
2. Or install from VSIX:
   ```bash
   code --install-extension mobilepilot-extension-0.1.0.vsix
   ```

## Configuration

Open VS Code settings and configure the following:

- **mobilePilot.serverUrl**: URL of your mobilePilot FastAPI server (default: `http://localhost:8000`)
- **mobilePilot.username**: Your username for authentication
- **mobilePilot.autoConnect**: Automatically connect on startup (default: `false`)
- **mobilePilot.enableNotifications**: Show notifications for events (default: `true`)
- **mobilePilot.pollingInterval**: How often to check for mobile prompts in milliseconds (default: `5000`)
- **mobilePilot.timeout**: Request timeout in milliseconds (default: `30000`)

## Usage

### Initial Setup

1. **Configure Server**: Set your mobilePilot server URL in settings
2. **Connect**: Use `Ctrl+Shift+P` and run "mobilePilot: Connect to mobilePilot Server"
3. **Authenticate**: Enter your username and password when prompted

### Commands

Access commands via `Ctrl+Shift+P` (Cmd+Shift+P on macOS):

- **mobilePilot: Connect to mobilePilot Server** - Connect to the server
- **mobilePilot: Disconnect from mobilePilot Server** - Disconnect from the server
- **mobilePilot: Show Status** - Display current connection status
- **mobilePilot: Send Test Prompt** - Send a test prompt to verify functionality
- **mobilePilot: Process Mobile Prompt** - Manually trigger mobile prompt processing

### Status Bar

The mobilePilot status is displayed in the VS Code status bar:

- 🔴 **Disconnected**: Click to connect
- 🟡 **Connecting**: Connection in progress
- 🔑 **Authenticating**: Authentication in progress
- 🟢 **Connected**: Click for status details
- ❌ **Error**: Click to retry connection

When connected, the status bar will show pending prompts count: `🟢 Mobile Pilot (2)`

### Mobile Prompt Processing

When a prompt is received from your mobile device:

1. A notification appears with the prompt preview
2. Choose from available actions:
   - **Execute**: Apply the Copilot suggestion
   - **Reject**: Decline the prompt
   - **View Details**: See full prompt details

The extension automatically handles:
- Code suggestions and completions
- Explanations via Copilot Chat
- Context-aware insertions based on active file

## Requirements

- VS Code 1.74.0 or higher
- GitHub Copilot extension (for full functionality)
- mobilePilot FastAPI server running and accessible

## Development

### Building from Source

1. **Clone the repository**:
   ```bash
   git clone https://github.com/mobilepilot/vscode-extension
   cd vscode-extension
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Build the extension**:
   ```bash
   npm run build
   ```

4. **Package the extension**:
   ```bash
   npm run package
   ```

### Running Tests

```bash
npm test
```

### Development Mode

1. Open the project in VS Code
2. Press `F5` to launch a new Extension Development Host
3. Test your changes in the new window

## API Integration

This extension communicates with the mobilePilot FastAPI server using:

- **Authentication**: JWT tokens with automatic refresh
- **Prompt Submission**: REST endpoints for sending prompts
- **Status Updates**: Health checks and connection monitoring
- **Mobile Prompts**: Polling for incoming mobile requests

## Troubleshooting

### Connection Issues

1. **Check server URL**: Ensure the mobilePilot server is running and accessible
2. **Verify credentials**: Make sure username/password are correct
3. **Network connectivity**: Check if there are firewall or network restrictions
4. **Server logs**: Check the FastAPI server logs for errors

### Authentication Problems

1. **Token expiry**: The extension automatically refreshes tokens
2. **Invalid credentials**: Re-enter username/password in settings
3. **Server configuration**: Verify the server authentication setup

### Extension Not Working

1. **Reload window**: `Ctrl+Shift+P` → "Developer: Reload Window"
2. **Check output**: View → Output → "mobilePilot" channel
3. **Check logs**: Help → Toggle Developer Tools → Console
4. **Reinstall extension**: Uninstall and reinstall the extension

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

MIT License - see LICENSE file for details

## Support

- GitHub Issues: [Report bugs or request features](https://github.com/mobilepilot/vscode-extension/issues)
- Documentation: [Full API documentation](https://github.com/mobilepilot/mobilepilot)

---

**Note**: This extension is part of the mobilePilot project, enabling remote control of GitHub Copilot from mobile devices.
