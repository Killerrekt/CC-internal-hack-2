from bs4 import BeautifulSoup
import requests

cont = requests.get("https://weather.com/en-IN/weather/today/l/43f285acfe034a76ec87901c46411256bad8d8d3e2882d36fb184297f2a13029")
soup = BeautifulSoup(cont.content,'html.parser')

temp = soup.find(class_ = "CurrentConditions--tempValue--MHmYY").text
feels = soup.find(class_ = "TodayDetailsCard--feelsLikeTempValue--2icPt").text
sunrise = soup.find_all(class_ = "SunriseSunset--dateValue--3H780")[0].text
sunset = soup.find_all(class_ = "SunriseSunset--dateValue--3H780")[1].text
chance = soup.find_all(class_ = "Column--precip--3JCDO")

print(temp, feels, sunrise, sunset, chance[9].text)