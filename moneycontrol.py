import csv
import requests
import argparse
from datetime import date
from bs4 import BeautifulSoup


def read_schemes(scheme_file):
    """
    reads a csv scheme file and returns a list of (scheme, category, code) dicts,
    """
    acc = []
    with open(scheme_file, "r") as fp:
        reader = csv.DictReader(fp)
        return list(reader)


def write_prices(prices_file, prices):
    """
    writes a csv prices file with columns (scheme, category, code, price, date)
    """
    with open(prices_file, "w", newline="") as f:
        idxwriter = csv.DictWriter(f, fieldnames=["scheme", "category", "code", "price", "date"])
        idxwriter.writeheader()
        idxwriter.writerows(prices)


def fetch_nav_price(code):
    """
    Given a nav code, returns the latest price from moneycontrol
    """
    url = "https://www.moneycontrol.com/mutual-funds/nav/x/{}".format(code)
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    price = float(soup.find("span", class_="amt").text[2:])
    return price


def fetch_quote_price(code):
    """
    Given a quote code, returns the latest price from moneycontrol
    """
    url = "https://www.moneycontrol.com/india/stockpricequote/x/x/{}".format(code)
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    price = float(soup.find("span", id="Bse_Prc_tick").strong.text)
    return price


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--schemes',
                        help="schemes filename",
                        required=True)
    parser.add_argument('-o', "--output",
                        help="prices output",
                        required=True)

    args = parser.parse_args()
    schemes = read_schemes(args.schemes)
    prices = []

    today = date.today()
    for scheme in schemes:
        if scheme["category"] == "nav":
            price = fetch_nav_price(scheme["code"])
        else:
            price = fetch_quote_price(scheme["code"])

        data = {"scheme": scheme["scheme"],
                "category": scheme["category"],
                "code": scheme["code"],
                "price": price,
                "date": today}
        prices.append(data)

    write_prices(args.output, prices)
