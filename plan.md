# Kế hoạch sau CP1 và CP2

## Bối cảnh đã chốt

- **Track:** B2 - Tính năng mới cho TA/học viên trong Discord.
- **Người dùng chính:** TA/labcoach vào cuối ngày.
- **Lát cắt:** AI nhóm các câu hỏi tương tự, đếm số lần lặp, xếp hạng ưu tiên và chỉ ra câu hỏi chưa được trả lời sau 4 giờ; TA nhận danh sách ưu tiên kèm link tin nhắn để xử lý.
- **Giới hạn:** AI chỉ gợi ý và xếp hạng; không tự gửi tin nhắn, không nêu danh tính học viên và không quyết định thay TA.
- **CP1/CP2 (đã hoàn thành):** Canvas đã có trong `canvas.md`; luồng chính đã được xác định ở CP2. Từ đây tập trung vào AI chạy thật, đo lường và chốt spec.

## CP3 - Video thao tác và số đo

**Hạn nộp:** 16:00 ngày 18/09/2026.

### Việc cần làm

1. **Hoàn thiện prototype theo một luồng end-to-end**

   - Nhập/chọn các tin nhắn Discord.
   - AI nhóm các câu hỏi tương tự.
   - Hiển thị số lần lặp và mức ưu tiên.
   - Phát hiện câu chưa có phản hồi sau 4 giờ.
   - Hiển thị link tin nhắn để TA mở và tự trả lời.
   - Có trạng thái không chắc chắn hoặc không đủ căn cứ để không đoán bừa.
2. **Tích hợp ít nhất một lời gọi AI thật**

   - Lời gọi AI phải nằm ở quyết định trung tâm: phân nhóm câu hỏi, tóm tắt hoặc xếp hạng ưu tiên.
   - Không hardcode toàn bộ kết quả demo.
   - Ghi rõ phần nào là AI thật, phần nào là mock; lưu log/trace cần thiết trong repo.
   - Không đưa nguyên data pack hoặc thông tin định danh lên repo công khai; chỉ dùng mã tin nhắn và trích dẫn ngắn.
3. **Xây golden set tối thiểu 20 case trong `eval/` (đã hoàn thành)**

   - Ít nhất 10 case lấy hoặc phát triển từ Discord pack.
   - Ít nhất 2 case cho mỗi lớp chỗ khó:
     - Câu hỏi giống nhau nhưng viết khác cách.
     - Câu hỏi đã được trả lời trong thread khác.
     - Tin nhắn của bot bị nhận nhầm là câu hỏi.
     - Một người gửi lặp lại nhiều lần.
   - Bổ sung 8-10 case thường và 2-4 case hiếm/chỗ khó.
   - Mỗi case có mã, input, output kỳ vọng và tiêu chí đạt/trượt.
4. **Chốt cách chấm trước khi chạy (đã hoàn thành)**

   - Đúng nhóm/chủ đề câu hỏi.
   - Đếm đúng số lần lặp, không tính nhầm tin bot.
   - Nhận diện đúng trạng thái đã trả lời/chưa trả lời sau 4 giờ.
   - Ưu tiên hợp lý và có link/mã tin để TA kiểm tra.
   - Nếu thiếu căn cứ thì đánh dấu không chắc/chuyển TA, không bịa.
5. **Chạy lượt đo đầu trên toàn bộ golden set (đã hoàn thành)**

   - Ghi đủ mọi case, kể cả case fail.
   - Lập bảng `case | input | output | đạt/trượt | lý do`.
   - Tính số thử, số đạt, tỷ lệ đạt và nhóm lỗi chính.
   - Không đổi tiêu chí sau khi đã thấy kết quả.
6. **Quay video CP3 dài khoảng 30 giây**

   - Quay một case bình thường từ input đến danh sách ưu tiên.
   - Nếu kịp, cho thấy một case khó: câu hỏi lặp, đã được trả lời hoặc tin bot.
   - Video phải thể hiện AI trả kết quả thật, không chỉ là mock UI.

### Sản phẩm phải có sau CP3

- Video thao tác 30 giây.
- Prototype có AI call thật ở quyết định trung tâm.
- `eval/` có golden set tối thiểu 20 case.
- Bảng kết quả lượt chạy đầu, có tổng số thử, số đạt, phần trăm và phân tích lỗi.

## CP4 - Chốt `spec.md` và quality bar

**Hạn nộp:** 21:00 ngày 18/09/2026. Sau thời điểm này không đổi chuẩn đạt.

### Việc cần làm

1. **Tạo và commit `spec.md`** theo `03-ai-spec-template.md`, hoàn thiện các phần:

   - §1 User & Job: TA/labcoach, workflow và bằng chứng mining Discord.
   - §2 Impact: so sánh ít nhất 3 hướng, giữ lại hướng bị loại và lý do chọn B2.
   - §3 Giải pháp tương tự: flow, điểm học được, điểm cần tránh và khác biệt của nhóm.
   - §4 Thiết kế: lát cắt một câu, tối thiểu 3 non-goals, mức prototype, automation và cost-of-error.
   - §4b: ít nhất 4 nguyên tắc HAX/PAIR, mỗi nguyên tắc chỉ rõ vị trí áp dụng trong prototype.
   - §5: 4 lớp chỗ khó và ít nhất 8 kịch bản lỗi.
   - §6: happy path, low-confidence, failure/không có căn cứ, correction và case ngoài phạm vi.
   - §7: chiều chất lượng, golden set, quality bar và kết quả lượt chạy.
   - §8: phân công, willing users và kế hoạch validation.
   - §9: changelog các thay đổi dựa trên case fail hoặc feedback.
2. **Chốt quality bar bằng số trước 21:00**

   - Ghi rõ dạng: `Đạt khi >= __% case qua bộ và __ điều kiện cứng`.
   - Điều kiện cứng nên bao gồm: không tính tin bot là câu hỏi, không đánh dấu đã trả lời khi không có reply hợp lệ, và mọi mục ưu tiên đều có căn cứ/link để TA kiểm tra.
   - Dùng cùng một quality bar để đối chiếu kết quả; nếu chưa đạt thì ghi nguyên nhân và kế hoạch sửa, không hạ chuẩn.
3. **Hoàn thiện evidence cho Track B (đã hoàn thành)**

   - Dẫn số liệu đã có: 1.092 tin nhắn, 779 tin từ người, 313 tin từ bot và 4 bản tin ngày.
   - Bổ sung ít nhất 5 ví dụ có mã tin nhắn, mỗi ví dụ trích tối đa 2 câu.
   - Ghi rõ phương pháp đếm, giới hạn dữ liệu: chỉ 3 ngày, chỉ kênh public và không suy đoán danh tính.
   - Phân tích các lỗi của bản tin hiện tại như tóm tắt cắt cụt, chuỗi nguồn chèn sai và câu hỏi đã/ chưa được phản hồi chưa rõ.
4. **Kiểm tra trước khi nộp CP4**

   - [ ] `spec.md` đã commit trước 21:00.
   - [ ] Quality bar có tỷ lệ phần trăm và điều kiện cứng.
   - [ ] Golden set có tối thiểu 20 case và phủ đủ 4 lớp chỗ khó.
   - [ ] Có bảng kết quả đầy đủ cả pass và fail.
   - [ ] Có ít nhất 4 nguyên tắc HAX/PAIR gắn với vị trí cụ thể.
   - [ ] Có ít nhất 8 kịch bản rủi ro, không chỉ mô tả chung chung.
   - [ ] Nêu rõ phần đã làm, phần mock và phần chưa làm xong.
   - [ ] Không có API key, nguyên data pack hoặc thông tin định danh trong repo public.

## Phân công đề xuất

| Người                   | Phần việc CP3/CP4                                                                    |
| ------------------------- | -------------------------------------------------------------------------------------- |
| Trương Hoàng Thành An | Điều phối, prompt, quality bar, hoàn thiện spec và kiểm tra nộp mốc           |
| Nguyễn Thị Minh Tiến   | Tích hợp AI call, xử lý dữ liệu/logic nhóm câu hỏi, log/trace                 |
| Phan Thị Khánh Linh     | Hoàn thiện giao diện luồng TA, trạng thái loading/không chắc chắn, quay video |
| Phạm Anh Minh            | Viết golden set, testcase 4 lớp chỗ khó, chạy và tổng hợp bảng đo            |

## Thứ tự ưu tiên nếu thiếu thời gian

1. AI call thật + luồng end-to-end chạy được.
2. Golden set 20 case + bảng đo trung thực.
3. Video CP3 30 giây.
4. Chốt quality bar và commit `spec.md` trước hạn CP4.
5. Bổ sung nghiên cứu giải pháp tương tự, multi-prototype và validation nếu còn thời gian.
