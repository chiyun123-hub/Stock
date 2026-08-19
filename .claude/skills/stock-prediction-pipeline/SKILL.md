---
name: stock-prediction-pipeline
description: 종목 데이터 수집 → 예측 모델 학습 → 백테스트 평가로 이어지는 Stock Prediction System 전체 파이프라인 오케스트레이터. "주가 예측 모델 만들어줘", "예측 파이프라인 실행/재실행", "모델 다시 학습해줘", "백테스트만 다시", "이 종목 예측해줘" 같은 요청에 반드시 사용할 것.
---

# Stock Prediction System 파이프라인

## Phase 0: 컨텍스트 확인

1. `_workspace/`, `data/`, `models/`에 이전 산출물이 있는지 확인한다.
2. 판별:
   - 산출물 없음 → **초기 실행** (전체 파이프라인)
   - 산출물 있음 + 사용자가 특정 단계만 요청("모델만 다시 학습해줘", "백테스트만 다시") → **부분 재실행** (해당 에이전트만 재호출)
   - 산출물 있음 + 새 종목/새 기간 요청 → **새 실행** (해당 종목 기준으로 전체 파이프라인, 기존 파일은 덮어쓰지 않고 종목/기간별 파일명으로 구분되므로 별도 이동 불필요)

## Phase 1: 데이터 수집

**실행 모드:** 서브 에이전트 (단일 작업, 결과만 반환하면 충분 — 실시간 조율 불필요)

`Agent(subagent_type="stock-data-collector", model="opus")`를 호출해 [stock-data-collection](../stock-data-collection/SKILL.md)을 수행시킨다. 입력: 티커, 기간(기본 5y), 주기(기본 1d).

반환된 CSV 경로를 다음 단계 입력으로 사용한다.

## Phase 2: 모델 학습

**실행 모드:** 서브 에이전트 (Phase 1 산출물에 순차 의존, 병렬/토론 불필요)

`Agent(subagent_type="stock-model-trainer", model="opus")`를 호출해 [stock-model-training](../stock-model-training/SKILL.md)을 수행시킨다. 입력: Phase 1의 CSV 경로.

검증 지표(방향 정확도 등)를 사용자에게 중간 보고한다.

## Phase 3: 백테스트 평가

**실행 모드:** 서브 에이전트

`Agent(subagent_type="stock-backtest-evaluator", model="opus")`를 호출해 [stock-backtest-evaluation](../stock-backtest-evaluation/SKILL.md)을 수행시킨다. 입력: Phase 2의 모델 경로, holdout 기간(기본 최근 60거래일).

## Phase 4: 최종 보고

세 단계 결과를 종합해 `_workspace/prediction_report_{ticker}_{date}.md`에 저장하고, 요약(데이터 기간, 모델 검증 지표, 백테스트 지표, 투자 자문 아님 고지)을 사용자에게 보고한다.

## 데이터 전달

파일 기반: `data/{ticker}_{period}.csv` → `models/{ticker}_model.pkl` + `models/{ticker}_features.json` → `_workspace/prediction_report_*.md`. 각 Phase는 이전 Phase의 파일 경로를 반환값으로 받아 다음 Agent 호출의 입력으로 전달한다.

## 에러 핸들링

- 각 Phase는 실패 시 1회 재시도한다. 재실패하면 해당 Phase 이후를 중단하고, 어디까지 완료되었는지와 실패 사유를 사용자에게 보고한다 (예: 데이터 수집은 성공했으나 학습용 데이터 부족으로 모델 학습 중단).
- supabase 저장 실패는 파이프라인을 막지 않는다 — 로컬 파일 저장은 항상 우선 보장한다.

## 테스트 시나리오

- **정상 흐름**: "AAPL 5년치로 예측 모델 만들고 백테스트까지 해줘" → Phase 1~4 전체 실행, 최종 보고서 생성.
- **에러 흐름**: 존재하지 않는 티커 요청 → Phase 1에서 실패 → 사유 보고 후 중단 (Phase 2, 3 미실행).
- **부분 재실행**: "모델만 다시 학습해줘, 피처에 RSI 추가해서" → Phase 0에서 기존 데이터 재사용 판단 → Phase 2만 재호출.
