import time
from dotenv import load_dotenv
load_dotenv()


from utils.audio_processor import process_input
from Core.transcriber import transcribe_all
from Core.summarize import summarize, generate_title
from Core.extractor import extract_all_insights
from Core.rag_engine import build_rag_chain, ask_question


def run_pipeline(source :str,language:str="english")->dict:
    print("Starting AI Video Assistant")

    chunks=process_input(source)

    transcript=transcribe_all(chunks,language=language)
    print(f"raw transcription (first 300 characters ) {transcript[:300]}")

    title = generate_title(transcript)
    time.sleep(1)  # Cooldown delay to prevent 429 errors

    summary = summarize(transcript)
    time.sleep(1)  # Cooldown delay

    # Single API call extracts action items, key decisions, and open questions
    insights = extract_all_insights(transcript)
    time.sleep(1)  # Cooldown delay
    rag_chain=build_rag_chain(transcript)

    return {
        "title": title,
        "transcript": transcript,
        "summary": summary,
        "action_items": insights.get("action_items", "None found."),
        "key_decisions": insights.get("key_decisions", "None found."),
        "open_questions": insights.get("open_questions", "None found."),
        "rag_chain": rag_chain,
    }


if __name__ == "__main__":
    # CLI entry point
    source = input("Enter YouTube URL or local file path: ").strip()
    language = input("Language (english/hinglish): ").strip() or "english"
    result = run_pipeline(source, language)


print("\n" + "=" * 60)
print(f"📌 Title: {result['title']}")
print(f"\n📋 Summary:\n{result['summary']}")
print(f"\n✅ Action Items:\n{result['action_items']}")
print(f"\n🔑 Key Decisions:\n{result['key_decisions']}")
print(f"\n❓ Open Questions:\n{result['open_questions']}")
print("=" * 60)


 # Phase 2 — Chat with your meeting via RAG
print("\n💬 Chat with your Video (type 'exit' to quit)\n")
rag_chain = result["rag_chain"]
while True:
    question = input("You: ").strip()
    if question.lower() in ["exit", "quit", "q"]:
        print("👋 Goodbye!")
        break
    if not question:
         continue
    answer = ask_question(rag_chain, question)
    print(f"\n🤖 Assistant: {answer}\n")