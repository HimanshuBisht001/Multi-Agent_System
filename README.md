# 🔬 Deep Research — Multi-Agent AI System

A multi-agent research pipeline powered by **LangChain** and **Groq (Llama 3.3)** with a clean **Streamlit** UI. Enter any topic and the system autonomously searches the web, scrapes top sources, writes a structured report, and critiques it — all in one click.

---

## 🧠 How It Works

The pipeline runs four agents/chains in sequence:

```
Search Agent → Reader Agent → Writer Chain → Critic Chain
```

| Step | Agent | Role |
|------|-------|------|
| 01 | **Search Agent** | Searches the web via Tavily and returns titles, URLs, and snippets |
| 02 | **Reader Agent** | Picks the most relevant URL and scrapes its full content |
| 03 | **Writer Chain** | Drafts a structured research report (Intro → Findings → Conclusion → Sources) |
| 04 | **Critic Chain** | Reviews the report and returns a score, strengths, and a one-line verdict |

Agents are built using LangChain's `create_agent` with tool-calling support. The Writer and Critic are lightweight LCEL chains (`ChatPromptTemplate | LLM | StrOutputParser`).

---

## 📁 Project Structure

```
Multi-Agent_System/
├── app.py              # Streamlit UI
├── pipeline.py         # Terminal runner (original CLI entry point)
├── agents.py           # Agent & chain definitions
├── tools.py            # Web search and URL scraping tools
├── requirements.txt    # Python dependencies
└── .env                # API keys (never commit this)
```

---

## ⚙️ Setup

### 1. Clone the repo

```bash
git clone https://github.com/YOUR_USERNAME/Multi-Agent_System.git
cd Multi-Agent_System
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure API keys

Create a `.env` file in the root directory:

```env
GROQ_API_KEY=your_groq_api_key
Tavily_API_Key=your_tavily_api_key
```

> Get your keys at [console.groq.com](https://console.groq.com) and [tavily.com](https://tavily.com)

---

## 🚀 Running the App

### Streamlit UI (recommended)

```bash
streamlit run app.py
```

Then open [http://localhost:8501](http://localhost:8501) in your browser.

### Terminal (CLI)

```bash
python pipeline.py
```

---

## 🌐 Deploy to Streamlit Community Cloud

1. Push this repo to GitHub (make sure `.env` is in `.gitignore`)
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repo and select `app.py` as the entry point
4. Add your API keys under **Settings → Secrets**:

```toml
GROQ_API_KEY = "your_groq_api_key"
Tavily_API_Key = "your_tavily_api_key"
```

5. Click **Deploy** — your app is live!

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| LLM | Groq — `llama-3.3-70b-versatile` |
| Agent Framework | LangChain `create_agent` |
| Chains | LangChain `ChatPromptTemplate` + `StrOutputParser` |
| Web Search | Tavily API |
| Web Scraping | `requests` + `BeautifulSoup4` |
| UI | Streamlit |
| Env Management | `python-dotenv` |

---

## 📦 Key Dependencies

```
langchain
langchain-core
langchain-community
langchain-groq
tavily-python==0.7.2
streamlit==1.45.1
beautifulsoup4==4.13.4
```

Full list in [`requirements.txt`](requirements.txt).

---

## 🔒 Security

- **Never commit your `.env` file.** It contains secret API keys.
- The `.gitignore` excludes `.env` and `.venv/` by default.
- If you accidentally push your keys, rotate them immediately at the provider's console.

---

## 🙌 Acknowledgements

- [LangChain](https://www.langchain.com/)
- [Groq](https://groq.com/) for blazing-fast inference
- [Tavily](https://tavily.com/) for search API
- [Streamlit](https://streamlit.io/) for the UI framework
