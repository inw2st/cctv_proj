# 1. 시스템 패키지 업데이트
sudo apt update

# 2. 파이썬 GPIO 제어 라이브러리 설치
sudo apt install python3-gpiozero python3-pigpio -y

# 3. 순정 데비안 GStreamer 및 카메라 핵심 플러그인 설치
sudo apt install gstreamer1.0-tools gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-libcamera -y