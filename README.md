# ChatGPT CLI (Python)  
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)  
[![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org/)  
[![OpenAI API](https://img.shields.io/badge/API-OpenAI-orange)](https://platform.openai.com/docs/)  

A simple, no-nonsense command-line interface to talk to OpenAI's ChatGPT models — all from your terminal.

---

## 🚀 Quick Start

```bash
git clone https://github.com/<your-username>/chatgpt-cli-py.git
cd chatgpt-cli-py
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Open .env and set your OPENAI_API_KEY
python app.py chat --model gpt-4o-mini
```

---

## ⚙️ Options

| Option         | Description                                                       |
| -------------- | ----------------------------------------------------------------- |
| `--model`      | Model name (e.g. `gpt-4o`, `gpt-4o-mini`)                         |
| `--system`     | Set a system prompt                                               |
| `--no-memory`  | Single-turn only (no conversation history)                        |

---

## 🛠 How It Works

- Reads your API key from `OPENAI_API_KEY` (env var) or `.env` file  
- Uses the [OpenAI Python SDK](https://github.com/openai/openai-python) with the modern `OpenAI()` client  
- Conversation is stored in memory during a session unless `--no-memory` is set  

---

## 🔒 Safety

Your API key stays local; the app only sends requests to OpenAI's API.

---

## 📜 License

MIT — see [LICENSE](LICENSE) for details.
