# POLY Phonics — 5세 입학 학부모 홍보 페이지

빌드 없는 정적 페이지. `python3 -m http.server 5290` → http://127.0.0.1:5290/ (영상 때문에 file:// 말고 서버로 연다).

**시안 단계(2026-11-25)**: `index.html` → `concepts.html`(시안 비교)로 이동. 시안 = `concept-a.html`(3D 클레이 월드) · `concept-b.html`(모험 지도) · `concept-c.html`(팝 스티커) · `concept-d.html`(실제 화면 쇼케이스).
모두 `assets/js/site.js`(소리·그림 찾기·영상·거르기·공유) 공용 + 시안별 css/js. 썸네일 `assets/img/concepts/` ← `~/.cache/agent-scratch/promo/thumbs.py`.
빠진 시안: 처음 A(크림 무대)·처음 D(명조 잡지형) → `_archive/`. 아래 표는 처음 A 기준 콘텐츠 출처(모든 시안 공통).

| 섹션 | 내용 · 출처 |
|---|---|
| 히어로 | Phonics Land Classmate Friends(보보·타타·누누) 컷아웃, /m/ 공식 녹음 버튼 |
| 소개(Why) | 파닉스 설명 3카드 — m을 '므'로 읽는 습관 팁은 POND 레슨 데이터(efl tip) |
| 커리큘럼 | FPR K 6 Units · 30 Lessons (POND `fprk-data.js` units) · 5세 K / 6세 A / 7세 B 칩 |
| 수업 흐름 | Constella Lesson Plan 수업 순서(Meaning First · Song · 본학습 · G-Learning) + Lesson 1 섹션(POND secs, TG plan) |
| Lesson 1 맛보기 | SB p14 Say It 6그림(mop man doll heart moon mitt) 소리 분류 + 'Pour the milk in the mug.' — 그림·소리 = 레슨팩 FP.K.U1L1 |
| 체험존 | 노래: POND ABC Song + L1 Chant 1–4 (720p 재인코딩) · 정규 수업: Constella Picture Match / Trace and Write (FP.K.U1L1, devconstella) · G-Learning: Toy Catch·Phonics Puzzle(혼자), Croco Phonics(함께, 2인) |
| FAQ · CTA | 공유 버튼(navigator.share → 링크 복사) |

- 색은 `assets/css/site.css` 맨 위 `:root` 토큰만 쓴다(캐릭터 시트 팔레트).
- 인쇄: A4 가로, 히어로 = 표지, 섹션당 1쪽(체험존 3쪽) → 10쪽. 인쇄 시 FAQ 답 모두 펼침.
- 캐릭터 컷아웃: `uv run --with numpy --with scipy --with pillow python tools/cutout.py SRC OUTDIR NAME [index]` (흰 배경 → 투명, 다리 사이 흰 구멍 처리). 원본 = `../공통이미지자료/01_Phonics_Friends Guide_v1/01_Classmate_Friends`.
