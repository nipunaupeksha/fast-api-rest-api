from sqlalchemy.orm import Session
from models.token import Token
from datetime import datetime


# Save token to check its validity
def save_token(db: Session, token: str, exp: datetime):
    db_token = Token(token=token, exp=exp)
    db.add(db_token)
    db.commit()
    db.refresh(db_token)


# Revoke token when logging out
def revoke_token(db: Session, token: str):
    db_token = db.query(Token).filter(Token.token == token).first()
    if db_token:
        db_token.is_revoked = True
        db.commit()


# Check token's validity with is_revoked value
def check_token_invalid(db: Session, token: str) -> bool:
    selected_token = db.query(Token).filter(Token.token == token).first()
    return selected_token.is_revoked if selected_token else True
