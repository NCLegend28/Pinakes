# Change Log

All notable changes to the mobilePilot VSCode extension will be documented in this file.

## [0.1.0] - 2025-06-19

### Added
- Initial release of mobilePilot VSCode extension
- Connection management to mobilePilot FastAPI server
- JWT authentication with automatic token refresh
- Real-time mobile prompt processing
- Status bar integration with connection status
- Configuration management for server settings
- Command palette integration with 5 core commands:
  - Connect/Disconnect server
  - Show status
  - Send test prompt
  - Process mobile prompts
- Interactive prompt approval workflow
- GitHub Copilot integration for:
  - Code suggestions and completions
  - Chat explanations
  - Context-aware code insertions
- Comprehensive error handling and notifications
- TypeScript implementation with webpack bundling
- Unit tests for core functionality
- VS Code debugging configuration

### Technical Features
- Modular architecture with separate managers for:
  - Configuration management
  - Status bar handling
  - API client communication
- Polling mechanism for mobile prompt detection
- Language-aware comment insertion
- Automatic server health checks
- Configurable polling intervals and timeouts
- Production-ready webpack build configuration

### Configuration Options
- `mobilePilot.serverUrl`: FastAPI server URL
- `mobilePilot.username`: Authentication username
- `mobilePilot.autoConnect`: Automatic connection on startup
- `mobilePilot.enableNotifications`: Toggle notifications
- `mobilePilot.pollingInterval`: Mobile prompt polling frequency
- `mobilePilot.timeout`: Request timeout duration

## [Unreleased]

### Planned Features
- Enhanced Copilot integration with advanced API usage
- Mobile prompt queueing and batch processing
- Offline mode with prompt caching
- Multi-workspace support
- Advanced authentication methods
- Performance optimizations
- Enhanced error recovery
- Telemetry and analytics
- Extension marketplace publication
