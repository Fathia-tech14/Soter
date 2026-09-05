from typing import Generic, List, Optional, TypeVar
from pydantic import BaseModel, Field

T = TypeVar("T")

class AnchorMetadata(BaseModel):
    campaign_ref: Optional[str] = Field(None, examples=["campaign-2024-001"])
    claim_id: Optional[str] = Field(None, examples=["claim-abc123"])
    package_id: Optional[str] = Field(None, examples=["package-x7y8z9"])

    model_config = {
        "json_schema_extra": {
            "examples": [
                {"campaign_ref": "campaign-2024-001", "claim_id": "claim-abc123"}
            ]
        }
    }


class ResultEnvelope(BaseModel, Generic[T]):
    """      Standardized success-path envelope returned by all AI inference endpoints.\n\n    Fields\n    ------\n    result          The endpoint-specific payload (type varies by endpoint).\n    confidence      Aggregate confidence score in [0, 1], when meaningful.\n    reasons         Human-readable list of reasons / explanations.\n    anchor_metadata Pass-through of the caller-supplied correlation metadata.\n    trace_id        Request-scoped correlation ID echoed from the\n                    X-Correlation-Id / X-Request-Id header for distributed\n                    tracing.\n    prompt_version  Version of the prompt template used for verification/inference.\n    """\n
    result: T\n    confidence: Optional[float] = Field(\n        None,\n        ge=0.0,\n        le=1.0,\n        description="Aggregate confidence score in [0, 1].",\n        examples=[0.92],\n    )\n    reasons: Optional[List[str]] = Field(\n        None,\n        description="Human-readable explanations or reasons for the result.",\n        examples=[["Liveness verification passed"]],\n    )\n    anchor_metadata: Optional[AnchorMetadata] = None\n    trace_id: Optional[str] = Field(\n        None,\n        description="Request-scoped correlation ID for distributed tracing.",\n        examples=["a1b2c3d4-e5f6-7890-abcd-ef1234567890"],\n    )\n    prompt_version: Optional[str] = Field(\n        None,\n        description="Version of the prompt template used for verification.",\n        examples=["v1"],\n    )\n    requires_review: Optional[bool] = Field(\n        None,\n        description="Flag indicating if the result requires manual human review.",\n        examples=[False],\n    )\n    confidence_banding: Optional[str] = Field(\n        None,\n        description="Confidence classification banding: HIGH, MEDIUM, LOW, UNKNOWN.",\n        examples=["HIGH"],\n    )\n