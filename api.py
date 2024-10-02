from fastapi import FastAPI, Depends, HTTPException, status, Form
from fastapi.security import OAuth2PasswordBearer
from auth import verify_password, create_access_token
from settings import VALID_USERNAME, HASHED_PASSWORD

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.post("/token")
async def login_for_access_token(
    username: str = Form(...),  # Принимаем username как данные формы
    password: str = Form(...)   # Принимаем password как данные формы
):
    if username != VALID_USERNAME or not verify_password(password, HASHED_PASSWORD):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": username})
    return {"access_token": access_token, "token_type": "bearer"}
