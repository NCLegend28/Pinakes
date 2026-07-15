# Interactive Web Client for Book Pack Builder

A modern, drag-and-drop web interface for processing books into structured summaries with real-time progress tracking.

## Features

- **Drag & Drop Upload** - Simply drag PDF or EPUB files into the browser
- **Real-time Progress** - Watch processing steps with live WebSocket updates
- **Beautiful Results Viewer** - Browse summaries, timelines, people, and themes
- **Download Pack Files** - Get the complete pack.yaml for GPT integration
- **Mobile Responsive** - Works on desktop, tablet, and mobile

## Quick Start

### 1. Install Dependencies

```bash
# Activate your virtual environment
source .venv/bin/activate  # or .venv\Scripts\activate on Windows

# Install web client dependencies
pip install -r requirements.txt
```

### 2. Set API Keys

```bash
export OPENAI_API_KEY="sk-..."
export OPENAI_CHAT_MODEL="gpt-4o-mini"
export OPENAI_EMBED_MODEL="text-embedding-3-large"
```

### 3. Run the Web Server

```bash
python app.py
```

The server will start at `http://localhost:5000`

### 4. Open in Browser

Navigate to `http://localhost:5000` and you'll see the interactive interface!

## Usage

1. **Upload Book**
   - Drag and drop a PDF or EPUB file into the drop zone
   - Or click to browse and select a file

2. **Enter Metadata**
   - Fill in Title and Author (required)
   - Optionally add Edition and Language
   - Adjust advanced options (chunk size, overlap)

3. **Process**
   - Click "Process Book"
   - Watch real-time progress updates
   - Processing typically takes 2-10 minutes depending on book size

4. **View Results**
   - Browse the Summary tab for book overview
   - Check People & Orgs for key entities
   - Explore Timeline for chronological events
   - Download the complete pack.yaml file

## Architecture

### Backend (Flask + SocketIO)

```
app.py
├── Upload endpoint (/api/upload)
├── Status endpoint (/api/status/<job_id>)
├── Results endpoint (/api/result/<job_id>)
├── Download endpoint (/api/download/<job_id>/pack.yaml)
└── WebSocket progress updates
```

### Frontend (HTML/CSS/JS)

```
web/
├── templates/
│   └── index.html          # Main interface
├── static/
    ├── css/
    │   └── style.css       # Modern, gradient design
    └── js/
        └── app.js          # Drag-drop + WebSocket client
```

### Processing Flow

```
1. User uploads file → /api/upload
2. Server starts background processing thread
3. Client joins WebSocket room for job_id
4. Server emits progress updates:
   - Ingesting (10%)
   - Chunking (30%)
   - Tier A summaries (40-55%)
   - Tier B summaries (55-65%)
   - Tier C summary (65-75%)
   - Extracting entities (75-85%)
   - Writing files (85-95%)
   - Building index (90-95%)
   - Complete (100%)
5. Client fetches results → /api/result/<job_id>
6. Display in beautiful interface
```

## Configuration

### Environment Variables

- `OPENAI_API_KEY` - Required for LLM processing
- `OPENAI_CHAT_MODEL` - Model for summaries (default: gpt-4o-mini)
- `OPENAI_EMBED_MODEL` - Model for embeddings (default: text-embedding-3-large)
- `SECRET_KEY` - Flask secret key (auto-generated if not set)

### File Limits

- **Max file size**: 50MB
- **Allowed formats**: PDF, EPUB
- **Upload folder**: `./uploads` (auto-created)
- **Output folder**: `./out` (auto-created)

## Customization

### Styling

Edit `web/static/css/style.css` to change colors, fonts, or layout.

### Processing Options

Users can adjust:
- **Chunk Size** (500-2000 tokens) - Smaller = more detail, slower
- **Overlap Ratio** (0-0.5) - Higher = better context, more redundancy

### Prompts

Modify prompts in `prompts/` directory to customize summary style.

## Production Deployment

### Option 1: Gunicorn (Recommended)

```bash
pip install gunicorn eventlet
gunicorn --worker-class eventlet -w 1 --bind 0.0.0.0:5000 app:app
```

### Option 2: Docker

```dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY . /app

RUN pip install -r requirements.txt

EXPOSE 5000
CMD ["python", "app.py"]
```

Build and run:
```bash
docker build -t book-pack-builder .
docker run -p 5000:5000 -e OPENAI_API_KEY=$OPENAI_API_KEY book-pack-builder
```

### Security Considerations

- Set a strong `SECRET_KEY` in production
- Use HTTPS (deploy behind nginx/Apache)
- Rate limit uploads to prevent abuse
- Implement authentication if needed
- Clean up old uploads/outputs periodically

## Troubleshooting

**WebSocket not connecting**
- Check that port 5000 is not blocked
- Ensure browser supports WebSocket (all modern browsers do)
- Check browser console for errors

**Processing hangs**
- Check API key is set correctly
- Verify OpenAI API quota/limits
- Look at server logs for errors

**File upload fails**
- Ensure file is < 50MB
- Check file is valid PDF or EPUB
- Verify `uploads/` directory exists and is writable

**Out of memory**
- Reduce chunk size
- Process smaller books
- Increase server RAM

## API Reference

### POST /api/upload

Upload and process a book.

**Form Data:**
- `file` - PDF or EPUB file
- `title` - Book title (required)
- `author` - Author name (required)
- `edition` - Edition (optional)
- `language` - Language (optional)
- `chunk_tokens` - Chunk size (default: 1000)
- `overlap` - Overlap ratio (default: 0.15)

**Response:**
```json
{
  "job_id": "abc123...",
  "message": "Processing started",
  "title": "Book Title",
  "author": "Author Name"
}
```

### GET /api/status/<job_id>

Get current processing status.

**Response:**
```json
{
  "job_id": "abc123...",
  "status": "processing",
  "progress": 45,
  "current_step": "tier_a",
  "filename": "book.pdf"
}
```

### GET /api/result/<job_id>

Get processed results (only when status = "completed").

**Response:**
```json
{
  "metadata": {...},
  "tier_c": {
    "summary_spoiler_safe": "...",
    "summary_full": "...",
    "theme_map": [...]
  },
  "people_orgs": [...],
  "timeline": [...]
}
```

### GET /api/download/<job_id>/pack.yaml

Download the complete pack.yaml file.

## Future Enhancements

- [ ] User accounts and history
- [ ] Batch processing multiple books
- [ ] Custom prompt templates via UI
- [ ] Search within processed books
- [ ] Export to different formats (Markdown, PDF)
- [ ] Share public links to processed books
- [ ] Compare multiple books side-by-side
- [ ] AI chat interface with the book content

## License

Same as the main book-pack-builder project.
