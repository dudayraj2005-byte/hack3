from transformers import pipeline

classifier = pipeline("zero-shot-classification")
sentiment = pipeline("sentiment-analysis")

CATEGORIES = ["Billing", "Technical", "Account", "General"]
SEVERITY_LEVELS = ["Low", "Medium", "High"]


def process_message(message: str):
    # 1. Category (AI)
    category_result = classifier(message, CATEGORIES)
    category = category_result["labels"][0]

    # 2. Severity (AI 🔥)
    severity_result = classifier(message, SEVERITY_LEVELS)
    severity = severity_result["labels"][0]

    # 3. Optional: sentiment boost (hybrid)
    sentiment_result = sentiment(message)[0]

    # If very negative → increase severity
    if sentiment_result["label"] == "NEGATIVE" and severity == "Low":
        severity = "Medium"

    # 4. Escalation logic
    escalate = severity == "High"

    # 5. Response (slightly smarter)
    if severity == "Low":
        response = "I can help you with that. Let me guide you."
    elif severity == "Medium":
        response = "I understand the issue. I'll assist you, and escalate if needed."
    else:
        response = "This seems critical. I'm escalating this to our support team right away."

    return {
        "response": response,
        "category": category,
        "severity": severity,
        "escalate": escalate
    }
