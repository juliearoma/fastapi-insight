import base64
import os
import etcd3
import json
import requests

from fastapi.logger import logger

class EtcdService:
    def __init__(self, host="192.168.7.105", prefix="/app/python/api/config"):
        """
        EtcdService 클래스 초기화.
        기본적으로 환경 변수에서 값을 읽거나, 없으면 기본값을 사용.
        """
        self.host = host
        self.prefix = prefix
        self.port = None
        self.items:dict = {}
        self._initialize_client()
        self.get_config()

    def _initialize_client(self):
        """
        환경 변수 및 기본값을 기반으로 Etcd 클라이언트를 초기화.
        """
        environment = os.getenv("PYTHON_ENV", "development")  # 기본값을 'development'로 설정
        if environment == "development":
            self.port = 13379 
        elif environment == "production":
            self.port = 12379 
        else:
            self.port = 13379 

        self.base_url = f"http://{self.host}:{self.port}/v3"

    def get_config(self):
        """
        Etcd에서 설정 데이터를 가져와 JSON으로 반환.
        """
        try:
            url = f"{self.base_url}/kv/range"
            
            # 키를 Base64로 인코딩
            prefix_encoded = base64.b64encode(self.prefix.encode("utf-8")).decode("utf-8")

            payload = {
                "key": prefix_encoded
            }

            response = requests.post(url, json=payload)
            response.raise_for_status()  # 요청 오류 확인

            response_data = response.json()

            # 키 값이 존재하는지 확인
            if "kvs" not in response_data or not response_data["kvs"]:
                raise ValueError("No data found in etcd for the given prefix")

            # etcd에서 가져온 데이터 디코딩
            config_data = base64.b64decode(response_data["kvs"][0]["value"]).decode("utf-8")

            dict_item = self.flatten_json(json.loads(config_data))
            
            for key, value in dict_item.items():
                self.items[key] = value
        except Exception as e:
            logger.error(f"Error fetching config: {e}")
            raise

    def flatten_json(self, json_object, parent_key='', sep=':'):
        """
        Flatten a nested JSON object for easier access.
        Converts {'a': {'b': {'c': 1}}} to {'a:b:c': 1}.
        """
        items = []
        for key, value in json_object.items():
            new_key = f"{parent_key}{sep}{key}" if parent_key else key
            if isinstance(value, dict):
                items.extend(self.flatten_json(value, new_key, sep=sep).items())
            else:
                items.append((new_key, value))
        return dict(items)

    def get(self, key, default=None):
        """
        환경 변수 또는 Etcd에서 값을 가져옵니다.
        환경 변수에서 우선적으로 검색하며, 없으면 Etcd에서 가져옵니다.
        """
        # 환경 변수에서 가져오기
        if key in self.items:
            return self.items[key]
        # 기본값 반환
        return default
