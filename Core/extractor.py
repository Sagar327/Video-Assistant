#This file is used to ask question from the video if we have any .
#Help in decision making

from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.runnables import RunnablePassthrough,RunnableLambda

import os
import json

def get_llm():
    return ChatMistralAI(model="mistral-small-latest",mistral_api_key=os.getenv("MISTRAL_API_KEY"),temperature=0.2) 
    ## temperature decide what level of reply we will get ,the lower the value the basic the reply gets.


def extract_all_insights(transcript: str) -> dict:
    """Consolidates action items, key decisions, and questions into a single call to prevent 429 rate limits."""
    llm=get_llm()
    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            "You are an expert meeting analyst. Analyze the transcript and extract insights into JSON.\n"
            "Respond ONLY with a valid JSON object containing exactly these keys:\n"
            "- 'action_items': Numbered list of tasks, owners, and deadlines (or 'None found.').\n"
            "- 'key_decisions': Numbered list of decisions made (or 'None found.').\n"
            "- 'open_questions': Numbered list of unresolved topics (or 'None found.')."
        ),
        ("human", "{text}")
    ])

    chain = (
        RunnablePassthrough() 
        | RunnableLambda(lambda x: {"text": x}) 
        | prompt 
        | llm 
        | StrOutputParser()
    )

    raw_output = chain.invoke(transcript)

    # Clean up formatting if model wraps output in ```json ... ```
    cleaned = (
        raw_output.strip()
        .removeprefix("```json")
        .removeprefix("```")
        .removesuffix("```")
        .strip()
    )

    try:
        return json.loads(cleaned)
    except Exception:
        # Fallback if json parsing fails
        return {
            "action_items": raw_output,
            "key_decisions": "Parsed in main output.",
            "open_questions": "Parsed in main output.",
        }