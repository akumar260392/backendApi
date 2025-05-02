from sqlalchemy import create_engine, Integer, String, Column
from sqlalchemy.orm import sessionmaker, declarative_base
from fastapi import HTTPException, FastAPI
from pydantic import BaseModel

app = FastAPI()

engine = create_engine('sqlite:///backend.db', echo=True)
Base = declarative_base()

class Login(Base):
    __tablename__ = "login"
    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)

Session = sessionmaker(bind=engine, autocommit=False, autoflush=False)
session = Session()

Base.metadata.create_all(engine)

# Pydantic model for request body
class UserInfo(BaseModel):
    email: str
    password: str

@app.post("/signup")
def CreateUser(userinfo: UserInfo):
    existing = session.query(Login).filter(Login.email == userinfo.email).first()
    if not existing:
        session.add(Login(email=userinfo.email, password=userinfo.password))
        session.commit()
        return {"message": "User Created"}
    else:
        raise HTTPException(status_code=409, detail="Email already exists")

@app.post("/login")
def Login_user(userinfo: UserInfo):
    user = session.query(Login).filter(Login.email == userinfo.email).first()
    if user:
        if userinfo.password == user.password:
            return {"message": "User Login Successful"}
        else:
            raise HTTPException(status_code=401, detail="Invalid Password")
    else:
        raise HTTPException(status_code=404, detail="User Not Found")



if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend_new:app", host="0.0.0.0", port=8000, reload=True)
