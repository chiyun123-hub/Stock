# Project: Stock Prediction System

## Tech Stack
- Language: Python 3.12+
- Key Libraries: yfinance, pandas, numpy, supabase (planned)

## Code Style & Conventions
- Use snake_case for all Python function and variable names.
- Type hints are strictly required.
- Write minimal, concise English comments.
- **IMPORTANT**: Never read or output large CSV data inside the chat.

## Core Commands
- Fetch Data: `python fetch_data.py`
- Run Tests: `pytest` (planned)

## Rules & Guardrails
- Always save generated datasets to the `data/` directory.
- All database configuration keys must load from a `.env` file.

## 하네스: Stock Prediction System

**목표:** yfinance로 수집한 시세 데이터를 기반으로 예측 모델을 학습·백테스트하고, 결과를 supabase에 저장한다. 투자 자문이 아니다.

**트리거:** 예측 모델 학습, 데이터 수집, 백테스트 관련 요청 시 `stock-prediction-pipeline` 스킬을 사용하라. 단순 질문은 직접 응답 가능.

**변경 이력:**
| 날짜 | 변경 내용 | 대상 | 사유 |
|------|----------|------|------|
| 2026-08-18 | 초기 구성 (stock-data-collector/stock-model-trainer/stock-backtest-evaluator 에이전트 + stock-data-collection/stock-model-training/stock-backtest-evaluation/supabase-storage/stock-prediction-pipeline 스킬, 서브 에이전트 순차 파이프라인) | 전체 | 데이터 수집→예측 모델링→백테스트→supabase 저장으로 이어지는 하네스 요청 |

## 하네스: 주식 시황 분석

**목표:** 한국 장 시간(평일 09:00~15:30 KST) 기준 국내(KOSPI/KOSDAQ)+해외 주식 시황을 공개 데이터로 스크리닝해, 상승/하락 예상 종목 후보를 각 최대 10개씩 참고용으로 정리한다. 투자 자문이 아니다. (기존 하네스 — 2026-08-12 구성, 예측 시스템과 별개 도메인으로 병행 운영)

**트리거:** 주식 분석/시황/상승·하락 종목 관련 요청 시 `kr-market-stock-scan` 스킬을 사용하라. 단순 질문은 직접 응답 가능.
