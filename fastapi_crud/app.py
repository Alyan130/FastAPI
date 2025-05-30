from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from dishName import getDishName

app=FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all for now
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class dish(BaseModel):
    id:int
    title:str
    price:str
    ingredients:List[str]


resturaunt:List[dish]=[
    dish(id=1, title="Margherita Pizza", price="$8.99", ingredients=["Tomato Sauce", "Mozzarella"]),
    dish(id=2, title="Spaghetti Carbonara", price="$11.50", ingredients=["Spaghetti", "Eggs", "Pancetta", "Parmesan"]),
    dish(id=3, title="Chicken Biryani", price="$9.99", ingredients=["Chicken", "Basmati Rice", "Yogurt", "Spices"]),
    dish(id=4, title="Beef Burger", price="$7.49", ingredients=["Beef Patty", "Lettuce", "Tomato", "Cheddar", "Bun"]),
    dish(id=5, title="Caesar Salad", price="$6.75", ingredients=["Romaine Lettuce", "Croutons", "Parmesan", "Caesar Dressing"]),
    dish(id=6, title="Vegetable Stir Fry", price="$7.99", ingredients=["Broccoli", "Carrots", "Bell Peppers", "Soy Sauce"]),
    dish(id=7, title="Sushi Roll", price="$10.25", ingredients=["Rice", "Nori", "Salmon", "Avocado", "Cucumber"]),
    dish(id=8, title="Tandoori Chicken", price="$12.00", ingredients=["Chicken", "Yogurt", "Lemon Juice", "Tandoori Spices"]),
    dish(id=9, title="Pancakes", price="$5.50", ingredients=["Flour", "Eggs", "Milk", "Maple Syrup"]),
    dish(id=10, title="Falafel Wrap", price="$6.99", ingredients=["Falafel", "Hummus", "Lettuce", "Tomato", "Wrap Bread"])
]

@app.get("/dishes")
def get_dishes():
    if len(resturaunt) > 0:
      return resturaunt
    else:
      return {"error":"No dish avalaible"}

@app.get("/name")
def getName():
  name = getDishName()
  return name

@app.get("/dishes/{dish_id}")
def get_dish(dish_id:int):
    for dish in resturaunt:
        if dish.id == dish_id:
            return dish
    return {"error":"Dish not found"}


@app.post("/dishes")
def create_dish(dish:dish):
   for d in resturaunt:
      if d.id == dish.id:
         return {"message":"Dish already available"}
   resturaunt.append(dish)
   return resturaunt


@app.put("/dish/{id}")
def update_dish(id:int, dish:dish):
  for index, dish in enumerate(resturaunt):
     if dish.id == id:
        resturaunt[index] = dish
  return {"error":"Dish not found"}

@app.delete("/dish/{id}")
def delete_dish(id:int):
 for index, dish in enumerate(resturaunt):
    if dish.id == id:
       resturaunt.pop(index)
 return {"error":"Dish not found"}
