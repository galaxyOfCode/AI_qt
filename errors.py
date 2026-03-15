"""Error handling utilities for AI Assistant application."""

import logging
from typing import Optional, Any
import openai
from requests.exceptions import HTTPError, Timeout, RequestException


def handle_file_errors(exc: Any) -> Optional[str]:
    """Handle file-related errors and return user-friendly messages."""

    if isinstance(exc, FileNotFoundError):
        return "Error: The file was not found."
    if isinstance(exc, PermissionError):
        return "Error: Permission denied when trying to read the file."
    if isinstance(exc, OSError):
        return "Error: An unexpected OS error occurred while reading the file."
    return None


def handle_openai_errors(exc: Any) -> Optional[str]:
    """Handle OpenAI API errors and return user-friendly messages."""

    logging.exception("OpenAI exception caught")

    if isinstance(exc, openai.APIConnectionError):
        cause = exc.__cause__ or exc
        return f"Error: Could not reach OpenAI server ({cause})"
    if isinstance(exc, openai.RateLimitError):
        return "Error: Rate limit exceeded. Please back off and retry shortly."
    if isinstance(exc, openai.APIStatusError):
        return f"Error: OpenAI returned status {exc.status_code} - {exc.response}"
    return None


def handle_request_errors(exc: Any) -> Optional[str]:
    """Handle network-related errors and return user-friendly messages."""
    if isinstance(exc, HTTPError):
        return "Error: An HTTP error occurred while making the request."
    if isinstance(exc, Timeout):
        return "Error: The request timed out."
    if isinstance(exc, RequestException):
        return "Error: A network-level error occurred during the request."
    return None
