# naritopik.com — trang công khai để Google tìm thấy (tầng miễn phí) + sau này VIP

Repo này chạy GitHub Pages ở tên miền `naritopik.com` (file `CNAME`). Học liệu nội bộ cho lớp ở repo `nttn6889/narikoreanbox` (hoc.naritopik.com).

## 3 tầng (cô chốt 26/10/2026)
- **Tầng 1 · Biết (miễn phí, trên site này):** kiến thức tóm tắt: bảng ngữ pháp câu 1–4, dấu hiệu từng dạng câu (bản tóm tắt), cấu trúc đề, giải đề thật 83/91/96/102 (đáp án + giải ngắn), danh sách từ vựng.
- **Tầng 2 · Luyện (VIP tự học, chưa làm — cần đăng nhập + thanh toán):** đề có chấm + giải thích từng lựa chọn sai, luyện theo dạng, lộ trình từ vựng, viết 51–54 so bài mẫu.
  Giá: 1 tháng 99.000đ · 3 tháng 199.000đ (khai trương 149.000đ cho 100 bạn đầu) · 6 tháng 299.000đ. Không bán gói ngày/tuần.
- **Tầng 3 · Sửa (học với cô):** giáo án / bản trình chiếu của cô **không bao giờ** đưa lên tầng 1–2; cô chấm 53/54, lộ trình riêng, app. Học viên lớp được dùng VIP miễn phí;
  đã mua VIP thì tiền VIP trừ vào học phí. Chấm viết lẻ cho người ngoài: không bán (giữ làm quyền lợi của lớp).
- Không đưa nội dung chép từ sách (Seoul, Cool/Quick TOPIK, 합격 레시피, 박이정, EBS) lên site này.

## Cấu trúc
- Site tĩnh sinh bằng `python3 tools/build.py` → ghi `index.html` các thư mục + `sitemap.xml`, `robots.txt`. **Không sửa tay file sinh ra.**
- Bài viết tay: `noi-dung/*.html`, dòng đầu là chú thích JSON (`path`, `title` ≤ ~65 ký tự, `desc` ≤ ~160, `type: page|article`, `crumb`, `lead`, `h1`, `nav`, `related`, `ld`).
  Bài (`article`) tự có mục lục (≥ 3 `<h2>`), khung “Biết rồi, giờ luyện” (`UPSELL`), JSON-LD Article + Breadcrumb.
- Ngữ pháp: `python3 tools/lay_du_lieu.py ../narikoreanbox` → `data/ngu-phap.json` (nhóm V01_*/V03_* của kho từ + nghĩa câu ví dụ `EXV` + nhãn nhóm `GN` từ `ngu-phap-luyen/`),
  rồi build: trang `/ngu-phap-topik/cau-1-2|cau-3-4/` + mỗi nhóm một trang.
- `assets/site.css` giao diện chung (tím `#53468F`, vàng `#D4A843`, font Be Vietnam Pro). Logo trong `assets/`.
- `ve-co/`, `hoc-cung-co/`, `thi-thu/` = trang chuyển hướng sang hoc.naritopik.com (link quảng cáo cũ) — giữ nguyên.
- Thêm bài: tạo `noi-dung/NN-ten.html`, thêm thẻ vào trang hub (`19-viet-hub`, `29-de-thi-hub`, trang chủ), build, kiểm tra Playwright (khung 390px, không cuộn ngang), commit.

## Việc tiếp theo
- Google Search Console (cô xác minh tên miền), gửi `sitemap.xml`.
- Bài mới: câu 53, 54, giải đề thật, dấu hiệu từng dạng câu đọc (bản tóm tắt).
- Giai đoạn 2 (VIP): kho riêng tư + Cloudflare Pages + Supabase (tài khoản: miễn phí / VIP / lớp) + SePay (VietQR, webhook kích hoạt).
