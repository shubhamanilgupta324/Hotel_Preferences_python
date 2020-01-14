import datetime
import bs4
from selenium import webdriver
import re
import time as t
from flask import Blueprint,request
from flask_cors import CORS
import json

blueprint = Blueprint('api', __name__)
CORS(blueprint)

# connecting through flask
@blueprint.route('/testing', methods=['POST'])
def test():
    jsonData = request.values["data"] # getting the json value from front end

    # start time of code
    start_time = datetime.datetime.now()

    # taking all the values in the variable
    user_json = json.loads(jsonData)
    checkinDate = user_json["c_in"]
    checkoutDate = user_json["c_out"]
    city_name = user_json["city"].lower()
    adults = user_json["adult"]
    child = user_json["child"]
    child_age = "2"

    # setting the driver path
    # Mehul was here also shubham is so gay
    chrome_path=r"C:\Users\Shubham\Downloads\chromedriver_win32\chromedriver"
    driver= webdriver.Chrome(chrome_path)

    # getting all the sites
    sites=["makemytrip","goibibo","yatra","cleartrip"]
    # sites=["makemytrip"]

    #  dictionary to save the minimum price for each hotel
    hotel_price={}
    hotel_price["The_Park_Navi_Mumbai-Navi_Mumbai"]=0
    hotel_price["residency hotel"] =0
    hotel_price["the resort"] = 0
    hotel_price["parle international"] = 0
    hotel_price["goldfinch hotel"] = 0
    hotel_price["sukh hotel"] = 0
    hotel_price["hotel le grande"] = 0
    hotel_price["hotel fortune"] = 0
    hotel_price["Annex Executive"] = 0
    hotel_price["Mango_Hotels_Navi_Mumbai_Airoli-Navi_Mumbai"] = 0
    hotel_price["Hotel_Manama-Mumbai"] = 0

    # to save the check in and check out time for each hotel
    c_in_c_out={}
    c_in_c_out["The_Park_Navi_Mumbai-Navi_Mumbai"]=[]
    c_in_c_out["residency hotel"] = []
    c_in_c_out["the resort"] = []
    c_in_c_out["parle international"] = []
    c_in_c_out["goldfinch hotel"] = []
    c_in_c_out["sukh hotel"] = []
    c_in_c_out["hotel le grande"] = []
    c_in_c_out["hotel fortune"] = []
    c_in_c_out["Annex Executive"] = []
    c_in_c_out["Mango_Hotels_Navi_Mumbai_Airoli-Navi_Mumbai"] = []
    c_in_c_out["Hotel_Manama-Mumbai"] = []

    # to save the facilities of each hotal
    h_facility={}
    h_facility["The_Park_Navi_Mumbai-Navi_Mumbai"]=[]
    h_facility["residency hotel"] = []
    h_facility["the resort"] = []
    h_facility["parle international"] = []
    h_facility["goldfinch hotel"] = []
    h_facility["sukh hotel"] = []
    h_facility["hotel le grande"] = []
    h_facility["hotel fortune"] = []
    h_facility["Annex Executive"] = []
    h_facility["Mango_Hotels_Navi_Mumbai_Airoli-Navi_Mumbai"] = []
    h_facility["Hotel_Manama-Mumbai"] = []

    # save the site name in which we are getting the lowest price
    h_name={}
    h_name["The_Park_Navi_Mumbai-Navi_Mumbai"]=""
    h_name["residency hotel"] = ""
    h_name["the resort"] = ""
    h_name["parle international"] = ""
    h_name["goldfinch hotel"] = ""
    h_name["sukh hotel"] = ""
    h_name["hotel le grande"] = ""
    h_name["hotel fortune"] = ""
    h_name["Annex Executive"] = ""
    h_name["Mango_Hotels_Navi_Mumbai_Airoli-Navi_Mumbai"] = ""
    h_name["Hotel_Manama-Mumbai"] = ""

    # city name
    city_name="mumbai"

    # all the hotels in the city
    city_hotel = {}
    city_hotel["mumbai"] = ["The_Park_Navi_Mumbai-Navi_Mumbai","the resort","parle international",
                            "goldfinch hotel","sukh hotel","hotel le grande",
                            "hotel fortune","Annex Executive","Mango_Hotels_Navi_Mumbai_Airoli-Navi_Mumbai","Hotel_Manama-Mumbai","residency hotel"]

    # MAKEMYTRIP
    def makemytrip(site,checkinDate,checkoutDate,h_facility):

        mmt_checkinDate_split = checkinDate.split("-")
        mmt_checkinDate = mmt_checkinDate_split[1] + mmt_checkinDate_split[2] + mmt_checkinDate_split[0]
        mmt_checkoutDate_split = checkoutDate.split("-")
        mmt_checkoutDate = mmt_checkoutDate_split[1] + mmt_checkoutDate_split[2] + mmt_checkoutDate_split[0]

        total_days = int(mmt_checkoutDate_split[2]) - int(mmt_checkinDate_split[2])

        from bs4 import BeautifulSoup
        from selenium import webdriver
        chrome_path = r"C:\Users\Shubham\Downloads\chromedriver_win32\chromedriver"
        driver = webdriver.Chrome(chrome_path)
        city_hotel = {}
        city_hotel["mumbai"] = ["residency hotel"]
        hotel_id = {}
        hotel_id["residency hotel"] = "201606151546012542"
        city_code_dict = {}
        city_code_dict["mumbai"] = "BOM"

        roomStayQualifier = adults + "e" + child + "e" + child_age + "e"
        # Finding Hotel Name Through the city name
        for hotel in city_hotel:
            if hotel == city_name:
                city_hotel_list = city_hotel[hotel]
        # Finding Hotel ID Through the hotel name
        for get_hotelID in city_hotel_list:
            hotelId = hotel_id[get_hotelID]

            url = "https://www.makemytrip.com/hotels/hotel-details/?checkin=" + mmt_checkinDate + "&checkout=" + mmt_checkoutDate + "&" \
            "country=IN&searchText=" + hotel + "%20Hotel&roomStayQualifier=" + roomStayQualifier + "&hotelId=" + hotelId

            try:
                main_page_data = driver.get(url)
                driver.set_window_position(-3000, 0)
                t.sleep(2)
                soup = BeautifulSoup(driver.page_source, "lxml")
                links = soup.find_all('div', {"": ""})
                for Residency_scrap1 in links:
                    links2 = Residency_scrap1.findAll("div", {"class": "miscellaneousGroup"})
                    if len(links2) != 0:
                        review2 = links2[0].find("ul", {"class": "facilityList2"}).find_all("li")  # Facilities Available
                        for j in review2:
                            rev=j.find_all("span")[1].text
                            h_facility[get_hotelID].append(rev)
            except:
                Exception = False
            try:
                for Residency_scrap3 in links:
                    links4 = Residency_scrap3.findAll("div", {"class": "_StandardRoom standardRoom"})
                    if len(links4) != 0:
                        disc2 = links4[0].find("p", {"class": "latoBlack font20 blueText"})  # Discounted_price
                        if hotel_price[get_hotelID] == 0:
                            hotel_price[get_hotelID] = int(disc2.text)
                            h_name[get_hotelID] = "www.makemytrip.com/"
                        else:
                            if hotel_price[get_hotelID] > int(disc2.text):
                                hotel_price[get_hotelID] = int(disc2.text)
                                h_name[get_hotelID] = "www.makemytrip.com/"
            except:
                Exception = False
        driver.quit()

        chrome_path = r"C:\Users\Shubham\Downloads\chromedriver_win32\chromedriver"
        driver = webdriver.Chrome(chrome_path)
        city_hotel = {}
        city_hotel["mumbai"] = ["Hotel_Manama-Mumbai"]
        hotel_id = {}
        hotel_id["Hotel_Manama-Mumbai"] = "200701101631373674"

        # Finding Hotel Name Through the city name
        for hotel in city_hotel:
            if hotel == city_name:
                city_hotel_list = city_hotel[hotel]
        # Finding Hotel ID Through the hotel name
        for get_hotelID in city_hotel_list:
            hotelId = hotel_id[get_hotelID]

            url = "https://www.makemytrip.com/hotels/hotel-details/?checkin=" + mmt_checkinDate + "&checkout=" + mmt_checkoutDate + "&" \
            "country=IN&searchText=" + hotel + "%20Hotel&roomStayQualifier=" + roomStayQualifier + "&hotelId=" + hotelId
            # print(url)
            try:
                main_page_data = driver.get(url)
                driver.set_window_position(-3000, 0)
                t.sleep(2)
                soup = BeautifulSoup(driver.page_source, "lxml")
                links = soup.find_all('div', {"": ""})
                for Residency_scrap1 in links:
                    links2 = Residency_scrap1.findAll("div", {"class": "miscellaneousGroup"})
                    if len(links2) != 0:
                        review2 = links2[0].find("ul", {"class": "facilityList2"}).find_all(
                            "li")  # Facilities Available
                        for j in review2:
                            rev = j.find_all("span")[1].text
                            h_facility[get_hotelID].append(rev)
            except:
                Exception = False
            try:
                for Residency_scrap3 in links:
                    links4 = Residency_scrap3.findAll("div", {"class": "_StandardRoom standardRoom"})
                    if len(links4) != 0:
                        disc2 = links4[0].find("p", {"class": "latoBlack font20 blueText"})  # Discounted_price
                        if hotel_price[get_hotelID] == 0:
                            hotel_price[get_hotelID] = int(disc2.text)
                            h_name[get_hotelID] = "www.makemytrip.com/"
                        else:
                            if hotel_price[get_hotelID] > int(disc2.text):
                                hotel_price[get_hotelID] = int(disc2.text)
                                h_name[get_hotelID] = "www.makemytrip.com/"
            except:
                Exception = False
        driver.quit()


        chrome_path = r"C:\Users\Shubham\Downloads\chromedriver_win32\chromedriver"
        driver = webdriver.Chrome(chrome_path)
        city_hotel = {}
        city_hotel["mumbai"] = ["Mango_Hotels_Navi_Mumbai_Airoli-Navi_Mumbai"]
        hotel_id = {}
        hotel_id["Mango_Hotels_Navi_Mumbai_Airoli-Navi_Mumbai"] = "201401241221502792"


        # Finding Hotel Name Through the city name
        for hotel in city_hotel:
            if hotel == city_name:
                city_hotel_list = city_hotel[hotel]
        # Finding Hotel ID Through the hotel name
        for get_hotelID in city_hotel_list:
            hotelId = hotel_id[get_hotelID]

            url = "https://www.makemytrip.com/hotels/hotel-details/?checkin=" + mmt_checkinDate + "&checkout=" + mmt_checkoutDate + "&" \
            "country=IN&searchText=" + hotel + "%20Hotel&roomStayQualifier=" + roomStayQualifier + "&hotelId=" + hotelId
            # print(url)
            try:
                main_page_data = driver.get(url)
                driver.set_window_position(-3000, 0)
                t.sleep(2)
                soup = BeautifulSoup(driver.page_source, "lxml")
                links = soup.find_all('div', {"": ""})
                for Residency_scrap1 in links:
                    links2 = Residency_scrap1.findAll("div", {"class": "miscellaneousGroup"})
                    if len(links2) != 0:
                        review2 = links2[0].find("ul", {"class": "facilityList2"}).find_all(
                            "li")  # Facilities Available
                        for j in review2:
                            rev = j.find_all("span")[1].text
                            h_facility[get_hotelID].append(rev)
            except:
                Exception = False
            try:
                for Residency_scrap3 in links:
                    links4 = Residency_scrap3.findAll("div", {"class": "_StandardRoom standardRoom"})
                    if len(links4) != 0:
                        disc2 = links4[0].find("p", {"class": "latoBlack font20 blueText"})  # Discounted_price
                        if hotel_price[get_hotelID] == 0:
                            hotel_price[get_hotelID] = int(disc2.text)
                            h_name[get_hotelID] = "www.makemytrip.com/"
                        else:
                            if hotel_price[get_hotelID] > int(disc2.text):
                                hotel_price[get_hotelID] = int(disc2.text)
                                h_name[get_hotelID] = "www.makemytrip.com/"
            except:
                Exception = False
        driver.quit()


        chrome_path = r"C:\Users\Shubham\Downloads\chromedriver_win32\chromedriver"
        driver = webdriver.Chrome(chrome_path)
        city_hotel = {}
        city_hotel["mumbai"] = ["hotel fortune"]
        hotel_id = {}
        hotel_id["hotel fortune"] = "200711051529003276"


        # Finding Hotel Name Through the city name
        for hotel in city_hotel:
            if hotel == city_name:
                city_hotel_list = city_hotel[hotel]
        # Finding Hotel ID Through the hotel name
        for get_hotelID in city_hotel_list:
            hotelId = hotel_id[get_hotelID]

            url = "https://www.makemytrip.com/hotels/hotel-details/?checkin=" + mmt_checkinDate + "&checkout=" + mmt_checkoutDate + "&" \
            "country=IN&searchText=" + hotel + "%20Hotel&roomStayQualifier=" + roomStayQualifier + "&hotelId=" + hotelId
            # print(url)
            try:
                main_page_data = driver.get(url)
                driver.set_window_position(-3000, 0)
                t.sleep(2)
                soup = BeautifulSoup(driver.page_source, "lxml")
                links = soup.find_all('div', {"": ""})
                for Residency_scrap1 in links:
                    links2 = Residency_scrap1.findAll("div", {"class": "miscellaneousGroup"})
                    if len(links2) != 0:
                        review2 = links2[0].find("ul", {"class": "facilityList2"}).find_all(
                            "li")  # Facilities Available
                        for j in review2:
                            rev = j.find_all("span")[1].text
                            h_facility[get_hotelID].append(rev)
            except:
                Exception = False
            try:
                for Residency_scrap3 in links:
                    links4 = Residency_scrap3.findAll("div", {"class": "_StandardRoom standardRoom"})
                    if len(links4) != 0:
                        disc2 = links4[0].find("p", {"class": "latoBlack font20 blueText"})  # Discounted_price
                        if hotel_price[get_hotelID] == 0:
                            hotel_price[get_hotelID] = int(disc2.text)
                            h_name[get_hotelID] = "www.makemytrip.com/"
                        else:
                            if hotel_price[get_hotelID] > int(disc2.text):
                                hotel_price[get_hotelID] = int(disc2.text)
                                h_name[get_hotelID] = "www.makemytrip.com/"
            except:
                Exception = False
        driver.quit()


        chrome_path = r"C:\Users\Shubham\Downloads\chromedriver_win32\chromedriver"
        driver = webdriver.Chrome(chrome_path)
        city_hotel = {}
        city_hotel["mumbai"] = ["hotel le grande"]
        hotel_id = {}
        hotel_id["hotel le grande"] = "20090509111906380"


        # Finding Hotel Name Through the city name
        for hotel in city_hotel:
            if hotel == city_name:
                city_hotel_list = city_hotel[hotel]
        # Finding Hotel ID Through the hotel name
        for get_hotelID in city_hotel_list:
            hotelId = hotel_id[get_hotelID]

            url = "https://www.makemytrip.com/hotels/hotel-details/?checkin=" + mmt_checkinDate + "&checkout=" + mmt_checkoutDate + "&" \
            "country=IN&searchText=" + hotel + "%20Hotel&roomStayQualifier=" + roomStayQualifier + "&hotelId=" + hotelId
            # print(url)
            try:
                main_page_data = driver.get(url)
                driver.set_window_position(-3000, 0)
                t.sleep(2)
                soup = BeautifulSoup(driver.page_source, "lxml")
                links = soup.find_all('div', {"": ""})
                for Residency_scrap1 in links:
                    links2 = Residency_scrap1.findAll("div", {"class": "miscellaneousGroup"})
                    if len(links2) != 0:
                        review2 = links2[0].find("ul", {"class": "facilityList2"}).find_all(
                            "li")  # Facilities Available
                        for j in review2:
                            rev = j.find_all("span")[1].text
                            h_facility[get_hotelID].append(rev)
            except:
                Exception = False
            try:
                for Residency_scrap3 in links:
                    links4 = Residency_scrap3.findAll("div", {"class": "_StandardRoom standardRoom"})
                    if len(links4) != 0:
                        disc2 = links4[0].find("p", {"class": "latoBlack font20 blueText"})  # Discounted_price
                        if hotel_price[get_hotelID] == 0:
                            hotel_price[get_hotelID] = int(disc2.text)
                            h_name[get_hotelID] = "www.makemytrip.com/"
                        else:
                            if hotel_price[get_hotelID] > int(disc2.text):
                                hotel_price[get_hotelID] = int(disc2.text)
                                h_name[get_hotelID] = "www.makemytrip.com/"
            except:
                Exception = False
        driver.quit()


        chrome_path = r"C:\Users\Shubham\Downloads\chromedriver_win32\chromedriver"
        driver = webdriver.Chrome(chrome_path)
        city_hotel = {}
        city_hotel["mumbai"] = ["sukh hotel"]
        hotel_id = {}
        hotel_id["sukh hotel"] = "200709241520434648"


        # Finding Hotel Name Through the city name
        for hotel in city_hotel:
            if hotel == city_name:
                city_hotel_list = city_hotel[hotel]
        # Finding Hotel ID Through the hotel name
        for get_hotelID in city_hotel_list:
            hotelId = hotel_id[get_hotelID]

            url = "https://www.makemytrip.com/hotels/hotel-details/?checkin=" + mmt_checkinDate + "&checkout=" + mmt_checkoutDate + "&" \
            "country=IN&searchText=" + hotel + "%20Hotel&roomStayQualifier=" + roomStayQualifier + "&hotelId=" + hotelId
            # print(url)
            try:
                main_page_data = driver.get(url)
                driver.set_window_position(-3000, 0)
                t.sleep(2)
                soup = BeautifulSoup(driver.page_source, "lxml")
                links = soup.find_all('div', {"": ""})
                for Residency_scrap1 in links:
                    links2 = Residency_scrap1.findAll("div", {"class": "miscellaneousGroup"})
                    if len(links2) != 0:
                        review2 = links2[0].find("ul", {"class": "facilityList2"}).find_all(
                            "li")  # Facilities Available
                        for j in review2:
                            rev = j.find_all("span")[1].text
                            h_facility[get_hotelID].append(rev)
            except:
                Exception = False
            try:
                for Residency_scrap3 in links:
                    links4 = Residency_scrap3.findAll("div", {"class": "_StandardRoom standardRoom"})
                    if len(links4) != 0:
                        disc2 = links4[0].find("p", {"class": "latoBlack font20 blueText"})  # Discounted_price
                        if hotel_price[get_hotelID] == 0:
                            hotel_price[get_hotelID] = int(disc2.text)
                            h_name[get_hotelID] = "www.makemytrip.com/"
                        else:
                            if hotel_price[get_hotelID] > int(disc2.text):
                                hotel_price[get_hotelID] = int(disc2.text)
                                h_name[get_hotelID] = "www.makemytrip.com/"
            except:
                Exception = False
        driver.quit()

        chrome_path = r"C:\Users\Shubham\Downloads\chromedriver_win32\chromedriver"
        driver = webdriver.Chrome(chrome_path)
        city_hotel = {}
        city_hotel["mumbai"] = ["goldfinch hotel"]
        hotel_id = {}
        hotel_id["goldfinch hotel"] = "201301061913516287"

        # Finding Hotel Name Through the city name
        for hotel in city_hotel:
            if hotel == city_name:
                city_hotel_list = city_hotel[hotel]
        # Finding Hotel ID Through the hotel name
        for get_hotelID in city_hotel_list:
            hotelId = hotel_id[get_hotelID]

            url = "https://www.makemytrip.com/hotels/hotel-details/?checkin=" + mmt_checkinDate + "&checkout=" + mmt_checkoutDate + "&" \
            "country=IN&searchText=" + hotel + "%20Hotel&roomStayQualifier=" + roomStayQualifier + "&hotelId=" + hotelId
            # print(url)
            try:
                main_page_data = driver.get(url)
                driver.set_window_position(-3000, 0)
                t.sleep(2)
                soup = BeautifulSoup(driver.page_source, "lxml")
                links = soup.find_all('div', {"": ""})
                for Residency_scrap1 in links:
                    links2 = Residency_scrap1.findAll("div", {"class": "miscellaneousGroup"})
                    if len(links2) != 0:
                        review2 = links2[0].find("ul", {"class": "facilityList2"}).find_all("li")  # Facilities Available
                        for j in review2:
                            rev = j.find_all("span")[1].text
                            h_facility[get_hotelID].append(rev)
            except:
                Exception = False
            try:
                for Residency_scrap3 in links:
                    links4 = Residency_scrap3.findAll("div", {"class": "_StandardRoom standardRoom"})
                    if len(links4) != 0:
                        disc2 = links4[0].find("p", {"class": "latoBlack font20 blueText"})  # Discounted_price
                        if hotel_price[get_hotelID] == 0:
                            hotel_price[get_hotelID] = int(disc2.text)
                            h_name[get_hotelID] = "www.makemytrip.com/"
                        else:
                            if hotel_price[get_hotelID] > int(disc2.text):
                                hotel_price[get_hotelID] = int(disc2.text)
                                h_name[get_hotelID] = "www.makemytrip.com/"
            except:
                Exception = False
        driver.quit()

        chrome_path = r"C:\Users\Shubham\Downloads\chromedriver_win32\chromedriver"
        driver = webdriver.Chrome(chrome_path)
        city_hotel = {}
        city_hotel["mumbai"] = ["parle international"]
        hotel_id = {}
        hotel_id["parle international"] = "200703161231099195"

        # Finding Hotel Name Through the city name
        for hotel in city_hotel:
            if hotel == city_name:
                city_hotel_list = city_hotel[hotel]
        # Finding Hotel ID Through the hotel name
        for get_hotelID in city_hotel_list:
            hotelId = hotel_id[get_hotelID]

            url = "https://www.makemytrip.com/hotels/hotel-details/?checkin=" + mmt_checkinDate + "&checkout=" + mmt_checkoutDate + "&" \
            "country=IN&searchText=" + hotel + "%20Hotel&roomStayQualifier=" + roomStayQualifier + "&hotelId=" + hotelId
            # print(url)
            try:
                main_page_data = driver.get(url)
                driver.set_window_position(-3000, 0)
                t.sleep(2)
                soup = BeautifulSoup(driver.page_source, "lxml")
                links = soup.find_all('div', {"": ""})
                for Residency_scrap1 in links:
                    links2 = Residency_scrap1.findAll("div", {"class": "miscellaneousGroup"})
                    if len(links2) != 0:
                        review2 = links2[0].find("ul", {"class": "facilityList2"}).find_all("li")  # Facilities Available
                        for j in review2:
                            rev = j.find_all("span")[1].text
                            h_facility[get_hotelID].append(rev)
            except:
                Exception = False
            try:
                for Residency_scrap3 in links:
                    links4 = Residency_scrap3.findAll("div", {"class": "_StandardRoom standardRoom"})
                    if len(links4) != 0:
                        disc2 = links4[0].find("p", {"class": "latoBlack font20 blueText"})  # Discounted_price
                        if hotel_price[get_hotelID] == 0:
                            hotel_price[get_hotelID] = int(disc2.text)
                            h_name[get_hotelID] = "www.makemytrip.com/"
                        else:
                            if hotel_price[get_hotelID] > int(disc2.text):
                                hotel_price[get_hotelID] = int(disc2.text)
                                h_name[get_hotelID] = "www.makemytrip.com/"
            except:
                Exception = False
        driver.quit()


        chrome_path = r"C:\Users\Shubham\Downloads\chromedriver_win32\chromedriver"
        driver = webdriver.Chrome(chrome_path)
        city_hotel = {}
        city_hotel["mumbai"] = ["the resort"]
        hotel_id = {}
        hotel_id["the resort"] = "200707250953377576"

        # Finding Hotel Name Through the city name
        for hotel in city_hotel:
            if hotel == city_name:
                city_hotel_list = city_hotel[hotel]
        # Finding Hotel ID Through the hotel name
        for get_hotelID in city_hotel_list:
            hotelId = hotel_id[get_hotelID]

            url = "https://www.makemytrip.com/hotels/hotel-details/?checkin=" + mmt_checkinDate + "&checkout=" + mmt_checkoutDate + "&" \
            "country=IN&searchText=" + hotel + "%20Hotel&roomStayQualifier=" + roomStayQualifier + "&hotelId=" + hotelId
            # print(url)
            try:
                main_page_data = driver.get(url)
                driver.set_window_position(-3000, 0)
                t.sleep(2)
                soup = BeautifulSoup(driver.page_source, "lxml")
                links = soup.find_all('div', {"": ""})
                for Residency_scrap1 in links:
                    links2 = Residency_scrap1.findAll("div", {"class": "miscellaneousGroup"})
                    if len(links2) != 0:
                        review2 = links2[0].find("ul", {"class": "facilityList2"}).find_all("li")  # Facilities Available
                        for j in review2:
                            rev = j.find_all("span")[1].text
                            h_facility[get_hotelID].append(rev)
            except:
                Exception = False
            try:
                for Residency_scrap3 in links:
                    links4 = Residency_scrap3.findAll("div", {"class": "_StandardRoom standardRoom"})
                    if len(links4) != 0:
                        disc2 = links4[0].find("p", {"class": "latoBlack font20 blueText"})  # Discounted_price
                        if hotel_price[get_hotelID] == 0:
                            hotel_price[get_hotelID] = int(disc2.text)
                            h_name[get_hotelID] = "www.makemytrip.com/"
                        else:
                            if hotel_price[get_hotelID] > int(disc2.text):
                                hotel_price[get_hotelID] = int(disc2.text)
                                h_name[get_hotelID] = "www.makemytrip.com/"
            except:
                Exception = False
        driver.quit()

        chrome_path = r"C:\Users\Shubham\Downloads\chromedriver_win32\chromedriver"
        driver = webdriver.Chrome(chrome_path)
        city_hotel = {}
        city_hotel["mumbai"] = ["The_Park_Navi_Mumbai-Navi_Mumbai"]
        hotel_id = {}
        hotel_id["The_Park_Navi_Mumbai-Navi_Mumbai"] = "200704121637479279"

        # Finding Hotel Name Through the city name
        for hotel in city_hotel:
            if hotel == city_name:
                city_hotel_list = city_hotel[hotel]
        # Finding Hotel ID Through the hotel name
        for get_hotelID in city_hotel_list:
            hotelId = hotel_id[get_hotelID]

            url = "https://www.makemytrip.com/hotels/hotel-details/?checkin=" + mmt_checkinDate + "&checkout=" + mmt_checkoutDate + "&" \
            "country=IN&searchText=" + hotel + "%20Hotel&roomStayQualifier=" + roomStayQualifier + "&hotelId=" + hotelId
            # print(url)
            try:
                main_page_data = driver.get(url)
                driver.set_window_position(-3000, 0)
                t.sleep(2)
                soup = BeautifulSoup(driver.page_source, "lxml")
                links = soup.find_all('div', {"": ""})
                for Residency_scrap1 in links:
                    links2 = Residency_scrap1.findAll("div", {"class": "miscellaneousGroup"})
                    if len(links2) != 0:
                        review2 = links2[0].find("ul", {"class": "facilityList2"}).find_all("li")  # Facilities Available
                        for j in review2:
                            rev = j.find_all("span")[1].text
                            h_facility[get_hotelID].append(rev)
            except:
                Exception = False
            try:
                for Residency_scrap3 in links:
                    links4 = Residency_scrap3.findAll("div", {"class": "_StandardRoom standardRoom"})
                    if len(links4) != 0:
                        disc2 = links4[0].find("p", {"class": "latoBlack font20 blueText"})  # Discounted_price
                        if hotel_price[get_hotelID] == 0:
                            hotel_price[get_hotelID] = int(disc2.text)
                            h_name[get_hotelID] = "www.makemytrip.com/"
                        else:
                            if hotel_price[get_hotelID] > int(disc2.text):
                                hotel_price[get_hotelID] = int(disc2.text)
                                h_name[get_hotelID] = "www.makemytrip.com/"
            except:
                Exception = False
        driver.quit()


        chrome_path = r"C:\Users\Shubham\Downloads\chromedriver_win32\chromedriver"
        driver = webdriver.Chrome(chrome_path)
        city_hotel = {}
        city_hotel["mumbai"] = ["Annex Executive"]
        hotel_id = {}
        hotel_id["Annex Executive"] = "201602021438236409"

        # Finding Hotel Name Through the city name
        for hotel in city_hotel:
            if hotel == city_name:
                city_hotel_list = city_hotel[hotel]
        # Finding Hotel ID Through the hotel name
        for get_hotelID in city_hotel_list:
            hotelId = hotel_id[get_hotelID]

            url = "https://www.makemytrip.com/hotels/hotel-details/?checkin=" + mmt_checkinDate + "&checkout=" + mmt_checkoutDate + "&" \
            "country=IN&searchText=" + hotel + "%20Hotel&roomStayQualifier=" + roomStayQualifier + "&hotelId=" + hotelId
            # print(url)
            try:
                main_page_data = driver.get(url)
                driver.set_window_position(-3000, 0)
                t.sleep(2)
                soup = BeautifulSoup(driver.page_source, "lxml")
                links = soup.find_all('div', {"": ""})
                for Residency_scrap1 in links:
                    links2 = Residency_scrap1.findAll("div", {"class": "miscellaneousGroup"})
                    if len(links2) != 0:
                        review2 = links2[0].find("ul", {"class": "facilityList2"}).find_all("li")  # Facilities Available
                        for j in review2:
                            rev = j.find_all("span")[1].text
                            h_facility[get_hotelID].append(rev)
            except:
                Exception = False
            try:
                for Residency_scrap3 in links:
                    links4 = Residency_scrap3.findAll("div", {"class": "_StandardRoom standardRoom"})
                    if len(links4) != 0:
                        disc2 = links4[0].find("p", {"class": "latoBlack font20 blueText"})  # Discounted_price
                        if hotel_price[get_hotelID] == 0:
                            hotel_price[get_hotelID] = int(disc2.text)
                            h_name[get_hotelID] = "www.makemytrip.com/"
                        else:
                            if hotel_price[get_hotelID] > int(disc2.text):
                                hotel_price[get_hotelID] = int(disc2.text)
                                h_name[get_hotelID] = "www.makemytrip.com/"
            except:
                Exception = False
        driver.quit()

    # GOIBIBO
    def goibibo(site,checkinDate,checkoutDate):

        # format the date
        go_checkinDate_split = checkinDate.split("-")
        go_checkinDate = go_checkinDate_split[0]  + go_checkinDate_split[1]  + go_checkinDate_split[2]
        go_checkoutDate_split = checkoutDate.split("-")
        go_checkoutDate = go_checkoutDate_split[0] + go_checkoutDate_split[1]  + go_checkoutDate_split[2]

        total_days = int(go_checkoutDate_split[2]) - int(go_checkinDate_split[2])

        roomStayQualifier = adults + "-" + child + "-" + child_age

        # hotel ids for url
        hotel_id = {}
        hotel_id["The_Park_Navi_Mumbai-Navi_Mumbai"] = "6571195111223029170"
        hotel_id["residency hotel"] = "3614109768092723331"
        hotel_id["the resort"] = "2362912313949093326"
        hotel_id["parle international"] = "5773950970688245045"
        hotel_id["goldfinch hotel"] = "3284505915249380043"
        hotel_id["sukh hotel"] = "4768950949133964669"
        hotel_id["hotel le grande"] = "3488104441006598328"
        hotel_id["hotel fortune"] = "6203860387500170863"
        hotel_id["Annex Executive"] = "4492873573747394964"
        hotel_id["Mango_Hotels_Navi_Mumbai_Airoli-Navi_Mumbai"] = "4905261939687894411"
        hotel_id["Hotel_Manama-Mumbai"] = "6389032922002493377"

        # hotel name for url
        hotel_name = {}
        hotel_name["The_Park_Navi_Mumbai-Navi_Mumbai"] = "the park"
        hotel_name["residency hotel"] = "Residency"
        hotel_name["the resort"] = "The Resort"
        hotel_name["parle international"] = "Parle International"
        hotel_name["goldfinch hotel"] = "goldfinch hotel"
        hotel_name["sukh hotel"] = "sukh hotel"
        hotel_name["hotel le grande"] = "Hotel Le Grande"
        hotel_name["hotel fortune"] = "Hotel Fortune"
        hotel_name["Annex Executive"] = "Hotel Annex Executive"
        hotel_name["Mango_Hotels_Navi_Mumbai_Airoli-Navi_Mumbai"] = "Mango Hotels Airoli"
        hotel_name["Hotel_Manama-Mumbai"] = "Manama Hotel"

        # loop through all the hotels
        for get_hotelID in city_hotel["mumbai"]:
            hotelName=hotel_name[get_hotelID]
            hotelId = hotel_id[get_hotelID]

            gbb_url = "https://www.goibibo.com/hotels/" + hotelName + "-" + hotelId + '/?hquery=%7B"ci"%3A"' + go_checkinDate + '"%2C"co"%3A"' + go_checkoutDate + '"%2C"r"%3A"'+roomStayQualifier+'"%2C"ibp"%3A"na"%2C"ts"%3A1%7D'''

            try:
                driver.get(gbb_url)
                driver.set_window_position(-3000, 0)
                soup = bs4.BeautifulSoup(driver.page_source, 'html.parser')
                Reduced_price = soup.findAll('span', {'class': 'ico32 greyDr fl'})
                # get the all reduced price
                for i in Reduced_price:
                    current_hotel_price = re.findall("([0-9]*)", i.text) # getting price from string
                    for j in current_hotel_price:
                        if j != "":
                            current_hotel_price = int(j)
                            break
                    # comparing the price
                    if hotel_price[get_hotelID] == 0:
                        hotel_price[get_hotelID] = current_hotel_price
                        h_name[get_hotelID] = "www.goibibo.com/"
                    else:
                        if hotel_price[get_hotelID] > current_hotel_price:
                            hotel_price[get_hotelID] = current_hotel_price
                            h_name[get_hotelID] = "www.goibibo.com/"
            except:
                exception = False

    # YATRA
    def yatra(site,checkinDate,checkoutDate):


        hotel_id = {}
        hotel_id["The_Park_Navi_Mumbai-Navi_Mumbai"] = "00002436"
        hotel_id["residency hotel"] = "00002546"
        hotel_id["the resort"] = "00001042"
        hotel_id["parle international"] = "00000349"
        hotel_id["goldfinch hotel"] = "00009838"
        hotel_id["sukh hotel"] = "00002687"
        hotel_id["hotel le grande"] = "00002742"
        hotel_id["hotel fortune"] = "00001333"
        hotel_id["Annex Executive"] = "00084405"
        hotel_id["Mango_Hotels_Navi_Mumbai_Airoli-Navi_Mumbai"] = "00017572"
        hotel_id["Hotel_Manama-Mumbai"] = "00001525"

        yatra_checkinDate_split=checkinDate.split("-")
        yatra_checkinDate=yatra_checkinDate_split[2]+"/"+yatra_checkinDate_split[1]+"/"+yatra_checkinDate_split[0]
        yatra_checkoutDate_split = checkoutDate.split("-")
        yatra_checkoutDate = yatra_checkoutDate_split[2] + "/" + yatra_checkoutDate_split[1] + "/" + yatra_checkoutDate_split[0]

        total_days = int(yatra_checkoutDate_split[2]) - int(yatra_checkinDate_split[2])

        for hotel,hotel_Id in hotel_id.items():

            # y_url = "https://hotel.yatra.com/hotel-search/dom/details?checkoutDate=" + yatra_checkoutDate + "&checkinDate=" + yatra_checkinDate + "&roomRequests%5B0%5D.id=1&roomRequests%5B0%5D.noOfAdults=2&roomRequests%5B0%5D.noOfChildren=1&roomRequests%5B0%5D.childrenAge%5B0%5D=0&source=BOOKING_ENGINE&pg=1&tenant=B2C&city.name="+hotel_code+"&city.code="+hotel_code+"&country.name=India&country.code=IND&hotelId="+hotel_Id

            y_url="https://hotel.yatra.com/hotel-search/dom/details?checkinDate="+yatra_checkinDate+"&" \
                  "checkoutDate="+yatra_checkoutDate+"&roomRequests%5B0%5D.id=1&roomRequests%5B0%5D.noOfAdults=1&" \
                  "roomRequests%5B0%5D.noOfChildren=0&source=BOOKING_ENGINE&tenant=B2C&" \
                  "hotelID="+hotel_Id+"&pg=1&htlFindMthd=booking%20engine:seo"

            # print(y_url)
            #     # storing the site to a driver
            try:
                driver.get(y_url)
                driver.set_window_position(-3000, 0)
                t.sleep(3)
                # extracting the price from p tag
                soup = bs4.BeautifulSoup(driver.page_source, 'html.parser')
                price = soup.findAll('p', {'class': 'full fm-lb fs-28 ng-binding'})
                # check so that price is not printed twice
                lst = []
                for i in price:
                    if i not in lst:
                        lst.append(i)
                        # print(i.text)
                        current_hotel_price = re.findall("([0-9]*[,][0-9]*)", i.text)
                        current_hotel_price = int((int(current_hotel_price[0].replace(",", "")))/total_days)
                        if hotel_price[hotel] == 0:
                            hotel_price[hotel]=current_hotel_price
                            h_name[hotel] = "www.yatra.com/"
                        else:
                            if hotel_price[hotel] > current_hotel_price:
                                hotel_price[hotel] = current_hotel_price
                                h_name[hotel] = "www.yatra.com/"
            except:
                exception = False

            try:
                # for checkin and out time
                checkin_out_time = soup.findAll('li', {'ng-if': 'htlInfo.checkIn && htlInfo.checkOut'})
                for i in checkin_out_time:
                    c_in_c_out[hotel].append(i.text)
                    # print(i.text)
            except:
                exception = False

    # CLEARTRIP
    def cleartrip(site,checkinDate,checkoutDate):


        hotel_id = {}
        hotel_id["The_Park_Navi_Mumbai-Navi_Mumbai"] = "41931"
        hotel_id["residency hotel"] = "0724751"
        hotel_id["the resort"] = "40988"
        hotel_id["parle international"] = "40993"
        hotel_id["goldfinch hotel"] = "423311"
        hotel_id["sukh hotel"] = "79328"
        hotel_id["hotel le grande"] = "160484"
        hotel_id["hotel fortune"] = "41914"
        hotel_id["Annex Executive"] = "1349760"
        hotel_id["Mango_Hotels_Navi_Mumbai_Airoli-Navi_Mumbai"] = "716644"
        hotel_id["Hotel_Manama-Mumbai"] = "41033"

        yatra_checkinDate_split = checkinDate.split("-")
        yatra_checkinDate = yatra_checkinDate_split[2] + yatra_checkinDate_split[1] + yatra_checkinDate_split[0][-2:]
        yatra_checkoutDate_split = checkoutDate.split("-")
        yatra_checkoutDate = yatra_checkoutDate_split[2] + yatra_checkoutDate_split[1] + yatra_checkoutDate_split[0][-2:]

        total_days=int(yatra_checkoutDate_split[2])-int(yatra_checkinDate_split[2])
        for hotel, hotel_Id in hotel_id.items():

            ct_url = "https://www.cleartrip.com/hotels/details/"+hotel_Id+"?c="+yatra_checkinDate+"|"+yatra_checkoutDate+"&r=2,0&shwb=true&compId=#"
            # print(ct_url)
            try:
                driver.get(ct_url)
                driver.set_window_position(-3000, 0)
                t.sleep(2)
                soup = bs4.BeautifulSoup(driver.page_source, 'html.parser')
                price = soup.findAll('b', {'id': 'b-min-price'})
                lst = []
                for i in price:
                    if i not in lst:
                        lst.append(i)
                        current_hotel_price = re.findall("([0-9]*[,][0-9]*)", i.text)
                        current_hotel_price=int((int(current_hotel_price[0].replace(",", "")))/total_days)
                        # current_hotel_price = hotel_price[hotel]
                        if hotel_price[hotel] == 0:
                            hotel_price[hotel] = current_hotel_price
                            h_name[hotel] ="https://hotel.yatra.com/"
                        else:
                            if hotel_price[hotel] > current_hotel_price:
                                hotel_price[hotel] = current_hotel_price
                                h_name[hotel] = "https://hotel.yatra.com/"
            except:
                exception = False

    # Lopping through all the sites
    for site in sites:
        if site == "makemytrip":
            makemytrip(site,checkinDate,checkoutDate,h_facility)
        if site == "goibibo":
            goibibo(site,checkinDate,checkoutDate)
        if site == "yatra":
            yatra(site,checkinDate,checkoutDate)
        if site == "cleartrip":
            cleartrip(site,checkinDate,checkoutDate)

    # getting the text and star rating for each hotel
    rating_data={}
    import sqlite3
    con=sqlite3.connect("hotel.db")
    cur = con.cursor()
    rows = cur.execute("select * from hotelDetails")
    for row in rows:
        rating_data[row[1]]=[row[3],row[4]]
    complete_data=[]
    count=0


    # common dummy facilities if any exception while scraping
    dummy_facility=["Housekeeping","Room Service","Power Backup","Room Controlled Air Conditioning","Attached Bathroom","levator Lift","Wi-Fi"]

    for hotel_val in city_hotel["mumbai"]:
        h_price_val = hotel_price[hotel_val]
        h_c_in_c_out_val = c_in_c_out[hotel_val]
        # common dummy checkin and checkout time if any exception while scraping
        h_c_in_val = "CHECKIN : 12:00 PM"
        h_c_out_val = "CHECKOUT : 10:00 AM"
        if(len(h_c_in_c_out_val) == 2):
            h_c_in_val=h_c_in_c_out_val[0]
            h_c_out_val=h_c_in_c_out_val[1]
        if len(h_facility[hotel_val]) == 0:
            h_facility_val =dummy_facility
        else:
            h_facility_val = h_facility[hotel_val]
        h_name_val = h_name[hotel_val]
        h_rating=rating_data[hotel_val]
        h_text_rating_val =h_rating[1]
        h_star_rating_val =h_rating[0]

        # updating the value in database
        cur.execute("update hotelDetails set h_price =? , h_site =? where h_name =?",(str(h_price_val) ,h_name_val,hotel_val))
        # creating the json for front end
        hotel_name=hotel_val.replace("-"," ").replace("_Navi_Mumbai","").replace("_"," ").replace("Navi Mumbai","").strip().upper()
        data_={'h_site':h_name_val,'h_name':hotel_name,'star_rating':h_star_rating_val,'text_rating':h_text_rating_val,'price':str(h_price_val),'checkIn':h_c_in_val,'CheckOut':h_c_out_val,'facility':h_facility_val}
        # appending json for each hotel in complete_data
        complete_data.append(data_)
        count=count+1

    con.close()


    end_time = datetime.datetime.now()
    total_time = end_time - start_time
    print(total_time)

    # returning the json back to front end
    return json.dumps({"success":complete_data})


