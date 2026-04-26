import RPi.GPIO as GPIO
import time
from mpu6050 import mpu6050

# 1. 핀 번호 정의 (채린님 설정값 그대로 반영)
STBY = 22
FL_PWM, FL_IN1, FL_IN2 = 12, 16, 18
FR_PWM, FR_IN1, FR_IN2 = 33, 13, 15
RL_PWM, RL_IN1, RL_IN2 = 32, 36, 38
RR_PWM, RR_IN1, RR_IN2 = 35, 37, 40
TRIG, ECHO = 29, 31

# 2. 하드웨어 초기화 세팅
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
motor_pins = [STBY, FL_PWM, FL_IN1, FL_IN2, FR_PWM, FR_IN1, FR_IN2, 
              RL_PWM, RL_IN1, RL_IN2, RR_PWM, RR_IN1, RR_IN2, TRIG]
GPIO.setup(motor_pins, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

# PWM 초기화
pwm_fl = GPIO.PWM(FL_PWM, 50); pwm_fl.start(0)
pwm_fr = GPIO.PWM(FR_PWM, 50); pwm_fr.start(0)
pwm_rl = GPIO.PWM(RL_PWM, 50); pwm_rl.start(0)
pwm_rr = GPIO.PWM(RR_PWM, 50); pwm_rr.start(0)

# IMU 센서 초기화
sensor = mpu6050(0x68)

# 3. 기능 함수 정의 (눈과 발 역할)
def get_distance():
    """초음파 센서 디버깅 버전"""
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)
    
    start_time = time.time()
    stop_time = time.time()
    
    # 1. 신호가 나갈 때까지 대기 (최대 0.05초)
    timeout = time.time() + 0.05
    while GPIO.input(ECHO) == 0:
        if time.time() > timeout:
            return 888.0  # Trig 핀이나 전원 문제일 때 출력됨
        start_time = time.time()
    
    # 2. 신호가 돌아올 때까지 대기
    timeout = time.time() + 0.05
    while GPIO.input(ECHO) == 1:
        if time.time() > timeout:
            return 777.0  # Echo 핀이나 거리 초과일 때 출력됨
        stop_time = time.time()
        
    distance = (stop_time - start_time) * 17150
    return distance

def drive(speed, direction="forward"):
    """모터 4개를 구동합니다. 왼쪽 바퀴들의 방향을 반전시켰습니다."""
    GPIO.output(STBY, GPIO.HIGH)
    
    if direction == "forward":
        # [오른쪽 바퀴: 정방향]
        GPIO.output([FR_IN1, RR_IN1], GPIO.HIGH)
        GPIO.output([FR_IN2, RR_IN2], GPIO.LOW)
        
        # [왼쪽 바퀴: 반전 (뒤로 돌던 걸 앞으로)]
        GPIO.output([FL_IN1, RL_IN1], GPIO.LOW) # HIGH였던 걸 LOW로
        GPIO.output([FL_IN2, RL_IN2], GPIO.HIGH) # LOW였던 걸 HIGH로
        
    elif direction == "stop":
        GPIO.output([FL_IN1, FL_IN2, FR_IN1, FR_IN2, RL_IN1, RL_IN2, RR_IN1, RR_IN2], GPIO.HIGH)
        speed = 0
    
    pwm_fl.ChangeDutyCycle(speed)
    pwm_fr.ChangeDutyCycle(speed)
    pwm_rl.ChangeDutyCycle(speed)
    pwm_rr.ChangeDutyCycle(speed)
# 4. 통합 실행 루프 (여기가 핵심!)
try:
    print("통합 제어 시스템 시작... 장애물이 20cm 안에 오면 멈춥니다.")
    while True:
        # [인지] 센서 데이터 읽기
        dist = get_distance()
        imu_data = sensor.get_accel_data() # 필요 시 활용
        
        # [판단 및 제어]
        if dist < 20: 
            drive(0, "stop")
            print(f"!!! 정지 !!! (장애물 거리: {dist:.1f} cm)")
        else:
            drive(40, "forward") # 40% 속도로 전진
            print(f"전진 중... (거리: {dist:.1f} cm, IMU Z: {imu_data['z']:.2f})")
            
        time.sleep(0.1) # 루프 주기 조절

except KeyboardInterrupt:
    print("\n사용자가 종료함")
finally:
    drive(0, "stop")
    GPIO.cleanup()
