---
date: 2026-10-15
tags: [tech]
type: tech-tool-study
status: draft
---

# REA — Projects

[[tech/devtools/rea/README|학습 진입점]]

모든 프로젝트는 승인받은 artifact와 분리된 환경을 전제로 한다. 산출물에는 artifact identity, 조사 명령·parameter, provider, evidence ID, limitation을 남긴다.

## 1. Legacy desktop app migration

설치 파일 또는 binary에서 data validation, file format, protocol, business rule을 evidence 기반으로 문서화한 뒤 신규 backend/client에 재구현한다.

- 시작: strings, config, resource, import와 file I/O 단서를 static inspection으로 수집
- 검증: sample input/output와 function·call reference를 매핑
- 산출물: behavior matrix, unknown 목록, compatibility test suite

## 2. Electron security / architecture audit

renderer → preload → main IPC 흐름, native addon, source map, network call을 추적해 feature 경계와 attack surface를 inventory화한다.

- 우선 조사: `contextIsolation`, IPC channel, permission request, external navigation
- 주의: 실제 runtime capture는 test profile·test endpoint에서만 수행
- 산출물: data-flow diagram, evidence-linked finding, remediation hypothesis

## 3. Authorized compatibility implementation

폐기 예정 SDK/client의 공개·허가된 동작을 조사하고 clean-room 원칙 아래 compatible adapter를 만든다.

- public documentation을 기준선으로 둔다.
- observed behavior는 adapter contract test로 바꾸고, inferred behavior는 별도 가설로 표시한다.
- 법적 범위와 license 조건은 기술적 evidence로 대체할 수 없다.

## 4. Android app maintenance

내부 enterprise APK의 Manifest, resource, class/method reference를 찾아 dependency, endpoint, feature 흐름을 inventory화한다.

- static APK inspection부터 시작해 권한·exported component·resource를 정리한다.
- device/adb는 승인된 test device에서만 사용한다.
- 결과는 upgrade·replacement 계획과 security review에 연결한다.

## 5. Web regression investigation

승인된 website의 structure, script, HAR를 버전·시점별로 비교해 UI 변화가 어느 request, resource, client-side branch와 관련되는지 좁힌다.

- static asset 비교로 가설을 만들고, 필요한 최소 범위에서 capture로 검증한다.
- HAR에는 cookie·authorization header·PII가 담길 수 있으므로 공유 전 redaction한다.

## Sources

- [REA README](https://github.com/morluto/rea)
- [REA Roadmap](https://github.com/morluto/rea/blob/main/docs/roadmap.md)
- [JADX](https://github.com/skylot/jadx)
