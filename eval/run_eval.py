"""
Evaluation Script - Run Golden Set
CP3 - AI Thực Chiến

Usage:
    python eval/run_eval.py

Output:
    - eval_results.json: Full evaluation results
    - logs/ai_calls.jsonl: LLM call logs (for proof of real AI calls)
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'codebase'))

import pandas as pd
import json
import re
from datetime import datetime

# Import modules
from parser import filter_questions
from classifier import classify_intent, INTENT_PATTERNS
from detector import detect_response_status
from ai import is_configured, call_llm

# ============================================================
# GOLDEN SET CASES (INTENT)
# ============================================================

def load_golden_set():
    """Load the JSON block maintained in eval/golden_set.md."""
    golden_set_path = os.path.join(os.path.dirname(__file__), "golden_set.md")
    with open(golden_set_path, "r", encoding="utf-8") as file:
        markdown = file.read()

    match = re.search(r"```json\s*(\[.*?\])\s*```", markdown, re.DOTALL)
    if match is None:
        raise ValueError(f"Could not find JSON golden set in {golden_set_path}")

    cases = json.loads(match.group(1))
    required_fields = {"id", "input", "expected_intent", "layer"}
    for case in cases:
        missing_fields = required_fields - set(case)
        if missing_fields:
            missing = ", ".join(sorted(missing_fields))
            raise ValueError(f"Golden set case {case.get('id', '<unknown>')} is missing: {missing}")

    return cases


GOLDEN_SET = load_golden_set()

# ============================================================
# INTENT EVALUATION
# ============================================================

def classify_single(question: str) -> str:
    """Classify single question using rule-based approach with priority."""
    from classifier import classify_single as rule_classify
    return rule_classify(question)

def evaluate_intent_classification():
    """Evaluate intent classification accuracy"""
    results = []
    for case in GOLDEN_SET:
        predicted = classify_single(case["input"])
        expected = case["expected_intent"]
        correct = predicted == expected
        results.append({
            "id": case["id"],
            "input": case["input"][:50],
            "expected": expected,
            "predicted": predicted,
            "correct": correct,
            "layer": case["layer"]
        })
    return results

# ============================================================
# STATUS DETECTION EVALUATION (DATA THẬT)
# ============================================================

def evaluate_status_detection():
    """
    Status detection: Đánh giá trên DATA THẬT từ CSV

    Logic detector:
    - questions có msg_id
    - Detector tìm: all_messages có reply_to == msg_id (tức có ai reply tới question)
    """
    # Load data thật
    DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "discord-pack", "k4_messages.csv")
    df = pd.read_csv(DATA_PATH)

    # Extract questions
    questions = filter_questions(df)

    # Run status detection
    questions_with_status = detect_response_status(questions, df)

    # Check: với mỗi question, detector có đúng không?
    correct = 0
    total = len(questions_with_status)

    for idx, row in questions_with_status.iterrows():
        msg_id = row['msg_id']

        # Ground truth: có tin nhắn nào reply tới msg_id này không?
        has_actual_replies = len(df[df['reply_to'] == msg_id]) > 0

        # Detector nói gì?
        detected_status = row['status']

        # Check:
        # - Nếu has_actual_replies = True → detector phải nói answered hoặc partial
        # - Nếu has_actual_replies = False → detector phải nói unanswered
        if has_actual_replies:
            is_correct = detected_status in ['answered', 'partial']
        else:
            is_correct = detected_status == 'unanswered'

        if is_correct:
            correct += 1

    accuracy = correct / total * 100 if total > 0 else 0

    # Count ground truth
    has_replies = sum(1 for idx, row in questions_with_status.iterrows()
                      if len(df[df['reply_to'] == row['msg_id']]) > 0)
    no_replies = total - has_replies

    print(f"\n📊 Status Detection Logic Check:")
    print(f"   Total questions: {total}")
    print(f"   Questions with replies: {has_replies}")
    print(f"   Questions without replies: {no_replies}")
    print(f"   Correct: {correct}/{total} ({accuracy:.1f}%)")

    results = [{
        "total": total,
        "correct": correct,
        "accuracy": accuracy,
        "has_replies": has_replies,
        "no_replies": no_replies
    }]

    return results, accuracy

# ============================================================
# MAIN EVALUATION
# ============================================================

def run_evaluation():
    print("=" * 70)
    print("📊 EVALUATION - DISCORD Q&A INTELLIGENCE")
    print("=" * 70)
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"Total intent test cases: {len(GOLDEN_SET)}")
    print()

    # 1. Intent Classification
    print("=" * 70)
    print("1️⃣ INTENT CLASSIFICATION EVALUATION")
    print("=" * 70)

    intent_results = evaluate_intent_classification()

    correct_intent = sum(1 for r in intent_results if r["correct"])
    accuracy_intent = correct_intent / len(intent_results) * 100

    print(f"\n📈 Overall Intent Accuracy: {accuracy_intent:.1f}% ({correct_intent}/{len(intent_results)})")

    # Per-layer accuracy
    layer_accuracy = {}
    for r in intent_results:
        layer = r["layer"]
        if layer not in layer_accuracy:
            layer_accuracy[layer] = {"correct": 0, "total": 0}
        layer_accuracy[layer]["total"] += 1
        if r["correct"]:
            layer_accuracy[layer]["correct"] += 1

    print("\n📊 Per-Layer Accuracy (4 lớp chỗ khó):")
    layer_names = {1: "Fact", 2: "Ambiguous", 3: "OutOfScope", 4: "Domain"}
    for layer in sorted(layer_accuracy.keys()):
        stats = layer_accuracy[layer]
        pct = stats["correct"] / stats["total"] * 100 if stats["total"] > 0 else 0
        bar = "█" * int(pct / 10) + "░" * (10 - int(pct / 10))
        print(f"   Layer {layer} ({layer_names.get(layer, 'Unknown'):12}) {bar} {stats['correct']}/{stats['total']} ({pct:.0f}%)")

    # 2. Status Detection (dùng data thật)
    print("\n" + "=" * 70)
    print("2️⃣ STATUS DETECTION EVALUATION (DATA THẬT)")
    print("=" * 70)

    status_results, accuracy_status = evaluate_status_detection()

    # 3. Quality Bar Check
    print("\n" + "=" * 70)
    print("🎯 QUALITY BAR CHECK")
    print("=" * 70)

    quality_bar = {"intent_accuracy": 80, "status_detection": 85}

    print(f"\nQuality Bar: Intent ≥ {quality_bar['intent_accuracy']}%, Status ≥ {quality_bar['status_detection']}%")

    if accuracy_intent >= quality_bar["intent_accuracy"]:
        print(f"✅ Intent Accuracy: {accuracy_intent:.1f}% >= {quality_bar['intent_accuracy']}%")
    else:
        print(f"❌ Intent Accuracy: {accuracy_intent:.1f}% < {quality_bar['intent_accuracy']}%")

    if accuracy_status >= quality_bar["status_detection"]:
        print(f"✅ Status Detection: {accuracy_status:.1f}% >= {quality_bar['status_detection']}%")
    else:
        print(f"❌ Status Detection: {accuracy_status:.1f}% < {quality_bar['status_detection']}%")

    # Save results
    results = {
        "timestamp": datetime.now().isoformat(),
        "summary": {
            "total_intent_cases": len(GOLDEN_SET),
            "intent_accuracy": accuracy_intent,
            "status_accuracy": accuracy_status,
            "correct_intent": correct_intent
        },
        "quality_bar": quality_bar,
        "per_layer": layer_accuracy,
        "intent_cases": intent_results,
        "status_summary": status_results[0]
    }

    output_path = os.path.join(os.path.dirname(__file__), "eval_results.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"\n📁 Results saved to: {output_path}")

    return results

if __name__ == "__main__":
    results = run_evaluation()
