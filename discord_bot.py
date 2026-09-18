"""
Discord Bot - Discord Q&A Intelligence
Dùng discord.py với pipeline đã có

Setup:
1. pip install discord.py python-dotenv pandas
2. Tạo .env với DISCORD_BOT_TOKEN
3. python3 discord_bot.py
"""

import os
import sys

# Load .env
from dotenv import load_dotenv
load_dotenv()

import discord
from discord import app_commands

# Import pipeline - add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from parser import filter_questions
from classifier import classify_intent
from clusterer import cluster_questions
from detector import detect_response_status
from scorer import calculate_priority_scores, get_top_questions, get_unanswered_urgent, get_trending_topics
from ai import is_configured

# Load data
import pandas as pd

DATA_PATH = "data/discord-pack/k4_messages.csv"
print(f"Loading data from {DATA_PATH}...")
df = pd.read_csv(DATA_PATH)
df['created_at_vn'] = pd.to_datetime(df['created_at_vn'])

# Extract questions
questions = filter_questions(df)
questions = classify_intent(questions, use_ai=False)  # Rule-based for speed
questions = cluster_questions(questions, use_ai=False)
questions = detect_response_status(questions, df)
questions = calculate_priority_scores(questions)
print(f"Loaded {len(questions)} questions")

# Discord bot setup
DISCORD_TOKEN = os.environ.get("DISCORD_BOT_TOKEN", "")

if not DISCORD_TOKEN:
    print("ERROR: DISCORD_BOT_TOKEN not set in .env")
    print("Get token from https://discord.com/developers/applications")
    sys.exit(1)

intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)
tree = app_commands.CommandTree(bot)

# ============================================================
# SLASH COMMANDS
# ============================================================

@bot.event
async def on_ready():
    await tree.sync()
    print(f"Bot logged in as {bot.user}")
    print(f"AI configured: {is_configured()}")
    print("Commands: /leaderboard, /unanswered, /trend, /stats")

@tree.command(name="leaderboard", description="Xem bảng xếp hạng câu hỏi ưu tiên")
async def leaderboard(interaction: discord.Interaction):
    await interaction.response.defer()

    top = get_top_questions(questions, n=10)

    embed = discord.Embed(
        title="📊 Leaderboard - Câu hỏi ưu tiên",
        color=discord.Color.blue()
    )

    for i, (_, row) in enumerate(top.iterrows(), 1):
        status_emoji = {"unanswered": "❌", "partial": "⚠️", "answered": "✅"}.get(row['status'], "❓")

        question = row['content'][:60] + "..." if len(str(row['content'])) > 60 else row['content']

        embed.add_field(
            name=f"#{i} {status_emoji} {str(row['intent']).replace('_', ' ').title()}",
            value=f"```{question}```\n⏱️ Score: {row['priority_score']:.1f}",
            inline=False
        )

    embed.set_footer(text=f"Total: {len(questions)} questions | AI: {'On' if is_configured() else 'Off'}")

    await interaction.followup.send(embed=embed)

@tree.command(name="unanswered", description="Xem câu hỏi chưa được trả lời sau N giờ")
async def unanswered(interaction: discord.Interaction, hours: int = 4):
    await interaction.response.defer()

    stale = get_unanswered_urgent(questions, hours_threshold=hours)

    embed = discord.Embed(
        title=f"❌ Câu hỏi chưa trả lời (>{hours}h)",
        color=discord.Color.red()
    )

    if len(stale) == 0:
        embed.description = "🎉 Không có câu hỏi nào tồn đọng!"
    else:
        for intent in stale['intent'].unique()[:5]:
            intent_qs = stale[stale['intent'] == intent]
            value = "\n".join([f"• {str(q['content'])[:50]}..." for _, q in intent_qs.head(3).iterrows()])
            embed.add_field(
                name=f"**{str(intent).replace('_', ' ').title()}** ({len(intent_qs)})",
                value=value or "...",
                inline=False
            )

    embed.set_footer(text=f"Unanswered: {len(stale)}/{len(questions)}")
    await interaction.followup.send(embed=embed)

@tree.command(name="trend", description="Xem chủ đề đang hot")
async def trend(interaction: discord.Interaction):
    await interaction.response.defer()

    topics = get_trending_topics(questions)

    embed = discord.Embed(
        title="🔥 Trend - Chủ đề đang hot",
        color=discord.Color.orange()
    )

    emoji_map = {
        'deadline_xp': '⏰', 'team': '👥', 'lab_technical': '💻',
        'schedule': '📅', 'support': '❓', 'github_phoenix': '🔧',
        'onboarding': '🎯', 'other': '📌'
    }

    for topic in topics[:6]:
        emoji = emoji_map.get(str(topic['intent']), '📌')
        embed.add_field(
            name=f"{emoji} {str(topic['intent']).replace('_', ' ').title()}",
            value=f"📊 {int(topic['count'])} câu | ⏱️ Avg score: {topic['avg_score']:.1f}",
            inline=True
        )

    await interaction.followup.send(embed=embed)

@tree.command(name="stats", description="Xem thống kê tổng quan")
async def stats(interaction: discord.Interaction):
    await interaction.response.defer()

    status_counts = questions['status'].value_counts()

    embed = discord.Embed(
        title="📈 Thống kê Discord Q&A",
        color=discord.Color.green()
    )

    embed.add_field(name="📝 Tổng câu hỏi", value=str(len(questions)), inline=True)
    embed.add_field(name="✅ Đã trả lời", value=str(int(status_counts.get('answered', 0))), inline=True)
    embed.add_field(name="⚠️ Partial", value=str(int(status_counts.get('partial', 0))), inline=True)
    embed.add_field(name="❌ Chưa trả", value=str(int(status_counts.get('unanswered', 0))), inline=True)
    embed.add_field(name="🔮 AI Mode", value="✅ On" if is_configured() else "❌ Off", inline=True)
    embed.add_field(name="🤖 Model", value=os.environ.get("MODEL", "qwen3.7-flash"), inline=True)

    await interaction.followup.send(embed=embed)

# ============================================================
# RUN BOT
# ============================================================

if __name__ == "__main__":
    print("=" * 50)
    print("Discord Q&A Intelligence Bot")
    print("=" * 50)
    print(f"Token: {'Set' if DISCORD_TOKEN else 'Not set'}")
    print(f"AI: {'Configured' if is_configured() else 'Not configured'}")
    print()
    print("Commands:")
    print("  /leaderboard - Top priority questions")
    print("  /unanswered  - Unanswered questions")
    print("  /trend       - Hot topics")
    print("  /stats       - Statistics")
    print("=" * 50)

    bot.run(DISCORD_TOKEN)
