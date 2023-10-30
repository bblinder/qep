from opentelemetry import trace
import requests
from flask import Flask, request
from waitress import serve

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello'

@app.route('/test')
def test_it():
    return 'OK'

@app.route('/check')
def credit_check():
    customernumber = request.args.get('customernum')

    current_span = trace.get_current_span()
    current_span.set_attribute("broker_id", customernumber)
    
    # Get Credit Score
    creditScoreReq = requests.get("http://creditprocessorservice:8899/getScore?customernum=" + customernumber)
    creditScore = int(creditScoreReq.text)
    creditScoreCategory = getCreditCategoryFromScore(creditScore)

    current_span = trace.get_current_span()
    current_span.set_attribute("score", creditScoreCategory)

    # Run Credit Check
    creditCheckReq = requests.get("http://creditprocessorservice:8899/runCreditCheck?customernum=" + str(customernumber) + "&score=" + str(creditScore))
    checkResult = str(creditCheckReq.text)

    return checkResult

def getCreditCategoryFromScore(score):
    creditScoreCategory = ''
    match score:
        case num if num > 850:
            creditScoreCategory = 'impossible'
        case num if 800 <= num <= 850 :
            creditScoreCategory = 'exceptional'
        case num if 740 <= num < 800 :
            creditScoreCategory = 'very good'
        case num if 670 <= num < 740 :
            creditScoreCategory = 'good'
        case num if 580 <= num < 670 :
            creditScoreCategory = 'fair'
        case num if 300 <= num < 580 :
            creditScoreCategory = 'poor'
        case _:
            creditScoreCategory = 'impossible'
    return creditScoreCategory

if __name__ == '__main__':
    serve(app, port=8888)