# Reddit Persona Analyzer

This project scrapes a Reddit user's public content, analyzes their behavior and personality using a language model (Google Gemini), and generates a detailed persona infographic.

##  Features

-  **Reddit Scraper** – Collects a user's latest posts and comments via PRAW.
-  **LLM-based Analyzer** – Uses structured parsing from Google Gemini to generate a persona.
-  **Infographic Generator** – Creates a visual representation of the user's persona using Pillow.

---

## 📁 Project Structure

```
.
├── main.py                  # Entry point
├── api_scraper.py          # Reddit data scraper
├── persona_generator.py      # Persona analyzer + image generator
├── posts-and-comments/     # Saved Reddit text data
├── avatar/                 # Downloaded Reddit avatars
├── output/                 # Final persona infographic images
└── .env                    # API keys (not committed)
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

### 3. Add environment variables

Create a `.env` file with the following:

```
CLIENT_ID=your_reddit_client_id
CLIENT_SECRET=your_reddit_client_secret
USER_AGENT=your_user_agent
GOOGLE_API_KEY=your_google_api_key
```

---

##  Usage

Run the main script:

```bash
python main.py
```

You'll be prompted to enter a Reddit username (without `u/`). The script will:

1. Download their avatar.
2. Fetch up to 1000 posts and comments.
3. Analyze the content to create a persona.
4. Generate a visual infographic and save it to `output/`.

---

##  Output

- Reddit text data → `posts-and-comments/<username>_reddit.txt`
- Avatar → `avatar/<username>.jpg`
- Infographic → `output/<username>.png`

---

##  Notes

- Only works for public Reddit profiles.
- The language model output may retry if formatting fails.
- Infographic layout adjusts dynamically based on content.

---

##  License

This project is licensed under the MIT License.

---

##  Future Ideas

- Support for other social platforms (e.g. Twitter, LinkedIn)
- Export persona as PDF or JSON
- Web app version with upload + image preview

---

Made with ❤️ using Reddit + AI.
