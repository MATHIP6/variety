import logging
import random

from requests import HTTPError

from variety import Util
from variety.plugins.builtin.downloaders.KonachanDownloader import KonachanDownloader
from variety.plugins.builtin.downloaders.UnsplashConfigurableSource import (
    UnsupportedConfig,
)
from variety.plugins.downloaders.ConfigurableImageSource import ConfigurableImageSource
from variety.Util import _


random.seed()


logger = logging.getLogger("variety")


class KonachanSource(ConfigurableImageSource):
    @classmethod
    def get_info(cls):
        return {
            "name": "Konachan",
            "description": _("Configurable source for fetching images from Konachan"),
            "author": "MATHIP6",
            "version": "0.1",
        }

    def get_source_type(self):
        return "konachan"

    def get_source_name(self):
        return "Konachan"

    def get_ui_instruction(self):
        return _("")

    def get_ui_short_instruction(self):
        return _("Tag name: ")

    def get_ui_short_description(self):
        return _("Fetch images from a given tag")

    def validate(self, query):
        try:
            tag_name = query
            query = f"https://konachan.net/post.json?tags={tag_name}"
            data = Util.fetch_json(query)
            valid = len(data) > 0
            return query, None if valid else _("No images found")
        except UnsupportedConfig:
            return query, _("Something's wrong with your search parameter")
        except Exception as e:
            if isinstance(e, HTTPError) and e.response.status_code == 404:
                return query, _("No images found")
            else:
                return query, _("Oops, this didn't work. Is the remote service up?")

    def create_downloader(self, config):
        return KonachanDownloader(self, config)
