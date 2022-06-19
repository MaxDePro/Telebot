import requests
from bs4 import BeautifulSoup

url_usd = 'https://www.google.com/search?q=%D0%BA%D1%83%D1%80%D1%81+%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80%D0%B0+%D0%BA+%D0%B3%D1%80%D0%B8%D0%B2%D0%BD%D0%B5&oq=%D0%BA%D1%83%D1%80%D1%81+%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80%D0%B0+%D0%BA+&aqs=chrome.2.69i57j35i39l2j0i20i263i512j0i512l6.6186j1j7&sourceid=chrome&ie=UTF-8'
url_eur = 'https://www.google.com/search?q=euro+%D0%BA+%D0%B3%D1%80%D0%B8%D0%B2%D0%BD%D0%B5&sxsrf=ALiCzsZ0iA8iVVDjoXlNv0SBcJo1YNktDw%3A1653903583139&ei=35CUYpqCCIqOrwTI1rL4DQ&oq=e+%D0%BA+%D0%B3%D1%80%D0%B8%D0%B2%D0%BD%D0%B5&gs_lcp=Cgdnd3Mtd2l6EAMYADIGCAAQHhAHMgYIABAeEAcyBggAEB4QBzIGCAAQHhAHMgYIABAeEAcyBggAEB4QBzIGCAAQHhAHMggIABAeEAcQBTIICAAQHhAHEAUyCAgAEB4QBxAFOgcIIxCwAxAnOgcIABBHELADOgoIABBHELADEMkDOggIABCSAxCwAzoSCC4QxwEQowIQyAMQsAMQQxgBOhIILhDHARDRAxDIAxCwAxBDGAFKBAhBGABKBAhGGABQlAZYlAZg0RVoAnABeACAAWiIAWiSAQMwLjGYAQCgAQHIAQzAAQHaAQQIARgI&sclient=gws-wiz'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36'}


def check_currency_usd():
    res = requests.get(url_usd, headers=headers)

    soup = BeautifulSoup(res.content, 'html.parser')

    convert = soup.findAll("span", {'class': 'SwHCTb', 'class': 'DFlfde', 'data-precision': 2})
    return convert[0].text


def check_currency_eur():
    res = requests.get(url_eur, headers=headers)

    soup = BeautifulSoup(res.content, 'html.parser')

    convert = soup.findAll("span", {'class': 'SwHCTb', 'class': 'DFlfde', 'data-precision': 2})
    return convert[0].text


