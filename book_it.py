from fastapi import FastAPI, Body, HTTPException
import requests
from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker, declarative_base
import uvicorn
from datetime import date
from pydantic import BaseModel

Base = declarative_base()
app = FastAPI()


class Book_it(BaseModel):
    books_name: str
    release_date: date
    author_name : str
    number_of_pages: int

class Book(Base):
    __tablename__='book'
    book_id=Column(Integer,primary_key=True)
    name_of_book=Column(String(120))
    release_date=Column(Date())
    author_name=Column(String(120))
    number_of_pages=Column(Integer())

engine = create_engine('mysql+pymysql://root:GeorgesNJ2001@localhost:3306/book_it')
Base.metadata.create_all(engine)
SessionLocal =sessionmaker(bind=engine)

session = SessionLocal()



@app.get('/book')
async def listing_books():
    all_books = session.query(Book).all()
    return {'List of all books': all_books}

@app.get('/books/${id}')
async def listing_one_book(id: int):
    one_book = session.query(Book).filter_by(book_id = id).first()
    if not one_book:
        raise HTTPException(status_code=404, detail=f"No such a book exist")
    else:
        return {"Details about the selected book": one_book.__dict__}


@app.delete("/books/${id}")
async def suppression(id : int):
    book_deleted = session.querry(Book).filter_by(book_id = id).first()
    if not book_deleted:
        raise HTTPException(status_code=404, detail=f"Book not found")
    else:
        session.delete(book_deleted)
        session.commit()
    return  {"message":"Book Succesfully deleted"}

@app.post("/book")
async def create(book: Book_it):
    book_created = Book(
        name_of_book=book.books_name,
        release_date=book.release_date,
        author_name=book.author_name,
        number_of_pages=book.number_of_pages
    )
    if book_created.number_of_pages < 2:
        raise HTTPException(status_code=404, detail=f"No such a book exist")
    elif book_created.release_date == date.today():
        raise HTTPException(status_code=404, detail=f"No such a book exist")
    else:
        session.add(book_created)
        session.commit()
        response={"message":"New book created successfully"}
        return response

@app.put("/books/${id}")
async def edit_book(id :int, book: Book_it):
    edited_book =session.query(Book).filter_by(book_id = id).first()
    if not edited_book:
        raise HTTPException(status_code=404,detail ="no such a book exists")
    edited_book.name_of_book = book.books_name
    edited_book.release_date = book.release_date
    edited_book.author_name = book.author_name
    edited_book.number_of_pages = book.number_of_pages
    if edited_book.number_of_pages < 2 or edited_book.release_date == date.today:
        raise HTTPException(status_code=404,detail ="Invalid book data, maybe try a high number of pages! or a different date")
    session.commit()
    return {"Message":"Book Succesfully updated"}



if __name__ =='__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)