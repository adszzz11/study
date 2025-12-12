"""
설정 관리

환경 변수 및 기본 설정값을 관리합니다.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()


class Config:
    """애플리케이션 설정"""

    # 프로젝트 루트
    PROJECT_ROOT = Path(__file__).parent.parent

    # 데이터 디렉터리
    DATA_DIR = PROJECT_ROOT / "data"
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    # 다운로드 디렉터리
    DOWNLOAD_DIR = DATA_DIR / "downloads"
    DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)

    # 데이터베이스
    DATABASE_PATH = DATA_DIR / "documents.db"

    # 로깅
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # Anthropic API (선택적)
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

    # HTTP 설정
    HTTP_TIMEOUT = 30.0  # seconds
    HTTP_RETRIES = 3

    # 스크래핑 설정
    DEFAULT_LIMIT = None  # None = 전체 수집
    SCRAPE_DELAY = 0.5  # seconds (서버 부하 방지)

    @classmethod
    def get_download_path(cls, jurisdiction: str, filename: str) -> Path:
        """
        다운로드 파일 경로 생성

        Args:
            jurisdiction: 지자체 코드
            filename: 파일명

        Returns:
            파일 경로
        """
        jurisdiction_dir = cls.DOWNLOAD_DIR / jurisdiction
        jurisdiction_dir.mkdir(parents=True, exist_ok=True)
        return jurisdiction_dir / filename


# 싱글톤 인스턴스
config = Config()
