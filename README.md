# PR 토론 아카이브

GitHub에서 벌어진 치열한 PR 토론을 **한글로 읽기 쉽게** 정리하는 Docusaurus 사이트입니다.

## 어떤 프로젝트인가요?

1. PR 링크를 주면 → 크롤링 스크립트가 모든 토론 데이터를 수집합니다
2. 한글로 번역/정리합니다 (원문 구조 그대로 보존)
3. 요약/분석을 추가합니다 (기술 커뮤니케이터 시점, 쉬운 말로)
4. Docusaurus 사이트에서 깔끔하게 열람합니다

## 시작하기

### 필요한 것

- Python 3
- Node.js 18+
- [GitHub CLI (`gh`)](https://cli.github.com/) — 인증 완료 상태

### 설치

```bash
git clone https://github.com/sins051301/discuss.git
cd discuss/site
npm install
```

### 사이트 실행

```bash
cd site
npm start
# http://localhost:3000 에서 열람
```

## 새 PR 추가하기

### 1단계: 크롤링

```bash
python3 fetch_pr.py https://github.com/facebook/react/pull/31715
```

`site/docs/{repo}-pr-{number}/raw.json`에 원본 데이터가 저장됩니다.

### 2단계: 번역/분석 페이지 생성

AI가 `raw.json`을 읽고 아래 두 파일을 생성합니다:

| 파일 | 내용 |
|------|------|
| `index.md` | 토론 원문을 구조 그대로 한글 번역 |
| `analysis.md` | 쟁점 정리, 배경 설명, 배울 점 분석 |

### 3단계: 확인

```bash
cd site && npm start
```

사이드바에 새 PR이 자동으로 나타납니다.

## 프로젝트 구조

```
discuss/
├── fetch_pr.py              # PR 토론 크롤링 스크립트
├── README.md
└── site/                    # Docusaurus 사이트
    ├── docusaurus.config.js
    ├── sidebars.js
    ├── src/css/custom.css
    └── docs/
        ├── intro.md                     # 홈 페이지
        ├── react-pr-31715/              # PR별 디렉토리
        │   ├── raw.json                 # 크롤링 원본
        │   ├── index.md                 # 한글 번역 정리
        │   └── analysis.md              # 요약/분석
        └── rfcs-pr-188/
            ├── raw.json
            ├── index.md
            └── analysis.md
```

## 수집하는 데이터

| 항목 | API 엔드포인트 |
|------|---------------|
| PR 메타데이터 | `GET /repos/{owner}/{repo}/pulls/{number}` |
| 일반 토론 댓글 | `GET /repos/{owner}/{repo}/issues/{number}/comments` |
| 코드 리뷰 댓글 | `GET /repos/{owner}/{repo}/pulls/{number}/comments` |
| 리뷰 | `GET /repos/{owner}/{repo}/pulls/{number}/reviews` |

모든 엔드포인트에서 페이지네이션(100건씩)을 처리합니다.

## 포함된 샘플

| PR | 토론 규모 | 내용 |
|----|----------|------|
| [react #31715](https://github.com/facebook/react/pull/31715) | 4건 | Flight 에러 분기 통합 |
| [rfcs #188](https://github.com/reactjs/rfcs/pull/188) | 281건 | React Server Components RFC (2년간 토론) |
