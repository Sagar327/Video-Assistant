import time
from dotenv import load_dotenv
load_dotenv()
import json


def run_pipeline(source: str, language: str = "english") -> dict:
    """Run the full AI pipeline. Heavy imports are deferred until runtime so
    this module can be safely imported by serverless platforms (like Vercel)
    without immediately requiring all ML dependencies.
    """
    # Deferred imports to avoid import-time side effects / heavy dependency loading
    from utils.audio_processor import process_input
    from Core.transcriber import transcribe_all
    from Core.summarize import summarize, generate_title
    from Core.extractor import extract_all_insights
    from Core.rag_engine import build_rag_chain

    print("Starting AI Video Assistant")

    chunks = process_input(source)

    transcript = transcribe_all(chunks, language=language)
    print(f"raw transcription (first 300 characters ) {transcript[:300]}")

    title = generate_title(transcript)
    time.sleep(1)  # Cooldown delay to prevent 429 errors

    summary = summarize(transcript)
    time.sleep(1)  # Cooldown delay

    # Single API call extracts action items, key decisions, and open questions
    insights = extract_all_insights(transcript)
    time.sleep(1)  # Cooldown delay
    rag_chain = build_rag_chain(transcript)

    return {
        "title": title,
        "transcript": transcript,
        "summary": summary,
        "action_items": insights.get("action_items", "None found."),
        "key_decisions": insights.get("key_decisions", "None found."),
        "open_questions": insights.get("open_questions", "None found."),
        "rag_chain": rag_chain,
    }


def handler(request):
    """Vercel-compatible handler. Accepts JSON body: {"source": "...", "language": "english"}
    Returns a JSON response with pipeline results.
    """
    try:
        payload = None
        # Vercel's request may provide a .json() method or .get_json
        if hasattr(request, "get_json"):
            payload = request.get_json()
        elif hasattr(request, "json"):
            payload = request.json
        else:
            # fallback: try reading body-like attributes
            body = getattr(request, "body", None)
            if body:
                payload = json.loads(body)

        source = (payload or {}).get("source")
        language = (payload or {}).get("language", "english")

        if not source:
            return {"statusCode": 400, "body": json.dumps({"error": "missing 'source' field"})}

        result = run_pipeline(source, language=language)
        return {"statusCode": 200, "body": json.dumps(result)}

    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}


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