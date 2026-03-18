import logging
import random
from variety.plugins.downloaders.DefaultDownloader import DefaultDownloader
from variety.Util import Util

logger = logging.getLogger("variety")


class KonachanDownloader(DefaultDownloader):
    def __init__(self, source, location):
        DefaultDownloader.__init__(self, source=source, config=location)

    def fill_queue(self):
        logger.info(lambda: "Konachan URL: " + self.config)

        queue = []
        url = self.config
        r = Util.fetch_json(url)
        try:
            for post in r:
                author = post["author"]
                origin_url = post["source"]
                image_url = post["file_url"]
                extra_metadata = {
                    "id": post["id"],
                    "author": author,
                    "tags": post["tags"],
                }
                queue.append((origin_url, image_url, extra_metadata))
        except Exception:
            logger.exception(lambda: "Could not process an item in the Konachan result")
        random.shuffle(queue)
        return queue
