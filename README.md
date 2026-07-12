# Olist E-commerce: Seller Performance & Churn Analysis

> **Lưu ý:** Dự án này tập trung xây dựng các chỉ số sức khỏe (Business Health Indicators) có tính giải thích cao để đề xuất hành động trực tiếp, không sử dụng Machine Learning.

---

## 1. Business Context (Bối cảnh Kinh doanh)
Dự án phân tích hiệu suất vận hành và xác định sớm rủi ro rời bỏ (churn) của các nhà bán hàng (Sellers) trên sàn Olist (Brazil). Thay vì chỉ báo cáo doanh số lịch sử thông thường, cuộc phân tích tập trung phát hiện các tín hiệu cảnh báo sớm (early warning signals), giúp đội ngũ Partner Support chủ động giữ chân các Seller có giá trị trước khi họ ngừng hoạt động.

---

## 2. Business Questions (Câu hỏi Kinh doanh)
Dự án tập trung giải quyết các bài toán kinh doanh cốt lõi:
*   **Chỉ báo chính:** Yếu tố vận hành nào là chỉ báo mạnh nhất khiến seller rời bỏ hệ thống?
*   **Tác động Logistics:** Hiệu suất giao hàng ảnh hưởng thế nào đến sự hài lòng của khách hàng?
*   **Độ ưu tiên:** Đội ngũ Partner Support nên ưu tiên hỗ trợ những seller nào trong tuần?
*   **Rủi ro tài chính:** Tổng giá trị giao dịch (GMV) hiện tại đang bị đe dọa là bao nhiêu?
*   **Hạn chế địa lý:** Khu vực địa lý nào đang gặp vấn đề về vận hành cần cải thiện?

---

## 3. Analytical Framework (Khung Phân tích)
Phân tích rủi ro của Seller dựa trên 5 khía cạnh vận hành chính:

*   **Seller Activity (Mức độ hoạt động):** Seller dừng nhận đơn mới từ bao giờ?
*   **Customer Experience (Trải nghiệm khách hàng):** Điểm đánh giá sụt giảm có liên quan đến việc giao hàng trễ không?
*   **Revenue Stability (Doanh thu):** Seller có bị giảm doanh số liên tục nhiều tháng?
*   **Operational Performance (Logistics):** Các vấn đề vận chuyển có phải là nguyên nhân chính khiến khách hàng không hài lòng?
*   **Geographic Risk (Địa lý):** Có vùng/bang nào gặp vấn đề hệ thống về vận hành?

---

## 4. Dataset & Seller Health Indicators (Chỉ số Sức khỏe Seller)

### Dữ liệu nguồn (Data Sources)
Dữ liệu được tích hợp từ các bảng gốc của Olist: `Orders`, `Order Items`, `Customers`, `Products`, `Payments`, `Reviews`, và `Sellers`.

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
Quy trình xử lý dữ liệu phục vụ ra quyết định:

`Dữ liệu thô (Data)` ➔ `Chỉ số Kinh doanh (Business Indicators)` ➔ `Chấm điểm Rủi ro (Risk Scoring)` ➔ `Dashboard trực quan (Power BI)` ➔ `Hành động từ Partner Support` ➔ `Giữ chân Seller (Seller Retention)`

---

## 6. Dashboard Overview (Tổng quan Dashboard)
![Dashboard](assets/dashboard.png)

Dashboard được thiết kế riêng cho team Partner Support để nhận diện nhanh các seller cần can thiệp khẩn cấp và tối ưu nguồn lực giữ chân dòng tiền (GMV):
*   **Executive Summary Page:**
    *   Các chỉ số KPIs cốt lõi (Tổng GMV gặp rủi ro, Số lượng seller rủi ro cao).
    *   Biểu đồ phân bổ mức độ rủi ro (Risk Distribution).
    *   Ma trận tương quan hiệu suất (Late Delivery vs Review Score).
    *   Danh sách ưu tiên can thiệp khẩn cấp (Action Required List) kèm gợi ý hành động cụ thể.

---

## 7. Key Findings (Các Kết quả Chính)
1.  **Giao trễ là nguyên nhân chính:** Sự chậm trễ giao hàng là chỉ báo mạnh nhất khiến seller rời bỏ.
2.  **Ngưỡng nhạy cảm 20%:** Độ hài lòng của khách hàng (Review Score) giảm cực nhanh khi tỷ lệ giao trễ vượt mốc 20%.
3.  **Doanh thu giảm 2 tháng liên tiếp:** Đây là dấu hiệu cảnh báo sớm rõ ràng nhất trước khi seller dừng hoạt động hẳn.
4.  **Hạn chế logistics vùng miền:** Các bang vùng sâu vùng xa (đặc biệt là Amazonas - AM) có tỷ lệ rủi ro cao nhất do hạ tầng vận chuyển yếu kém.

---

## 8. Recommendation Engine (Động cơ Khuyến nghị)
Dựa vào điểm số rủi ro Churn Risk Score, hệ thống tự động đưa ra các đề xuất hành động cụ thể cho đội ngũ vận hành:

| Mức độ Rủi ro (Risk Level) | Hành động Đề xuất (Suggested Action) |
|---------------------------|-------------------------------------|
| **Critical (Nghiêm trọng)** | Liên hệ trực tiếp trong 24 giờ, đề xuất giải pháp/ưu đãi phí hoa hồng để giữ chân |
| **High (Cao)** | Đánh giá lại hiệu suất logistics, tìm phương án tối ưu đối tác vận chuyển |
| **Medium (Trung bình)** | Tiếp tục theo dõi sát sao hiệu suất trong 30 ngày tiếp theo |
| **Low (Thấp)** | Không cần hành động, duy trì gửi báo cáo hiệu suất tự động định kỳ |

---

## 9. Business Impact (Tác động Kinh doanh)
Tác động thực tế đem lại cho team Partner Support:
*   **Phát hiện sớm:** Chủ động nhận diện seller có rủi ro rời đi từ sớm nhờ các chỉ số cảnh báo.
*   **Tối ưu nguồn lực:** Tập trung hỗ trợ nhóm seller có ảnh hưởng doanh thu lớn trước (GMV exposure).
*   **Giám sát liên tục:** Cập nhật liên tục hiệu suất vận hành của seller qua dashboard tự động.
*   **Hạn chế thất thoát:** Giúp giữ chân seller kịp thời, bảo vệ dòng doanh thu ước tính khoảng **$375,000 GMV**.

---

## 10. Technical Implementation (Triển khai Kỹ thuật)
Kiến trúc dữ liệu tự động hóa đằng sau các chỉ số kinh doanh:
*   **Ingestion:** Kéo dữ liệu tự động từ Kaggle API & Exchange Rate API, chạy validate chất lượng bằng `Great Expectations`.
*   **Transformation:** Làm sạch và denormalize các bảng nguồn thành bảng `orders_master` duy nhất (PostgreSQL Silver Layer).
*   **Analytics Layer:** Tính toán các chỉ số sức khỏe và churn risk score bằng SQL tối ưu (PostgreSQL Gold Layer - CTEs, Window Functions, Dynamic Thresholds).

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
