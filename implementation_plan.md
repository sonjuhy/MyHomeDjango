# MyHomeDjango 리팩토링 구현 계획: TDD 및 타입 힌트 전면 적용

본 계획은 프로젝트 전체에 걸쳐 테스트 커버리지 100%를 달성하고, 모든 코드에 파이썬 타입 힌트를 적용하기 위한 상향식(Core-First) 점진적 접근 방식입니다.

## 1단계: 인프라 및 환경 구성 (Infrastructure Setup)
- **작업 내용:** 
  - `requirements-dev.txt` (또는 `requirements.txt`)에 개발 및 테스트 도구 추가: `pytest`, `pytest-django`, `pytest-cov`, `pytest-mock`, `mypy`, `django-stubs`.
  - `pytest.ini` 생성 및 Django 설정 연동.
  - `mypy.ini` (또는 `pyproject.toml`) 설정 파일 생성으로 엄격한 타입 검사(Strict Typing) 기준 마련.
- **목표:** TDD와 타입 검증을 수행할 수 있는 완벽한 환경 구축.

## 2단계: 핵심 도메인 및 유틸리티 모듈 (Core Foundations)
- **작업 내용:** 의존성이 적고 시스템의 기반이 되는 모듈에 우선적으로 타입 힌트와 테스트 코드를 적용합니다.
  - `MyHome/models.py`: 모델 필드, 메서드 리턴 타입 지정. 모델 생성/조회/수정/삭제 테스트 작성.
  - `MyHome/db/` (`database_enum.py`, `file_database_connection.py`, `iot_database_connection.py`, `light_database.py`): 타입 힌트 추가 및 데이터베이스 연결/쿼리 모킹(Mocking) 테스트.
  - `MyHome/file/` (`file_json.py`, `file_move.py`): 파일 시스템 입출력 및 JSON 파싱/저장 모듈 타이핑 및 분리된 테스트 진행.
- **TDD 사이클:** 테스트 실패(Red) -> 타입/코드 보강(Green) -> 코드 최적화(Refactor).

## 3단계: 외부 연동 및 서비스 모듈 (External Integrations)
- **작업 내용:** 핵심 모듈을 기반으로 동작하는 외부 서비스 연동 계층입니다. `pytest-mock`을 적극 활용하여 외부 시스템 의존성 없이 독립적인 테스트를 구성합니다.
  - `MyHome/MQTT/`: MQTT 클라이언트(Publish/Subscribe) 로직 타입 힌팅 및 모킹 테스트. (ex: `mqtt_json_parser.py`)
  - `MyHome/kafka/`: Kafka Producer/Consumer 메시지 송수신 로직 검증 및 타입 추가.
  - `MyHome/schedule/`: `APScheduler` 기반의 백그라운드 작업 및 스케줄러 등록/실행 검증.
- **목표:** 외부 서비스가 중단된 상태에서도 100% 커버리지를 유지할 수 있는 테스트 스위트 구성.

## 4단계: 애플리케이션 프레젠테이션 계층 (Web Layer)
- **작업 내용:** 사용자와 맞닿아 있는 뷰와 설정 코드를 다룹니다.
  - `MyHome/views.py`: Django `RequestFactory` 또는 `Client`를 사용하여 API 엔드포인트 응답, 상태 코드, 파라미터 타입 검증 및 100% 분기(Branch) 커버리지 달성.
  - `MyHome/admin.py`, `MyHome/apps.py`, `MyHomeDjango/urls.py` 등 프레임워크 설정 영역 테스트 보강.
- **목표:** 기능의 진입점부터 결과 반환까지의 전체 흐름 검증.

## 5단계: 최종 점검 및 커버리지 리뷰
- **작업 내용:**
  - `pytest --cov=MyHome --cov-report=term-missing` 명령어를 통해 전체 커버리지를 측정합니다.
  - 100%에 도달하지 못한 불가피한 예외(예: 스크립트 직접 실행 블록 `if __name__ == "__main__":` 등)를 확인하고 문서화 또는 `pragma: no cover` 처리.
  - `mypy`를 실행하여 타입 에러가 0건인지 최종 확인.

---

이 계획은 각 단계별로 작은 Pull Request 혹은 커밋 단위로 진행하여, 시스템의 안정성을 지속적으로 모니터링하며 진행됩니다.