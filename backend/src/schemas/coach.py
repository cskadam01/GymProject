from typing import Annotated

from pydantic import BaseModel, StringConstraints


InviteCode = Annotated[str, StringConstraints(strip_whitespace=True, min_length=12, max_length=64)]


class JoinCoach(BaseModel):
    code: InviteCode
