---
name: stock-model-training
description: 수집된 시세 CSV로 피처를 만들고 다음날 종가/등락 방향을 예측하는 모델을 학습·검증한다. "모델 학습해줘", "예측 모델 만들어줘", "피처 추가해서 다시 학습" 같은 요청에 stock-model-trainer 에이전트가 사용.
---

# 예측 모델 학습

## 절차

1. **입력 확인**: `data/{ticker}_{period}.csv`가 없으면 먼저 [stock-data-collection](../stock-data-collection/SKILL.md)으로 데이터부터 수집하라고 안내한다.
2. **피처 생성**: `scripts/build_features.py`로 이동평균, 변동성, RSI 등 예측 시점 이전 데이터만 사용하는 피처를 만든다.
3. **시간순 분할**: 셔플 없이 마지막 N%(기본 20%)를 validation으로 분리한다.
4. **학습**: `scripts/train_model.py`로 모델을 학습하고 `models/{ticker}_model.pkl`, `models/{ticker}_features.json`으로 저장한다.
5. **보고**: MAE/RMSE(가격 예측 시) 또는 방향 정확도(등락 예측 시)를 validation 기준으로 보고한다. 학습 정확도만 보고하고 검증 지표를 생략하지 않는다 — 과적합 은폐 방지.

## Look-ahead bias 체크리스트

- 피처 계산에 `shift(-N)` 등 미래 값을 참조하지 않았는가
- 정규화(스케일링) 통계는 train 구간에서만 계산했는가
- 타깃(다음날 종가 등)이 피처에 그대로 섞여 들어가지 않았는가

## supabase 기록

학습 완료 후 `metrics`, `features`를 [supabase-storage](../supabase-storage/SKILL.md)의 `model_runs` 테이블에 기록할 수 있다 (선택, `.env` 설정 필요).
