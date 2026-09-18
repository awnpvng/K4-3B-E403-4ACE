"""
STEP 7: Output Formatting
- Leaderboard: Top câu hỏi ưu tiên
- Unanswered: Câu hỏi chưa trả lời
- Trend: Chủ đề đang hot
"""

import pandas as pd
from typing import List, Dict
from datetime import datetime

def format_leaderboard(questions: pd.DataFrame) -> str:
    """
    Format leaderboard câu hỏi.

    Output mẫu:
    # 📊 Leaderboard - Câu hỏi ưu tiên

    ## Top 10 câu hỏi cần xử lý

    | # | Priority | Intent | Câu hỏi | Status | Answered |
    |---|----------|--------|---------|--------|----------|
    | 1 | 8.5 | deadline_xp | "Deadline nộp lab..." | ⚠️ Unanswered | — |
    """
    output = ["# 📊 Leaderboard - Câu hỏi ưu tiên\n"]
    output.append("## Top câu hỏi cần xử lý\n")

    if len(questions) == 0:
        output.append("_Không có câu hỏi nào_")
        return '\n'.join(output)

    # Header
    output.append("| # | Priority | Intent | Câu hỏi | Status | Answered | Link |")
    output.append("|---|----------|--------|---------|--------|----------|------|")

    for i, (idx, row) in enumerate(questions.iterrows(), 1):
        # Truncate question
        question = row['content'][:60] + "..." if len(str(row['content'])) > 60 else row['content']

        # Status icon
        status_icon = {
            'unanswered': '❌ Unanswered',
            'partial': '⚠️ Partial',
            'answered': '✅ Answered'
        }.get(row.get('status', 'unknown'), '❓')

        # Intent label
        intent_label = row.get('intent', 'unknown').replace('_', ' ')

        # Link placeholder
        link = f"[→](https://discord.com/msg/{row['msg_id']})"
        answer = str(row.get('answered', '') or '—')
        if len(answer) > 100:
            answer = answer[:100] + "..."

        output.append(f"| {i} | {row.get('priority_score', 0):.1f} | {intent_label} | {question} | {status_icon} | {answer} | {link} |")

    # Stats
    output.append("\n---\n")
    output.append(f"_Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}_")

    return '\n'.join(output)

def format_unanswered(questions: pd.DataFrame, hours_threshold: int = 4) -> str:
    """
    Format danh sách câu hỏi chưa trả lời.

    MOCK: Thời gian không đầy đủ trong data nên dùng msg_id thay link
    """
    output = ["# ❌ Câu hỏi chưa được trả lời\n"]
    output.append(f"_Sau {hours_threshold}+ giờ_\n")

    if len(questions) == 0:
        output.append("_Tuyệt vời! Không có câu hỏi nào tồn._")
        return '\n'.join(output)

    # Group by intent
    for intent in questions['intent'].unique():
        intent_qs = questions[questions['intent'] == intent]

        output.append(f"\n## {intent.replace('_', ' ').title()} ({len(intent_qs)})\n")

        for idx, row in intent_qs.iterrows():
            question = row['content'][:100]
            if len(str(row['content'])) > 100:
                question += "..."

            output.append(f"- **ID: {row['msg_id']}** | {question}")

    output.append("\n---\n")
    output.append(f"_Total: {len(questions)} câu hỏi chưa trả lời_\n")
    output.append(f"_Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}_")

    return '\n'.join(output)

def format_trend(questions: pd.DataFrame) -> str:
    """
    Format xu hướng chủ đề.

    Output mẫu:
    # 🔥 Trend - Chủ đề đang hot

    ## Top topics

    1. **deadline_xp** - 12 câu hỏi, điểm TB: 5.2
    2. **team** - 8 câu hỏi, điểm TB: 4.1
    """
    output = ["# 🔥 Trend - Chủ đề đang hot\n"]

    if len(questions) == 0:
        output.append("_Không có dữ liệu_")
        return '\n'.join(output)

    # Calculate trend scores
    topic_stats = questions.groupby('intent').agg({
        'msg_id': 'count',
        'priority_score': ['sum', 'mean']
    }).round(2)

    topic_stats.columns = ['count', 'total_score', 'avg_score']
    topic_stats = topic_stats.reset_index()
    topic_stats = topic_stats.sort_values('total_score', ascending=False)

    output.append("## Top chủ đề\n")

    emoji_map = {
        'deadline_xp': '⏰',
        'team': '👥',
        'lab_technical': '💻',
        'schedule': '📅',
        'support': '❓',
        'github_phoenix': '🔧',
        'onboarding': '🎯',
        'unclassified': '❓'
    }

    for i, row in topic_stats.iterrows():
        emoji = emoji_map.get(row['intent'], '📌')
        label = row['intent'].replace('_', ' ').title()

        output.append(
            f"{emoji} **{label}**\n"
            f"   - {int(row['count'])} câu hỏi\n"
            f"   - Điểm ưu tiên TB: {row['avg_score']:.1f}\n"
        )

    output.append("\n---\n")
    output.append(f"_Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}_")

    return '\n'.join(output)

def format_for_discord(results: Dict) -> str:
    """
    Format output cho Discord embed.
    """
    # Mock Discord embed
    embed = {
        "title": "📊 Q&A Intelligence Report",
        "description": "Tổng hợp câu hỏi từ Discord",
        "fields": [
            {
                "name": "Tổng câu hỏi",
                "value": str(results['stats']['total_questions']),
                "inline": True
            },
            {
                "name": "Đã trả lời",
                "value": str(results['stats']['answered']),
                "inline": True
            },
            {
                "name": "Chưa trả lời",
                "value": str(results['stats']['unanswered']),
                "inline": True
            }
        ]
    }

    return str(embed)
