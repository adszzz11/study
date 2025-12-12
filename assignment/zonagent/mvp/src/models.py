"""
데이터 모델 정의

Document, Jurisdiction 등의 핵심 데이터 구조를 정의합니다.
"""

from dataclasses import dataclass, field
from datetime import datetime, date
from enum import Enum
from typing import Optional
from pathlib import Path


class DocumentType(Enum):
    """문서 타입 열거형"""
    AGENDA = "agenda"
    MINUTES = "minutes"
    PACKET = "packet"
    VIDEO = "video"

    def __str__(self):
        return self.value


class Jurisdiction(Enum):
    """지자체 열거형"""
    CHEROKEE = "cherokee"
    ALPHARETTA = "alpharetta"
    HOLLY_SPRINGS = "holly_springs"
    MARIETTA = "marietta"

    def __str__(self):
        return self.value

    @property
    def display_name(self) -> str:
        """표시용 이름"""
        names = {
            Jurisdiction.CHEROKEE: "Cherokee County",
            Jurisdiction.ALPHARETTA: "City of Alpharetta",
            Jurisdiction.HOLLY_SPRINGS: "City of Holly Springs",
            Jurisdiction.MARIETTA: "City of Marietta",
        }
        return names[self]


@dataclass
class Document:
    """
    회의 문서 데이터 모델

    Attributes:
        url: 문서 원본 URL
        title: 회의 제목
        doc_type: 문서 타입 (agenda, minutes 등)
        meeting_date: 회의 날짜
        jurisdiction: 지자체
        file_path: 다운로드된 파일 경로 (선택)
        checksum: 파일 체크섬 (중복 방지용, 선택)
        scraped_at: 스크래핑 시간 (자동 생성)
        id: 데이터베이스 ID (자동 생성)
    """
    url: str
    title: str
    doc_type: DocumentType
    meeting_date: date
    jurisdiction: Jurisdiction
    file_path: Optional[Path] = None
    checksum: Optional[str] = None
    scraped_at: datetime = field(default_factory=datetime.now)
    id: Optional[int] = None

    def __post_init__(self):
        """타입 변환 처리"""
        # Enum 문자열을 Enum으로 변환
        if isinstance(self.doc_type, str):
            self.doc_type = DocumentType(self.doc_type)
        if isinstance(self.jurisdiction, str):
            self.jurisdiction = Jurisdiction(self.jurisdiction)

        # 날짜 문자열을 date로 변환
        if isinstance(self.meeting_date, str):
            self.meeting_date = datetime.fromisoformat(self.meeting_date).date()

        # Path 문자열을 Path로 변환
        if self.file_path and isinstance(self.file_path, str):
            self.file_path = Path(self.file_path)

    def to_dict(self) -> dict:
        """딕셔너리로 변환 (데이터베이스 저장용)"""
        return {
            "id": self.id,
            "url": self.url,
            "title": self.title,
            "doc_type": self.doc_type.value,
            "meeting_date": self.meeting_date.isoformat(),
            "jurisdiction": self.jurisdiction.value,
            "file_path": str(self.file_path) if self.file_path else None,
            "checksum": self.checksum,
            "scraped_at": self.scraped_at.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Document":
        """딕셔너리에서 생성 (데이터베이스 조회용)"""
        return cls(
            id=data.get("id"),
            url=data["url"],
            title=data["title"],
            doc_type=DocumentType(data["doc_type"]),
            meeting_date=datetime.fromisoformat(data["meeting_date"]).date(),
            jurisdiction=Jurisdiction(data["jurisdiction"]),
            file_path=Path(data["file_path"]) if data.get("file_path") else None,
            checksum=data.get("checksum"),
            scraped_at=datetime.fromisoformat(data["scraped_at"]),
        )

    def __repr__(self) -> str:
        """디버깅용 표현"""
        return (
            f"Document(id={self.id}, "
            f"jurisdiction={self.jurisdiction.value}, "
            f"type={self.doc_type.value}, "
            f"date={self.meeting_date}, "
            f"title='{self.title[:50]}...')"
        )


@dataclass
class ScraperResult:
    """
    스크래핑 결과 요약

    Attributes:
        jurisdiction: 지자체
        total_found: 발견한 총 문서 수
        total_new: 새로 추가된 문서 수
        total_skipped: 스킵된 문서 수 (중복 등)
        errors: 에러 목록
        duration_seconds: 실행 시간 (초)
    """
    jurisdiction: Jurisdiction
    total_found: int = 0
    total_new: int = 0
    total_skipped: int = 0
    errors: list[str] = field(default_factory=list)
    duration_seconds: float = 0.0

    def __repr__(self) -> str:
        """디버깅용 표현"""
        return (
            f"ScraperResult("
            f"{self.jurisdiction.value}: "
            f"found={self.total_found}, "
            f"new={self.total_new}, "
            f"skipped={self.total_skipped}, "
            f"errors={len(self.errors)}, "
            f"time={self.duration_seconds:.1f}s"
            f")"
        )

    def summary(self) -> str:
        """사람이 읽기 쉬운 요약"""
        lines = [
            f"📊 {self.jurisdiction.display_name} 스크래핑 결과",
            f"   발견: {self.total_found}개",
            f"   신규: {self.total_new}개",
            f"   스킵: {self.total_skipped}개",
            f"   에러: {len(self.errors)}개",
            f"   소요 시간: {self.duration_seconds:.1f}초",
        ]

        if self.errors:
            lines.append("\n⚠️  에러 목록:")
            for i, error in enumerate(self.errors[:5], 1):  # 처음 5개만
                lines.append(f"   {i}. {error}")
            if len(self.errors) > 5:
                lines.append(f"   ... 외 {len(self.errors) - 5}개")

        return "\n".join(lines)


# 타입 힌트 별칭
DocumentList = list[Document]
