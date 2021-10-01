from passlib.hash import pbkdf2_sha256
from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator


class User(models.Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=20, unique=True)
    full_name = fields.CharField(max_length=100)
    password = fields.CharField(max_length=100)
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "user"

    async def check_password(self, password: str) -> bool:
        return pbkdf2_sha256.verify(password, self.password)

    async def save(self, *args, **kwargs):
        if "$pbkdf2-sha256" not in self.password:
            self.password = pbkdf2_sha256.hash(self.password)
        return await super(User, self).save(*args, **kwargs)


UserInSchema = pydantic_model_creator(User, name="UserIn", exclude_readonly=True)
UserOutSchema = pydantic_model_creator(User, name="UserOut", exclude=["password"])
