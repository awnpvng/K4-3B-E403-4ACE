"""
STEP 4: Question Clustering
- Semantic similarity trên text
- Merge câu hỏi tương tự
- Trích representative question
"""

import pandas as pd
from typing import Dict, List
from collections import Counter
import re

# Mock similarity matrix (thay bằng embedding cosine similarity khi có API)
SIMILARITY_THRESHOLD = 0.7

def cluster_questions(questions: pd.DataFrame, use_ai: bool = True) -> pd.DataFrame:
    """
    Nhóm câu hỏi tương tự thành clusters.

    Args:
        questions: DataFrame câu hỏi đã phân loại intent
        use_ai: True = dùng semantic similarity, False = keyword matching

    Returns:
        DataFrame với cột 'cluster_id' thêm vào
    """
    questions = questions.copy()
    questions['cluster_id'] = None
    questions['similarity_key'] = questions['content'].apply(normalize_for_clustering)

    cluster_id = 0

    for idx, row in questions.iterrows():
        if questions.at[idx, 'cluster_id'] is not None:
            continue

        # Tìm các câu hỏi tương tự
        similar = find_similar(questions, idx, use_ai=use_ai)

        # Gán cluster_id
        questions.at[idx, 'cluster_id'] = cluster_id
        for sim_idx in similar:
            questions.at[sim_idx, 'cluster_id'] = cluster_id

        cluster_id += 1

    # Đếm cluster size
    cluster_sizes = questions.groupby('cluster_id').size()
    questions['cluster_size'] = questions['cluster_id'].map(cluster_sizes)

    return questions

def normalize_for_clustering(text: str) -> str:
    """Chuẩn hóa text để so sánh"""
    if pd.isna(text):
        return ""

    # Lowercase
    text = text.lower()

    # Remove special chars
    text = re.sub(r'[^\w\s]', ' ', text)

    # Normalize whitespace
    text = ' '.join(text.split())

    return text

def find_similar(questions: pd.DataFrame, idx: int, use_ai: bool = True) -> List[int]:
    """
    Tìm các câu hỏi tương tự với câu hỏi tại idx.
    """
    if use_ai:
        # TODO: Dùng embedding similarity (OpenAI/Gemini)
        # Hiện tại mock bằng exact match và keyword overlap
        pass

    # Rule-based similarity
    current = questions.loc[idx, 'similarity_key']
    current_intent = questions.loc[idx, 'intent']
    similar_indices = []

    for i, row in questions.iterrows():
        if i == idx or questions.at[i, 'cluster_id'] is not None:
            continue

        # Same intent = potential cluster
        if row['intent'] == current_intent:
            # Check keyword overlap
            current_words = set(current.split())
            row_words = set(row['similarity_key'].split())

            if len(current_words) > 0:
                overlap = len(current_words & row_words) / len(current_words)
                if overlap >= 0.3:
                    similar_indices.append(i)

    return similar_indices

def get_representative(row: pd.Series, questions: pd.DataFrame) -> str:
    """
    Trích câu hỏi đại diện cho cluster.
    - Ưu tiên: đã trả lời > chưa trả lời
    - Độ dài vừa phải
    """
    cluster_id = row['cluster_id']
    cluster_questions = questions[questions['cluster_id'] == cluster_id]

    # Ưu tiên câu đã trả lời
    answered = cluster_questions[cluster_questions['status'] == 'answered']
    if len(answered) > 0:
        # Chọn câu ngắn nhất trong answered
        rep = answered.nsmallest(1, 'n_chars').iloc[0]
        return rep['content'][:200]

    # Chọn câu ngắn nhất chưa trả lời
    rep = cluster_questions.nsmallest(1, 'n_chars').iloc[0]
    return rep['content'][:200]

def get_cluster_summary(questions: pd.DataFrame) -> List[Dict]:
    """Tóm tắt các clusters"""
    clusters = []

    for cluster_id in questions['cluster_id'].unique():
        if pd.isna(cluster_id):
            continue

        cluster = questions[questions['cluster_id'] == cluster_id]

        clusters.append({
            'cluster_id': int(cluster_id),
            'size': len(cluster),
            'intent': cluster['intent'].iloc[0],
            'representative': cluster['content'].iloc[0][:100],
            'unanswered_count': len(cluster[cluster['status'] == 'unanswered']),
            'avg_priority': cluster['priority_score'].mean() if 'priority_score' in cluster.columns else 0
        })

    # Sort by priority
    clusters.sort(key=lambda x: x['avg_priority'], reverse=True)

    return clusters
