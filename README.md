# KBO 선수 이름 이어붙이기

한 선수의 KBO 등록명 뒤 두 글자가 다른 선수 등록명의 앞 두 글자와 같으면 겹치는 부분을 한 번만 써서
이어붙인다 (예: 최원태 + 원태인 → 최원태인). 야구나라(yagoonara.com) 선수 검색 API에서 전체 선수
데이터를 수집해 가능한 모든 조합을 찾고, 결과를 검색/필터 가능한 단일 HTML 페이지로 만든다.

## 실행 순서

```
python3 scrape.py          # data/players.json 생성 (야구나라 API에서 전체 선수 수집)
python3 subset_font.py     # assets/pretendard-subset.woff2 생성 (최초 1회만 필요)
python3 build_matches.py   # data/payload.json 생성 (이름 조합 계산)
python3 render.py          # index.html 생성 (template.html + payload.json + 폰트를 하나로 합침)
```

`data/players.json`, `assets/pretendard-subset.woff2`는 이미 이 폴더에 포함되어 있으므로,
데이터를 다시 받을 필요가 없다면 `build_matches.py`와 `render.py`만 다시 실행해도 된다.

## 파일 구성

- `scrape.py` — 야구나라 `/api/players` 에서 전체 선수 목록 수집
- `build_matches.py` — 이름 겹침 로직 + 팀/현역·은퇴/국적 메타데이터로 매치 목록 계산
- `subset_font.py` — Pretendard 가변 폰트를 이 페이지에 실제로 쓰이는 글자만 남기고 서브셋
- `template.html` — `__PAYLOAD__`/`__FONT_B64__` 플레이스홀더가 있는 페이지 템플릿 (HTML/CSS/JS)
- `render.py` — 위 세 가지를 합쳐 최종 `index.html` 생성
- `data/players.json` — 수집한 원본 선수 데이터 (5,021명)
- `data/payload.json` — 계산된 이름 조합 결과 (페이지가 그대로 읽어 렌더링하는 JSON)
- `assets/` — 서브셋된 Pretendard 폰트와 글자셋 목록
- `index.html` — 최종 결과물 (외부 요청 없이 그 자체로 완결된 단일 파일)
