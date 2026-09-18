# Discord Q&A Intelligence Pipeline

**Track B2** - Tính năng mới cho Discord | **CP3 - AI Thực Chiến**

## Team

| Phần việc | Người phụ trách |
|---|---|
| Mining data và kiểm chứng evidence | Nguyễn Thị Minh Tiến |
| Thiết kế flow/mock prototype | Phan Thị Khánh Linh |
| Prompt, logic nhóm và xếp hạng | Trương Hoàng Thành An |
| Golden set, test và demo | Phạm Anh Minh |

## Problem Statement

**Pain:** TA/labcoach mất thời gian rà lại Discord, không biết câu hỏi nào đang hot hay còn tồn.

**Lát cắt:** Một TA cuối ngày muốn xử lý câu hỏi tồn trong Discord; AI nhóm các câu hỏi tương tự, xếp hạng mức độ ưu tiên và chỉ ra câu chưa được trả lời sau 4 giờ.

## Pipeline Architecture

```
Discord Messages → Parse & Filter → Intent Classification → Clustering → Response Detection → Scoring → Output
```

| Step | Component | Type |
|------|-----------|------|
| 1 | Input (Discord messages) | ⚙️ Rule |
| 2 | Parse & Filter | ⚙️ Rule |
| 3 | Intent Classification | ✨ AI |
| 4 | Question Clustering | ✨ AI |
| 5 | Response Detection | ⚙️ Rule |
| 6 | Scoring & Ranking | ✨ AI |
| 7 | Output (Leaderboard) | ⚙️ Rule |

## Features

### 4 Slash Commands

- `/leaderboard` - Xem BXH câu hỏi ưu tiên
- `/unanswered` - Câu hỏi chưa trả lời sau 4 giờ
- `/trend` - Chủ đề đang hot
- `/stats` - Xem thống kê pipeline và trạng thái AI

## Evidence

- **1,092 tin nhắn** trong Discord pack (12-14/09/2026)
- **107 câu hỏi** (13.7% trong 779 tin người)
- **87.9% không có reply** ← Pain validated
- 4 bản tin ngày bot đang chạy có lỗi thật

## Evaluation Results

| Metric | Result | Quality Bar |
|--------|--------|-------------|
| Intent Accuracy | 80% (24/30) | ≥80% ✅ |
| Status Detection | 100% (107/107) | ≥85% ✅ |

## Project Structure

```
codebase/
├── main.py          # Main pipeline
├── parser.py       # Step 2: Parse & Filter
├── classifier.py    # Step 3: Intent Classification
├── clusterer.py    # Step 4: Question Clustering
├── detector.py      # Step 5: Response Detection
├── scorer.py       # Step 6: Scoring & Ranking
└── output.py       # Step 7: Output Formatting

eval/
├── golden_set.md   # 30 test cases
├── run_eval.py     # Evaluation script
└── eval_results.json

evidence/
└── mining_results.md
```

## Setup

```bash
# Install dependencies
pip install pandas numpy

# Run the end-to-end demo from the repository root
python demo.py

# Run evaluation
python eval/run_eval.py
```

The demo and evaluator use the Discord CSV at
`data/discord-pack/k4_messages.csv`. This data pack is not included in the
current public repository snapshot; restore it locally before running the
pipeline.

## Quality Bar

- Intent Accuracy ≥ 80%
- Status Detection ≥ 85%
- No hallucination (câu trả lời không căn cứ)

## License

MIT - Chỉ dùng trong khoá AI20k
