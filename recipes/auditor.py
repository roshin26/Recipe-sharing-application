import json
import logging
# pyrefly: ignore [missing-import]
from transformers import pipeline

logger = logging.getLogger(__name__)

# Lazy-load the classifier so the model only downloads once on first use
_classifier = None


def _get_classifier():
    """Lazy-load the zero-shot classification pipeline."""
    global _classifier
    if _classifier is None:
        logger.info("Loading Hugging Face zero-shot classifier (first time may take a minute)...")
        _classifier = pipeline(
            "zero-shot-classification",
            model="facebook/bart-large-mnli",
        )
    return _classifier


# The dietary labels the AI will classify against
DIETARY_LABELS = [
    "contains meat",
    "contains seafood or fish",
    "contains dairy",
    "contains eggs",
    "contains gluten",
    "contains nuts",
    "vegan friendly",
    "vegetarian friendly",
]

# Mapping from AI labels to user-friendly badge text and emoji
LABEL_DISPLAY = {
    "contains meat": {"text": "Contains Meat", "emoji": "🥩", "css_class": "badge-meat"},
    "contains seafood or fish": {"text": "Contains Seafood", "emoji": "🐟", "css_class": "badge-seafood"},
    "contains dairy": {"text": "Contains Dairy", "emoji": "🧀", "css_class": "badge-dairy"},
    "contains eggs": {"text": "Contains Eggs", "emoji": "🥚", "css_class": "badge-eggs"},
    "contains gluten": {"text": "Contains Gluten", "emoji": "🌾", "css_class": "badge-gluten"},
    "contains nuts": {"text": "Contains Nuts", "emoji": "🥜", "css_class": "badge-nuts"},
    "vegan friendly": {"text": "Vegan", "emoji": "🌱", "css_class": "badge-vegan"},
    "vegetarian friendly": {"text": "Vegetarian", "emoji": "🥬", "css_class": "badge-vegetarian"},
}

# Confidence threshold — only tag if the AI is this confident
CONFIDENCE_THRESHOLD = 0.70


def audit_ingredients(ingredients_text):
    """
    Uses a Hugging Face Zero-Shot NLP Classifier to analyze raw ingredient
    text and return a list of dietary tags with confidence scores.

    Args:
        ingredients_text (str): The raw text of recipe ingredients.

    Returns:
        list[dict]: A list of dietary tag dicts, e.g.:
            [{"label": "contains meat", "text": "Contains Meat",
              "emoji": "🥩", "css_class": "badge-meat", "confidence": 0.94}]
    """
    if not ingredients_text or len(ingredients_text.strip()) < 5:
        return []

    try:
        classifier = _get_classifier()
        result = classifier(
            ingredients_text,
            DIETARY_LABELS,
            multi_label=True,  # A recipe can match multiple labels
        )

        tags = []
        for label, score in zip(result["labels"], result["scores"]):
            if score >= CONFIDENCE_THRESHOLD:
                display = LABEL_DISPLAY.get(label, {})
                tags.append({
                    "label": label,
                    "text": display.get("text", label),
                    "emoji": display.get("emoji", "🏷️"),
                    "css_class": display.get("css_class", "badge-default"),
                    "confidence": round(score, 2),
                })

        return tags

    except Exception as e:
        logger.error(f"AI Auditor error: {e}")
        return []
