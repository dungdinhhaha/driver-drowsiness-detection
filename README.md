# Hệ Thống Phát Hiện Buồn Ngủ Cho Người Lái Xe

Hệ thống sử dụng webcam để giám sát người lái xe và phát hiện dấu hiệu buồn ngủ thông qua việc theo dõi trạng thái mắt.

## Tính Năng

- Phát hiện khuôn mặt và mắt theo thời gian thực
- Tính toán tỷ lệ mắt (EAR) để xác định trạng thái mắt
- Cảnh báo khi phát hiện buồn ngủ (mắt nhắm > 1 giây)
- Hiển thị trực quan:
  - Viền xanh quanh mặt khi tỉnh táo
  - Viền đỏ và cảnh báo khi buồn ngủ
  - Hiển thị giá trị EAR
- Cảnh báo bằng âm thanh

## Yêu Cầu Hệ Thống

- Python 3.6 trở lên
- Webcam
- Các thư viện Python (xem requirements.txt)

## Cài Đặt

1. Clone repository:
```bash
git clone https://github.com/[username]/driver-drowsiness-detection.git](https://github.com/dungdinhhaha/driver-drowsiness-detection.git
cd driver-drowsiness-detection
```

2. Tạo và kích hoạt môi trường ảo:
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.\.venv\Scripts\activate   # Windows
```

3. Cài đặt các thư viện cần thiết:
```bash
pip install -r requirements.txt
```

4. Tải model dlib:
- Tải file `shape_predictor_68_face_landmarks.dat` từ [dlib.net](http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2)
- Giải nén và đặt vào thư mục `models/`

5. Thêm file âm thanh cảnh báo:
- Đặt file `alarm.wav` vào thư mục `sounds/`

## Sử Dụng

Chạy chương trình:
```bash
python drowsiness_detection.py
```

Các phím điều khiển:
- `q`: Thoát chương trình

## Điều Chỉnh Thông Số

Bạn có thể điều chỉnh độ nhạy của hệ thống bằng cách thay đổi các thông số trong file `drowsiness_detection.py`:

- `EYE_AR_THRESH`: Ngưỡng để xác định mắt nhắm (mặc định: 0.26)
  - Giảm giá trị để hệ thống ít nhạy cảm hơn
  - Tăng giá trị để hệ thống nhạy cảm hơn

- `EYE_AR_CONSEC_FRAMES`: Số khung hình liên tiếp mắt nhắm để báo động (mặc định: 30)
  - 30 khung hình ≈ 1 giây (ở 30 FPS)
  - Tăng giá trị để yêu cầu thời gian nhắm mắt dài hơn
  - Giảm giá trị để phát hiện nhanh hơn

## Cấu Trúc Dự Án

```
driver-drowsiness-detection/
├── models/
│   └── shape_predictor_68_face_landmarks.dat
├── sounds/
│   └── alarm.wav
├── drowsiness_detection.py
├── requirements.txt
└── README.md
```

## Đóng Góp

Mọi đóng góp đều được hoan nghênh! Vui lòng tạo issue hoặc pull request.

## Giấy Phép

MIT License 
