"""
BaseScraper 추상 클래스

모든 지자체 스크래퍼가 상속해야 하는 기본 클래스입니다.
"""

from abc import ABC, abstractmethod
from typing import Optional
import logging
from datetime import datetime

from ..models import Document, DocumentList, Jurisdiction, ScraperResult


class BaseScraper(ABC):
    """
    스크래퍼 추상 기본 클래스

    모든 지자체 스크래퍼는 이 클래스를 상속하고
    필수 메서드를 구현해야 합니다.
    """

    def __init__(self, jurisdiction: Jurisdiction):
        """
        Args:
            jurisdiction: 담당 지자체
        """
        self.jurisdiction = jurisdiction
        self.logger = logging.getLogger(f"scraper.{jurisdiction.value}")

    @abstractmethod
    def scrape(self, limit: Optional[int] = None) -> DocumentList:
        """
        회의 문서 스크래핑 (Backfill 모드)

        Args:
            limit: 최대 수집 개수 (None이면 전체)

        Returns:
            Document 리스트
        """
        pass

    @abstractmethod
    def get_base_url(self) -> str:
        """
        지자체 회의 포털 기본 URL

        Returns:
            기본 URL 문자열
        """
        pass

    def run(self, limit: Optional[int] = None) -> ScraperResult:
        """
        스크래퍼 실행 및 결과 요약

        Args:
            limit: 최대 수집 개수

        Returns:
            ScraperResult 객체
        """
        self.logger.info(
            f"Starting scraper for {self.jurisdiction.display_name}"
        )

        start_time = datetime.now()
        result = ScraperResult(jurisdiction=self.jurisdiction)

        try:
            # 스크래핑 실행
            documents = self.scrape(limit=limit)
            result.total_found = len(documents)

            self.logger.info(
                f"Found {len(documents)} documents for {self.jurisdiction.value}"
            )

            return documents, result

        except Exception as e:
            error_msg = f"Scraping failed: {str(e)}"
            self.logger.error(error_msg, exc_info=True)
            result.errors.append(error_msg)
            return [], result

        finally:
            # 실행 시간 기록
            end_time = datetime.now()
            result.duration_seconds = (end_time - start_time).total_seconds()

    def _log_progress(self, message: str, level: str = "info"):
        """
        진행 상황 로깅

        Args:
            message: 로그 메시지
            level: 로그 레벨 (info, warning, error)
        """
        log_method = getattr(self.logger, level, self.logger.info)
        log_method(message)
