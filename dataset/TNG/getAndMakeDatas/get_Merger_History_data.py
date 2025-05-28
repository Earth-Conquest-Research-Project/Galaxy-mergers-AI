import requests
import h5py
import os
import numpy as np
import os
from dotenv import load_dotenv

# .env 파일에서 환경 변수 불러오기
load_dotenv()

# 환경 변수 사용
api_key = os.getenv("TNG_API_KEY")

# 1. TNG50 merger history API endpoint
api_url = 'https://www.tng-project.org/api/TNG50-1/files/merger_history/'

# 2. headers 설정 (user-agent 필수)
headers = {
    "User-Agent": "python-requests/2.31.0",
    "API-Key": api_key
}

# 3. merger history 파일 리스트 가져오기
response = requests.get(api_url, headers=headers)
response.raise_for_status()
file_urls = response.json()['files']

# 4. 다운로드 경로 설정
save_dir = "./dataset/TNG/mergerHistoryData"
os.makedirs(save_dir, exist_ok=True)

# 5. 파일 하나씩 다운로드 & 확인
for file_url in file_urls:
    filename = file_url.split("/")[-1]
    save_path = os.path.join(save_dir, filename)

    # 이미 다운로드했다면 건너뜀
    if not os.path.exists(save_path):
        print(f"Downloading {filename}...")
        with requests.get(file_url, stream=True, headers=headers) as r:
            r.raise_for_status()
            with open(save_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
    else:
        print(f"{filename} already exists.")

    # 파일 열어서 데이터셋 구조 출력
    with h5py.File(save_path, 'r') as f:
        print(f"\n=== {filename} ===")
        def print_structure(name, obj):
            if isinstance(obj, h5py.Dataset):
                print(f"{name}: shape={obj.shape}, dtype={obj.dtype}")
        f.visititems(print_structure)

        # 예시: SnapNumLastMajorMerger 출력
        if 'SnapNumLastMajorMerger' in f:
            data = f['SnapNumLastMajorMerger'][:10]
            print("SnapNumLastMajorMerger (first 10):", data)