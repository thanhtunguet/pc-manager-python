# PC Manager Telegram Bot

🖥️ **Telegram bot để điều khiển máy tính cá nhân từ xa thông qua các lệnh chat**

Bot này sử dụng Google Gemini AI để hiểu ý định người dùng và thực hiện các lệnh điều khiển máy tính thông qua REST API.

## ✨ Tính năng

- 🔵 **Bật máy tính từ xa** - Gửi lệnh bật máy tính qua API
- 🔴 **Tắt máy tính từ xa** - Gửi lệnh tắt máy tính qua API  
- 📊 **Kiểm tra trạng thái máy tính** - Kiểm tra máy tính có đang hoạt động hay không
- 🤖 **Chat thông minh** - Sử dụng Google Gemini AI để hiểu ngôn ngữ tự nhiên
- 🌐 **Hỗ trợ đa ngôn ngữ** - Tiếng Việt và tiếng Anh
- 🔒 **Hỗ trợ SOCKS Proxy** - Hoạt động qua SOCKS proxy cho các khu vực hạn chế

## 📋 Yêu cầu

### Yêu cầu chung:
- Telegram Bot Token (từ [@BotFather](https://t.me/BotFather))
- Google Gemini API Key
- PC với REST API endpoint có sẵn

### Yêu cầu cho Python:
- Python 3.11+

### Yêu cầu cho Docker:
- Docker Engine 20.10+
- Docker Compose 2.0+ (khuyến nghị)

## 🚀 Cài đặt

### 1. Clone repository

```bash
git clone <repository-url>
cd pc-manager-python
```

### 2. Cài đặt dependencies (chỉ khi chạy với Python)

```bash
pip install -r requirements.txt
```

### 3. Thiết lập biến môi trường

Sao chép file `.env.example` thành `.env`:

```bash
cp .env.example .env
```

Chỉnh sửa file `.env` với thông tin của bạn:

```env
# Telegram Bot Token từ @BotFather
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here

# Google Gemini API Key
GEMINI_API_KEY=your_gemini_api_key_here

# PC API Base URL (ví dụ: http://192.168.1.100:8000)
PC_API_BASE_URL=http://your_pc_ip:port

# SOCKS Proxy Configuration (tùy chọn - để trống nếu không cần)
PROXY_HOST=your_proxy_ip
PROXY_PORT=1080
PROXY_USERNAME=your_proxy_username
PROXY_PASSWORD=your_proxy_password
```

**Lưu ý về SOCKS Proxy:**
- Nếu bạn ở các quốc gia có chặn Telegram, bạn cần cấu hình SOCKS proxy
- Để trống `PROXY_HOST` và `PROXY_PORT` nếu không cần proxy
- `PROXY_USERNAME` và `PROXY_PASSWORD` chỉ cần thiết nếu proxy yêu cầu xác thực

### 4. Chạy bot

#### Cách 1: Chạy trực tiếp với Python

```bash
python main.py
```

#### Cách 2: Chạy với Docker (Khuyến nghị)

**Sử dụng Docker Compose (dễ nhất):**

```bash
# Build và chạy container
docker-compose up -d

# Xem logs
docker-compose logs -f

# Dừng container
docker-compose down
```

**Sử dụng Docker trực tiếp:**

```bash
# Build image
docker build -t pc-manager-bot .

# Chạy container
docker run -d \
  --name pc-manager-bot \
  --env-file .env \
  --restart unless-stopped \
  pc-manager-bot

# Xem logs
docker logs -f pc-manager-bot

# Dừng container
docker stop pc-manager-bot
docker rm pc-manager-bot
```

## 📚 Hướng dẫn sử dụng

### Các lệnh bot:

- `/start` - Bắt đầu sử dụng bot
- `/help` - Hiển thị hướng dẫn sử dụng
- `/status` - Kiểm tra trạng thái máy tính

### Điều khiển máy tính:

Bot sẽ tự động nhận diện ý định của bạn khi gửi tin nhắn:

**Bật máy tính:**
- "Bật máy tính"
- "Mở máy"
- "Khởi động máy"
- "Turn on PC"
- "Start computer"

**Tắt máy tính:**
- "Tắt máy tính"
- "Shutdown"
- "Tắt nguồn"
- "Turn off PC"
- "Power off"

**Kiểm tra trạng thái:**
- "Kiểm tra máy tính"
- "Trạng thái máy"
- "PC status"
- "Check computer"

### Chat thông thường:

Bạn cũng có thể chat bình thường với bot. Bot sẽ sử dụng Google Gemini AI để trả lời các câu hỏi không liên quan đến điều khiển máy tính.

## 🔧 Cấu hình PC API

Bot yêu cầu PC của bạn có REST API với các endpoint sau:

- `POST /power-on` - Bật máy tính
- `POST /power-off` - Tắt máy tính
- `GET /is-online` - Kiểm tra trạng thái (trả về JSON với field `online: boolean`)

## 📁 Cấu trúc project

```
project/
├── bot/
│   ├── __init__.py          # Package initialization
│   ├── handlers.py          # Telegram bot handlers
│   └── gemini_client.py     # Google Gemini AI client
├── .env.example             # Environment variables template
├── .dockerignore            # Docker ignore file
├── Dockerfile               # Docker image configuration
├── docker-compose.yml       # Docker Compose configuration
├── main.py                  # Entry point
├── requirements.txt         # Python dependencies
└── README.md               # Documentation
```

## 📝 Logging

Bot sử dụng Python logging để ghi log các hoạt động:

- Thông tin khởi tạo bot
- Tin nhắn từ người dùng
- Kết quả phân tích từ Gemini AI
- Lỗi kết nối API
- Các lỗi khác

## 🛠️ Troubleshooting

### Lỗi thường gặp:

1. **Bot không khởi động được:**
   - Kiểm tra `TELEGRAM_BOT_TOKEN` có đúng không
   - Kiểm tra `GEMINI_API_KEY` có hợp lệ không

2. **Không kết nối được đến PC:**
   - Kiểm tra `PC_API_BASE_URL` có đúng không
   - Đảm bảo PC API đang chạy và có thể truy cập được
   - Kiểm tra firewall/network settings

3. **Gemini AI không hoạt động:**
   - Kiểm tra API key Gemini có hợp lệ không
   - Kiểm tra quota API còn hay không

4. **Không kết nối được Telegram (do chặn):**
   - Cấu hình SOCKS proxy trong file `.env`
   - Kiểm tra proxy server có hoạt động không
   - Thử các proxy server khác nhau
   - Kiểm tra username/password của proxy

5. **Lỗi khi chạy với Docker:**
   - Đảm bảo Docker đang chạy: `docker --version`
   - Kiểm tra file `.env` có trong thư mục project
   - Xem logs container: `docker-compose logs -f`
   - Restart container: `docker-compose restart`

### Debug mode:

Để bật debug mode, thay đổi logging level trong `main.py`:

```python
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG  # Thay đổi từ INFO thành DEBUG
)
```

## 🤝 Đóng góp

Mọi đóng góp đều được chào đón! Hãy tạo issue hoặc pull request.

## 📄 License

Dự án này sử dụng MIT License.

## 🔒 Bảo mật

- Không commit file `.env` vào git
- Giữ bí mật các API key
- Sử dụng HTTPS cho PC API khi có thể
- Hạn chế quyền truy cập Telegram bot

## 📞 Hỗ trợ

Nếu gặp vấn đề, hãy tạo issue trên GitHub hoặc liên hệ với chúng tôi.