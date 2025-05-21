# creating a pydantic model to create a data schema
from pydantic import (
    BaseModel,
    EmailStr,
    AnyUrl,
    Field,
    field_validator,
    model_validator,
    computed_field,
)
from typing import Optional, Annotated, Self
from address import Address


class Patient(BaseModel):
    name: Annotated[
        str,
        Field(
            max_length=50,
            title="Name of the patient",
            description="Name of the patient in less than fifty chars",
            examples=["Enrique", "John Doe"],
        ),
    ]
    email: Annotated[EmailStr, Field(max_length=80)]
    age: Annotated[int, Field(ge=0, lt=120)]
    linkedin: Optional[AnyUrl] = None
    weight: Annotated[float, Field(gt=0, strict=True)]
    height: Annotated[float, Field(gt=0, strict=True)]
    married: Annotated[
        bool,
        Field(
            default=False, title="Married status", description="Is the patient married?"
        ),
    ]
    allergies: Annotated[Optional[list[str]], Field(default=None, max_length=5)]
    contact_details: dict[str, str]
    address: Address

    # validator functions
    # so we should return the value are it is validated or any transformation is performed on it, otherwise it will be None
    @field_validator("email")
    @classmethod
    def validate_email(cls, value: EmailStr) -> EmailStr:
        """check if the email is in the allowed email domains"""
        valid_domains = ["hdfc.com", "icici.com"]
        if value.split("@")[1] not in valid_domains:
            raise ValueError(
                f"Email domain is not allowed, supported types: {valid_domains}"
            )
        return value

    @field_validator("name")
    @classmethod
    def transform_name(cls, value: str) -> str:
        """return name in title case"""
        return value.title()

    # this validates the field before implicit type conversion
    # @field_validator("age",mode='before')

    # this validates the field after implicit type conversion
    # @field_validator("age", mode="after")
    # @classmethod
    # def validate_age(cls, value: int) -> int:
    #     """check age"""
    #     if value < 100:
    #         return value
    #     else:
    #         raise ValueError("Age cannot be greater than 100 or less than zero")

    @model_validator(mode="after")
    def validate_emergency_contact(self) -> Self:
        if self.age > 60 and not self.contact_details.get("emergency_contact"):
            raise ValueError("Emergency contact is required for patients above 60")
        return self

    @computed_field
    @property
    def bmi(self) -> float:
        """calculate bmi"""
        return round(self.weight / (self.height**2), 2)
