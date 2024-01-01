

import os


class Uploader:

    @staticmethod
    def user_image(instance, filename):
        return f"User_Image/{instance.username}/{filename}"

    @staticmethod
    def question_image(instance, filename):
        return f"Question_Image/{instance.course_topic.course.title}/{instance.course_topic.topic_title}/{instance.pk}/{filename}"

