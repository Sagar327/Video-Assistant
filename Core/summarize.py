from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.runnables import RunnablePassthrough,RunnableLambda

import os

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

    chunk_summaries =[map_chain.invoke({"text":chunk}) for chunk in chunks ] 
    """the above chunk_summaries function get invokes each time when the {text} appear """

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


    combined_chain=(
        RunnablePassthrough() | RunnableLambda(lambda x:{"text":x}) | combined_prompt | llm | StrOutputParser
    )

    return combined_chain.invoke(combined)
    """
    The "combined_chain" will return a summary of the video given to the system.
    
    """

def generate_title(transcript:str)->str:
    llm=get_llm()

    title_chain=(
        RunnablePassthrough() | RunnableLambda(lambda x:{"text":x}) |
        ChatPromptTemplate.from_message([
            (
                "system",
                "Based on the meeting transcript, generate a short professional meeting title"
                "(max 8 words). Only return the title ,nothing else.",
            ),
            ("human","{text}"),
        ])
        | llm
        | StrOutputParser()

    )

    return title_chain(transcript[:2000])