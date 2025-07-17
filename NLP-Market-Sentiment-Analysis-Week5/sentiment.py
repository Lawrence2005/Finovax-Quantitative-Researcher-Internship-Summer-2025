# Crypto Fear & Greed Index Fetching Required Packages
import requests
import pandas as pd
import matplotlib.pyplot as plt

# Crypto Fear & Greed Index Fetching and Plotting Functions
def get_FNG_index(limit=60, format='json', date_format='cn'):
    """
    Fetch the daily Fear and Greed Index data from the Alternative.me API.

    Parameters:
    limit (int): The number of entries to return (Default to 60, which returns the latest 60 days of data; set to 0 for all available data).
    format (str): The format of the response (Default to 'json').
    date_format (str): The format of the date in the response (Default to 'cn' for Chinese format; 'us', 'kr', and 'world' also available).

    Returns:
    pd.DataFrame: A date-indexed DataFrame containing the Fear and Greed Index values and their classifications.

    Raises:
    Exception: If the API request fails or returns an error status code.
    """

    url = "https://api.alternative.me/fng/"
    params = {
        "limit": limit,
        "format": format,
        "date_format": date_format
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()

        indices = pd.DataFrame(data['data'])
        indices = indices.sort_values('timestamp', ascending=True).reset_index(drop=True).set_index('timestamp')
        indices = indices[['value', 'value_classification']]

        return indices
    else:
        raise Exception(f"API request failed with status code {response.status_code}")

def plot_FNG_index(indices: pd.DataFrame):
    """
    Plot the Fear and Greed Index values and their classifications.

    Parameters:
    indices (pd.DataFrame): A DataFrame containing the Fear and Greed Index values and their classifications.
    """

    plt.figure(figsize=(14, 7))

    plt.plot(indices.index, indices['value'], label='Fear & Greed Index', color='blue')

    plt.title('Fear & Greed Index Over Time')
    plt.xlabel('Date')
    plt.ylabel('Index Value')
    
    plt.xticks(rotation=45)
    plt.grid()
    plt.legend()
    plt.tight_layout()
    plt.show()

# FINBERT Sentiment Analysis Required Packages
import pandas as pd
import scipy
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, roc_auc_score
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# FINBERT Model Loading and Sentiment Prediction Functions
def FINBERT_model_create():
    """
    Create and return the FINBERT model and tokenizer.

    Returns:
    tokenizer (AutoTokenizer): The tokenizer for the FINBERT model.
    model (AutoModelForSequenceClassification): The FINBERT model for sequence classification.
    """

    # Load the tokenizer and model from the pre-trained FINBERT model
    tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")
    model = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert")

    return tokenizer, model

def FINBERT_predict(tokenizer, model, texts: list[str] | str):
    """
    Predict sentiment using the FINBERT model.

    Parameters:
    tokenizer: The tokenizer for the FINBERT model.
    model: The FINBERT model.
    text (list[str] | str): The input text(s) to analyze.

    Returns:
    int: The predicted sentiment label.
    """

    if isinstance(texts, str):
        texts = [texts]

    predictions = {}
    tokenizer_kwargs = {"padding": True, "truncation": True, "max_length": 512}
    
    for t in texts:
        with torch.no_grad():
            input_sequence = tokenizer(t, return_tensors="pt", **tokenizer_kwargs)
            logits = model(**input_sequence).logits
            scores = {
                k: v
                for k, v in zip(
                    model.config.id2label.values(),
                    scipy.special.softmax(logits.numpy().squeeze()),
                )
            }
        sentimentFinbert = max(scores, key=scores.get)
        sentiment_prob = round(float(max(scores.values())), 2)

        predictions[t] = (sentimentFinbert, sentiment_prob)

    return predictions