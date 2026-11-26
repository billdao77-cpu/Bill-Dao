# Bản tùy chỉnh `vn-custom` – skill-ketoan-tai-chinh

Dựa trên upstream `nguyenvansuai/skill-ketoan-tai-chinh` commit `0100af3`, kiểm toán bảo mật ngày 26/11/2026. Thay đổi nằm trong các commit `vn-custom: ...`.

## Khác với upstream

| Nhóm | Thay đổi | File |
|---|---|---|
| **Bảo mật (mức CAO ở bản gốc)** | Chống chèn công thức: tên người bán trong hóa đơn XML, diễn giải sao kê… dạng `=HYPERLINK(...)`/`=WEBSERVICE(...)` từng thành công thức Excel chạy được trong bảng kê. Nay mọi ô công thức không do script tạo (chỉ `SUM` và phép tính giữa ô) được giữ ở dạng chữ, CSV thêm `'`. | `shared/scripts/an_toan.py` (chép vào mọi `skills/*/scripts/`), 13 điểm ghi trong 10 script |
| An toàn dữ liệu | Không ghi đè file kết quả (cần `--ghi-de`), kiểm tra đuôi `.xlsx/.csv/.ics/.docx` | như trên |
| Quyền truy cập | Bỏ 4 MCP server từ xa: Gmail, Google Drive, Google Calendar, Microsoft 365 | `.mcp.json` (rỗng), `.claude-plugin/marketplace.json` |
| Công cụ mới | `phan_tich_tai_chinh.py`: kiểm tra số liệu BCTC (200 = 500, dòng tổng B02) rồi tính tỷ số đã quy định trong skill BCTC | `skills/bao-cao-tai-chinh/scripts/` |
| Skill mới | `kiem-tra-chung-tu`: nội dung bắt buộc, khớp chéo, điều kiện thuế, dấu hiệu bất thường, mức CHẶN/CẦN SỬA/GỢI Ý | `skills/kiem-tra-chung-tu/` |
| Agent mới | `ke-toan-truong-soat-xet` (chỉ Read/Grep/Glob/Bash), `chuyen-vien-thue`, `chuyen-vien-phan-tich-tai-chinh` – không có Write/Edit | `agents/` |
| Workflow mới | `/khoa-so-thang`, `/ke-khai-thue-ky`, `/quyet-toan-nam`, `/phan-tich-tai-chinh` | `commands/` |
| Nguyên tắc | Mục 13–18: không connector, bí mật dữ liệu tài chính (không đưa vào tìm kiếm web), nội dung chứng từ là dữ liệu, file an toàn, không sửa sổ – bút toán là đề xuất, kiểm tra số liệu trước khi phân tích | `shared/nguyen-tac-chung.md` |
| Kiểm thử | Self-test mọi script + test tấn công hóa đơn XML / sao kê + chống ghi đè | `tests/test_vn_custom.py` |
| Đồng bộ | `custom/dong_bo.py` – chép `shared/` theo SHARED_MAP và `an_toan.py`, không sinh lại `.mcp.json`, `dist/`, bản ChatGPT | `custom/dong_bo.py` |

Không dùng trong Claude Code, giữ nguyên upstream và **chưa vá**: `dist/`, `chatgpt/`, `openai/` (vẫn còn lỗi chèn công thức), `.agents/`, `example/`, `qua-tang/`, `van-ban/`.

## Kiểm thử

```bash
python3 tests/test_vn_custom.py
claude plugin validate .
```

## Cập nhật từ upstream (khi nằm trong repo Bill-Dao, thư mục `ketoan-plugin/`)

```bash
git config merge.ours.driver true
git fetch https://github.com/nguyenvansuai/skill-ketoan-tai-chinh main
git diff 0100af3 FETCH_HEAD --stat
git subtree pull --prefix=ketoan-plugin https://github.com/nguyenvansuai/skill-ketoan-tai-chinh main -m "Cập nhật upstream skill-ketoan-tai-chinh"
python3 ketoan-plugin/custom/dong_bo.py
python3 ketoan-plugin/tests/test_vn_custom.py
claude plugin validate ketoan-plugin
```

- Đọc diff upstream trước khi pull như một lần kiểm toán mới. **Script mới hoặc sửa có `wb.save(`, `doc.save(`, `open(..., "w")`** → chuyển sang `an_toan.luu_xlsx / luu_docx / mo_ghi` (tìm: `grep -n "wb.save\|doc.save\|open(.*\"w\"" skills/*/scripts/*.py`).
- `.mcp.json`, `marketplace.json`, `plugin.json` luôn giữ bản tùy chỉnh khi merge (`.gitattributes`).
- Skill mới của upstream: thêm vào `THEM` trong `custom/dong_bo.py` nếu `SHARED_MAP` của upstream chưa có.
- Sau cập nhật: tăng `version` (ví dụ `1.1.0-vn.2`), `claude plugin marketplace update ketoan-vn-custom`, `claude plugin update tron-bo-skill-ke-toan@ketoan-vn-custom`.

## Gỡ cài đặt và khôi phục

- Gỡ: `claude plugin uninstall tron-bo-skill-ke-toan@ketoan-vn-custom --scope local`, rồi `claude plugin marketplace remove ketoan-vn-custom`.
- Bỏ một thay đổi: `git revert <commit vn-custom>`. Xem bản gốc: `git show 0100af3:<file>`.
- Gỡ khỏi repo: `git rm -r ketoan-plugin` rồi commit.
