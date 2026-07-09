/*
 * [Netlify Functions 전용] - Netlify 배포 시에만 사용됨
 * 도커 배포 시에는 이 파일 사용 안함
 */

exports.handler = async (event) => {
  const headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Allow-Methods': 'OPTIONS,POST'
  };

  if (event.httpMethod === 'OPTIONS') {
    return {
      statusCode: 204,
      headers
    };
  }

  try {
    // 클라이언트에서 전달된 데이터 파싱
    const { message, category } = JSON.parse(event.body);
    
    // 환경 변수에서 실제 API URL 가져오기
    const API_URL = (process.env.REACT_APP_API_URL || process.env.API_URL || '').replace(/\/+$/, '');
    if (!API_URL) {
      return {
        statusCode: 503,
        body: JSON.stringify({ error: 'REACT_APP_API_URL 또는 API_URL 환경변수가 설정되어 있지 않습니다.' }),
        headers
      };
    }
    
    // 실제 백엔드 API 호출
    const response = await fetch(`${API_URL}/api/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message, category })
    });

    const data = await response.json();
    
    return {
      statusCode: 200,
      body: JSON.stringify(data),
      headers
    };
  } catch (error) {
    return {
      statusCode: 500,
      body: JSON.stringify({ error: error.message }),
      headers
    };
  }
};
