from transformers import pipeline

class ChatModerationAgent:
    def __init__(self):
        # Load Hugging Face toxic comment classifier
        self.classifier = pipeline("text-classification", model="unitary/toxic-bert")

    def moderate(self, message: str):
        if not message or message.strip() == "":
            return {"status": "Empty", "reason": "No message provided."}

        # Run prediction
        results = self.classifier(message)

        # Example output: [{'label': 'toxic', 'score': 0.98}]
        label = results[0]['label']
        score = results[0]['score']

        if label.lower() in ["toxic", "insult", "threat", "hate"]:
            return {
                "status": "Abusive",
                "reason": f"Message flagged as {label} with confidence {score:.2f}"
            }
        else:
            return {
                "status": "Safe",
                "reason": f"Message classified as non-toxic with confidence {score:.2f}"
            }
