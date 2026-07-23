# 🎬 AI Video Assistant

> **AI-powered video intelligence platform** that transforms meetings, lectures, interviews, and YouTube videos into structured insights using **Whisper, Mistral AI, LangChain, and Retrieval-Augmented Generation (RAG).**

Upload a **local video** or provide a **YouTube URL** to automatically generate high-quality transcripts, AI summaries, action items, key decisions, and chat with your video through a semantic search-powered interface.

---

## ✨ Features

- 🎥 Analyze **YouTube videos** and **local audio/video files**
- 🎙️ Speech-to-text transcription
  - **Whisper** for English
  - **Sarvam AI** for Hinglish
- 📝 AI-generated meeting/video summaries
- 🏷️ Automatic title generation
- ✅ Extract action items
- 📌 Identify key decisions
- ❓ Detect unresolved questions
- 🧠 Chat with your video using **Retrieval-Augmented Generation (RAG)**
- 📄 Export transcripts and AI-generated notes
- 🎨 Modern Streamlit dashboard with interactive chat interface

---

## 🏗️ Architecture

```text
           Video / YouTube URL
                    │
                    ▼
        Audio Extraction (FFmpeg)
                    │
                    ▼
         Audio Chunking (Pydub)
                    │
                    ▼
     Whisper / Sarvam Transcription
                    │
                    ▼
          Complete Transcript
        ┌───────────┴───────────┐
        ▼                       ▼
 AI Summarization         Chroma Vector DB
        │                       │
        └───────────┬───────────┘
                    ▼
      Retrieval-Augmented Generation
                    │
                    ▼
          Interactive AI Chat
```

---

## 🛠️ Tech Stack

| Category | Technologies |
|----------|--------------|
| **Frontend** | Streamlit |
| **Backend** | Python |
| **LLM** | Mistral AI |
| **Framework** | LangChain (LCEL) |
| **Speech Recognition** | Whisper, Sarvam AI |
| **Vector Database** | ChromaDB |
| **Embeddings** | HuggingFace Sentence Transformers |
| **Audio Processing** | FFmpeg, Pydub, yt-dlp |

---

## 📸 Preview

<img width="1917" height="966" alt="AI Video Assistant Dashboard" src="https://github.com/user-attachments/assets/8e9d808f-ed57-4704-b08b-9e2bd29af63d" />

---

## 🚀 Getting Started

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/Sagar327/Video-Assistant.git
cd Video-Assistant
```

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Configure Environment Variables

Create a `.env` file.

```env
MISTRAL_API_KEY=your_mistral_api_key
SARVAM_API_KEY=your_sarvam_api_key
WHISPER_MODEL=small
```

### 4️⃣ Install FFmpeg

Ensure **FFmpeg** is installed and available in your system PATH.

Verify installation:

```bash
ffmpeg -version
```

### 5️⃣ Launch the Application

```bash
streamlit run app.py
```

---

## 📂 Project Structure

```text
Video-Assistant/
│
├── Core/
│   ├── extractor.py
│   ├── rag_engine.py
│   ├── summarize.py
│   ├── transcriber.py
│   └── vector_store.py
│
├── utils/
│   └── audio_processor.py
│
├── app.py
├── main.py
├── requirements.txt
├── README.md
└── .env.example
```

---

## 🎯 Future Improvements

- 📂 Drag & Drop video upload
- 🎥 Timestamp-aware answers
- 🌍 Additional language support
- 👥 Speaker diarization
- 📑 PDF meeting reports
- ☁️ Cloud deployment
- 🔐 User authentication

---

## 👨‍💻 Author

**Sagar Gahlyan**

- GitHub: https://github.com/Sagar327
- LinkedIn: https://linkedin.com/in/sagar-gahlyan

---

## ⭐ Support

If you found this project useful or interesting, consider **starring the repository**. It helps others discover the project and supports future development.
