import requests
import base64

# 파일 읽기
with open('phase1_enhanced_signals.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Base64 인코딩
encoded_content = base64.b64encode(content.encode('utf-8')).decode('utf-8')

# GitHub API 요청
url = "https://api.github.com/repos/ddiddikeny/upload/contents/phase1_enhanced_signals.py"
headers = {
    "Accept": "application/vnd.github.v3+json",
    "User-Agent": "Python"
}

data = {
    "message": "Phase 1 향상된 신호 탐지 시스템 - 강력신호 대폭 개선",
    "content": encoded_content
}

response = requests.put(url, json=data, headers=headers)
print(f"상태 코드: {response.status_code}")

if response.status_code == 201:
    print("✅ 파일 업로드 성공!")
    print("📱 VM에서 다음 명령어로 다운로드하세요:")
    print("wget -O phase1_enhanced_signals.py https://raw.githubusercontent.com/ddiddikeny/upload/main/phase1_enhanced_signals.py")
else:
    print("❌ 업로드 실패")
