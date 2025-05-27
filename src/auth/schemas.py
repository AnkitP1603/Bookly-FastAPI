from pydantic import BaseModel, Field
from datetime import datetime
import uuid
from typing import List
from src.books.schemas import Book
from src.reviews.schemas import Review

class UserCreateModel(BaseModel):
    username : str = Field(max_length=10)
    email : str = Field(max_length=40)
    password : str = Field(min_length=6)
    first_name : str = Field(max_length=25) 
    last_name : str = Field(max_length=25)

class User(BaseModel):
    uid: uuid.UUID
    username : str
    email : str
    first_name : str
    last_name : str 
    password_hash : str = Field(exclude=True)
    is_verified : bool 
    created_at : datetime 
    updated_at : datetime

class UserBookModel(User):
    books : List[Book]
    reviews : List[Review]

class UserLoginModel(BaseModel):
    email : str = Field(max_length=40)
    password : str = Field(min_length=6)


class EmailModel(BaseModel):
    addresses : List[str]


class PasswordResetRequestModel(BaseModel):
    email: str


class PasswordResetConfirmModel(BaseModel):
    new_password: str
    confirm_new_password: str