from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.runnables import RunnablePassthrough,RunnableLambda

import os
import time
from tenacity import retry, stop_after_attempt, wait_random_exponential


def get_llm():
    return ChatMistralAI(model="mistral-small-latest",mistral_api_key=os.getenv("MISTRAL_API_KEY"),temperature=0.3)


def split_transcript(transcript:str)-> list:
    """
    this is used to get chunks from the transcript
    
    """
    splitter=RecursiveCharacterTextSplitter(
        chunk_size=3000,
        chunk_overlap=200
    )
    return splitter.split_text(transcript)

# Automatically retries the call if a 429 Rate Limit error is returned
@retry(wait=wait_random_exponential(min=2, max=10), stop=stop_after_attempt(4))
def _safe_invoke(chain, input_data):
    return chain.invoke(input_data)


def summarize(transcript:str)->str:
    llm=get_llm()

    """
    the chunk i am splitting in 3000 will get summarized using this function

    """
    map_prompt=ChatPromptTemplate.from_messages(
        [
            ("system","Summarize this portion of a metting transcript concisely."),
            ("human","{text}"),
        ]
        )

    map_chain=map_prompt | llm | StrOutputParser()
    """
    the map_chain generate prompt of each chunk then pass it 
    to llm then the llm will create a structured output parser 
      
     """

    chunks=split_transcript(transcript)

    chunk_summaries = []
    for chunk in chunks:

        summary = _safe_invoke(map_chain, {"text": chunk})

        chunk_summaries.append(summary)

        time.sleep(0.5)  # 0.5s pause between chunks to keep request rate smooth
    """the above chunk_summaries loop invokes each time when the {text} appear """


    combined="\n\n".join(chunk_summaries)

    combined_prompt=ChatPromptTemplate.from_messages(
        [
        (
            "system",
            "You are an expert metting summarizer. Combine these partial summaries"
            "into one final professional meeting summary in bullet points.",
        ),
        ("human","{text}"),
        ]
    )


    combined_chain =combined_prompt | llm | StrOutputParser()
    return combined_chain.invoke({"text": combined})
    """
    The "combined_chain" will return a summary of the video given to the system.
    
    """

def generate_title(transcript: str) -> str:
    llm = get_llm()

    title_prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            "Based on the meeting transcript, generate a short professional meeting title "
            "(max 8 words). Only return the title, nothing else."
        ),
        ("human", "{text}"),
    ])

    title_chain = title_prompt | llm | StrOutputParser()
    return title_chain.invoke({"text": transcript[:2000]})