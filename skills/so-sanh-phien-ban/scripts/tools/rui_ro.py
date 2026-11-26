"""Chấm mức rủi ro hợp đồng theo ma trận Khả năng × Ảnh hưởng (bản vn-custom).

Mục đích: mọi báo cáo rà soát, sổ rủi ro dùng cùng một thang 4 mức – Thấp / Trung bình / Cao / Nghiêm trọng – có lý do
kiểm tra lại được. Điểm số là công cụ hỗ trợ nhận định chuyên môn, không phải kết luận pháp lý.
"""

THANG_KHA_NANG = {
    1: "Hiếm – chỉ xảy ra trong tình huống bất thường",
    2: "Ít – có thể xảy ra nhưng chưa có dấu hiệu",
    3: "Có thể – đã gặp với giao dịch tương tự",
    4: "Dễ xảy ra – có dấu hiệu từ đối tác/hồ sơ",
    5: "Gần như chắc chắn – điều khoản/thực tế đã dẫn tới hậu quả",
}
THANG_ANH_HUONG = {
    1: "Không đáng kể – sửa được ngay, không tốn tiền",
    2: "Nhỏ – chi phí hoặc chậm trễ nhỏ, xử lý nội bộ",
    3: "Trung bình – thiệt hại tài chính đáng kể hoặc tranh chấp có thể thương lượng",
    4: "Lớn – thiệt hại lớn, mất quyền đòi, phải kiện tụng",
    5: "Rất nghiêm trọng – hợp đồng/điều khoản vô hiệu, trách nhiệm không giới hạn, rủi ro hình sự hoặc mất toàn bộ giá trị",
}
MUC = [(4, "Thấp"), (9, "Trung bình"), (16, "Cao"), (25, "Nghiêm trọng")]
THU_TU = {"Nghiêm trọng": 0, "Cao": 1, "Trung bình": 2, "Thấp": 3}


def _muc(diem, anh_huong):
    m = next(ten for tran, ten in MUC if diem <= tran)
    if anh_huong == 5 and THU_TU[m] > THU_TU["Cao"]:
        m = "Cao"  # hậu quả rất nghiêm trọng thì tối thiểu là Cao dù khả năng thấp
    return m


def danh_gia_rui_ro(danh_sach, ben_nguoi_dung=""):
    if not isinstance(danh_sach, list) or not danh_sach:
        return {"loi": "danh_sach phải là danh sách rủi ro, ví dụ [{\"dieu\": \"Điều 8\", \"rui_ro\": \"...\", \"kha_nang\": 3, \"anh_huong\": 4}]"}
    kq, loi = [], []
    for i, r in enumerate(danh_sach, 1):
        try:
            k, a = int(r.get("kha_nang")), int(r.get("anh_huong"))
        except (TypeError, ValueError):
            loi.append(f"Dòng {i}: kha_nang và anh_huong phải là số nguyên 1–5")
            continue
        if not (1 <= k <= 5 and 1 <= a <= 5):
            loi.append(f"Dòng {i}: kha_nang/anh_huong ngoài khoảng 1–5")
            continue
        if not r.get("rui_ro"):
            loi.append(f"Dòng {i}: thiếu mô tả rủi ro")
            continue
        muc = _muc(k * a, a)
        kq.append({"dieu": r.get("dieu", ""), "rui_ro": r["rui_ro"], "kha_nang": k, "anh_huong": a, "diem": k * a,
                   "muc_do": muc, "ly_do_cham": f"Khả năng {k}: {THANG_KHA_NANG[k]}; Ảnh hưởng {a}: {THANG_ANH_HUONG[a]}",
                   "bien_phap": r.get("bien_phap", ""), "nguoi_phu_trach": r.get("nguoi_phu_trach", "")})
    if loi:
        return {"loi": loi}
    kq.sort(key=lambda x: (THU_TU[x["muc_do"]], -x["diem"]))
    dem = {m: sum(1 for x in kq if x["muc_do"] == m) for m in ("Nghiêm trọng", "Cao", "Trung bình", "Thấp")}
    if dem["Nghiêm trọng"]:
        kn = "Không nên ký khi chưa xử lý các rủi ro Nghiêm trọng"
    elif dem["Cao"]:
        kn = f"Chỉ nên ký sau khi sửa hoặc có biện pháp kiểm soát cho {dem['Cao']} rủi ro Cao"
    else:
        kn = "Có thể ký nếu người có thẩm quyền chấp nhận các rủi ro còn lại"
    return {"ben_nguoi_dung": ben_nguoi_dung or "(chưa xác định – phải hỏi trước khi kết luận)",
            "ket_qua": kq, "so_luong_theo_muc": dem, "goi_y_ket_luan": kn,
            "phuong_phap": "Điểm = Khả năng (1–5) × Ảnh hưởng (1–5): 1–4 Thấp, 5–9 Trung bình, 10–16 Cao, 20–25 Nghiêm trọng; "
                           "Ảnh hưởng 5 tối thiểu là Cao.",
            "luu_y": "Điểm số phản ánh nhận định chuyên môn của người chấm, không phải kết luận pháp lý. Người có thẩm quyền "
                     "quyết định chấp nhận, sửa hoặc từ chối từng rủi ro."}


TOOLS = [
    {"name": "danh_gia_rui_ro", "fn": danh_gia_rui_ro,
     "description": "Chấm mức rủi ro hợp đồng 4 mức (Thấp/Trung bình/Cao/Nghiêm trọng) theo ma trận Khả năng × Ảnh hưởng (1–5), "
                    "sắp xếp theo mức, đếm số lượng và gợi ý kết luận ký/sửa/không ký; kèm lý do chấm để kiểm tra lại.",
     "schema": {"type": "object", "required": ["danh_sach"], "properties": {
         "ben_nguoi_dung": {"type": "string", "description": "Người dùng là bên nào trong hợp đồng"},
         "danh_sach": {"type": "array", "items": {"type": "object", "required": ["rui_ro", "kha_nang", "anh_huong"], "properties": {
             "dieu": {"type": "string"}, "rui_ro": {"type": "string"},
             "kha_nang": {"type": "integer", "description": "1 hiếm … 5 gần như chắc chắn"},
             "anh_huong": {"type": "integer", "description": "1 không đáng kể … 5 rất nghiêm trọng"},
             "bien_phap": {"type": "string"}, "nguoi_phu_trach": {"type": "string"}}}}}}},
]
