from json import dumps
from requests_html import HTMLSession

HEADERS = {
    "sec_ch_ua": '(Not(A:Brand";v="8", "Chromium";v="99", "Google Chrome";v="99"',
    "sec_ch_ua_platform": "Linux",
    "user_agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.35 Safari/537.36",
}


def get_response(url):
    session = HTMLSession()
    response = session.get(url, headers=HEADERS)
    return response


def get_data(response):
    card_global = response.html.find("div.card-global")
    card_indonesia = response.html.find("div.card-indonesia")

    datas = [
        {
            "global": {
                "negara": card_global[0].find("h2", first=True).text,
                "terkonfirmasi": card_global[1].find("h2", first=True).text,
                "meninggal": card_global[2].find("h2", first=True).text,
                "update_terakhir": response.html.find("div.col-sm-12.card-title")[
                    0
                ].text.split(" ")[2],
            }
        },
        {
            "indonesia": {
                "positif": card_indonesia[0].find("h2", first=True).text,
                "negatif": card_indonesia[1].find("h2", first=True).text,
                "meninggal": card_indonesia[2].find("h2", first=True).text,
                "update_terakhir": response.html.find("div.col-sm-12.card-title")[-1]
                .find("p", first=True)
                .text.split(": ")[-1],
            }
        },
    ]

    return datas


def main():
    url = "http://covid19.go.id"
    response = get_response(url)
    datas = get_data(response)
    print(dumps(datas, indent=2))


if __name__ == "__main__":
    main()
