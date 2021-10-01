import tortoise
from fastapi import APIRouter, Depends, HTTPException, status

from . import authentications, models, schemas

router = APIRouter(prefix="/user", tags=["user"])


@router.post(
    "", status_code=status.HTTP_201_CREATED, response_model=models.UserOutSchema
)
async def create_user(user_data: models.UserInSchema):
    try:
        user_obj = await models.User.create(**user_data.dict(exclude_unset=True))
        return await models.UserOutSchema.from_tortoise_orm(user_obj)
    except tortoise.exceptions.IntegrityError:
        raise HTTPException(status_code=400, detail="username aleary taken")


@router.post(
    "/login",
    responses={
        "200": {
            "model": schemas.UserLoginOutSchema,
            "description": "succesfull response",
        }
    },
)
async def login(user_credential: schemas.LoginSchema):
    try:
        user_data = user_credential.dict()
        user = await models.User.get(username=user_data["username"])
        if not await user.check_password(user_data["password"]):
            raise HTTPException(
                detail="authetnication failed due incorrect password", status_code=401
            )
        token = await authentications.create_jwt_token(user)
        return {"status": "success", "message": "login successfull", "token": token}
    except tortoise.exceptions.DoesNotExist:
        raise HTTPException(
            detail="unauthorized access due to incorrect username", status_code=401
        )


@router.get("", response_model=models.UserOutSchema)
async def get_user_details(user: models.User = Depends(authentications.authetnicate)):
    return await models.UserOutSchema.from_tortoise_orm(user)
