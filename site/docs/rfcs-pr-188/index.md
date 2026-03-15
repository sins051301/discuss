---
sidebar_label: "rfcs PR #188 — React Server Components"
sidebar_position: 1
---

# RFC: React Server Components

> **원문 PR**: https://github.com/reactjs/rfcs/pull/188
> **저장소**: reactjs/rfcs | **작성자**: @josephsavona | **상태**: merged
> **생성일**: 2020-12-21 | **머지일**: 2022-10-25
> **변경**: +609 / -0 (1개 파일) | **토론**: 199 댓글 + 42 리뷰 코멘트 + 40 리뷰
> **라벨**: `CLA Signed`, `react core team`
> **주요 참여자**: @gaearon (22), @josephsavona (16), @brillout (13), @wmertens (12), @Ephem (4), @Daniel15 (3), @markerikson (2), @ShanonJackson (2), @dfabulich (1) 외 다수

---

## PR 설명

이 RFC에서 우리는 React에 Server Components를 도입할 것을 제안합니다. **이 RFC를 읽기 전에 Server Components를 소개하는 우리의 발표 영상을 시청하는 것을 권장합니다.**

---

## 토론 내용

### @Daniel15 — 2020-12-21

서버 사이드가 Node.js에 강하게 결합될 건가요, 아니면 다른 JS 런타임(예: Java의 Rhino, C#의 ClearScript에 내장된 V8, ChakraCore 등)에서도 실행할 수 있나요? RFC에서 Node에 대한 유일한 언급은 디버깅 관련("Node에서 API를 디버깅한다")인데, 서버 사이드 컴포넌트가 Node에 강하게 결합되는지 여부는 불명확합니다.

JavaScript의 주요 이점이자 인기의 이유 중 하나는 많은 곳에서 실행된다는 점이므로, 하나의 특정 구현에 결합하는 것은 아쉬울 것입니다.

---

### @josephsavona (React 팀) — 2020-12-21

React Server Components는 개념적으로 JS 런타임과 분리되어 있지만, 어느 정도의 환경별 통합도 필요합니다. 예를 들어, 현재 일반 사용을 위한 Node.js 통합(데모에서 사용됨)과 Relay를 위한 내부 통합을 지원합니다. 다른 환경에 대한 지원 추가를 고려할 수 있으며, 어떤 것을 우선시해야 하는지에 대한 커뮤니티의 피드백에 관심이 있습니다.

---

### @markerikson — 2020-12-21

@josephsavona 그 질문의 나머지 반쪽: 백엔드가 JS 기반이 _아닌_ 경우(즉, Python, Java, Go 등) 이 서버 기능이 얼마나 실현 가능한가요?

---

### @josephsavona (React 팀) — 2020-12-21

이것은 잠재적인 미래 탐구를 위한 흥미로운 영역입니다. Server Components의 응답 프로토콜("슬롯이 있는 스트리밍 JSON")을 계속 반복하고 있으며, 이를 표준화할 준비가 아직 되지 않았습니다. 요약하면, 흥미로운 아이디어이지만 아직 시기상조로 느껴집니다.

---

### @dfabulich — 2020-12-21 — 주요 쟁점: async/await

FAQ의 "왜 async/await를 사용하지 않나요" 섹션에 대해 **잘못된 결정을 내렸다고 생각합니다.**

현재 코드는 _매우 놀라운_ 패턴을 사용합니다: 결과값이 캐시되어 있으면 동기적으로 값을 반환하지만, 그렇지 않으면 페처가 _Promise를 throw합니다_. async/await를 사용하면 이 코드를 이해하기 훨씬 쉬워질 것입니다.

---

### @ShanonJackson — 2020-12-21 — 주요 비판: 복잡성

이런 API를 도입하면 SSR을 사용하는 사람들은 이제 1가지 대신 **3가지 종류의 컴포넌트**(서버/클라이언트/이소모픽)를 생각해야 합니다. hooks를 사랑한 이유는 현재 React 프로젝트에서 스케일을 방해하는 **진짜 문제**를 해결했기 때문입니다. 반면 이것은 현재 직면하고 있는 진짜 문제를 해결하지 못합니다.

---

### @brillout — 2020-12-28 — 대안 제안

Client Components가 Server Components를 import할 수 없다는 제한이 복잡성의 원인입니다. 이 제한을 완화하는 대안을 제안합니다.

---

### @josephsavona (React 팀) — 2021-01-05 — 핵심 설계 결정

**왜 CC에서 SC Import를 금지하나요?** CC가 SC를 렌더링하려면 CC의 state를 서버에 보내야 합니다. 하지만 state는 직렬화 가능하다고 보장할 수 없습니다(Symbol, 클래스 인스턴스, 클로저 등). 수천 행의 데이터를 state에 보유하는 것은 매우 일반적이고, 이를 매 요청마다 직렬화해서 서버로 보내는 것은 비현실적입니다.

---

### @gaearon (React 팀) — 2021-01-03 — 프레임 비유로 라우팅 설명

각 "콘텐츠 영역"(탭 바 같은)이 실제로 "프레임"의 컨테이너라고 상상할 수 있습니다. 탭을 바꾸면 해당 "프레임"의 Server Component 트리를 새로 페치합니다. 각 "프레임"은 독립적인 Server Component 트리를 가지며, Client Component state는 프레임 내에서 유지됩니다.

---

### @gaearon (React 팀) — 2021-05-10 — 순수성에 대해

우리의 의미에서 "순수"는 항상 같은 입력에 같은 출력을 반환해야 합니다 — **같은 데이터베이스 상태가 주어지면**. React의 순수성 개념은 학문적 순수성보다 실용적입니다.

---

### @gaearon (React 팀) — 2022-10-25 — 최종 머지

여러분의 피드백에 대응하여 여러 변경을 했습니다:
- `.server.js` / `.client.js` 파일명 규칙을 **`'use client'` 지시어**로 대체
- Server Components에 **네이티브 async/await 지원** 추가

이것을 첫 번째 반복으로 진행하겠습니다.

---

### @apiel — 2023-11-28 — 후기 피드백

RSC가 개발자 여정의 중요한 부분을 놓치고 있습니다. 클라이언트 사이드 컴포넌트에서 새로운 RSC를 로드하는 것이 "정말로 불가능"합니다. 추천 사항을 따르면 동적 데이터를 얻기 위해 여전히 API를 사용해야 합니다.
