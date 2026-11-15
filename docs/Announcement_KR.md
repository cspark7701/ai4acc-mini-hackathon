# 📢 가속기 AI 튜토리얼 세션 & 미니 해커톤

**AI Tutorial Session for Accelerators & Mini-Hackathon**

---

## 🌟 개요

**가속기 AI 튜토리얼 세션 & 미니 해커톤**에 참가하시는 모든 연구원, 엔지니어, 대학원생 여러분을 진심으로 환영합니다!

본 행사는 최신 인공지능(AI) 및 머신러닝(ML) 기법을 입자 가속기 물리 모델링, 폐루프 빔 궤도 제어, 그리고 에이전틱 자율 운전 워크플로우에 접목하는 이론적 기초와 실습 역량을 집중적으로 함양하는 1일 집중 튜토리얼 및 챌린지입니다.

- **일시:** 2026년 11월 19일 (목) 09:00 – 17:00
- **장소:** KOMAC / KAERI (한국원자력연구원 양성자과학연구단)
- **참가 등록 (Indico):** [https://indico.korea.ac.kr/event/114/](https://indico.korea.ac.kr/event/114/)
- **주요 대상:** 가속기 물리 및 제어 박사후연구원, 대학원생 및 학부생
- **강사진:**
  - **박종식 박사 (Chong Shik Park, Ph.D.)** — 고려대학교 세종캠퍼스 (Korea University, Sejong)
  - **Thorsten Hellert 박사 (Thorsten Hellert, Ph.D.)** — 로렌스 버클리 국립연구소 (LBNL) / Osprey 연구팀

---

## 🕒 프로그램 일정표 (Master Schedule)

| 시간                | 세션 구분         | 세부 내용 및 강사                                                                                                                                                                     |
|:-----------------:|:-------------:|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **09:00 – 09:10** | 개회 및 오리엔테이션   | 워크숍 목표 소개, 실습 환경 점검 및 W&B 챌린지 안내                                                                                                                                               |
| **09:10 – 10:30** | **강의 1**      | **입자 가속기를 위한 AI/ML 기초 및 폐루프 제어**<br>*(AI/ML Foundations and Closed-Loop Control for Particle Accelerators)*<br>강사: 박종식 박사 (고려대학교 세종캠퍼스)                                        |
| **10:30 – 10:40** | 휴식 및 질의응답     | 세션 간 휴식 및 1차 Q&A                                                                                                                                                               |
| **10:40 – 12:00** | **강의 2**      | **가속기 연구를 위한 에이전틱 AI: Osprey 프레임워크 응용**<br>*(Agentic AI for Accelerator Research: Osprey Applications)*<br>강사: Thorsten Hellert 박사                                             |
| **12:00 – 13:30** | 점심 식사 및 네트워킹  | 식사 및 참가자 간 교류                                                                                                                                                                  |
| **13:30 – 16:30** | **미니 해커톤 실습** | **빔 궤도 정렬 벤치마크 챌린지 (Beam Orbit Alignment Benchmark)**<br>• 트랙 1: 신경망 대리모델(MLP) 기반 역문제 최적화 제어<br>• 트랙 2: 물리 기반 사전지식(ORM) 결합 강화학습(RL) 제어<br>• 트랙 3: 가우시안 프로세스 기반 베이지안 최적화(BO) 제어 |
| **16:30 – 17:00** | 시상 및 총평       | Weights & Biases 실시간 리더보드 결과 확인, 우수 참가자 시상 및 폐회                                                                                                                                |

---

## 💻 참가자 필수 준비 사항 (Participant Preparation)

원활하고 유익한 실습 진행을 위해 참가자 여러분께서는 워크숍 참가 전 아래 사항을 확인해 주시기 바랍니다.

### 1. 개인 노트북 지참 (BYOD — Bring Your Own Device)

- 실습 및 오후 미니 해커톤 참가를 위해 **개인 노트북과 충전 어댑터**를 필히 지참해 주시기 바랍니다.
- 현장 와이파이(Wi-Fi) 무선 인터넷이 제공됩니다.

### 2. 운영체제 및 Docker Desktop 사전 설치 안내 (Windows / Mac / Linux)

- **Windows, macOS, Linux** 등 참가자분께서 평소 사용하시는 어떠한 운영체제(OS) 환경이든 모두 지원합니다.
- 본 실습에서는 의존성 충돌 없는 원활한 환경 구동을 위해 Docker를 활용합니다. 참가자 여러분께서는 아래 안내에 따라 사전에 환경을 준비해 주시기 바랍니다.

#### 🪟 Windows 사용자 (Docker Desktop + WSL 2 활성화):

1. [Docker Desktop 공식 웹사이트](https://www.docker.com/products/docker-desktop/)에서 Windows용 설치 프로그램을 다운로드하여 설치합니다.
2. **WSL 2 (Windows Subsystem for Linux) 활성화:**
   - 관리자 권한으로 PowerShell 또는 명령 프롬프트(CMD)를 실행한 후 다음 명령어를 입력합니다:
     
     ```powershell
     wsl --install
     ```
     
     *(이미 WSL이 설치된 경우 `wsl --update` 실행)*
   - Docker Desktop 설정(Settings $\rightarrow$ General)에서 **"Use the WSL 2 based engine"** 옵션이 체크되어 있는지 확인합니다.
3. 시스템 재부팅 요청이 있을 경우 재부팅 후 Docker Desktop 앱을 실행해 둡니다.

#### 🍎 Mac (macOS) 사용자:

1. [Docker Desktop 공식 웹사이트](https://www.docker.com/products/docker-desktop/)에서 본인의 Mac 칩 사양(Apple Silicon M1/M2/M3/M4 또는 Intel 칩)에 맞는 버전을 다운로드하여 설치합니다.
2. 설치 후 Docker Desktop 앱을 실행하여 초기 권한 및 백그라운드 서비스 등록을 완료합니다.

#### 🐧 Linux 사용자 (Ubuntu/Debian 및 CentOS/RHEL):

- 별도의 GUI 앱 없이 터미널에서 패키지 관리자를 통해 Docker 엔진과 Docker Compose 플러그인을 설치합니다:
  - **Ubuntu / Debian:**
    
    ```bash
    sudo apt update && sudo apt install -y docker.io docker-compose-plugin
    sudo systemctl enable --now docker
    sudo usermod -aG docker $USER
    ```
  - **CentOS / RHEL (Red Hat Enterprise Linux) / Rocky Linux:**
    
    ```bash
    sudo dnf install -y yum-utils
    sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
    sudo dnf install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
    sudo systemctl enable --now docker
    sudo usermod -aG docker $USER
    ```
    
    *(참고: docker 그룹 추가 후 변경사항 적용을 위해 터미널 재로그인이 필요합니다.)*

- **공식 해커톤 Docker 컨테이너 실행:**
  - **Windows 간편 실행:** 배포된 `run_hackathon_windows.bat` 파일을 **더블 클릭**하면 자동으로 Docker 엔진 상태를 점검하고 컨테이너를 실행합니다.
  - **macOS / Linux 간편 실행:** 터미널에서 `./run_hackathon_mac_linux.sh` 실행 (또는 더블 클릭).
  - **직접 터미널 명령어 입력:**
    ```bash
    docker run -it --rm -p 127.0.0.1:8888:8888 cspark7701/ai4acc-hackathon-2026:latest
    ```
  *(어떤 터미널에서든 위 단 한 줄의 명령어를 실행하거나 배치 파일을 더블 클릭한 후, 웹 브라우저에서 `http://localhost:8888`로 접속하시면 즉시 실습을 시작하실 수 있습니다.)*

### 3. Weights & Biases (W&B) 라이브 리더보드 (계정 생성 불필요)

- 본 미니 해커톤은 머신러닝 실험 추적 및 라이브 리더보드 플랫폼인 **Weights & Biases (W&B)**를 활용합니다.
- **W&B 계정 가입이나 API 키 발급은 필요하지 않습니다.** 당일 배포되는 실행 파일(`run_hackathon_windows.bat` / `run_hackathon_mac_linux.sh`)이 함께 제공되는 워크숍 공용 키 파일(`wandb.apikey`)을 컨테이너에 자동으로 전달하므로, 벤치마크 결과가 리더보드에 바로 등록됩니다.
- `wandb.apikey` 파일은 실행 파일과 **같은 폴더**에 그대로 두시고, 워크숍 외부로 공유하지 말아 주시기 바랍니다.
- 각 팀은 당일 **고유한 팀 이름**을 정해 노트북의 `TEAM_NAME`에 입력합니다. 리더보드는 행사장 화면을 통해 실시간으로 확인하실 수 있습니다. *(네트워크가 없는 경우에도 벤치마크 실행 및 로컬 점수 확인은 가능합니다.)*

---

## ✅ 참가 전 체크리스트 (Readiness Checklist)

- [ ] Indico 워크숍 사전 참가 등록 완료 ([https://indico.korea.ac.kr/event/114/](https://indico.korea.ac.kr/event/114/))
- [ ] 개인 노트북 및 전원 어댑터 준비 완료
- [ ] Docker Desktop 설치 및 실행 확인 (Windows: WSL 2 활성화 확인, macOS: 앱 실행 확인) 또는 Linux Docker Engine 준비 완료
- [ ] 해커톤 팀 이름 구상 (W&B 계정 가입은 필요하지 않습니다)
