---
date: 2026-09-09
tags: [tech]
type: tech-tool-study
status: draft
---

# Muse 시작하기: 초기 WHAM 로컬 재현

[[tech/ai/muse/README|학습 진입점]] → [[tech/ai/muse/04-learning/02-deep-dive|Deep dive]]

## 목표와 준비

목표는 공개 **200M WHAM + tiny-sample**에서 생성 결과를 관찰하는 것이다. 아래는 공식 Model Card를 바탕으로 정리한 절차이며, 이 노트 작성 과정에서 모델 추론을 실행한 것은 아니다. WHAM-RT 설치 절차로 사용하지 않는다.

- 공식 검증 환경은 Ubuntu 또는 Windows WSL2이며 CUDA GPU를 전제로 한다. macOS 지원을 가정하지 않는다.
- Python 3.9, Git·Git LFS와 충분한 저장 공간을 준비한다. checkpoint 크기와 GPU 메모리는 서로 다르다.
- License를 읽고 목적에 맞는 사용인지 확인한다.
- 실행 저장소·weights·dataset·생성물은 공개 study vault 밖의 별도 실험 디렉터리에 둔다.

## 1. 코드와 환경 준비

아래 명령은 별도 실험 디렉터리에서 실행한다. HTTPS clone은 공식 안내의 SSH 주소를 바꾼 형태다. 설치 스크립트를 먼저 읽고 필요한 시스템 의존성을 확인한다.

```bash
GIT_LFS_SKIP_SMUDGE=1 git clone https://huggingface.co/microsoft/wham WHAM
cd WHAM
less setup_local.sh
./setup_local.sh
source venv/bin/activate
```

## 2. 필요한 파일만 받기

1. 모델 저장소의 **Files and versions → models**에서 `WHAM_200M.ckpt`를 받아 `models/`에 둔다.
2. 공식 sample dataset에서 `tiny-sample`을 받아 저장소 루트에 둔다.
3. LFS pointer 텍스트만 받은 상태가 아닌지 실제 파일 크기를 확인한다.

```text
WHAM/
├── models/WHAM_200M.ckpt
├── tiny-sample/
├── run_dreaming.py
└── run_server.py
```

## 3. 첫 rollout 생성

```bash
python run_dreaming.py --help
python run_dreaming.py --model_path models/WHAM_200M.ckpt --data_path tiny-sample
```

`dreaming_output/`의 `.mp4`로 prompt 뒤의 전개를 보고, `.npz`로 생성 배열을 확인한다. 최초 출력까지 시간이 걸릴 수 있으므로 바로 실패로 판단하지 않는다.

## 4. 선택: Demonstrator

```bash
python run_server.py --model models/WHAM_200M.ckpt
```

공식 Demonstrator는 Windows 앱이다. 저장소의 `wham_demonstrator` 안내에 따라 실행하고 로컬 모델 서버에 연결한다. 서버 실행만으로 Quake II 실시간 데모가 되는 것은 아니다.

## 완료 기준

- [ ] 사용한 repository revision, checkpoint, sample 이름을 기록했다.
- [ ] 출력 영상과 원래 prompt를 구분했다.
- [ ] 정상적으로 이어지는 장면과 이상한 전개를 각각 한 사례 이상 기록했다.
- [ ] 추론 소요 시간·GPU·batch size를 함께 기록했다.
- [ ] 공개 노트에는 원본 코드·모델·dataset을 재배포하지 않았다.

## 문제 해결

| 증상 | 먼저 확인할 것 |
|---|---|
| checkpoint를 읽지 못함 | 경로, 다운로드 완료 여부, LFS pointer 여부 |
| CUDA 오류 | GPU 지원 여부와 설치 스크립트·드라이버 환경 |
| 메모리 부족 | 작은 모델과 batch size 사용 여부 |
| 첫 출력이 늦음 | 프로세스 상태·GPU 사용량·첫 sequence 완료 여부 |
| 타 게임 prompt에서 붕괴 | Bleeding Edge 밖 입력이라는 학습 범위 제한 |

공유 전 생성물의 watermark와 provenance metadata를 유지하고 배포 조건을 확인한다. 이 실습의 기본 공개 산출물은 직접 작성한 관찰 기록이다.

## Sources

- [공식 Model Card·실행 코드·weights](https://huggingface.co/microsoft/wham)
- [Bleeding Edge sample dataset](https://huggingface.co/datasets/microsoft/bleeding-edge-gameplay-sample)
- [Microsoft Research License](https://huggingface.co/microsoft/wham/blob/main/LICENSE.md)

## 추가 조사: Meta Muse 첫 학습 절차

> 확인일: 2026-09-09. 위 WHAM 설치 명령은 Meta Muse 실행법이 아니다. 아래는 **제안된 실습**이며 실행 기록이 아니다.

1. [공식 Muse 발표](https://about.fb.com/news/2026/09/introducing-muse-personal-ai-agent/)에서 연결한 제품 경로를 이용하고, 계정·지역에서 제공되는지 확인한다. 접근 불가하면 공식 사례를 읽은 기록으로 남긴다.
2. 공개 자료로 끝나는 작은 목표를 입력한다. 예: 아래 학습 계획 요청.
3. 결과물(Artifact)과 활동 기록(activity log)을 대조해 출처가 실제 결론을 뒷받침하는지 확인한다.
4. Goals에서 계획과 진행 상태를, Memory에서 기억한 정보를 확인한다. 공식 설계 글은 Memory 파일을 직접 읽고 편집할 수 있다고 설명한다.

```text
Meta Muse 공식 발표와 Muse Spark 1.3 발표를 읽고
모델과 제품의 차이를 배우는 3일 학습 계획을 만들어 줘.
각 항목에 원문 링크와 완료 조건을 넣어 줘.
확인한 사실과 네 제안을 구분해 줘.
```

완료 기준: 출처 검증 1건, 사실/제안 구분, 계획 대비 결과 차이 기록. 실제 사용하지 않았다면 성공 여부를 채우지 않는다.

출처: [How We Designed Muse — Goals, Memory, Artifacts](https://introducing.muse.ai/).
