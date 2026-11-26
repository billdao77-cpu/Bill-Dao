# Bản tùy chỉnh `vn-custom` – plugin hanhchinh-nhansu

Nhánh này dựa trên upstream `nguyenvansuai/hanhchinh-nhansu` tại commit `268678e` (tag `upstream-268678e`),
đã kiểm toán bảo mật ngày 26/11/2026. Mọi thay đổi nằm trong các commit `vn-custom: ...` để dễ xem lại và hoàn tác.

## Khác với upstream

| Nhóm | Thay đổi | File |
|---|---|---|
| Quyền truy cập | Bỏ 6 MCP server từ xa (Gmail, Calendar, Drive, Microsoft 365, Zoom, Slack có OAuth clientId cứng). Plugin không tự kết nối dịch vụ nào; connector nếu cần thì người dùng tự bật trong Claude. | `.mcp.json` (rỗng), `.claude-plugin/marketplace.json` |
| Quyền truy cập | Agent `tham-dinh-hcns` chỉ được dùng Read, Grep, Glob, Bash; thêm quy tắc chống prompt injection, che dữ liệu cá nhân | `agents/tham-dinh-hcns.md` |
| An toàn dữ liệu | Công cụ xuất file không ghi đè file đã có (cần `ghi_de=true`), bắt buộc đúng đuôi `.docx/.xlsx/.ics` | `tools/__init__.py` |
| An toàn dữ liệu | Sổ văn bản CSV chống chèn công thức Excel (`=`, `+`, `-`, `@`) | `tools/so_van_ban.py` |
| Kiểm tra đầu vào | Mọi công cụ kiểm tra tham số theo schema: thiếu bắt buộc, tham số lạ, giá trị ngoài danh sách | `tools/__init__.py` |
| CLI | `--ds`, `--schema <tên>`; lỗi trả JSON thay vì traceback | `tools/cong_cu.py` |
| Nghiệp vụ mới | Công cụ `tinh_luong_lam_them`, `kiem_tra_gio_lam_them`; skill `cham-cong-tinh-luong`; lệnh `/chot-cong` | `tools/cham_cong.py`, `skills/cham-cong-tinh-luong/`, `commands/chot-cong.md` |
| Hướng dẫn | Nguyên tắc chung thêm: xác minh hiệu lực văn bản từ nguồn chính thức, nhãn [Đã xác minh]/[Chưa có căn cứ], kiểm tra đầu vào – mâu thuẫn, thẩm quyền và quyết định nhân sự, bảo mật dữ liệu, chống prompt injection | `shared/nguyen-tac-chung.md` (+ bản sao trong `skills/*/references/`) |
| Tham số pháp lý | Cập nhật nhãn NĐ 161/2026 (lương cơ sở), ghi chú ngày áp dụng biểu thuế TNCN 5 bậc | `tools/tham_so.py`, `shared/quy-dinh-lao-dong-2026.md` |
| Kiểm thử | Test riêng cho phần tùy chỉnh | `tests/test_vn_custom.py` |
| Đồng bộ | `custom/dong_bo.py` chép `shared/` và `tools/` vào từng skill mà không sinh lại `.mcp.json`, `dist/`, bản ChatGPT | `custom/dong_bo.py` |

Không dùng tới khi chạy trong Claude Code (giữ nguyên từ upstream, không được nạp): `dist/`, `chatgpt/`, `openai/`, `.agents/`, `example/`.
Các thư mục này **chưa** được vá (bản ChatGPT/Codex vẫn dùng mã cũ) – không dùng chúng từ nhánh này.

## Kiểm thử

```bash
python3 tests/test_cong_cu.py
python3 tests/test_vn_custom.py
claude plugin validate .
```

## Cập nhật từ upstream mà không mất phần tùy chỉnh

Bản này nằm trong repo Bill-Dao, thư mục `hcns-plugin/`, được thêm bằng `git subtree` (giữ nguyên lịch sử upstream và các commit `vn-custom:`). Chạy từ gốc repo Bill-Dao:

```bash
git config merge.ours.driver true
git fetch https://github.com/nguyenvansuai/hanhchinh-nhansu main
git diff 268678e FETCH_HEAD --stat
git subtree pull --prefix=hcns-plugin https://github.com/nguyenvansuai/hanhchinh-nhansu main -m "Cập nhật upstream hanhchinh-nhansu"
python3 hcns-plugin/custom/dong_bo.py
python3 hcns-plugin/tests/test_cong_cu.py && python3 hcns-plugin/tests/test_vn_custom.py
claude plugin validate hcns-plugin
```

- **Đọc diff của upstream trước khi pull** (lệnh `git diff` ở trên) và coi đó là một lần kiểm toán mới. Cần chú ý file mới trong `hooks/`, các thay đổi ở `.mcp.json` hoặc `settings.json`, lệnh `subprocess` hoặc truy cập mạng trong `tools/`, và các câu chỉ dẫn lạ trong `SKILL.md`. Thay `268678e` bằng commit upstream của lần cập nhật gần nhất.
- Khi merge, `.mcp.json`, `.claude-plugin/marketplace.json` và `.claude-plugin/plugin.json` luôn giữ bản của nhánh này (do `.gitattributes`, cần bật `merge.ours.driver`).
- Nếu xung đột ở `skills/*/scripts/tools/*` hoặc `skills/*/references/*`: giải quyết ở `tools/` và `shared/` (đây là nguồn), rồi chạy `python3 hcns-plugin/custom/dong_bo.py` để sinh lại các bản sao.
- Sau khi cập nhật, tăng `version` trong `.claude-plugin/plugin.json` và `marketplace.json` (ví dụ `1.0.0-vn.2`), rồi chạy `claude plugin marketplace update hcns-vn-custom` và `claude plugin update hanhchinh-nhansu@hcns-vn-custom`.

## Khôi phục bản gốc

- Xem đúng bản upstream đã kiểm toán: `git show 268678e:README.md`, hoặc lấy lại toàn bộ bằng `git archive 268678e | tar -x -C /đường/dẫn/tạm`.
- Bỏ một thay đổi cụ thể: `git revert <commit vn-custom: ...>` (các commit vẫn còn trong lịch sử Bill-Dao).
- Gỡ plugin khỏi Claude Code: `claude plugin uninstall hanhchinh-nhansu@hcns-vn-custom --scope local`, rồi `claude plugin marketplace remove hcns-vn-custom`.
- Gỡ hẳn khỏi repo: `git rm -r hcns-plugin` rồi commit. Lịch sử vẫn còn để khôi phục khi cần.
