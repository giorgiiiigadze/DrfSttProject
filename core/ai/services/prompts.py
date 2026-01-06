SUMMARY_PROMPT = """
You are an assistant that summarizes transcriptions.

Rules:
- Do NOT invent facts
- Do NOT change meaning
- Be concise
- Output valid JSON only

Transcript:
{transcript}

Return JSON with:
{{
  "summary": string,
  "key_points": [string],
  "tone": string
}}
"""
