import os
from flask import Flask, request, jsonify
from openai import OpenAI

app = Flask(__name__)

# Read API key from environment variable
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    print("WARNING: OPENAI_API_KEY is not configured")

client = OpenAI(
    api_key=api_key
) if api_key else None


@app.route("/health", methods=["GET"])
def health():

    return jsonify({
        "status": "healthy",
        "service": "ai-log-analyzer"
    })


@app.route("/analyze", methods=["POST"])
def analyze_log():

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body is required"
        }), 400

    if "log" not in data:
        return jsonify({
            "error": "log field is required"
        }), 400

    log_message = data["log"]

    # Basic log filtering
    if "ERROR" not in log_message and "CRITICAL" not in log_message:
        return jsonify({
            "message": "Log does not require AI analysis",
            "log": log_message
        })

    if client is None:
        return jsonify({
            "error": "OPENAI_API_KEY is not configured"
        }), 500

    prompt = f"""
You are an expert DevOps and SRE log analysis assistant.

Analyze the following application log:

{log_message}

Provide the result using exactly these sections:

Severity:
Root Cause:
Impact:
Recommendation:

Requirements:

- Determine whether the issue is LOW, MEDIUM, HIGH, or CRITICAL.
- Explain the probable root cause.
- Explain the impact on the application.
- Give practical troubleshooting/remediation steps.
- Keep the response concise.
"""

    try:

        response = client.responses.create(
            model="gpt-5-mini",
            input=prompt
        )

        analysis = response.output_text

        return jsonify({
            "log": log_message,
            "analysis": analysis
        })

    except Exception as e:

        return jsonify({
            "error": "AI analysis failed",
            "details": str(e)
        }), 500


if __name__ == "__main__":

    print("AI Log Analyzer starting...")

    app.run(
        host="0.0.0.0",
        port=8000
    )
