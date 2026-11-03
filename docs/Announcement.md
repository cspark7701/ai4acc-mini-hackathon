# 📢 공지사항: 가속기 분야 AI 활용 튜토리얼 & 미니 해커톤
# Announcement: AI Applications in Accelerators Tutorial & Mini-Hackathon

---

# [한국어 공지사항]

## 🌟 행사 개요

**가속기 분야 AI 활용 튜토리얼 & 미니 해커톤**에 참가하시는 모든 연구원, 엔지니어, 대학원생 여러분을 진심으로 환영합니다!

본 행사는 최신 인공지능(AI) 및 머신러닝(ML) 기법을 입자 가속기 물리 모델링, 폐루프 빔 궤도 제어, 그리고 에이전틱 자율 운전 워크플로우에 접목하는 이론적 기초와 실습 역량을 집중적으로 함양하는 1일 집중 튜토리얼 및 챌린지입니다.

- **행사 일시:** 2026년 11월 3일 (화) 09:00 – 17:00
- **행사 장소:** KOMAC / KAERI (한국원자력연구원 양성자과학연구단)
- **주요 대상:** 가속기 물리 및 제어 분야 연구원, 박사후연구원, 대학원생 및 도메인 엔지니어
- **강사진:**
  - **박종식 박사 (Chong Shik Park, Ph.D.)** — 고려대학교 세종캠퍼스 (Korea University, Sejong)
  - **Thorsten Hellert 박사 (Thorsten Hellert, Ph.D.)** — 로렌스 버클리 국립연구소 (LBNL) / Osprey 연구팀

---

## 🕒 프로그램 일정표 (Master Schedule)

| 시간 | 세션 구분 | 세부 내용 및 강사 |
| :---: | :---: | :--- |
| **09:00 – 09:10** | 개회 및 오리엔테이션 | 워크숍 목표 소개, 실습 환경 점검 및 W&B 챌린지 안내 |
| **09:10 – 10:30** | **강의 1** | **입자 가속기를 위한 AI/ML 기초 및 폐루프 제어**<br>*(AI/ML Foundations and Closed-Loop Control for Particle Accelerators)*<br>강사: 박종식 박사 (고려대학교 세종캠퍼스) |
| **10:30 – 10:40** | 휴식 및 질의응답 | 세션 간 휴식 및 1차 Q&A |
| **10:40 – 12:00** | **강의 2** | **가속기 연구를 위한 에이전틱 AI: Osprey 프레임워크 응용**<br>*(Agentic AI for Accelerator Research: Osprey Applications)*<br>강사: Thorsten Hellert 박사 |
| **12:00 – 13:30** | 점심 식사 및 네트워킹 | 식사 및 참가자 간 교류 |
| **13:30 – 16:30** | **미니 해커톤 실습** | **빔 궤도 정렬 벤치마크 챌린지 (Beam Orbit Alignment Benchmark)**<br>• 트랙 1: 신경망 대리모델(MLP) 기반 역문제 최적화 제어<br>• 트랙 2: 물리 기반 사전지식(ORM) 결합 강화학습(RL) 제어<br>• 트랙 3: 가우시안 프로세스 기반 베이지안 최적화(BO) 제어 |
| **16:30 – 17:00** | 시상 및 총평 | Weights & Biases 실시간 리더보드 결과 확인, 우수 참가자 시상 및 폐회 |

---

## 💻 참가자 필수 준비 사항 (Participant Preparation)

원활하고 유익한 실습 진행을 위해 참가자 여러분께서는 행사 당일 전 아래 사항을 확인해 주시기 바랍니다.

### 1. 개인 노트북 지참 (BYOD — Bring Your Own Device)
- 실습 및 오후 미니 해커톤 참가를 위해 **개인 노트북과 충전 어댑터**를 필히 지참해 주시기 바랍니다.
- 현장 와이파이(Wi-Fi) 무선 인터넷이 제공됩니다.

### 2. 운영체제 플랫폼 안내 (Windows, Mac, Linux 모두 환영)
- **Windows, macOS, Linux** 등 참가자분께서 평소 사용하시는 어떠한 운영체제(OS) 환경이든 환영합니다.
- 본 튜토리얼의 모든 실습 코드는 브라우저 기반의 **Google Colab (별도 로컬 설치 불필요, 권장)** 환경에 완벽히 최적화되어 있습니다.
- 로컬 환경이나 Docker 환경에서 직접 구동을 원하시는 경우에도 모두 원활하게 동작하도록 패키징되어 있습니다.

### 3. Weights & Biases (W&B) 무료 계정 사전 생성
- 본 해커톤은 머신러닝 실험 추적 및 라이브 리더보드 플랫폼인 **Weights & Biases (W&B)**를 활용합니다.
- 행사 전 [wandb.ai](https://wandb.ai) (또는 [wandb.ai/site/ko](https://wandb.ai/site/ko))에서 **무료 개인 계정**을 미리 가입해 주시기 바랍니다.
- 가입 후 [wandb.ai/authorize](https://wandb.ai/authorize)에서 발급되는 본인의 API 키를 메모해 오시면, 행사 당일 단 한 줄의 코드로 자신의 제어 알고리즘 결과를 라이브 리더보드에 등록하실 수 있습니다. *(오프라인 및 익명 모드도 지원하므로 미가입자도 벤치마크 실행 자체는 가능합니다.)*

---

## ✅ 참가 전 체크리스트 (Readiness Checklist)

- [ ] 개인 노트북 및 전원 어댑터 준비 완료
- [ ] 구글 계정(Google Colab 접속용) 로그인 가능 확인
- [ ] [wandb.ai](https://wandb.ai) 무료 계정 생성 및 API 키 확인
- [ ] (선택 사항) 로컬 파이썬(3.10+) 또는 Docker Desktop 사전 설치 (로컬 실행 희망자)

---
<div style="page-break-after: always;"></div>

# [English Announcement]

## 🌟 Event Overview

We cordially invite researchers, engineers, postdoctoral scholars, and graduate students to the **AI Applications in Accelerators Tutorial & Mini-Hackathon**!

This intensive, full-day educational workshop and competition bridges cutting-edge Artificial Intelligence (AI) and Machine Learning (ML) techniques with physical beam dynamics, closed-loop accelerator orbit correction, and agentic autonomous operational workflows.

- **Date & Time:** Tuesday, November 3, 2026 | 09:00 – 17:00 KST
- **Location:** KOMAC / KAERI (Korea Multi-purpose Accelerator Complex / Korea Atomic Energy Research Institute)
- **Target Audience:** Graduate students, postdocs, accelerator physicists, and domain control engineers
- **Distinguished Instructors:**
  - **Chong Shik Park, Ph.D.** — Korea University, Sejong
  - **Thorsten Hellert, Ph.D.** — Lawrence Berkeley National Laboratory (LBNL) / Osprey Project Team

---

## 🕒 Master Program Schedule

| Time (KST) | Session Type | Details & Lecturers |
| :---: | :---: | :--- |
| **09:00 – 09:10** | Welcome & Orientation | Opening remarks, workshop objectives, setup verification & W&B intro |
| **09:10 – 10:30** | **Lecture 1** | **AI/ML Foundations and Closed-Loop Control for Particle Accelerators**<br>Lecturer: Chong Shik Park, Ph.D. (Korea University, Sejong) |
| **10:30 – 10:40** | Break & Discussion | Intermission and Q&A |
| **10:40 – 12:00** | **Lecture 2** | **Agentic AI for Accelerator Research: Osprey Applications**<br>Lecturer: Thorsten Hellert, Ph.D. |
| **12:00 – 13:30** | Lunch & Networking | Complimentary lunch and attendee collaboration |
| **13:30 – 16:30** | **Mini-Hackathon** | **Beam Orbit Alignment Benchmark Challenge**<br>• Track 1: Supervised Neural Surrogate (MLP) Inverse Optimization<br>• Track 2: Physics-Informed Closed-Loop Reinforcement Learning (RL)<br>• Track 3: Gaussian Process Bayesian Optimization (BO) Controller |
| **16:30 – 17:00** | Leaderboard Awards | W&B Live Leaderboard review, awards presentation & closing remarks |

---

## 💻 Participant Preparation & Hardware Requirements

To guarantee a seamless and productive hands-on experience, please review the following requirements prior to attending:

### 1. Bring Your Own Laptop (BYOD)
- All participants are requested to **bring their personal laptop and power adapter** for the morning tutorials and the afternoon hackathon.
- High-speed venue Wi-Fi connectivity will be provided.

### 2. Platform Flexibility (Windows, macOS, and Linux are All Welcome)
- You are welcome to use **any operating system: Windows, macOS, or Linux**.
- All interactive challenge notebooks are turnkey-ready and fully supported on **Google Colab (recommended, zero local installation required)**.
- Participants preferring local execution may also run the provided environments natively via Python 3.10+ / JupyterLab or via the included Docker container.

### 3. Create a Free Weights & Biases (W&B) Account in Advance
- The hackathon utilizes **Weights & Biases (W&B)** for real-time experiment tracking, telemetry visualization, and the live competition leaderboard.
- Please register for a **free personal account** at [wandb.ai](https://wandb.ai) prior to the tutorial.
- After signing up, obtain your API authorization key at [wandb.ai/authorize](https://wandb.ai/authorize). Having this ready allows you to link your notebook runs to the live leaderboard in seconds. *(Offline and anonymous logging modes are also supported for attendees who prefer not to create an account).*

---

## ✅ Pre-Event Readiness Checklist

- [ ] Personal laptop and power adapter ready
- [ ] Active Google account tested for Google Colab access
- [ ] Free [wandb.ai](https://wandb.ai) account created & API key retrieved from [wandb.ai/authorize](https://wandb.ai/authorize)
- [ ] (Optional) Local Python 3.10+ environment or Docker Desktop installed for participants choosing local execution

---

## 📍 Inquiries & Contact
- **Host Institution:** KOMAC / KAERI
- **Repository & Code:** [AI Applications in Accelerators Hackathon GitHub Repository](https://github.com/cspark/ai4acc-mini-hackathon)
- For technical questions regarding environment setup, refer to `docs/Technical Preparation.docx` or `docs/DOCKER_GUIDE.md`.
