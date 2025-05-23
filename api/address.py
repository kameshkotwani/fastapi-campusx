from pydantic import BaseModel, Field
from typing import Annotated


class Address(BaseModel):
    city: Annotated[str, Field(..., description="The city where the house is located.")]
    state: Annotated[
        str, Field(..., description="The state where the house is located.")
    ]
    pincode: Annotated[
        int, Field(..., description="The pincode of the house location.")
    ]
