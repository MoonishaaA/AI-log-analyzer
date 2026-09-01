from flask import Flask, jsonify
import logging
import random
import time

app = Flask(__name__)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s"
)

logger = logging.getLogger("demo-app")


@app.route("/")
def home():
    logger.info("Home endpoint accessed")

    return jsonify({
        "status": "success",
        "message": "AI Log Analyzer Demo Application"
    })


@app.route("/health")
def health():
    logger.info("Health check successful")

    return jsonify({
        "status": "healthy"
    })


@app.route("/login")
def login():
    logger.info("User login request received")

    return jsonify({
        "status": "success",
        "message": "User logged in"
    })


@app.route("/database")
def database():
    logger.info("Connecting to database")

    # Simulate database failure
    if random.choice([True, False]):
        logger.error(
            "Database connection failed: connection timeout"
        )

        return jsonify({
            "status": "error",
            "message": "Database connection failed"
        }), 500

    logger.info("Database connection successful")

    return jsonify({
        "status": "success",
        "message": "Database connection successful"
    })


@app.route("/redis")
def redis():
    logger.info("Connecting to Redis")

    if random.choice([True, False]):
        logger.error("Redis connection refused")

        return jsonify({
            "status": "error",
            "message": "Redis connection refused"
        }), 500

    logger.info("Redis connection successful")

    return jsonify({
        "status": "success",
        "message": "Redis connection successful"
    })


@app.route("/payment")
def payment():
    logger.info("Payment request received")

    if random.choice([True, False]):
        logger.error(
            "Payment service returned HTTP 500"
        )

        return jsonify({
            "status": "error",
            "message": "Payment processing failed"
        }), 500

    logger.info("Payment processed successfully")

    return jsonify({
        "status": "success",
        "message": "Payment successful"
    })


@app.route("/external-api")
def external_api():
    logger.info("Calling external API")

    time.sleep(1)

    if random.choice([True, False]):
        logger.error(
            "External API request timed out"
        )

        return jsonify({
            "status": "error",
            "message": "External API timeout"
        }), 504

    logger.info("External API request successful")

    return jsonify({
        "status": "success",
        "message": "External API request successful"
    })


@app.route("/authentication")
def authentication():
    logger.info("Authentication request received")

    if random.choice([True, False]):
        logger.warning(
            "Authentication failed for user"
        )

        return jsonify({
            "status": "error",
            "message": "Authentication failed"
        }), 401

    logger.info("Authentication successful")

    return jsonify({
        "status": "success",
        "message": "Authentication successful"
    })


@app.route("/random-error")
def random_error():

    errors = [
        "Database connection timeout",
        "Redis connection refused",
        "Authentication failed",
        "Payment service returned HTTP 500",
        "External API request timed out",
        "Insufficient memory available"
    ]

    error_message = random.choice(errors)

    logger.error(error_message)

    return jsonify({
        "status": "error",
        "message": error_message
    }), 500


if __name__ == "__main__":

    logger.info("Application starting")

    app.run(
        host="0.0.0.0",
        port=5000
    )
