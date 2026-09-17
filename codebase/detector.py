"""
STEP 5: Response Detection
- Check reply_to có reply chưa
- Kiểm tra role của người reply (Bot | TA | Mod | User)
"""

import pandas as pd
from typing import Dict, List

def detect_response_status(questions: pd.DataFrame, all_messages: pd.DataFrame) -> pd.DataFrame:
    """
    Phát hiện trạng thái trả lời của câu hỏi.

    Status:
    - answered: có reply từ người khác
    - partial: có reply nhưng có thể chưa giải quyết
    - unanswered: không có reply
    """
    questions = questions.copy()
    questions['status'] = 'unanswered'
    questions['replier_role'] = None
    questions['reply_time_hours'] = None

    # Parse time
    all_messages['created_at_vn'] = pd.to_datetime(all_messages['created_at_vn'])
    questions['created_at_vn'] = pd.to_datetime(questions['created_at_vn'])

    for idx, row in questions.iterrows():
        msg_id = row['msg_id']

        # Tìm các tin nhắn reply tới msg_id này
        replies = all_messages[all_messages['reply_to'] == msg_id]

        if len(replies) == 0:
            # Không có reply
            questions.at[idx, 'status'] = 'unanswered'
            continue

        # Có reply - kiểm tra loại
        replier = replies.iloc[0]

        if replier['is_bot']:
            questions.at[idx, 'status'] = 'partial'
            questions.at[idx, 'replier_role'] = 'bot'
        else:
            questions.at[idx, 'status'] = 'answered'
            questions.at[idx, 'replier_role'] = 'user'

        # Tính thời gian reply
        reply_time = replier['created_at_vn']
        question_time = row['created_at_vn']
        hours = (reply_time - question_time).total_seconds() / 3600
        questions.at[idx, 'reply_time_hours'] = round(hours, 1)

    return questions

def get_status_distribution(questions: pd.DataFrame) -> Dict:
    """Thống kê phân bố status"""
    status_counts = questions['status'].value_counts()

    # Tính tỷ lệ unanswered sau N giờ
    unanswered = questions[questions['status'] == 'unanswered']
    if len(unanswered) > 0:
        # Giả định: câu hỏi mới hơn 4 giờ không tính là "tồn"
        now = questions['created_at_vn'].max()
        unanswered['age_hours'] = (now - unanswered['created_at_vn']).dt.total_seconds() / 3600
        stale_4h = len(unanswered[unanswered['age_hours'] > 4])
    else:
        stale_4h = 0

    return {
        'answered': int(status_counts.get('answered', 0)),
        'partial': int(status_counts.get('partial', 0)),
        'unanswered': int(status_counts.get('unanswered', 0)),
        'stale_4h': stale_4h
    }
