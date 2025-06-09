import openai
import logging
from requests.exceptions import HTTPError, Timeout, RequestException
from typing import Optional, Any


def handle_file_errors(exc: Any) -> Optional[str]:
    if isinstance(exc, FileNotFoundError):
        return "Error: The file was not found."
    elif isinstance(exc, PermissionError):
        return "Error: Permission denied when trying to read the file."
    elif isinstance(exc, OSError):
        return "Error: An unexpected OS error occurred while reading the file."
    # nothing matched
    return None


def handle_openai_errors(exc: Any) -> Optional[str]:
    # Log full stack trace for diagnostics
    logging.exception("OpenAI exception caught")
    
    if isinstance(exc, openai.APIConnectionError):
        cause = exc.__cause__ or exc
        return f"Error: Could not reach OpenAI server ({cause})"
    elif isinstance(exc, openai.RateLimitError):
        return "Error: Rate limit exceeded. Please back off and retry shortly."
    elif isinstance(exc, openai.APIStatusError):
        return f"Error: OpenAI returned status {exc.status_code} - {exc.response}"
    return None


def handle_request_errors(exc: Any) -> Optional[str]:
    if isinstance(exc, HTTPError):
        return "Error: An HTTP error occurred while making the request."
    elif isinstance(exc, Timeout):
        return "Error: The request timed out."
    elif isinstance(exc, RequestException):
        return "Error: A network-level error occurred during the request."
    # Don’t always swallow exceptions—only catch what you expect
    return None
