from transformers import pipeline

# 🔹 Load AI models (runs once)
classifier = pipeline("zero-shot-classification")
sentiment = pipeline("sentiment-analysis")

# 🔹 Labels
CATEGORIES = ["Billing", "Technical", "Account", "General"]
SEVERITY_LEVELS = ["Low", "Medium", "High"]

# 🔹 Optional keyword boost (hybrid = more accurate)
HIGH_PRIORITY_WORDS = [
    "urgent", "immediately", "asap",
    "not working at all", "payment failed",
    "refund not received", "error again and again"
]


def process_message(message: str):
    message_lower = message.lower()

    # 🧠 1. Category detection (AI)
    category_result = classifier(message, CATEGORIES)
    category = category_result["labels"][0]

    # 🧠 2. Severity detection (AI)
    severity_result = classifier(message, SEVERITY_LEVELS)
    severity = severity_result["labels"][0]

    # 🧠 3. Sentiment analysis (AI)
    sentiment_result = sentiment(message)[0]

    # ⚡ 4. Hybrid boost (VERY IMPORTANT)
    # If strong keywords → force High
    if any(word in message_lower for word in HIGH_PRIORITY_WORDS):
        severity = "High"

    # If negative tone and low → upgrade to Medium
    elif sentiment_result["label"] == "NEGATIVE" and severity == "Low":
        severity = "Medium"

    # 🎫 5. Escalation logic
    escalate = severity == "High"

    # 💬 6. Smart responses
    if severity == "Low":
        response = "Sure! I can help you with that. Let me guide you."
    elif severity == "Medium":
        response = "I understand your issue. I'll assist you and escalate if needed."
    else:
        response = "This seems critical. I'm escalating your issue to our support team immediately."

    return {
        "response": response,
        "category": category,
        "severity": severity,
        "escalate": escalate
    }
