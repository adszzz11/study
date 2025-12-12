"""
City of Marietta (CivicEngage) 스크래퍼

CivicEngage Agenda Center 플랫폼 기반의 Marietta 회의 문서를 수집합니다.
"""

import httpx
from bs4 import BeautifulSoup
from typing import Optional
import re
from datetime import datetime
from urllib.parse import urljoin

from .base import BaseScraper
from ..models import Document, DocumentList, DocumentType, Jurisdiction


class MariettaScraper(BaseScraper):
    """
    City of Marietta CivicEngage 플랫폼 스크래퍼

    특징:
    - 서버 렌더링 + jQuery (하이브리드)
    - 초기 HTML에 데이터 포함
    - BeautifulSoup 우선 사용
    """

    # CSS Selectors (Phase 0에서 확인됨)
    SELECTORS = {
        "agenda_center": "#agendaCenter",
        "meeting_rows": ".catAgendaRow",
        "meeting_date_strong": "strong",  # <strong>Dec 8, 2025</strong>
        "meeting_title_link": "a[href*='ViewFile/Agenda']",
        "minutes_link": "a[href*='ViewFile/Minutes']",
        "all_links": "a[href*='ViewFile']",
    }

    # 기본 URL
    BASE_URL = "https://www.mariettaga.gov"
    AGENDA_CENTER_URL = f"{BASE_URL}/AgendaCenter"

    # 날짜 패턴
    # 표시: "Dec 8, 2025" or "December 8, 2025"
    # URL: "_12082025" (MMDDYYYY)
    DATE_PATTERN_DISPLAY = r"(\w+)\s+(\d{1,2}),\s+(\d{4})"
    DATE_PATTERN_URL = r"_(\d{2})(\d{2})(\d{4})"

    def __init__(self):
        super().__init__(Jurisdiction.MARIETTA)
        self.client = httpx.Client(timeout=30.0, follow_redirects=True)

    def __del__(self):
        """리소스 정리"""
        if hasattr(self, 'client'):
            self.client.close()

    def get_base_url(self) -> str:
        """기본 URL 반환"""
        return self.BASE_URL

    def scrape(self, limit: Optional[int] = None) -> DocumentList:
        """
        Marietta 회의 문서 스크래핑

        Args:
            limit: 최대 수집 개수 (None이면 전체)

        Returns:
            Document 리스트
        """
        self._log_progress(f"Fetching page: {self.AGENDA_CENTER_URL}")

        try:
            # HTML 가져오기
            response = self.client.get(self.AGENDA_CENTER_URL)
            response.raise_for_status()

            self._log_progress(
                f"Received {len(response.text):,} bytes of HTML"
            )

            # BeautifulSoup으로 파싱
            soup = BeautifulSoup(response.text, "html.parser")

            # Agenda Center 컨테이너 찾기
            agenda_center = soup.select_one(self.SELECTORS["agenda_center"])
            if not agenda_center:
                raise ValueError("Agenda Center container not found")

            # 회의 행 찾기
            rows = agenda_center.select(self.SELECTORS["meeting_rows"])
            self._log_progress(f"Found {len(rows)} meeting rows")

            # 각 행에서 문서 추출
            documents = []
            meetings_processed = 0

            for i, row in enumerate(rows):
                try:
                    docs = self._parse_meeting_row(row)
                    if docs:
                        documents.extend(docs)
                        meetings_processed += 1

                        # limit은 "회의 수"가 아니라 "문서 수"로 적용
                        if limit and len(documents) >= limit:
                            break

                except Exception as e:
                    self.logger.warning(
                        f"Failed to parse row {i+1}: {e}",
                        exc_info=True
                    )
                    continue

            self._log_progress(
                f"Successfully parsed {len(documents)} documents "
                f"from {meetings_processed} meetings"
            )

            return documents[:limit] if limit else documents

        except httpx.HTTPError as e:
            raise RuntimeError(f"HTTP error: {e}")
        except Exception as e:
            raise RuntimeError(f"Scraping error: {e}")

    def _parse_meeting_row(self, row) -> DocumentList:
        """
        회의 행에서 Document 객체들 추출

        HTML 구조:
        <div class="catAgendaRow">
          <strong>Dec 8, 2025</strong> — Posted Dec 4, 2025 9:44 AM
          <a href="/AgendaCenter/ViewFile/Agenda/_12082025-2854?html=true">
            Board of Lights and Water Meeting
          </a>
          <a href="/AgendaCenter/ViewFile/Minutes/_12082025-2854">
            <img src=".../HomeIconMinutes.png" />
          </a>
          <div>
            <a href="...?html=true">HTML</a>
            <a href="...">PDF</a>
            <a href="...?packet=true">Packet</a>
          </div>
        </div>

        Args:
            row: BeautifulSoup 행 객체

        Returns:
            Document 리스트 (Agenda, Minutes, Packet)
        """
        documents = []

        # 날짜 추출
        date_elem = row.select_one(self.SELECTORS["meeting_date_strong"])
        if not date_elem:
            raise ValueError("Date element not found")

        date_text = date_elem.get_text(strip=True)

        # 회의 제목 추출 (Agenda 링크의 텍스트)
        title_link = row.select_one(self.SELECTORS["meeting_title_link"])
        if not title_link:
            raise ValueError("Meeting title link not found")

        meeting_title = title_link.get_text(strip=True)

        # 모든 링크 찾기
        all_links = row.select(self.SELECTORS["all_links"])

        for link in all_links:
            href = link.get("href")
            if not href:
                continue

            # 절대 URL로 변환
            full_url = urljoin(self.BASE_URL, href)

            # 링크 타입 판별
            doc_type = self._determine_doc_type(href, link)
            if not doc_type:
                continue

            # 날짜 파싱 (URL에서 추출 시도, 실패 시 텍스트에서)
            meeting_date = self._parse_date_from_url(href)
            if not meeting_date:
                meeting_date = self._parse_date_from_text(date_text)

            # Document 생성
            doc_title = f"{meeting_title} - {doc_type.value.capitalize()}"
            documents.append(Document(
                url=full_url,
                title=doc_title,
                doc_type=doc_type,
                meeting_date=meeting_date,
                jurisdiction=self.jurisdiction,
            ))

        return documents

    def _determine_doc_type(self, href: str, link_elem) -> Optional[DocumentType]:
        """
        링크 URL과 요소로부터 문서 타입 판별

        Args:
            href: 링크 URL
            link_elem: BeautifulSoup 링크 요소

        Returns:
            DocumentType 또는 None
        """
        # Minutes 링크
        if "ViewFile/Minutes" in href:
            return DocumentType.MINUTES

        # Agenda 링크
        if "ViewFile/Agenda" in href:
            # Packet 파라미터 확인
            if "packet=true" in href:
                return DocumentType.PACKET
            # HTML/PDF 구분은 하지 않고 모두 Agenda로 처리
            # (중복 방지를 위해 PDF만 수집)
            elif "html=true" in href:
                return None  # HTML 버전은 스킵
            else:
                return DocumentType.AGENDA

        return None

    def _parse_date_from_url(self, url: str) -> Optional[datetime.date]:
        """
        URL에서 날짜 추출

        Format: /AgendaCenter/ViewFile/Agenda/_12082025-2854
        Pattern: _MMDDYYYY

        Args:
            url: URL 문자열

        Returns:
            date 객체 또는 None
        """
        match = re.search(self.DATE_PATTERN_URL, url)
        if match:
            month, day, year = match.groups()
            try:
                dt = datetime(int(year), int(month), int(day))
                return dt.date()
            except ValueError:
                return None
        return None

    def _parse_date_from_text(self, date_text: str) -> datetime.date:
        """
        날짜 문자열을 date 객체로 변환

        Format: "Dec 8, 2025" or "December 8, 2025"
        Pattern: Month DD, YYYY

        Args:
            date_text: 날짜 문자열

        Returns:
            date 객체

        Raises:
            ValueError: 파싱 실패 시
        """
        match = re.match(self.DATE_PATTERN_DISPLAY, date_text.strip())
        if not match:
            raise ValueError(f"Date format not recognized: {date_text}")

        month_name, day, year = match.groups()

        # 월 이름을 숫자로 변환 (약어 + 전체)
        month_map = {
            # 전체 이름
            "January": 1, "February": 2, "March": 3, "April": 4,
            "May": 5, "June": 6, "July": 7, "August": 8,
            "September": 9, "October": 10, "November": 11, "December": 12,
            # 약어
            "Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4,
            "May": 5, "Jun": 6, "Jul": 7, "Aug": 8,
            "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12,
        }

        month = month_map.get(month_name)
        if not month:
            raise ValueError(f"Unknown month: {month_name}")

        # datetime 객체 생성 후 date만 반환
        dt = datetime(int(year), month, int(day))
        return dt.date()


# 편의 함수
def create_marietta_scraper() -> MariettaScraper:
    """Marietta 스크래퍼 인스턴스 생성"""
    return MariettaScraper()
