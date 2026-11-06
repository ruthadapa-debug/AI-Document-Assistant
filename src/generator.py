
import os
import time
import streamlit as st
from google import genai


def get_api_key():
    """Read the Gemini API key from Streamlit secrets or environment."""

    try:
        api_key = st.secrets.get("GEMINI_API_KEY")
    except Exception:
        api_key = None

    if not api_key:
        api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError(
            "Gemini API key is missing. Add it to "
            ".streamlit/secrets.toml."
        )

    return api_key


def generate_answer(question, context):
    """Generate a document-based answer using Gemini."""

    try:
        client = genai.Client(api_key=get_api_key())
    except Exception as e:
        return f"API setup error: {e}"

    prompt = f"""
You are Docu AI, an AI document assistant.

Answer the user's question using ONLY the document context below.

Instructions:
1. Give a clear, simple, helpful answer.
2. Use bullet points when useful.
3. Do not invent information.
4. If the answer is not present in the context, say:
   "I could not find the answer in the document."

DOCUMENT CONTEXT:
{context}

USER QUESTION:
{question}

ANSWER:
"""

    # Try the preferred model first, followed by alternatives.
    models = [
        "gemini-3.6-flash",
        "gemini-2.5-flash-lite",
        "gemini-2.0-flash",
    ]

    last_error = None

    for model in models:
        for attempt in range(3):
            try:
                response = client.models.generate_content(
                    model=model,
                    contents=prompt,
                )

                if response.text:
                    return response.text

                return (
                    "Gemini returned an empty answer. "
                    "Please try asking your question again."
                )

            except Exception as e:
                last_error = e
                error_text = str(e).lower()

                is_quota_error = (
                    "429" in error_text
                    or "resource_exhausted" in error_text
                    or "quota" in error_text
                )

                is_model_error = (
                    "404" in error_text
                    or "not found" in error_text
                    or "not supported" in error_text
                )

                is_temporary_error = (
                    "503" in error_text
                    or "500" in error_text
                    or "unavailable" in error_text
                    or "service unavailable" in error_text
                )

                # Try the next model if this model is unavailable
                # or its quota has been exhausted.
                if is_quota_error or is_model_error:
                    break

                # Retry temporary server errors.
                if is_temporary_error and attempt < 2:
                    time.sleep(2 * (attempt + 1))
                    continue

                # Stop retrying this model.
                if is_temporary_error:
                    break

                # Display the actual error for troubleshooting.
                return f"Gemini API error ({model}): {e}"

    # All models failed. Explain the most likely cause.
    error_text = str(last_error).lower() if last_error else ""

    if (
        "429" in error_text
        or "resource_exhausted" in error_text
        or "quota" in error_text
    ):
        return (
            "Your Gemini API quota may be exhausted. Check your API "
            "usage and limits in Google AI Studio. You may need to "
            "wait for the quota to reset or review your billing settings. "
            "Trying another model does not guarantee additional quota."
        )

    return (
        "Gemini could not generate an answer using the available models.\n\n"
        f"Last API error: {last_error}\n\n"
        "Check your API key, model availability, and internet connection."
    )
