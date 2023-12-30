

import os


class Uploader:

    @staticmethod
    def user_image(instance, filename):
        return f"User_Image/{instance.username}/{filename}"

