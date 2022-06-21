from contextlib import contextmanager
from sqlalchemy import create_engine
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# pdialect+driver://username:password@host:port/database
engine = create_engine('mariadb+mariadbconnector://root:root@meta-soft.iptime.org:53306/temp')
Base = declarative_base()
Base.metadata.create_all(engine)
# DBSession = sessionmaker(bind=engine)
# session = DBSession()

@contextmanager
def session_scope():
    # Create a session
    Session = sqlalchemy.orm.sessionmaker()
    Session.configure(bind=engine)
    session = Session()
    try:
        yield session
        session.commit()
        print("try session commit")
    except:
        session.rollback()
        print("rollback")
        raise
    finally:
        session.close()



from . import UserView
from . import RoleUserView