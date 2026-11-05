from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal


def get_db():
    with SessionLocal() as session:
        yield session              # the route runs here; then the session is closed


SessionDep = Annotated[Session, Depends(get_db)]
