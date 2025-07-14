# Reddit Persona Analyzer

This project scrapes a Reddit user's public content, analyzes their behavior and personality using a language model (Google Gemini), and generates a detailed persona **with cited Reddit content**. It outputs both a structured text file and a visual infographic.

##  Features

-  **Reddit Scraper** – Collects a user's latest posts and comments using PRAW.
-  **LLM-Based Analyzer** – Uses Google Gemini (via LangChain) to generate a persona based on the user's behavior.
-  **Infographic Generator** – Produces a visual image summarizing the persona.
-  **Citation Output** – Each persona trait includes a quoted Reddit comment or post with a link as evidence.
-  **Text + Image Output** – Saves both a readable `.txt` file and a `.png` infographic.

---

##  Project Structure

```
.
├── main.py                   # Entry point
├── api_scraper.py           # Reddit data scraper
├── image_generator.py       # LLM persona builder + image generator
├── posts-and-comments/      # Saved Reddit text data
├── avatar/                  # Downloaded Reddit avatars
├── output/                  # Output persona image
|--output with citation/     #Output person in text file along with citation
├── .env                     # API keys (not committed)
└── README.md
```

---

##  Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/your-username/reddit-persona-analyzer.git
cd reddit-persona-analyzer
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

Required packages:

- `praw`
- `requests`
- `python-dotenv`
- `pillow`
- `langchain`
- `langchain-google-genai`
- `pydantic`

### 3. Configure API Keys

Create a `.env` file:

```env
CLIENT_ID=your_reddit_client_id
CLIENT_SECRET=your_reddit_client_secret
USER_AGENT=your_user_agent
GOOGLE_API_KEY=your_google_api_key
```

---

##  Usage

```bash
python main.py
```

You'll be prompted to enter a full Reddit profile URL (e.g., `https://www.reddit.com/user/kojied/`).

The script will:

1. Download the user's avatar
2. Fetch 1000 posts and comments
3. Analyze the user via Gemini LLM
4. Save a `.txt` persona with citations and generate a `.png` infographic

---

##  Output

Files will be saved in the `output/` folder:

- `output/<username>_persona.txt` – Persona with **citation** for each trait
- `output/<username>.png` – Visual infographic
- `posts-and-comments/<username>_reddit.txt` – Raw Reddit data
- `avatar/<username>.jpg` – Downloaded avatar image

---

##  Sample Users (for submission)

Please ensure these users are run and committed:

- [`https://www.reddit.com/user/kojied/`](https://www.reddit.com/user/kojied/)
- [`https://www.reddit.com/user/Hungry-Move-6603/`](https://www.reddit.com/user/Hungry-Move-6603/)

---

##  Notes

- Only public Reddit profiles are supported
- LLM may retry if output is not parseable
- You can easily extend this to other platforms or export formats

---

##  License

MIT License

---

##  Future Enhancements

- Export as JSON/PDF
- Web interface for uploading Reddit usernames
- Cross-platform persona fusion (Reddit + Twitter)

---

Made with ❤️ by a Reddit + AI Enthusiast
