---
name: stock-data-collection
description: yfinance로 종목의 과거 일봉/주봉 시세를 다운로드해 data/ 디렉토리에 CSV로 저장하고, 필요시 supabase에도 업서트한다. "데이터 수집해줘", "N년치 데이터 받아줘", "티커 추가해서 다시 받아줘" 같은 요청에 stock-data-collector 에이전트가 사용.
---

# 시세 데이터 수집

## 절차

1. **기존 데이터 확인**: `data/{ticker}_{period}.csv`가 이미 있으면 최신성(마지막 날짜)을 확인하고, 사용자가 "다시 받아줘"라고 명시하지 않는 한 재사용을 제안한다.
2. **다운로드**: `scripts/fetch_ticker.py`를 사용해 yfinance로 다운로드한다.
   ```bash
   python .claude/skills/stock-data-collection/scripts/fetch_ticker.py AAPL --period 5y --interval 1d
   ```
3. **저장**: `data/{ticker}_{period}.csv`. 파일명의 `_new` 접미사 규칙은 적용하지 않는다 — 이 경로는 파이프라인이 반복 참조하는 고정 데이터 산출물이다 (CLAUDE.md 규칙의 예외 대상과 동일한 성격).
4. **결측치/이상치 요약**: 행 수, 기간, `NaN` 컬럼별 개수를 콘솔에만 출력하고 채팅에는 요약 문장으로만 보고한다. CSV 원문을 채팅에 출력하지 않는다.
5. **(선택) supabase 저장**: 요청 시 [supabase-storage](../supabase-storage/SKILL.md) 스킬의 `market_data` 테이블 스키마와 업서트 스크립트를 사용한다.

## 여러 종목 처리

여러 티커를 요청받으면 `scripts/fetch_ticker.py`를 티커별로 순차 호출한다 (yfinance rate limit 방지를 위해 병렬 다운로드는 피한다). 실패한 티커는 건너뛰고 마지막에 실패 목록을 보고한다.

## 주의

- 상장 전 구간이나 거래정지로 인한 결측은 그대로 둔다. 임의 보간(ffill/interpolate)은 모델 단계에서, 방법을 명시한 채로만 수행한다.
