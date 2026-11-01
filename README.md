# GHN Logistics Service – FastAPI + Swagger UI

Demo tích hợp **GHN (Giao Hàng Nhanh) API** vào microservice Python:
1. Ước tính phí vận chuyển  2. Tạo đơn  3. Theo dõi vận đơn

## Cấu trúc
```
ghn-seminar/
├── app/
│   ├── main.py         # Các endpoint FastAPI (Swagger UI tự sinh)
│   ├── ghn_client.py   # Wrapper gọi GHN API
│   ├── schemas.py      # Pydantic models (validate request)
│   └── config.py       # Đọc cấu hình từ .env
├── run.py
├── requirements.txt
└── .env.example
```

## Bước 1 – Chuẩn bị môi trường
```bash
python -m venv venv
venv\Scripts\activate          # Windows   (Linux/Mac: source venv/bin/activate)
pip install -r requirements.txt
```

## Bước 2 – Lấy Token & ShopId của GHN (môi trường TEST)
1. Đăng ký tại https://5sao.ghn.dev/account (tài khoản dev, miễn phí).
2. Vào **Cài đặt → Thông tin cá nhân/API** để lấy **Token**.
3. Tạo cửa hàng (shop) → lấy **ShopId**

## Bước 3 – Cấu hình
Điền `GHN_TOKEN`, `GHN_SHOP_ID`

## Bước 4 – Chạy server
```bash
python run.py
```
Mở **http://127.0.0.1:8000/docs** → Swagger UI.

## Bước 5 – Demo theo thứ tự trên Swagger UI
| # | Endpoint | Mục đích |
|---|----------|----------|
| 1 | `GET /master-data/provinces` → `/districts` → `/wards` | Lấy `district_id`, `ward_code` người nhận |
| 2 | `GET /shipping/services` | Xem gói dịch vụ khả dụng |
| 3 | `POST /shipping/fee` | Ước tính phí |
| 4 | `POST /orders` | Tạo đơn → nhận `order_code` |
| 5 | `GET /orders/{order_code}/tracking` | Theo dõi trạng thái |
| 6 | `POST /orders/{order_code}/cancel` | Huỷ đơn (nếu cần) |

Ví dụ body `POST /shipping/fee`:
```json
{ "to_district_id": 1442, "to_ward_code": "20314", "weight": 500,
  "length": 20, "width": 15, "height": 10, "insurance_value": 200000, "service_type_id": 2 }
```

## Lỗi thường gặp
| Lỗi | Nguyên nhân / cách xử lý |
|-----|--------------------------|
| 401 / "Token is invalid" | Sai Token hoặc dùng token dev cho môi trường prod (kiểm tra `GHN_ENV`) |
| "ShopId not found" | Chưa điền `GHN_SHOP_ID` đúng |
| "route not found service" | Tuyến lấy-giao không được hỗ trợ → kiểm tra `from/to district, ward_code` |
| Sai `ward_code` | `ward_code` là **chuỗi**, phải lấy từ master-data |
