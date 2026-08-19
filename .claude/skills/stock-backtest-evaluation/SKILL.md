---
name: stock-backtest-evaluation
description: 학습된 모델을 holdout 구간에 적용해 방향 정확도·누적수익률·MDD를 산출하는 백테스트를 수행한다. "백테스트 해줘", "모델 성능 평가해줘", "예측 정확도 확인해줘" 같은 요청에 stock-backtest-evaluator 에이전트가 사용.
---

# 백테스트 및 평가

## 절차

1. **입력 확인**: `models/{ticker}_model.pkl`이 없으면 [stock-model-training](../stock-model-training/SKILL.md)으로 먼저 학습하라고 안내한다.
2. **holdout 검증**: 학습 시 분리된 validation 구간과 별도로, 가장 최근 구간을 holdout으로 사용한다 (모델 학습에 전혀 쓰이지 않은 구간).
3. **평가**: `scripts/backtest.py`로 방향 정확도, 누적수익률(모델 신호를 단순 매수/보유/매도로 가정), 최대낙폭(MDD)을 계산한다.
4. **보고**: 결과를 `_workspace/backtest_{ticker}_{date}.md`에 저장하고, 요약을 사용자에게 보고한다. 보고서 끝에 반드시 "이 결과는 투자 자문이 아니며 과거 데이터 기반 참고용입니다"를 명시한다.
5. **(선택) supabase 기록**: [supabase-storage](../supabase-storage/SKILL.md)의 `backtest_results` 테이블에 기록한다.

## 주의

- 백테스트 구간이 학습/검증에 사용된 구간과 겹치면 결과가 무의미하다 — 항상 시간순으로 완전히 분리되었는지 확인한다.
- 거래 비용(수수료, 슬리피지)을 반영하지 않은 단순 시뮬레이션임을 보고서에 명시한다.
