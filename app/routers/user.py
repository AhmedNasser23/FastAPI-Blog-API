from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import models, schemas, utils
from ..database import get_db

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

"""
# Create User
"""
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(
    user: schemas.UserCreate, 
    db: Session = Depends(get_db)
):
    # Hash the password - user.password
    
    user_mail = db.query(models.User).filter(models.User.email == user.email).first()
    if user_mail:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"Email {user.email} is already registered."
        )

    user.password = utils.hash(user.password)

    new_user = models.User(**user.model_dump())

    db.add(new_user) # Add new user to the session
    db.commit() # Commit the session to the database
    db.refresh(new_user) # Refresh the instance to get the new data from the database
    return new_user

"""
# Get User
"""
@router.get("/{id}", response_model=schemas.UserOut)
def get_user(
    id: int, 
    db: Session = Depends(get_db)
):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"user with id: {id} was not found."
        )
    return user