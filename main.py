import csv
import math
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from tkinter import *
from bs4 import BeautifulSoup
import re
from geopy.geocoders import Nominatim
geo_local = Nominatim(user_agent='South Korea')

dp = Tk()
main_frame = Frame(dp)
dp.geometry('500x150')
dp.title('near police')
main_frame.pack()

driver = webdriver.Chrome("es\chromedriver")
wait = WebDriverWait(driver, 30)
url = "https://www.dabangapp.com/"
driver.get(url)

def calculate_distance(lat1, lon1, lat2, lon2):
    # Convert coordinates to radians
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    distance = 6371000 * c  # Radius of the Earth in kilometers
    return distance


def find_nearest_police_station(user_lat, user_lon):
    nearest_station = None
    min_distance = float('inf')  # Initialize with infinity

    with open('changeANSI.csv', 'r', encoding='cp949') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row

        for row in reader:
            address, lat, lon = row[2], float(row[3]), float(row[4])
            distance = calculate_distance(user_lat, user_lon, lat, lon)
            if distance < min_distance:
                min_distance = distance
                nearest_station = (address, distance)

    return nearest_station


def geocoding(address):
    try:
        geo = geo_local.geocode(address)
        x_y = [geo.latitude, geo.longitude]
        return x_y

    except:
        return [0,0]

def get_loc():
    driver.switch_to.window(driver.window_handles[1])
    address = "none"
    html = driver.page_source # 페이지의 elements모두 가져오기
    soup = BeautifulSoup(html, 'html.parser') # BeautifulSoup사용하기
    address = soup.find_all('div', attrs={"class": "styled__NewAddress-sc-8pfhii-4 diajmd"})
    addr = address[0].get_text()
    addr = re.sub("도로명", "", addr)
    my_lat = geocoding(addr)[0]
    my_log = geocoding(addr)[1]
    nearest_police_station, distance = find_nearest_police_station(my_lat, my_log)
    distance = round(distance)
    #out = "가장 가까운 경찰서는 " + nearest_police_station + "이고 거리는" + str(distance) + "m 떨어져 있습니다."
    print("Nearest police station:", nearest_police_station)
    print("Distance : ", distance, "m")
    out = "가장 가까운 경찰서는 " + nearest_police_station + "이고 거리는" + str(distance) + "m 떨어져 있습니다."
    print(out)
    out_label.config(text=out)
    

find_button = Button(main_frame, text="찾기", command=get_loc, height=2)
find_button.grid(row=2, column=1)
info_label = Label(main_frame, text="찾기 버튼을 눌러주세요." ,height=2)
info_label.grid(row=13, column=1)
out_label = Label(main_frame, height=2)
out_label.grid(row=14, column=1)
exp_label = Label(main_frame, text="All Rights Reserved. Designed by Donggeon Jo",height=2)
exp_label.grid(row=16, column=1)

dp.mainloop()