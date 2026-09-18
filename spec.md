# AI SPEC - Discord Q&A Intelligence

**Nhóm:** 3B-E403-4ACE  
**Zone:** 3  
**Hướng:** [ ] A - VLearn  [x] B - Trợ lý Học viên  [ ] C - Làn mở  
**Loại:** [ ] Tối ưu tính năng có sẵn  [x] Tính năng mới

## §1. User & Job

### User và workflow

- **Job executor (chính):** TA/labcoach vào cuối ngày trong server Discord để xử lý câu hỏi tồn đọng.
- **Job executor (phụ):** Học viên muốn xem câu hỏi đã được trả lời để tự tra cứu thông tin.
- **Workflow hiện tại:** Rà nhiều tin nhắn, tự nhận diện câu hỏi, tìm câu hỏi lặp, kiểm tra câu nào đã có phản hồi và chọn câu cần xử lý trước.
- **Hậu quả:** Mất thời gian tổng hợp, có thể bỏ sót câu hỏi cần trả lời sớm và không có thứ hạng ưu tiên rõ ràng.

### Core JTBD

> Khi kết thúc một ngày có nhiều tin nhắn Discord, TA/labcoach muốn tìm nhanh các câu hỏi đang lặp và chưa được trả lời để xử lý theo mức độ ưu tiên.

### Problem statement

TA/labcoach đang phải rà thủ công nhiều tin nhắn Discord nhưng không biết câu hỏi nào bị lặp, câu nào còn tồn và câu nào cần xử lý trước, nên mất thời gian và có nguy cơ bỏ sót câu hỏi quan trọng.

### Evidence

Nguồn: `data/discord-pack/k4_messages.csv` và `data/discord-pack/k4_daily_reports.md`, được tổng hợp trong `evidence/mining_results.md`.

- 1.092 tin nhắn trong giai đoạn 12-14/09/2026.
- 779 tin từ người và 313 tin từ bot.
- 107 câu hỏi có dấu hỏi, tương đương 13,7% tin nhắn của người.
- Mining report ghi nhận 87,9% câu hỏi không có reply.
- Có 4 bản tin ngày của bot gặp lỗi tóm tắt, nguồn tham chiếu hoặc thiếu xếp hạng ưu tiên.

### Ví dụ nguyên văn

| Message ID | Ví dụ | Vấn đề liên quan |
|---|---|---|
| M99769 | "[@D7688] cho mình hỏi một team mấy bạn?" | Câu hỏi về quy tắc team |
| M67317 | "2b vs 2a vẫn join chung được luôn ạ ?" | Câu hỏi domain về team |
| M76498 | "Sổ tay học viên https://drive.google.com/..." | Cần kiểm tra ngữ cảnh/link |
| M71241 | "[@D3694] anh ơi cái repo này là template đúng không ạ https://github.com/..." | Câu hỏi GitHub/repo |
| M63574 | "A ơi, cho e hỏi, buổi workshop chủ nhật ngày mai thì có tính vào số buổi nghỉ ko ạ? Giả dụ sáng mai e có việc thì sao ạ?" | Câu hỏi lịch/nghỉ |

**Giới hạn evidence:** Dataset chỉ bao phủ 3 ngày và các kênh có trong Discord pack. Nhóm không suy đoán danh tính người gửi. [CẦN BỔ SUNG nếu cần: link/log khảo sát chuẩn A; hiện nhóm đang dùng evidence chuẩn B từ mining.]

## §2. Impact và quyết định chọn

### Các ứng viên

| Ứng viên | Người hưởng lợi | Tần suất | Chi phí hiện tại | Khả thi | Quyết định |
|---|---:|---|---|---|---|
| Dashboard câu hỏi chưa trả lời | TA/labcoach | Mỗi ngày | Phải rà toàn bộ Discord để tìm câu hỏi tồn | Cao, đã có detector và output | Giữ làm thành phần chính |
| Nhóm câu hỏi tương tự | TA/labcoach và học viên có câu hỏi lặp | Mỗi ngày, đặc biệt khi có deadline | Mất thời gian đọc nhiều câu cùng chủ đề | Trung bình, hiện dùng keyword overlap | Giữ làm thành phần chính |
| Xếp hạng ưu tiên | TA/labcoach | Mỗi ngày | Không biết xử lý câu nào trước | Cao, đã có scorer | Giữ làm thành phần chính |
| Tự động gửi câu trả lời | Học viên và TA | Mỗi khi có câu hỏi | Rủi ro trả lời sai quy định hoặc bịa nguồn | Thấp do cost-of-error cao | Loại |

**Lưu ý số liệu:** Chưa có log đo thời gian TA tiết kiệm hoặc số người dùng theo từng ứng viên. Bảng trên dùng số liệu mining và đánh giá khả thi kỹ thuật, không phải khảo sát định lượng người dùng.

### Ứng viên đã loại

- **Tự động trả lời học viên:** loại vì nếu câu hỏi thiếu căn cứ hoặc là edge case về điểm/XP, câu trả lời sai có thể gây mất điểm và mất niềm tin. Hệ thống chỉ gợi ý, nhóm và xếp hạng để TA kiểm tra.
- **Dashboard tổng quát không có nhóm/ưu tiên:** loại vì không giải quyết trực tiếp pain “không biết câu nào cần xử lý trước”.
- **Thu thập dữ liệu Discord mới theo thời gian thực:** chưa build trong CP3; prototype dùng snapshot CSV để tập trung chứng minh pipeline phân tích.

### Ứng viên chọn

Chọn lát cắt **nhóm câu hỏi tương tự + phát hiện trạng thái reply + xếp hạng ưu tiên**, vì một pipeline có thể xử lý ba pain đã quan sát được: câu hỏi lặp, câu hỏi chưa được trả lời và báo cáo không có thứ hạng. Bằng chứng đầu vào gồm 1.092 tin nhắn, 107 câu hỏi và 87,9% câu hỏi được mining report ghi nhận là chưa có reply.

## §3. Giải pháp tương tự đã nghiên cứu

[CẦN BỔ SUNG: Tên/link và ghi chú nghiên cứu trực tiếp của nhóm cho ít nhất 2 sản phẩm. Phần dưới là khung tạm để hoàn thiện.]

### Discord search/thread

- **Flow:** Tìm từ khóa hoặc mở thread để xem câu hỏi và reply.
- **Đáng học:** Giữ message ID/thread làm điểm kiểm tra trực tiếp cho TA.
- **Đáng né:** Người dùng vẫn phải tự đọc và tự xếp thứ tự nhiều câu hỏi.
- **Nhóm khác:** Tự động gom nhóm, gắn status và priority trong một danh sách xử lý.

### Helpdesk/triage dashboard

- **Flow:** Nhận ticket, gắn nhãn, xếp hàng theo trạng thái/độ ưu tiên.
- **Đáng học:** Hiển thị trạng thái và hàng đợi xử lý rõ ràng.
- **Đáng né:** Không áp dụng máy móc mô hình ticket cho hội thoại Discord không cấu trúc.
- **Nhóm khác:** Dùng dữ liệu Discord, giữ lại link/message ID và yêu cầu TA duyệt trước khi phản hồi.

## §4. Thiết kế

### Lát cắt MỘT CÂU

> Một TA/labcoach cuối ngày đưa snapshot tin nhắn Discord vào pipeline; hệ thống nhóm các câu hỏi tương tự, phát hiện trạng thái phản hồi và xếp hạng câu hỏi cần xử lý; TA nhận danh sách có intent, số lần lặp, status, priority và message ID để tự kiểm tra.

### Non-goals

1. Không tự gửi câu trả lời cho học viên.
2. Không bịa deadline, policy, lỗi kỹ thuật hoặc nguồn tham chiếu khi dữ liệu không đủ.
3. Không suy đoán hoặc hiển thị danh tính học viên.
4. Không đồng bộ tin nhắn Discord real-time trong CP3.
5. Không thay thế quyết định cuối cùng của TA/labcoach.

### Mức prototype

**Mức:** [ ] Sketch  [x] Mock  [ ] Working

- **Đã làm thật:** parser, rule-based intent classifier, keyword clustering, response detector, priority scorer và output pipeline.
- **AI thật:** module `ai.py` gọi endpoint OpenAI-compatible/Qwen khi có API key và ghi log tại `logs/ai_calls.jsonl`. Repo đã có log các lần gọi thành công.
- **Mock/fallback:** khi không có API key, classifier/clustering chạy rule-based; UI đọc snapshot output để phục vụ demo.
- **Chưa làm:** semantic embedding clustering hoàn chỉnh, đồng bộ Discord real-time và đánh giá nội dung reply có giải quyết câu hỏi hay không.

### Automation và cost-of-error

Chọn **augment/conditional**, không chọn automate hoàn toàn. AI tự nhóm, gợi ý intent, status và priority; TA kiểm tra message ID và quyết định phản hồi. Với các câu hỏi về deadline, XP, điểm hoặc lỗi kỹ thuật, cost-of-error cao nên hệ thống phải cho phép fallback và chuyển TA thay vì tự trả lời.

### §4b. Nguyên tắc áp dụng

| Nguyên tắc | Áp dụng cụ thể |
|---|---|
| G10 - Thu hẹp phạm vi khi nghi ngờ | Case không đủ thông tin giữ trạng thái cần TA kiểm tra; không tự sinh câu trả lời. |
| G11 - Giải thích vì sao | Output giữ intent, status, priority, cluster size và message ID để TA truy ngược dữ liệu. |
| G8 - Gạt bỏ dễ dàng | TA có thể bỏ qua gợi ý, mở message gốc và tự xử lý; không có nút tự động gửi câu trả lời. |
| G9 - Sửa dễ dàng | Bộ lọc intent/status và danh sách message giúp TA kiểm tra, đối chiếu và sửa quyết định ngoài AI. |
| PAIR - Explainability & Trust | Hiển thị căn cứ từ message/link và trạng thái AI/fallback, không trình bày phán đoán như sự thật tuyệt đối. |
| PAIR - Errors & Graceful Failure | Khi thiếu API key hoặc thiếu căn cứ, dùng rule fallback và báo rõ giới hạn thay vì bịa kết quả. |

## §5. Kiểu lỗi - 4 lớp chỗ khó và kịch bản

| ID | Lớp | Tình huống | Hành vi mong muốn |
|---|---|---|---|
| R01 | 1 - Fact | CVAT lỗi “nguồn tham chiếu” ở bước 3 nhưng không có tài liệu lỗi tương ứng | Gắn lab technical, báo cần căn cứ/tài liệu, không tự bịa cách sửa |
| R02 | 1 - Fact | Link Phoenix không vào được | Gắn onboarding, hiển thị vấn đề cần hỗ trợ và message ID để TA kiểm tra |
| R03 | 2 - Ambiguous | “Deadline nộp Lab2 là khi nào?” nhưng không có ngày/thông báo đi kèm | Gắn deadline/XP, đánh dấu cần xác nhận và hỏi thêm thông tin |
| R04 | 2 - Ambiguous | “Có bạn trả lời trước 21:00, vậy đã chốt chưa?” | Không khẳng định policy; yêu cầu đối chiếu nguồn chính thức |
| R05 | 3 - OutOfScope | “Thư viện trường ở đâu?” | Không ép vào intent khóa học; gắn `other` hoặc chuyển TA |
| R06 | 3 - OutOfScope | Hỏi có được nghỉ lab vì đi thực tập không | Báo đây là quy định cần thẩm quyền trường/doanh nghiệp; không tự quyết định |
| R07 | 4 - Domain | Team cần 5 người hay 4 người | Gắn team và ưu tiên kiểm tra vì sai có thể ảnh hưởng việc lập team |
| R08 | 4 - Domain | XP có tính cho workshop offline hoặc nộp trễ 1 phút không | Gắn deadline/XP, yêu cầu policy chính thức, không bịa câu trả lời |
| R09 | 4 - Domain | Điểm danh trên Zoom hay MyVinUni | Gắn quy định domain và yêu cầu xác nhận kênh chính thức |
| R10 | 4 - Domain | Commit GitHub lỗi nhưng Vlearn vẫn nhận code | Gắn edge case deadline/XP, đưa TA kiểm tra vì có thể ảnh hưởng điểm |

## §6. Bốn đường đi của trải nghiệm

- **Happy path:** Nạp/chọn snapshot -> chạy phân tích -> xem cluster, intent, số lần lặp, status và priority -> mở message ID để TA xử lý.
- **Low-confidence (②):** Input mơ hồ hoặc nhiều keyword xung đột -> hiển thị intent dự đoán/fallback và trạng thái cần TA kiểm tra; không tự trả lời.
- **Failure/không căn cứ (①):** Không có API key, không tìm thấy nguồn hoặc AI call lỗi -> báo AI unavailable/fallback rule-based; giữ output ở mức gợi ý.
- **Correction:** TA đối chiếu message gốc, bỏ qua hoặc sửa cách hiểu; hệ thống không tự gửi câu trả lời và không khóa quyết định của TA.
- **Ngoài phạm vi (③):** Câu hỏi về thư viện/căn tin/trường ngoài khóa -> gắn `other` hoặc chuyển TA, không ép vào schedule/course intent.
- **Đặc thù domain (④):** Câu hỏi deadline, XP, team, điểm danh -> xếp ưu tiên và yêu cầu căn cứ policy trước khi phản hồi.

## §7. Kiểm thử

### Chiều chất lượng

- **Intent accuracy:** Tỷ lệ case mà intent dự đoán trùng `expected_intent` trong golden set. Người chấm khác có thể kiểm tra bằng cách chạy `python eval/run_eval.py`.
- **Status detection:** Tỷ lệ câu hỏi trong snapshot mà status detector khớp ground truth `reply_to`; `answered/partial` được tính là có phản hồi, `unanswered` là không có reply.
- **No hallucination:** Pass khi output không tự khẳng định deadline/policy/cách sửa lỗi nếu không có căn cứ trong dữ liệu; case thiếu căn cứ phải được chuyển TA hoặc ghi rõ fallback.

### Golden set

`eval/golden_set.md` có 30 case, vượt mức tối thiểu 20 và phủ đủ 4 lớp chỗ khó. Evaluator đọc trực tiếp block JSON trong golden set. Các case fail được giữ lại để phản ánh ranh giới taxonomy, không đổi expected chỉ để tăng điểm.

### Quality bar đã chốt

> Đạt khi intent accuracy >= 80%, status detection >= 85%, và không có câu trả lời nghiệp vụ không có căn cứ.

### Kết quả lượt chạy

| Lượt | Bộ test | Intent | Status | Kết luận |
|---|---|---:|---:|---|
| Lượt hiện tại | 30 golden cases + 107 câu hỏi snapshot | 24/30 = 80% | 107/107 = 100% | Đạt ngưỡng đã chốt |

Phân tích 6 case intent chưa đạt: nhầm giữa `schedule` và `deadline_xp`, `support` và `lab_technical`, hoặc câu hỏi deadline chưa có keyword đủ rõ. Đây là lỗi ranh giới phân loại, không phải pipeline crash.

**Giới hạn phép đo:** `expected_status` và `expected_cluster_size` trong từng golden case chưa được evaluator đối chiếu trực tiếp; cluster quality và priority ranking chưa có metric tự động riêng. Status hiện được đánh giá trên toàn bộ snapshot 107 câu hỏi.

## §8. Phân công và kế hoạch

| Phần việc | Người phụ trách |
|---|---|
| Điều phối, prompt, spec, quality bar | Trương Hoàng Thành An |
| Mining/evidence, tích hợp AI, code | Nguyễn Thị Minh Tiến |
| Frontend prototype, loading/fallback, demo video | Phan Thị Khánh Linh |
| Golden set, testcase, chạy và tổng hợp eval | Phạm Anh Minh |

### Willing users

- Đinh Lê Bình An - sinh viên khóa 3
- Hồ Hoàng Phương Anh - sinh viên khóa 4
- Tô Anh Đức - sinh viên khóa 4

**Kết quả validation:** Đinh Lê Bình An góp ý `/leaderboard` cần hiển thị thêm câu trả lời đi kèm câu hỏi để ban tổ chức và học viên dễ tập trung xử lý; nhóm đã bổ sung cột `Answered`. Hồ Hoàng Phương Anh xem lại bản sửa và phản hồi “thấy ổn rồi”. Chi tiết: `validation/feedback_log.md`. Nhóm chưa đo thời gian hoàn thành task.


### Multi-prototype

Chưa thực hiện so sánh nhiều prototype. Bản hiện tại chọn pipeline dashboard/leaderboard vì khớp lát cắt TA cuối ngày và có thể demo end-to-end.

## §9. Changelog

| Thời điểm | Đổi gì | Vì sao |
|---|---|---|
| 18/09/2026 | Tăng golden set từ 25 lên 30 case | Bổ sung case keyword collision, out-of-scope và partial status |
| 18/09/2026 | Cho evaluator đọc trực tiếp `eval/golden_set.md` | Tránh kết quả 25 case lệch với golden set 30 case |
| 18/09/2026 | Điều chỉnh classifier priority và keyword support | Giảm việc support lấn át GitHub/lab/schedule |
| 18/09/2026 | Chạy lại pipeline/evaluator | Xác nhận 24/30 intent và 107/107 status |
| 18/09/2026 | Bổ sung cột `Answered` trong `/leaderboard` | Đinh Lê Bình An góp ý cần thấy câu trả lời đi kèm câu hỏi; Hồ Hoàng Phương Anh xem lại và phản hồi “thấy ổn rồi” |

## Các thông tin còn thiếu cần bổ sung trước khi nộp

2. Bảng impact có số người hưởng lợi, tần suất và thời gian/chi phí đo thực tế.
3. Tên/link 2 sản phẩm tương tự đã nghiên cứu.
4. Mapping ít nhất 10 golden case với message ID/chatlog nguồn.
5. Xác nhận 8-10 case thường và 2-4 case hiếm.
6. Feedback log của ít nhất 2 willing users nếu muốn lấy bonus validation.
7. Nếu yêu cầu chứng minh đầy đủ cluster/priority, cần bổ sung evaluator tương ứng; hiện chưa có số đo tự động cho hai chiều này.
8. Xác nhận lại số liệu “13 answered/94 unanswered” trong mining report so với “84 có reply/23 không reply” của detector, vì hai phép đo đang dùng định nghĩa khác nhau.
