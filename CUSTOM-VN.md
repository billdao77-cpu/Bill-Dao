# Bản tùy chỉnh `vn-custom` – skill-sales-marketing

Dựa trên upstream `nguyenvansuai/skill-sales-marketing` commit `d1a67fb`, kiểm toán bảo mật ngày 26/11/2026. Thay đổi nằm trong các commit `vn-custom: ...`.

## Khác với upstream

| Nhóm | Thay đổi | File |
|---|---|---|
| Quyền truy cập | Bỏ 8 MCP server từ xa: Gmail, Google Calendar, Google Drive, Canva, **Shopify**, **HubSpot**, **TikTok Ads**, Notion. Plugin không kết nối tài khoản quảng cáo, CRM, cửa hàng. | `.mcp.json` (rỗng), `.claude-plugin/marketplace.json` |
| An toàn dữ liệu | `tao_pipeline.py`, `bang_cai_khuyen_mai.py` không ghi đè file (cần `--ghi-de`), kiểm tra đuôi file; tên sales bắt đầu bằng `=+-@` không thành công thức Excel; `validate_copy.py --fix` ghi `<tên>.nfc<đuôi>`, không sửa file gốc | `skills/*/scripts/` |
| Nguyên tắc | Mục 13–20: kiểm tra chất lượng dữ liệu, nhãn số liệu, không hứa hiệu quả, mọi thao tác ghi qua connector phải xác nhận (thay câu "tạo liên hệ, ghi chú được" của HubSpot), không đưa dữ liệu khách/doanh thu vào tìm kiếm web, nơi lưu hồ sơ doanh nghiệp (tránh commit lên git), chống prompt injection, file mới | `shared/nguyen-tac-chung.md` |
| Cấu trúc skill | Thẻ 10 mục cho 17 skill (vai trò, bối cảnh, mục tiêu, đầu vào, tiêu chí đánh giá, ví dụ, giới hạn – quy trình/đầu ra trong SKILL.md) | `shared/the-skill.md` |
| Agent mới | `marketing-strategist`, `content-creator`, `sales-coach`, `funnel-architect`, `growth-analyst`, `crm-customer-success` – điều phối skill có sẵn; không có Write/Edit | `agents/` |
| Workflow mới | `/chien-luoc-marketing`, `/chien-dich-quang-cao`, `/pheu-ban-hang`, `/toi-uu-sales`, `/phan-tich-hieu-qua` | `commands/` |
| Kiểm thử | Test riêng | `tests/test_vn_custom.py` |
| Đồng bộ | `custom/dong_bo.py` – chép `shared/` vào skill, không sinh lại `.mcp.json`, `dist/`, bản ChatGPT | `custom/dong_bo.py` |

Không dùng trong Claude Code, giữ nguyên upstream và **chưa vá**: `dist/`, `chatgpt/`, `openai/`, `.agents/`, `example/`, `qua-tang/` (3 file Excel mẫu – đã kiểm tra không có macro/liên kết ngoài).

## Kiểm thử

```bash
python3 tests/chay_kiem_thu.py
python3 tests/test_vn_custom.py
claude plugin validate .
```

## Cập nhật từ upstream (khi nằm trong repo Bill-Dao, thư mục `sales-plugin/`)

```bash
git config merge.ours.driver true
git fetch https://github.com/nguyenvansuai/skill-sales-marketing main
git diff d1a67fb FETCH_HEAD --stat
git subtree pull --prefix=sales-plugin https://github.com/nguyenvansuai/skill-sales-marketing main -m "Cập nhật upstream skill-sales-marketing"
python3 sales-plugin/custom/dong_bo.py
python3 sales-plugin/tests/chay_kiem_thu.py && python3 sales-plugin/tests/test_vn_custom.py
claude plugin validate sales-plugin
```

- Đọc diff upstream trước khi pull như một lần kiểm toán mới (hook, `.mcp.json`, lệnh mạng/subprocess trong script, chỉ dẫn lạ trong SKILL.md).
- `.mcp.json`, `marketplace.json`, `plugin.json` luôn giữ bản tùy chỉnh khi merge (`.gitattributes`).
- Xung đột ở `skills/*/references/*`: giải quyết ở `shared/` rồi chạy `custom/dong_bo.py`. Xung đột ở 3 script đã vá: giữ đoạn `vn-custom` (chống ghi đè).
- Sau cập nhật: tăng `version` (ví dụ `1.0.0-vn.2`), `claude plugin marketplace update sales-marketing-vn-custom`, `claude plugin update tron-bo-skill-sales-marketing@sales-marketing-vn-custom`.

## Gỡ cài đặt và khôi phục

- Gỡ: `claude plugin uninstall tron-bo-skill-sales-marketing@sales-marketing-vn-custom --scope local`, rồi `claude plugin marketplace remove sales-marketing-vn-custom`.
- Bỏ một thay đổi: `git revert <commit vn-custom>`. Xem bản gốc: `git show d1a67fb:<file>`.
- Gỡ khỏi repo: `git rm -r sales-plugin` rồi commit.
