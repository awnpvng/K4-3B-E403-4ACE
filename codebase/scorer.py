"""
STEP 6: Scoring & Ranking
- Frequency Score: đếm tần suất câu hỏi trong cluster
- Urgency Weight: trọng số cho deadline/XP
- Freshness Score: hàm suy giảm thời gian
- Unanswered Penalty: bonus cho câu chưa giải đáp
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Trọng số urgency cho từng intent
URGENCY_WEIGHTS = {
    'deadline_xp': 1.5,    # Cao - ảnh hưởng điểm/XP
    'team': 1.3,            # Trung-bao - deadline ghép đội
    'lab_technical': 1.2,  # Trung - cần giải quyết để làm bài
    'schedule': 1.0,        # Thường
    'support': 0.8,        # Thường
    'github_phoenix': 0.9,  # Thường
    'onboarding': 1.1,      # Trung - cần hoàn thành onboarding
    'unclassified': 0.7     # Thấp
}

def calculate_priority_scores(questions: pd.DataFrame) -> pd.DataFrame:
    """
    Tính điểm ưu tiên cho từng câu hỏi.

    Score = frequency * urgency * freshness * unanswered_bonus
    """
    questions = questions.copy()

    # 1. Frequency Score (số câu hỏi trong cluster)
    if 'cluster_size' not in questions.columns:
        questions['cluster_size'] = 1
    questions['frequency_score'] = questions['cluster_size']

    # 2. Urgency Weight
    questions['urgency_weight'] = questions['intent'].map(
        lambda x: URGENCY_WEIGHTS.get(x, 0.7)
    )

    # 3. Freshness Score (time decay)
    # Câu hỏi mới hơn = điểm cao hơn (ưu tiên xử lý sớm)
    now = questions['created_at_vn'].max()
    questions['age_hours'] = (now - pd.to_datetime(questions['created_at_vn'])).dt.total_seconds() / 3600

    # Exponential decay: score = e^(-age/24) - giảm 50% mỗi 24h
    questions['freshness_score'] = np.exp(-questions['age_hours'] / 24)

    # 4. Unanswered Bonus
    questions['unanswered_bonus'] = questions['status'].apply(
        lambda x: 1.5 if x == 'unanswered' else (1.2 if x == 'partial' else 1.0)
    )

    # Tổng hợp score
    questions['priority_score'] = (
        questions['frequency_score'] *
        questions['urgency_weight'] *
        questions['freshness_score'] *
        questions['unanswered_bonus']
    )

    # Round
    questions['priority_score'] = questions['priority_score'].round(2)

    return questions

def get_top_questions(questions: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    """Lấy top N câu hỏi ưu tiên cao nhất"""
    return questions.nlargest(n, 'priority_score')

def get_unanswered_urgent(questions: pd.DataFrame, hours_threshold: int = 4) -> pd.DataFrame:
    """Lấy câu hỏi chưa trả lời sau N giờ"""
    unanswered = questions[questions['status'] == 'unanswered'].copy()

    if 'age_hours' in unanswered.columns:
        stale = unanswered[unanswered['age_hours'] > hours_threshold]
    else:
        now = questions['created_at_vn'].max()
        unanswered['age_hours'] = (now - pd.to_datetime(unanswered['created_at_vn'])).dt.total_seconds() / 3600
        stale = unanswered[unanswered['age_hours'] > hours_threshold]

    return stale.sort_values('priority_score', ascending=False)

def get_trending_topics(questions: pd.DataFrame) -> dict:
    """Lấy các chủ đề đang hot (theo intent và thời gian)"""
    # Group by intent và tính tổng priority
    topic_scores = questions.groupby('intent').agg({
        'priority_score': ['sum', 'mean', 'count'],
        'unanswered_bonus': 'mean'
    }).round(2)

    topic_scores.columns = ['total_score', 'avg_score', 'count', 'unanswered_ratio']
    topic_scores = topic_scores.reset_index()

    # Sort by total_score
    topic_scores = topic_scores.sort_values('total_score', ascending=False)

    return topic_scores.to_dict('records')
