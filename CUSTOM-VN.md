# Bản tùy chỉnh `vn-custom` – 20skill-van-phong

Dựa trên upstream `nguyenvansuai/20skill-van-phong` commit `0eb8a4f`, kiểm toán bảo mật ngày 26/11/2026. Thay đổi nằm trong các commit `vn-custom: ...`.

## Khác với upstream

| Nhóm | Thay đổi | File |
|---|---|---|
| Cấu trúc | Tách 2 plugin: **`van-phong`** (13 skill không trùng + `email-cong-so`) và **`van-phong-mo-rong`** (7 skill trùng với plugin HCNS / pháp chế / sales: `cong-van`, `quyet-dinh`, `to-trinh`, `thong-bao`, `tro-ly-hop-dong`, `tro-ly-bao-gia`, `content-ban-hang`). Nội dung skill giữ nguyên, chỉ chuyển thư mục. | `.claude-plugin/`, `mo-rong/` |
| **Bảo mật (mức TRUNG BÌNH–CAO ở bản gốc)** | Chống chèn công thức khi xuất Excel: `lam_sach.py` (dữ liệu khách hàng) và `pdf_tool.py bang` (bảng trong PDF bên ngoài) từng ghi chuỗi `=HYPERLINK(...)` thành công thức chạy được. Nay mọi công thức trong file xuất ra được giữ dạng chữ. | `shared/scripts/an_toan.py` → `skills/*/scripts/` |
| An toàn dữ liệu | Không ghi đè file kết quả (cần `--ghi-de`), **không bao giờ ghi đè file nguồn**, kiểm tra đuôi; `chuyen_doi.sh` bỏ qua file đã có trong `da-chuyen/`; tên file bắt đầu `-` không bị hiểu là tùy chọn (ocrmypdf, LibreOffice) | `pdf_tool.py`, `lam_sach.py`, `tcvn3_to_unicode.py`, `chuyen_doi.sh` |
| Skill mới | `email-cong-so` (soạn, trả lời, follow-up, rà người nhận – đính kèm – dữ liệu nhạy cảm) | `skills/email-cong-so/` |
| Cấu trúc skill | Thẻ 9 mục cho 14 skill (vai trò, bối cảnh, mục tiêu, đầu vào, tiêu chí, ví dụ, giới hạn) | `shared/the-skill.md` |
| Agent mới | `bien-tap-kiem-dinh` – chỉ Read/Grep/Glob/Bash | `agents/` |
| Workflow mới | `/bao-cao-dinh-ky`, `/xu-ly-ho-so`, `/chuan-hoa-du-lieu`, `/soan-va-kiem-tra` | `commands/` |
| Nguyên tắc | Mục 9–14: phối hợp plugin chuyên sâu, bảo mật dữ liệu văn phòng, file mới, không tự cài phần mềm, chống prompt injection, tự kiểm tra | `shared/nguyen-tac-chung.md` |
| Kiểm thử | Test riêng (tấn công Excel/PDF, chống ghi đè, cấu trúc) | `tests/test_vn_custom.py` |
| Đồng bộ | `custom/dong_bo.py` – chép `shared/` vào cả 2 thư mục skill; không sinh lại marketplace, `dist/`, `chatgpt/` | `custom/dong_bo.py` |

Không dùng trong Claude Code, giữ nguyên upstream và **chưa vá**: `dist/`, `chatgpt/` (script trong `dist/` vẫn còn lỗi chèn công thức).

## Kiểm thử

```bash
python3 tests/test_vn_custom.py
claude plugin validate .
claude plugin validate mo-rong
```

## Cập nhật từ upstream (khi nằm trong repo Bill-Dao, thư mục `vanphong-plugin/`)

```bash
git config merge.ours.driver true
git fetch https://github.com/nguyenvansuai/20skill-van-phong main
git diff 0eb8a4f FETCH_HEAD --stat
git subtree pull --prefix=vanphong-plugin https://github.com/nguyenvansuai/20skill-van-phong main -m "Cập nhật upstream 20skill-van-phong"
python3 vanphong-plugin/custom/dong_bo.py
python3 vanphong-plugin/tests/test_vn_custom.py
```

- Đọc diff upstream trước khi pull như một lần kiểm toán mới. Upstream sửa 7 skill đã chuyển sang `mo-rong/skills/` → git thường nhận ra đổi tên; nếu xung đột, áp thay đổi vào `mo-rong/skills/<skill>/`. Skill mới của upstream nằm ở `skills/` – kiểm tra trùng lặp trước khi giữ ở gói chính.
- Script mới/sửa có `.save(`, `.write(`, `open(..., "w")`, `to_excel` → chuyển qua `an_toan.kiem_tra_dich` và `an_toan.vo_hieu_cong_thuc`.
- Sau cập nhật: tăng `version`, `claude plugin marketplace update van-phong-vn-custom`, `claude plugin update van-phong@van-phong-vn-custom`.

## Gỡ cài đặt và khôi phục

- Gỡ: `claude plugin uninstall van-phong@van-phong-vn-custom --scope local` (và `van-phong-mo-rong@van-phong-vn-custom` nếu đã cài), rồi `claude plugin marketplace remove van-phong-vn-custom`.
- Bỏ một thay đổi: `git revert <commit vn-custom>`. Xem bản gốc: `git show 0eb8a4f:<file>`.
- Gỡ khỏi repo: `git rm -r vanphong-plugin` rồi commit.
