from fastapi import APIRouter, status, Depends
from fastapi.exceptions import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession 
from typing import List
from src.books.book_data import books
from src.books.schemas import Book, BookCreateModel, BookUpdateModel, BookDetailModel
from src.db.main import get_session
from .service import BookService
from src.auth.dependencies import AccessTokenBearer, RoleChecker
from datetime import datetime
from src.errors import BookNotFound

book_router = APIRouter()
book_service = BookService()
access_token_bearer = AccessTokenBearer()
role_checker = Depends(RoleChecker(['admin','user']))

@book_router.get('/', response_model=List[Book], dependencies=[role_checker])
async def get_all_books(session:AsyncSession = Depends(get_session), token_details:dict=Depends(access_token_bearer)):
    # print(token_details)
    # print(f"Here: {datetime.fromtimestamp(token_details['exp'])}")
    books = await book_service.get_all_books(session)
    return books


@book_router.get('/user/{user_uid}', response_model=List[Book], dependencies=[role_checker])
async def get_user_book_submission(user_uid:str, session:AsyncSession = Depends(get_session), token_details:dict=Depends(access_token_bearer)):
    books = await book_service.get_user_books(user_uid,session)
    return books


@book_router.post('/',status_code=status.HTTP_201_CREATED, response_model=Book, dependencies=[role_checker])
async def create_book(book_data:BookCreateModel, session:AsyncSession = Depends(get_session), token_details:dict=Depends(access_token_bearer)) -> dict:
    user_id = token_details.get('user')['user_uid']
    new_book = await book_service.create_book(book_data,user_id,session)
    return new_book


@book_router.get('/{id}',response_model=BookDetailModel, dependencies=[role_checker])
async def get_book(id:str, session:AsyncSession = Depends(get_session), token_details:dict=Depends(access_token_bearer)) -> dict:
    book = await book_service.get_book(id,session)
    if book:
        return book
    else:
        raise BookNotFound()
    

@book_router.delete('/{id}', status_code=status.HTTP_202_ACCEPTED, dependencies=[role_checker])
async def delete_book(id:str, session:AsyncSession = Depends(get_session), token_details:dict=Depends(access_token_bearer)):
    book_to_delete = await book_service.delete_book(id,session)
    if book_to_delete:
        return {"message":f"Book with id {id} deleted successfully"}
    else:
        raise BookNotFound()

@book_router.patch('/{id}',response_model=Book, dependencies=[role_checker])
async def update_book(id:str, book_data:BookUpdateModel, session:AsyncSession = Depends(get_session), token_details:dict=Depends(access_token_bearer)) -> dict:
    updated_book = await book_service.update_book(id,book_data,session) 
    if updated_book:
        return updated_book
    else:
        raise BookNotFound()


