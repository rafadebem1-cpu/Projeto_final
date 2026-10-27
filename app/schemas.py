from pydantic import BaseModel, Field, StrictInt, field_validator, ConfigDict


class PredictionRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    pixels: list[StrictInt] = Field(
        min_length=784,
        max_length=784,
        description="Exatamente 784 pixels, cada um entre 0 e 255."
    )

    @field_validator("pixels")
    @classmethod
    def validar_faixa_pixels(cls, pixels: list[int]) -> list[int]:
        if any(pixel < 0 or pixel > 255 for pixel in pixels):
            raise ValueError("Cada pixel deve estar entre 0 e 255.")
        return pixels


class PredictionResponse(BaseModel):
    predicted_digit: StrictInt = Field(
        ge=0,
        le=9,
        description="Dígito previsto pelo modelo."
    )