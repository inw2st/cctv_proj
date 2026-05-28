from gpiozero import DigitalInputDevice, PWMOutputDevice
import time
import subprocess
from datetime import datetime

# ==========================================
# 1. 하드웨어 핀 설정
# ==========================================
ir_sensor = DigitalInputDevice(14, pull_up=False)
buzzer = PWMOutputDevice(15, frequency=2000)

# ==========================================
# 2. 설정값
# ==========================================
COOLDOWN = 5  # 감지 후 재감지 무시 시간 (초)
last_detected = 0


# ==========================================
# 3. 기능 함수
# ==========================================
def play_warning_sound():
   print("🚨 [경고] 움직임 감지! 삐삐삑!")
   for _ in range(3):
       buzzer.value = 0.5
       time.sleep(0.08)
       buzzer.off()
       time.sleep(0.05)


def record_video():
   timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
   filename = f"cctv_{timestamp}.h264"

   print(f"📹 [녹화 시작] 5초간 녹화 -> {filename}")

   cmd = f"rpicam-vid -t 5000 -o {filename}"

   try:
       result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
       if result.returncode == 0:
           print(f"💾 [녹화 완료] {filename}\n")
       else:
           print(f"❌ 녹화 실패:\n{result.stderr}\n")
   except Exception as e:
       print(f"❌ 오류: {e}\n")


# ==========================================
# 4. 메인 루프
# ==========================================
print("=" * 50)
print("  🛡️ CCTV 보안 시스템 가동")
print("  종료하려면 Ctrl+C")
print("=" * 50)

try:
   while True:
       if ir_sensor.value == 1:
           now = time.time()
           if now - last_detected > COOLDOWN:
               last_detected = now
               play_warning_sound()
               record_video()
       else:
           buzzer.off()
       time.sleep(0.1)

except KeyboardInterrupt:
   buzzer.off()
   print("\n🛡️ 시스템이 안전하게 종료되었습니다.")
