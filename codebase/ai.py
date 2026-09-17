"""
AI Module - Real LLM calls
Dùng Gemini API cho CP3

API: Gemini 1.5 Flash (free tier)
"""

import os
import json
import re
from typing import Dict, List, Optional

# Check for API key
API_KEY = os.environ.get("GEMINI_API_KEY", "")

def is_configured() -> bool:
    """Kiểm tra đã configure API key chưa"""
    return bool(API_KEY)

def call_gemini(prompt: str, system: str = "") -> Optional[str]:
    """
    Gọi Gemini API.

    Args:
        prompt: User prompt
        system: System prompt (optional)

    Returns:
        Response text hoặc None nếu lỗi
    """
    if not API_KEY:
        print("   ⚠️ GEMINI_API_KEY not set - using mock")
        return None

    try:
        import urllib.request
        import urllib.error

        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"

        payload = {
            "contents": [{
                "parts": [{"text": prompt}]
            }]
        }

        if system:
            payload["systemInstruction"] = {"parts": [{"text": system}]}

        data = json.dumps(payload).encode("utf-8")

        req = urllib.request.Request(
            url,
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST"
        )

        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode("utf-8"))

            if "candidates" in result and len(result["candidates"]) > 0:
                return result["candidates"][0]["content"]["parts"][0]["text"]

            return None

    except Exception as e:
        print(f"   ❌ Gemini API error: {e}")
        return None

# ============================================================
# PROMPTS
# ============================================================

INTENT_CLASSIFY_PROMPT = """Bạn là trợ lý phân loại câu hỏi Discord cho khóa học AI.

Phân loại câu hỏi sau vào một trong các intent:
- deadline_xp: Hỏi về deadline, nộp bài, XP, điểm, điểm danh
- team: Hỏi về lập team, thành viên nhóm
- lab_technical: Hỏi về lab, CVAT, lỗi kỹ thuật
- schedule: Hỏi về lịch, workshop, buổi học
- support: Hỏi hỗ trợ chung
- github_phoenix: Hỏi về GitHub, platform Phoenix
- onboarding: Hỏi về onboarding, đăng nhập
- other: Câu hỏi khác

Câu hỏi: {question}

Trả lời CHỈ bằng intent name, không giải thích."""

SEMANTIC_CLUSTER_PROMPT = """Bạn là trợ lý nhóm câu hỏi Discord.

Các câu hỏi:
{questions}

Tìm các câu hỏi có cùng ý nghĩa và nhóm chúng lại. Trả lời theo format:
{{
  "clusters": [
    {{"representative": "câu hỏi đại diện", "similar": ["câu 1", "câu 2"]}}
  ]
}}

CHỉ nhóm các câu hỏi THỰC SỰ giống nhau về ý nghĩa."""

# ============================================================
# AI FUNCTIONS
# ============================================================

def ai_classify_intent(question: str) -> Dict:
    """
    Dùng AI để phân loại intent.

    Returns:
        {"intent": str, "confidence": float}
    """
    if not API_KEY:
        # Mock fallback
        return {"intent": "support", "confidence": 0.5}

    response = call_gemini(
        INTENT_CLASSIFY_PROMPT.format(question=question[:500])
    )

    if response:
        intent = response.strip().lower()
        valid_intents = [
            "deadline_xp", "team", "lab_technical", "schedule",
            "support", "github_phoenix", "onboarding", "other"
        ]

        if intent in valid_intents:
            return {"intent": intent, "confidence": 0.9}

    return {"intent": "other", "confidence": 0.5}

def ai_cluster_questions(questions: List[str]) -> Dict:
    """
    Dùng AI để nhóm câu hỏi tương tự.

    Returns:
        {"clusters": [{"representative": str, "similar": List[str]}]}
    """
    if not API_KEY:
        # Mock: mỗi câu 1 cluster
        return {
            "clusters": [{"representative": q, "similar": []} for q in questions[:5]]
        }

    questions_text = "\n".join([f"- {q[:100]}" for q in questions[:20]])

    response = call_gemini(
        SEMANTIC_CLUSTER_PROMPT.format(questions=questions_text)
    )

    if response:
        try:
            # Parse JSON response
            import json
            # Extract JSON from response
            match = re.search(r'\{[\s\S]*\}', response)
            if match:
                return json.loads(match.group())
        except:
            pass

    return {"clusters": []}

def ai_generate_summary(questions: List[str], status: str) -> str:
    """
    Tạo tóm tắt ngắn cho cluster câu hỏi.
    """
    if not API_KEY:
        return f"Tóm tắt {len(questions)} câu hỏi"

    prompt = f"""Tóm tắt ngắn (dưới 50 từ) các câu hỏi sau về chủ đề chính:

{chr(10).join([f"- {q}" for q in questions[:10]])}

Trạng thái: {status}"""

    response = call_gemini(prompt)
    return response if response else f"{len(questions)} câu hỏi về chủ đề chính"
