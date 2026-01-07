import json
import math

from django.db import transaction
from django.core.exceptions import PermissionDenied

from langchain_core.prompts import PromptTemplate

from .llm import get_llm
from .prompts import SUMMARY_PROMPT

TOKENS_PER_CREDIT = 1000
CHARS_PER_TOKEN = 4

def estimate_tokens(text: str) -> int:
    return max(1, len(text) // CHARS_PER_TOKEN)


def tokens_to_credits(tokens: int) -> int:
    return math.ceil(tokens / TOKENS_PER_CREDIT)


def summarize_transcript(*, user, transcript_text: str) -> dict:

    estimated_tokens = estimate_tokens(transcript_text)
    required_credits = tokens_to_credits(estimated_tokens)

    with transaction.atomic():
        user.refresh_from_db()

        if user.credits < required_credits:
            raise PermissionDenied(
                "You do not have enough credits to summarize this audio."
            )

        user.credits -= required_credits
        user.save(update_fields=["credits"])

    llm = get_llm()
    prompt = PromptTemplate.from_template(SUMMARY_PROMPT)
    chain = prompt | llm

    try:
        response = chain.invoke({"transcript": transcript_text})
        data = json.loads(response.content)

    except Exception:
        with transaction.atomic():
            user.refresh_from_db()
            user.credits += required_credits
            user.save(update_fields=["credits"])
        raise

    data["input_tokens"] = estimated_tokens
    data["output_tokens"] = None
    data["tokens_used"] = estimated_tokens
    data["credits_used"] = required_credits

    return data
