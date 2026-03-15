---
sidebar_label: "react PR #31715"
sidebar_position: 1
---

# [Flight] 중단(halt) 시 onError/onPostpone를 호출하지 않도록 수정하고 에러 분기를 통합

> **원문 PR**: https://github.com/facebook/react/pull/31715
> **저장소**: facebook/react | **작성자**: @sebmarkbage | **상태**: merged
> **생성일**: 2024-12-10 | **머지일**: 2024-12-10
> **변경**: +78 / -168 (5개 파일)
> **라벨**: `CLA Signed`, `React Core Team`
> **브랜치**: `flightunifyerror` → `main`

---

## PR 설명

스트림을 중단(halt)할 때 `onError`/`onPostpone`를 호출하면 안 됩니다. 해당 노드는 아직 에러가 발생한 것이 아니기 때문입니다. 또한 해당 노드의 digest도 유실될 수 있습니다.

현재 thenable과 스트림에 대한 에러 분기가 너무 많습니다. 이를 `erroredTask` 아래로 통합합니다. 에러 발생 시 task를 할당하지 않는 케이스들에 대해서는 아직 통합하지 않았습니다.

---

## 토론 내용

### @vercel\[bot\] — 2024-12-10 04:40

**Vercel 배포 상태**

| 프로젝트 | 상태 | 미리보기 | 업데이트 |
|--------|------|---------|---------|
| react-compiler-playground | Ready | [미리보기 링크](https://react-compiler-playground-git-fork-sebmarkb-9682e9-fbopensource.vercel.app) | Dec 10, 2024 4:41am |

---

### @react-sizebot — 2024-12-10 04:43

**번들 사이즈 변경 리포트**

주요 프로덕션 번들 크기에는 변화가 없었습니다 (`react-dom`, `ReactDOM` 등 모두 `=`).

다만 Flight 관련 서버 번들들에서 사이즈 감소가 확인됩니다:

| 번들 | 변경 전 | 변경 후 | gzip 변경 전 | gzip 변경 후 |
|------|---------|---------|-------------|-------------|
| react-server-flight.production.js (experimental) | 64.70 kB | 62.40 kB | 12.56 kB | 12.40 kB |
| react-server-flight.development.js (experimental) | 108.56 kB | 104.98 kB | 19.54 kB | 19.31 kB |
| react-server-dom-webpack-server.node.production.js (experimental) | 102.94 kB | 100.75 kB | 20.76 kB | 20.59 kB |

에러 분기 통합으로 인해 Flight 서버 번들 크기가 전반적으로 **약 2~3.5 kB 감소**했습니다.

---

### 리뷰

#### @gnoff — APPROVED — 2024-12-10 16:36

*(승인, 별도 코멘트 없음)*
