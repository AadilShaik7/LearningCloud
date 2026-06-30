from pydantic import BaseModel, Field, field_validator


class TaskCreate(BaseModel):
    title: str = Field(
        min_length=1,
        max_length=200,
        description="Short description of the task",
    )

    @field_validator("title")
    @classmethod
    def title_cannot_be_blank(cls, value: str) -> str:
        cleaned_value = value.strip()

        if not cleaned_value:
            raise ValueError("Title cannot be empty or only spaces")

        return cleaned_value


class TaskResponse(BaseModel):
    id: int
    title: str
    completed: bool