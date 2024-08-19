from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from .. import models, oauth2, schemas, utils
from ..database import get_db

router = APIRouter(
    tags=["Authentication"],
)


@router.post("/login", response_model=schemas.Token)
def login(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    stmt = select(models.User).filter_by(email=user_credentials.username)
    db_user = db.execute(stmt).scalar_one_or_none()

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid credentials"
        )

    if not utils.verify_password(user_credentials.password, db_user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid credentials"
        )

    # create a token
    access_token = oauth2.create_access_token(data={"user_id": db_user.id})

    # return token
    return {"access_token": access_token, "token_type": "bearer"}
