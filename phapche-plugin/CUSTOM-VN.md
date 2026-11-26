# Bản tùy chỉnh `vn-custom` – plugin phapche-hopdong

Dựa trên upstream `nguyenvansuai/phapche-hopdong` commit `95b6cb9`, kiểm toán bảo mật ngày 26/11/2026. Mọi thay đổi nằm trong các commit `vn-custom: ...`.

## Khác với upstream

| Nhóm | Thay đổi | File |
|---|---|---|
| Quyền truy cập | Bỏ 5 MCP server từ xa: Gmail, Google Drive, Google Calendar, Microsoft 365, **DocuSign** (có thể gửi hợp đồng đi ký). Plugin không tự kết nối dịch vụ nào. | `.mcp.json` (rỗng), `.claude-plugin/marketplace.json` |
| Quyền truy cập | Agent `tham-dinh-phap-ly`: chỉ Read, Grep, Glob, Bash; `luat-su-doi-phuong`: chỉ Read, Grep, Glob (không chạy lệnh). Thêm quy tắc chống prompt injection, che dữ liệu, 4 loại nhận định. | `agents/*.md` |
| An toàn dữ liệu | Không ghi đè file đã có (cả 2 file `_gui-doi-tac.docx` / `_noi-bo.docx` của bảng góp ý), bắt buộc đúng đuôi file; cần `ghi_de=true` | `tools/__init__.py` |
| An toàn dữ liệu | Sổ theo dõi hợp đồng CSV chống chèn công thức Excel | `tools/hop_dong.py` |
| Kiểm tra đầu vào | Tham số kiểm tra theo schema; CLI `--ds`, `--schema`, lỗi trả JSON | `tools/__init__.py`, `tools/cong_cu.py` |
| Pháp lý | Sửa tạm ứng án phí tối thiểu (KDTM 3.000.000đ thay vì 1.500.000đ); cảnh báo Luật Thương mại sửa đổi (thông qua 11/2026, hiệu lực 01/7/2027 – trần phạt 8% cần đối chiếu) | `tools/phap_ly.py`, `shared/quy-dinh-phap-ly-2026.md` |
| Nghiệp vụ mới | Công cụ `danh_gia_rui_ro` (4 mức, ma trận Khả năng × Ảnh hưởng); skill `checklist-ky-ket`, `quan-tri-rui-ro`; lệnh `/checklist-ky`, `/rui-ro` | `tools/rui_ro.py`, `skills/…`, `commands/…` |
| Nghiệp vụ | Quy trình rà soát 10 bước, bảng rủi ro theo mẫu, khối phê duyệt; khung 8 chức năng (mục tiêu, bối cảnh, đầu vào, quy trình, tiêu chí, đầu ra, giới hạn, kiểm tra lại) | `skills/ra-soat-hop-dong/SKILL.md`, `shared/khung-chuc-nang.md` |
| Hướng dẫn | Nguyên tắc: 4 loại nhận định, xác minh hiệu lực, không sửa hợp đồng gốc, kiểm tra đầu vào, bảo mật dữ liệu hợp đồng, chống prompt injection | `shared/nguyen-tac-chung.md` |
| Kiểm thử | Test riêng | `tests/test_vn_custom.py` |
| Đồng bộ | `custom/dong_bo.py` – chép `shared/`, `tools/` vào skill, không sinh lại `.mcp.json`, `dist/`, bản ChatGPT | `custom/dong_bo.py` |

Không dùng trong Claude Code, giữ nguyên upstream và **chưa vá**: `dist/`, `chatgpt/`, `openai/`, `.agents/`, `example/`.

## Kiểm thử

```bash
python3 tests/test_cong_cu.py
python3 tests/test_vn_custom.py
claude plugin validate .
```

## Cập nhật từ upstream (khi nằm trong repo Bill-Dao, thư mục `phapche-plugin/`)

```bash
git config merge.ours.driver true
git fetch https://github.com/nguyenvansuai/phapche-hopdong main
git diff 95b6cb9 FETCH_HEAD --stat
git subtree pull --prefix=phapche-plugin https://github.com/nguyenvansuai/phapche-hopdong main -m "Cập nhật upstream phapche-hopdong"
python3 phapche-plugin/custom/dong_bo.py
python3 phapche-plugin/tests/test_cong_cu.py && python3 phapche-plugin/tests/test_vn_custom.py
claude plugin validate phapche-plugin
```

- Đọc diff upstream trước khi pull như một lần kiểm toán mới (hook, `.mcp.json`, lệnh mạng/subprocess trong `tools/`, chỉ dẫn lạ trong SKILL.md). Thay `95b6cb9` bằng commit upstream lần cập nhật gần nhất.
- `.mcp.json`, `marketplace.json`, `plugin.json` luôn giữ bản tùy chỉnh khi merge (`.gitattributes`).
- Xung đột ở bản sao trong `skills/*/scripts|references`: giải quyết ở `tools/`, `shared/` rồi chạy `custom/dong_bo.py`.
- Sau cập nhật: tăng `version` (ví dụ `1.0.0-vn.2`), `claude plugin marketplace update phapche-vn-custom`, `claude plugin update phapche-hopdong@phapche-vn-custom`.

## Gỡ cài đặt và khôi phục

- Gỡ: `claude plugin uninstall phapche-hopdong@phapche-vn-custom --scope local`, rồi `claude plugin marketplace remove phapche-vn-custom`.
- Bỏ một thay đổi: `git revert <commit vn-custom>`. Xem bản gốc: `git show 95b6cb9:<file>`.
- Gỡ khỏi repo: `git rm -r phapche-plugin` rồi commit.
