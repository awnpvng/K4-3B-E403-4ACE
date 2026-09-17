"""
Discord Q&A Intelligence Pipeline
CP3 - AI Thực Chiến - Track B2

Pipeline: Input → Parse → Intent → Cluster → Detect → Score → Output
"""

import pandas as pd
import os
from datetime import datetime, timedelta
from typing import List, Dict, Tuple
import json

# Import các module
from parser import filter_questions, extract_metadata
from classifier import classify_intent
from clusterer import cluster_questions, get_representative
from detector import detect_response_status
from scorer import calculate_priority_scores
from output import format_leaderboard, format_unanswered, format_trend

# ============================================================
# CONFIG
# ============================================================
DATA_PATH = "data/discord-pack/k4_messages.csv"
OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ============================================================
# MAIN PIPELINE
# ============================================================
def run_pipeline(use_ai: bool = True, sample_size: int = None) -> Dict:
    """
    Chạy pipeline hoàn chỉnh.

    Args:
        use_ai: True = dùng LLM thật, False = mock
        sample_size: None = toàn bộ, int = số lượng sample

    Returns:
        Dict chứa kết quả pipeline
    """
    print("=" * 60)
    print("⚡ DISCORD Q&A INTELLIGENCE PIPELINE")
    print("=" * 60)

    # ===== STEP 1: INPUT =====
    print("\n📥 [STEP 1] Loading messages...")
    df = pd.read_csv(DATA_PATH)
    df['created_at_vn'] = pd.to_datetime(df['created_at_vn'])

    if sample_size:
        df = df.head(sample_size)

    print(f"   Loaded: {len(df)} messages")

    # ===== STEP 2: PARSE & FILTER =====
    print("\n🔧 [STEP 2] Parsing & Filtering...")
    questions = filter_questions(df)
    print(f"   Questions extracted: {len(questions)}")

    # ===== STEP 3: INTENT CLASSIFICATION =====
    print("\n🧠 [STEP 3] Intent Classification...")
    questions = classify_intent(questions, use_ai=use_ai)
    intent_counts = questions['intent'].value_counts()
    print(f"   Intents: {dict(intent_counts)}")

    # ===== STEP 4: QUESTION CLUSTERING =====
    print("\n🧠 [STEP 4] Question Clustering...")
    questions = cluster_questions(questions, use_ai=use_ai)
    clusters = questions['cluster_id'].nunique()
    print(f"   Clusters formed: {clusters}")

    # ===== STEP 5: RESPONSE DETECTION =====
    print("\n💬 [STEP 5] Response Detection...")
    questions = detect_response_status(questions, df)
    status_counts = questions['status'].value_counts()
    print(f"   Status: {dict(status_counts)}")

    # Get representative questions (after status is available)
    questions['representative'] = questions.apply(
        lambda x: get_representative(x, questions), axis=1
    )

    # ===== STEP 6: SCORING & RANKING =====
    print("\n🧠 [STEP 6] Scoring & Ranking...")
    questions = calculate_priority_scores(questions)

    # Sort by priority score
    top_questions = questions.nlargest(10, 'priority_score')
    print(f"   Top priority: {len(top_questions)} questions")

    # ===== STEP 7: OUTPUT =====
    print("\n📤 [STEP 7] Generating Output...")

    results = {
        'all_questions': questions,
        'top_questions': top_questions,
        'leaderboard': format_leaderboard(top_questions),
        'unanswered': format_unanswered(questions[questions['status'] == 'unanswered']),
        'trend': format_trend(questions),
        'stats': {
            'total_messages': len(df),
            'total_questions': len(questions),
            'answered': len(questions[questions['status'] == 'answered']),
            'unanswered': len(questions[questions['status'] == 'unanswered']),
            'clusters': clusters,
        }
    }

    # Save outputs
    save_outputs(results)

    print("\n✅ Pipeline complete!")
    return results

def save_outputs(results: Dict):
    """Lưu kết quả ra file"""
    # Leaderboard
    with open(f"{OUTPUT_DIR}/leaderboard.md", "w", encoding="utf-8") as f:
        f.write(results['leaderboard'])

    # Unanswered questions
    with open(f"{OUTPUT_DIR}/unanswered.md", "w", encoding="utf-8") as f:
        f.write(results['unanswered'])

    # Trend
    with open(f"{OUTPUT_DIR}/trend.md", "w", encoding="utf-8") as f:
        f.write(results['trend'])

    # Stats JSON
    with open(f"{OUTPUT_DIR}/stats.json", "w", encoding="utf-8") as f:
        json.dump(results['stats'], f, indent=2, default=str)

    # Full questions CSV
    results['all_questions'].to_csv(f"{OUTPUT_DIR}/questions_analyzed.csv", index=False)

    print(f"   Saved to {OUTPUT_DIR}/")

# ============================================================
# SLASH COMMANDS (MOCK)
# ============================================================
def cmd_leaderboard():
    """Mock /leaderboard command"""
    results = run_pipeline(sample_size=100)
    print("\n" + results['leaderboard'])

def cmd_unanswered():
    """Mock /unanswered command"""
    results = run_pipeline(sample_size=100)
    print("\n" + results['unanswered'])

def cmd_trend():
    """Mock /trend command"""
    results = run_pipeline(sample_size=100)
    print("\n" + results['trend'])

# ============================================================
# DEMO
# ============================================================
if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == "/leaderboard":
            cmd_leaderboard()
        elif cmd == "/unanswered":
            cmd_unanswered()
        elif cmd == "/trend":
            cmd_trend()
        else:
            print(f"Unknown command: {cmd}")
    else:
        # Run full pipeline
        results = run_pipeline(use_ai=True)
        print("\n" + "=" * 60)
        print("📊 FINAL RESULTS")
        print("=" * 60)
        print(results['leaderboard'])
