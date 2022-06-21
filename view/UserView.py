from email.mime import base
from ntpath import join
from flask import Blueprint

import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, select
from sqlalchemy import ForeignKey
from sqlalchemy.orm import declarative_base, relationship

import db_connector
from . import RoleUserView

from .base import Base

from itertools import product


class User(Base):
   __tablename__ = 'tb_user'
   id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
   username = sqlalchemy.Column(sqlalchemy.String(length=100))
   password = sqlalchemy.Column(sqlalchemy.String(length=100))
   name = sqlalchemy.Column(sqlalchemy.String(length=30))
   email = sqlalchemy.Column(sqlalchemy.String(length=50))
   last_modified_password_date = sqlalchemy.Column(sqlalchemy.DateTime)
   status = sqlalchemy.Column(sqlalchemy.String(length=10), default="T")
   created_date = sqlalchemy.Column(sqlalchemy.DateTime)
   last_modified_date = sqlalchemy.Column(sqlalchemy.DateTime)

   role_user = relationship("RoleUser", backref='user')

   def __str__(self):
    return '[ id: {0}, username: {1}, password: {2}, name: {3}, email: {4}, last_modified_password_date: {5}, status: {6}, created_date: {7}, last_modified_date: {8} ]'.format(self.id, self.username, self.password, self.name, self.email, self.last_modified_password_date, self.status, self.created_date, self.last_modified_date)

Base.metadata.create_all(db_connector.engine)

# Create a session
Session = sqlalchemy.orm.sessionmaker()
Session.configure(bind=db_connector.engine)
session = Session()

# def addEmployee(firstName,lastName):
#    newEmployee = Employee(firstname=firstName, lastname=lastName)
#    session.add(newEmployee)
#    session.commit()

def selectAll(session):
    users = session.query(User).all()
    print("select ALL")
    for user in users:
        print(" - " + user.username + ' ' + user.name)

    # print(type(users))
    return users

def selectAllJoin(session): 
    users = session.query(User).join(RoleUserView.RoleUser).all()
    print("select ALL")
    for user in users:
        print(" - " + user.username + ' ' + user.name + ' ')
        # print(str(user.role_user))
        print(type(user.role_user), '\n')
        print(dir(user.role_user))

    # print(type(users))
    return users

# q = session.query(Table1.field1, Table1.field2)\
#     .outerjoin(Table2)\ # use in case you have relationship defined
#     # .outerjoin(Table2, Table1.id == Table2.table_id)\ # use if you do not have relationship defined
#     .filter(Table2.tbl2_id == None)    

def selectById(search_id): 
    user = session.query(User).filter_by()

def selectByStatus(search_username):
   users = session.query(User).filter_by(username=search_username)
   for user in users:
       print(" - " + user.username + ' ' + user.name)

# def updateEmployeeStatus(id, isActive):
#    user = session.query(User).get(id)
#    employee.active = isActive
#    session.commit()

# def deleteEmployee(id):
#    session.query(Employee).filter(Employee.id == id).delete()
#    session.commit()

# Add some new employees
# addEmployee("Bruce", "Wayne")
# addEmployee("Diana", "Prince")
# addEmployee("Clark", "Kent")

# Show all employees
# print('All Employees')
# selectAll()
# print("----------------")

# Update employee status
# updateEmployeeStatus(2,False)

# Show active employees
# print('Active Employees')
# selectByStatus(True)
# print("----------------")

# Delete employee
# deleteEmployee(1)

# Show all employees
# print('All Employees')
# selectAll()
# print("----------------")