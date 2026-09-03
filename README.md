# Personal AI Assistant

A desktop personal AI assistant with:

- **Voice interface** (STT + TTS) – Whisper / ElevenLabs
- **PC control** tools (open apps, files, system info, etc.)
- **Browser automation**
- **Long-term memory** (SQLite + embeddings-ready)
- **Multi-agent orchestration**
- **Electron** desktop shell
- **FastAPI** backend with WebSocket streaming

## Quick Start (Windows)

```bat
install.bat
start.bat
```

## Development

### Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements.txt
cp ../.env.example .env        # edit keys
python run.py
```

### Frontend (Vite + React)

```bash
cd frontend
npm install
npm run dev
```

### Electron

```bash
cd electron
npm install
npm start
```

## Building Installer

```bat
build.bat
```

Produces a Windows installer via NSIS + PyInstaller + Electron.

## Architecture

```
User (Voice / Text)
        │
   Electron UI  ←→  WebSocket  ←→  FastAPI Backend
                                      │
                    ┌─────────────────┼─────────────────┐
                    │                 │                 │
               Conversation      PC / Browser      Memory Agent
                  Agent             Agents
                    │                 │                 │
                    └────────── Orchestrator ───────────┘
                                      │
                              LLM (OpenAI / local)
```

## Environment Variables

See `.env.example`.

## License

MIT
