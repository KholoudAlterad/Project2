# ✨ Mythic Creatures Project ✨

A Python project that demonstrates **web scraping**, **API usage**, and **retry/error handling** while keeping things fun with legendary creatures 🐉🧙‍♂️.

This project was built as part of the **Day 6 Checkpoint** learning objectives:
- ✅ Scrape data from a public website
- ✅ Consume 2+ public APIs (Serper + Scenario)
- ✅ Implement error handling and retry logic
- ✅ Use Git with feature branches
- ✅ Provide a Postman collection
- ✅ Include a comprehensive README

---

## 🚀 Features

### 1. 🧙 Scrape Legendary Creatures (Wikipedia)
- Scrapes [Wikipedia’s list of legendary creatures by type](https://en.wikipedia.org/wiki/List_of_legendary_creatures_by_type).
- Extracts creature **names**.
- Displays a **random sample** each run so results differ.
- Optionally shows as many creatures as you want.

### 2. 🔍 Web Search (Serper API)
- Uses the [Serper API](https://serper.dev/) to run real Google-like searches.
- Input any query → prints **title, link, snippet**.
- Demonstrates `POST` requests, JSON handling, and error checking (`401 Unauthorized`).

### 3. 🎨 Image Generation (Scenario API)
- Uses [Scenario API](https://docs.scenario.com/) to generate images from text prompts.
- Flow:
  1. Start a `txt2img` job.
  2. Poll until job finishes.
  3. Fetch the `assetId` → get the final **image URL**.
- You can paste the URL into a browser to view/download your generated creature.

---

## 🛠️ Requirements

- Python 3.10+
- `pip install -r requirements.txt`

`requirements.txt`:
- requests
- beautifulsoup4
- python-dotenv

## ⚙️ Setup

### 1. **Clone this repo**
   git clone https://github.com/<your-username>/Project2.git
   cd Project2

### 2. **Create virtual environment**
python -m venv venv
# Windows PowerShell
.\venv\Scripts\Activate.ps1
# macOS/Linux
source venv/bin/activate

### 3. **Install dependencies**
- pip install -r requirements.txt

### 4. **Configure API keys in .env**
- SERPER_API_KEY_given=your-serper-key
- SCENARIO_API_KEY=your-scenario-key
- SCENARIO_API_SECRET=your-scenario-secret

---

## ▶️ Run the Project

- python main.py

---

## 🌐 Example Runs

### 1. **Scraper**
⚡ Summoning legendary creatures...

✅ Random sample of 10 creatures:
- 1 : Dragon
- 2 : Kraken
- 3 : Yeti
...

### 2. **Serper**
🔎 Searching the web with Serper...

Python Web Scraping : https://example.com/python
Learn the basics of scraping websites using Python...
------

### 3. **Scenario**
🎨 Conjuring image with Scenario AI...

▶️ Started job: job_12345
status: in-progress
status: success
✅ Image URL: https://cdn.cloud.scenario.com/asset_abc123...

---

## 📬 API Testing with Postman

### **You’ll find the collections in the postman/ folder:**
  1. scenario-api.postman_collection.json
  2. serper-api.postman_collection.json

### **To test:**
- Open Postman
- Click Import
- Upload either collection
- Add your API keys
- Send requests and check responses

### **This helped confirm that:**
- Auth works
- The requests are well-formed
- The responses match what’s expected in the script