# Evidence - Mining Results
# CP3 - AI Thực Chiến - Track B2

## Method
Phân tích data: `data/discord-pack/k4_messages.csv`
- Tool: Python pandas
- Date: 2024-09-17
- Total messages analyzed: 1,092

## Mining Results

### 1. Overview
| Metric | Value |
|--------|-------|
| Total messages | 1,092 |
| Human messages | 779 (71.3%) |
| Bot messages | 313 (28.7%) |
| Unique authors | 202 |

### 2. Questions Analysis
| Metric | Value |
|--------|-------|
| Questions (with "?") | 107 |
| Questions rate | 13.7% of human messages |
| Answered | 13 (12.1%) |
| Unanswered | 94 (87.9%) |
| Partial | 0 |

**Finding:** 87.9% questions have NO reply - significant pain point

### 3. Intent Distribution
| Intent | Count | % |
|--------|-------|---|
| deadline_xp | 32 | 29.9% |
| team | 29 | 27.1% |
| support | 27 | 25.2% |
| schedule | 16 | 15.0% |
| lab_technical | 13 | 12.1% |
| github_phoenix | 8 | 7.5% |
| onboarding | 5 | 4.7% |
| unclassified | 3 | 2.8% |

### 4. Unanswered Questions Examples (5+ quotes)

**Quote 1:** 
- ID: M99769
- Time: 2026-09-12 18:57
- Content: "[@D7688] cho mình hỏi một team mấy bạn?"
- Intent: team

**Quote 2:**
- ID: M67317
- Time: 2026-09-12 21:54
- Content: "2b vs 2a vẫn join chung được luôn ạ ?"
- Intent: team

**Quote 3:**
- ID: M76498
- Time: 2026-09-13 15:30
- Content: "Sổ tay học viên https://drive.google.com/..."
- Intent: support

**Quote 4:**
- ID: M71241
- Time: 2026-09-13 23:05
- Content: "[@D3694] anh ơi cái repo này là template đúng không ạ https://github.com/..."
- Intent: github_phoenix

**Quote 5:**
- ID: M63574
- Time: 2026-09-12 11:06
- Content: "A ơi, cho e hỏi, buổi workshop chủ nhật ngày mai thì có tính vào số buổi nghỉ ko ạ? Giả dụ sáng mai e có việc thì sao ạ?"
- Intent: schedule

### 5. Daily Report Issues (from k4_daily_reports.md)

**Issue 1: Nguồn tham chiếu bug**
- Location: K4-L2-3 · bản tin 2026-09-14
- Problem: Text corruption "nguồn tham chiếuhi" inserted in middle of words
- Example: "lỗi nguồn tham chiếuhi chạy bước 3"

**Issue 2: Truncated summaries**
- Location: K4-L2-3 · bản tin 2026-09-13
- Problem: Summary ends mid-sentence "...Một số câu hỏi chưa được giải đá"
- Missing: Complete information

**Issue 3: Unverified "Đã có phản hồi"**
- Location: Multiple reports
- Problem: Bot claims "Đã có phản hồi" without verification
- Example: "Đã có phản hồi, chưa xác nhận đã xử lý"

**Issue 4: No priority ranking**
- Problem: Questions listed without priority score
- TA cannot quickly identify urgent questions

## Pain Points Validated

| Pain | Evidence | Source |
|------|----------|--------|
| Questions not getting answers | 87.9% unanswered | k4_messages.csv |
| No priority ranking | Reports lack ranking | k4_daily_reports.md |
| Similar questions repeated | Multiple "team size" questions | k4_messages.csv |
| Summary truncation | Incomplete reports | k4_daily_reports.md |

## Conclusion

Evidence supports the problem statement:
- TA needs to manually scan 1,092 messages to find unanswered questions
- Current daily reports are incomplete and unprioritized
- 87.9% of questions remain unanswered in the dataset
