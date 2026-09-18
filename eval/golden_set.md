# Golden Set - Discord Q&A Intelligence
# CP3 - AI Thực Chiến

## Structure
Mỗi case có:
- `id`: Mã case
- `input`: Câu hỏi đầu vào
- `expected_intent`: Intent kỳ vọng
- `expected_status`: Status kỳ vọng (answered/unanswered/partial)
- `layer`: Lớp chỗ khó (1-Fact/2-Ambiguous/3-OutOfScope/4-Domain)
- `notes`: Ghi chú

## Golden Set Cases

```json
[
  {
    "id": "GS001",
    "input": "Deadline nộp Lab2 là khi nào vậy ạ?",
    "expected_intent": "deadline_xp",
    "expected_cluster_size": 3,
    "expected_status": "unanswered",
    "layer": 2,
    "notes": "Câu hỏi deadline phổ biến - cần xác nhận ngày cụ thể"
  },
  {
    "id": "GS002",
    "input": "Team mình cần 5 bạn đúng không ạ?",
    "expected_intent": "team",
    "expected_cluster_size": 2,
    "expected_status": "answered",
    "layer": 4,
    "notes": "Câu hỏi về quy tắc cụ thể của khóa - sai sẽ ảnh hưởng đến việc lập team"
  },
  {
    "id": "GS003",
    "input": "CVAT bị lỗi 'nguồn tham chiếu' ở bước 3, phải làm sao?",
    "expected_intent": "lab_technical",
    "expected_cluster_size": 1,
    "expected_status": "unanswered",
    "layer": 1,
    "notes": "Cần căn cứ vào tài liệu lab - AI không nên bịa đáp lỗi cụ thể"
  },
  {
    "id": "GS004",
    "input": "Buổi workshop chủ nhật có điểm danh không ạ?",
    "expected_intent": "schedule",
    "expected_cluster_size": 2,
    "expected_status": "answered",
    "layer": 4,
    "notes": "Quy định cụ thể của khóa"
  },
  {
    "id": "GS005",
    "input": "Mình không biết làm lab, ai giúp mình với?",
    "expected_intent": "support",
    "expected_cluster_size": 1,
    "expected_status": "unanswered",
    "layer": 3,
    "notes": "Câu hỏi mơ hồ - cần xác định rõ lab nào, vấn đề cụ thể gì"
  },
  {
    "id": "GS006",
    "input": "Link repo github của chương trình ở đâu vậy?",
    "expected_intent": "github_phoenix",
    "expected_cluster_size": 1,
    "expected_status": "answered",
    "layer": 1,
    "notes": "Câu hỏi có thể trả lời bằng thông tin có sẵn"
  },
  {
    "id": "GS007",
    "input": "XP bị trừ khi nghỉ buổi workshop có được cộng lại không?",
    "expected_intent": "deadline_xp",
    "expected_cluster_size": 1,
    "expected_status": "unanswered",
    "layer": 4,
    "notes": "Quy định XP - cần căn cứ vào policy của khóa"
  },
  {
    "id": "GS008",
    "input": "Có ai biết thư viện trường ở đâu không?",
    "expected_intent": "other",
    "expected_cluster_size": 1,
    "expected_status": "answered",
    "layer": 1,
    "notes": "Câu hỏi đời thường, không liên quan đến khóa học - cần phân loại other"
  },
  {
    "id": "GS009",
    "input": "Điểm danh trên Zoom hay trên app MyVinUni?",
    "expected_intent": "deadline_xp",
    "expected_cluster_size": 2,
    "expected_status": "answered",
    "layer": 4,
    "notes": "Quy định cụ thể của khóa"
  },
  {
    "id": "GS010",
    "input": "Mình gửi mail cho ai để xin nghỉ buổi học?",
    "expected_intent": "support",
    "expected_cluster_size": 1,
    "expected_status": "answered",
    "layer": 1,
    "notes": "Hỏi quy trình - có thể trả lời"
  },
  {
    "id": "GS011",
    "input": "Lab Coach có thể giải quyết vấn đề kỹ thuật không?",
    "expected_intent": "support",
    "expected_cluster_size": 1,
    "expected_status": "unanswered",
    "layer": 3,
    "notes": "Câu hỏi về thẩm quyền - cần làm rõ vai trò Lab Coach"
  },
  {
    "id": "GS012",
    "input": "Deadline ghép đội là 21:00 ngày nào?",
    "expected_intent": "deadline_xp",
    "expected_cluster_size": 3,
    "expected_status": "answered",
    "layer": 4,
    "notes": "Câu hỏi deadline cụ thể - thông tin có trong thông báo"
  },
  {
    "id": "GS013",
    "input": "Tại sao commit lên github bị lỗi?",
    "expected_intent": "github_phoenix",
    "expected_cluster_size": 1,
    "expected_status": "unanswered",
    "layer": 1,
    "notes": "Cần thông tin lỗi cụ thể để hỗ trợ"
  },
  {
    "id": "GS014",
    "input": "Mình có 4 bạn, thiếu 1 bạn thì có sao không?",
    "expected_intent": "team",
    "expected_cluster_size": 2,
    "expected_status": "answered",
    "layer": 4,
    "notes": "Quy tắc team - cần căn cứ vào quy định"
  },
  {
    "id": "GS015",
    "input": "Workshop buổi 1 có bắt buộc tham gia không?",
    "expected_intent": "schedule",
    "expected_cluster_size": 2,
    "expected_status": "answered",
    "layer": 4,
    "notes": "Quy định cụ thể - có thể trả lời"
  },
  {
    "id": "GS016",
    "input": "Nộp code trên Vlearn nhưng commit lên github bị lỗi thì có bị trừ điểm không?",
    "expected_intent": "deadline_xp",
    "expected_cluster_size": 1,
    "expected_status": "unanswered",
    "layer": 4,
    "notes": "Câu hỏi về edge case - cần quy định rõ ràng"
  },
  {
    "id": "GS017",
    "input": "Có được nghỉ lab nếu đi làm thực tập không?",
    "expected_intent": "schedule",
    "expected_cluster_size": 1,
    "expected_status": "unanswered",
    "layer": 3,
    "notes": "Ngoài phạm vi khóa học - thuộc quy định trường/doanh nghiệp"
  },
  {
    "id": "GS018",
    "input": "Link phoenix bị lỗi, vào không được, phải làm sao?",
    "expected_intent": "onboarding",
    "expected_cluster_size": 1,
    "expected_status": "answered",
    "layer": 1,
    "notes": "Vấn đề kỹ thuật - có thể hỗ trợ"
  },
  {
    "id": "GS019",
    "input": "XP có tính cho các buổi workshop offline không?",
    "expected_intent": "deadline_xp",
    "expected_cluster_size": 2,
    "expected_status": "answered",
    "layer": 4,
    "notes": "Quy tắc XP - cần căn cứ vào policy"
  },
  {
    "id": "GS020",
    "input": "Clone repo rồi nhưng không biết branch nào là đúng?",
    "expected_intent": "github_phoenix",
    "expected_cluster_size": 1,
    "expected_status": "unanswered",
    "layer": 1,
    "notes": "Cần thông tin cụ thể từ tài liệu lab"
  },
  {
    "id": "GS021",
    "input": "Mình nên chọn hướng CV cho bài lab không?",
    "expected_intent": "lab_technical",
    "expected_cluster_size": 1,
    "expected_status": "unanswered",
    "layer": 3,
    "notes": "Câu hỏi tư vấn - ngoài phạm vi tính năng"
  },
  {
    "id": "GS022",
    "input": "Thông báo trên Phoenix có gửi email không?",
    "expected_intent": "onboarding",
    "expected_cluster_size": 1,
    "expected_status": "unanswered",
    "layer": 1,
    "notes": "Câu hỏi về tính năng platform"
  },
  {
    "id": "GS023",
    "input": "Nộp lab muộn 1 phút có được tính không?",
    "expected_intent": "deadline_xp",
    "expected_cluster_size": 1,
    "expected_status": "unanswered",
    "layer": 4,
    "notes": "Edge case - cần quy định rõ"
  },
  {
    "id": "GS024",
    "input": "Có cần fork repo trước khi commit không?",
    "expected_intent": "github_phoenix",
    "expected_cluster_size": 1,
    "expected_status": "answered",
    "layer": 4,
    "notes": "Quy trình kỹ thuật cụ thể"
  },
  {
    "id": "GS025",
    "input": "Lịch học trên email và Outlook khác nhau, tin cái nào?",
    "expected_intent": "schedule",
    "expected_cluster_size": 1,
    "expected_status": "unanswered",
    "layer": 4,
    "notes": "Cần căn cứ vào kênh chính thức của khóa"
  },
  {
    "id": "GS026",
    "input": "Clone repo rồi nhưng không biết branch nào đúng, ai chỉ mình với?",
    "expected_intent": "github_phoenix",
    "expected_cluster_size": 1,
    "expected_status": "unanswered",
    "layer": 1,
    "notes": "Tín hiệu GitHub phải được ưu tiên hơn từ khóa hỗ trợ chung 'chỉ mình'"
  },
  {
    "id": "GS027",
    "input": "Lab bị lỗi, ai hướng dẫn mình cách sửa với?",
    "expected_intent": "lab_technical",
    "expected_cluster_size": 1,
    "expected_status": "unanswered",
    "layer": 1,
    "notes": "Câu hỏi kỹ thuật có từ khóa hỗ trợ, nhưng intent chính là lab_technical"
  },
  {
    "id": "GS028",
    "input": "Cho mình hỏi căn tin trường đóng cửa lúc mấy giờ?",
    "expected_intent": "other",
    "expected_cluster_size": 1,
    "expected_status": "answered",
    "layer": 3,
    "notes": "Câu hỏi ngoài phạm vi khóa học, không nên ép vào schedule"
  },
  {
    "id": "GS029",
    "input": "Bot đã gửi hướng dẫn nhưng mình vẫn chưa hiểu bước này, ai giải thích thêm giúp mình với?",
    "expected_intent": "support",
    "expected_cluster_size": 1,
    "expected_status": "partial",
    "layer": 3,
    "notes": "Có bot reply nhưng chưa chứng minh câu hỏi đã được giải quyết hoàn toàn"
  },
  {
    "id": "GS030",
    "input": "Có bạn trả lời là phải nộp trước 21:00, vậy đã chốt chưa ạ?",
    "expected_intent": "deadline_xp",
    "expected_cluster_size": 1,
    "expected_status": "answered",
    "layer": 2,
    "notes": "Có reply của user nhưng nội dung còn cần xác nhận; dùng làm case kiểm tra status semantics"
  }
]
```

## Quality Dimensions

| Dimension | Definition | Pass Criteria |
|-----------|------------|---------------|
| Intent Accuracy | Đúng intent theo mapping | ≥80% cases |
| Status Detection | Đúng trạng thái trả lời | ≥85% cases |
| Cluster Quality | Câu hỏi tương tự cùng cluster | ≥70% pairs |
| Priority Ranking | Câu hỏi urgent được ưu tiên | Top 5 đúng |

## Quality Bar

**Đạt khi:**
- Intent accuracy ≥ 80%
- Status detection ≥ 85%
- Không có hallucination (câu trả lời không căn cứ)
