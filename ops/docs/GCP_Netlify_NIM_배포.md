# GCP Cloud Run + Netlify + NVIDIA NIM 배포 가이드

이 문서는 공모전 데모 운영을 위한 권장 배포 구조를 설명한다.

- 프론트엔드: Netlify
- 백엔드: GCP Cloud Run의 FastAPI 게이트웨이
- LLM: NVIDIA NIM API
- 보조 미러: GitHub Pages

## 배포 의도

이 서비스는 완성형 독립 앱이 아니라 지자체 앱에 붙일 수 있는 AI 애드온 데모다. 따라서 GPU 서버를 직접 상시 운영하지 않고, Cloud Run에는 얇은 API 게이트웨이만 배포한다. LLM 추론은 NVIDIA NIM API로 위임한다.

## GitHub Actions 워크플로우

사용 워크플로우:

- `.github/workflows/deploy-gcp-netlify.yml`

워크플로우가 수행하는 일:

1. GCP 서비스 계정 JSON 키로 인증한다.
2. 필요한 GCP API를 활성화한다.
3. Artifact Registry 저장소를 생성하거나 재사용한다.
4. GitHub Secrets 값을 GCP Secret Manager에 생성/갱신한다.
5. NIM 배포용 경량 Docker 이미지를 빌드하고 푸시한다.
6. Cloud Run에 FastAPI 게이트웨이를 배포한다.
7. `/health` 엔드포인트를 호출해 배포 상태를 검증한다.
8. Cloud Run URL을 React 런타임 설정에 주입해 Netlify에 배포한다.

## 필요한 GitHub Secrets

아래 값만 채우면 창업/정책/트렌드 카테고리를 포함한 전체 데모 배포 워크플로우를 실행할 수 있다.

| 이름 | 용도 |
| --- | --- |
| `GCP_SERVICE_ACCOUNT_KEY` | GCP 서비스 계정 JSON 키 전체 |
| `NVIDIA_API_KEY` | NVIDIA NIM API 호출 키 |
| `SERVICE_KEY` | 공공데이터/정책 API 서비스 키 |
| `NAVER_CLIENT_ID` | 트렌드 분석용 네이버 데이터랩 Client ID |
| `NAVER_CLIENT_SECRET` | 트렌드 분석용 네이버 데이터랩 Client Secret |
| `NETLIFY_AUTH_TOKEN` | Netlify CLI 배포 토큰 |
| `NETLIFY_SITE_ID` | 기존 Netlify 사이트 ID |

## GCP 인증 설정

기본 배포 방식은 서비스 계정 JSON 키를 사용한다. 조직정책 때문에 JSON 키 생성이 막히는 경우에는 `ops/docs/GCP_Workload_Identity_Federation_설정.md`를 따라 키 없는 인증으로 전환할 수 있다.

처음 만든 프로젝트에서는 `Service Usage API`가 꺼져 있을 수 있다. 이 API가 꺼져 있으면 배포 워크플로우가 다른 API를 자동 활성화하지 못한다. 최초 1회 아래 링크에서 `Service Usage API`를 직접 사용 설정한다.

- https://console.developers.google.com/apis/api/serviceusage.googleapis.com/overview?project=distinguished-cinema-h3bf2

## GCP 서비스 계정 권한

`GCP_SERVICE_ACCOUNT_KEY`에 들어 있는 서비스 계정에는 다음 역할이 필요하다.

| 역할 | 필요한 이유 |
| --- | --- |
| `roles/run.admin` | Cloud Run 서비스 배포 |
| `roles/artifactregistry.admin` | Docker 저장소 생성 및 이미지 푸시 |
| `roles/secretmanager.admin` | Secret Manager 시크릿 생성/갱신 |
| `roles/serviceusage.serviceUsageAdmin` | Service Usage, Cloud Run, Artifact Registry, Secret Manager 등 필요한 GCP API 활성화 |
| `roles/iam.serviceAccountUser` | Cloud Run 런타임 서비스 계정 사용 |
| `roles/resourcemanager.projectIamAdmin` | 런타임 서비스 계정에 Secret Accessor 권한 부여 |

운영 보안을 더 엄격하게 가져갈 경우, 첫 배포 후에는 `roles/resourcemanager.projectIamAdmin`을 제거하고 Secret Accessor 권한을 수동 고정해도 된다.

## 기본 배포 입력값

워크플로우 수동 실행 시 기본값:

| 입력 | 기본값 |
| --- | --- |
| `region` | `asia-northeast3` |
| `service_name` | `dgu-nim-gateway` |
| `artifact_repo` | `dgu-chatbot` |
| `deploy_netlify` | `true` |

## 백엔드 런타임 설정

Cloud Run은 다음 값으로 배포된다.

| 환경변수 | 값 |
| --- | --- |
| `MODEL_PROVIDER` | `nim` |
| `RETRIEVAL_PROVIDER` | `keyword` |
| `NIM_BASE_URL` | `https://integrate.api.nvidia.com/v1` |
| `NIM_MODEL` | `meta/llama-3.1-8b-instruct` |
| `KEYWORD_EMBEDDING_DIMENSIONS` | `512` |
| `CORS_ALLOW_ORIGINS` | `https://dgu-chat-bot.netlify.app,https://lxnx-hn.github.io` |

`RETRIEVAL_PROVIDER=keyword`는 Cloud Run 이미지를 가볍게 유지하기 위한 명시적 운영 모드다. 기존 `sentence-transformers` 기반 검색은 `RETRIEVAL_PROVIDER=embedding`과 `requirements.txt` 기반 이미지 빌드로 보존된다.

## 배포 후 확인

워크플로우 성공 후 다음을 확인한다.

1. Cloud Run URL의 `/health` 응답이 `status: ok`인지 확인한다.
2. Netlify 사이트가 새 UI 제목과 런타임 `config.js`를 제공하는지 확인한다.
3. 프론트엔드에서 질문/카테고리를 넣어 `/api/chat` 호출이 성공하는지 확인한다.
4. NVIDIA NIM 호출 비용과 Cloud Run 요청량을 GCP/NVIDIA 콘솔에서 확인한다.

## 남은 주의점

- Cloud Run은 `min-instances=0`이라 첫 요청에서 콜드스타트가 생길 수 있다.
- `keyword` 검색은 가볍지만, 기존 `sentence-transformers` 검색보다 의미 유사도 품질은 낮을 수 있다.
- GitHub Secrets와 GCP Secret Manager에 같은 키가 저장되므로 키 교체 시 워크플로우를 다시 실행해야 한다.
- 네이버 데이터랩 키가 없으면 배포 워크플로우가 실패한다. 전체 데모에서는 트렌드 분석 카테고리를 포함하기 때문이다.
- Netlify 사이트가 기존 GitHub 자동 배포와 연결되어 있으면, Netlify UI의 자동 배포 설정과 GitHub Actions 배포가 충돌하지 않는지 확인해야 한다.
