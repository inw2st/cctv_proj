import time
import subprocess
from datetime import datetime
from gpiozero import DigitalInputDevice, PWMOutputDevice

# ==========================================
# 1. 하드웨어 핀 설정 (행그리님 결선 기준)
# ==========================================
ir_sensor = DigitalInputDevice(14)         # 8번 핀 (적외선 행동감지 센서 Out)
buzzer = PWMOutputDevice(15, frequency=2000) # 10번 핀 (부저 시그널, 가장 소리 좋은 2000Hz 고정)


# ==========================================
# 2. 기능 함수 정의
# ==========================================
def play_warning_sound():
    """움직임 감지 시 2000Hz로 삐삐삑 경고음을 내는 함수"""
    print("🚨 [경고] 움직임 감지! 삐삐삑!!")
    for _ in range(3):
        buzzer.value = 0.5  # 부저 가동
        time.sleep(0.08)    # 0.08초 소리 출력
        buzzer.off()        # 부저 차단
        time.sleep(0.05)    # 0.05초 미세 휴식


def record_video():
    """Linux 'timeout'과 GStreamer MJPEG 명세를 매칭하여 유실 없는 5초 녹화를 수행하는 함수"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"cctv_{timestamp}.avi"
    
    print(f"📹 [녹화 시작] 쉘 직통 모드로 5초간 영상을 녹화합니다 -> 파일명: {filename}")
    
    # timeout -s INT 5를 통해 정확히 5초 후 Ctrl+C 인터럽트 효과를 주어 파일 정리를 마무리지음
    cmd = f"timeout -s INT 5 gst-launch-1.0 -e libcamerasrc ! video/x-raw,width=640,height=480,framerate=15/1 ! videoconvert ! jpegenc ! avimux ! filesink location={filename}"
    
    try:
        # shell=True 방식으로 실행하여 리눅스 bash가 파이프라인 기호(!)를 정상적으로 처리하게 유도
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        # 정상적인 타임아웃 종료 코드(124) 또는 인라인 정상 종료(0, 130) 검증
        if result.returncode not in [0, 124, 130, -2]:
            print(f"❌ GStreamer 파이프라인 가동 실패 (Return Code: {result.returncode})")
            print(f"📋 상세 에러 내용:\n{result.stderr}")
        else:
            print(f"💾 [녹화 완료] 영상 파일이 디렉토리에 확실하게 저장되었습니다.\n")
            
    except Exception as e:
        print(f"❌ 시스템 내부 스크립트 오류 발생: {e}\n")


# ==========================================
# 3. 메인 감지 시스템 루프
# ==========================================
print("=" * 60)
print("  🛡️ 순정 데비안 가속 안정형 CCTV 보안 시스템 가동")
print("  (프로그램을 종료하려면 터미널에서 Ctrl+C를 누르세요)")
print("=" * 60)

try:
    while True:
        if ir_sensor.value == 1:
            play_warning_sound()  # 1. 2000Hz 경고음 발생
            record_video()        # 2. 쉘 직통 마스터 파이프라인 가동 (5초 녹화 블로킹)
            time.sleep(2)         # 연속 감지 꼬임 방지를 위한 안전 버퍼 타임
        else:
            buzzer.off()          # 평시 부저 차단 상태 유지
            time.sleep(0.1)       # CPU 점유율 과부하 방지 전용 미세 휴식

except KeyboardInterrupt:
    buzzer.off()
    print("\n🛡️ 보안 시스템이 안전하게 종료되었습니다.")
