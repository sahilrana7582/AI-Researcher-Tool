from pydantic import BaseModel, ConfigDict, Field


class ResearchRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    query: str = Field(
        min_length=1,
        max_length=5000,
        description="The research question to answer.",
        examples=["What are the main benefits of retrieval-augmented generation?"],
    )


class ResearchResponse(BaseModel):
    answer: str