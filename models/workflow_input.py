"""
Workflow Input Models
Pydantic models for workflow input validation with automatic domain normalization.
Supports AgentOS API integration with structured input schemas.
"""

from pydantic import BaseModel, Field, field_validator
from utils.workflow_helpers import normalize_domain


class WorkflowInput(BaseModel):
    """
    Input model for Octave Clone sales intelligence workflow.

    Automatically normalizes domain inputs to https:// format, accepting:
    - sendoso.com
    - www.sendoso.com
    - http://sendoso.com
    - https://sendoso.com

    All formats are normalized to: https://sendoso.com

    This model enables:
    1. Flexible user input (no need to type https://)
    2. AgentOS API integration with input validation
    3. Type safety for workflow parameters
    """

    vendor_domain: str = Field(
        description="Vendor's website domain (e.g., 'sendoso.com' or 'https://sendoso.com')"
    )
    prospect_domain: str = Field(
        description="Prospect's website domain (e.g., 'octavehq.com' or 'https://octavehq.com')"
    )

    @field_validator('vendor_domain', 'prospect_domain', mode='before')
    @classmethod
    def normalize_domain_field(cls, v, info):
        """Normalize domain to https:// format"""
        if not v:
            raise ValueError(f"{info.field_name} is required")
        return normalize_domain(v)


# Example usage:
# from models.workflow_input import WorkflowInput
#
# # User can provide flexible input
# user_input = WorkflowInput(
#     vendor_domain="sendoso.com",           # Auto-normalized to https://sendoso.com
#     prospect_domain="www.octavehq.com"     # Auto-normalized to https://octavehq.com
# )
#
# # Use with workflow (Pydantic v2 model_dump() replaces custom to_workflow_dict())
# workflow.print_response(input=user_input.model_dump(), stream=True)
