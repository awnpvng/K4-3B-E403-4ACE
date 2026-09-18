"""
AI Module - Real LLM calls
Dùng OpenAI-compatible API (Qwen3.7-flash)

Config:
- OPENAI_API_KEY: API key (required)
- OPENAI_BASE_URL: API endpoint
- MODEL: Model name (default: qwen3.7-flash)
"""

import os
import json
import ssl
from typing import Dict, List, Optional


from dotenv import load_dotenv
load_dotenv()

# Config từ environment
API_KEY = os.environ.get("OPENAI_API_KEY", "")
BASE_URL = os.environ.get(
    "OPENAI_BASE_URL",
    "https://ws-3yxiehnuth1rm9pt.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1"
)
MODEL = os.environ.get("MODEL", "qwen3.7-flash")

# SSL context cho internal APIs (không verify certificate)
SSL_CONTEXT = ssl.create_default_context()
SSL_CONTEXT.check_hostname = False
SSL_CONTEXT.verify_mode = ssl.CERT_NONE

def is_configured() -> bool:
    """Kiểm tra đã configure API key chưa"""
    return bool(API_KEY)

def call_llm(prompt: str, system: str = "") -> Optional[str]:
    """
    Gọi OpenAI-compatible API (Qwen).
    """
    if not API_KEY:
        print("   ⚠️ OPENAI_API_KEY not set - using mock")
        return None

    try:
        import urllib.request
        import urllib.error

        url = f"{BASE_URL}/chat/completions"

        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": MODEL,
            "messages": messages,
            "temperature": 0.1
        }

        data = json.dumps(payload).encode("utf-8")

        req = urllib.request.Request(
            url,
            data=data,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {API_KEY}"
            },
            method="POST"
        )

        with urllib.request.urlopen(req, timeout=60, context=SSL_CONTEXT) as response:
            result = json.loads(response.read().decode("utf-8"))

            if "choices" in result and len(result["choices"]) > 0:
                return result["choices"][0]["message"]["content"]

            return None

    except urllib.error.HTTPError as e:
        print(f"   ❌ HTTP error: {e.code} - {e.reason}")
        return None
    except Exception as e:
        print(f"   ❌ API error: {e}")
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

Tìm các câu hỏi có cùng ý nghĩa và nhóm chúng lại. Trả lời theo format JSON:
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
    """
    if not API_KEY:
        return {"intent": "other", "confidence": 0.5}

    response = call_llm(
        INTENT_CLASSIFY_PROMPT.format(question=question[:500])
    )

    if response:
        intent = response.strip().lower()
        # Clean response - extract first word/line
        intent = intent.split('\n')[0].strip()

        valid_intents = [
            "deadline_xp", "team", "lab_technical", "schedule",
            "support", "github_phoenix", "onboarding", "other"
        ]

        if intent in valid_intents:
            return {"intent": intent, "confidence": 0.95}
        elif intent in ["schedule"]:
            return {"intent": "schedule", "confidence": 0.9}

    return {"intent": "other", "confidence": 0.5}

def ai_cluster_questions(questions: List[str]) -> Dict:
    """
    Dùng AI để nhóm câu hỏi tương tự.
    """
    if not API_KEY:
        return {"clusters": [{"representative": q, "similar": []} for q in questions[:5]]}

    questions_text = "\n".join([f"- {q[:100]}" for q in questions[:20]])

    response = call_llm(
        SEMANTIC_CLUSTER_PROMPT.format(questions=questions_text)
    )

    if response:
        import re
        try:
            match = re.search(r'\{[\s\S]*\}', response)
            if match:
                return json.loads(match.group())
        except:
            pass

    return {"clusters": []}

def ai_generate_summary(questions: List[str], status: str) -> str:
    """Tạo tóm tắt ngắn cho cluster câu hỏi."""
    if not API_KEY:
        return f"Tóm tắt {len(questions)} câu hỏi"

    prompt = f"""Tóm tắt ngắn (dưới 50 từ) các câu hỏi sau về chủ đề chính:

{chr(10).join([f"- {q}" for q in questions[:10]])}

Trạng thái: {status}"""

    response = call_llm(prompt)
    return response if response else f"{len(questions)} câu hỏi về chủ đề chính"

# ============================================================
# TEST
# ============================================================
if __name__ == "__main__":
    print("Testing AI Module...")
    print(f"API Key set: {bool(API_KEY)}")
    print(f"Base URL: {BASE_URL}")
    print(f"Model: {MODEL}")

    if API_KEY:
        test = ai_classify_intent("Deadline nộp Lab2 là khi nào?")
        print(f"Test classification: {test}")
    else:
        print("No API key - skipping test")
