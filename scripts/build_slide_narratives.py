#!/usr/bin/env python3
"""Build script for Lecture 1 Slide Narratives (English & Korean).

Generates:
  - presentations/Lecture_1_Slide_Narratives_EN.tex -> presentations/Lecture_1_Slide_Narratives_EN.pdf
  - presentations/Lecture_1_Slide_Narratives_KR.tex -> presentations/Lecture_1_Slide_Narratives_KR.pdf

Author: Chong Shik Park, Ph.D. (Korea University, Sejong)
Date: November 19, 2026
"""

import sys
import subprocess
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PRESENTATIONS_DIR = ROOT / "presentations"

# Slide Data Dictionary (1 to 35)
SLIDES = [
    {
        "num": 1,
        "category": "Title Slide",
        "title_en": "AI/ML Foundations & Closed-Loop Control",
        "title_kr": "가속기 인공지능/머신러닝 기초 및 폐루프 궤도 제어",
        "visual_en": "Title banner with Korea University logo, course title, lecturer credentials (Dr. Chong Shik Park), and hackathon theme.",
        "visual_kr": "고려대학교 로고, 강좌 제목, 연사 정보(박종식 교수), 해커톤 주제가 포함된 타이틀 슬라이드.",
        "script_en": (
            "Good morning, everyone, and welcome to Lecture 1 of our AI Applications in Accelerators Tutorial and Mini-Hackathon. "
            "My name is Chong Shik Park from Korea University, Sejong. Over the next eighty minutes, we will bridge the gap between "
            "classical accelerator beam physics and modern artificial intelligence. We will start from first principles—transverse "
            "beam dynamics, Hill's equation, and orbit response matrices—and progress systematically to cutting-edge closed-loop control: "
            "neural surrogate digital twins, reinforcement learning policies with physics priors, and Bayesian optimization. "
            "Our primary objective today is not just theoretical understanding, but empowering every one of you to design, train, "
            "and benchmark autonomous controllers during this afternoon's mini-hackathon."
        ),
        "script_kr": (
            "안녕하십니까, 참가자 여러분. 가속기 인공지능 응용 튜토리얼 및 미니 해커톤의 첫 번째 강의에 오신 것을 환영합니다. "
            "저는 고려대학교 세종캠퍼스 가속기과학과의 박종식입니다. 오늘 첫 번째 강의에서는 고전 가속기 빔 물리와 현대 인공지능 기법을 "
            "체계적으로 연결하고자 합니다. 횡방향 빔 동역학, 힐 방정식(Hill's equation), 궤도 응답 행렬(ORM)과 같은 기본 물리 원리에서 "
            "출발하여, 신경망 기반 디지털 트윈 대리 모델(surrogate model), 물리 사전 지식 기반 강화학습(RL), 그리고 베이지안 최적화(BO)에 "
            "이르는 폐루프 제어 기법을 심도 있게 다룰 것입니다. 오늘 강의의 목표는 단순한 이론 학습을 넘어, 오후에 진행될 미니 해커톤에서 "
            "여러분 스스로 고성능 자율 제어기를 직접 설계하고 벤치마크할 수 있는 실질적인 역량을 갖추는 것입니다."
        ),
        "cues_en": "Set an inspiring, hands-on, practical tone. Emphasize that physical physics principles and AI algorithms will be treated as partners.",
        "cues_kr": "강의의 실무적·학술적 가치를 강조하고, 물리학적 기본 원리와 최신 인공지능 알고리즘이 상호 보완적으로 작동함을 밝힙니다.",
        "qa_en": "Q: Is prior deep learning experience mandatory? A: No, we build intuition from linear optics matrices up to deep networks.",
        "qa_kr": "Q: 딥러닝 사전 경험이 부족해도 해커톤 참여가 가능한가요? A: 네, 선형 전달 행렬 기초부터 단계별로 설명하므로 충분히 따라오실 수 있습니다.",
        "trans_en": "To motivate our journey, let us first examine why modern particle accelerators demand artificial intelligence.",
        "trans_kr": "본격적인 강의에 앞서, 현대 가속기 시설에서 왜 인공지능 기법이 필수적으로 요구되는지 그 배경을 살펴보겠습니다."
    },
    {
        "num": 2,
        "category": "Operational Context",
        "title_en": "Why AI in Particle Accelerators?",
        "title_kr": "현대 입자 가속기에서 왜 인공지능인가?",
        "visual_en": "Card layout detailing high-intensity beam stability challenges, sub-micron tolerances, beam loss damage risks, and human operator cognitive saturation.",
        "visual_kr": "고강도 빔 안정성 요건, 서브미크론 허용오차, 빔 손실로 인한 방사화 및 초전도 챔버 파손 위험, 운전원의 인지 한계를 정리한 개요 카드.",
        "script_en": (
            "Modern particle accelerators—whether synchrotrons, free-electron lasers, or high-intensity spallation sources—are "
            "among the most complex engineering systems ever constructed. Machines like 4th-generation light sources demand transverse "
            "beam orbit stability down to sub-micron or even nanometer levels. Simultaneously, multi-megawatt beam power means that a fractional "
            "beam loss lasting a few microseconds can puncture a vacuum chamber or quench a superconducting radio-frequency cavity, "
            "causing weeks of unscheduled downtime. Traditional linear feedback controllers assume stationary, linear responses. "
            "However, real physical accelerators depart sharply from linearity due to magnet core saturation, hysteresis, ambient thermal drift, "
            "and coupling. Human operators cannot continuously optimize hundreds of coupled parameters in real time. "
            "This is where AI becomes a necessity: it delivers fast predictive digital twins, autonomous multi-objective optimization, "
            "and millisecond anomaly interlocks."
        ),
        "script_kr": (
            "4세대 방사광가속기, 자유전자레이저(FEL), 고강도 중성자 파쇄원 등 현대 가속기는 인류가 제작한 가장 정밀하고 복잡한 장치 중 하나입니다. "
            "이러한 최첨단 시설에서는 횡방향 빔 궤도를 수백 나노미터에서 서브미크론 수준으로 일정하게 유지해야 합니다. 동시에 메가와트급 "
            "빔 에너지를 다루기 때문에, 단 수 마이크로초 동안의 미세한 빔 손실(beam loss)만으로도 진공 챔버가 손상되거나 초전도 가속관(SRF)이 "
            "퀜치(quench)되어 수억 원 이상의 운영 손실과 수주일간의 빔 정지를 초래할 수 있습니다. 기존의 비례-적분(PI) 및 선형 피드백 제어기는 "
            "가속기 시스템이 선형이고 시불변이라는 가정에 의존합니다. 하지만 실제 가속기 전자석은 자기 포화, 히스테리시스, 열적 드리프트 등 "
            "강한 비선형성을 지닙니다. 수백 개의 제어 변수를 인간 운전원이 수동으로 최적화하는 것은 한계에 도달했습니다. "
            "따라서 고속 대리 모델, 자율 다목적 최적화, 밀리초 단위 이상 진단을 수행하는 인공지능 도입이 필연적입니다."
        ),
        "cues_en": "Stress the real-world operational stakes: hardware safety, beam brightness, and the failure modes of standard linear controllers.",
        "cues_kr": "가속기 운전 현장의 실제 위험성(장비 파손, 빔 품질 저하, 빔 다운타임)을 강조하여 AI 도입의 필요성을 각인시킵니다.",
        "qa_en": "Q: Can standard PID feedback handle non-linear drift? A: Only locally near the setpoint; large excursions cause oscillation or divergence.",
        "qa_kr": "Q: 기존의 PID 제어로 비선형 드리프트를 해결할 수 없나요? A: 기준점 부근의 미세 선형 구간에서는 가능하지만, 포화나 외란 발생 시 발진하거나 수렴 속도가 급격히 저하됩니다.",
        "trans_en": "Now let us review the master roadmap for today's workshop.",
        "trans_kr": "이어서 오늘 하루 동안 진행될 튜토리얼 및 해커톤의 전체 프로그램 일정을 살펴보겠습니다."
    },
    {
        "num": 3,
        "category": "Workshop Curriculum",
        "title_en": "Master Curriculum & Program Schedule",
        "title_kr": "전체 교육과정 및 마스터 프로그램 일정",
        "visual_en": "Three-part schedule: Lecture 1 (Physics & ML Foundations), Lecture 2 (Agentic AI with Dr. Thorsten Hellert), and Afternoon Mini-Hackathon.",
        "visual_kr": "3단계 일정 카드: 제1강(기초 이론 및 제어), 제2강(Thorsten Hellert 박사의 에이전틱 AI), 오후 미니 해커톤 실습 및 실시간 리더보드.",
        "script_en": (
            "Here is our program for the day, carefully structured to move from rigorous foundations to hands-on competition. "
            "This morning, in Lecture 1, I will cover the accelerator physics principles and the machine learning foundations governing "
            "orbit control. Immediately following, Dr. Thorsten Hellert from Lawrence Berkeley National Laboratory will present Lecture 2, "
            "exploring cutting-edge Agentic AI—how LLM agents use Python API tools, orchestrate multi-physics simulations, and enforce "
            "operational guardrails. In the afternoon, starting at 1:30 PM, you will compete in the 3.5-hour Mini-Hackathon. "
            "You will deploy and tune controllers inside a realistic Gymnasium simulation environment of a 15-meter transport line, "
            "tracking your scores on our live Weights and Biases leaderboard across 30 standardized seeds."
        ),
        "script_kr": (
            "오늘 프로그램은 체계적인 이론 교육에서 시작하여 참가자 주도의 실전 해커톤으로 이어집니다. "
            "오전 제1강에서는 제가 횡방향 빔 물리와 대리 모델링, 세 가지 머신러닝 패러다임을 강의합니다. 이어지는 제2강에서는 미국 로렌스 "
            "버클리 국립연구소(LBNL)의 Thorsten Hellert 박사님께서 최신 에이전틱 AI(Agentic AI) 기술을 소개합니다. 거대언어모델(LLM)이 "
            "파이썬 API 도구를 직접 실행하며 가속기 시뮬레이션을 자율 오케스트레이션하는 기법을 배울 수 있습니다. 그리고 오후 1시 30분부터는 "
            "본격적인 미니 해커톤이 3시간 30분 동안 펼쳐집니다. 15미터 빔 전송선 시뮬레이션 환경에서 여러분만의 제어기를 튜닝하고, "
            "Weights & Biases 실시간 리더보드를 통해 30개 표준 시드에 대한 최종 점수를 경쟁하게 됩니다."
        ),
        "cues_en": "Highlight the direct connection between Lecture 1 concepts and the afternoon challenge tasks (TODO 1, 2, 3).",
        "cues_kr": "오전 강의에서 배우는 이론들이 오후 해커톤 과제(TODO 1, 2, 3)에 직접 어떻게 활용되는지 연계성을 강조합니다.",
        "qa_en": "Q: How are teams evaluated in the hackathon? A: Using a standardized 30-seed benchmark scoring formula balancing success, speed, and precision.",
        "qa_kr": "Q: 해커톤 평가는 어떻게 이루어지나요? A: 30개 표준 시드에 대해 성공 여부, 수렴 속도, 안착 정밀도를 종합한 1000점 만점 공식으로 평가합니다.",
        "trans_en": "Let us now survey the broader landscape of AI applications across modern accelerators.",
        "trans_kr": "그렇다면 가속기 과학 전반에서 인공지능은 어떠한 핵심 기둥들로 분류되어 적용되고 있는지 살펴보겠습니다."
    },
    {
        "num": 4,
        "category": "Domain Overview",
        "title_en": "AI Pillars: Surrogates & Optimization",
        "title_kr": "가속기 인공지능 핵심 분야 (1): 대리 모델 및 자율 최적화",
        "visual_en": "Two major pillars: Pillar 1 (Fast Neural Surrogate Digital Twins) and Pillar 2 (Autonomous Multi-Objective Tuning via Bayesian Optimization).",
        "visual_kr": "핵심 기둥 1: 고속 디지털 트윈 대리 모델(초고속 시뮬레이션), 핵심 기둥 2: 가우시안 프로세스 베이지안 최적화를 통한 자율 다목적 튜닝.",
        "script_en": (
            "Artificial intelligence in accelerators is typically organized into four foundational pillars. On this slide, we examine "
            "the first two. Pillar 1 is Neural Surrogate Digital Twins. Traditional particle tracking codes like ELEGANT, MAD-X, or OPAL "
            "model complete particle distributions and collective space-charge forces with high fidelity, but they require minutes to hours "
            "for a single simulation. By training deep neural networks on historical simulation or machine datasets, we construct surrogate "
            "models that predict beam parameters in sub-millisecond timescales—often faster than 0.2 milliseconds. This enables real-time "
            "model-predictive control and virtual diagnostics. Pillar 2 is Autonomous Multi-Objective Optimization. Real beam tuning requires "
            "balancing competing objectives—such as maximizing photon flux while minimizing beam emittance and halo. Bayesian optimization "
            "with Gaussian Processes models epistemic uncertainty, allowing algorithms to find Pareto-optimal operating points in dozens "
            "of machine shots rather than thousands of blind steps."
        ),
        "script_kr": (
            "가속기 인공지능 응용은 크게 네 가지 기둥으로 나뉩니다. 이 슬라이드에서는 첫 번째와 두 번째 기둥을 살펴봅니다. "
            "첫 번째 기둥은 '신경망 대리 모델(Digital Twin Surrogates)'입니다. ELEGANT나 MAD-X 같은 정밀 수치 시뮬레이션 코드는 "
            "공간전하 효과와 집단 현상을 정확히 모사하지만, 1회 계산에 수 분에서 수 시간이 소요됩니다. 딥러닝 대리 모델은 이러한 비선형 "
            "동역학을 사전에 학습하여 0.2 밀리초 이하의 초고속으로 결과를 예측합니다. 이를 통해 실시간 모델 예측 제어(MPC)가 가능해집니다. "
            "두 번째 기둥은 '자율 다목적 최적화(Autonomous Multi-Objective Optimization)'입니다. 가속기 운전 시 빔 에미턴스 최소화와 "
            "빔 투과율 최대화는 종종 상충(trade-off) 관계에 놓입니다. 가우시안 프로세스(GP) 기반 베이지안 최적화는 불확실성을 모델링하여 "
            "수천 번의 무작위 스캔 대신 수십 회의 최소 빔 측정만으로 최적의 파레토 프론트(Pareto front)를 찾아냅니다."
        ),
        "cues_en": "Contrast the execution speed of physical tracking codes (minutes/hours) against neural surrogates (< 0.2 ms).",
        "cues_kr": "정밀 시뮬레이션 코드의 느린 계산 시간과 딥러닝 대리 모델의 밀리초 이하 추론 속도를 명확히 대조합니다.",
        "qa_en": "Q: Can neural surrogates extrapolate outside their training range? A: Pure MLPs fail to extrapolate; physics-informed architectures or regularization are required.",
        "qa_kr": "Q: 대리 모델이 학습 범위를 벗어난 영역에서도 정확한가요? A: 순수 MLP는 외삽 능력이 떨어지므로, 물리 사전 지식이나 적절한 규제 기법이 필수적입니다.",
        "trans_en": "Now let us examine the remaining two pillars: anomaly detection and autonomous scientific agents.",
        "trans_kr": "이어서 가속기 AI의 세 번째와 네 번째 기둥인 이상 진단 및 에이전틱 AI를 살펴보겠습니다."
    },
    {
        "num": 5,
        "category": "Domain Overview",
        "title_en": "AI Pillars: Diagnostics, Protection & Agents",
        "title_kr": "가속기 인공지능 핵심 분야 (2): 진단, 장비 보호 및 자율 에이전트",
        "visual_en": "Pillar 3 (Anomaly Detection, Fault Prediction & Virtual Diagnostics) and Pillar 4 (Agentic AI & Scientific LLM Assistants).",
        "visual_kr": "핵심 기둥 3: 이상 감지, 고장 예측 인터록 및 가상 진단, 핵심 기둥 4: LLM 기반 에이전틱 AI 및 자율 시뮬레이션 오케스트레이션.",
        "script_en": (
            "Pillar 3 encompasses Diagnostics, Anomaly Detection, and Machine Protection. Modern facilities deploy unsupervised "
            "autoencoders and recurrent networks to monitor thousands of telemetry streams simultaneously—detecting subtle precursor thermal drifts "
            "or RF breakdown patterns milliseconds before an actual trip occurs. This allows protective interlocks to abort the beam gracefully. "
            "Furthermore, virtual diagnostics use neural networks to infer longitudinal bunch profiles or emittance non-invasively at 100 Hz, "
            "where physical intercepting screens would destroy the beam. Pillar 4 represents the frontier: Agentic AI and Autonomous Scientific Assistants. "
            "By interfacing Large Language Models with domain-specific Python execution environments and EPICS control APIs, agents can "
            "read diagnostic alarms, reason over lattice physics, formulate multi-step mitigation strategies, and safely execute orbit corrections."
        ),
        "script_kr": (
            "세 번째 기둥은 '지능형 진단, 이상 감지 및 장비 보호'입니다. 비지도 오토인코더와 순환신경망(RNN)을 활용하여 수천 개의 텔레메트리 "
            "신호를 실시간 감시함으로써, RF 브레이크다운이나 초전도 공동의 퀜치 징후를 수 밀리초 전에 사전 감지하여 장비를 선제적으로 보호합니다. "
            "또한 빔을 파괴하는 와이어 스캐너 대신, 비파괴 센서 데이터로부터 종방향 빔 프로파일을 실시간 복원하는 '가상 진단(virtual diagnostics)'도 "
            "활발히 적용되고 있습니다. 네 번째 기둥은 '에이전틱 AI(Agentic AI)'입니다. 거대언어모델(LLM)이 파이썬 제어 스크립트와 가속기 EPICS "
            "네트워크에 직접 연동되어, 운전원의 자연어 명령을 해석하고 다단계 제어 작업을 자율적으로 기획 및 안전하게 수행하는 차세대 기술입니다."
        ),
        "cues_en": "Mention Thorsten Hellert's upcoming Lecture 2 as the deep dive into Pillar 4.",
        "cues_kr": "네 번째 기둥인 에이전틱 AI는 제2강에서 Thorsten Hellert 박사가 구체적인 실무 사례와 함께 집중적으로 다룰 것임을 안내합니다.",
        "qa_en": "Q: What is a virtual diagnostic? A: An ML model that predicts hard-to-measure destructive beam metrics from easy, non-destructive upstream sensors.",
        "qa_kr": "Q: 가상 진단이란 무엇인가요? A: 빔을 차단해야만 측정할 수 있는 물리량을, 비파괴 센서 측정값으로부터 머신러닝으로 실시간 추론해내는 기술입니다.",
        "trans_en": "With this landscape established, let us dive into the core physics of transverse beam dynamics.",
        "trans_kr": "이제 가속기 인공지능의 물리적 토대가 되는 횡방향 빔 동역학의 지배 방정식으로 들어가 보겠습니다."
    },
    {
        "num": 6,
        "category": "Physics Foundations",
        "title_en": "Hill's Equation & Transverse Motion",
        "title_kr": "힐 방정식(Hill's Equation)과 횡방향 입자 운동",
        "visual_en": "Lorentz force equation, linear magnetic expansion, quadrupole focusing gradient K(s), and Hill's differential equation.",
        "visual_kr": "로렌츠 힘 방정식, 2극/4극 자장 선형 전개, 집속 구배 K(s), 주기적 복원력을 나타내는 힐의 2계 선형 미분방정식.",
        "script_en": (
            "Transverse beam dynamics begins with the Lorentz force: d p / d t = q ( E + v cross B ). In high-energy particle accelerators, "
            "magnetic deflection dominates electric deflection by a factor of the speed of light c, so magnetic fields are universally used "
            "for steering and focusing. Expanding the vertical magnetic field B_y around the design orbit yields a dipole field B_0, a quadrupole "
            "gradient G = d B_y / d x, and higher-order multipoles. Normalizing the quadrupole gradient by the beam magnetic rigidity B-rho defines "
            "the focusing function K(s) = q G / p. Applying Newton's second law in curvilinear coordinates yields Hill's equation: "
            "x double-prime of s plus K(s) x of s equals zero. Hill's equation is structurally identical to a harmonic oscillator, but with a crucial "
            "difference: the spring constant K(s) is position-dependent and periodic along the beamline."
        ),
        "script_kr": (
            "횡방향 입자 운동은 로렌츠 힘 방정식에서 시작됩니다: d p / d t = q ( E + v × B ). 상대론적 속도를 갖는 고에너지 빔에서는 "
            "자기장에 의한 편향력이 전기장보다 광속 c배만큼 강력하므로, 빔의 궤도 수정과 집속에는 전자석이 주로 사용됩니다. "
            "설계 궤도 부근에서 수직 자장 B_y를 테일러 전개하면 2극 자장 B_0, 4극 자장 구배 G = ∂B_y/∂x, 그리고 6극 이상의 고차 다극 자장이 나타납니다. "
            "자장 구배 G를 빔의 자기 강도(magnetic rigidity) B-rho로 정규화하면 집속 함수 K(s) = q G / p가 정의됩니다. "
            "곡선 좌표계에서 운동방정식을 정리하면 바로 가속기 물리학의 근간인 '힐 방정식(Hill's equation)': x''(s) + K(s)x(s) = 0을 얻게 됩니다. "
            "이는 용수철 상수 K(s)가 가속기 위치 s에 따라 주기적으로 변하는 조화 진동자(harmonic oscillator) 방정식과 수학적으로 완전히 동일합니다."
        ),
        "cues_en": "Emphasize the physical intuition: K(s) > 0 focuses horizontally, K(s) < 0 defocuses horizontally. Earnestine betatron oscillation.",
        "cues_kr": "K(s) > 0이면 수평 집속(QF), K(s) < 0이면 수평 발산(QD)이 일어나며, 빔이 중심 궤도를 따라 주기적 진동을 수행함을 설명합니다.",
        "qa_en": "Q: Why is K position-dependent? A: Because the beam traverses distinct magnetic elements: focusing quads, defocusing quads, and field-free drifts.",
        "qa_kr": "Q: 왜 K가 위치 s의 함수인가요? A: 빔이 진행하면서 집속 전자석, 발산 전자석, 자장이 없는 드리프트 구간을 번갈아 통과하기 때문입니다.",
        "trans_en": "How do we solve Hill's equation analytically? That brings us to Courant-Snyder optics.",
        "trans_kr": "위치 종속적 복원력을 지닌 힐 방정식을 해석적으로 풀기 위해 쿠랑-스나이더(Courant-Snyder) 광학 변수를 도입합니다."
    },
    {
        "num": 7,
        "category": "Beam Optics",
        "title_en": "Betatron Motion & Courant-Snyder Optics",
        "title_kr": "베타트론 운동과 쿠랑-스나이더(Courant-Snyder) 광학",
        "visual_en": "Floquet-form solution x(s) = sqrt(epsilon * beta(s)) * cos(psi(s) + phi_0), beta function envelope, phase advance psi(s), and Courant-Snyder parameters.",
        "visual_kr": "플로케 해 x(s) = √(ε·β(s))·cos(ψ(s)+φ₀), 베타 함수 β(s), 위상 전진 ψ(s), 에미턴스 ε 및 빔 포락선(envelope) 다이어그램.",
        "script_en": (
            "Because the restoring coefficient K(s) varies with s, the solution to Hill's equation cannot be a simple sinusoid of constant amplitude. "
            "Using Floquet theory, Courant and Snyder proved in 1958 that the general trajectory is given by: "
            "x(s) = square root of epsilon times beta(s), multiplied by the cosine of psi(s) plus phi_0. "
            "Here, beta(s) is the betatron amplitude function. It acts as a local envelope modifier: where beta(s) is large, the beam breathes outward; "
            "where beta(s) is small, the beam is tightly focused. The phase advance psi(s) is the integral of 1 / beta(w) d w from 0 to s, "
            "governing how rapidly betatron phase accumulates. The quantity epsilon is the beam emittance—the invariant phase-space area "
            "enclosed by the beam ellipse. Together with alpha(s) = - 1/2 beta-prime and gamma(s) = (1 + alpha^2)/beta, these form the Twiss parameters."
        ),
        "script_kr": (
            "K(s)가 위치에 따라 변하므로, 힐 방정식의 해는 단순한 고정 진폭 사인파가 될 수 없습니다. 1958년 쿠랑과 스나이더는 플로케(Floquet) "
            "정리를 적용하여 일반해가 x(s) = √(ε·β(s))·cos(ψ(s) + φ₀)의 형태로 표현됨을 증명했습니다. "
            "여기서 β(s)는 '베타트론 진폭 함수(beta function)'로, 국소 빔 크기의 포락선(envelope)을 결정합니다. β(s)가 큰 곳에서는 빔 폭이 "
            "넓어지고, β(s)가 작은 곳에서는 빔이 강하게 집속됩니다. 위상 전진 ψ(s)는 1/β를 적분한 값으로, 입자가 진동 위상을 얼마나 빠르게 축적하는지 "
            "나타냅니다. 에미턴스 ε은 빔이 위상 공간에서 차지하는 불변 면적입니다. α, β, γ로 구성되는 트위스(Twiss) 매개변수는 "
            "선형 빔 광학 계산의 핵심 언어입니다."
        ),
        "cues_en": "Draw the connection between beta(s) and beam envelope sigma = sqrt(epsilon * beta).",
        "cues_kr": "실제 빔 폭 표준편차 σ(s) = √(ε·β(s)) 관계를 언급하여 물리적인 빔 크기와 베타 함수의 직접적 연결고리를 설명합니다.",
        "qa_en": "Q: Is emittance conserved under acceleration? A: Geometric emittance shrinks with momentum (adiabatic damping), but normalized emittance is conserved.",
        "qa_kr": "Q: 가속 과정에서 에미턴스는 보존되나요? A: 기하학적 에미턴스는 단열 감쇠(adiabatic damping)로 줄어들지만, 정규화 에미턴스는 보존됩니다.",
        "trans_en": "Now let us derive how steering magnets kick this betatron oscillation downstream: the Orbit Response Matrix.",
        "trans_kr": "이러한 베타트론 진동에 스티어링 전자석이 킥을 가했을 때 하류의 궤도가 어떻게 변하는지, 궤도 응답 행렬을 유도해보겠습니다."
    },
    {
        "num": 8,
        "category": "Analytical Optics",
        "title_en": "Orbit Response Matrix Derivation",
        "title_kr": "궤도 응답 행렬(Orbit Response Matrix, ORM) 유도",
        "visual_en": "Transfer-line betatron Green's function, R_ij equation with distance-decay denominator (1 + 0.05 Delta s), downstream causality (R_ij = 0 for j <= i).",
        "visual_kr": "단일 통과 빔라인 그린 함수, 감쇠 분모 (1 + 0.05·Δs)가 포함된 R_ij 수식, 상류에서 하류로만 작용하는 인과율(j ≤ i 일 때 R_ij = 0).",
        "script_en": (
            "When a dipole corrector magnet located at longitudinal position s_i applies an angular kick theta_i, it introduces a localized "
            "slope discontinuity delta x-prime = theta_i. Downstream at BPM station s_j, the perturbed trajectory is given by the single-pass "
            "transport-line Green's function. The orbit response element R_ij is defined as the displacement at BPM j per unit kick at steerer i: "
            "R_ij = square root of beta_i times beta_j times the sine of the phase advance difference psi_j minus psi_i. "
            "In our hackathon transport lattice, this response is modeled with simplified optics: a constant phase advance of 2 pi times 0.18 rad/m "
            "and a mild amplitude decay: R_ij = 1.2 sin(2 pi * 0.18 * Delta s) / (1 + 0.05 * Delta s). "
            "Most importantly, notice the strict downstream causality: a corrector can only affect BPMs located downstream of it (s_j > s_i). "
            "If BPM j is upstream of steerer i, R_ij is identically zero. This gives the 6 by 12 ORM its distinctive triangular causal structure."
        ),
        "script_kr": (
            "위치 s_i에 위치한 보정용 스티어링 전자석이 각도 θ_i만큼의 킥을 가하면, 입자 궤도에 Δx' = θ_i의 기울기 불연속이 발생합니다. "
            "하류의 s_j 위치에 있는 빔 위치 모니터(BPM)에서 측정되는 궤도 변화는 빔라인 전달 그린 함수(Green's function)에 의해 결정됩니다. "
            "단위 킥당 궤도 변화를 나타내는 궤도 응답 행렬(ORM) 원소 R_ij는 R_ij = √(β_i·β_j)·sin(ψ_j - ψ_i)로 정의됩니다. "
            "우리 해커톤 전송선에서는 위상 전진율 2π×0.18 rad/m와 완만한 진폭 감쇠를 반영하여 R_ij = 1.2·sin(2π·0.18·Δs) / (1 + 0.05·Δs)로 모델링되었습니다. "
            "여기서 가장 중요한 물리적 법칙은 '인과율(causality)'입니다. 스티어러는 자신보다 하류(downstream, s_j > s_i)에 위치한 BPM에만 영향을 줄 수 있으며, "
            "상류(upstream)에 있는 BPM에 대한 응답은 엄밀하게 0입니다. 이로 인해 6×12 크기의 ORM 행렬은 하삼각 형태의 인과적 구조를 갖게 됩니다."
        ),
        "cues_en": "Differentiate transport-line response (sine, strictly causal) from storage ring closed-orbit formula (2 sin(pi * nu) in denominator).",
        "cues_kr": "저장링의 폐궤도 공식(분모에 2·sin(πν) 포함)과 단일 통과 전송선의 인과적 그린 함수(sin 항) 간의 명확한 차이점을 환기합니다.",
        "qa_en": "Q: Can an upstream steerer correct downstream distortion? A: Yes, but downstream steerers cannot correct upstream distortion.",
        "qa_kr": "Q: 상류 스티어러로 하류 오차를 잡을 수 있나요? A: 가능합니다. 반대로 하류 스티어러로는 상류의 왜곡을 물리적으로 되돌릴 수 없습니다.",
        "trans_en": "Let us examine the physical layout of the transport lattice designed for our hackathon challenge.",
        "trans_kr": "이제 오늘 미니 해커톤에서 제어하게 될 15미터 빔 전송선의 실제 기하학적 배치도를 살펴보겠습니다."
    },
    {
        "num": 9,
        "category": "Hackathon Benchmark",
        "title_en": "15-Meter Transport Lattice Architecture",
        "title_kr": "15미터 빔 전송 격자 구조 및 진단 장치 배치",
        "visual_en": "Full lattice schematic showing 15.0 m length, 6 quadrupole magnets (alternating QF and QD), 6 dipole steerers (HCM1-3, VCM1-3), and 12 BPM stations.",
        "visual_kr": "15.0m 전송선 모식도: 교대 배치된 6개의 4극자(QF/QD), 6개의 2극 보정 전자석(HCM1~3, VCM1~3), 12개의 BPM 진단 스테이션.",
        "script_en": (
            "Here is the physical layout of our hackathon challenge lattice. It represents a realistic 15.0-meter high-energy transport line. "
            "Along this beamline, we have three pairs of alternating quadrupole magnets: focusing quadrupoles QF1 through QF3 and defocusing "
            "quadrupoles QD1 through QD3, creating an alternating-gradient FODO-like structure. For orbit correction, we have six dipole steering "
            "magnets: three horizontal steerers HCM1, HCM2, HCM3 and three vertical steerers VCM1, VCM2, VCM3, located between s = 0.2 meters "
            "and s = 8.0 meters. Finally, twelve Beam Position Monitors, BPM 1 through BPM 12, are distributed from s = 1.0 meter to s = 15.0 meters. "
            "Notice that steerers are concentrated in the first half of the line, while BPMs extend all the way to the end. "
            "Your controller's goal is to observe the 12 BPM readings and command the 6 steerer currents to flatten the beam orbit."
        ),
        "script_kr": (
            "이 슬라이드는 오늘 해커톤에서 다룰 15.0미터 길이의 빔 전송선 물리 배치도입니다. "
            "교대 배치된 6개의 4극 자석(QF1~3, QD1~3)이 FODO와 유사한 교대 구배 집속 격자를 구성하고 있습니다. "
            "궤도 제어를 위한 구동기(actuator)로는 수평 스티어러 3대(HCM1, 2, 3)와 수직 스티어러 3대(VCM1, 2, 3) 등 총 6대의 전자석이 "
            "s = 0.2m부터 8.0m 구간에 걸쳐 배치되어 있습니다. 빔 궤도 진단을 위한 센서로는 12대의 BPM(BPM 1~12)이 s = 1.0m부터 15.0m까지 "
            "전송선 전체에 걸쳐 균등하게 설치되어 있습니다. 스티어러 전자석은 전송선 전반부에 집중되어 있고, 진단 BPM은 끝단까지 배치되어 "
            "있음을 주목해 주십시오. 여러분의 제어기는 12개 BPM의 변위를 관측하여 6개 스티어러 전류를 정밀하게 인가해야 합니다."
        ),
        "cues_en": "Point out the dimensions: 12 BPM observations (inputs to controller), 6 corrector kicks (outputs of controller).",
        "cues_kr": "제어기 관점에서 관측값은 12차원 BPM 벡터, 제어 행동은 6차원 전류 델타(ΔI) 벡터임을 명확히 연결 짓습니다.",
        "qa_en": "Q: Why are there 6 correctors but 12 BPMs? A: The system is over-determined, requiring pseudo-inverse or regression optimization.",
        "qa_kr": "Q: 왜 스티어러는 6개인데 BPM은 12개인가요? A: 과결정(over-determined) 시스템이므로 완전 역행렬 대신 의사역행렬이나 최적화 기법이 필요합니다.",
        "trans_en": "However, in real accelerators, power supplies and sensors have hard physical limitations.",
        "trans_kr": "실제 가속기 현장에서는 전원 공급 장치와 센서의 하드웨어적 한계가 존재합니다. 다음 슬라이드에서 이를 확인해보겠습니다."
    },
    {
        "num": 10,
        "category": "Physical Limits",
        "title_en": "Hardware Limits & Actuator Bounds",
        "title_kr": "하드웨어 구동 한계 및 센서 노이즈 제약",
        "visual_en": "Hardware bounds card: Total current capacity [-5.0 A, +5.0 A], per-step slew rate limit [-0.8 A, +0.8 A], Gaussian measurement noise sigma = 10 um.",
        "visual_kr": "하드웨어 한계 요약: 총 코일 전류 허용치 [-5.0A, +5.0A], 단계당 슬루레이트 제한 [-0.8A, +0.8A], 센서 가우시안 노이즈 바닥 σ = 10 ㎛.",
        "script_en": (
            "A major reason toy simulation algorithms fail when deployed on real physical accelerators is the failure to respect hardware boundaries. "
            "In our benchmark environment, three strict physical constraints are enforced. First, Total Current Saturation: each corrector power "
            "supply is physically bounded to [-5.0 A, +5.0 A]. Exceeding this limit trips the over-current interlock. "
            "Second, Slew Rate and Inductive Limits: due to coil inductance L and power supply voltage limits d I / d t = V / L, the current can "
            "change by at most 0.8 Amperes per time step: delta I in [-0.8 A, +0.8 A]. Because the initial distortion requires total currents "
            "up to 2.84 Amperes to cancel, any controller physically requires at least 3 to 4 steps to converge—it is physically impossible to "
            "reach the sub-30 micron target in a single step! Third, Sensor Noise Floor: every BPM reading is corrupted by zero-mean Gaussian jitter "
            "with a standard deviation of 0.010 mm (10 microns). A controller that chases fluctuations below 10 microns is overfitting noise."
        ),
        "script_kr": (
            "이상적인 시뮬레이션에서 잘 작동하던 알고리즘이 실제 가속기에 적용되었을 때 실패하는 가장 큰 원인은 하드웨어 제약 조건을 간과하기 때문입니다. "
            "본 벤치마크 환경에는 세 가지 엄격한 물리적 한계가 구현되어 있습니다. 첫째, '총 전류 한계'입니다. 전자석 코일의 정격 용량으로 인해 "
            "총 전류는 [-5.0 A, +5.0 A] 범위로 제한됩니다. 둘째, '슬루레이트(slew rate) 및 유도 기전력 한계'입니다. 코일 인덕턴스(L)와 "
            "전원 전압 한계(dI/dt = V/L)로 인해, 한 번의 제어 단계에서 인가할 수 있는 전류 증분은 최대 0.8 암페어로 엄격히 제한됩니다: "
            "ΔI ∈ [-0.8 A, +0.8 A]. 초기 궤도 왜곡을 보정하기 위해 필요한 누적 전류가 최대 2.84 A에 달하므로, 어떠한 완벽한 제어기라도 "
            "물리적으로 최소 3~4스텝 이상이 소요됩니다. 1스텝 만의 수렴은 물리적으로 불가능합니다! 셋째, '센서 노이즈 바닥'입니다. "
            "모든 BPM 측정값에는 표준편차 σ = 0.010 mm (10 ㎛)의 가우시안 지터가 포함됩니다. 10 ㎛ 이하의 잔여 오차를 억지로 잡으려 하면 "
            "노이즈를 증폭시키는 과적합이 발생합니다."
        ),
        "cues_en": "Emphasize the 3 to 4 step minimum! Explain why this is crucial for interpreting hackathon speed scores.",
        "cues_kr": "0.8A 스텝 제한으로 인해 최소 3~4스텝이 소요된다는 점을 강조하여, 해커톤 수렴 속도 점수의 물리적 한계를 인지시킵니다.",
        "qa_en": "Q: What happens if an agent returns delta_I = 2.0 A? A: The environment hard-clips it to 0.8 A, but well-behaved agents should constrain actions internally.",
        "qa_kr": "Q: 제어기가 ΔI = 2.0 A를 출력하면 어떻게 되나요? A: 환경 내부에서 0.8 A로 강제 클리핑되지만, 바람직한 제어기는 자체적으로 경계를 준수해야 합니다.",
        "trans_en": "Beyond linear limits, magnetic cores exhibit non-linear physical saturation.",
        "trans_kr": "하드웨어 한계에 더해, 전자석 철심 내부에서 일어나는 비선형 자기 포화 현상을 살펴보겠습니다."
    },
    {
        "num": 11,
        "category": "Non-Linear Physics",
        "title_en": "Magnetic Core Non-Linear Saturation",
        "title_kr": "전자석 철심의 비선형 자기 포화(Magnetic Core Saturation)",
        "visual_en": "B-H saturation curve, cubic saturation formula Y = I*R - 0.015*(I^3*R) + Y0 + epsilon, and comparison between linear vs saturated orbit responses.",
        "visual_kr": "B-H 자기 포화 곡선, 3차 비선형 수식 Y = I·R - 0.015·(I³·R) + Y₀ + ε, 선형 응답과 비선형 포화 응답 곡선의 편차 비교.",
        "script_en": (
            "In introductory accelerator physics courses, magnetic field strength B is assumed to scale linearly with excitation current I: "
            "B equals mu-zero N I over g. However, real accelerator magnet cores are composed of ferromagnetic laminated silicon steel. "
            "At low currents, magnetic domains align easily. But above 1.5 to 2.0 Amperes, magnetic permeability mu-r drops precipitously as domain "
            "alignment saturates. In our simulation environment, this is modeled via a classic cubic soft-saturation term: "
            "Y = I times R minus 0.015 times ( I cubed times R ) plus Y_0 plus epsilon. "
            "Notice what this means: when total current reaches 2.5 Amperes, the cubic term subtracts nearly 23 percent of the expected deflection! "
            "If a controller assumes linear optics, it will severely underestimate the required kick, undershoot the correction, and oscillate. "
            "Capturing and compensating this non-linear saturation is precisely why we need machine learning surrogates."
        ),
        "script_kr": (
            "기초 가속기 물리학에서는 암페어 법칙에 따라 전자석 자장 B가 인가 전류 I에 정비례한다고 가정합니다: B = μ₀·N·I / g. "
            "하지만 실제 전자석 철심은 강자성체인 규소강판 등으로 제작됩니다. 전류가 낮을 때는 자벽(magnetic domain)이 쉽게 정렬되지만, "
            "전류가 1.5~2.0 A를 넘어서면 철심 내부의 자기 모멘트가 포화되면서 비투자율 μ_r이 급격히 저하됩니다. "
            "우리 환경에서는 이를 3차 소프트 포화 항으로 정밀하게 모사했습니다: Y = I·R - 0.015·(I³·R) + Y₀ + ε. "
            "이 수식이 의미하는 바를 주목해 주십시오. 누적 전류가 2.5 A에 도달하면, 3차 포화 항(-0.015·I³)으로 인해 선형 예상치보다 자장이 "
            "무려 23% 이상 감소합니다! 선형 광학 모델(ORM)에만 의존하는 제어기는 필요한 킥의 크기를 과소평가하여 목표치에 도달하지 못하고 "
            "헤매게 됩니다. 바로 이 비선형 포화 효과를 사전에 학습하고 보상하기 위해 머신러닝 대리 모델이 필요한 것입니다."
        ),
        "cues_en": "Point to the -0.015 * I^3 term. Show that the distortion correction requires up to 2.84 A, deep inside this non-linear regime.",
        "cues_kr": "초기 궤도 보정에 최대 2.84 A의 전류가 필요하므로, 3차 포화 효과가 극대화되는 비선형 영역에서 제어가 이루어짐을 역설합니다.",
        "qa_en": "Q: Can classical SVD converge under this cubic saturation? A: It can converge with a conservative low gain alpha=0.45, but it takes 9.4 steps instead of 3.6.",
        "qa_kr": "Q: 고전 SVD 제어기는 이 비선형 포화 상태에서 수렴하지 못하나요? A: 게인(α=0.45)을 낮추면 수렴은 하지만, 9.4스텝이나 걸려 고득점을 얻기 어렵습니다.",
        "trans_en": "Now let us transition into Machine Learning: how do neural networks model complex non-linear functions?",
        "trans_kr": "이제 머신러닝의 기초로 넘어가서, 인공신경망이 어떻게 이러한 복잡한 비선형 함수를 학습하는지 원리를 살펴보겠습니다."
    },
    {
        "num": 12,
        "category": "ML Foundations",
        "title_en": "Artificial Neurons & Layer Composition",
        "title_kr": "인공 뉴런(Artificial Neuron)과 신경망 계층 구성",
        "visual_en": "Anatomy of an artificial neuron: inputs x_i, synaptic weights w_i, bias b, linear combination z = w^T x + b, activation sigma(z), and Multi-Layer Perceptron stacking.",
        "visual_kr": "인공 뉴런 구조: 입력 x_i, 시냅스 가중치 w_i, 편향 b, 선형 결합 z = wᵀx + b, 활성화 함수 σ(z), 다층 퍼셉트론(MLP) 레이어 적층 모식도.",
        "script_en": (
            "The fundamental building block of deep learning is the artificial neuron, originally conceived by McCulloch and Pitts in 1943. "
            "A neuron receives an input vector x in R^n. Each input is scaled by a trainable synaptic weight w_i, summed together, and shifted "
            "by a scalar bias b: z = w^T x + b. This pre-activation value z is then passed through a non-linear activation function sigma(z) "
            "to produce the scalar output a. Stacking these neurons in parallel creates a dense layer: h = sigma( W x + b ), where W is a weight "
            "matrix and b is a bias vector. Stacking multiple dense layers sequentially produces a Multi-Layer Perceptron (MLP). "
            "According to the Universal Approximation Theorem proven by Cybenko and Hornik, a feedforward network with non-linear activations "
            "can approximate any continuous non-linear physical function on a compact domain to arbitrary precision."
        ),
        "script_kr": (
            "딥러닝의 가장 기본 단위는 1943년 매컬럭과 피츠가 제안한 '인공 뉴런(artificial neuron)'입니다. "
            "뉴런은 n차원 입력 벡터 x를 받습니다. 각 입력값은 학습 가능한 시냅스 가중치 w_i와 곱해진 후 합산되며, 임계값을 조절하는 편향 b가 "
            "더해집니다: z = wᵀx + b. 이 선형 결합 값 z는 비선형 활성화 함수 σ(z)를 통과하여 최종 출력 a를 생성합니다. "
            "이러한 뉴런들을 병렬로 배치하면 밀집 레이어(dense layer) h = σ(W x + b)가 형성되며, 여러 개의 레이어를 순차적으로 적층하면 "
            "'다층 퍼셉트론(Multi-Layer Perceptron, MLP)'이 완성됩니다. 시벤코(Cybenko)와 호닉(Hornik)의 보편 근사 정리(Universal Approximation Theorem)에 "
            "따르면, 비선형 활성화 함수를 가진 다층 신경망은 적절한 가중치만 주어진다면 어떠한 연속 비선형 물리 함수도 임의의 정밀도로 근사할 수 있습니다."
        ),
        "cues_en": "Clarify the distinction between linear transformation (W x + b) and non-linear mapping sigma(z).",
        "cues_kr": "선형 변환(W x + b)과 비선형 활성화 함수 σ(z)의 명확한 역할 분담을 설명합니다.",
        "qa_en": "Q: What happens if sigma is linear? A: The entire network collapses to a single matrix multiplication, losing all non-linear power.",
        "qa_kr": "Q: 활성화 함수 σ가 선형이면 어떻게 되나요? A: 아무리 많은 레이어를 쌓아도 단 하나의 행렬 곱으로 축퇴되어 비선형성을 전혀 표현할 수 없습니다.",
        "trans_en": "This brings us to a critical question: how do different activation functions shape neural representations?",
        "trans_kr": "그렇다면 활성화 함수는 신경망 내부에서 구체적으로 어떤 역할을 하며, 어떤 함수들이 사용되는지 확인해보겠습니다."
    },
    {
        "num": 13,
        "category": "ML Foundations",
        "title_en": "Activation Functions in Neural Networks",
        "title_kr": "신경망 활성화 함수(Activation Functions)의 역할과 분류",
        "visual_en": "Four core operational roles of activations, mathematical catalog: ReLU, Leaky ReLU, Tanh, Sigmoid, GELU, Linear, and plot of f(z) vs f'(z).",
        "visual_kr": "활성화 함수의 4대 핵심 역할, 주요 활성화 함수 수식 및 특성(ReLU, Leaky ReLU, Tanh, Sigmoid, GELU, Linear), 함수값 및 도함수 비교 그래프.",
        "script_en": (
            "Activation functions fulfill four essential operational roles in accelerator neural networks. First, Breaking Linearity: without them, "
            "deep architectures collapse to a single linear matrix. Second, Universal Approximation: non-linearities allow the network to model "
            "cubic core saturation and sextupole aberrations. Third, Gradient Gating: the derivative sigma-prime of z dictates how loss gradients "
            "propagate backward during training; non-saturating functions prevent vanishing gradients. Fourth, Output Coordinate Preservation: "
            "intermediate layers need non-linearities, but regression outputs predicting spatial coordinates in millimeters must use the linear identity function. "
            "In our catalog, ReLU is the default choice: f(z) = max(0, z), offering derivative 1 for positive z, which prevents vanishing gradients. "
            "Tanh squashes values to [-1, 1], useful for normalized priors but prone to saturation. GELU provides smooth probabilistic gating, "
            "popular in modern transformer and surrogate models."
        ),
        "script_kr": (
            "가속기 신경망에서 활성화 함수는 네 가지 본질적인 역할을 수행합니다. 첫째, '선형성 타파'입니다. 활성화 함수가 없다면 아무리 깊은 신경망도 "
            "하나의 선형 행렬로 붕괴됩니다. 둘째, '비선형 물리 동역학의 근사'입니다. 자기 포화나 6극자 왜곡을 정확히 표현할 수 있게 합니다. "
            "셋째, '역전파 그래디언트 제어'입니다. 도함수 σ'(z)는 오차 신호가 상류 레이어로 전달되는 게이트 역할을 하며, 기울기 소실(vanishing gradient)을 "
            "방지합니다. 넷째, '출력 공간의 물리적 연속성 보장'입니다. 은닉층에는 비선형성이 필수적이지만, 빔 궤도 변위(mm)를 예측하는 출력층은 "
            "반드시 선형 항등 함수(linear identity)를 사용하여 인위적인 값 클리핑을 막아야 합니다. "
            "가장 널리 쓰이는 ReLU는 z > 0에서 도함수가 항상 1이므로 기울기 소실을 완벽히 방지하며 계산 효율이 매우 뛰어납니다."
        ),
        "cues_en": "Reiterate Role 4: Output layer MUST use Linear/Identity! Never apply Sigmoid or Tanh to unnormalized physical coordinates.",
        "cues_kr": "네 번째 역할인 '출력층의 선형 활성화 함수 필수 사용'을 거듭 강조합니다. 출력에 Sigmoid 등을 적용하면 빔 변위가 인위적으로 잘리게 됩니다.",
        "qa_en": "Q: What is the 'dying ReLU' problem? A: If a neuron's input is negative, its gradient is 0 and it can never recover; Leaky ReLU fixes this.",
        "qa_kr": "Q: 'Dying ReLU' 현상이란 무엇인가요? A: 입력값이 0 이하가 되면 기울기가 0이 되어 가중치가 더 이상 업데이트되지 않는 현상이며, Leaky ReLU로 완화할 수 있습니다.",
        "trans_en": "To make this concrete, let us look at a worked example: surrogating an analytical particle transfer matrix.",
        "trans_kr": "이러한 활성화 함수의 거동을 입자 전달 행렬을 모사하는 구체적인 예제를 통해 시각적으로 확인해보겠습니다."
    },
    {
        "num": 14,
        "category": "ML Foundations",
        "title_en": "NN Surrogate Example: Particle Transfer Matrix",
        "title_kr": "신경망 대리 모델 예제: 입자 전달 행렬(Transfer Matrix M) 학습",
        "visual_en": "Surrogate formulation mapping (x_0, x'_0) to (x_f, x'_f), compact vector notation z_f = f_theta(z_0), symplecticity det(M) = 1, and enlarged TikZ architecture diagram.",
        "visual_kr": "초기 위상공간 (x₀, x'₀)에서 최종 (x_f, x'_f)로의 매핑 수식, 벡터 표현 ẑ_f = f_θ(z₀), 심플렉틱 조건 det(M) = 1, 확대된 TikZ 신경망 구조도.",
        "script_en": (
            "To bridge machine learning directly with beam optics, let us construct a neural surrogate for a linear transfer matrix M. "
            "In linear optics, the transverse particle trajectory from initial position s_0 to diagnostic station s_f is governed by the 2 by 2 "
            "transfer matrix: [x_f, x-prime_f]^T = M [x_0, x-prime_0]^T, with det M = 1 ensuring phase-space area conservation by Liouville's theorem. "
            "Instead of analytical matrix multiplication, we train a neural surrogate f_theta mapping R^2 to R^2: "
            "z_hat_f = W^(3) sigma( W^(2) sigma( W^(1) z_0 + b^(1) ) + b^(2) ) + b^(3). "
            "We train this network over thousands of particle tracking pairs using Mean Squared Error loss. On the right, you see the network layout: "
            "2 input nodes for initial coordinate and angle, two hidden layers with 4 units each, and 2 output nodes predicting final position and angle. "
            "Notice the critical label at the bottom: the output activation must be strictly linear to preserve unbounded phase-space coordinates."
        ),
        "script_kr": (
            "머신러닝과 빔 광학을 직접 연결해보기 위해, 선형 전달 행렬 M을 신경망으로 대리 모델링하는 예제를 구성했습니다. "
            "선형 빔 광학에서 초기 위치 s₀의 횡방향 좌표와 각도 (x₀, x'₀)는 2×2 전달 행렬 M을 통해 최종 위치 (x_f, x'_f)로 변환됩니다: "
            "[x_f, x'_f]ᵀ = M · [x₀, x'₀]ᵀ. 이때 리우빌 정리(Liouville's theorem)에 의해 행렬식 det M = 1을 만족하며 위상 공간 면적이 보존됩니다. "
            "우리는 해석적 행렬 곱 대신 2차원에서 2차원으로 매핑하는 신경망 f_θ를 구성했습니다: "
            "ẑ_f = W⁽³⁾ σ( W⁽²⁾ σ( W⁽¹⁾ z₀ + b⁽¹⁾ ) + b⁽²⁾ ) + b⁽³⁾. "
            "수천 개의 트래킹 입자 쌍에 대해 평균제곱오차(MSE) 손실 함수로 이 네트워크를 학습시킵니다. "
            "오른쪽 구조도를 보시면 2개의 입력 뉴런, 4개의 뉴런을 갖는 2개의 은닉층, 그리고 최종 좌표를 예측하는 2개의 출력 뉴런으로 이루어져 있습니다. "
            "하단에 강조되어 있듯이, 최종 출력 뉴런의 활성화 함수는 반드시 선형 항등 함수여야 합니다."
        ),
        "cues_en": "Point out the compact vector notation z_f = f_theta(z_0). Explain that Jacobian determinant det(J) measures area conservation.",
        "cues_kr": "컴팩트한 벡터 표기법 ẑ_f = f_θ(z₀)를 설명하고, 신경망 야코비 행렬식 det(J)가 위상공간 면적 보존을 나타냄을 언급합니다.",
        "qa_en": "Q: Can an MLP preserve det(M) = 1 exactly? A: Standard MLPs only approximate det(J) ≈ 1; Hamiltonian Neural Networks (HNNs) enforce it exactly.",
        "qa_kr": "Q: 일반 MLP가 det(M) = 1을 완벽히 보존할 수 있나요? A: 일반 MLP는 오차 범위 내에서 근사할 뿐이며, 엄밀한 보존을 위해서는 해밀토니안 신경망(HNN)이나 PINN 구조가 필요합니다.",
        "trans_en": "What happens if we choose different activation functions inside this surrogate? Let us look at Slide 15.",
        "trans_kr": "이 전달 행렬 대리 모델의 은닉층에 서로 다른 활성화 함수를 적용하면 위상 공간에서 어떤 기하학적 왜곡이 일어나는지 살펴보겠습니다."
    },
    {
        "num": 15,
        "category": "ML Foundations",
        "title_en": "NN Surrogate: Activation Functions in Beam Transport",
        "title_kr": "빔 전송 대리 모델에서 활성화 함수별 위상 공간 변형",
        "visual_en": "Three-way comparison of Linear, ReLU, and Tanh activation impacts on phase-space ellipses, symplecticity preservation, and mathematical collapse.",
        "visual_kr": "선형(Linear), ReLU, Tanh 활성화 함수가 위상공간 타원에 미치는 기하학적 영향 비교: 행렬 축퇴, 다면체 꺾임, 에미턴스 수축 현상.",
        "script_en": (
            "This slide reveals the profound geometric impact of activation function selection when surrogating beam transport. "
            "First, consider Linear Activation: stacking linear dense layers mathematically collapses into a single matrix product W_eff x + b_net. "
            "It is mathematically identical to a transfer matrix. It perfectly preserves smooth phase-space ellipses and symplecticity, "
            "but it possesses zero capacity to model non-linear saturation or sextupole kicks. "
            "Second, consider ReLU: because ReLU is piecewise linear, it partitions phase space into polyhedral facets separated by activation hyperplanes. "
            "It transforms smooth continuous beam ellipses into faceted polygons with sharp slope kinks! Furthermore, in regions where neurons die "
            "(z < 0), the Jacobian determinant collapses to zero, completely violating Liouville's theorem. "
            "Third, consider Tanh: near the origin, tanh(z) is approximately z, accurately reproducing linear betatron motion. However, at large amplitudes, "
            "hidden neurons saturate to plus or minus one, squashing the ellipse into an S-curve, artificially shrinking beam emittance, and producing "
            "unphysical boundary artifacts. This demonstrates why activation selection must be guided by beam physics."
        ),
        "script_kr": (
            "이 슬라이드는 전달 행렬을 학습할 때 활성화 함수 선택이 위상 공간에 미치는 심오한 기하학적 영향을 보여줍니다. "
            "첫째, '선형 활성화 함수'를 은닉층에 사용하면 모든 계층이 단 하나의 유효 행렬 곱 W_eff x + b_net으로 축퇴됩니다. "
            "수학적으로 선형 전달 행렬과 완전히 동일하므로 매끄러운 빔 타원과 심플렉틱 면적 보존을 완벽히 유지하지만, 3차 자기 포화나 6극자 왜곡을 "
            "전혀 표현할 수 없습니다. "
            "둘째, 'ReLU'는 조각별 선형(piecewise linear) 함수이므로 위상 공간을 초평면으로 분할합니다. 그 결과 매끄러운 빔 타원이 모서리가 각진 "
            "'다면체 다각형(faceted polygon)'으로 변형됩니다! 더욱이 뉴런이 비활성화(z < 0)되는 음의 영역에서는 야코비 행렬식이 0으로 붕괴되어 "
            "리우빌 정리를 심각하게 위반합니다. "
            "셋째, 'Tanh'는 원점 부근에서는 tanh(z) ≈ z로 선형 광학을 잘 모사하지만, 진폭이 큰 빔 헤일로(halo) 영역에서는 ±1로 포화되어 "
            "타원을 S자 형태로 찌그러뜨리고 빔 에미턴스를 인위적으로 축소시키는 왜곡을 일으킵니다."
        ),
        "cues_en": "Emphasize: Linear preserves ellipses but lacks non-linearity; ReLU facets ellipses; Tanh saturates emittance. Core physics intuition!",
        "cues_kr": "선형은 비선형을 못 배우고, ReLU는 타원을 각지게 만들며, Tanh는 에미턴스를 왜곡시킨다는 물리적 직관을 명확히 대조합니다.",
        "qa_en": "Q: Which activation is best for our hackathon MLP? A: ReLU or Leaky ReLU in hidden layers, but linear in output.",
        "qa_kr": "Q: 이번 해커톤 MLP에는 어떤 활성화 함수가 가장 적합한가요? A: 은닉층에는 ReLU 또는 Leaky ReLU를 사용하고, 출력층에는 반드시 선형을 적용하는 것이 표준입니다.",
        "trans_en": "Once an architecture is defined, how do we optimize its millions of parameters? Let us examine modern optimization algorithms.",
        "trans_kr": "신경망 구조를 정의한 후, 수만 개의 파라미터를 어떻게 최적화하는지 최신 최적화 알고리즘들을 살펴보겠습니다."
    },
    {
        "num": 16,
        "category": "ML Foundations",
        "title_en": "Optimization Algorithms in Machine Learning",
        "title_kr": "머신러닝 최적화 알고리즘: 경사하강법부터 Adam 및 L-BFGS-B까지",
        "visual_en": "Comparison card of first-order and quasi-Newton optimizers: SGD, Momentum, Adam (first & second moments), and SciPy L-BFGS-B with box constraints.",
        "visual_kr": "1차 경사하강법 및 준뉴턴 최적화 비교 카드: SGD, 모멘텀, Adam(1차 및 2차 모멘트 적응형 스케일링), 박스 경계 준뉴턴 L-BFGS-B.",
        "script_en": (
            "Training a neural network means finding parameter weights theta that minimize the loss function L(theta). "
            "On this slide, we compare four major optimization algorithms. First is Stochastic Gradient Descent (SGD): it steps in the direction "
            "of steepest descent: theta becomes theta minus eta times gradient L. While simple, SGD oscillates wildly across high-curvature ravines. "
            "Second is Momentum SGD: it adds an inertia term gamma v_(t-1), dampening transverse oscillations and accelerating along consistent ravines. "
            "Third is the Adam Optimizer—Adaptive Moment Estimation. Adam computes both the first moment m_t (the exponentially decaying gradient average) "
            "and the second raw moment v_t (the uncentered variance). By dividing the step by square root of v_t, Adam automatically scales down updates "
            "for parameters that receive noisy, high-magnitude gradients and scales up updates for subtle parameters. It is the gold standard for training "
            "accelerator surrogates. Fourth is L-BFGS-B: a second-order quasi-Newton method that approximates the inverse Hessian from gradient history. "
            "Unlike Adam, which is used for offline network training, L-BFGS-B is used in our hackathon for online model inversion under strict [-0.8 A, 0.8 A] bounds."
        ),
        "script_kr": (
            "신경망 학습이란 손실 함수 L(θ)를 최소화하는 파라미터 θ를 찾아가는 과정입니다. 이 슬라이드에서는 4가지 주요 최적화 알고리즘을 비교합니다. "
            "첫째는 '확률적 경사하강법(SGD)'입니다: 최급강하 방향으로 θ ← θ - η∇L 만큼 이동합니다. 단순하지만 곡률이 큰 협곡 지형에서 발진하며 수렴이 느립니다. "
            "둘째는 '모멘텀(Momentum) SGD'입니다: 이전 단계의 관성 벡터 γ·v를 더해주어 진동을 억제하고 일관된 경사 방향으로 빠르게 가속합니다. "
            "셋째는 'Adam(Adaptive Moment Estimation)'입니다: 1차 모멘트(기울기 평균)와 2차 모멘트(기울기 제곱 평균)를 동시에 추적하여, 파라미터별로 "
            "학습률을 적응형으로 스케일링합니다. 민감한 파라미터의 스텝은 줄이고 둔감한 파라미터의 스텝은 키워주므로, 결합된 다채널 자석 대리 모델 학습의 "
            "표준으로 사용됩니다. 넷째는 'L-BFGS-B'입니다: 헤시안 역행렬을 근사하는 2차 준뉴턴(quasi-Newton) 기법입니다. 오프라인 학습에 쓰이는 Adam과 달리, "
            "L-BFGS-B는 해커톤 제어기에서 매 스텝 대리 모델을 역산(inversion)하여 [-0.8A, 0.8A] 전류 한계 내에서 최적의 킥을 도출할 때 사용됩니다."
        ),
        "cues_en": "Highlight the role separation: Adam is used to TRAIN the surrogate offline; L-BFGS-B is used to INVERT the surrogate online at every step.",
        "cues_kr": "역할 구분을 명확히 합니다: Adam은 오프라인에서 대리 모델을 '학습'시킬 때 쓰이고, L-BFGS-B는 온라인에서 대리 모델을 '역산'하여 제어 킥을 찾을 때 쓰입니다.",
        "qa_en": "Q: Why not use L-BFGS-B to train the MLP? A: L-BFGS-B requires full batch evaluation and struggles with stochastic mini-batch noise.",
        "qa_kr": "Q: MLP 학습 자체에 L-BFGS-B를 쓰면 안 되나요? A: 소규모 데이터나 결정론적 문제에서는 우수하지만, 미니배치 노이즈가 있는 대규모 데이터에서는 Adam이 훨씬 강건합니다.",
        "trans_en": "Are MLPs the only neural network used in accelerators? Absolutely not. Let us examine specialized neural architectures.",
        "trans_kr": "그렇다면 가속기에서는 MLP만 사용될까요? 전혀 아닙니다. 현대 가속기 물리에 특화된 고급 신경망 구조들을 살펴보겠습니다."
    },
    {
        "num": 17,
        "category": "ML Foundations",
        "title_en": "Specialized Neural Architectures: Beyond Plain MLPs",
        "title_kr": "MLP를 넘어선 가속기 특화 신경망 구조: PINN, PRNN, VAE, U-Net",
        "visual_en": "Four-quadrant panel layout covering PINN (ODE/PDE loss residual), PRNN/RNN (recurrent dynamic memory), VAE (probabilistic latent manifold), and U-Net (multiscale skip connections).",
        "visual_kr": "4분면 패널 레이아웃: PINN(물리 미분방정식 손실 통합), PRNN/RNN(시간적 동역학 및 히스테리시스 메모리), VAE(확률적 잠재 공간 및 이상 진단), U-Net(다중 스케일 스킵 연결 및 빔 영상 복원).",
        "script_en": (
            "While plain MLPs excel at static black-box regression, physical accelerators present challenges that violate standard feedforward assumptions. "
            "Here we introduce four domain-adapted deep learning architectures. First, Physics-Informed Neural Networks (PINNs): they embed governing "
            "differential equations—such as Hill's equation or Poisson's space-charge equation—directly into the training loss via automatic differentiation: "
            "L_PINN = L_data + lambda || D[f](x) ||^2. This guarantees physical conservation laws like symplecticity even in data-sparse drift sections. "
            "Second, Physics-Guided Recurrent Neural Networks (PRNNs): sequential architectures with hidden memory h_t = sigma( W_h h_(t-1) + W_x x_t + b ). "
            "Unlike static MLPs, PRNNs capture non-Markovian memory, temporal eddy current lags, and magnetic iron hysteresis loops during magnet cycling. "
            "Third, Variational Autoencoders (VAEs): probabilistic encoder-decoders that map observations to a continuous latent Gaussian distribution z ~ N(mu, Sigma), "
            "optimized via the Evidence Lower Bound (ELBO). VAEs compress 6D bunch phase-space distributions and detect precursor beam trip anomalies. "
            "Fourth, U-Net and CNNs: fully convolutional encoder-decoders with multiscale skip connections, preserving spatial translation equivariance "
            "for real-time beam profile screen imaging (YAG, OTR), halo segmentation, and 3D magnetic field interpolation."
        ),
        "script_kr": (
            "단순한 MLP는 정적 회귀 문제에는 우수하지만, 실제 가속기 현장의 복잡한 물리 법칙을 만족시키기에는 한계가 있습니다. "
            "이 슬라이드에서는 가속기 물리에 최적화된 4가지 고급 딥러닝 아키텍처를 소개합니다. "
            "첫째는 '물리 정보 신경망(PINN)'입니다: 힐 방정식이나 포아송 공간전하 방정식 같은 지배 미분방정식을 자동미분(autograd)을 통해 손실 함수에 직접 "
            "통합합니다: L_PINN = L_data + λ·||D[f](x)||². 이를 통해 데이터가 부족한 드리프트 구간에서도 에너지 및 심플렉틱 보존 법칙을 완벽히 만족합니다. "
            "둘째는 '물리 유도 순환신경망(PRNN/RNN)'입니다: 내부 은닉 상태 h_t를 통해 이전 시점의 이력을 기억합니다. 정적 입력만 처리하는 MLP와 달리, "
            "전자석 충방전 시 발생하는 비선형 자기 히스테리시스 루프, 와전류(eddy current) 지연, 초전도 공동의 감쇠 현상을 정확히 추적합니다. "
            "셋째는 '변이형 오토인코더(VAE)'입니다: 입력 데이터를 연속적인 가우시안 잠재 공간 z ~ N(μ, Σ)으로 압축하고 ELBO를 최대화합니다. "
            "6차원 입자 다발 위상 공간 압축 및 빔 정지 전조 증상을 비지도 학습으로 감지하는 데 탁월합니다. "
            "넷째는 'U-Net 및 합성곱 신경망(CNN)'입니다: 공간적 병진 대칭성을 활용하며, 축소 경로와 확장 경로를 연결하는 스킵 연결(skip connection)을 통해 "
            "YAG/OTR 형광 스크린 빔 프로파일 영상 복원, 빔 헤일로 분할, 3차원 자장 맵 보간을 서브픽셀 정밀도로 수행합니다."
        ),
        "cues_en": "Walk through each quadrant methodically. Emphasize why each overcomes specific limitations of plain MLPs in accelerator operations.",
        "cues_kr": "각 사분면을 시계 방향으로 짚어가며, 각 구조가 단순 MLP의 어떤 물리적 한계점을 극복했는지 명확히 설명합니다.",
        "qa_en": "Q: Can PINNs be used for closed-loop orbit control? A: Yes, PINN surrogates provide superior generalization when operating far from design calibration orbits.",
        "qa_kr": "Q: 폐루프 궤도 제어에 PINN을 대리 모델로 쓸 수 있나요? A: 가능합니다. 보정 킥이 매우 커서 훈련 데이터 범위를 벗어날 때 PINN이 훨씬 물리적으로 신뢰할 수 있는 예측을 제공합니다.",
        "trans_en": "Now let us enter the core competitive tracks of our mini-hackathon, beginning with Paradigm 1: Supervised Learning.",
        "trans_kr": "이제 오늘 미니 해커톤의 첫 번째 핵심 트랙인 지도학습 대리 모델 역산 제어로 들어가 보겠습니다."
    },
    {
        "num": 18,
        "category": "Paradigm 1: Supervised Learning",
        "title_en": "Supervised Learning: Digital Twins & Hyperparameters",
        "title_kr": "지도학습: 디지털 트윈 대리 모델링 및 하이퍼파라미터",
        "visual_en": "Left column: Terminology (weights, loss, backprop, epoch, batch, early stopping). Right column: Hyperparameter taxonomy table with tunable rows highlighted in red (TODO 1).",
        "visual_kr": "좌측: 핵심 용어(가중치, 손실 함수, 역전파, 에포크, 배치, 조기 종료). 우측: 참가자 튜닝 가능 변수(TODO 1)가 빨간색으로 강조된 하이퍼파라미터 분류표.",
        "script_en": (
            "Paradigm 1 represents the standard digital twin approach: supervised forward surrogate modeling. "
            "On the left, we define the core training mechanics. Weights W and biases b are updated iteratively by backpropagating loss gradients. "
            "An epoch represents one complete pass through all 1,500 training shots. A batch B is the subset of shots evaluated per gradient step. "
            "Early stopping halts training when validation loss plateaus, preventing the model from memorizing Gaussian sensor jitter. "
            "On the right, we present the hyperparameter taxonomy governing your model. The red rows indicate the exact parameters you can tune "
            "in notebook TODO 1: the learning rate eta (default 10^-3 with Adam), the batch size B (32 to 128), the hidden layer architecture "
            "(default 128, 64, 32), the activation function (ReLU or Leaky ReLU), the L2 weight regularization alpha (10^-4), and max epochs (400). "
            "Tuning these parameters directly governs the accuracy of your forward digital twin."
        ),
        "script_kr": (
            "첫 번째 패러다임은 가속기 디지털 트윈의 표준 기법인 '지도학습 순방향 대리 모델링'입니다. "
            "좌측에는 모델 학습의 핵심 메커니즘을 정리했습니다. 가중치 W와 편향 b는 손실 함수의 기울기를 역전파하여 반복 수정됩니다. "
            "에포크(epoch)는 1,500개의 전체 훈련 데이터를 1회 완독하는 주기이며, 배치(batch)는 1회 가중치 업데이트에 사용되는 샘플 묶음입니다. "
            "조기 종료(early stopping)는 검증 손실이 더 이상 줄어들지 않을 때 학습을 멈춰 센서 노이즈 과적합을 방지합니다. "
            "우측 표에는 여러분이 노트북 TODO 1에서 직접 수정할 수 있는 핵심 하이퍼파라미터들이 빨간색으로 강조되어 있습니다. "
            "학습률(기본 10⁻³), 배치 크기(32~128), 은닉층 구조(기본 128, 64, 32), 활성화 함수(ReLU/Tanh), L2 규제 계수(10⁻⁴), 최대 에포크 수 등이 포함됩니다. "
            "이 하이퍼파라미터들을 어떻게 최적화하느냐에 따라 여러분의 디지털 트윈 정밀도가 결정됩니다."
        ),
        "cues_en": "Call out the red asterisks: these match TODO 1 in the participant notebook. Highlighting gives attendees clear hackathon targets.",
        "cues_kr": "빨간색 별표(*)로 표시된 행들이 참가자 노트북 TODO 1에서 직접 수정할 수 있는 변수임을 강조합니다.",
        "qa_en": "Q: What happens if batch size is too small? A: Training is slower on GPUs and gradient updates can be excessively noisy.",
        "qa_kr": "Q: 배치 크기가 너무 작으면 어떻게 되나요? A: 그래디언트 노이즈가 심해져 손실 값이 요동치고, GPU 병렬 연산 효율이 떨어집니다.",
        "trans_en": "Let us examine the exact architecture of the MLP surrogate digital twin.",
        "trans_kr": "그렇다면 이 디지털 트윈 신경망의 입출력 구조와 계층 배치는 어떻게 이루어져 있는지 확인해보겠습니다."
    },
    {
        "num": 19,
        "category": "Paradigm 1: Supervised Learning",
        "title_en": "The Neural Surrogate Digital Twin",
        "title_kr": "신경망 대리 모델 디지털 트윈 구조",
        "visual_en": "High-resolution schematic showing 6 input currents, three hidden layers (128, 64, 32 units) with ReLU activations, and 12 output predicted BPM readings.",
        "visual_kr": "신경망 디지털 트윈 구조도: 6개 입력 전류 [I₁~I₆], 3개 은닉층(128, 64, 32 뉴런)과 ReLU 활성화, 12개 출력 예측 궤도 [Ŷ₁~Ŷ₁₂].",
        "script_en": (
            "Here is the detailed topology of our neural surrogate digital twin. It maps the 6 dipole corrector currents directly to the 12 BPM "
            "orbit readings: f_theta maps R^6 to R^12. The input layer ingests the current vector: HCM 1 to 3 and VCM 1 to 3. "
            "The signal propagates through three fully connected hidden layers: the first layer expands the 6 inputs into 128 abstract features; "
            "the second layer condenses them to 64 units; and the third layer refines them to 32 units. All hidden layers employ ReLU activations. "
            "The output layer projects the 32 units onto the 12 BPM predictions through a linear activation. In total, this network contains 11,596 "
            "trainable parameters. While a linear matrix has only 72 parameters, these 11,596 weights provide the mathematical capacity needed to "
            "capture the cubic non-linear core saturation across the entire operating domain."
        ),
        "script_kr": (
            "이 슬라이드는 해커톤에서 사용되는 신경망 대리 모델의 구체적인 구조도입니다. "
            "6개의 보정 전자석 전류를 입력받아 12개 BPM의 궤도 변위를 실시간 예측하는 R⁶ → R¹² 매핑 구조입니다. "
            "입력층은 6개의 수평/수직 스티어러 전류 [I₁, ..., I₆]를 받습니다. "
            "이 신호는 세 개의 밀집 은닉층을 거칩니다: 첫 번째 은닉층은 6개의 입력을 128개의 고차원 특징 공간으로 확장하고, "
            "두 번째 층은 64개로 압축하며, 세 번째 층은 32개로 정제합니다. 세 은닉층 모두 ReLU 활성화 함수를 사용합니다. "
            "마지막 출력층은 32개의 추상 특징을 12개 BPM 예측 변위값 [Ŷ₁, ..., Ŷ₁₂]으로 선형 투영합니다. "
            "이 네트워크의 총 학습 파라미터는 11,596개입니다. 선형 ORM 행렬이 단 72개의 파라미터만 갖는 것에 비해, 11,596개의 가중치는 "
            "3차 비선형 자기 포화 효과를 전 작동 영역에 걸쳐 정밀하게 학습할 수 있는 충분한 표현 용량을 제공합니다."
        ),
        "cues_en": "Contrast 72 parameters (linear ORM) with 11,596 parameters (MLP). Emphasize why parameter capacity is required for non-linear saturation.",
        "cues_kr": "선형 ORM의 72개 파라미터와 MLP의 11,596개 파라미터 용량을 대조하여 비선형성 포착 능력을 설명합니다.",
        "qa_en": "Q: Can we make the network smaller, say (32, 16)? A: Yes, in fact, a smaller tanh network can sometimes generalize better and evaluate faster.",
        "qa_kr": "Q: 은닉층을 (32, 16)처럼 더 작게 줄여도 되나요? A: 좋은 질문입니다. 실제로 적절히 설계된 작은 Tanh 신경망이 과적합 없이 더 빠르고 우수한 성능을 내기도 합니다.",
        "trans_en": "How well does this surrogate perform when tested on unseen validation data? Let us look at Slide 20.",
        "trans_kr": "그렇다면 이 신경망 대리 모델을 한 번도 본 적 없는 독립 검증 데이터에 평가했을 때 오차는 어느 정도일까요?"
    },
    {
        "num": 20,
        "category": "Paradigm 1: Supervised Learning",
        "title_en": "Surrogate Training & Holdout Validation",
        "title_kr": "대리 모델 훈련 및 독립 홀드아웃(Holdout) 검증 결과",
        "visual_en": "Empirical validation table: Linear Ridge (RMSE = 0.0960 mm) vs MLP Surrogate (RMSE = 0.0118 mm), approaching theoretical Gaussian noise floor (0.0100 mm).",
        "visual_kr": "검증 성능 비교표: 선형 릿지 모델(RMSE = 0.0960 mm) 대비 MLP 신경망 대리 모델(RMSE = 0.0118 mm), 가우시안 노이즈 바닥(0.0100 mm)에 근접.",
        "script_en": (
            "To prove that our neural surrogate has learned the true physics rather than memorizing noise, we perform holdout validation. "
            "We synthesize 1,500 offline shots sampled uniformly across [-3.0 A, +3.0 A]. We train on 1,200 shots and evaluate strictly on 300 isolated "
            "test shots. Look at the benchmark table. A regularized Linear Ridge model achieves a test RMSE of 0.0960 mm. It suffers from high bias: "
            "it cannot capture the cubic saturation falloff. In stark contrast, our MLP Neural Surrogate achieves an RMSE of 0.0118 mm! "
            "Remember from Slide 10 that our BPM sensors have an inherent Gaussian noise floor of 0.0100 mm (10 microns). "
            "The neural network has pushed the prediction error down to within 1.8 microns of the theoretical noise floor. "
            "It has learned the linear betatron response and the cubic non-linear core saturation without overfitting the sensor jitter."
        ),
        "script_kr": (
            "신경망 대리 모델이 노이즈를 암기한 것이 아니라 실제 물리 법칙을 학습했음을 검증하기 위해 엄밀한 홀드아웃(Holdout) 평가를 수행합니다. "
            "전류 범위 [-3.0A, +3.0A]에서 생성한 1,500개 샷 중 1,200개로 학습하고, 완전히 격리된 300개 테스트 샷으로 평가했습니다. "
            "비교표를 보시면, 선형 릿지(Ridge) 모델은 테스트 RMSE가 0.0960 mm에 달합니다. 3차 자기 포화를 선형 모델로는 전혀 설명할 수 없기 때문입니다. "
            "반면 MLP 신경망 대리 모델은 0.0118 mm의 뛰어난 테스트 RMSE를 달성했습니다! "
            "앞선 슬라이드에서 우리 BPM 센서의 본질적인 가우시안 노이즈 바닥이 0.0100 mm(10 ㎛)라고 말씀드렸습니다. "
            "신경망의 예측 오차가 이론적 노이즈 한계선에 불과 1.8 ㎛ 차이로 근접한 것입니다. "
            "이는 신경망이 센서 지터에 과적합되지 않으면서, 선형 궤도 응답과 3차 자기 포화 물리 효과를 거의 완벽히 학습했음을 입증합니다."
        ),
        "cues_en": "Emphasize the theoretical noise floor: 0.0118 mm vs 0.0100 mm. You cannot physically do better than 0.0100 mm without overfitting noise!",
        "cues_kr": "0.0118 mm와 센서 노이즈 바닥 0.0100 mm를 비교하며, 노이즈 바닥 이하로 오차를 줄이려는 시도는 과적합일 뿐임을 상기시킵니다.",
        "qa_en": "Q: Why is Ridge RMSE 0.096 mm so much worse? A: At 2.5 A, cubic saturation causes a 23% error that linear regression cannot resolve.",
        "qa_kr": "Q: 릿지 모델의 오차가 0.096 mm로 큰 이유는 무엇인가요? A: 2.5 A 부근에서 발생하는 23%의 3차 자기 포화 오차를 선형 모델로는 수용할 수 없기 때문입니다.",
        "trans_en": "Now that we have an accurate forward digital twin, how do we use it for closed-loop orbit control?",
        "trans_kr": "이제 정확한 순방향 디지털 트윈을 확보했습니다. 이를 폐루프 궤도 제어에 어떻게 활용하는지 살펴보겠습니다."
    },
    {
        "num": 21,
        "category": "Paradigm 1: Supervised Learning",
        "title_en": "Closed-Loop Control Architecture",
        "title_kr": "폐루프 제어 아키텍처 및 대리 모델 역산 흐름",
        "visual_en": "Closed-loop feedback schematic: Beamline Environment, BPM reading Y, Present current I, Digital Twin Inversion Optimizer, Action delta I, and closed-loop feedback.",
        "visual_kr": "폐루프 피드백 블록도: 가속기 전송선 환경, BPM 측정값 Y, 현재 누적 전류 I, 디지털 트윈 역산 최적화기, 제어 킥 ΔI, 폐루프 피드백 순환 구조.",
        "script_en": (
            "Here is the architecture of closed-loop orbit control. Notice the information flow. "
            "At step t, the beamline produces an observation vector Y in R^12 from the BPMs. The controller also reads the present total current "
            "vector I_t in R^6 from the environment metadata. This total current is vital: because saturation depends cubically on total current, "
            "you cannot calculate the correct incremental kick without knowing where you currently sit on the B-H curve! "
            "The controller passes Y and I_t into an inversion optimizer. Using the trained neural digital twin f_theta, the optimizer solves for "
            "the delta current action delta I in [-0.8 A, +0.8 A] that will cancel the residual orbit at step t+1. "
            "The action is applied to the power supplies, the magnets adjust, the beam deflects, and new BPM readings are measured. "
            "This cycle repeats until the orbit RMS drops below 0.030 mm."
        ),
        "script_kr": (
            "이 다이어그램은 폐루프 궤도 제어 시스템의 전체 정보 흐름을 보여줍니다. "
            "스텝 t에서 빔라인 BPM 센서로부터 12차원 관측 궤도 Y가 측정됩니다. 이때 제어기는 환경 메타데이터로부터 현재 전자석들에 인가되어 있는 "
            "누적 전류 벡터 I_t(R⁶)를 함께 읽어옵니다. 이 현재 전류 정보는 대단히 중요합니다! 자기 포화는 누적 전류의 3승에 비례하므로, 현재 자신이 "
            "B-H 곡선의 어느 지점에 위치해 있는지를 알지 못하면 올바른 증분 킥(ΔI)을 계산할 수 없습니다. "
            "제어기는 관측 궤도 Y와 현재 전류 I_t를 모델 역산 최적화기에 입력합니다. 학습된 신경망 디지털 트윈 f_θ를 활용하여, 다음 스텝 t+1에서 "
            "잔여 궤도를 0으로 상쇄시킬 수 있는 최적의 델타 전류 ΔI ∈ [-0.8A, 0.8A]를 계산합니다. "
            "이 킥이 전원 장치에 인가되면 자장이 변경되고, 빔이 편향되어 새로운 BPM 측정값이 관측됩니다. 이 폐루프 루틴은 궤도 RMS 오차가 "
            "목표치인 0.030 mm 이하로 떨어질 때까지 반복됩니다."
        ),
        "cues_en": "Stress the importance of reading info['currents']! Without total current I_t, compensating saturation is impossible.",
        "cues_kr": "환경의 info['currents']로부터 현재 누적 전류를 읽어오는 것이 포화 보상의 핵심 열쇠임을 힘주어 설명합니다.",
        "qa_en": "Q: What if we don't track total current? A: The policy assumes it's always near 0 A, under-correcting severely at high currents.",
        "qa_kr": "Q: 현재 전류를 추적하지 않으면 어떻게 되나요? A: 항상 0A 부근의 선형 영역에 있다고 착각하여, 고전류 포화 영역에서 킥을 크게 과소평가하게 됩니다.",
        "trans_en": "Let us contrast this with the classical approach used in accelerators for decades: Baseline 0 SVD.",
        "trans_kr": "이제 수십 년간 가속기 제어의 표준으로 군림해 온 고전 선형 SVD 제어 방식(Baseline 0)과 비교해보겠습니다."
    },
    {
        "num": 22,
        "category": "Baseline 0: Classical Linear SVD",
        "title_en": "Baseline 0: Classical Linear SVD",
        "title_kr": "베이스라인 0: 고전적 선형 SVD 의사역행렬 제어기",
        "visual_en": "SVD decomposition R^T = U Sigma V^T, Moore-Penrose pseudo-inverse (R^T)^dagger, feedback formula delta I = - alpha * (R^T)^dagger * Y, gain alpha tuning.",
        "visual_kr": "응답행렬 특이값 분해 Rᵀ = UΣVᵀ, 무어-펜로즈 의사역행렬 (Rᵀ)†, 피드백 수식 ΔI = -α·(Rᵀ)†·Y, 피드백 게인 α에 따른 수렴 속도 비교.",
        "script_en": (
            "Baseline 0 represents classical accelerator orbit correction: Moore-Penrose pseudo-inverse control via Singular Value Decomposition (SVD). "
            "Under an idealized linear model, orbit shift is Y = Delta I times R. Transposing gives R^T Delta I = Y. Because R^T is a 12 by 6 matrix, "
            "it has more rows than columns. We decompose R^T using SVD: R^T = U Sigma V^T, and compute the pseudo-inverse: (R^T)^dagger = V Sigma^-1 U^T. "
            "The correction law is: delta I = - alpha times (R^T)^dagger times Y. "
            "With the conservative default gain alpha = 0.45, this controller converges robustly on all 30 seeds, achieving a 100% success rate. "
            "However, because it has zero awareness of cubic saturation, it under-corrects at high currents and takes an average of 9.4 steps to converge, "
            "earning a benchmark score of 674.398 points. If you tune the gain alpha up to 1.2, it accelerates to about 3.7 steps, but higher gains "
            "cause severe overshoots and limit-cycle oscillations around the noise floor."
        ),
        "script_kr": (
            "베이스라인 0은 전통적인 가속기 궤도 보정의 표준인 '특이값 분해(SVD) 기반 무어-펜로즈 의사역행렬 제어기'입니다. "
            "이상적인 선형 모델에서 궤도 변위는 Y = ΔI · R로 표현되며, 전치하면 Rᵀ·ΔI = Y가 됩니다. Rᵀ은 12×6 행렬이므로 행이 열보다 많은 "
            "과결정 시스템입니다. SVD 분해 Rᵀ = UΣVᵀ를 통해 의사역행렬 (Rᵀ)† = VΣ⁻¹Uᵀ를 계산하고, 비례 게인 α를 곱해 제어 킥을 인가합니다: "
            "ΔI = -α · (Rᵀ)† · Y. 기본 보수적 게인 α = 0.45를 적용하면 30개 시드 전체에서 안정적으로 100% 성공률을 달성합니다. "
            "하지만 이 제어기는 3차 자기 포화를 전혀 알지 못하므로, 고전류 영역에서 킥을 계속 과소평가하여 수렴까지 평균 9.4스텝이나 소요되며 "
            "공식 벤치마크 점수는 674.398점에 머무릅니다. 게인을 α = 1.2 수준으로 높이면 약 3.7스텝까지 단축할 수 있지만, 게인이 너무 커지면 "
            "오버슈트와 목표 경계면에서의 진동 위험이 급격히 증가합니다."
        ),
        "cues_en": "Explain the gain trade-off: alpha=0.45 is safe but slow (9.4 steps); alpha=1.2 is fast (3.7 steps) but risks instability.",
        "cues_kr": "게인 트레이드오프를 설명합니다: α=0.45는 안전하지만 9.4스텝으로 느리고, α=1.2는 3.7스텝으로 빠르지만 오버슈트 위험이 있습니다.",
        "qa_en": "Q: Why is R transposed? A: Because our convention defines Y as row vector (1x12) and currents as (1x6): Y = I * R.",
        "qa_kr": "Q: 왜 R을 전치(transpose)하여 역행렬을 구하나요? A: 수식 정의상 Y가 (1×12) 행 벡터이고 전류 I가 (1×6) 행 벡터이므로(Y = I·R), 전치해야 올바른 차원이 맞습니다.",
        "trans_en": "Now let us see what happens when we replace linear SVD with our non-linear neural surrogate: Baseline 1.",
        "trans_kr": "그렇다면 선형 SVD 대신 우리가 학습시킨 비선형 신경망 대리 모델을 역산에 적용하면 어떤 결과가 나올까요? 베이스라인 1을 살펴보겠습니다."
    },
    {
        "num": 23,
        "category": "Baseline 1 (Track 1)",
        "title_en": "Baseline 1 (Track 1): Supervised Neural Inversion",
        "title_kr": "베이스라인 1 (트랙 1): 딥러닝 대리 모델 역산 최적화",
        "visual_en": "Mathematical objective for model inversion: min_{Delta I} || Y - f_theta(I) + f_theta(I + Delta I) ||^2 + lambda || Delta I ||^2, L-BFGS-B solver, and 4.0 step convergence.",
        "visual_kr": "모델 역산 목적함수 수식: 잔여 궤도 최소화 및 액추에이터 페널티 정규화, SciPy L-BFGS-B 솔버, 평균 4.0스텝 수렴(779.169점).",
        "script_en": (
            "Baseline 1 is the core controller for Track 1: model-based optimization via digital twin inversion. "
            "At each time step, instead of using a constant linear matrix, we formulate an online optimization problem using our trained MLP: "
            "minimize over delta I the norm of Y minus f_theta(I) plus f_theta(I + delta I) squared, plus lambda times the action norm squared. "
            "Notice the formulation: f_theta(I + delta I) minus f_theta(I) is the predicted orbit change. Adding it to the current BPM observation Y "
            "yields the exact predicted orbit at the next step. Because f_theta captures the cubic saturation, the optimizer knows exactly how much "
            "extra current is required to overcome magnetic saturation. We solve this 6-dimensional optimization problem per step in about 15 milliseconds "
            "using SciPy's L-BFGS-B algorithm, enforcing the [-0.8 A, +0.8 A] delta bounds. "
            "Baseline 1 converges in an average of 4.0 steps on test seed 42 and across all 30 seeds, earning 779.169 points—more than 100 points higher than SVD!"
        ),
        "script_kr": (
            "베이스라인 1은 해커톤 트랙 1의 핵심인 '디지털 트윈 역산 기반 모델 최적화 제어기'입니다. "
            "매 스텝마다 고정된 선형 행렬 대신, 우리가 사전에 학습시킨 MLP 대리 모델을 활용하여 다음과 같은 최적화 문제를 풉니다: "
            "min_{ΔI} || Y - f_θ(I) + f_θ(I + ΔI) ||² + λ ||ΔI||². "
            "이 수식의 의미를 보십시오: f_θ(I + ΔI) - f_θ(I)는 델타 킥 ΔI에 의해 유도될 궤도 변화량을 의미하며, 현재 관측값 Y에 더해주면 "
            "다음 스텝의 '예측 잔여 궤도'가 됩니다. 대리 모델 f_θ가 3차 자기 포화를 정확히 알고 있기 때문에, 포화를 극복하기 위해 전류를 얼마나 "
            "더 주어야 하는지 최적화 알고리즘이 스스로 계산해냅니다. SciPy의 L-BFGS-B 솔버를 사용하여 [-0.8A, 0.8A] 경계 내에서 단 15밀리초 만에 "
            "해를 구합니다. 그 결과 평균 4.0스텝 만에 목표치에 완벽히 안착하며, 779.169점을 기록하여 고전 SVD보다 무려 100점 이상 높은 점수를 획득합니다!"
        ),
        "cues_en": "Point out the score leap: from 674.398 (SVD) to 779.169 (Baseline 1). The 100-point jump comes purely from anticipating cubic saturation.",
        "cues_kr": "674점에서 779점으로의 100점 이상 비약적인 점수 상승을 언급하며, 비선형 포화를 예측하는 모델의 위력을 실감케 합니다.",
        "qa_en": "Q: Can we score higher than 779 in Track 1? A: Yes! In TODO 1, training a more accurate surrogate (e.g. tanh with lbfgs) scores over 924 points!",
        "qa_kr": "Q: 트랙 1에서 779점보다 더 높은 점수를 낼 수 있나요? A: 네! TODO 1에서 대리 모델 정밀도를 높이면(예: Tanh 신경망) 924점 이상을 달성할 수 있습니다.",
        "trans_en": "Now let us shift to Paradigm 2: Reinforcement Learning and adaptive closed-loop policies.",
        "trans_kr": "이어서 최적화 역산 대신 실시간 피드백 정책을 학습하는 두 번째 패러다임, 강화학습(Reinforcement Learning)으로 넘어가겠습니다."
    },
    {
        "num": 24,
        "category": "Paradigm 2: Reinforcement Learning",
        "title_en": "Reinforcement Learning: MDP Formulation & Hyperparameters",
        "title_kr": "강화학습: 마르코프 결정 과정(MDP) 정식화 및 하이퍼파라미터",
        "visual_en": "Left column: Closed-loop MDP formulation (S, A, P, R, gamma), reward function formula, cumulative return J(theta). Right column: RL hyperparameter taxonomy table (TODO 2).",
        "visual_kr": "좌측: 폐루프 MDP 프레임워크(상태, 행동, 전이, 보상 함수, 할인율), 누적 보상 J(θ). 우측: 참가자 튜닝 변수(TODO 2)가 강조된 RL 하이퍼파라미터 분류표.",
        "script_en": (
            "Reinforcement Learning treats orbit correction as a sequential decision-making problem formalized as a Markov Decision Process (MDP). "
            "On the left, the State Space S is the 12-dimensional BPM reading vector Y. The Action Space A is the 6-dimensional steerer delta kick vector "
            "in [-0.8 A, +0.8 A]^6. The Transition Dynamics P embody the accelerator transport physics, magnet core saturation, and sensor noise. "
            "The Reward Function R is engineered to reflect real operational priorities: r_t = - w_rms * RMS_(t+1) - w_act * ||a_t||^2 - c_step + b_term. "
            "Notice the components: a penalty on orbit RMS, a penalty on coil heating, a step penalty c_step incentivizing speed, and a terminal bonus for success. "
            "On the right, we highlight the hyperparameters you can tune in notebook TODO 2: the discount factor gamma (0.95 to 0.99), the policy learning rate, "
            "the harmonic damping parameter kappa, the reward weights w_rms and w_act, and the step penalty c_step."
        ),
        "script_kr": (
            "강화학습(RL)은 궤도 보정을 마르코프 결정 과정(MDP) 기반의 순차적 의사결정 문제로 다룹니다. "
            "좌측을 보시면, 상태 공간 S는 12개 BPM의 변위 측정값 Y입니다. 행동 공간 A는 6개 스티어러에 인가할 전류 증분 ΔI ∈ [-0.8A, 0.8A]⁶입니다. "
            "전이 확률 P는 가속기 빔 물리, 자기 포화, 센서 노이즈가 결합된 환경 동역학입니다. "
            "보상 함수 R은 가속기 운전 목표를 정밀하게 반영합니다: r_t = - w_rms·RMS_{t+1} - w_act·||a_t||² - c_step + b_term. "
            "잔여 궤도 오차 페널티, 코일 발열 억제를 위한 액션 페널티, 빠른 수렴을 유도하는 스텝 페널티(c_step), 그리고 목표 달성 보너스(b_term)로 구성됩니다. "
            "우측 표에는 노트북 TODO 2에서 수정 가능한 변수들이 정리되어 있습니다: 할인율 γ(0.95~0.99), 정책 학습률, 하모닉 댐핑 계수 κ, "
            "보상 가중치(w_rms, w_act), 스텝 페널티(c_step) 등이 포함됩니다."
        ),
        "cues_en": "Explain the step penalty c_step: it forces the agent to finish in as few steps as possible to maximize hackathon speed points.",
        "cues_kr": "스텝 페널티(c_step)의 역할을 강조합니다: 매 스텝마다 감점을 부여함으로써 에이전트가 최소 스텝으로 수렴하도록 유도합니다.",
        "qa_en": "Q: Why is gamma < 1 needed in finite episodes? A: Gamma discounts distant rewards, ensuring temporal credit assignment focuses on immediate corrections.",
        "qa_kr": "Q: 유한한 에피소드에서도 할인율 γ < 1이 필요한가요? A: 네, 미래 보상을 적절히 할인함으로써 당장 궤도를 줄이는 즉각적 행동에 높은 가중치를 부여하기 위함입니다.",
        "trans_en": "How do we structure an RL agent that learns quickly without destroying the beam? Track 2: Physics Priors.",
        "trans_kr": "그렇다면 위험한 무작위 탐색 없이, 안정적이면서도 빠르게 동작하는 강화학습 제어기를 어떻게 구성할 수 있을까요? 트랙 2를 보시겠습니다."
    },
    {
        "num": 25,
        "category": "Track 2 Challenge",
        "title_en": "Track 2: Closed-Loop RL with Physics Priors",
        "title_kr": "트랙 2: 물리 사전 지식 결합 폐루프 강화학습 정책",
        "visual_en": "Physics-informed residual policy architecture: Delta I = gamma(t) * [ - alpha * (R^T)^dagger * Y + W_learned * Y + b ], analytical prior + learned residual.",
        "visual_kr": "물리 사전 지식 기반 잔차 정책 구조도: ΔI = γ(t)·[ -α·(Rᵀ)†·Y + W_learned·Y + b ], 해석적 선형 사전 지식과 학습된 비선형 보정 잔차의 결합.",
        "script_en": (
            "Training an RL agent from pure scratch (tabula rasa) on an accelerator is dangerous and sample-inefficient: the agent would apply random "
            "kicks and lose the beam. Track 2 solves this by deploying a Physics-Informed Residual Policy Architecture. "
            "Look at the control equation: delta I(t) = gamma(t) times the sum of an Analytical Physics Prior and a Learned Residual Offset: "
            "delta I = gamma(t) [ - alpha (R^T)^dagger Y + W_learned Y + b ]. "
            "The analytical prior is our trusted SVD pseudo-inverse: it immediately handles 80 percent of the correction using known beam optics. "
            "The learned residual—governed by weight matrix W_learned and bias b—only needs to learn the missing non-linear physics: the cubic core saturation! "
            "In the unmodified baseline agent, W_learned and b start at zero, so it acts purely as a damped SVD controller scoring 590.559 points. "
            "Your challenge in Track 2 is to train or tune this residual to anticipate saturation, enabling lightning-fast sub-millisecond policy execution."
        ),
        "script_kr": (
            "가속기 환경에서 아무런 사전 지식 없이 바닥부터(tabula rasa) 강화학습을 수행하면, 초기에 무작위 킥을 인가하여 빔이 챔버에 충돌하게 됩니다. "
            "트랙 2에서는 이를 해결하기 위해 '물리 사전 지식 결합 잔차 정책(Physics-Informed Residual Policy)'을 도입했습니다. "
            "제어 방정식을 보십시오: ΔI(t) = γ(t) · [ -α·(Rᵀ)†·Y + W_learned·Y + b ]. "
            "앞부분의 해석적 물리 사전 지식은 우리가 잘 알고 있는 SVD 의사역행렬입니다. 전체 궤도 보정의 80% 이상을 즉각적이고 안정적으로 처리합니다. "
            "뒷부분의 학습된 잔차(W_learned, b)는 선형 모델이 설명하지 못하는 '3차 자기 포화 왜곡'만을 전담하여 학습합니다! "
            "기본 제공되는 기준 제어기에서는 W_learned와 b가 0으로 초기화되어 있어 단순 감쇠 SVD로 동작하며 590.559점을 기록합니다. "
            "트랙 2에서 참가자 여러분의 과제는 이 잔차 파라미터를 학습시키거나 보정하여 비선형 포화를 완벽히 극복하는 고성능 정책을 완성하는 것입니다."
        ),
        "cues_en": "Emphasize why residual learning is powerful: learning a delta around a good physical prior is 100x faster than learning from scratch.",
        "cues_kr": "우수한 물리 사전 지식 주변의 '잔차(residual)'만을 학습하는 기법이 바닥부터 학습하는 것보다 100배 이상 빠르고 안전함을 설명합니다.",
        "qa_en": "Q: Can we replace the linear SVD prior with a non-linear inverse? A: Absolutely! In the solution notebook, an exact inverse prior scores 939.981 points!",
        "qa_kr": "Q: 선형 SVD 대신 비선형 역산 모델을 사전 지식으로 교체해도 되나요? A: 완벽한 전략입니다! 주최 측 솔루션에서는 포화 보상 사전 지식을 적용하여 939.981점을 달성했습니다.",
        "trans_en": "Notice the gamma(t) term in front of the policy. What is its mathematical role? Let us look at Slide 26.",
        "trans_kr": "정책 수식 맨 앞에 곱해진 감쇠 계수 γ(t)는 과연 어떤 역할을 수행할까요? 슬라이드 26에서 그 비밀을 밝혀보겠습니다."
    },
    {
        "num": 26,
        "category": "Track 2 Challenge",
        "title_en": "Dynamic Harmonic Step Damping",
        "title_kr": "동적 조화 스텝 감쇠(Dynamic Harmonic Step Damping)",
        "visual_en": "Damping schedule formula gamma(t) = 1.0 / (1.0 + kappa * t), decay curve from 1.0 down to 0.4, and phase-space portrait showing suppression of limit-cycle oscillations.",
        "visual_kr": "감쇠 스케줄 수식 γ(t) = 1.0 / (1.0 + κ·t), 1.0에서 0.4로 완만히 감소하는 감쇠 곡선, 10 ㎛ 노이즈 경계면에서의 리미트 사이클 진동 억제 궤적도.",
        "script_en": (
            "When high-gain closed-loop policies approach the target convergence boundary (RMS < 0.030 mm), a dangerous instability emerges: "
            "sensor noise amplification. Remember that our BPMs have a 10-micron Gaussian jitter. A controller with constant high feedback gain "
            "will interpret sensor noise as a real orbit error, apply sharp corrector kicks, and bounce back and forth across the 30-micron target boundary "
            "in an endless limit-cycle oscillation. To eliminate this terminal oscillation, Track 2 incorporates Dynamic Harmonic Step Damping: "
            "gamma(t) = 1.0 / ( 1.0 + kappa * t ), with default kappa = 0.03. "
            "At step 0, gamma is exactly 1.0, giving full control authority to make large multi-millimeter corrections. As step t increases, "
            "gamma decays smoothly—reaching about 0.7 by step 10 and 0.5 by step 30. This progressively dampens high-frequency jitter amplification, "
            "allowing the beam orbit to land softly and permanently below the 30-micron target."
        ),
        "script_kr": (
            "고이득 폐루프 제어기가 목표 수렴 경계면(RMS < 0.030 mm) 부근에 도달했을 때 가장 흔히 겪는 문제는 '센서 노이즈 증폭으로 인한 발진'입니다. "
            "BPM 센서에는 10 ㎛의 가우시안 지터가 존재합니다. 고정된 높은 게인을 유지하는 제어기는 이 측정 노이즈를 실제 궤도 오차로 오인하여 "
            "불필요한 과도 킥을 인가하게 되며, 결과적으로 30 ㎛ 경계면을 넘나들며 끝없이 요동치는 리미트 사이클(limit-cycle)에 빠지게 됩니다. "
            "이러한 종단 진동을 원천 차단하기 위해 도입된 기법이 '동적 조화 스텝 감쇠(Dynamic Harmonic Step Damping)'입니다: "
            "γ(t) = 1.0 / (1.0 + κ·t), 기본 감쇠 계수 κ = 0.03. "
            "스텝 t = 0일 때는 γ = 1.0으로 최대 제어 권한을 발휘하여 초기 수 밀리미터의 왜곡을 단숨에 줄입니다. "
            "스텝이 진행됨에 따라 제어 권한이 완만하게 감소하여(10스텝 시 약 0.7, 30스텝 시 약 0.5), 고주파 노이즈 반응을 부드럽게 억제하고 "
            "30 ㎛ 목표 영역 내에 궤도가 안정적으로 안착하도록 만듭니다."
        ),
        "cues_en": "Explain why constant gain fails near the boundary: high gain chases 10 um noise, exceeding 30 um threshold. Damping solves this.",
        "cues_kr": "고정 게인이 왜 실패하는지 설명합니다: 10 ㎛ 노이즈를 쫓아가다 30 ㎛ 목표치를 초과하게 되며, 감쇠 기법이 이를 해결함을 역설합니다.",
        "qa_en": "Q: What happens if kappa is too large, say 0.2? A: Control authority decays too quickly, freezing the orbit before reaching 0.030 mm.",
        "qa_kr": "Q: κ 값이 0.2처럼 너무 크면 어떻게 되나요? A: 제어 권한이 너무 일찍 소진되어, 0.030 mm 목표선에 도달하기도 전에 전류 변경이 멈추게 됩니다.",
        "trans_en": "Now let us turn to our third paradigm: Bayesian Optimization and Gaussian Processes.",
        "trans_kr": "이제 세 번째 패러다임이자 샘플 효율성의 정점인 가우시안 프로세스 기반 베이지안 최적화(트랙 3)를 살펴보겠습니다."
    },
    {
        "num": 27,
        "category": "Paradigm 3: Bayesian Optimization",
        "title_en": "Bayesian Optimization: Probabilistic GPs & Hyperparameters",
        "title_kr": "베이지안 최적화: 확률론적 가우시안 프로세스(GP) 및 하이퍼파라미터",
        "visual_en": "Left column: 4-step BO workflow (Non-parametric prior, Gaussian conditioning, Acquisition optimization, Beamline evaluation). Right column: BO hyperparameter table (TODO 3).",
        "visual_kr": "좌측: 베이지안 최적화 4단계 흐름(비모수 사전분포, 사후 조건부 분포 도출, 획득함수 최적화, 빔라인 측정 갱신). 우측: 참가자 튜닝 변수(TODO 3)가 강조된 BO 하이퍼파라미터 분류표.",
        "script_en": (
            "Bayesian Optimization is the premier paradigm for sample-efficient black-box tuning. Unlike neural networks that require thousands "
            "of shots, Gaussian Processes model physical functions from dozens of shots while providing rigorous epistemic uncertainty. "
            "On the left, the four-step workflow unfolds: Step 1 establishes a non-parametric GP prior f(x) ~ GP( m(x), k(x, x') + sigma_n^2 ). "
            "Step 2 performs analytical Gaussian conditioning on observed shots D_t, yielding an exact posterior mean mu(x) and uncertainty sigma(x). "
            "Step 3 optimizes an acquisition function, such as Lower Confidence Bound (LCB), balancing exploitation (minimizing mu) against exploration "
            "(sampling high sigma). Step 4 queries the physical beamline and refits the model. "
            "On the right, we present the hyperparameter taxonomy for notebook TODO 3: the covariance kernel (Matérn-5/2), actuator lengthscales ell, "
            "signal variance sigma_f^2, the fixed noise floor sigma_n = 0.010 mm, the exploration trade-off kappa, and regularizer lambda."
        ),
        "script_kr": (
            "베이지안 최적화(BO)는 샘플 효율성이 극대화된 블랙박스 최적화 기법입니다. 수천 개의 데이터가 필요한 신경망과 달리, "
            "가우시안 프로세스(GP)는 수십 개의 샷만으로도 물리 함수를 정확히 모델링하며 각 지점의 '불확실성(uncertainty)'을 정량적으로 제공합니다. "
            "좌측의 4단계 워크플로우를 보십시오: 1단계에서는 비모수적 GP 사전분포 f(x) ~ GP(m, k + σ_n²)를 설정합니다. "
            "2단계에서는 측정된 데이터셋 D_t에 대한 조건부 확률을 해석적으로 계산하여 예측 평균 μ(x)과 불확실성 σ(x)을 도출합니다. "
            "3단계에서는 하한 신뢰 구간(LCB) 획득 함수를 최적화하여 탐색(exploration)과 활용(exploitation)의 균형점을 찾습니다. "
            "4단계에서는 도출된 최적 킥을 빔라인에 인가하고 데이터를 갱신합니다. "
            "우측 표에는 노트북 TODO 3에서 튜닝할 수 있는 변수들이 정리되어 있습니다: 마테른(Matérn-5/2) 커널, 자석별 상관 길이(lengthscale) ℓ, "
            "신호 분산 σ_f², 고정 노이즈 바닥 σ_n = 0.010 mm, 탐색 파라미터 κ, 정규화 계수 λ 등이 포함됩니다."
        ),
        "cues_en": "Point out Noise Variance sigma_n = 0.010 mm is FIXED! Emphasize that modifying this sensor noise breaks the benchmark boundary.",
        "cues_kr": "노이즈 분산 σ_n = 0.010 mm는 물리적 센서 특성이므로 절대 수정해서는 안 되는 고정 파라미터임을 명시합니다.",
        "qa_en": "Q: Why Matérn-5/2 instead of RBF? A: RBF assumes infinitely differentiable curves (too smooth); Matérn-5/2 matches realistic physical magnetic saturation.",
        "qa_kr": "Q: 왜 RBF 커널 대신 Matérn-5/2를 쓰나요? A: RBF는 무한 번 미분 가능한 비현실적인 매끄러움을 가정하지만, Matérn-5/2는 2회 미분 가능하여 실제 전자석 포화 특성에 완벽히 부합합니다.",
        "trans_en": "How does this GP model operate inside our closed-loop challenge? Let us examine Track 3 on Slide 28.",
        "trans_kr": "이 가우시안 프로세스 모델이 해커톤 트랙 3 폐루프 제어기 내부에서 어떻게 구동되는지 살펴보겠습니다."
    },
    {
        "num": 28,
        "category": "Track 3 Challenge",
        "title_en": "Track 3: Closed-Loop Bayesian Optimization",
        "title_kr": "트랙 3: 가우시안 프로세스 기반 폐루프 베이지안 최적화",
        "visual_en": "Track 3 controller architecture, calibration on 300 offline shots, step-by-step closed-loop execution, and opportunity for true online GP refitting via callbacks.",
        "visual_kr": "트랙 3 제어기 아키텍처, 300회 오프라인 샷 기반 GP 캘리브레이션, 폐루프 스텝별 LCB 최적화, 콜백을 활용한 실시간 온라인 GP 갱신 확장성.",
        "script_en": (
            "Here is how Track 3 operates. In the reference implementation, a GaussianProcessRegressor with a Matérn-5/2 kernel is fitted offline "
            "on 300 calibration shots across [-3.5 A, +3.5 A]. At each time step on the physical beamline, the controller reads the current BPM readings Y "
            "and present total current I_t. It queries the GP surrogate to predict the mean orbit change and the epistemic uncertainty for candidate kicks delta I. "
            "It solves for the delta I that minimizes the Lower Confidence Bound acquisition function under [-0.8 A, +0.8 A] bounds. "
            "Notice a crucial operational insight: like Baseline 1, the reference Track 3 controller is closed-loop (it re-solves from the latest BPM reading), "
            "but its GP model is fitted once and kept fixed. Participants who register a step_callback in the notebook can add each new (current, orbit) "
            "measurement to the GP dataset and refit it online, turning Track 3 into true active online Bayesian optimization!"
        ),
        "script_kr": (
            "트랙 3 제어기의 구동 원리입니다. 기준 코드에서는 [-3.5A, +3.5A] 범위에서 수집된 300개의 캘리브레이션 샷으로 Matérn-5/2 커널 GP를 사전 학습시킵니다. "
            "매 스텝마다 제어기는 최신 BPM 관측값 Y와 현재 누적 전류 I_t를 전달받습니다. 대리 모델을 통해 후보 킥 ΔI에 대한 예측 평균 궤도와 "
            "불확실성을 계산하고, LCB 획득 함수를 최소화하는 최적의 델타 전류를 도출합니다. "
            "여기서 매우 중요한 실무적 포인트를 짚어드립니다: 기준 코드의 트랙 3 제어기는 매 스텝 최신 측정값으로부터 최적화를 다시 풀기 때문에 "
            "'폐루프(closed-loop)' 제어기이지만, GP 모델 자체는 사전에 고정된 오프라인 모델입니다. 참가자 여러분께서 노트북의 CALLBACKS 딕셔너리에 "
            "step_callback을 등록하여 매 스텝 획득한 새로운 측정값을 GP에 실시간 추가하고 재학습(refit)시킨다면, 진정한 '온라인 실시간 베이지안 최적화'로 "
            "업그레이드할 수 있습니다!"
        ),
        "cues_en": "Clarify: closed-loop control vs online model updating. Emphasize the callback opportunity for participants seeking maximum scores.",
        "cues_kr": "폐루프 제어와 온라인 모델 갱신의 차이를 명확히 구분해주고, 콜백을 활용한 온라인 GP 갱신이 고득점의 비결임을 귀띔합니다.",
        "qa_en": "Q: Does online GP refitting slow down execution? A: Yes, GP fitting scales O(N^3) with sample size N, so keep the online buffer small (e.g., 50 shots).",
        "qa_kr": "Q: 실시간으로 GP를 재학습하면 속도가 너무 느려지지 않나요? A: 맞습니다. GP 연산량은 데이터 수의 3승(O(N³))에 비례하므로, 최근 50개 정도의 슬라이딩 윈도우 버퍼만 유지하는 것이 좋습니다.",
        "trans_en": "Let us examine the exact mathematical formulation of the Lower Confidence Bound acquisition function.",
        "trans_kr": "그렇다면 트랙 3의 핵심 의사결정 수식인 하한 신뢰 구간(LCB) 획득 함수를 자세히 살펴보겠습니다."
    },
    {
        "num": 29,
        "category": "Track 3 Challenge",
        "title_en": "Lower Confidence Bound Acquisition",
        "title_kr": "하한 신뢰 구간(Lower Confidence Bound, LCB) 획득 함수",
        "visual_en": "LCB acquisition formula: alpha_LCB(Delta I) = RMS( Y - mu(I) + mu(I + Delta I) ) - kappa * sigma_bar(Delta I) + lambda * || Delta I ||^2, exploitation vs exploration.",
        "visual_kr": "LCB 획득 함수 수식: 예측 RMS 잔여 오차(활용) - κ·불확실성(탐색) + λ·액션 페널티, 탐색 계수 κ = 0일 때의 3.6스텝 초고속 수렴 성과.",
        "script_en": (
            "The decision engine of Track 3 is the Lower Confidence Bound (LCB) acquisition function: "
            "alpha_LCB(delta I) = RMS of predicted next orbit, minus kappa times the mean predicted uncertainty sigma_bar, plus lambda times ||delta I||^2. "
            "The first term represents exploitation: driving the predicted orbit error down to zero. The second term represents exploration: "
            "subtracting uncertainty encourages the algorithm to probe actuator current regions where the model is unconfident, such as deep non-linear saturation. "
            "The trade-off parameter kappa governs this balance. In our benchmark, because our GP surrogate was already well-calibrated on 300 offline shots, "
            "setting kappa = 0—pure exploitation of the accurate mean—converges in an extraordinary average of just 3.6 steps! "
            "It earns 878.384 points, making Track 3 the reigning Rank 1 controller on our official leaderboard."
        ),
        "script_kr": (
            "트랙 3의 핵심 의사결정 수식인 하한 신뢰 구간(LCB) 획득 함수입니다: "
            "α_LCB(ΔI) = RMS(예측 다음 궤도) - κ · σ̄(불확실성) + λ · ||ΔI||². "
            "첫 번째 항은 '활용(exploitation)'으로, 예측 잔여 궤도 오차를 0으로 줄이는 역할을 합니다. 두 번째 항은 '탐색(exploration)'으로, "
            "불확실성이 높은 미지의 자장 영역을 탐색하도록 장려합니다. 탐색 가중치 κ가 이 둘의 균형을 결정합니다. "
            "주목할 점은, 우리 해커톤 환경에서는 사전 300회 샷을 통해 GP 모델이 이미 매우 정밀하게 보정되어 있다는 사실입니다. "
            "따라서 κ = 0으로 설정하여 사후 평균만을 순수하게 활용(pure exploitation)했을 때, 전체 30개 시드에서 평균 단 3.6스텝 만에 "
            "목표치에 안착하는 놀라운 속도를 기록했습니다! 공식 점수 878.384점을 획득하며 현재 벤치마크 랭킹 1위를 차지하고 있습니다."
        ),
        "cues_en": "Highlight the 3.6 step convergence: near the physical 3-step limit imposed by the 0.8 A slew rate! Rank 1 performance.",
        "cues_kr": "0.8A 슬루레이트 한계가 부과하는 이론적 최소 스텝(3스텝)에 거의 도달한 3.6스텝의 경이적인 수렴 속도를 강조합니다.",
        "qa_en": "Q: When should kappa > 0 be used? A: When entering unmapped lattice regimes or when magnetic drift occurs online.",
        "qa_kr": "Q: κ > 0 탐색이 필요한 경우는 언제인가요? A: 사전에 캘리브레이션되지 않은 낯선 자장 영역으로 진입하거나 미지의 드리프트가 발생했을 때 필수적입니다.",
        "trans_en": "Now let us examine the formal Gymnasium software contract governing your code in this afternoon's challenge.",
        "trans_kr": "이제 오늘 오후 여러분이 직접 코딩하게 될 Gymnasium 표준 시뮬레이션 환경 규격을 살펴보겠습니다."
    },
    {
        "num": 30,
        "category": "Gymnasium Environment Contract",
        "title_en": "Gymnasium Environment Contract",
        "title_kr": "체육관(Gymnasium) 환경 API 표준 규격",
        "visual_en": "Standard Gym interface: env.reset(seed) -> (obs, info) and env.step(action) -> (obs, reward, terminated, truncated, info), BenchmarkController act() contract.",
        "visual_kr": "표준 Gymnasium API 인터페이스: reset(seed) 및 step(action) 입출력 명세, BenchmarkController.act(obs, info) 표준 클래스 규약.",
        "script_en": (
            "To ensure scientific reproducibility, our simulation environment AcceleratorOrbitGymEnv adheres strictly to Farama Gymnasium standards. "
            "The environment provides two core methods. First, reset(seed): it resets all corrector currents to zero, applies random distortion kicks "
            "Y_0 drawn from the seed, and returns the initial 12-element BPM observation vector obs and an info dictionary containing runtime metadata. "
            "Second, step(action): it accepts a 6-element delta current array, clips it to [-0.8 A, +0.8 A], updates total currents, and computes the new orbit. "
            "It returns five outputs: the new observation obs; the scalar training reward; terminated, which triggers when RMS drops below 0.030 mm (success!); "
            "truncated, which triggers if step count reaches 50 without success (failure!); and the updated info dictionary. "
            "Every competitor controller must inherit from BenchmarkController and implement the standard act(obs, info) method returning a 6-element action."
        ),
        "script_kr": (
            "벤치마크의 학술적 엄밀성과 재현성을 위해, 시뮬레이션 환경 AcceleratorOrbitGymEnv는 글로벌 표준인 Farama Gymnasium API를 엄격히 준수합니다. "
            "환경은 두 가지 핵심 메서드를 제공합니다. 첫째, reset(seed): 모든 스티어러 전류를 0으로 리셋하고 해당 시드의 초기 왜곡 Y₀를 인가한 뒤, "
            "초기 12차원 BPM 관측값(obs)과 런타임 메타데이터가 담긴 info 딕셔너리를 반환합니다. "
            "둘째, step(action): 6차원 델타 전류 액션을 받아 [-0.8A, 0.8A]로 클리핑한 후 환경을 전진시킵니다. "
            "반환값은 5가지입니다: 새로운 관측값 obs, 보상 r, 성공 종료 여부 terminated(RMS < 0.030 mm 도달 시 True), "
            "최대 스텝 초과 중단 여부 truncated(50스텝 도달 시 True), 그리고 최신 info 딕셔너리입니다. "
            "여러분이 작성할 모든 제어기는 BenchmarkController 클래스를 상속받아 표준 act(obs, info) 메서드를 구현해야 합니다."
        ),
        "cues_en": "Reiterate: terminated = True means success (RMS < 0.03 mm); truncated = True means timeout failure at 50 steps.",
        "cues_kr": "terminated=True는 0.03 mm 도달 성공을, truncated=True는 50스텝 타임아웃 실패를 의미함을 명확히 구분 짓습니다.",
        "qa_en": "Q: Can act() inspect info['currents']? A: Yes! Total currents are realistic diagnostic telemetry provided in info.",
        "qa_kr": "Q: act() 메서드 안에서 info['currents']를 사용해도 되나요? A: 네, 적극 권장합니다! 실제 가속기 전원 공급 장치에서도 현재 전류는 실시간 텔레메트리로 제공됩니다.",
        "trans_en": "How are controllers officially scored across the 30 seeds? Let us examine the official scoring formula on Slide 31.",
        "trans_kr": "그렇다면 30개 시드에 대해 제어기 성능은 어떤 공식으로 채점될까요? 슬라이드 31의 공식 채점 수식을 확인해보겠습니다."
    },
    {
        "num": 31,
        "category": "Evaluation Protocol",
        "title_en": "Standardized 30-Seed Scoring Formula",
        "title_kr": "공식 30개 시드 평가 프로토콜 및 채점 공식",
        "visual_en": "Three-component scoring formula s_k = 400 (Success) + 300 * max(0, (20 - n_k)/19) (Speed) + 300 * clip(ln(0.030/RMS) / ln(0.030/0.010), 0, 1) (Precision).",
        "visual_kr": "3대 핵심 채점 공식: 성공 점수(400점) + 속도 점수(최대 300점, 1~20스텝 선형 감쇠) + 정밀도 점수(최대 300점, 30 ㎛에서 10 ㎛ 노이즈 바닥까지 로그 스케일).",
        "script_en": (
            "To establish a fair, mathematically rigorous benchmark, your controllers are evaluated across 30 standardized seeds: range(1, 31). "
            "On each seed k, the controller earns a score s_k from 0 to 1,000 points based on three operational pillars. "
            "If a seed fails to reach RMS < 0.030 mm within 50 steps, it scores exactly ZERO points! Robustness is king: a single failure costs up to 1,000 points. "
            "For successful seeds, the score comprises three terms: "
            "First, Success Points (400 pts): awarded immediately for reaching the sub-30 micron threshold. "
            "Second, Speed Points (up to 300 pts): scaled linearly as 300 times (20 - n_k) / 19. If you converge in 1 step, you earn 300 points; "
            "at 20 steps or more, you earn 0 speed points. "
            "Third, Precision Points (up to 300 pts): scaled logarithmically from 0 at the 0.030 mm target boundary to 300 at the 0.010 mm sensor noise floor: "
            "300 times ln(0.030 / RMS) / ln(0.030 / 0.010). Every factor of improvement in residual orbit earns equal points! "
            "Your official benchmark score is the arithmetic mean across all 30 seeds."
        ),
        "script_kr": (
            "공정하고 엄밀한 벤치마크 평가를 위해, 모든 참가자의 제어기는 1번부터 30번까지 30개의 고정 표준 시드에서 평가됩니다. "
            "각 시드 k에서 획득하는 점수 s_k는 세 가지 기둥에 기반하여 0점에서 1,000점 만점으로 계산됩니다. "
            "만약 50스텝 내에 0.030 mm 목표를 달성하지 못하면 해당 시드는 가차 없이 '0점' 처리됩니다! 단 한 번의 실패도 평균 점수를 대폭 깎아먹으므로 강건성이 최우선입니다. "
            "성공한 시드에 대해서는 세 가지 점수가 합산됩니다: "
            "첫째, '성공 점수(400점)': 0.030 mm 이하 도달 즉시 400점 전액이 부여됩니다. "
            "둘째, '수렴 속도 점수(최대 300점)': 300 × (20 - n_k) / 19 수식에 따라, 1스텝 만에 수렴하면 300점 만점, 20스텝 이상 소요되면 0점 처리됩니다. "
            "셋째, '안착 정밀도 점수(최대 300점)': 0.030 mm 목표선에서 센서 노이즈 바닥인 0.010 mm까지 로그 스케일로 부여됩니다: "
            "300 × ln(0.030 / RMS) / ln(0.030 / 0.010). 잔여 궤도를 노이즈 바닥에 가깝게 안착시킬수록 정밀도 점수가 만점에 수렴합니다. "
            "30개 시드의 점수를 산술 평균한 값이 여러분의 최종 챌린지 점수가 됩니다."
        ),
        "cues_en": "Emphasize the scoring balance: 400 success + 300 speed + 300 precision. A single timeout to 50 steps gives 0 points and ruins the average!",
        "cues_kr": "성공 400점, 속도 300점, 정밀도 300점의 균형을 강조하며, 단 1개 시드의 실패(0점)가 전체 순위에 치명적임을 경고합니다.",
        "qa_en": "Q: Why is current norm not scored? A: Total current is dictated by the seed's distortion kick and varies by only 2% between controllers.",
        "qa_kr": "Q: 전류 크기(current norm)는 왜 점수에 반영되지 않나요? A: 보정에 필요한 누적 전류는 시드의 초기 왜곡 크기에 의해 대부분 결정되며, 제어기간 편차가 2% 미만으로 미미하기 때문입니다.",
        "trans_en": "How do our reference baselines and tracks perform under this official formula? Let us examine the live leaderboard.",
        "trans_kr": "이 공식 채점 기준에 따라 기존 베이스라인과 챌린지 트랙 제어기들의 성능을 직접 비교해보겠습니다."
    },
    {
        "num": 32,
        "category": "Leaderboard & Trajectories",
        "title_en": "Tested Benchmark Leaderboard & Trajectories",
        "title_kr": "공식 벤치마크 리더보드 및 수렴 궤적 비교",
        "visual_en": "Leaderboard table: Rank 1 BO (878.384 pts, 3.6 steps), Rank 2 Supervised MLP (779.169 pts, 4.0 steps), Rank 3 Classical SVD (674.398 pts, 9.4 steps), Rank 4 Reference RL (590.559 pts, 10.8 steps).",
        "visual_kr": "공식 리더보드 결과표: 1위 베이지안 최적화(878.384점, 3.6스텝), 2위 지도학습 MLP(779.169점, 4.0스텝), 3위 고전 SVD(674.398점, 9.4스텝), 4위 기준 RL(590.559점, 10.8스텝).",
        "script_en": (
            "Here is the official baseline leaderboard across all 30 evaluation seeds. All four reference controllers achieve 100% success rate, "
            "so their rankings are determined entirely by speed and precision. "
            "Rank 1 is Track 3: Bayesian Optimization with a calibrated GP and kappa = 0. It converges in an average of just 3.6 steps and lands "
            "at an incredible residual RMS of 0.0136 mm—earning 878.384 points! "
            "Rank 2 is Baseline 1: Supervised Neural Inversion with our MLP digital twin. Anticipating cubic saturation allows it to converge in 4.0 steps, "
            "earning 779.169 points. "
            "Rank 3 is Baseline 0: Classical Linear SVD with alpha = 0.45. It converges safely, but taking 9.4 steps limits its score to 674.398 points. "
            "Rank 4 is the reference Track 2 RL agent. Because its residual weights are untrained, it acts as a damped pseudo-inverse, taking 10.8 steps "
            "and scoring 590.559 points. "
            "On the right, the RMS trajectory plot illustrates the difference: BO and MLP plunge below the 30-micron target within 4 steps, "
            "while SVD and RL descend far more gradually."
        ),
        "script_kr": (
            "30개 표준 평가 시드 전체에 대한 공식 기준 리더보드입니다. 네 가지 제어기 모두 100% 성공률을 달성했으므로, 순위는 전적으로 수렴 속도와 "
            "안착 정밀도에 의해 갈렸습니다. "
            "영예의 1위는 '트랙 3 베이지안 최적화(BO)'입니다: 보정된 GP와 κ = 0 설정을 통해 평균 3.6스텝 만에 수렴하고, 잔여 RMS를 0.0136 mm까지 "
            "극적으로 낮추어 878.384점이라는 압도적 고득점을 기록했습니다! "
            "2위는 '베이스라인 1 지도학습 신경망 역산(MLP)'입니다: 3차 포화를 정확히 예측하여 4.0스텝 만에 안착하며 779.169점을 얻었습니다. "
            "3위는 '베이스라인 0 고전 선형 SVD(α=0.45)'입니다: 안정적이지만 9.4스텝이 소요되어 속도 점수가 깎이며 674.398점에 머물렀습니다. "
            "4위는 '트랙 2 기준 RL 에이전트'입니다: 잔차 가중치가 아직 미학습 상태이므로 단순 감쇠 SVD로 동작하여 10.8스텝, 590.559점을 기록했습니다. "
            "우측 궤적 그래프를 보시면 BO와 MLP는 4스텝 이내에 0.030 mm 목표선 아래로 수직 낙하하는 반면, SVD와 RL은 완만한 계단식 하강을 보입니다."
        ),
        "cues_en": "Highlight the spread: from 590 points up to 878 points. Show that tuning moves agents up this live ladder.",
        "cues_kr": "590점에서 878점에 이르는 점수 격차를 짚어주며, 참가자들의 튜닝에 따라 순위가 실시간으로 뒤바뀔 수 있음을 강조합니다.",
        "qa_en": "Q: Can RL beat BO? A: Yes! A tuned residual policy or model-predictive RL agent in the solution scores 939.981 points!",
        "qa_kr": "Q: RL(트랙 2)이 BO(트랙 3)를 이길 수 있나요? A: 당연히 가능합니다! 주최 측 솔루션에서 잔차를 제대로 학습시킨 RL 에이전트는 무려 939.981점으로 전체 1위를 차지했습니다.",
        "trans_en": "Let us summarize how all these controllers compare across methodology, latency, and sample efficiency.",
        "trans_kr": "각 제어 기법들의 장단점, 연산 지연시간, 샘플 효율성을 종합 비교 분석해보겠습니다."
    },
    {
        "num": 33,
        "category": "Method Comparison Summary",
        "title_en": "Method Comparison Summary",
        "title_kr": "제어 방식별 종합 비교 요약 (기법, 연산 지연 및 성능)",
        "visual_en": "Full structured comparison matrix: SVD vs MLP Inversion vs Adaptive RL vs Bayesian Optimization across mechanism, data requirements, latency, pros, cons, and reference/solution scores.",
        "visual_kr": "종합 비교 매트릭스 표: 기법별 핵심 메커니즘, 필요 데이터량, 1스텝당 추론 지연시간, 장단점, 기준 점수 및 주최 측 솔루션 점수 비교.",
        "script_en": (
            "This table presents a comprehensive trade-off matrix across all methods. "
            "Classical SVD requires zero training data and executes in less than 0.1 milliseconds, but it is blind to non-linear saturation. "
            "Supervised MLP Inversion captures non-linear saturation accurately from 1,500 offline shots, scoring 779 with reference settings "
            "and 924 with a tuned surrogate. However, solving an optimization problem online takes 15 to 30 milliseconds per step—the slowest policy. "
            "Track 2 RL combines analytical priors with learned residuals. Because it is a feedforward policy network, it executes in less than 0.5 milliseconds—"
            "thirty times faster than MLP inversion! While the reference agent scores 590, training the residual reaches 940 points. "
            "Track 3 Bayesian Optimization offers unmatched sample efficiency from just 300 calibration shots, scoring 878 offline and 910 with online refitting. "
            "Notice the trade-off: if you need maximum execution speed, RL wins; if you have limited experimental calibration shots, BO wins; "
            "if you have abundant offline simulation data, Supervised Inversion wins."
        ),
        "script_kr": (
            "이 표는 오늘 다룬 모든 제어 기법들의 장단점과 핵심 특성을 집대성한 비교 매트릭스입니다. "
            "고전 SVD는 사전 훈련 데이터가 전혀 필요 없고 0.1 밀리초 이하로 가장 빠르지만, 비선형 포화를 전혀 다루지 못합니다. "
            "지도학습 MLP 역산은 1,500개 오프라인 샷으로 비선형성을 완벽히 포착하여 기본 779점, 튜닝 시 924점까지 달성합니다. "
            "다만 매 스텝 최적화 수치해를 구해야 하므로 스텝당 15~30 밀리초가 소요되어 가장 느립니다. "
            "트랙 2 강화학습 정책은 물리 사전 지식과 잔차를 결합한 순방향 신경망이므로, 0.5 밀리초 이하의 초고속 실시간 제어가 가능합니다. "
            "기준 점수는 590점이지만, 잔차를 튜닝하면 940점이라는 최고점을 기록합니다. "
            "트랙 3 베이지안 최적화는 단 300개의 샷만으로 878~910점을 기록하는 최강의 샘플 효율성을 자랑합니다. "
            "요약하자면, 초고속 실시간성이 최우선이라면 RL, 빔 측정 샷 수가 극도로 제한된다면 BO, 풍부한 시뮬레이션 데이터가 있다면 지도학습 대리 모델이 정답입니다."
        ),
        "cues_en": "Walk through the trade-offs: speed vs data requirements vs algorithmic complexity. This synthesizes the whole lecture.",
        "cues_kr": "연산 속도, 필요 데이터량, 알고리즘 복잡도 간의 삼각 트레이드오프를 짚어주며 강의 전체를 유기적으로 정리합니다.",
        "qa_en": "Q: Which track is recommended for beginners? A: Track 1 (TODO 1) is the most intuitive starting point, followed by Track 3.",
        "qa_kr": "Q: 초심자에게는 어떤 트랙을 가장 추천하시나요? A: 딥러닝 입문자에게는 직관적인 트랙 1(TODO 1)을 먼저 권장하며, 이후 트랙 3이나 트랙 2로 확장하는 것이 좋습니다.",
        "trans_en": "Now, what specific strategies can you execute this afternoon to climb the leaderboard? Let us look at Slide 34.",
        "trans_kr": "그렇다면 오늘 오후 해커톤에서 리더보드 상위권에 오르기 위한 구체적인 실전 공략 전략을 공유해 드리겠습니다."
    },
    {
        "num": 34,
        "category": "Strategic Advice",
        "title_en": "Strategic Advice for Competitors",
        "title_kr": "해커톤 참가자를 위한 실전 공략 전략 (TODO 1, 2, 3)",
        "visual_en": "Concrete engineering tactics for Track 1 (TODO 1: Tanh, L-BFGS, layer width), Track 2 (TODO 2: Gain, residual training, damping), and Track 3 (TODO 3: Online refitting, kappa schedules).",
        "visual_kr": "트랙별 핵심 튜닝 전략 카드: 트랙 1(TODO 1 대리 모델 고도화), 트랙 2(TODO 2 잔차 정책 학습 및 감쇠 튜닝), 트랙 3(TODO 3 온라인 GP 갱신 및 동적 κ 스케줄).",
        "script_en": (
            "Here is your tactical playbook for this afternoon's mini-hackathon. "
            "For Track 1 competitors (TODO 1): do not settle for the default MLP! Experiment with Tanh activations or smooth GeLU; try training with "
            "solver='lbfgs' on the offline data; adjust the hidden layers to (64, 32) or (256, 128, 64); and tune the L2 penalty alpha. "
            "A surrogate that cuts validation RMSE from 0.0118 mm to 0.0105 mm will immediately boost your benchmark score over 920 points. "
            "For Track 2 competitors (TODO 2): first, optimize the feedback gain alpha in the physics prior (try alpha between 0.8 and 1.2); "
            "second, tune the harmonic damping factor kappa (try 0.02 to 0.05); third, train the residual weights W_learned using supervised regression "
            "against the surrogate error or policy gradient reinforcement learning. "
            "For Track 3 competitors (TODO 3): test kappa values between 0.0 and 0.5; register a step_callback to refit the GP online with every new step; "
            "and implement a dynamic kappa schedule that explores early and exploits late. "
            "Above all, remember our golden rule: robustness comes first! A policy that fails even one seed scores zero on that seed."
        ),
        "script_kr": (
            "오늘 오후 미니 해커톤에서 승리하기 위한 실전 튜닝 전략 가이드입니다. "
            "트랙 1(TODO 1 대리 모델 튜닝) 참가자 여러분: 기본 제공된 MLP 설정에 머무르지 마십시오! Tanh나 GeLU 같은 매끄러운 활성화 함수를 시도해보고, "
            "오프라인 학습 시 solver='lbfgs'를 적용해보십시오. 은닉층 구조를 (64, 32)로 경량화하거나 (256, 128)로 확장하고 L2 규제를 조절하십시오. "
            "검증 RMSE를 0.0118 mm에서 0.0105 mm 부근으로 조금만 낮춰도 920점 이상의 초고득점을 즉시 달성할 수 있습니다! "
            "트랙 2(TODO 2 RL 정책 튜닝) 참가자 여러분: 첫째, 물리 사전 지식의 선형 게인 α를 0.8~1.2 사이로 최적화하십시오. 둘째, 하모닉 감쇠 계수 κ를 "
            "0.02~0.05 사이에서 정밀 튜닝하십시오. 셋째, 선형 모델의 오차 데이터를 타깃으로 삼아 잔차 행렬 W_learned를 회귀 학습시키거나 정책 그래디언트로 학습시키십시오. "
            "트랙 3(TODO 3 베이지안 최적화) 참가자 여러분: κ 값을 0.0~0.5 사이에서 테스트하고, step_callback을 활용해 측정 데이터를 온라인으로 GP에 반영하십시오. "
            "초기에는 탐색하고 후기에는 활용하는 동적 κ 스케줄러도 훌륭한 전략입니다. "
            "무엇보다 가장 중요한 황금률은 '강건성이 최우선'이라는 점입니다! 단 한 번의 시드 실패(0점)도 없도록 안정성을 먼저 확보한 후 속도와 정밀도를 올리십시오."
        ),
        "cues_en": "Reinforce: 'Do not modify env.R or evaluation seeds!' Abide by AGENTS.md rules. Encourage experimentation.",
        "cues_kr": "환경의 물리 상수나 평가 시드를 조작하지 않고 정정당당하게 알고리즘 자체를 개선해야 한다는 규칙을 환기하며 도전 의식을 북돋웁니다.",
        "qa_en": "Q: Can we combine methods, e.g. GP prior with RL? A: Absolutely! Novel hybrid architectures are welcome and often win hackathons.",
        "qa_kr": "Q: 두 가지 방식을 융합해도 되나요? A: 물론입니다! GP 예측을 사전 지식으로 활용하는 하이브리드 제어기는 실제 연구에서도 매우 강력한 접근법입니다.",
        "trans_en": "Finally, let us summarize our morning journey and transition to Lecture 2 with Dr. Thorsten Hellert.",
        "trans_kr": "이제 오늘 강의를 마무리하며 핵심 교훈을 정리하고, Thorsten Hellert 박사님의 제2강으로 넘어가겠습니다."
    },
    {
        "num": 35,
        "category": "Summary & Transition",
        "title_en": "Summary & Transition to Lecture 2",
        "title_kr": "강의 요약, 핵심 교훈 및 제2강 연계 안내",
        "visual_en": "Summary takeaways card: Physics-guided ML is indispensable, non-linear saturation requires modern AI, and transition banner introducing Lecture 2: Agentic AI for Accelerators.",
        "visual_kr": "핵심 교훈 정리 카드: 물리 지식과 ML의 융합 필수성, 비선형 포화 극복, 이어서 진행될 제2강 '가속기 과학을 위한 에이전틱 AI(Thorsten Hellert 박사)' 안내 배너.",
        "script_en": (
            "To conclude Lecture 1, let us review our core takeaways. "
            "First, accelerator physics and machine learning are complementary partners: pure black-box models fail to extrapolate, while pure linear optics "
            "stalls under non-linear magnetic saturation. By combining beam optics priors with deep surrogates, adaptive RL, or Gaussian Processes, "
            "we achieve robust, sub-millisecond, sub-micron orbit control. "
            "Second, our 30-seed benchmark scoring formula rewards controllers that balance robustness, speed, and precision down to the 10-micron noise floor. "
            "Now, we transition directly to Lecture 2. Dr. Thorsten Hellert from Lawrence Berkeley National Laboratory will present 'Agentic AI for "
            "Accelerator Research.' You will discover how autonomous LLM agents leverage Python execution environments, orchestrate multi-physics simulations, "
            "and implement operational safety guardrails. "
            "Thank you all for your attention. I look forward to an exciting and competitive hackathon this afternoon!"
        ),
        "script_kr": (
            "제1강을 마치며 핵심 교훈 세 가지를 정리하겠습니다. "
            "첫째, '가속기 물리학과 머신러닝의 융합'은 선택이 아닌 필수입니다. 순수 블랙박스 신경망은 외삽 영역에서 물리 법칙을 위반하며, "
            "순수 선형 광학 모델은 자기 포화라는 비선형 현실 앞에서 무력해집니다. 물리 사전 지식에 딥러닝 대리 모델, 적응형 RL, 베이지안 최적화를 "
            "결합할 때 비로소 밀리초 이하의 초고속, 서브미크론 정밀도의 강건한 궤도 제어가 완성됩니다. "
            "둘째, 해커톤 채점 공식은 10 ㎛ 노이즈 바닥까지의 강건성, 속도, 정밀도를 종합 평가하도록 설계되었습니다. "
            "이제 잠시 휴식 후, 미국 LBNL의 Thorsten Hellert 박사님께서 진행하시는 제2강 '가속기 연구를 위한 에이전틱 AI'가 이어집니다. "
            "최신 거대언어모델 에이전트가 가속기 제어 환경을 자율적으로 분석하고 시뮬레이션을 오케스트레이션하는 놀라운 최신 기술을 만나보실 수 있습니다. "
            "경청해 주셔서 대단히 감사드리며, 오후 해커톤에서 여러분의 멋진 활약을 기대하겠습니다!"
        ),
        "cues_en": "End with strong enthusiasm. Welcome questions from the audience before handing over to Dr. Hellert.",
        "cues_kr": "열정적인 어조로 강의를 마무리하고, 질의응답 시간을 가진 뒤 제2강 Thorsten Hellert 박사에게 마이크를 넘깁니다.",
        "qa_en": "Q: Where are the lecture slides and notes stored? A: In presentations/ and lecture_notes/ inside the repository root.",
        "qa_kr": "Q: 강의 슬라이드와 강의 노트는 어디서 볼 수 있나요? A: 저장소 루트의 presentations/ 및 lecture_notes/ 디렉토리에 PDF와 마크다운으로 모두 제공됩니다.",
        "trans_en": "Thank you, and enjoy Lecture 2 and the Afternoon Hackathon!",
        "trans_kr": "감사합니다. 이어서 제2강과 오후 해커톤을 유익하게 즐겨주시기 바랍니다!"
    }
]

def tex_clean(text: str) -> str:
    """Escape TeX special characters (&, %, _, ^) outside math mode, and &/% inside math mode."""
    unicode_map = [
        ("⁽¹⁾", "$^{(1)}$"), ("⁽²⁾", "$^{(2)}$"), ("⁽³⁾", "$^{(3)}$"),
        ("μ₀", r"$\mu_0$"), ("φ₀", r"$\phi_0$"), ("ẑ_f", r"$\hat{z}_f$"),
        ("det(J)", r"$\det(J)$"), ("det(M)", r"$\det(M)$"), ("det M", r"$\det M$"),
        ("₀", "$_0$"), ("₁", "$_1$"), ("₂", "$_2$"), ("₃", "$_3$"),
        ("³", "$^3$"), ("²", "$^2$"), ("ᵀ", "$^T$"),
    ]
    for u, rep in unicode_map:
        text = text.replace(u, rep)

    parts = text.split("$")
    for i in range(len(parts)):
        if i % 2 == 0:
            p = parts[i]
            p = re.sub(r"(?<!\\)&", r"\&", p)
            p = re.sub(r"(?<!\\)%", r"\%", p)
            p = re.sub(r"(?<!\\)_", r"\_", p)
            p = p.replace("^", r"\textasciicircum{}")
            parts[i] = p
        else:
            p = parts[i]
            p = re.sub(r"(?<!\\)%", r"\%", p)
            p = re.sub(r"(?<!\\)&", r"\&", p)
            parts[i] = p
    return "$".join(parts)

def build_english_tex():
    out = [r'''\documentclass[11pt,a4paper]{article}
\usepackage[margin=1in]{geometry}
\usepackage{fontspec}
\setmainfont{DejaVu Serif}
\setsansfont{DejaVu Sans}
\setmonofont{DejaVu Sans Mono}
\usepackage{amsmath,amssymb,amsfonts,bm}
\usepackage{xcolor}
\usepackage{booktabs}
\usepackage{tcolorbox}
\tcbuselibrary{skins,breakable}
\usepackage{fancyhdr}
\usepackage{hyperref}

\definecolor{navy}{HTML}{002060}
\definecolor{primaryblue}{HTML}{184C78}
\definecolor{accent}{HTML}{2980B9}
\definecolor{darkgray}{HTML}{2C3E50}
\definecolor{lightbg}{HTML}{F8FAFC}
\definecolor{bordergray}{HTML}{CBD5E1}
\definecolor{tunablered}{HTML}{C0392B}
\definecolor{successgreen}{HTML}{27AE60}
\definecolor{gold}{HTML}{B48C14}

\pagestyle{fancy}
\fancyhf{}
\setlength{\headheight}{15pt}
\fancyhead[L]{\small\bfseries\color{primaryblue}AI Applications in Accelerators \enspace$|$\enspace Lecture 1 Slide Narratives}
\fancyhead[R]{\small\color{darkgray}Chong Shik Park, Ph.D.}
\fancyfoot[C]{\thepage}
\renewcommand{\headrulewidth}{0.5pt}

\hypersetup{
    colorlinks=true,
    linkcolor=primaryblue,
    urlcolor=accent,
    pdftitle={Lecture 1 Slide Narratives (English)},
    pdfauthor={Chong Shik Park, Ph.D.}
}

\begin{document}

\begin{titlepage}
    \centering
    \vspace*{1.5cm}
    {\Huge\bfseries\color{navy}AI Applications in Accelerators\\[0.3em]Tutorial \& Mini-Hackathon\par}
    \vspace{1.0cm}
    {\LARGE\bfseries\color{primaryblue}Lecture 1: AI/ML Foundations \& Closed-Loop Control\par}
    \vspace{0.4cm}
    {\Large\color{accent}Comprehensive Slide-by-Slide Presenter Script \& Technical Companion\par}
    \vspace{1.5cm}

    \begin{tcolorbox}[colback=white,colframe=accent,width=0.85\textwidth,arc=4pt]
        \centering
        \textbf{Author \& Instructor:}\\[0.2em]
        {\large\bfseries Chong Shik Park, Ph.D.}\\[0.2em]
        Department of Accelerator Science, Korea University, Sejong\\[0.2em]
        \texttt{kuphy@korea.ac.kr} \enspace$|$\enspace November 19, 2026
    \end{tcolorbox}

    \vspace{1.5cm}
    \begin{minipage}{0.85\textwidth}
        \small\color{darkgray}
        \textbf{Document Overview:}\\
        This document provides the complete word-for-word spoken narrative, technical background notes, slide visual descriptions, pedagogical focus points, anticipated participant questions with model answers, and natural verbal transition cues for all 35 slides comprising Lecture 1. It serves as an authoritative speaker reference for delivering the lecture and as a self-contained study companion for hackathon participants.
    \end{minipage}
    \vfill
    {\footnotesize\color{darkgray}Korea University Accelerator Physics Laboratory \enspace$\bullet$\enspace 2026}
\end{titlepage}

\tableofcontents
\clearpage
''']

    for s in SLIDES:
        title = tex_clean(s['title_en'])
        cat = tex_clean(s['category'])
        visual = tex_clean(s['visual_en'])
        script = tex_clean(s['script_en'])
        cues = tex_clean(s['cues_en'])
        qa = tex_clean(s['qa_en'])
        trans = tex_clean(s['trans_en'])

        out.append(f"\\section{{Slide {s['num']}: {title}}}\n")
        out.append(f"\\textbf{{\\color{{accent}}Category:}} {cat} \\hfill \\textbf{{\\color{{primaryblue}}Slide Index:}} {s['num']} / 35\n\n")

        out.append(r"\begin{tcolorbox}[colback=lightbg,colframe=bordergray,title=\textbf{Slide Visual Blueprint},fonttitle=\small\color{darkgray},arc=3pt]")
        out.append(visual + "\n")
        out.append(r"\end{tcolorbox}" + "\n\n")

        out.append(r"\begin{tcolorbox}[colback=white,colframe=primaryblue,title=\textbf{Spoken Presenter Script},fonttitle=\bfseries\color{white},arc=4pt]")
        out.append(script + "\n")
        out.append(r"\end{tcolorbox}" + "\n\n")

        out.append(r"\begin{itemize}")
        out.append(f"    \\item \\textbf{{\\color{{navy}}Pedagogical Focus \\& Emphasis:}} {cues}")
        out.append(f"    \\item \\textbf{{\\color{{successgreen}}Anticipated Participant Q\\&A:}} {qa}")
        out.append(f"    \\item \\textbf{{\\color{{accent}}Verbal Transition to Next Slide:}} \\emph{{{trans}}}")
        out.append(r"\end{itemize}")
        out.append(r"\vspace{0.8em}\hrule\vspace{1.2em}")
        out.append("\n")

    out.append(r"\end{document}")
    return "\n".join(out)

def build_korean_tex():
    out = [r'''\documentclass[11pt,a4paper]{article}
\usepackage[margin=1in]{geometry}
\usepackage{fontspec}
\setmainfont{Noto Serif CJK KR}
\setsansfont{Noto Sans CJK KR}
\setmonofont{Noto Sans Mono CJK KR}

\usepackage{amsmath,amssymb,amsfonts,bm}
\usepackage{xcolor}
\usepackage{booktabs}
\usepackage{tcolorbox}
\tcbuselibrary{skins,breakable}
\usepackage{fancyhdr}
\usepackage{hyperref}

\definecolor{navy}{HTML}{002060}
\definecolor{primaryblue}{HTML}{184C78}
\definecolor{accent}{HTML}{2980B9}
\definecolor{darkgray}{HTML}{2C3E50}
\definecolor{lightbg}{HTML}{F8FAFC}
\definecolor{bordergray}{HTML}{CBD5E1}
\definecolor{tunablered}{HTML}{C0392B}
\definecolor{successgreen}{HTML}{27AE60}
\definecolor{gold}{HTML}{B48C14}

\pagestyle{fancy}
\fancyhf{}
\setlength{\headheight}{15pt}
\fancyhead[L]{\small\bfseries\color{primaryblue}가속기 인공지능 튜토리얼 \enspace$|$\enspace 제1강 슬라이드 내러티브 대본}
\fancyhead[R]{\small\color{darkgray}박종식 교수 (고려대학교)}
\fancyfoot[C]{\thepage}
\renewcommand{\headrulewidth}{0.5pt}

\hypersetup{
    colorlinks=true,
    linkcolor=primaryblue,
    urlcolor=accent,
    pdftitle={Lecture 1 Slide Narratives (Korean)},
    pdfauthor={Chong Shik Park, Ph.D.}
}

\begin{document}

\begin{titlepage}
    \centering
    \vspace*{1.5cm}
    {\Huge\bfseries\color{navy}가속기 인공지능 응용\\[0.3em]튜토리얼 및 미니 해커톤\par}
    \vspace{1.0cm}
    {\LARGE\bfseries\color{primaryblue}제1강: AI/ML 기초 및 폐루프 궤도 제어\par}
    \vspace{0.4cm}
    {\Large\color{accent}슬라이드별 상세 구두 발표 대본 및 기술 해설서 (한국어판)\par}
    \vspace{1.5cm}

    \begin{tcolorbox}[colback=white,colframe=accent,width=0.85\textwidth,arc=4pt]
        \centering
        \textbf{강연자 및 저자:}\\[0.2em]
        {\large\bfseries 박종식 교수 (Chong Shik Park, Ph.D.)}\\[0.2em]
        고려대학교 세종캠퍼스 가속기과학과\\[0.2em]
        \texttt{kuphy@korea.ac.kr} \enspace$|$\enspace 2026년 11월 19일
    \end{tcolorbox}

    \vspace{1.5cm}
    \begin{minipage}{0.85\textwidth}
        \small\color{darkgray}
        \textbf{문서 개요 및 목적:}\\
        본 문서는 제1강 총 35개 슬라이드 전체에 대한 구두 발표 대본(Verbatim Script), 슬라이드 시각 구성 요약, 교육적 강조 포인트, 예상 질의응답(Q\&A), 그리고 다음 슬라이드로의 자연스러운 전환 멘트를 수록한 공식 강연 해설서입니다. 강연자의 실전 발표 가이드이자, 해커톤 참가자들의 자습 및 복습용 교재로 활용됩니다.
    \end{minipage}
    \vfill
    {\footnotesize\color{darkgray}고려대학교 가속기물리연구실 \enspace$\bullet$\enspace 2026}
\end{titlepage}

\tableofcontents
\clearpage
''']

    for s in SLIDES:
        title = tex_clean(s['title_kr'])
        cat = tex_clean(s['category'])
        visual = tex_clean(s['visual_kr'])
        script = tex_clean(s['script_kr'])
        cues = tex_clean(s['cues_kr'])
        qa = tex_clean(s['qa_kr'])
        trans = tex_clean(s['trans_kr'])

        out.append(f"\\section{{슬라이드 {s['num']}: {title}}}\n")
        out.append(f"\\textbf{{\\color{{accent}}분류:}} {cat} \\hfill \\textbf{{\\color{{primaryblue}}슬라이드 번호:}} {s['num']} / 35\n\n")

        out.append(r"\begin{tcolorbox}[colback=lightbg,colframe=bordergray,title=\textbf{슬라이드 시각 구성 요약},fonttitle=\small\color{darkgray},arc=3pt]")
        out.append(visual + "\n")
        out.append(r"\end{tcolorbox}" + "\n\n")

        out.append(r"\begin{tcolorbox}[colback=white,colframe=primaryblue,title=\textbf{발표자 구두 대본 (Spoken Script)},fonttitle=\bfseries\color{white},arc=4pt]")
        out.append(script + "\n")
        out.append(r"\end{tcolorbox}" + "\n\n")

        out.append(r"\begin{itemize}")
        out.append(f"    \\item \\textbf{{\\color{{navy}}교수학적 강조점 (Focus Point):}} {cues}")
        out.append(f"    \\item \\textbf{{\\color{{successgreen}}예상 질문 및 모범 답변 (Q\\&A):}} {qa}")
        out.append(f"    \\item \\textbf{{\\color{{accent}}다음 슬라이드 연결 멘트 (Transition):}} {trans}")
        out.append(r"\end{itemize}")
        out.append(r"\vspace{0.8em}\hrule\vspace{1.2em}")
        out.append("\n")

    out.append(r"\end{document}")
    return "\n".join(out)

def main():
    en_tex_path = PRESENTATIONS_DIR / "Lecture_1_Slide_Narratives_EN.tex"
    kr_tex_path = PRESENTATIONS_DIR / "Lecture_1_Slide_Narratives_KR.tex"

    print("Writing English TeX source...")
    en_tex_path.write_text(build_english_tex(), encoding="utf-8")

    print("Writing Korean TeX source...")
    kr_tex_path.write_text(build_korean_tex(), encoding="utf-8")

    print("Compiling English PDF with xelatex...")
    for _ in range(2):
        subprocess.run(["xelatex", "-interaction=nonstopmode", en_tex_path.name], cwd=PRESENTATIONS_DIR, check=True)

    print("Compiling Korean PDF with xelatex...")
    for _ in range(2):
        subprocess.run(["xelatex", "-interaction=nonstopmode", kr_tex_path.name], cwd=PRESENTATIONS_DIR, check=True)

    en_pdf = PRESENTATIONS_DIR / "Lecture_1_Slide_Narratives_EN.pdf"
    kr_pdf = PRESENTATIONS_DIR / "Lecture_1_Slide_Narratives_KR.pdf"

    if en_pdf.is_file() and kr_pdf.is_file():
        print(f"SUCCESS: Generated {en_pdf} ({en_pdf.stat().st_size} bytes)")
        print(f"SUCCESS: Generated {kr_pdf} ({kr_pdf.stat().st_size} bytes)")
        return 0
    else:
        print("ERROR: Failed to generate one or both PDFs.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
