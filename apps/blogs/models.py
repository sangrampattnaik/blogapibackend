import re

import tortoise
from passlib.hash import pbkdf2_sha256
from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator

from .utils import generate_random_string


class Blog(models.Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=200)
    body = fields.TextField()
    slug = fields.TextField()
    image_path = fields.CharField(max_length=100)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "blog"

    async def save(self, *args, **kwargs):
        self.slug = re.sub(" ", "-", self.title)
        while await Blog.filter(slug=self.slug).exists():
            self.slug += "-" + await generate_random_string()
        return await super(Blog, self).save(*args, **kwargs)


BlogInSchema = pydantic_model_creator(
    Blog, name="BlogIn", exclude_readonly=True, exclude=["slug"]
)
BlogOutSchema = pydantic_model_creator(Blog, name="BlogOut")
