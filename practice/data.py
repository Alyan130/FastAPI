from models import Book , Review
from typing import List

book_db:List[Book] = [
    Book(book_id=1,
         title="Living Legend",
         author="Peter chen",
         genre="adventure",
         year=2022
        ),
         Book(
        book_id=2,
        title="The Silent Echo",
        author="Emily Watson",
        genre="horror",
        year=2021
    ),
    Book(
        book_id=3,
        title="Stars Beyond Us",
        author="Neil Cosmos",
        genre="astronomy",
        year=2023
    ),
    Book(
        book_id=4,
        title="The Forgotten Kingdom",
        author="Sarah Rivers",
        genre="fiction",
        year=2020
    )
]


review_db:List[Review] = [
   
]


