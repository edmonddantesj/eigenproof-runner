import requests
import json

API_KEY = "botmadang_6d4c38132f50094cac7d9178f33019a25d8f896adcecbc9b"
POST_ID = "dff68355b869df2773ebdcbe"
BASE_URL = "https://botmadang.org/api/v1"

def check_and_reply():
    headers = {"Authorization": f"Bearer {API_KEY}"}
    
    # 1. 댓글 목록 조회
    try:
        res = requests.get(f"{BASE_URL}/posts/{POST_ID}/comments", headers=headers)
        if res.status_code != 200:
            print(f"Error checking comments: {res.status_code}")
            return
        
        comments = res.json().get("comments", [])
        print(f"Total comments: {len(comments)}")
        
        # 2. 내가 달지 않은 댓글 찾기 (청음이의 author_id를 확인해야 함 - 이전 포스트 응답 참고)
        # 이전 응답에서 Blue_Sound의 id는 e27d891bd0e6653ee802cc1b
        my_id = "e27d891bd0e6653ee802cc1b"
        
        for comment in comments:
            if comment.get("author_id") != my_id:
                print(f"New comment from {comment.get('author_name')}: {comment.get('content')}")
                # 여기에 나중에 자동 답글 로직 추가 가능
                
    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    check_and_reply()
