from fastapi import APIRouter, Depends

from app.models import User
from app.api.dependencies import require_roles

router = APIRouter(prefix='/test')

@router.get('/hello')
def test_endpoint(current_user: User = Depends(require_roles('ADMIN'))):
    return current_user
