# GCP Workload Identity Federation 설정

서비스 계정 JSON 키 생성이 조직정책으로 막힌 경우, GitHub Actions는 Workload Identity Federation으로 GCP에 인증한다.

## 1. Cloud Shell 열기

GCP 콘솔에서 Cloud Shell을 연다.

https://console.cloud.google.com/

## 2. 변수 설정

아래 값 중 `PROJECT_ID`만 본인 프로젝트 ID로 바꾼다.

```bash
export PROJECT_ID="YOUR_GCP_PROJECT_ID"
export PROJECT_NUMBER="$(gcloud projects describe "${PROJECT_ID}" --format="value(projectNumber)")"
export REGION="asia-northeast3"
export POOL_ID="github-actions"
export PROVIDER_ID="github"
export SERVICE_ACCOUNT_ID="dgu-github-deployer"
export SERVICE_ACCOUNT_EMAIL="${SERVICE_ACCOUNT_ID}@${PROJECT_ID}.iam.gserviceaccount.com"
export REPO="LxNx-Hn/chatbot-with-kt-dgucenter"
```

## 3. 필요한 API 활성화

```bash
gcloud services enable \
  iam.googleapis.com \
  iamcredentials.googleapis.com \
  sts.googleapis.com \
  cloudresourcemanager.googleapis.com \
  serviceusage.googleapis.com \
  run.googleapis.com \
  artifactregistry.googleapis.com \
  secretmanager.googleapis.com \
  compute.googleapis.com \
  --project "${PROJECT_ID}"
```

## 4. 서비스 계정 생성

이미 있으면 이 명령은 실패할 수 있다. 그 경우 다음 단계로 넘어간다.

```bash
gcloud iam service-accounts create "${SERVICE_ACCOUNT_ID}" \
  --project "${PROJECT_ID}" \
  --display-name "DGU GitHub deployer"
```

## 5. 서비스 계정 권한 부여

```bash
for ROLE in \
  roles/run.admin \
  roles/artifactregistry.admin \
  roles/secretmanager.admin \
  roles/serviceusage.serviceUsageAdmin \
  roles/iam.serviceAccountUser \
  roles/resourcemanager.projectIamAdmin
do
  gcloud projects add-iam-policy-binding "${PROJECT_ID}" \
    --member "serviceAccount:${SERVICE_ACCOUNT_EMAIL}" \
    --role "${ROLE}" \
    --quiet
done
```

## 6. Workload Identity Pool 생성

이미 있으면 이 명령은 실패할 수 있다. 그 경우 다음 단계로 넘어간다.

```bash
gcloud iam workload-identity-pools create "${POOL_ID}" \
  --project "${PROJECT_ID}" \
  --location "global" \
  --display-name "GitHub Actions"
```

## 7. GitHub OIDC Provider 생성

```bash
gcloud iam workload-identity-pools providers create-oidc "${PROVIDER_ID}" \
  --project "${PROJECT_ID}" \
  --location "global" \
  --workload-identity-pool "${POOL_ID}" \
  --display-name "GitHub ${REPO}" \
  --issuer-uri "https://token.actions.githubusercontent.com" \
  --attribute-mapping "google.subject=assertion.sub,attribute.actor=assertion.actor,attribute.repository=assertion.repository,attribute.ref=assertion.ref" \
  --attribute-condition "assertion.repository == '${REPO}'"
```

## 8. GitHub Actions가 서비스 계정을 가장할 수 있게 허용

```bash
gcloud iam service-accounts add-iam-policy-binding "${SERVICE_ACCOUNT_EMAIL}" \
  --project "${PROJECT_ID}" \
  --role "roles/iam.workloadIdentityUser" \
  --member "principalSet://iam.googleapis.com/projects/${PROJECT_NUMBER}/locations/global/workloadIdentityPools/${POOL_ID}/attribute.repository/${REPO}"
```

## 9. GitHub Secrets에 넣을 값 출력

```bash
echo "GCP_PROJECT_ID=${PROJECT_ID}"
echo "GCP_SERVICE_ACCOUNT_EMAIL=${SERVICE_ACCOUNT_EMAIL}"
echo "GCP_WORKLOAD_IDENTITY_PROVIDER=projects/${PROJECT_NUMBER}/locations/global/workloadIdentityPools/${POOL_ID}/providers/${PROVIDER_ID}"
```

위 세 값을 GitHub Actions Secrets에 등록한다.

https://github.com/LxNx-Hn/chatbot-with-kt-dgucenter/settings/secrets/actions

## 공식 문서

- https://docs.cloud.google.com/iam/docs/workload-identity-federation-with-deployment-pipelines
- https://docs.github.com/actions/deployment/security-hardening-your-deployments/configuring-openid-connect-in-google-cloud-platform
- https://github.com/google-github-actions/auth
