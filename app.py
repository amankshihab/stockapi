import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify
from flask_restful import Resource, Api
from datetime import datetime

app = Flask(__name__)
api = Api(app)

class stonks(Resource):
    def get(self, ticker):
        
        info = {}

        url = f"https://in.finance.yahoo.com/quote/{ticker}?p={ticker}&.tsrc=fin-srch"

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
        }

        try:
            stock_page = requests.get(url, headers = headers)
        except:
            print("Could not get page")

        stock = BeautifulSoup(stock_page.text, 'html.parser')

        stock_price = stock.findAll("span", class_ = "Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)")

        if stock.findAll("span", class_ = "Trsdu(0.3s) Fw(500) Pstart(10px) Fz(24px) C($negativeColor)"):
            change = stock.findAll("span", class_ = "Trsdu(0.3s) Fw(500) Pstart(10px) Fz(24px) C($negativeColor)")
        else:
            change = stock.findAll("span", class_ = "Trsdu(0.3s) Fw(500) Pstart(10px) Fz(24px) C($positiveColor)")

        info['Change'] = change[0].get_text()
        info['Price/share'] = stock_price[0].get_text()
        info['Ticker'] = ticker
        info['Last Checked:'] = datetime.now()
        
        return(jsonify(info))

api.add_resource(stonks, '/<string:ticker>')

if __name__ == "__main__":
    app.run(debug = True)