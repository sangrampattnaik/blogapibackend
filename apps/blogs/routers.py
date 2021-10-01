from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from tortoise.contrib.fastapi import HTTPNotFoundError

from apps.users.authentications import authetnicate

from . import models, utils
from .schemas import Status, BlogIn

router = APIRouter(prefix="/blog", tags=["blogs"])


@router.get("", response_model=List[models.BlogOutSchema])
async def get_blogs():
    return await models.BlogOutSchema.from_queryset(models.Blog.all())


@router.post(
    "", response_model=models.BlogOutSchema, status_code=status.HTTP_201_CREATED
)
async def create_blog(blog_data: BlogIn):
    data = blog_data.dict()
    data['image_path'] = await utils.convert_base64_toimage_and_save_file(data.pop('base64_image_encoded'))
    blog_obj = await models.Blog.create(**data)
    return await models.BlogOutSchema.from_tortoise_orm(blog_obj)


@router.get(
    "/{slug}",
    response_model=models.BlogOutSchema,
    responses={404: {"model": HTTPNotFoundError}},
)
async def get_detail_blog(slug: str):
    return await models.BlogOutSchema.from_queryset_single(models.Blog.get(slug=slug))


@router.delete(
    "/{slug}", response_model=Status, responses={404: {"model": HTTPNotFoundError}}
)
async def delete_specific_blog(slug: str, user = Depends(authetnicate)):
    breakpoint()
    deleted_count = await models.Blog.filter(slug=slug).delete()
    if not deleted_count:
        raise HTTPException(status_code=404, detail=f"Blog not found")
    return Status(message=f"Deleted blog {slug}")
