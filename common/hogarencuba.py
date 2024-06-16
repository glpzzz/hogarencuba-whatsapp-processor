import requests
import os

from dotenv import load_dotenv
from datetime import datetime


class HogarEnCubaClient:
    _instance = None
    _baseUrl = None
    _token = None

    def __new__(cls):
        if cls._instance is None:
            load_dotenv()
            cls._instance = super().__new__(cls)
            cls._baseUrl = os.getenv("BASEURL")

            response = requests.post(
                cls._baseUrl + "/login",
                {"username": os.getenv("USERNAME"), "password": os.getenv("PASSWORD")},
            )

            if response.status_code == 200:
                cls._token = response.json().get("access_token")
            else:
                raise ValueError("No authentication")

        return cls._instance

    @classmethod
    def get_first_unsent(cls):

        url = cls._baseUrl + "/whatsapp-messages/unsent?per-page=1"
        response = requests.get(
            url,
            headers={
                "Authorization": f"Bearer {cls._token}",
                "Content-Type": "application/json",
            },
        )

        if response.status_code != 200:
            raise ValueError(f"{response.status_code}: {response.reason}")

        data = response.json()

        if data["items"]:
            return data["items"][0]
        else:
            return None

    @classmethod
    def get_unsent_messages(cls):

        url = cls._baseUrl + "/whatsapp-messages/unsent"
        records = []

        while url:
            response = requests.get(
                url,
                headers={
                    "Authorization": f"Bearer {cls._token}",
                    "Content-Type": "application/json",
                },
            )

            if response.status_code != 200:
                raise ValueError(f"{response.status_code}: {response.reason}")

            data = response.json()
            records += data["items"]

            url = data["_links"].get("next", {}).get("href")

        return records

    @classmethod
    def mark_message_as_sent(cls, message_id):
        current_date = datetime.now()

        url = cls._baseUrl + f"/whatsapp-messages/{message_id}"

        response = requests.patch(
            url,
            headers={
                "Authorization": f"Bearer {cls._token}",
                "Content-Type": "application/json",
            },
            json={"sent_at": current_date.strftime("%Y-%m-%d %H:%M:%S")},
        )

        if response.status_code != 200:
            raise ValueError(f"{response.status_code}: {response.reason}")

        return response.status_code == 200

    @classmethod
    def mark_message_as_tried(cls, message_id):
        current_date = datetime.now()

        url = cls._baseUrl + f"/whatsapp-messages/{message_id}"

        response = requests.patch(
            url,
            headers={
                "Authorization": f"Bearer {cls._token}",
                "Content-Type": "application/json",
            },
            json={"tried_at": current_date.strftime("%Y-%m-%d %H:%M:%S")},
        )

        if response.status_code != 200:
            raise ValueError(f"{response.status_code}: {response.reason}")

        return response.status_code == 200

    @classmethod
    def set_message_output(cls, message_id, output):
        url = cls._baseUrl + f"/whatsapp-messages/{message_id}"

        response = requests.patch(
            url,
            headers={
                "Authorization": f"Bearer {cls._token}",
                "Content-Type": "application/json",
            },
            json={"output": output},
        )

        if response.status_code != 200:
            raise ValueError(f"{response.status_code}: {response.reason}")

        return response.status_code == 200
