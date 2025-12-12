"""
SQLite 데이터베이스 레이어

Document 저장, 조회, 중복 체크 등의 데이터베이스 작업을 처리합니다.
"""

import sqlite3
from pathlib import Path
from typing import Optional
from datetime import date, datetime
from contextlib import contextmanager

from .models import Document, DocumentType, Jurisdiction, DocumentList


class Database:
    """SQLite 데이터베이스 관리 클래스"""

    def __init__(self, db_path: Path | str = "data/documents.db"):
        """
        Args:
            db_path: SQLite 데이터베이스 파일 경로
        """
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    @contextmanager
    def _get_connection(self):
        """데이터베이스 연결 컨텍스트 매니저"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # 딕셔너리 형태로 결과 반환
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def _init_db(self):
        """데이터베이스 스키마 초기화"""
        with self._get_connection() as conn:
            cursor = conn.cursor()

            # documents 테이블
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS documents (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    url TEXT NOT NULL UNIQUE,
                    title TEXT NOT NULL,
                    doc_type TEXT NOT NULL,
                    meeting_date TEXT NOT NULL,
                    jurisdiction TEXT NOT NULL,
                    file_path TEXT,
                    checksum TEXT,
                    scraped_at TEXT NOT NULL,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # 인덱스 생성 (검색 성능 향상)
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_jurisdiction_date
                ON documents(jurisdiction, meeting_date DESC)
            """)

            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_doc_type
                ON documents(doc_type)
            """)

            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_url
                ON documents(url)
            """)

    def insert_document(self, doc: Document) -> Optional[int]:
        """
        문서 삽입 (중복 시 무시)

        Args:
            doc: 삽입할 Document 객체

        Returns:
            삽입된 문서의 ID (중복 시 None)
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()

            try:
                cursor.execute("""
                    INSERT INTO documents (
                        url, title, doc_type, meeting_date,
                        jurisdiction, file_path, checksum, scraped_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    doc.url,
                    doc.title,
                    doc.doc_type.value,
                    doc.meeting_date.isoformat(),
                    doc.jurisdiction.value,
                    str(doc.file_path) if doc.file_path else None,
                    doc.checksum,
                    doc.scraped_at.isoformat(),
                ))

                return cursor.lastrowid

            except sqlite3.IntegrityError:
                # 중복 URL
                return None

    def insert_many(self, documents: DocumentList) -> tuple[int, int]:
        """
        여러 문서 일괄 삽입

        Args:
            documents: Document 리스트

        Returns:
            (삽입된 개수, 스킵된 개수)
        """
        inserted = 0
        skipped = 0

        for doc in documents:
            if self.insert_document(doc):
                inserted += 1
            else:
                skipped += 1

        return inserted, skipped

    def document_exists(self, url: str) -> bool:
        """
        URL로 문서 존재 여부 확인

        Args:
            url: 확인할 URL

        Returns:
            존재 여부
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT 1 FROM documents WHERE url = ?", (url,))
            return cursor.fetchone() is not None

    def get_last_scrape_date(
        self,
        jurisdiction: Jurisdiction,
        doc_type: Optional[DocumentType] = None
    ) -> Optional[date]:
        """
        특정 지자체의 마지막 스크래핑 날짜 조회

        Args:
            jurisdiction: 지자체
            doc_type: 문서 타입 (선택)

        Returns:
            마지막 회의 날짜 (없으면 None)
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()

            if doc_type:
                cursor.execute("""
                    SELECT MAX(meeting_date) as last_date
                    FROM documents
                    WHERE jurisdiction = ? AND doc_type = ?
                """, (jurisdiction.value, doc_type.value))
            else:
                cursor.execute("""
                    SELECT MAX(meeting_date) as last_date
                    FROM documents
                    WHERE jurisdiction = ?
                """, (jurisdiction.value,))

            row = cursor.fetchone()
            if row and row["last_date"]:
                return datetime.fromisoformat(row["last_date"]).date()
            return None

    def get_documents(
        self,
        jurisdiction: Optional[Jurisdiction] = None,
        doc_type: Optional[DocumentType] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        limit: int = 100
    ) -> DocumentList:
        """
        문서 조회 (필터링 가능)

        Args:
            jurisdiction: 지자체 필터 (선택)
            doc_type: 문서 타입 필터 (선택)
            start_date: 시작 날짜 (선택)
            end_date: 종료 날짜 (선택)
            limit: 최대 조회 개수

        Returns:
            Document 리스트
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()

            # 동적 쿼리 생성
            query = "SELECT * FROM documents WHERE 1=1"
            params = []

            if jurisdiction:
                query += " AND jurisdiction = ?"
                params.append(jurisdiction.value)

            if doc_type:
                query += " AND doc_type = ?"
                params.append(doc_type.value)

            if start_date:
                query += " AND meeting_date >= ?"
                params.append(start_date.isoformat())

            if end_date:
                query += " AND meeting_date <= ?"
                params.append(end_date.isoformat())

            query += " ORDER BY meeting_date DESC LIMIT ?"
            params.append(limit)

            cursor.execute(query, params)
            rows = cursor.fetchall()

            return [Document.from_dict(dict(row)) for row in rows]

    def get_statistics(self) -> dict:
        """
        전체 통계 조회

        Returns:
            통계 딕셔너리
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()

            # 전체 통계
            cursor.execute("""
                SELECT
                    COUNT(*) as total_documents,
                    COUNT(DISTINCT jurisdiction) as total_jurisdictions,
                    COUNT(DISTINCT meeting_date) as total_meetings,
                    MIN(meeting_date) as earliest_meeting,
                    MAX(meeting_date) as latest_meeting
                FROM documents
            """)
            overall = dict(cursor.fetchone())

            # 지자체별 통계
            cursor.execute("""
                SELECT
                    jurisdiction,
                    COUNT(*) as count,
                    MIN(meeting_date) as earliest,
                    MAX(meeting_date) as latest
                FROM documents
                GROUP BY jurisdiction
            """)
            by_jurisdiction = {
                row["jurisdiction"]: {
                    "count": row["count"],
                    "earliest": row["earliest"],
                    "latest": row["latest"],
                }
                for row in cursor.fetchall()
            }

            # 문서 타입별 통계
            cursor.execute("""
                SELECT doc_type, COUNT(*) as count
                FROM documents
                GROUP BY doc_type
            """)
            by_doc_type = {
                row["doc_type"]: row["count"]
                for row in cursor.fetchall()
            }

            return {
                "overall": overall,
                "by_jurisdiction": by_jurisdiction,
                "by_doc_type": by_doc_type,
            }

    def print_statistics(self):
        """통계를 사람이 읽기 쉽게 출력"""
        stats = self.get_statistics()

        print("📊 데이터베이스 통계")
        print("=" * 60)

        overall = stats["overall"]
        print(f"\n전체:")
        print(f"  총 문서: {overall['total_documents']:,}개")
        print(f"  지자체: {overall['total_jurisdictions']}개")
        print(f"  회의: {overall['total_meetings']:,}개")
        if overall['earliest_meeting']:
            print(f"  기간: {overall['earliest_meeting']} ~ {overall['latest_meeting']}")

        if stats["by_jurisdiction"]:
            print(f"\n지자체별:")
            for jurisdiction, data in stats["by_jurisdiction"].items():
                print(f"  {jurisdiction:20s}: {data['count']:4,}개  "
                      f"({data['earliest']} ~ {data['latest']})")

        if stats["by_doc_type"]:
            print(f"\n문서 타입별:")
            for doc_type, count in stats["by_doc_type"].items():
                print(f"  {doc_type:10s}: {count:4,}개")

        print("=" * 60)
