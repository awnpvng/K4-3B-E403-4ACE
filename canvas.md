
## Track, đề

**Track B - B2: Tính năng mới cho TA/học viên trong Discord.**

## Job executor

**Một TA/labcoach vào cuối ngày, trong server Discord chung, cần biết câu hỏi nào đang nóng và câu nào chưa được trả lời để chọn việc cần xử lý trước.**

## Pain một câu

**TA/labcoach đang rà lại nhiều tin nhắn Discord, nhưng không biết câu hỏi nào bị lặp hoặc còn tồn, nên mất thời gian tổng hợp và có thể bỏ sót câu hỏi cần trả lời sớm.**

## 1-2 bằng chứng đầu

1. **1.092 tin nhắn** trong Discord pack giai đoạn 12-14/09/2026, gồm **779 tin từ người và 313 tin từ bot**. Cách đếm: đọc `k4_messages.csv`, đếm tổng số dòng dữ liệu và nhóm theo cột `is_bot`.
2. Pack có **4 bản tin ngày** do bot đang chạy thật. Khi đối chiếu `k4_daily_reports.md`, bản tin có lỗi tóm tắt/cắt cụt và chưa cho TA một thứ hạng rõ ràng giữa câu hỏi nóng với câu hỏi chưa được trả lời.

## Lát cắt MỘT CÂU

**Một TA cuối ngày muốn xử lý câu hỏi tồn trong Discord; AI nhóm các câu hỏi tương tự, xếp hạng mức độ ưu tiên và chỉ ra câu chưa được trả lời sau 4 giờ; TA nhận được danh sách ưu tiên kèm link tin nhắn để trả lời.**

## AI tự làm đến đâu

**AI tự nhóm câu hỏi tương tự, đếm số lần lặp, phát hiện câu chưa có phản hồi và xếp hạng ưu tiên; AI không tự gửi tin nhắn, không nêu danh tính học viên và không quyết định thay TA vì mọi hành động phản hồi cần người duyệt.**

Willing users dự kiến: **[Tên TA/labcoach 1]**, **[Tên TA/labcoach 2]**, **[Tên học viên/TA 3]** đồng ý thử prototype ngoài nhóm.

## Phân công có tên

| Phần việc                           | Người phụ trách       |
| ------------------------------------- | ------------------------- |
| Mining data và kiểm chứng evidence | Nguyễn Thị Minh Tiến   |
| Thiết kế flow/mock prototype        | Phan Thị Khánh Linh     |
| Prompt, logic nhóm và xếp hạng    | Trương Hoàng Thành An |
| Golden set, test và demo             | Phạm Anh Minh            |
