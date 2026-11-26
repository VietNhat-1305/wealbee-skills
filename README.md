# Wealbee Skills

Bộ Agent Skills mã nguồn mở để AI phân tích cổ phiếu Việt Nam bằng số liệu báo cáo tài chính đã kiểm chứng, thay vì số nhớ mang máng.

Mỗi skill là một quy trình phân tích hoàn chỉnh. Skill lấy số qua [Wealbee Data API](https://data.wealbee.com/docs), tính tăng trưởng, biên, ROE và trung vị theo một cách thống nhất, rồi viết báo cáo có link tới đúng file PDF gốc. Skill không đưa khuyến nghị mua bán.

[English below](#english)

## Có gì trong bộ này

| Skill | Bạn hỏi | Bạn nhận |
|---|---|---|
| [`wealbee-snapshot`](skills/wealbee-snapshot/SKILL.md) | "Phân tích nhanh VNM" | Một trang: kết quả quý, xu hướng 6 quý, vị trí so với mặt bằng, tin gần đây, điểm cần đọc kỹ |
| [`wealbee-earnings-review`](skills/wealbee-earnings-review/SKILL.md) | "Đọc BCTC quý 3 của HPG" | Đọc sâu một BCTC: kết quả kinh doanh, cân đối, dòng tiền, phép kiểm, lịch sử sửa |
| [`wealbee-peer-compare`](skills/wealbee-peer-compare/SKILL.md) | "So sánh VCB, BID, CTG" | Bảng 2–10 mã cùng kỳ, cạnh trung vị, kèm file CSV |
| [`wealbee-benchmark`](skills/wealbee-benchmark/SKILL.md) | "ROE 20% của FPT là cao hay thấp?" | Trung vị, p25–p75 của mọi BCTC cùng loại hình, vị trí của mã |
| [`wealbee-news-digest`](skills/wealbee-news-digest/SKILL.md) | "Tin về ngân hàng tuần này" | Bản tin gom từ nhiều báo, tách dữ kiện với nhận định |
| [`wealbee-fact-check`](skills/wealbee-fact-check/SKILL.md) | "Số trong bài này đúng không?" | Bảng Đúng / Sai / Không kiểm được, kèm số đúng và nguồn |
| [`wealbee-explain`](skills/wealbee-explain/SKILL.md) | "ROE là gì, cho ví dụ thật" | Định nghĩa từ từ điển 490 thuật ngữ, ví dụ tính bằng BCTC thật |
| [`wealbee-watchlist`](skills/wealbee-watchlist/SKILL.md) | "Danh mục của tôi có gì mới từ hôm qua?" | BCTC mới, BCTC bị sửa hay bị rút, tin mới, gom theo mã |
| [`wealbee-earnings-reaction`](skills/wealbee-earnings-reaction/SKILL.md) | "Từ lúc ra BCTC đến giờ VNM tăng bao nhiêu?", "backtest mỗi lần công bố BCTC" | Lợi suất sau 1, 5, 10, 20 phiên và đến nay so với chỉ số; backtest nhiều mã theo nhóm tăng trưởng lợi nhuận |
| [`wealbee-data`](skills/wealbee-data/SKILL.md) | (nền tảng) | Cài khoá, công cụ dòng lệnh `wealbee.py`, quy tắc chung về số liệu và pháp lý |

Xem đầu ra thật, chạy ngày 25/11/2026:

- [Phân tích nhanh Vinamilk (VNM), quý 3/2026](examples/wealbee-snapshot-vnm-20261125/SNAPSHOT.md)
- [So sánh 5 ngân hàng BID, CTG, MBB, TCB, VCB, quý 3/2026](examples/wealbee-peer-compare-ngan-hang-20261125/COMPARISON.md)
- [Phản ứng giá sau 90 lần công bố BCTC của VN30 năm 2026, và VNM từ lúc công bố đến nay](examples/wealbee-earnings-reaction-vn30-20261126/REACTION.md)

## Cài đặt

### Claude Code (khuyên dùng)

```text
/plugin marketplace add VietNhat-1305/wealbee-skills
/plugin install wealbee-skills@wealbee
```

Hoặc chép thư mục `skills/` vào `~/.claude/skills/` (dùng cho mọi dự án) hoặc `.claude/skills/` trong dự án. Giữ nguyên `wealbee-data` cạnh các skill khác, vì mọi skill gọi script trong đó.

### Agent khác theo chuẩn Agent Skills

Chép thư mục `skills/` vào chỗ agent đọc skill. Agent cần chạy được Python 3.9 trở lên và gọi mạng tới `data.wealbee.com`. Script chỉ dùng thư viện chuẩn, không cần `pip install`. Skill `wealbee-earnings-reaction` cần thêm mạng tới nguồn giá công khai (VNDirect, dự phòng DNSE) hoặc file giá CSV của bạn.

### Khoá API

1. Lấy khoá tại https://wealbee.com/developers.
2. Đặt khoá bằng một trong hai cách:
   - biến môi trường: `export WEALBEE_API_KEY=wb_live_...`
   - hoặc ghi một dòng `WEALBEE_API_KEY=wb_live_...` vào file `~/.config/wealbee/.env`
3. Kiểm tra: `python3 skills/wealbee-data/scripts/wealbee.py account`

Không dán khoá vào khung chat. Script không bao giờ in khoá ra kết quả. Riêng skill `wealbee-explain` khi chỉ tra từ điển thì không cần khoá.

## Dùng thử

Sau khi cài, hỏi bình thường bằng tiếng Việt hoặc tiếng Anh:

```text
Phân tích nhanh HPG quý gần nhất
So sánh MWG với FRT về lợi nhuận và ROE
Biên lợi nhuận gộp 25% của DGC là cao hay thấp so với thị trường?
Kiểm tra giúp: "VNM lãi 3.000 tỷ quý 3/2026, tăng 20%"
Có gì mới về VNM, FPT, HPG từ hôm qua?
```

Kết quả ghi vào thư mục làm việc dạng `wealbee-<skill>-<chủ-đề>-<ngày>/`. Thư mục gồm file báo cáo Markdown và thư mục `evidence/` chứa JSON thô, để ai cũng kiểm lại được từng số.

## Nguyên tắc

1. **Chỉ dùng số API trả về.** Thiếu số thì ghi "Data API chưa có", không ước đoán.
2. **Mỗi số có kỳ, đơn vị, phạm vi hợp nhất hay riêng, và link file PDF gốc.** BCTC chưa kiểm chứng xong (`needs_review`) được ghi rõ.
3. **Đặt số cạnh trung vị thay cho "tốt" hay "xấu".** Trung vị tính trên mọi BCTC cùng loại hình và cùng kỳ.
4. **Không khuyến nghị mua, bán, nắm giữ, không giá mục tiêu, không dự báo giá.** Luật Chứng khoán 2019 coi khuyến nghị là tư vấn đầu tư, cần giấy phép. Chi tiết ở [`tuan-thu.md`](skills/wealbee-data/references/tuan-thu.md).

Cách tính từng chỉ số nằm ở [`chi-so.md`](skills/wealbee-data/references/chi-so.md). Giới hạn dữ liệu hiện tại nằm ở [`du-lieu.md`](skills/wealbee-data/references/du-lieu.md), ví dụ doanh thu ngân hàng còn trống và vốn chủ công ty mẹ chưa có ở mọi BCTC.

## Cấu trúc

```text
.claude-plugin/          plugin.json, marketplace.json (cài bằng /plugin)
skills/
  wealbee-data/          nền tảng: SKILL.md, scripts/wealbee.py, references/
  wealbee-*/             9 skill phân tích, mỗi skill một SKILL.md (một số có evals/)
examples/                đầu ra thật, kèm evidence/
scripts/validate_skills.py   kiểm cấu trúc skill, link, eval, và quét khoá lộ
tests/                   test cho wealbee.py, chạy không cần mạng
```

## Phát triển

```bash
python3 scripts/validate_skills.py      # kiểm cấu trúc và link
python3 -m unittest discover -s tests   # test script, không gọi mạng
```

Eval của từng skill nằm ở `skills/<skill>/evals/`, đúng định dạng `claude plugin eval` đọc. Eval gọi API thật nên cần khoá. Xem [CONTRIBUTING.md](CONTRIBUTING.md).

## Giấy phép và lưu ý

Mã nguồn theo giấy phép [MIT](LICENSE). Số liệu thuộc Wealbee Data API và theo điều khoản của dịch vụ đó.

Nội dung do các skill tạo ra là thông tin tham khảo, không phải khuyến nghị đầu tư. Hãy đọc file BCTC gốc trước khi ra quyết định.

---

## English

**Wealbee Skills** is an open-source set of Agent Skills for analysing Vietnamese listed companies (HOSE, HNX, UPCOM) with verified quarterly financial statements from the [Wealbee Data API](https://data.wealbee.com/docs).

Each skill is a complete workflow:

- **snapshot**: one stock on one page;
- **earnings-review**: a deep read of one filing;
- **peer-compare**: several companies side by side;
- **benchmark**: a metric against the median of all filings of the same company type;
- **news-digest**: news clustered from many outlets;
- **fact-check**: checks the numbers in any text against the filings;
- **explain**: a term explained with real filed numbers;
- **watchlist**: what changed since a given date;
- **earnings-reaction**: how the price moved after each financial statement release, and an event-study backtest across tickers and quarters.

Every number carries its period, unit, scope and a link to the source PDF. Ratios are computed the same way in every skill. The skills never give buy, sell or hold calls, because Vietnamese securities law treats those as licensed investment advice.

**Install (Claude Code):** `/plugin marketplace add VietNhat-1305/wealbee-skills`, then `/plugin install wealbee-skills@wealbee`. You can also copy `skills/` into `~/.claude/skills/`.

**API key:** get one at https://wealbee.com/developers and set `WEALBEE_API_KEY` as an environment variable or in `~/.config/wealbee/.env`.

**Requirements:** Python 3.9+, standard library only.

The skills write reports in Vietnamese by default and switch to English when asked. Sample outputs are in [`examples/`](examples/). The code is under the MIT licence. Outputs are for information only and are not investment advice.
