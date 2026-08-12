from fastapi import APIRouter

from app.common.utils import try_parse_uuid
from app.core.dependency import CurrentUserDep
from app.core.exception import UnauthorizedError
from app.modules.users.dependency import UserServiceDep
from app.modules.users.model import User
from app.modules.users.schema import UserResponse

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=UserResponse)
async def get_me(
    service: UserServiceDep,
    current_user: CurrentUserDep,
) -> User:
    user_id = try_parse_uuid(current_user.get("sub"))
    if not user_id:
        raise UnauthorizedError(detail="Invalid token subject")
    return await service.get(user_id)
