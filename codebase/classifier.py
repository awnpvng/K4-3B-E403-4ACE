"""
STEP 3: Intent Classification
- Rule-based keyword matching (primary)
- LLM fallback khi không khớp
- Priority: deadline > team > schedule > lab > github > onboarding > support
"""

import pandas as pd
import re
from typing import Dict, List
import os

# Intent với priority (số càng nhỏ = ưu tiên càng cao)
INTENT_PRIORITY = {
    'support': 1,           # Hỗ trợ chung - catch-all cuối cùng
    'deadline_xp': 2,       # Deadline/XP - cụ thể nhất
    'team': 3,
    'schedule': 4,
    'github_phoenix': 5,
    'onboarding': 6,
    'lab_technical': 7,     # Lab Technical - bị các intent khác override
    'other': 8
}

# Intent definitions với keywords
# Priority = thứ tự duyệt (duyệt ngược: ưu tiên thấp = xét trước)
# => Vì find all matches rồi sort theo priority
INTENT_PATTERNS = {
    'lab_technical': {
        'keywords': [
            r'\blab\b', r'\bCVAT\b', r'lỗi\b', r'cài đặt', r'install',
            r'run\b', r'bước\s', r'làm lab', r'bài lab', r'làm\s*lab',
            r'code\b', r'lập trình', r'bị lỗi', r'bug\b', r'step\s'
        ],
        'description': 'Câu hỏi về lab kỹ thuật'
    },
    'github_phoenix': {
        'keywords': [
            r'github', r'\bgit\b', r'\bfork\b', r'\bclone\b', r'\bpull\b',
            r'\bpush\b', r'pull request', r'\brepo\b', r'\bbranch\b', r'commit'
        ],
        'description': 'Câu hỏi về GitHub, platform Phoenix'
    },
    'onboarding': {
        'keywords': [
            r'onboard', r'đăng nhập', r'tài khoản', r'link mời', r'xác minh',
            r'vào\s*được', r'không\s*vào', r'phoenix', r'vlearn', r'profile'
        ],
        'description': 'Câu hỏi về onboarding, tài khoản'
    },
    'schedule': {
        'keywords': [
            r'workshop', r'buổi học', r'buổi workshop', r'thứ\s*\d',
            r'bắt buộc', r'chủ nhật', r'ngày mai', r'thời gian', r'học trực tuyến',
            r'zoom', r'outlook', r'lịch học', r'tham gia', r'vắng', r'sáng\b.*học',
            r'học\s*sáng', r'buổi\b'
        ],
        'description': 'Câu hỏi về lịch, workshop, thời gian'
    },
    'team': {
        'keywords': [
            r'team\b', r'đội\b', r'nhóm\b', r'thành viên', r'ghép đội',
            r'lập đội', r'lập nhóm', r'5 bạn', r'4 bạn', r'số lượng',
            r'thiếu bạn'
        ],
        'description': 'Câu hỏi về lập team, thành viên'
    },
    'deadline_xp': {
        'keywords': [
            r'\bXP\b', r'điểm danh', r'deadline', r'nộp bài', r'nộp lab',
            r'muộn', r'trễ', r'bị trừ', r'trừ điểm', r'cộng điểm',
            r'1 phút', r'mấy phút', r'tính không', r'điểm\b.*không'
        ],
        'description': 'Câu hỏi về deadline, nộp bài, XP, điểm'
    },
    'support': {
        'keywords': [
            r'hỏi\b', r'hỗ trợ', r'giúp', r'cho mình', r'cho e',
            r'thắc mắc', r'xin hỏi', r'giải đáp', r'chỉ mình', r'hướng dẫn',
            r'tư vấn', r'xin\b', r'liên hệ', r'gửi mail', r'ai giúp',
            r'bạn nào', r'người nào', r'thư viện', r'biết\b'
        ],
        'description': 'Câu hỏi hỗ trợ chung'
    }
}

def classify_intent(questions: pd.DataFrame, use_ai: bool = True) -> pd.DataFrame:
    """
    Phân loại intent cho từng câu hỏi.

    Args:
        questions: DataFrame chứa câu hỏi
        use_ai: True = dùng LLM cho unclassified, False = rule-only

    Returns:
        DataFrame với cột 'intent' thêm vào
    """
    questions = questions.copy()
    questions['intent'] = 'other'
    questions['intent_confidence'] = 0.0

    # Rule-based classification
    for idx, row in questions.iterrows():
        content = row['content']

        # Find matching intents
        matches = []
        for intent_name, intent_info in INTENT_PATTERNS.items():
            for pattern in intent_info['keywords']:
                if re.search(pattern, content, re.IGNORECASE):
                    priority = INTENT_PRIORITY.get(intent_name, 99)
                    matches.append((intent_name, priority))
                    break

        if matches:
            # Sort by priority and pick the best
            matches.sort(key=lambda x: x[1])
            best_intent = matches[0][0]
            questions.at[idx, 'intent'] = best_intent
            questions.at[idx, 'intent_confidence'] = 0.8 if len(matches) == 1 else 0.6

    # LLM fallback cho other/unclassified (nếu use_ai=True)
    if use_ai:
        other = questions[questions['intent'] == 'other']
        if len(other) > 0:
            print(f"   [AI] Classifying {len(other)} unclassified questions...")
            questions = llm_classify(questions)

    return questions

def llm_classify(questions: pd.DataFrame) -> pd.DataFrame:
    """
    Dùng LLM để phân loại câu hỏi không khớp keyword.

    MOCK IMPLEMENTATION - Thay bằng API call thật khi deploy
    """
    # TODO: Replace with actual LLM API call
    # Ví dụ: Gemini API, OpenAI API

    # MOCK: Giữ nguyên là 'other' - sẽ dùng LLM thật sau
    return questions

def get_intent_summary(questions: pd.DataFrame) -> Dict:
    """Tóm tắt phân bố intent"""
    summary = questions.groupby('intent').agg({
        'msg_id': 'count',
        'intent_confidence': 'mean'
    }).rename(columns={'msg_id': 'count'})

    return summary.to_dict('index')

def classify_single(question: str) -> str:
    """
    Classify single question - standalone function for evaluation.
    """
    # Find matching intents
    matches = []
    for intent_name, intent_info in INTENT_PATTERNS.items():
        for pattern in intent_info['keywords']:
            if re.search(pattern, question, re.IGNORECASE):
                priority = INTENT_PRIORITY.get(intent_name, 99)
                matches.append((intent_name, priority))
                break

    if matches:
        matches.sort(key=lambda x: x[1])
        return matches[0][0]

    return "other"
