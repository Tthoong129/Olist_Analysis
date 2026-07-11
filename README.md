# Olist E-commerce: Seller Performance & Churn Analysis

> **Lưu ý quan trọng:** Dự án này không nhằm mục đích dự báo rời bỏ (churn) bằng Machine Learning. Thay vào đó, dự án tập trung vào việc xây dựng các chỉ số kinh doanh có tính giải thích cao (interpretable business indicators) để giúp các bên liên quan hiểu rõ lý do tại sao người bán gặp rủi ro và cần thực hiện hành động cụ thể nào để cải thiện.

---

## 1. Business Context (Bối cảnh Kinh doanh)
Dự án này phân tích hiệu suất của nhà bán hàng trên nền tảng Olist (Brazil) để xác định các mô hình vận hành liên quan đến rủi ro rời bỏ hệ thống (seller churn). Thay vì chỉ báo cáo doanh số lịch sử thông thường, cuộc phân tích tập trung phát hiện các tín hiệu cảnh báo sớm (early warning signals), cho phép đội ngũ Partner Support chủ động giữ chân các nhà bán hàng có giá trị trước khi họ ngừng hoạt động.

---

## 2. Business Questions (Câu hỏi Kinh doanh)
Để hỗ trợ ra quyết định, dự án tập trung giải quyết các câu hỏi kinh doanh cốt lõi:
*   **Chỉ báo chính:** Yếu tố vận hành nào là chỉ báo mạnh nhất cho việc seller rời bỏ hệ thống?
*   **Tác động Logistics:** Hiệu suất giao hàng ảnh hưởng như thế nào đến sự hài lòng của khách hàng?
*   **Độ ưu tiên:** Đội ngũ Partner Support nên ưu tiên hỗ trợ các seller nào trong tuần này?
*   **Rủi ro tài chính:** Tổng giá trị giao dịch (GMV) hiện tại đang bị đe dọa là bao nhiêu?
*   **Hạn chế địa lý:** Khu vực địa lý nào đang gặp vấn đề về vận hành cần cải thiện?

---

## 3. Analytical Framework (Khung Phân tích)
Dự án tiếp cận toàn diện qua các khía cạnh vận hành để đánh giá rủi ro:

*   **Seller Activity (Mức độ hoạt động):** Seller có dấu hiệu ngừng nhận đơn hàng mới từ bao giờ?
*   **Customer Experience (Trải nghiệm khách hàng):** Điểm đánh giá sụt giảm có liên quan mật thiết đến sự chậm trễ giao hàng không?
*   **Revenue Stability (Độ ổn định doanh thu):** Seller có đang trải qua tình trạng suy thoái doanh thu liên tục qua các tháng?
*   **Operational Performance (Hiệu suất vận hành):** Các vấn đề logistics có phải là nguyên nhân chính khiến khách hàng không hài lòng?
*   **Geographic Risk (Rủi ro địa lý):** Có tiểu bang nào đang gặp vấn đề hệ thống về hiệu suất vận hành không?

---

## 4. Dataset & Seller Health Indicators (Chỉ số Sức khỏe Seller)

### Dữ liệu nguồn (Data Sources)
Dữ liệu được tích hợp từ các bảng cốt lõi của Olist: `Orders`, `Order Items`, `Customers`, `Products`, `Payments`, `Reviews`, và `Sellers`.

### Chỉ số Sức khỏe Seller (Seller Health Indicators)
Các chỉ số được tạo thêm nhằm phục vụ mục đích phân tích và chấm điểm sức khỏe kinh doanh:

| Chỉ số (Indicator) | Ý nghĩa Kinh doanh (Business Meaning) |
|-------------------|--------------------------------------|
| **Recency** | Xác định xem seller đã ngừng nhận đơn hàng mới hay chưa |
| **Late Delivery Rate** | Hiệu suất vận hành logistics của seller |
| **Revenue Trend** | Phát hiện xu hướng sụt giảm kinh doanh liên tục |
| **Recent Reviews** | Mức độ hài lòng hiện tại của khách hàng (90 ngày qua) |
| **Historical Reviews** | Điểm đánh giá nền tảng để đối chiếu chất lượng dịch vụ |
| **Churn Risk Score** | Điểm số tổng hợp đánh giá sức khỏe của seller (0 - 100) |

---

## 5. Decision Workflow (Luồng Quyết định)
Dự án được thiết kế theo luồng khép kín từ dữ liệu thô đến hành động thực tế:

`Dữ liệu thô (Data)` ➔ `Chỉ số Kinh doanh (Business Indicators)` ➔ `Chấm điểm Rủi ro (Risk Scoring)` ➔ `Dashboard trực quan (Power BI)` ➔ `Hành động từ Partner Support` ➔ `Giữ chân Seller (Seller Retention)`

---

## 6. Dashboard Overview (Tổng quan Dashboard)
![Dashboard](assets/dashboard.png)
*(Lưu ý: Bỏ ảnh chụp màn hình Power BI vào thư mục assets/dashboard.png để hiển thị)*

Dashboard được thiết kế chuyên biệt cho các quản lý Partner Support để nhanh chóng xác định các seller cần can thiệp và ưu tiên hành động dựa trên mức độ ảnh hưởng đến dòng tiền (GMV):
*   **Executive Summary Page:**
    *   Các chỉ số KPIs cốt lõi (Tổng GMV gặp rủi ro, Số lượng seller rủi ro cao).
    *   Biểu đồ phân bổ mức độ rủi ro (Risk Distribution).
    *   Ma trận tương quan hiệu suất (Late Delivery vs Review Score).
    *   Danh sách ưu tiên can thiệp khẩn cấp (Action Required List) kèm gợi ý hành động cụ thể.

---

## 7. Key Findings (Các Kết quả Chính)
1.  **Giao trễ là chỉ báo mạnh nhất:** Sự chậm trễ trong giao hàng là yếu tố vận hành có tương quan cao nhất dẫn đến việc seller rời bỏ hệ thống.
2.  **Ngưỡng nhạy cảm 20%:** Độ hài lòng của khách hàng (Review Score) suy giảm cực nhanh ngay khi tỷ lệ giao hàng trễ vượt quá ngưỡng 20%.
3.  **Cảnh báo sớm từ doanh thu:** Sụt giảm doanh thu liên tục trong 2 tháng là tín hiệu cảnh báo sớm đáng tin cậy nhất trước khi seller hoàn toàn ngừng hoạt động.
4.  **Hạn chế địa lý:** Các rào cản logistics theo vùng địa lý (đặc biệt là các bang xa như Amazonas - AM) ảnh hưởng nghiêm trọng đến khả năng duy trì hoạt động của seller.

---

## 8. Recommendation Engine (Động cơ Khuyến nghị)
Dựa vào điểm số rủi ro Churn Risk Score, hệ thống tự động đưa ra các đề xuất hành động cụ thể cho đội ngũ vận hành:

| Mức độ Rủi ro (Risk Level) | Hành động Đề xuất (Suggested Action) |
|---------------------------|-------------------------------------|
| **Critical (Nghiêm trọng)** | Liên hệ trực tiếp với seller trong vòng 24 giờ, đề xuất giải pháp/ưu đãi phí hoa hồng để giữ chân |
| **High (Cao)** | Đánh giá lại hiệu suất logistics của seller, tìm phương án tối ưu đối tác vận chuyển |
| **Medium (Trung bình)** | Tiếp tục theo dõi sát sao hiệu suất trong 30 ngày tiếp theo |
| **Low (Thấp)** | Không cần hành động, duy trì gửi báo cáo hiệu suất tự động định kỳ |

---

## 9. Business Impact (Tác động Kinh doanh)
Thay vì bị động chờ đợi seller ngừng hoạt động, giải pháp này giúp đội ngũ Partner Support:
*   **Phát hiện sớm:** Nhận diện các seller có rủi ro rời bỏ từ rất sớm nhờ các chỉ số cảnh báo.
*   **Tối ưu nguồn lực:** Ưu tiên can thiệp dựa trên mức độ ảnh hưởng doanh thu (GMV exposure).
*   **Giám sát liên tục:** Cập nhật liên tục hiệu suất vận hành của seller qua dashboard tự động.
*   **Giảm thiểu tổn thất:** Giúp giữ chân seller kịp thời, bảo vệ dòng doanh thu ước tính lên tới **$375,000 GMV**.

---

## 10. Technical Implementation (Triển khai Kỹ thuật)
Đằng sau các chỉ số kinh doanh là một hệ thống dữ liệu tự động hóa hoàn chỉnh:
*   **Ingestion:** Kéo dữ liệu tự động từ Kaggle API & Exchange Rate API, chạy kiểm tra chất lượng dữ liệu bằng `Great Expectations`.
*   **Transformation:** Làm sạch và denormalize các bảng nguồn thành bảng `orders_master` duy nhất (PostgreSQL Silver Layer).
*   **Analytics Layer:** Tính toán các chỉ số sức khỏe và churn risk score thông qua các câu lệnh SQL tối ưu (PostgreSQL Gold Layer - CTEs, Window Functions, Dynamic Thresholds).

---

## 11. Installation & Run (Cài đặt & Thực thi)

### 1. Cấu hình Kaggle API Token (Bắt buộc để tải dữ liệu)
Để script Python tự động tải dữ liệu Olist từ Kaggle mà không bị báo lỗi, bạn cần tải và đặt file xác thực của Kaggle vào đúng vị trí trên máy tính của mình theo các bước chi tiết sau:

#### **Bước 1: Tải file xác thực `kaggle.json` từ Kaggle**
1. Click truy cập trực tiếp vào đường dẫn này: **[https://www.kaggle.com/settings](https://www.kaggle.com/settings)** (Đăng nhập tài khoản Kaggle của anh nếu trình duyệt yêu cầu).
2. Chuyển sang tab **API Tokens** (như trong ảnh chụp màn hình của anh).
3. Nhìn xuống phần **Legacy API Credentials** ở phía dưới cùng.
4. Nhấn vào nút **Create Legacy API Key** (Tạo khóa API Legacy).
5. Trình duyệt sẽ tự động tải xuống file **`kaggle.json`** về máy tính (thường sẽ nằm trong thư mục `Downloads` hoặc `Tải xuống` của máy tính).

#### **Bước 2: Di chuyển file vào đúng thư mục trên máy tính**

*   **Dành cho hệ điều hành WINDOWS:**
    1. Nhấn tổ hợp phím **`Windows + R`** trên bàn phím để mở hộp thoại `Run`.
    2. Nhập chữ **`%USERPROFILE%`** vào ô trống rồi nhấn nút **OK** (hoặc gõ Enter). Một thư mục cá nhân của bạn sẽ tự động hiện lên (đường dẫn thực tế có dạng `C:\Users\Tên_Máy_Tính_Của_Bạn`).
    3. Tìm xem trong thư mục này đã có thư mục con nào tên là **`.kaggle`** (có dấu chấm ở đầu) chưa:
       * *Nếu chưa có:* Click chuột phải vào khoảng trống ➔ chọn **New (Mới)** ➔ chọn **Folder (Thư mục)**. Đặt tên thư mục này là **`.kaggle`** rồi nhấn Enter.
       * *(Mẹo: Nếu Windows không cho tạo thư mục có dấu chấm ở đầu, bạn hãy đặt tên thư mục là `.kaggle.` - có thêm dấu chấm ở cuối, Windows sẽ tự động sửa thành `.kaggle` cho bạn).*
    4. Mở thư mục **`.kaggle`** vừa tạo ra.
    5. Copy (Sao chép) file **`kaggle.json`** bạn đã tải về ở Bước 1 và Paste (Dán) vào bên trong thư mục `.kaggle` này.
    6. Đường dẫn cuối cùng phải chuẩn xác là: `C:\Users\Tên_Máy_Tính_Của_Bạn\.kaggle\kaggle.json`.

*   **Dành cho hệ điều hành macOS / LINUX:**
    1. Mở ứng dụng **Terminal** lên.
    2. Chạy lần lượt 3 dòng lệnh sau bằng cách copy-paste và gõ Enter:
       ```bash
       mkdir -p ~/.kaggle
       cp ~/Downloads/kaggle.json ~/.kaggle/
       chmod 600 ~/.kaggle/kaggle.json
       ```

---

### 2. Cài đặt môi trường
Tạo virtual environment và cài đặt thư viện:
```bash
python -m venv .venv
source .venv/bin/activate  # Trên Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Thiết lập biến môi trường
Tạo file `.env` từ file mẫu và chỉnh sửa cấu hình kết nối (nếu cần):
```bash
cp .env.example .env
```

### 4. Khởi tạo Database (Docker)
Khởi chạy PostgreSQL container:
```bash
docker-compose up -d
```

### 5. Chạy Data Pipeline
Thực thi toàn bộ luồng data tự động:
```bash
python src/pipeline.py
```
