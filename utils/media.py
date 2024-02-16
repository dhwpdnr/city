import os.path
from uuid import uuid4


def save_media(media, dir_name):
    if media != "undefined":
        media_name = media.name
        extention = os.path.splitext(media_name)[1]
        uuid_name = uuid4().hex + extention
        file_path = os.path.join(dir_name, uuid_name)
        media_path = os.path.join("media", file_path)

        if not os.path.exists(os.path.dirname(media_path)):
            os.makedirs(os.path.dirname(media_path))

        with open(media_path, "wb+") as destination:
            destination.write(media.read())

        return file_path, media_name
    return "", ""
