"""
STEP 2: Parse & Filter
- Filter: is_bot = False
- Filter: có dấu '?'
- Extract: msg_id, content, timestamp, guild
"""

import pandas as pd
import re
from typing import List, Dict

def filter_questions(df: pd.DataFrame) -> pd.DataFrame:
    """
    Lọc lấy câu hỏi từ DataFrame tin nhắn.

    Criteria:
    1. Không phải bot
    2. Có dấu '?'
    3. Không phải tin ngắn (spam)
    """
    # Filter: not bot
    human_messages = df[df['is_bot'] == False].copy()

    # Filter: có dấu '?'
    questions = human_messages[
        human_messages['content'].str.contains(r'\?', regex=True, na=False)
    ].copy()

    # Filter: không phải spam (ít nhất 10 ký tự)
    questions = questions[questions['n_chars'] >= 10]

    # Thêm các cột metadata
    questions['msg_id'] = questions['msg_id']
    questions['content_clean'] = questions['content'].apply(clean_content)

    return questions

def clean_content(text: str) -> str:
    """Làm sạch nội dung để phân tích"""
    if pd.isna(text):
        return ""

    # Loại bỏ mentions
    text = re.sub(r'\[@[\w]+\]', '[USER]', text)

    # Loại bỏ links
    text = re.sub(r'\[link:[^\]]+\]', '[LINK]', text)

    # Loại bỏ email
    text = re.sub(r'\[[\w]+@vinuni.edu.vn\]', '[EMAIL]', text)

    return text.strip()

def extract_metadata(questions: pd.DataFrame) -> pd.DataFrame:
    """
    Trích xuất metadata từ câu hỏi.
    """
    # Thêm cột đếm từ
    questions['word_count'] = questions['content_clean'].str.split().str.len()

    # Thêm giờ trong ngày
    questions['hour'] = pd.to_datetime(questions['created_at_vn']).dt.hour

    # Thêm ngày
    questions['date'] = pd.to_datetime(questions['created_at_vn']).dt.date

    return questions
