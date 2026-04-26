# 🛒 자율주행 스마트 카트 프로젝트
**목표**: QR 인식 기반 최적 경로 주행 카트

## 🛠 하드웨어 구성
- **제어기**: Raspberry Pi 4B (4GB)
- **모터 드라이버**: TB6612FNG
- **센서**: RPLidar A1, MPU6050, USB Camera
- **컨버터**: LM2596 스텝다운 컨버터

## 📌 핀 맵 (Pin Mapping)
- 모터 A: GPIO 12 (PWM), 17, 27
- 모터 B: GPIO 13 (PWM), 22, 23

## 구조 
- smart_cart_project/ (GitHub Repository)
├── launch/                 # 여러 노드(모터+리다+QR)를 한 번에 켜는 실행 파일
│   └── cart_launch.py
├── smart_cart_project/     # 실제 파이썬 코드들이 들어가는 곳 (Package Name)
│   ├── __init__.py
│   ├── motor_node.py       # [D-7] 모터 제어 (TB6612FNG)
│   ├── qr_node.py          # [D-4] QR 코드 인식 및 메뉴 선택
│   └── path_planner.py     # [D-2] 최적 경로 계산 (TSP)
├── resource/               # ROS2 시스템용 폴더 (그대로 두기)
├── test/                   # 테스트용 폴더 (그대로 두기)
├── package.xml             # 패키지 정보 및 의존성 라이브러리 설정
├── setup.py                # 실행 명령어(Entry Point) 설정 파일 (가장 중요!)
├── setup.cfg               # 설치 설정
└── README.md               # 핀 맵 및 프로젝트 요약