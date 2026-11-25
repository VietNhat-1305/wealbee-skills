# Đóng góp

Cảm ơn bạn quan tâm. Bộ skill này phục vụ người đọc dùng số liệu để ra quyết định tiền bạc, nên mọi thay đổi giữ 4 nguyên tắc trong README: chỉ dùng số API trả về, mỗi số có nguồn, so với trung vị thay cho "tốt/xấu", không khuyến nghị.

## Trước khi mở pull request

```bash
python3 scripts/validate_skills.py
python3 -m unittest discover -s tests
```

CI chạy hai lệnh này trên Python 3.9 và 3.12.

## Thêm hoặc sửa một skill

- Thư mục `skills/<tên>/`, tên bắt đầu bằng `wealbee-`, chữ thường và gạch nối.
- `SKILL.md` có frontmatter `name` (trùng tên thư mục) và `description` (dưới 1024 ký tự). Description nói skill làm gì và khi nào dùng, kèm vài câu người dùng hay hỏi.
- Phần thân dưới 500 dòng. Phần dài thì tách sang `references/`.
- Lấy số qua `../wealbee-data/scripts/wealbee.py`, không gọi API riêng. Cần dữ liệu mới thì thêm lệnh vào script, kèm test.
- Có khuôn đầu ra cố định (tên thư mục, file Markdown, thư mục `evidence/`).
- Script giữ chỉ dùng thư viện chuẩn, chạy được với Python 3.9.

## Eval

Mỗi eval là một thư mục `skills/<skill>/evals/<tên-case>/` gồm `prompt.md`, `case.yaml` (`schema_version: "1.1"`) và `graders/NN-*.md`. Mỗi grader là một câu kiểm được. Eval gọi API thật nên cần `WEALBEE_API_KEY`. Có Claude Code bản mới thì chạy được bằng lệnh sau, trong thư mục skill:

```bash
claude plugin eval . --allow-tools Write,Edit,Bash
```

## Không bao giờ

- Commit khoá API, file `.env` hay kết quả có chứa khoá. CI quét chuỗi `wb_live_` và `wb_test_`.
- Thêm câu chữ mang tính khuyến nghị ("nên mua", "giá mục tiêu", "cổ phiếu tiềm năng") vào khuôn đầu ra.
- Đưa số liệu không có trong API vào ví dụ mẫu.

## Báo lỗi dữ liệu

Số trong API khác file PDF gốc thì mở issue, ghi mã, kỳ, chỉ tiêu, số API, số trong PDF và trang PDF.
