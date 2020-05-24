import requests

from PIL import Image
from io import BytesIO
from concurrent.futures import ThreadPoolExecutor

from telegram import Bot
from tqdm import tqdm


class StickersProcessor:
    base_url: str = "https://tlgrm.ru/stickers"
    max_workers: int = 20

    def __init__(self, bot_token: str):
        self.bot = Bot(token=bot_token)

    def load_sticker_pack(self, name_link: str):
        sticker_set = self.bot.get_sticker_set(name=name_link, timeout=3).to_dict().get("stickers")

        if sticker_set:
            for sticker in tqdm(sticker_set):
                sticker["file"] = self.bot.get_file(sticker["file_id"]).to_dict()

        return sticker_set

    @classmethod
    def fetch_stickers_page(cls, page_num: int):
        req_params = {
            "page": page_num,
            "ajax": True,
        }
        response_json = requests.get(
            url=cls.base_url,
            params=req_params,
            headers={"x-requested-with": "XMLHttpRequest"}
        ).json()
        return response_json["data"]

    @classmethod
    def fetch_image_from_url(cls, url: str):
        return Image.open(BytesIO(requests.get(url).content))
