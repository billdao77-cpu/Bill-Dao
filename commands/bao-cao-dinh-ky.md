---
description: Báo cáo định kỳ từ file số liệu – làm sạch và kiểm tra dữ liệu, tính số bằng code, báo cáo "kết luận trước", slide tóm tắt nếu cần, kiểm định trước khi gửi.
argument-hint: "[kỳ báo cáo, file số liệu Excel/CSV, người nhận, có cần slide không]"
---

Lập báo cáo định kỳ cho: $ARGUMENTS

1. `bang-excel`: kiểm tra dữ liệu (trùng, thiếu, sai định dạng); cần làm sạch → `python3 "${CLAUDE_PLUGIN_ROOT}/skills/bang-excel/scripts/lam_sach.py" <vào> <ra mới>.xlsx`. Tính tổng, so kế hoạch/cùng kỳ bằng Python, ghi "Đã kiểm tra phép tính".
2. `bao-cao`: kết luận 1–3 câu → bảng số liệu (có nguồn, kỳ) → nhận định → đề xuất (người, hạn).
3. `slide-pptx` nếu người dùng cần trình chiếu: ≤ 8 slide, tiêu đề slide là kết luận; file mới.
4. Agent `bien-tap-kiem-dinh`: đối chiếu số trong báo cáo với file số liệu.

Đầu ra: báo cáo hoàn chỉnh + bảng chất lượng dữ liệu + bảng "Thông tin cần bổ sung/kiểm tra" (+ file .pptx). Không gửi.
