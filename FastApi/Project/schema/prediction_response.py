from pydantic import BaseModel, Field
from typing import Annotated, Dict

class PredictionResponse(BaseModel):
    predicted_Category: Annotated[str, Field(..., description="The predicted insurance premimum category", example="High")]
    confidence: Annotated[float, Field(..., description="Models confidence score for predicted class(0 to 10)", example=0.853)]
    class_probabilities: Annotated[dict, Field(...,description="Probability distribution among all different classes", example={"Low": 0.01, "Medium": 0.15, "High": 0.84})]
    