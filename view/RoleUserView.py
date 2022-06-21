from flask import Blueprint
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import ForeignKey as foreign_key
import db_connector
from sqlalchemy.orm import declarative_base, relationship

from .base import Base

class RoleUser(Base):
   __tablename__ = 'tb_role_user'
   user_id = sqlalchemy.Column(sqlalchemy.Integer,  foreign_key("tb_user.id"), primary_key=True)
   role_id = sqlalchemy.Column(sqlalchemy.Integer, foreign_key("tb_role.id"))

#    user = relationship("User", backref="roleUsers")

   def __str__(self):
    return '[ user_id: {0}, role_id: {1} ]'.format(self.user_id, self.role_id)

# Base.metadata.create_all(db_connector.engine)

# # Create a session
# Session = sqlalchemy.orm.sessionmaker()
# Session.configure(bind=db_connector.engine)
# session = Session()

# # def addEmployee(firstName,lastName):
# #    newEmployee = Employee(firstname=firstName, lastname=lastName)
# #    session.add(newEmployee)
# #    session.commit()

# def selectAll(session):
#     # users = session.query(User).all()
#     slsect()
#     print("select ALL")
#     for user in users:
#         print(" - " + user.username + ' ' + user.name)

#     # print(type(users))
#     return users

# def selectById(search_id): 
#     user = session.query(User).filter_by()

# def selectByStatus(search_username):
#    users = session.query(User).filter_by(username=search_username)
#    for user in users:
#        print(" - " + user.username + ' ' + user.name)

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