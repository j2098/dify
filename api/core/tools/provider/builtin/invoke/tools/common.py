import base64

from httpx import Timeout, post

from core.file.file_manager import download


def file_to_base64(file: str) -> str:
    data = download(file)
    return base64.b64encode(data).decode("utf-8")


def base64_to_binary(base64_str: str) -> bytes:
    return base64.b64decode(base64_str)


def run(base_url: str, api_key: str, payload: dict):
    resp = post(f"{base_url}/api/v1/run", 
                json=payload, 
                headers={
                    "Content-Type": "application/json", 
                    "Authorization": f"Bearer {api_key}"
                },
                timeout=Timeout(timeout=300))
    if resp.status_code != 200:
        raise Exception(f"Failed to run tool, status code: {resp.status_code}, response: {resp.text}")
    return resp.json()
