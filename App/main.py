from fastapi import Depends, HTTPException, status, FastAPI, Request, APIRouter
from sqlalchemy.orm import Session
from . import schemas, crud, deps, models
from .email_service import send_email
from fastapi.responses import JSONResponse
from .api import user, organisation, member, role
from .database import engine
import logging

# Initialize the database
models.Base.metadata.create_all(bind=engine)

# Initialize FastAPI application
app = FastAPI()

# Create a router
router = APIRouter()

# Include the routers for various endpoints
app.include_router(user.router, prefix="/user", tags=["User"])
app.include_router(organisation.router, prefix="/organisation", tags=["Organisation"])
app.include_router(member.router, prefix="/member", tags=["Member"])
app.include_router(role.router, prefix="/role", tags=["Role"])

# Define your custom routes
@router.post("/signup")
async def signup(user: schemas.UserCreate, db: Session = Depends(deps.get_db)):
    new_user = crud.create_user(db=db, user=user)
    invite_link = f"http://localhost:8000/organisation/invite?token=some_unique_token"
    
    send_email(
        to_email=user.email,
        subject="Welcome to Our Service!",
        content=f"Thank you for signing up to our service. Click the link to join: {invite_link}"
    )
    return {"message": "User signed up successfully, invitation sent."}

@router.post("/reset-password/")
async def reset_password(email: str, db: Session = Depends(deps.get_db)):
    user = crud.get_user_by_email(db=db, email=email)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    send_email(
        to_email=user.email,
        subject="Password Updated Successfully",
        content="Your password has been updated. If this wasn't you, please contact support immediately."
    )
    return {"message": "Password updated and email sent successfully."}

@router.post("/signin")
async def signin(credentials: schemas.UserLogin, db: Session = Depends(deps.get_db)):
    user = crud.authenticate_user(db=db, email=credentials.email, password=credentials.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    access_token, refresh_token = crud.create_tokens(user=user)
    
    send_email(
        to_email=user.email,
        subject="New Login Alert",
        content="A new login to your account was detected. If this wasn't you, please contact support immediately."
    )
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.error(f"An error occurred: {exc}")
    return JSONResponse(
        status_code=500,
        content={"message": "Internal Server Error"}
    )

# Include the custom router in the FastAPI app
app.include_router(router, prefix="/auth")
