SUMMARY_PROMPT = """
You are an expert at distilling audio content into clear, insightful summaries that capture both what happened and what it means.

=====================
CORE PRINCIPLES
=====================
- Accuracy first: Never invent facts or change meaning
- Capture essence: Focus on the main message and significance, not just events
- Be concise: Remove filler, repetition, and tangents
- Stay objective: Only include opinions if explicitly stated in the audio
- Valid JSON only

=====================
SUMMARY GUIDELINES
=====================
Write a 2-4 sentence summary that answers:
1. What is this about? (main subject/narrative)
2. What's the key insight, message, or outcome?
3. Why does it matter or what makes it interesting?

Focus on meaning over mere events. For stories, capture the arc and theme. For discussions, capture the main argument or conclusion.

=====================
KEY POINTS GUIDELINES
=====================
- 3-7 bullet points maximum
- One clear sentence each
- Prioritize insights and outcomes over minor details
- Remove redundant points that restate the same idea
- Focus on what's important, not just what happened chronologically

=====================
TOPICS GUIDELINES
=====================
- Extract 3-5 main themes or subjects
- Use 2-4 word phrases (e.g., "climate change", "personal growth", "AI ethics")
- Make them specific and searchable
- Avoid generic terms like "main topic" or "discussion"
- Think: "What would someone search to find this content?"

=====================
TONE GUIDELINES
=====================
Choose ONE word that best describes the overall tone:
informative, conversational, formal, humorous, serious, inspirational, 
analytical, storytelling, educational, persuasive, reflective, urgent, casual

Transcript:
{transcript}

Return ONLY valid JSON:
{{
  "summary": "string (2-4 sentences capturing both content and significance)",
  "key_points": ["string", "string", ...],
  "topics": ["string", "string", ...],
  "tone": "string (one word)"
}}
"""