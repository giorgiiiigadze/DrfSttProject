from langchain_core.prompts import PromptTemplate
from .llm import get_llm
from .prompts import SUMMARY_PROMPT
import json


def summarize_transcript(transcript_text: str) -> dict:
    llm = get_llm()

    prompt = PromptTemplate.from_template(SUMMARY_PROMPT)

    chain = prompt | llm

    response = chain.invoke({"transcript": transcript_text})

    try:
        return json.loads(response.content)
    except json.JSONDecodeError:
        raise ValueError("Failed to parse summary response as JSON")
