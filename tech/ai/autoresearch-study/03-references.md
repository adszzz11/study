# Part 3: References

## 공식 소스

| 리소스 | 링크 |
|--------|------|
| GitHub 리포지토리 | [karpathy/autoresearch](https://github.com/karpathy/autoresearch) |
| 부모 프로젝트 (nanochat) | [karpathy/nanochat](https://github.com/karpathy/nanochat) |
| Karpathy 발표 트윗 | [X 포스트 (2026-03-07)](https://x.com/karpathy/status/2029701092347630069) |
| 후속 트윗 | [X 포스트 (후속)](https://x.com/karpathy/status/2031135152349524125) |
| 분석 노트북 | [analysis.ipynb](https://github.com/karpathy/autoresearch/blob/master/analysis.ipynb) |
| GitHub Discussions | [karpathy/autoresearch/discussions](https://github.com/karpathy/autoresearch/discussions) |
| 학습 데이터 | [climbmix-400b-shuffle (HuggingFace)](https://huggingface.co/datasets/karpathy/climbmix-400b-shuffle) |
| 소규모 실험용 데이터 | [tinystories-gpt4-clean (HuggingFace)](https://huggingface.co/datasets/karpathy/tinystories-gpt4-clean) |

## 추천 학습 자료

### 🟢 입문

| 자료 | 형태 | 설명 |
|------|------|------|
| [Dummy's Guide (X 스레드)](https://x.com/hooeem/status/2030720614752039185) | X 스레드 | 뉴럴넷 초보자를 위한 autoresearch 맥락 설명 |
| [DataCamp Guide to AutoResearch](https://www.datacamp.com/tutorial/guide-to-autoresearch) | 튜토리얼 | 단계별 가이드, 코드 설명 포함 |
| [Karpathy Autoresearch Explained (DataScienceDojo)](https://datasciencedojo.com/blog/karpathy-autoresearch-explained/) | 블로그 | 100 Experiments Overnight — 개요 설명 |
| [MarkTechPost 소개](https://www.marktechpost.com/2026/03/08/andrej-karpathy-open-sources-autoresearch-a-630-line-python-tool-letting-ai-agents-run-autonomous-ml-experiments-on-single-gpus/) | 기사 | 630줄 Python 도구 소개 |

### 🟡 중급

| 자료 | 형태 | 설명 |
|------|------|------|
| [Autoresearch Pattern (mager.co)](https://www.mager.co/blog/2026-03-14-autoresearch-pattern/) | 블로그 | 자기 개선 에이전트의 청사진 패턴 분석 |
| [Universal Skill 변환 (Medium)](https://medium.com/@k.balu124/i-turned-andrej-karpathys-autoresearch-into-a-universal-skill-1cb3d44fc669) | 블로그 | autoresearch를 범용 스킬로 변환한 경험기 |
| [PM을 위한 가이드](https://www.news.aakashg.com/p/autoresearch-guide-for-pms) | 뉴스레터 | 프로덕트 매니저 관점의 분석 |
| [Builder's Playbook (Substack)](https://sidsaladi.substack.com/p/autoresearch-101-builders-playbook) | 뉴스레터 | AI 스킬/프롬프트/에이전트 자기 개선 실전 가이드 |

### 🔴 고급

| 자료 | 형태 | 설명 |
|------|------|------|
| [SkyPilot 스케일링 블로그](https://blog.skypilot.co/scaling-autoresearch/) | 블로그 | GPU 클러스터로 autoresearch 확장 — 910건 실험 |
| [Latent Space: Sparks of Recursive Self Improvement](https://www.latent.space/p/ainews-autoresearch-sparks-of-recursive) | 팟캐스트/뉴스레터 | 재귀적 자기 개선의 함의 심층 분석 |
| [Fortune: Revolutionary Implications](https://fortune.com/2026/03/17/andrej-karpathy-loop-autonomous-ai-agents-future/) | 기사 | 자율 AI 연구 에이전트의 미래 분석 |
| [VentureBeat 심층 분석](https://venturebeat.com/technology/andrej-karpathys-new-open-source-autoresearch-lets-you-run-hundreds-of-ai) | 기사 | 혁명적 함의 — 업계 반응 |

## 커뮤니티

| 플랫폼 | 링크 | 특징 |
|--------|------|------|
| GitHub Discussions | [autoresearch/discussions](https://github.com/karpathy/autoresearch/discussions) | 공식 토론 |
| awesome-autoresearch | [GitHub](https://github.com/alvinunreal/awesome-autoresearch) | 큐레이션 리스트 |
| X/Twitter | `#autoresearch` | 실험 결과 공유 |
| Reddit r/MachineLearning | autoresearch 관련 스레드 | 커뮤니티 토론 |

## 오픈소스 / 관련 프로젝트

| 프로젝트 | 설명 | 링크 |
|---------|------|------|
| nanochat | autoresearch의 부모 프로젝트 (ChatGPT 학습) | [GitHub](https://github.com/karpathy/nanochat) |
| nanoGPT | Karpathy의 미니멀 GPT 학습 코드 | [GitHub](https://github.com/karpathy/nanoGPT) |
| Muon Optimizer | 행렬 파라미터 최적화 (Newton 기반) | autoresearch 내장 |
| Flash Attention 3 | 효율적 어텐션 커널 | `kernels` 패키지 |
| rustbpe | Rust 기반 BPE 토크나이저 | [PyPI](https://pypi.org/project/rustbpe/) |
