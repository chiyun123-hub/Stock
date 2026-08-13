# 해외 주식 분석 - 2026-08-13 09:04 KST

## 🔴 사후 갱신 (8/12 해외 정산 완료 후, 09:2x KST) — 아래 후보 목록보다 우선해서 읽을 것

본 파일 작성 직후 8/12 해외 정산을 실행했고(6건 중 적중 3건, 50.0%), 그 결과가 **오늘 상승 후보 절반의 근거를 직접 약화시킨다.** 정산으로 확인된 패턴:

> **"이미 크게 움직인 뒤의 방향 연장" 베팅은 8/12에 2전 2패였다.**
> - PLTR: 실적 서프라이즈로 이미 급등 실현 → 추가 상승 예상 → **-2.23%**
> - ONON: 전일 -20.29% 폭락 → 추가 하락 예상 → **+0.32% 반등**
> - 상승·하락 양방향 모두 실패했으므로 방향 문제가 아니라 **패턴 자체의 문제**(평균회귀)다.

**오늘 상승 후보 중 LITE·CRWV·SMCI·GLW 4개가 정확히 이 패턴이다** — 모두 8/11 장 마감 후 실적을 발표해 8/12 정규장에서 급등이 이미 실현됐고, 8/13 판단은 모멘텀 연장에 기댄다. 본문에서 이미 "근거 강도: 중 (이미 급등 실현)"으로 낮춰뒀지만, 정산 데이터를 반영하면 **강도를 '하'로 더 낮추고 통합 리포트 상위 후보에서는 제외하는 것이 타당하다.** 4개 중 CRWV·SMCI는 시간외까지 마이너스(-1.41%, -0.77%)라 더 약하다.

반대로 정산에서 **유효성이 확인된 패턴**은 "애널리스트 등급·목표주가 상향 직후"(AKAM: UBS 상향 → +5.24%, 6건 중 최대 적중폭)와 "신호 2개 이상 일치"(단일 신호로 축소된 INTC만 실패)다. 이 기준을 오늘 목록에 적용하면 **상대적으로 신뢰할 만한 후보는 신선한 촉매 + 시간외 확인이 있는 쪽**이다:
- 상승: **HLIT**(8/12 장 마감 후 실적, 브로드밴드 +54%, 가이던스 상향, 시간외 +19.17%), CURI(동일 구조, 단 마이크로캡), CAVA
- 하락: **CBRS**(시간외 -16.53%), **SECZ**(-22.02%), **STUB**(-13.70%), **CSCO**(-5.02%), **COHR**(-5%), **APP**(52주 저점 붕괴 + 복수 등급 강등)

또한 정산에서 **"애널리스트 목표가 괴리는 당일 방향 신호로 쓸 수 없다"(2/4 동전던지기)** 가 확인됐다. 따라서 본문 NBIS 후보의 핵심 근거였던 "종가가 컨센서스 목표가를 따라잡아 상단 여력 소진"은 **근거로서 무효에 가깝다.** NBIS는 사실상 시간외 -1.97% 단일 신호만 남으므로, 패턴 3(단일 신호로 축소된 후보는 제외)에 따라 **하락 후보에서 빼는 것이 맞다.**

→ 정정된 권고: 상승 **3개**(HLIT·CURI·CAVA), 하락 **6개**(CBRS·SECZ·STUB·CSCO·COHR·APP)를 우선하고, LITE·CRWV·SMCI·GLW·NBIS·NBIX·PFGC는 참고용으로만 싣는다. 상세 근거는 `site/lessons_overseas.md` 참조.

---

## 과거 정산 반영
- 최초 작성 시점에는 `site/lessons_overseas.md` **파일 없음 → 참고할 과거 정산 없음**이었다. 작성 직후 8/12 정산을 실행해 이 파일을 신설했고, 그 결과를 위 "사후 갱신" 항목에 반영했다.
- 다만 오케스트레이터가 전달한 8/12 교훈 2건은 이번 분석에 선반영했다: (1) 거시지표는 뉴스 인용이 아니라 ECOS 원본 API를 직접 호출해 채웠다, (2) 개별 종목 등락률·가격은 뉴스 요약본을 믿지 않고 시세 원본(stockanalysis.com 종목 페이지, 종가 시각 표기 확인)에서 재검증한 값만 채택했다. 이 재검증 과정에서 실제로 뉴스 요약 오류 3건을 걸러냈다(아래 "검증에서 걸러낸 오류" 참조).

---

## 거시 맥락 (한국은행 ECOS Open API 원본 직접 호출)

**원/달러 매매기준율** — ECOS 통계표 `731Y001` (주요국 통화의 대원화환율), 항목 `0000001`, 일별
| 날짜 | 값(원) |
|---|---|
| 2026-07-30 | 1450.1 |
| 2026-07-31 | 1441.1 |
| 2026-08-03 | 1433.6 |
| 2026-08-04 | 1429.9 |
| 2026-08-05 | 1428.2 |
| 2026-08-06 | 1424.8 |
| 2026-08-07 | 1418.8 |
| 2026-08-10 | 1420.1 |
| 2026-08-11 | 1415.3 |
| 2026-08-12 | 1415.0 |

→ 2주간 **-35.1원(-2.42%) 원화 강세**. 8거래일 중 7일 하락으로 추세가 일관됨.
→ **한국 투자자 관점 함의**: 원화 강세는 해외주식 보유 시 원화 환산 수익률에 **역풍**이다. 8/12 기준 달러 자산은 환율에서만 2주간 약 -2.4%가 깎인다. 아래 후보들의 목표가·기대 변동폭은 모두 USD 기준이며, 원화 환산 시 이 환율 방향을 별도로 차감해 보아야 한다.

**한국은행 기준금리** — ECOS 통계표 `722Y001`, 항목 `0101000`, 일별
- 2026-06-01~06-10: 연 2.50%
- 2026-08-01~08-10: 연 **2.75%** (인상 반영 후 유지)

**미국 7월 CPI (8/12 발표)**: 헤드라인 +0.1% m/m, 연 3.4%(컨센서스 부합) / 코어 +0.2% m/m, 연 2.5%.
**8/12 미 정규장 마감**: 나스닥 종합 +0.54% (26,588), S&P500 +0.26% (7,749), 다우 -0.04% (53,770).

---

## ⚠️ 이번 후보 목록의 구조적 한계 (반드시 먼저 읽을 것)

이번 상승/하락 후보는 **상당 부분이 하나의 동일한 변수**에 걸려 있다. 서로 독립적인 베팅이 아니다.

- 상승 후보 중 LITE·CRWV·SMCI·GLW는 **8/11 장 마감 후 실적 발표 → 8/12 정규장에서 이미 급등이 실현된** 종목이다. 8/13에 대한 판단은 "모멘텀 연장"이라는 **약한 근거**에 기댄다.
- 하락 후보 중 CBRS·COHR·CSCO는 **8/12 장 마감 후 실적을 발표했고, 실적·가이던스가 컨센서스를 상회했음에도 시간외에서 하락**했다.
- 즉 두 목록은 결국 같은 관찰("AI 인프라 실적은 강하지만 주가가 기대치를 이미 선반영") 의 앞면과 뒷면이다. **AI 인프라 섹터 전반이 8/13에 차익실현으로 돌면 상승 후보가 함께 무너지고, 반대로 강세가 이어지면 하락 후보 중 CBRS·COHR·CSCO가 함께 회복한다.**
- 따라서 상승 목록의 AI 인프라 4종목(LITE·CRWV·SMCI·GLW)과 하락 목록의 AI 3종목(CBRS·COHR·CSCO)은 **묶음 1개짜리 베팅으로 취급**해야 하며, 개수만큼의 분산 효과가 없다.
- 상대적으로 이 변수에서 독립적인 후보: 상승 HLIT·CURI·CAVA / 하락 APP·NBIX·PFGC·STUB·SECZ.

---

## 상승 가능성이 관측되는 후보 (7개)

> 기준가는 모두 **미국 정규장 종가 기준 2026-08-12** (4:00 PM EDT), 시세 원본에서 종가 시각을 직접 확인함.

### 1. Harmonic (HLIT) — 근거 강도: 상
- `priceAtPrediction`: **12.00 USD** / `priceAtPredictionTime`: 미국 정규장 종가 기준 2026-08-12
- 시간외 14.30달러 (+19.17%, 8/12 장 마감 후)
- 근거①: 8/12 Q2 실적에서 **브로드밴드 매출 전년비 +54% 사상 최대**, 수주 호조를 이유로 연간 가이던스 상향
- 근거②: 시간외 +19.17%로 시장 반응이 즉각 확인됨 (정규장 종가 대비 갭업 상태로 8/13 개장 예상)
- 근거③: 비디오 사업 매각 완료로 브로드밴드 순수 사업자로 전환 — 구조적 마진 개선 스토리
- `targetPrice`: **15.29 USD** / `targetBasis`: 애널리스트 컨센서스 목표주가 (7인, Buy), stockanalysis.com 집계 2026-08-12 기준
- `sourceUrl`: https://stockanalysis.com/stocks/hlit/
- `sourceTitle`: Harmonic Inc. (HLIT) Stock Price, Quote & After-Hours — StockAnalysis

### 2. CuriosityStream (CURI) — 근거 강도: 중 (마이크로캡 주의)
- `priceAtPrediction`: **2.80 USD** / `priceAtPredictionTime`: 미국 정규장 종가 기준 2026-08-12
- 시간외 4.00달러 (+42.86%, 8/12 19:59 EDT)
- 근거①: 8/12 Q2에서 **순이익 사상 최대**, 라이선싱 매출 1,410만 달러 **+48%**(신규 파트너십 기여), 연간 매출·조정 EBITDA 가이던스 상향
- 근거②: 시간외 +42.86%
- `targetPrice`: **5.33 USD** / `targetBasis`: 애널리스트 컨센서스 (3인, Buy) — **커버리지 3인뿐이라 신뢰도 낮음**. 시간외가 4.00달러이므로 단기 현실적 저항선은 4달러 초반대로 보는 편이 타당
- `sourceUrl`: https://stockanalysis.com/stocks/curi/
- `sourceTitle`: CuriosityStream Inc. (CURI) Stock Price, Quote & After-Hours — StockAnalysis
- ⚠️ 시가총액 1.66억 달러 마이크로캡. 시간외 유동성이 얇아 정규장 갭이 유지되지 않을 위험이 큼

### 3. Lumentum (LITE) — 근거 강도: 중 (이미 급등 실현)
- `priceAtPrediction`: **932.47 USD** / `priceAtPredictionTime`: 미국 정규장 종가 기준 2026-08-12
- 8/12 정규장 +13.63% (+111.88달러)
- 근거①: FY4Q 매출 **10.1억 달러로 전년비 2배 이상**, CEO가 펌프 레이저 출하 **+80% YoY, 사실상 완판** 언급
- 근거②: JP모건 목표주가 **1,165 → 1,280달러 상향(Overweight)**
- `targetPrice`: **1,148.30 USD** / `targetBasis`: 애널리스트 컨센서스 (24인, Buy), stockanalysis.com 2026-08-12 기준 / 개별 최고치는 JPMorgan 1,280달러
- `sourceUrl`: https://finance.yahoo.com/markets/stocks/articles/lumentum-rockets-15-blowout-earnings-172227881.html
- `sourceTitle`: Lumentum Rockets 15% on Blowout Earnings, Coherent Climbs 9%, Corning Gains 5% on Optics Earnings
- ⚠️ 상단 "구조적 한계" 묶음에 포함

### 4. CoreWeave (CRWV) — 근거 강도: 중 (이미 급등 실현)
- `priceAtPrediction`: **107.73 USD** / `priceAtPredictionTime`: 미국 정규장 종가 기준 2026-08-12
- 8/12 정규장 +19.28% (+17.41달러)
- 근거①: 2Q 매출 25.8억 달러, **전년비 +112%**, 신규 계약 250억 달러
- 근거②: **수주잔고 1,042억 달러**(전분기 994억 달러 대비 +48억) — 하이퍼스케일러 capex 지속의 직접 증거. capex·2026 매출 가이던스 동반 상향
- `targetPrice`: **142.54 USD** / `targetBasis`: 애널리스트 컨센서스 (38인, Buy), stockanalysis.com 2026-08-12 기준
- `sourceUrl`: https://finance.yahoo.com/markets/article/ai-infrastructure-stocks-surge-after-strong-earnings-from-coreweave-supermicro-142304399.html
- `sourceTitle`: AI infrastructure stocks surge after strong earnings from CoreWeave, Supermicro
- ⚠️ 상단 "구조적 한계" 묶음에 포함. 2025년 순손실 12.0억 달러로 적자 지속
- ⚠️ **시간외 106.21달러 (-1.41%, 8/12 19:59 EDT)** — 상승 후보로서 약한 역신호
- 📌 **기준가 검증 노트**: CRWV는 8/12 리포트에서 "장 마감 후 촉매로 기준가 왜곡"(기준가 90.32달러가 8/11 종가로, 실적·시간외 +13% 발생 前 가격) 사유로 정산 영구 제외된 종목이다. 오늘 기준가 107.73달러는 **그 촉매를 8/12 정규장이 통째로 소화한 뒤의 종가**이므로(90.32 → 107.73 = 정확히 +19.28%) 동일 왜곡이 없다. 8/12 장 마감 후 신규 실적·가이던스·계약 공시가 없고 논평 기사(TipRanks/CNBC/WSJ)뿐임을 시세 원본에서 확인했다. `priceBasis` 정의("촉매 반영 후, 예측 시점 마지막 체결가")와 일치하며 정상 정산 대상이다. 다만 근거 성격이 어제(신선한 촉매)와 달리 오늘은 **모멘텀 연장**이라 강도를 중으로 뒀다.

### 5. Super Micro Computer (SMCI) — 근거 강도: 중 (이미 급등 실현)
- `priceAtPrediction`: **37.61 USD** / `priceAtPredictionTime`: 미국 정규장 종가 기준 2026-08-12
- 8/12 정규장 +19.02% (+6.01달러), 시간외 37.32달러 (-0.77%)
- 근거①: FY4Q 조정 EPS **1.70달러(컨센 1.59달러 상회)**, 총마진 17.6%로 컨센서스를 892bp 상회. **FY27 매출 가이던스 650~720억 달러**로 컨센서스 대폭 상회, 신규 수주 600억 달러 이상
- 근거②: 복수 하우스 목표가 상향 — Bernstein SocGen 37→**42달러**(Market Perform), Rosenblatt 40→**45달러**(Buy)
- `targetPrice`: **41.75 USD** / `targetBasis`: 애널리스트 컨센서스 (19인, **Hold**), stockanalysis.com 2026-08-12 기준
- `sourceUrl`: https://stocktwits.com/news-articles/markets/equity/smci-stock-eyes-1-month-high-as-analysts-lift-price-targets-caution-margins-not-sustainable/cZo8RzHRJgF
- `sourceTitle`: SMCI Stock Eyes 1-Month High As Analysts Lift Targets After Earnings, But Caution AI Server Margins 'Not Sustainable'
- ⚠️ **상충 신호**: 매출은 컨센서스(112.6억)를 소폭 하회한 111.2억 달러였고, 컨센서스 등급이 Hold이며 애널리스트들이 "AI 서버 마진 지속 불가" 경계를 명시했다. 시간외도 소폭 마이너스. 근거 강도를 중으로 낮춘 이유.

### 6. Corning (GLW) — 근거 강도: 중
- `priceAtPrediction`: **167.44 USD** / `priceAtPredictionTime`: 미국 정규장 종가 기준 2026-08-12
- 8/12 정규장 +5.18% (+8.25달러), 시간외 167.68달러 (+0.14%)
- 근거①: LITE·COHR 광부품 실적 서프라이즈의 read-through로 광통신 수요 확인
- 근거②: 직전 실적 후 -18% 급락했던 구간에서 회복 중이며, 복수 애널리스트가 목표가는 낮췄으나 매수 등급을 유지하며 "낙폭 과다" 평가
- `targetPrice`: **191.40 USD** / `targetBasis`: 애널리스트 컨센서스 (16인, Buy), stockanalysis.com 2026-08-12 기준
- `sourceUrl`: https://247wallst.com/investing/2026/08/12/lumentum-rockets-15-on-blowout-earnings-coherent-climbs-9-corning-gains-5-on-optics-earnings-and-coreweave-super-micro-read-through/
- `sourceTitle`: Lumentum Rockets 15% on Blowout Earnings, Coherent Climbs 9%, Corning Gains 5% on Optics Earnings
- ⚠️ 상단 "구조적 한계" 묶음에 포함. P/E 77배로 밸류에이션 부담

### 7. CAVA Group (CAVA) — 근거 강도: 중
- `priceAtPrediction`: **69.47 USD** / `priceAtPredictionTime`: 미국 정규장 종가 기준 2026-08-12
- 8/12 정규장 +14.24% (+8.66달러)
- 근거①: 2Q 매출 3.654억 달러, **동일점포 매출 +9%, 방문객 트래픽 +5.3%** — 사이클로스포라(상추 공급처) 이슈에도 불구한 수치
- 근거②: 2026년 75~77개 신규 출점 계획 유지, 연간 조정 EBITDA 가이던스 1.81~1.91억 달러 재확인
- `targetPrice`: **89.08 USD** / `targetBasis`: 애널리스트 컨센서스 (27인, Buy), stockanalysis.com 2026-08-12 기준
- `sourceUrl`: https://investrade.com/mid-morning-look-august-12-2026/
- `sourceTitle`: Mid-Morning Look: August 12, 2026 — Investrade
- ✅ AI 인프라 변수에서 독립적인 후보

---

## 하락 가능성이 관측되는 후보 (9개)

> 기준가는 모두 **미국 정규장 종가 기준 2026-08-12** (4:00 PM EDT).

### 1. Cerebras Systems (CBRS) — 근거 강도: 상
- `priceAtPrediction`: **262.06 USD** / `priceAtPredictionTime`: 미국 정규장 종가 기준 2026-08-12
- 8/12 정규장 +11.63%, **시간외 218.75달러 (-16.53%)**
- 근거①: 8/12 Q2에서 매출 +103% YoY·마진 개선에도 **분기 순손실 4.505억 달러**(전년 동기는 흑자) — 성장 대비 손실 확대
- 근거②: 시간외 -16.53%로 시장이 즉각 부정 반응. 정규장 종가가 컨센서스 목표주가 292달러에 근접(-10%)해 상단 여력이 얇았던 상태
- `targetPrice`: **218~230 USD 구간** / `targetBasis`: **추정** (근거: 8/12 시간외 체결가 218.75달러가 8/13 정규장 갭다운 기준선. 컨센서스 292달러는 실적 전 수치라 하락 시나리오 기준으로 부적합)
- `sourceUrl`: https://stockanalysis.com/stocks/cbrs/
- `sourceTitle`: Cerebras Systems (CBRS) Stock Price, Quote & After-Hours — StockAnalysis
- ⚠️ 상단 "구조적 한계" 묶음에 포함

### 2. Securitize (SECZ) — 근거 강도: 중상
- `priceAtPrediction`: **7.86 USD** / `priceAtPredictionTime`: 미국 정규장 종가 기준 2026-08-12
- 8/12 정규장 +6.36%, **시간외 6.13달러 (-22.02%)**
- 근거①: 8/12 Q2 실적 발표 후 시간외 -22.02%
- 근거②: 매출은 +724.5% 급증했으나 **순손실 5,126만 달러** 지속. 52주 저점 6.04달러에 시간외 가격이 근접
- `targetPrice`: **6.10~6.50 USD 구간** / `targetBasis`: **추정** (근거: 시간외 체결가 6.13달러 + 52주 저점 6.04달러가 지지선. 컨센서스 15.00달러는 실적 전 수치)
- `sourceUrl`: https://stockanalysis.com/stocks/secz/
- `sourceTitle`: Securitize Corp. (SECZ) Stock Price, Quote & After-Hours — StockAnalysis
- ✅ AI 인프라 변수에서 독립적

### 3. StubHub Holdings (STUB) — 근거 강도: 중상
- `priceAtPrediction`: **8.54 USD** / `priceAtPredictionTime`: 미국 정규장 종가 기준 2026-08-12
- 8/12 정규장 +4.27%, **시간외 7.37달러 (-13.70%)**
- 근거①: 2Q에서 **월드컵 특수로 매출·GMS 사상 최대에도 순손실** 기록 — 비용 증가가 매출 증가를 상쇄. 최대 이벤트를 치르고도 흑자 전환 실패라는 점이 구조적 우려
- 근거②: 시간외 -13.70%. TTM 순손실 18.6억 달러, 52주 고점 27.89달러 대비 -69% 구간
- `targetPrice`: **7.30~7.60 USD 구간** / `targetBasis`: **추정** (근거: 시간외 체결가 7.37달러. 컨센서스 13.38달러는 실적 전 수치라 하락 시나리오에 부적합)
- `sourceUrl`: https://stockanalysis.com/stocks/stub/
- `sourceTitle`: StubHub Holdings (STUB) Stock Price, Quote & After-Hours — StockAnalysis
- ✅ AI 인프라 변수에서 독립적

### 4. Cisco Systems (CSCO) — 근거 강도: 중상
- `priceAtPrediction`: **123.88 USD** / `priceAtPredictionTime`: 미국 정규장 종가 기준 2026-08-12
- 8/12 정규장 +2.86% (+3.45달러), **시간외 118.86달러 (-5.02%)**
- 근거①: FY4Q EPS **1.22달러로 컨센서스 1.13달러를 7.96% 상회**하고 가이던스도 상회했음에도 시간외 -5.02% — 전형적인 "재료 소멸" 반응
- 근거②: 연초 대비 시총 +74.5%, P/E 41.29배로 네트워크 장비주로서 이례적 밸류에이션. 정규장 종가 123.88달러가 시장이 주목하던 124.62달러 저항선 바로 아래에서 막힌 상태
- `targetPrice`: **118.50~120.00 USD 구간** / `targetBasis`: **추정** (근거: 시간외 체결가 118.86달러가 8/13 갭다운 기준선. 참고로 컨센서스는 132.59달러(26인, Buy)로 실적 전 수치이며 방향이 반대)
- `sourceUrl`: https://stockanalysis.com/stocks/csco/
- `sourceTitle`: Cisco Systems (CSCO) Stock Price, Quote & After-Hours — StockAnalysis
- ⚠️ 상단 "구조적 한계" 묶음에 포함

### 5. Coherent (COHR) — 근거 강도: 중상
- `priceAtPrediction`: **355.64 USD** / `priceAtPredictionTime`: 미국 정규장 종가 기준 2026-08-12
- 8/12 정규장 +8.24% (+27.07달러), **시간외 약 -5%**
- 근거①: FY4Q 매출 20.5억 달러(**+33.8% YoY**, 컨센 19.8억 상회), 조정 EPS 1.74달러(컨센 1.62달러 상회), FY27 1Q 가이던스 22~24억 달러로 공격적. **그럼에도 시간외 -5%**
- 근거②: 실적 발표 전 정규장에서 이미 +8.24% 선반영. P/E 148.46배, 시총 전년비 +294%로 기대치가 극단적으로 높은 상태
- `targetPrice`: **335~340 USD 구간** / `targetBasis`: **추정** (근거: 시간외 -5% 적용 시 약 338달러. 컨센서스 394.62달러(21인, Buy)는 실적 전 수치)
- `sourceUrl`: https://www.investing.com/news/stock-market-news/coherent-posts-a-blowout-q4-and-aggressive-guidance-yet-shares-take-a-5-haircut-4856014
- `sourceTitle`: Coherent posts a blowout Q4 and aggressive guidance, yet shares take a 5% haircut
- ⚠️ 상단 "구조적 한계" 묶음에 포함

### 6. AppLovin (APP) — 근거 강도: 상
- `priceAtPrediction`: **303.76 USD** / `priceAtPredictionTime`: 미국 정규장 종가 기준 2026-08-12
- 8/12 정규장 -4.68%, 시간외 305.43달러 (+0.55%)
- 근거①: 2Q 매출 19.24억 달러로 컨센 19.35억 하회 — **2021년 상장 이후 첫 매출 미스**이자 자체 가이던스 중간값 첫 미달(Piper Sandler). 3Q 가이던스 20.7억 달러도 컨센 20.8억 하회
- 근거②: **복수 하우스 등급 강등 및 목표가 대폭 하향** — BofA Neutral 강등, Wells Fargo·Piper Sandler 강등, Benchmark 775→500달러, Scotiabank 775→515달러
- 근거③: 8/12 종가 303.76달러가 **52주 저점 303.17달러에 사실상 붙은 상태**(연중 -45.8%, 52주 고점 745.61달러 대비 -59%) — 기술적 지지선 붕괴 임박
- `targetPrice`: **285~300 USD 구간** / `targetBasis`: **추정** (근거: 52주 저점 303.17달러 하향 이탈 시 다음 지지 부재. 컨센서스 553.47달러는 하향 조정이 아직 다 반영되지 않은 후행 집계라 참고 불가로 판단)
- `sourceUrl`: https://seekingalpha.com/news/4627857-applovin-breaks-investors-hearts-with-20-percent-drop-after-q2-results-receives-multiple
- `sourceTitle`: AppLovin breaks investors' hearts with 20% drop after Q2 results; receives multiple downgrades
- ✅ AI 인프라 변수에서 독립적
- ⚠️ **상충 신호**: 시간외 +0.55%로 소폭 반등. 이미 -45% 하락한 상태라 기술적 반등 여지도 존재

### 7. Nebius Group (NBIS) — 근거 강도: 중
- `priceAtPrediction`: **259.20 USD** / `priceAtPredictionTime`: 미국 정규장 종가 기준 2026-08-12
- 8/12 정규장 **+34.14%**, 시간외 254.10달러 (-1.97%)
- 근거①: 2Q 매출 5.823억 달러(**+454% YoY**)로 실적 자체는 강했으나, 하루 +34.14% 급등으로 **정규장 종가가 애널리스트 컨센서스 목표주가 261.44달러를 사실상 따라잡음(잔여 상단 +0.86%)** — 밸류에이션 여력 소진
- 근거②: 시간외 -1.97%로 급등 직후 차익실현 시작. P/E 1,578배, 시총 전년비 +304.2%
- `targetPrice`: **250~256 USD 구간** / `targetBasis`: **추정** (근거: 시간외 체결가 254.10달러 + 컨센서스 261.44달러가 상단 캡으로 작용)
- `sourceUrl`: https://stockanalysis.com/stocks/nbis/
- `sourceTitle`: Nebius Group (NBIS) Stock Price, Quote & After-Hours — StockAnalysis
- ⚠️ **상충 신호 큼**: 실적 펀더멘털은 명백히 강하다. 이 후보는 "실적이 나쁘다"가 아니라 "하루 +34% 급등 후 목표가 소진"이라는 순수 기술적·밸류에이션 근거에만 의존한다. 근거 강도를 중으로 제한한 이유.

### 8. Neurocrine Biosciences (NBIX) — 근거 강도: 중
- `priceAtPrediction`: **156.49 USD** / `priceAtPredictionTime`: 미국 정규장 종가 기준 2026-08-12
- 8/12 정규장 -3.37% (-5.45달러), 시간외 156.06달러 (-0.27%)
- 근거①: 프래더-윌리 증후군 전문가들이 자사 희귀질환 치료제 **Vykat XR 관련 사망 7건 보고**를 근거로 안전성 우려 제기 — 규제 이슈로 확대될 경우 다단계 하락 가능성
- 근거②: 8/12 정규장 -3.37% 및 시간외 추가 약세로 시장 반응 확인. 안전성 이슈는 통상 1일에 소화되지 않고 며칠에 걸쳐 반영됨
- `targetPrice`: **148~154 USD 구간** / `targetBasis`: **추정** (근거: 안전성 이슈 지속 시 직전 지지 구간. 컨센서스 213.13달러(27인, Strong Buy)는 이슈 반영 전 수치)
- `sourceUrl`: https://investrade.com/mid-morning-look-august-12-2026/
- `sourceTitle`: Mid-Morning Look: August 12, 2026 — Investrade
- ✅ AI 인프라 변수에서 독립적
- ⚠️ 주력 제품 INGREZZA는 별개로 긍정적 데이터(KINECT-PRO) 발표, 매출 +34.4%·순이익 +102.6%로 펀더멘털은 견조

### 9. Performance Food Group (PFGC) — 근거 강도: 중
- `priceAtPrediction`: **107.41 USD** / `priceAtPredictionTime`: 미국 정규장 종가 기준 2026-08-12
- 8/12 정규장 -5.75% (-6.55달러)
- 근거①: FY4Q 조정 EPS 1.59달러로 컨센 1.60달러 하회, 매출 180억 달러로 컨센 180.9억 하회
- 근거②: **가이던스 이중 하회** — FY27 1Q 매출 179~181억 달러(컨센 181.3억 하회), FY27 연간 725~730억 달러(컨센 726.8억 하회)
- `targetPrice`: **102~106 USD 구간** / `targetBasis`: **추정** (근거: 8/12 -5.75% 갭다운 후 가이던스 하회 소화 구간. 컨센서스 123.31달러(14인, Buy)는 실적 전 수치)
- `sourceUrl`: https://investrade.com/mid-morning-look-august-12-2026/
- `sourceTitle`: Mid-Morning Look: August 12, 2026 — Investrade
- ✅ AI 인프라 변수에서 독립적
- ⚠️ 상충 신호: 매출 +13.3%, 전 사업부 점유율 확대 등 펀더멘털은 양호. 하락폭이 8/12에 이미 상당 부분 반영됐을 수 있음

---

## 검증에서 걸러낸 오류 (뉴스 요약 ≠ 시세 원본)

8/12 교훈을 적용해 시세 원본과 대조한 결과 다음을 걸러냈다. 후보 목록에 반영하지 않았거나 방향을 뒤집었다.

1. **"8/12 S&P500이 0.3% 하락해 7,728.20으로 마감, AppLovin -6%가 최대 하락"** — 이는 실제로 **8/11 세션** 수치다. 8/12 실제 종가는 7,749(+0.26%)로, 7,728 → 7,749가 정확히 +0.27%로 맞아떨어져 하루 밀린 리캡임을 확인했다. **AppLovin -6%도 8/11 수치**이며 8/12 실제 등락률은 -4.68%다. 이 값으로 정정해 반영했다.
2. **"NBIS가 8/13 프리마켓에서 +16%"** — 시세 원본 확인 결과 NBIS는 **8/12 정규장에 이미 +34.14%로 마감**했고 시간외는 -1.97%였다. 해당 +16%/+20%는 8/12 장중 수치였다. 이 정정 때문에 NBIS를 상승 후보에서 **하락 후보로 이동**시켰다(목표가 소진).
3. **Coherent(COHR)를 상승 후보로 분류할 뻔한 건** — 8/12 정규장 +8.24%만 보면 상승 후보지만, COHR은 **8/12 장 마감 후** 실적을 발표했고 블로우아웃 실적에도 시간외 -5%였다. 시간외 확인이 없었으면 방향을 반대로 적을 뻔했다. **하락 후보로 분류**.

추가로 근거 상충으로 **제외**한 종목: ATRO(+17.33%, 종가 87.89달러이나 컨센서스 목표주가 85.38달러가 현재가보다 **낮음** → 상단 여력 부재), HRB(+16.09%, 종가 54.18달러이나 컨센서스 목표주가 46.67달러로 현재가보다 낮고 등급 Hold).

---

## 팀 협업 기록

- **→ `domestic`으로 발신 (09:0x KST)**: ECOS 원본 기준 원/달러 2주 추이(1450.1 → 1415.0, -2.42% 원화 강세), 기준금리 2.75%, 미국 7월 CPI 및 8/12 마감 지수, AI 인프라/광통신 어닝 서프라이즈 클러스터(CRWV 수주잔고 1,042억 달러 / SMCI FY27 가이던스 / LITE 펌프레이저 완판, 동반 COHR·GLW)의 국내 read-through(HBM·광모듈·FC-BGA·전력/냉각 협력사) 공유. 단 원화 강세(수출주 환산 역풍)와 AI 수요 강세가 서로 상충하므로 두 신호를 독립 카운트하지 말고 순효과로 볼 것을 함께 권고.
- **← `domestic`으로부터 수신 (09:3x KST)**: 국내발 교차 확인 요청 3건을 받아 조사 후 회신했다. **후보 목록 반영 여부: 3건 모두 해외 후보 목록 자체를 바꾸지는 않았다**(국내 종목 판단용 질의였고, 조사 결과가 해외 후보의 채택·배제 근거와 겹치지 않았기 때문). 다만 조사 과정에서 확인한 사실은 아래와 같고, 향후 해외 분석에 쓸 수 있어 기록한다.
  1. **AI 서버 부품(MLCC·FC-BGA) 섹터 리레이팅 확인** — Ibiden 8월 초 FY26 전망 상향(생성형 AI 수요 상회), Murata FY26 캐펙스 2,500억 엔 중 800억 엔을 서버용 MLCC 증설에 추가 배정(AI 서버는 MLCC를 일반 서버의 13배 사용, 리드타임 24주), 업계 전반 가격 인상(삼성전기 5월 15~20%, Taiyo Yuden 2Q 15~25%, TDK 협상 중). → 오늘 상승 후보의 AI 인프라 테마와 **같은 축**이므로 독립 신호가 아니다. "구조적 한계" 섹션의 묶음 경고를 오히려 강화하는 정보다.
  2. **바이오텍·2차전지 글로벌 이탈은 반증됨** — XBI $159.39 **+0.84%**, LIT $75.21 **+1.48%** (둘 다 Aug 12, 2026, 4:00 PM EDT 종가, 시세 원본 확인). 미국 바이오텍은 1년 총수익률 +88.02%로 강세다. 국내에서 관측된 바이오·2차전지 이탈은 **한국 국한 수급 현상**이라고 회신했고, `domestic`의 알테오젠 후보 근거를 낮추도록 권고했다.
  3. **나토·미 해군 조달 지연은 실재** — 독일 F126 프리깃 취소(26년 6월), 네덜란드 대잠 프리깃 3년 지연(26년 5월, 2033년 이후), 미 해군 DDG-51 누적 25개월·버지니아급 평균 4년 지연. 단 이는 유럽·미국 자체 프로그램이며 **한국 조선사 수주분의 취소·지연이 확인된 것은 아니라는 점**을 명확히 구분해 회신했다(MASGA 진행, HJ중공업 첫 미 MRO 수주, 미 해군 MRO 시장 2030년 80~120억 달러 확대 전망 등 반대 신호 병존).
  - ⚠️ 조사 중 검색 요약본에서 "8월 반도체 ETF 자금 이탈(SOXL -15억 달러, Applied Materials 실적 실망)" 자료가 나왔으나 **2025년 자료**여서 채택하지 않았다. 오늘 반복 확인된 오류 유형이다.

- **8/12 해외 정산 (완료, 09:2x KST)**: `site/data.json` 8/12 항목의 해외 6건에 종가·등락률·적중 여부를 기입하고 `verified.overseas: true`로 변경했다(백업 `data.json.bak4`). **적중 3/6 (50.0%)** — 상승 AKAM 적중·PLTR 실패, 하락 GOOGL·UAL 적중·ONON·INTC 실패. CRWV는 기준가 왜곡으로 정산 영구 제외 유지. `site/lessons_overseas.md`를 신설해 신호 패턴 5개를 기록했고, 그 결과를 본 파일 최상단 "🔴 사후 갱신"에 반영했다.
- **↔ `reportwriter`와 교신**: 완료 통보 후 CRWV 관련 확인 질의를 받았다("어제 정산 영구 제외된 종목이 오늘 재등장했는데 기준가 왜곡이 없는 게 맞나"). 시세 원본에서 CRWV 8/12 시간외(106.21달러, -1.41%)와 마감 후 신규 공시 부재를 재확인해 **왜곡 없음**으로 답했고, 위 "기준가 검증 노트"를 신설했다. 아울러 (a) 오늘 근거는 신선한 촉매가 아니라 모멘텀 연장이라는 점, (b) 시간외 -1.41%가 약한 역신호라는 점, (c) CRWV를 LITE·SMCI·GLW와 함께 AI 인프라 묶음으로 묶어 통합 상위 10개에서 과다 선정되지 않게 할 것을 각주로 요청했다.
- **8/12 해외 정산 (미실행, 예정)**: `reportwriter`로부터 8/12 국내 정산 결과(13건 중 8건 적중, 61.5%)를 공유받았다. 해외 6건(PLTR·AKAM·ONON·GOOGL·INTC·UAL, CRWV는 영구 제외)은 **8/12 미국 정규장 세션 종가** 기준으로 정산 예정이다(8/12 항목의 해외 기준가가 8/11 종가이므로 대상 거래일은 8/12 세션). 정산 시 `site/lessons_overseas.md`를 신설해 신호 패턴별 교훈을 축적한다.

---

## 참고

- **데이터 기준 시각**: 2026-08-13 09:04 KST = 2026-08-12 20:04 EDT (미국 정규장 마감 후 시간외 거래 시간대)
- **모든 기준가(`priceAtPrediction`)는 2026-08-12 미국 정규장 종가**이며, 시세 원본 페이지에서 "Aug 12, 2026, 4:00 PM EDT" 종가 시각을 개별 확인했다.
- **시간외 가격은 참고 신호로만 사용**했으며 기준가로 쓰지 않았다. 시간외 체결은 유동성이 얇아 8/13 정규장 시가와 괴리될 수 있다.
- 거시지표(환율·기준금리)는 한국은행 ECOS Open API(`https://ecos.bok.or.kr/api/StatisticSearch/...`)를 **직접 호출한 원본 값**이며 뉴스 인용이 아니다.
- 해외 데이터는 국내 대비 실시간성이 낮다(시차 13시간, 정보 접근성 제약). 특히 8/13 미국 정규장은 KST 22:30에 개장하므로, 본 분석 시점 이후 프리마켓에서 상황이 바뀔 수 있다.
- **누락된 데이터**: COHR의 정확한 시간외 체결가(-5%라는 보도 수치만 확보, 시세 원본에서 숫자 미확인), 8/12 시간외 손실 상위 종목 전체 목록(상위 5개만 확보되어 CBRS가 목록에 노출되지 않음 — CBRS는 개별 종목 페이지에서 직접 확인).
- **이는 확정된 예측이 아니라 공개 정보 기반 참고용 스크리닝이다.** 매수·매도 추천이 아니다. 각 종목은 "상승/하락 가능성이 관측됨" 수준의 서술이며, 특히 상단 "구조적 한계" 항목에 적었듯 후보 개수만큼의 독립성이 없다.
