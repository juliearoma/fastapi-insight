from fastcrud import FastCRUD

from src.app.core.schemas import TokenBlacklistCreate, TokenBlacklistUpdate

from ..db.token_blacklist import TokenBlacklist

CRUDTokenBlacklist = FastCRUD[TokenBlacklist, TokenBlacklistCreate, TokenBlacklistUpdate, TokenBlacklistUpdate, None]
crud_token_blacklist = CRUDTokenBlacklist(TokenBlacklist)
