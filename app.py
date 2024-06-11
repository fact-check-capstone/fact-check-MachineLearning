from fastapi import FastAPI, Form
from pydantic import BaseModel
import pickle
import re
import string

# Load the SVM model
with open("models/svm.pkl", "rb") as file:
    svm_model = pickle.load(file)

# Load the vectorizer
with open("models/tfidf_vectorizer.pkl", "rb") as file:
    vectorizer = pickle.load(file)


# Preprocessing function (for cleaning text)
def preprocess_text(text):
    """
    Preprocesses the input text by converting it to lowercase, removing punctuation,
    digits, and extra spaces.

    Args:
    - text (str): The input text to be preprocessed.

    Returns:
    - str: The preprocessed text.
    """
    text = text.lower()
    text = re.sub(
        r"\(HOAX\)|\(FITNAH\)|\(SALAH\)|\(DISINFORMASI\)|\[SALAH\]|\[SALAH\]:", "", text
    )
    text = re.sub(f"[{re.escape(string.punctuation)}]", "", text)
    text = re.sub(r"\d+", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


app = FastAPI()


class PredictionOutput(BaseModel):
    """
    Represents the output data for the prediction endpoint.

    Attributes:
    - text (str): The input text.
    - is_hoax (bool): Indicates whether the input text is a hoax or not.
    """

    text: str
    is_hoax: bool


@app.post("/predict", response_model=PredictionOutput)
def predict(text: str = Form(...)):
    """
    Predicts whether the input text is a hoax or not.

    Args:
    - text (str): The input text to be analyzed for hoax detection.

    Returns:
    - PredictionOutput: The predicted label for the input text.
    """
    clean_text = preprocess_text(text)
    text_tfidf = vectorizer.transform([clean_text])

    svm_prediction = svm_model.predict(text_tfidf)[0]
    svm_result = bool(svm_prediction == 1)

    return PredictionOutput(text=text, clean_text=clean_text, is_hoax=svm_result)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080)
