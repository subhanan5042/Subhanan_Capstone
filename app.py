from email import header
from operator import index
from flask import Flask, request, render_template, jsonify
from model import SentimentRecommenderModel


app = Flask(__name__)

sentiment_model = SentimentRecommenderModel()


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/PREDICTION', methods=['POST'])
def prediction():
    #GETTING USER FROM HTML FORM-FILL
    user=request.form['userName']
    #CONVERTING TO LOWER CASE FOR PROCESSING
    user=user.lower()
    items=sentiment_model.sentiment_recommendations_extract(user)

    if(not(items is None)):
        print(f"retrieving items....{len(items)}")
        print(items)
        # data=[items.to_html(classes="table-striped table-hover", header="true",index=False)
        return render_template("index.html", column_names=items.columns.values, row_data=list(items.values.tolist()), zip=zip)
    else:
        return render_template("index.html", message="USER NAME NOT FOUND. NO RECOMMENDATIONS!")


@app.route('/PREDICT-SENTIMENT', methods=['POST'])
def predict_sentiment():
    #GETTING THE REVIEW TEXT FROM HTML FORM
    review_text = request.form["reviewText"]
    print(review_text)
    pred_sentiment = sentiment_model.classify_sentiment(review_text)
    print(pred_sentiment)
    return render_template("index.html", sentiment=pred_sentiment)


if __name__ == '__main__':
    app.run()
