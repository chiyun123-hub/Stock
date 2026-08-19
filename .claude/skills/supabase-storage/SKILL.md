---
name: supabase-storage
description: 시세 데이터/모델 성능/백테스트 결과를 supabase 테이블에 저장·조회하는 공유 유틸리티 스킬. .env의 SUPABASE_URL/SUPABASE_KEY를 사용. stock-data-collector, stock-model-trainer, stock-backtest-evaluator가 공용으로 사용.
---

# Supabase 저장

## 원칙

- 자격증명은 반드시 `.env`에서 로드한다 (`SUPABASE_URL`, `SUPABASE_KEY`). 코드에 하드코딩 금지 — 위반 시 프로젝트 규칙(CLAUDE.md) 위배.
- `.env`가 없거나 키가 비어있으면 supabase 저장을 건너뛰고 로컬 파일 저장만 수행한 뒤, 사용자에게 `.env` 설정이 필요하다고 안내한다. 에러로 전체 파이프라인을 중단시키지 않는다.

## 테이블 스키마

`scripts/schema.sql`에 3개 테이블 정의:

- `market_data(ticker, date, open, high, low, close, volume)` — 시세 원본
- `model_runs(id, ticker, trained_at, features, metrics)` — 학습 실행 기록
- `backtest_results(id, model_run_id, ticker, period_start, period_end, direction_accuracy, cumulative_return, max_drawdown)` — 백테스트 결과

## 사용

```bash
python .claude/skills/supabase-storage/scripts/upsert_market_data.py data/aapl_5y.csv AAPL
```

최초 1회 `scripts/schema.sql`을 supabase SQL 편집기에서 실행해 테이블을 만들어야 한다. 이 스킬은 테이블을 자동 생성하지 않는다 — DDL 실행은 사용자 승인이 필요한 작업이다.
