"""
ZonAgent MVP - 메인 CLI 프로그램

Cherokee County 회의 문서 스크래퍼
"""

import argparse
import logging
import sys
from typing import Optional

from .config import config
from .database import Database
from .models import Jurisdiction
from .scrapers import get_scraper


def setup_logging(level: str = "INFO"):
    """로깅 설정"""
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format=config.LOG_FORMAT,
        handlers=[
            logging.StreamHandler(sys.stdout),
        ]
    )


def cmd_backfill(args):
    """Backfill 모드: 과거 데이터 수집"""
    logger = logging.getLogger(__name__)

    # 지자체 이름 매핑
    jurisdiction_names = {
        "cherokee": "Cherokee County",
        "marietta": "City of Marietta",
    }

    display_name = jurisdiction_names.get(args.jurisdiction, args.jurisdiction)

    logger.info("=" * 60)
    logger.info("ZonAgent - Backfill Mode")
    logger.info("=" * 60)
    logger.info(f"지자체: {display_name}")
    logger.info(f"최대 수집: {args.limit if args.limit else '전체'}")
    logger.info(f"데이터베이스: {config.DATABASE_PATH}")
    logger.info("=" * 60)

    # 데이터베이스 초기화
    db = Database(config.DATABASE_PATH)

    try:
        # 스크래퍼 생성 (팩토리 패턴)
        scraper = get_scraper(args.jurisdiction)

        # 스크래핑 실행
        logger.info("\n🚀 스크래핑 시작...\n")
        documents, result = scraper.run(limit=args.limit)

        # 데이터베이스에 저장
        logger.info("\n💾 데이터베이스 저장 중...\n")
        inserted, skipped = db.insert_many(documents)

        # 결과 업데이트
        result.total_new = inserted
        result.total_skipped = skipped

        # 결과 출력
        logger.info("\n" + "=" * 60)
        logger.info(result.summary())
        logger.info("=" * 60)

        # 성공
        sys.exit(0)

    except ValueError as e:
        # 지원하지 않는 지자체
        logger.error(f"\n❌ {e}")
        sys.exit(1)

    except Exception as e:
        logger.error(f"\n❌ 오류 발생: {e}", exc_info=args.verbose)
        sys.exit(1)


def cmd_stats(args):
    """통계 조회"""
    logger = logging.getLogger(__name__)

    logger.info("=" * 60)
    logger.info("ZonAgent MVP - Statistics")
    logger.info("=" * 60)

    # 데이터베이스 연결
    db = Database(config.DATABASE_PATH)

    # 통계 출력
    db.print_statistics()

    sys.exit(0)


def cmd_list(args):
    """문서 목록 조회"""
    logger = logging.getLogger(__name__)

    # 데이터베이스 연결
    db = Database(config.DATABASE_PATH)

    # 지자체 필터
    jurisdiction = None
    if args.jurisdiction:
        try:
            jurisdiction = Jurisdiction(args.jurisdiction)
        except ValueError:
            logger.error(f"Unknown jurisdiction: {args.jurisdiction}")
            sys.exit(1)

    # 문서 조회
    documents = db.get_documents(
        jurisdiction=jurisdiction,
        limit=args.limit
    )

    # 출력
    logger.info(f"\n📋 문서 목록 (최근 {len(documents)}개)\n")
    logger.info("=" * 80)

    for doc in documents:
        logger.info(
            f"{doc.meeting_date} | {doc.jurisdiction.value:15s} | "
            f"{doc.doc_type.value:10s} | {doc.title[:40]}"
        )

    logger.info("=" * 80)
    logger.info(f"총 {len(documents)}개\n")

    sys.exit(0)


def main():
    """메인 함수"""
    parser = argparse.ArgumentParser(
        description="ZonAgent - Georgia Municipal Meeting Document Scraper (Cherokee & Marietta)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Cherokee County 전체 문서 수집
  python -m src.main backfill --jurisdiction cherokee

  # Marietta 최근 10개만 수집
  python -m src.main backfill --jurisdiction marietta --limit 10

  # 통계 조회 (모든 지자체)
  python -m src.main stats

  # 특정 지자체 문서 목록 보기
  python -m src.main list --jurisdiction marietta --limit 20
        """
    )

    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="상세 로그 출력"
    )

    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        default="INFO",
        help="로그 레벨 (기본: INFO)"
    )

    subparsers = parser.add_subparsers(dest="command", help="명령어")

    # backfill 명령어
    parser_backfill = subparsers.add_parser(
        "backfill",
        help="과거 데이터 수집 (Backfill 모드)"
    )
    parser_backfill.add_argument(
        "--jurisdiction", "-j",
        required=True,
        choices=["cherokee", "marietta"],  # Phase 2: marietta 추가
        help="지자체 선택"
    )
    parser_backfill.add_argument(
        "--limit", "-l",
        type=int,
        default=None,
        help="최대 수집 개수 (기본: 전체)"
    )
    parser_backfill.set_defaults(func=cmd_backfill)

    # stats 명령어
    parser_stats = subparsers.add_parser(
        "stats",
        help="데이터베이스 통계 조회"
    )
    parser_stats.set_defaults(func=cmd_stats)

    # list 명령어
    parser_list = subparsers.add_parser(
        "list",
        help="수집된 문서 목록 조회"
    )
    parser_list.add_argument(
        "--jurisdiction", "-j",
        choices=["cherokee", "marietta"],  # Phase 2: marietta 추가
        help="지자체 필터"
    )
    parser_list.add_argument(
        "--limit", "-l",
        type=int,
        default=20,
        help="최대 조회 개수 (기본: 20)"
    )
    parser_list.set_defaults(func=cmd_list)

    # 인자 파싱
    args = parser.parse_args()

    # 로깅 설정
    log_level = "DEBUG" if args.verbose else args.log_level
    setup_logging(log_level)

    # 명령어 실행
    if args.command is None:
        parser.print_help()
        sys.exit(1)

    args.func(args)


if __name__ == "__main__":
    main()
