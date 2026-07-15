# Environment Setup Guide

## Required Environment Variables

The Tools Hub backend requires certain environment variables to be set for full functionality.

### Setting Up Your .env File

1. Copy the example file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and add your actual API keys:
   ```bash
   # Required for Book Pack Builder (for AI summarization)
   ANTHROPIC_API_KEY=your_actual_anthropic_api_key_here
   ```

3. Restart the backend server to load the new environment variables

### Getting an Anthropic API Key

1. Visit https://console.anthropic.com/
2. Sign up or log in
3. Navigate to API Keys section
4. Create a new API key
5. Copy the key and paste it into your `.env` file

### Verifying Setup

After setting up your `.env` file, you can verify it's working by:

1. Restart the backend server
2. Try building a book pack via the API
3. Check the job status - it should no longer fail with "ANTHROPIC_API_KEY" error

### Security Notes

- **NEVER** commit your `.env` file to version control
- The `.env` file is already listed in `.gitignore`
- Keep your API keys secret and secure
- Rotate your keys periodically for security
