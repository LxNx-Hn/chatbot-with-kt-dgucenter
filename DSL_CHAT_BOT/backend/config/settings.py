import os
from dotenv import load_dotenv
from config.constants import DEFAULT_NIM_MODEL

# .env 파일 로드
load_dotenv()

# API 키 설정 (환경변수로부터 가져오기)
SERVICE_KEY = os.getenv('SERVICE_KEY')

# LLM provider 설정
MODEL_PROVIDER = os.getenv('MODEL_PROVIDER', 'local').strip().lower()
NVIDIA_API_KEY = os.getenv('NVIDIA_API_KEY') or os.getenv('NIM_API_KEY')
NIM_BASE_URL = os.getenv('NIM_BASE_URL', 'https://integrate.api.nvidia.com/v1').rstrip('/')
NIM_MODEL = os.getenv('NIM_MODEL', DEFAULT_NIM_MODEL)
NIM_TIMEOUT_SECONDS = float(os.getenv('NIM_TIMEOUT_SECONDS', '60'))

# API URL 설정
POLICY_API_URLS = {
    'url1': 'https://api.odcloud.kr/api/15132761/v1/uddi:181018f4-37d5-4500-b23f-9f9f2a840bc3',
    'url2': 'https://nidapi.k-startup.go.kr/api/kisedKstartupService/v1/getAnnouncementInformation/'
}

# 데이터 파일 경로
DATA_PATHS = {
    'startup_data': './data/master_summary_final.csv',
    'business_data': './data/final_data.csv'
}

# 데이터랩 API 설정 (환경변수로부터 가져오기)
NAVER_DATALAB_CONFIG = {
    'client_id': os.getenv('NAVER_CLIENT_ID'),
    'client_secret': os.getenv('NAVER_CLIENT_SECRET')
}
