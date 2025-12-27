# How do you approach system scalability?

## English

My approach to scalability is built on three principles:

**1. Design for horizontal scaling from day one.** At Danal, I containerized our services with Kubernetes so we could add capacity by spinning up more pods, not by upgrading hardware.

**2. Identify and eliminate bottlenecks proactively.** I use monitoring and observability tools to understand system behavior under load before it becomes a problem. My experience with the LGTM stack (Loki, Grafana, Tempo, Mimir) has been valuable here.

**3. Optimize where it matters.** Not everything needs to be infinitely scalable. I focus optimization efforts on the critical path—for payments, that was transaction processing; for Zonagent, it might be the AI inference pipeline or data aggregation layer.

I'd be curious to learn more about Zonagent's current architecture and where scalability challenges are emerging.

---

## 한글

확장성에 대한 제 접근 방식은 세 가지 원칙에 기반합니다:

**1. 처음부터 수평 확장을 고려하여 설계합니다.** 다날에서 Kubernetes로 서비스를 컨테이너화하여 하드웨어를 업그레이드하는 것이 아니라 더 많은 파드를 띄워서 용량을 늘릴 수 있게 했습니다.

**2. 병목 현상을 사전에 식별하고 제거합니다.** 모니터링과 관찰 가능성 도구를 사용하여 문제가 되기 전에 부하 상태에서의 시스템 동작을 이해합니다. LGTM 스택(Loki, Grafana, Tempo, Mimir) 경험이 여기서 가치 있었습니다.

**3. 중요한 곳에 최적화합니다.** 모든 것이 무한히 확장 가능할 필요는 없습니다. 최적화 노력을 크리티컬 패스에 집중합니다—결제에서는 트랜잭션 처리였고, Zonagent에서는 AI 추론 파이프라인이나 데이터 집계 레이어일 수 있습니다.

Zonagent의 현재 아키텍처와 어디서 확장성 도전이 나타나고 있는지 더 알고 싶습니다.
