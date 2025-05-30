from models import Book, Review ,ApiResponse
from data import book_db , review_db
from fastapi import FastAPI, status , Path, Query
from typing import Literal , List

app = FastAPI()

@app.get("/books")
def get_books(genre:Literal["fiction","astronomy","horror","adventure"]=None,author:str=None, year:int=None): 
 if(not genre and not author and not year):
   return book_db

 filtered_books = [book for book in book_db if book.author == author or book.genre == genre or book.year == year]

 if(len(filtered_books) > 0):
    return ApiResponse(status_code=status.HTTP_200_OK, data=filtered_books)
 else:
  return ApiResponse(status_code=status.HTTP_404_NOT_FOUND,data=None)         
      

@app.get("/books/{bookid}")
def single_book(bookid:int):
   for book in book_db:
     if book.book_id == bookid:
       return ApiResponse(status_code=status.HTTP_200_OK,data=book)
   else:
     return ApiResponse(status_code=status.HTTP_404_NOT_FOUND,data=None)


@app.post("/book")
def add_book(book:Book):
    if(book):
     book_db.append(book)
     return ApiResponse(status_code=status.HTTP_201_CREATED,data=book)
    else:
      return ApiResponse(status_code=status.HTTP_204_NO_CONTENT, data=None)
    


@app.post("/books/{book_id}/review")
def add_review(book_id:int,review:Review):
   for book in book_db:
     if book.book_id == book_id:
         review_db.append(review)
         return ApiResponse(status_code=status.HTTP_201_CREATED,data=review)
   else:
     return ApiResponse(status_code=status.HTTP_404_NOT_FOUND, data=None)


@app.post("/reviews")
def all_reviews():
   return ApiResponse(status_code=status.HTTP_200_OK,data=review_db)


