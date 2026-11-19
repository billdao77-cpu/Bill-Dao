# Prompt – Báo tăng, giảm BHXH tháng 11

## Chuẩn bị (trước giờ dạy)

1. Cài plugin Hành chính – Nhân sự (trọn bộ, hoặc tối thiểu skill `bhxh-che-do`).
2. Bật **Code execution** (claude.ai: Settings → Capabilities; ChatGPT: Code Interpreter).
3. Mở cuộc trò chuyện mới, **đính kèm 3 file trong `dau-vao/`**: `thong-tin-cong-ty.md`, `danh-sach-dong-bhxh-thang-10.xlsx`, `bien-dong-nhan-su-thang-11.xlsx`.

## Prompt demo (chép nguyên văn)

```
Tôi là HCNS Công ty TNHH Công nghệ Bình Minh (thông tin đính kèm), mới làm BHXH lần đầu, công ty dùng phần mềm iBH.
Đính kèm danh sách đang đóng BHXH tháng 10/2026 và ghi chú biến động nhân sự tháng 11/2026.
Người không có trong file biến động thì giữ nguyên như tháng 10.
Hãy lập cho tôi file hướng dẫn kê khai BHXH tháng 11: tăng ai, giảm ai, điều chỉnh ai, mỗi người gõ gì vào phần mềm,
hồ sơ nộp gì, còn thiếu thông tin gì của ai, tổng tiền phải đóng và hạn đóng.
```

Kết quả đúng: xem `ket-qua-mau/ket-qua.md` và file `huong-dan-ke-khai-thang-11-2026.docx` – **tăng 2 (TM), giảm 3 (TS, KL, GH), điều chỉnh 2 (DC)**, gom 1 bảng thủ tục 600, TK1-TS cho An và Khoa trong cùng hồ sơ; **anh Khoa còn thiếu 4 thông tin** (ghi THIẾU trong bảng TK1-TS); anh Cường **vẫn đóng tháng 11, GH từ tháng 12**; chị Bình, chị Giang không kê khai; **tổng nộp 55.260.000đ, hạn 31/12/2026**.

## Prompt hỏi tiếp (nếu còn thời gian)

```
Xuất thêm danh sách đúng mẫu D02-LT để tôi trình giám đốc duyệt trước khi nộp.
```

```
Soạn tin nhắn hướng dẫn chị Dung nộp giấy tờ hưởng chế độ thai sản và cho biết chị được nghỉ, được hưởng thế nào.
```

```
Anh Cường nghỉ việc thì được hưởng trợ cấp thất nghiệp không? Soạn hướng dẫn gửi anh ấy.
```

## Prompt đầy đủ khi đã kết nối Drive, Gmail, Calendar (chỉ giảng trên slide, không demo)

```
Đọc file "Danh sách lao động" và các quyết định nhân sự tháng 11 trong thư mục "Nhân sự/2026" trên Drive,
lập danh sách báo tăng – giảm BHXH tháng 11 và lưu vào thư mục "BHXH/2026/T11",
tạo nháp email hướng dẫn giấy tờ gửi riêng từng người,
và tạo nhắc hạn trên lịch: nộp hồ sơ tháng 11, chốt sổ cho anh Cường, báo tăng lại anh Em ngày 01/12.
```

Lý do không demo phần connector: dữ liệu nhân sự thật nằm rải rác nhiều file, quyền truy cập Drive mỗi lớp mỗi khác. Đặt sẵn file trong `dau-vao/` cho kết quả ổn định.
