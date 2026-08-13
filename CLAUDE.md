# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 프로젝트 이름

- 이 프로젝트(폴더)의 이름: **주식**

## Instructions

- 답변은 한글로 작성한다.
- 답변은 간결하게 작성한다.
- 새로 만드는 파일은 파일명 끝에 `_new`를 붙인다. **예외**: 하네스가 정해진 경로로 반복해서 읽고 쓰는 고정 파일(`_workspace/*.md`, `site/data.json`, `site/index.html`, `site/artifact_url.txt`, `site/lessons_*.md` 등)에는 적용하지 않는다 — 이런 파일은 매번 새로 만드는 게 아니라 계속 갱신되는 데이터/산출물이며, 경로가 고정되어야 다른 에이전트·스킬이 참조할 수 있다. 사용자에게 전달하는 일회성 산출물(예: `주식분석리포트_{날짜}_{시간}_new.md`)에는 그대로 적용한다.

## Status

This folder currently contains no application source code — only the Claude Code CLI executable (`claude.exe`), its local `.claude/` settings, and the agent/skill harness described below.

## 하네스: 주식 시황 분석

**목표:** 한국 장 시간(평일 09:00~15:30 KST) 기준 국내(KOSPI/KOSDAQ)+해외 주식 시황을 공개 데이터로 스크리닝해, 상승/하락 예상 종목 후보를 각 최대 10개씩 참고용으로 정리한다. 투자 자문이 아니다.

**트리거:** 주식 분석/시황/상승·하락 종목 관련 요청 시 `kr-market-stock-scan` 스킬을 사용하라. 단순 질문은 직접 응답 가능.

**변경 이력:**
| 날짜 | 변경 내용 | 대상 | 사유 |
|------|----------|------|------|
| 2026-08-12 | 초기 구성 (domestic-stock-analyst, overseas-stock-analyst, market-report-writer 에이전트 + domestic/overseas-stock-screening, stock-report-format, kr-market-stock-scan 스킬) | 전체 | 국내·해외 주식 상승/하락 예상 종목 각 10개 분석 요청 |
| 2026-08-12 | 서브 에이전트(팬아웃→팬인) 방식을 에이전트 팀 방식으로 전환 — 3개 에이전트 정의에 "팀 통신 프로토콜" 추가, 오케스트레이터를 이름 지정 소환(`domestic`/`overseas`/`reportwriter`) + `SendMessage`/`TaskCreate` 기반으로 재작성 | agents/domestic-stock-analyst.md, agents/overseas-stock-analyst.md, agents/market-report-writer.md, skills/kr-market-stock-scan/SKILL.md | 사용자가 에이전트끼리 실시간으로 소통하는 팀 단위 하네스를 요청 |
| 2026-08-12 | 오케스트레이터에 Phase 2 "기관 순매수 즉시 브리핑" 추가 — 장중이면 `domestic`이 본 스크리닝보다 먼저 기관 순매수 상위 종목 중 최근 1주 수익률 top3를 조회해 `main`에게 즉시 전달 | agents/domestic-stock-analyst.md, agents/market-report-writer.md, skills/kr-market-stock-scan/SKILL.md | 장 열리면 기업(기관)이 사들이는 종목과 그중 수익률 top3를 즉시 보고 싶다는 요청 |
| 2026-08-12 | 최종 리포트를 채팅에 붙여넣는 대신 날짜별 이력이 누적되는 웹페이지(Artifact)로 발행하도록 전환 — `stock-report-website` 스킬 신설(`site/data.json` 누적 저장 + 차가운 톤 디자인 원칙 + Artifact 갱신 발행), market-report-writer가 리포트 작성 후 이 스킬로 사이트 발행까지 담당 | skills/stock-report-website (신설), agents/market-report-writer.md, skills/kr-market-stock-scan/SKILL.md | 사용자가 결과를 채팅이 아닌, 첫 화면에 오늘 핵심 이슈 10개 + 날짜별 예측 이력을 보여주는 전용 웹페이지로 요청 |
| 2026-08-12 | Auto Mode classifier가 Artifact 발행을 "공개 표면 생성"으로 차단 → `.claude/settings.json`(신설, 프로젝트 공용)에 `Artifact` 도구 허용 규칙 추가 | .claude/settings.json (신설) | 서브에이전트·오케스트레이터 모두 Artifact 발행 시 classifier에 막혀 사용자 승인으로 해결 |
| 2026-08-12 | 사이트를 스크롤 방식에서 왼쪽 사이드바 클릭 전환 구조(오늘 핵심 이슈/날짜별 예측 이력/날짜별 예측 정확도)로 개편, 화면 전환·항목 등장·차트 성장 애니메이션 추가 | skills/stock-report-website/SKILL.md, site/index.html | 사용자가 스크롤 대신 사이드바 탐색 + 애니메이션 효과를 요청 |
| 2026-08-12 | 오늘의 핵심 이슈·종목 근거에 `sourceUrl`/`sourceTitle` 필드 추가 — 클릭하면 분석에 사용한 원문 기사/공시가 새 탭으로 열림 | agents/domestic-stock-analyst.md, agents/overseas-stock-analyst.md, agents/market-report-writer.md, skills/stock-report-website/SKILL.md, site/index.html | 사용자가 핵심 이슈를 클릭해 분석 근거가 된 원문으로 들어가고 싶다고 요청 |
| 2026-08-12 | 날짜별 예측 이력에 종목별 "현재가 → 목표가"(`targetPrice`/`targetBasis`) 표시 추가 — 증권사 목표주가 우선, 없으면 근거 명시한 추정 범위, 근거 없으면 생략 | agents/domestic-stock-analyst.md, agents/overseas-stock-analyst.md, skills/stock-report-website/SKILL.md, site/index.html | 사용자가 상승/하락 후보마다 지금 얼마고 얼마까지 갈 것으로 예상하는지 데이터로 채워달라고 요청 |
| 2026-08-12 | 예측 정확도 검증(정산) + 학습 루프 추가 — 종목마다 `priceAtPrediction` 기록, 장 마감 후 `domestic`/`overseas`가 종가 조회해 `hit`/`changePct` 판정, 결과를 신호 패턴 단위로 `site/lessons_domestic.md`/`lessons_overseas.md`에 축적하고 다음 분석에서 참고, 사이트 날짜 상세 화면에 SVG 적중률 차트 렌더링, 오케스트레이터에 Phase 4 "정산" 추가 | agents/domestic-stock-analyst.md, agents/overseas-stock-analyst.md, skills/stock-report-website/SKILL.md, skills/kr-market-stock-scan/SKILL.md | 예측 정확도를 사후 검증하고, 실패 신호 패턴은 버리고 성공 패턴은 누적 반영해달라는 요청 |

Update this file when the harness or project scope changes.
