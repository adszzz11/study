"""
Cherokee County (Granicus) 스크래퍼

Granicus 플랫폼 기반의 Cherokee County Planning Commission 회의 문서를 수집합니다.
"""

import httpx
from bs4 import BeautifulSoup
from typing import Optional
import re
from datetime import datetime
from urllib.parse import urljoin

from .base import BaseScraper
from ..models import Document, DocumentList, DocumentType, Jurisdiction


class CherokeeScraper(BaseScraper):
    """
    Cherokee County Granicus 플랫폼 스크래퍼

    특징:
    - 서버 렌더링 HTML (Playwright 불필요)
    - 테이블 구조로 명확한 데이터
    - CSS Selector 기반 파싱
    """

    # CSS Selectors (Phase 0에서 확인됨)
    SELECTORS = {
        "meeting_table": "table.listingTable",
        "meeting_rows": "tr.listingRow",
        "cells": "td.listItem",
    }

    # 날짜 정규식: "December 12, 2025 - 3:00 PM"
    DATE_PATTERN = r"(\w+)\s+(\d{1,2}),\s+(\d{4})\s+-\s+(\d{1,2}):(\d{2})\s+(AM|PM)"

    # 기본 URL
    BASE_URL = "https://cherokeega.granicus.com"
    MEETING_LIST_URL = f"{BASE_URL}/ViewPublisher.php?view_id=1"

    def __init__(self):
        super().__init__(Jurisdiction.CHEROKEE)
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
        Cherokee County 회의 문서 스크래핑

        Args:
            limit: 최대 수집 개수 (None이면 전체)

        Returns:
            Document 리스트
        """
        self._log_progress(f"Fetching page: {self.MEETING_LIST_URL}")

        try:
            # HTML 가져오기
            response = self.client.get(self.MEETING_LIST_URL)
            response.raise_for_status()

            self._log_progress(
                f"Received {len(response.text):,} bytes of HTML"
            )

            # BeautifulSoup으로 파싱
            soup = BeautifulSoup(response.text, "html.parser")

            # 회의 테이블 찾기
            table = soup.select_one(self.SELECTORS["meeting_table"])
            if not table:
                raise ValueError("Meeting table not found")

            # 회의 행 찾기
            rows = table.select(self.SELECTORS["meeting_rows"])
            self._log_progress(f"Found {len(rows)} meeting rows")

            # 각 행에서 문서 추출
            documents = []
            for i, row in enumerate(rows):
                if limit and i >= limit:
                    break

                try:
                    docs = self._parse_meeting_row(row)
                    documents.extend(docs)
                except Exception as e:
                    self.logger.warning(
                        f"Failed to parse row {i+1}: {e}",
                        exc_info=True
                    )
                    continue

            self._log_progress(
                f"Successfully parsed {len(documents)} documents"
            )

            return documents

        except httpx.HTTPError as e:
            raise RuntimeError(f"HTTP error: {e}")
        except Exception as e:
            raise RuntimeError(f"Scraping error: {e}")

    def _parse_meeting_row(self, row) -> DocumentList:
        """
        회의 행에서 Document 객체들 추출

        HTML 구조:
        <tr class="listingRow">
          <td class="listItem">Meeting Name</td>
          <td class="listItem">December 12, 2025 - 3:00 PM</td>
          <td class="listItem"><a href="...">Agenda</a></td>
          <td class="listItem"><a href="...">Minutes</a></td>
          <td class="listItem"><a href="...">Video</a></td>
        </tr>

        Args:
            row: BeautifulSoup 행 객체

        Returns:
            Document 리스트 (Agenda, Minutes, Video)
        """
        cells = row.select(self.SELECTORS["cells"])

        if len(cells) < 5:
            raise ValueError(f"Expected 5 cells, got {len(cells)}")

        # 회의 정보 추출
        meeting_name = cells[0].get_text(strip=True)
        date_text = cells[1].get_text(strip=True)
        meeting_date = self._parse_date(date_text)

        documents = []

        # Agenda
        agenda_link = cells[2].find("a")
        if agenda_link and agenda_link.get("href"):
            documents.append(Document(
                url=urljoin(self.BASE_URL, agenda_link["href"]),
                title=f"{meeting_name} - Agenda",
                doc_type=DocumentType.AGENDA,
                meeting_date=meeting_date,
                jurisdiction=self.jurisdiction,
            ))

        # Minutes
        minutes_link = cells[3].find("a")
        if minutes_link and minutes_link.get("href"):
            # javascript:void(0) 같은 더미 링크 제외
            href = minutes_link["href"]
            if not href.startswith("javascript"):
                documents.append(Document(
                    url=urljoin(self.BASE_URL, href),
                    title=f"{meeting_name} - Minutes",
                    doc_type=DocumentType.MINUTES,
                    meeting_date=meeting_date,
                    jurisdiction=self.jurisdiction,
                ))

        # Video (Phase 1에서는 제외 - javascript:void(0) 처리 필요)
        # video_link = cells[4].find("a")
        # if video_link and video_link.get("href"):
        #     ... (Phase 2에서 구현)

        return documents

    def _parse_date(self, date_text: str) -> datetime.date:
        """
        날짜 문자열을 date 객체로 변환

        Format: "December 12, 2025 - 3:00 PM"
        Pattern: Month DD, YYYY - H:MM AM/PM

        Args:
            date_text: 날짜 문자열

        Returns:
            date 객체

        Raises:
            ValueError: 파싱 실패 시
        """
        match = re.match(self.DATE_PATTERN, date_text.strip())
        if not match:
            raise ValueError(f"Date format not recognized: {date_text}")

        month_name, day, year, hour, minute, ampm = match.groups()

        # 월 이름을 숫자로 변환
        month_map = {
            "January": 1, "February": 2, "March": 3, "April": 4,
            "May": 5, "June": 6, "July": 7, "August": 8,
            "September": 9, "October": 10, "November": 11, "December": 12,
        }

        month = month_map.get(month_name)
        if not month:
            raise ValueError(f"Unknown month: {month_name}")

        # 12시간 형식을 24시간으로 변환 (시간은 사용 안 하지만 검증용)
        hour = int(hour)
        if ampm == "PM" and hour != 12:
            hour += 12
        elif ampm == "AM" and hour == 12:
            hour = 0

        # datetime 객체 생성 후 date만 반환
        dt = datetime(int(year), month, int(day), hour, int(minute))
        return dt.date()


# 편의 함수
def create_cherokee_scraper() -> CherokeeScraper:
    """Cherokee 스크래퍼 인스턴스 생성"""
    return CherokeeScraper()
