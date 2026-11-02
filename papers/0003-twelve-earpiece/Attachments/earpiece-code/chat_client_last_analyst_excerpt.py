)
from schemas.chat_consumption import ChatFunctionConsumptionFn
from localization.core.languages import is_non_english, language_name
from localization.prompts.language_instruction import build_language_instruction

if TYPE_CHECKING:
    from services.mcp_integration.mcp_client import MCPClientManager


logger = getLogger(__name__)


LAST_ANALYST_INSTRUCTION = (
    "\n\n## You are the last analyst for this request\n"
    "This request has already been passed between analysts and cannot be "
    "passed on again -- a further transfer will be ignored and the user will "
    "receive nothing. Do not call any redirect function. Answer as much of the "
    "question as you can with the functions you have. If the question is "
    "genuinely outside what you can do, say so plainly and ask the user for "
    "the one thing that would let you help -- naming a single player, or a "
    "single team -- rather than transferring."
)

REDIRECT_REFUSED_MESSAGE = (
    "This request cannot be transferred to another analyst, and no transfer "
    "has taken place. Do not call any redirect function again. Answer the user "
    "now using the functions you have and the selection you already hold. If "
    "you genuinely cannot answer, say so plainly and ask the user for the one "
    "thing that would let you help."
)

