from database.database import Database
import uuid


class Stack:
     def __init__(self):
         self.items = []

     def __repr__(self):
         return f"<Stack with {len(self.items)} inside>"

     def empty(self):
         """
         checks if stack is empty

         returns: Bool

         """
         return len(self.items) == 0

     def push(self, path):
         """
         inserts into stack at the begining

         @param path: current path in the file system

         """
         # Insert at top of stack
         self.items.insert(0,path)

     def pop(self):

         """
         removes from top of stack

         """
         # Remove from top of stack
         del self.items[0]

     def position(self,index):

         """
         returns an element at a givin position inside the stack

         @param index: position inside of the stack

         @returns: String

         """
         return self.items[index]

     def end(self):

         """
         returns element at the end of the stack

         @returns: String

         """
         return self.items[len(self.items)-1]

     def size(self):
         """
         returns size of the stack

         @returns: Integer

         """
         return len(self.items)

     def save_to_db(self):
         """
         saves self.items to database if the same path is already in the database, increment the count by 1

         """
         Database.update('routes', {'route': self.items}, {'$set': {'route': self.items}, '$inc': {'count': 1} })
