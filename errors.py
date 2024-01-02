import openai
from requests.exceptions import HTTPError, Timeout, RequestException


def handle_file_errors(exception) -> str:
    if isinstance(exception, FileNotFoundError):
        content = ("Error: The file was not found.")
    if isinstance(exception, PermissionError):
        content = ("Error: Permission denied when trying to read the file.")
    if isinstance(exception, OSError):
        content = (
            "Error: An error occurred while reading from the file the file.")
    return content


def handle_openai_errors(exception) -> str:
    if isinstance(exception, openai.APIConnectionError):
        content = "The server could not be reached\n" + \
            str(exception.__cause__)
    if isinstance(exception, openai.RateLimitError):
        content = "A 'Rate Limit Notice' was received; we should back off a bit."
    if isinstance(exception, openai.APIStatusError):
        content = "A non-200-range status code was received: " + \
            str(exception.status_code) + " " + str(exception.response)
    return content


def handle_request_errors(exception) -> str:
    if isinstance(exception, HTTPError):
        content = "An HTTP error occurred"
    if isinstance(exception, Timeout):
        content = "The request timed-out"
    if isinstance(exception, RequestException):
        content = "An exception occurred while handling your request"
    if isinstance(exception, Exception):
        content = "An unexpected error occurred"
    return content
