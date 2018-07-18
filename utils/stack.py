from database.database import Database
import uuid




class Stack:
     def __init__(self):
         self.items = []

     def __repr__(self):
         return f"<Stack with {len(self.items)} inside>"

     def isEmpty(self):
         return self.items == []

     def push(self, item):
         self.items.insert(0,item)

     def pop(self):
         return self.items.pop(0)

     def first(self):
         return self.items[1]

     def peek(self):
         return self.items[len(self.items)-1]

     def size(self):
         return len(self.items)

     def save_to_db(self):
         Database.update('routes', {'route': self.items}, {'$set': {'route': self.items}, '$inc': {'count': 1} })
