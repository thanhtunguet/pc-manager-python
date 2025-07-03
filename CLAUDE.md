Bạn là lập trình viên Python backend giỏi. Hãy viết một project Telegram bot hoàn chỉnh với yêu cầu như sau:

---

## 📌 Mô tả project:

Viết một **Telegram bot** điều khiển máy tính cá nhân từ xa thông qua các lệnh chat.
Máy tính cá nhân có sẵn REST API:

* `POST /power-on`
* `POST /power-off`
* `GET /is-online`

Bot sẽ:

* Nhận message người dùng qua Telegram.
* Gửi nội dung message đó đến **Google Gemini API với function calling** để phân tích ý định người dùng.
* Gemini sẽ trả về:

  * Tên hàm (function name) tương ứng với intent: `turn_on_pc`, `turn_off_pc`, `check_pc_status`
  * Nếu không có intent, trả lời tự nhiên bằng Gemini.

Bot xử lý:

* Nếu nhận được `turn_on_pc` → gọi `POST /power-on`
* Nếu `turn_off_pc` → gọi `POST /power-off`
* Nếu `check_pc_status` → gọi `GET /is-online`
* Nếu không phải 3 intent trên → trả lời lại user bằng Gemini natural response.

---

## 📌 Công nghệ yêu cầu:

* Python 3.11+
* `python-telegram-bot`
* `google-generativeai`
* `requests`
* `dotenv`

---

## 📌 Cấu trúc project:

```
project/
├── bot/
│   ├── __init__.py
│   ├── handlers.py
│   └── gemini_client.py
├── .env.example
├── main.py
├── requirements.txt
└── README.md
```

---

## 📌 Yêu cầu chi tiết:

### 1️⃣ Biến môi trường `.env`

* `TELEGRAM_BOT_TOKEN`
* `GEMINI_API_KEY`
* `PC_API_BASE_URL`

---

### 2️⃣ Gemini function definitions:

Khai báo 3 function cho Gemini:

```json
[
  {
    "name": "turn_on_pc",
    "description": "Bật máy tính cá nhân."
  },
  {
    "name": "turn_off_pc",
    "description": "Tắt máy tính cá nhân."
  },
  {
    "name": "check_pc_status",
    "description": "Kiểm tra trạng thái máy tính (online/offline)."
  }
]
```

---

### 3️⃣ Xử lý logic:

* Nhận message Telegram.
* Gửi đến Gemini kèm function definitions.
* Nếu Gemini trả về function call → xử lý API tương ứng.
* Nếu không → trả lời tự nhiên.

---

### 4️⃣ Yêu cầu code:

* Code rõ ràng, clean Pythonic.
* Có logging.
* Có exception handling.
* README hướng dẫn cài đặt.

---

## 📌 Output:

* **Project hoàn chỉnh** với đầy đủ code từng file.
* Nêu rõ cấu trúc từng file.
* Viết README.md.
* Viết requirements.txt.

---

Hãy viết **full code** từng file, đúng cấu trúc đã yêu cầu, với comment đầy đủ.
