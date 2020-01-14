from bs4 import BeautifulSoup
from selenium import webdriver
import re
from datetime import date, timedelta
import time as t
import sqlite3

# create database to save the rating and hotel details
con=sqlite3.connect("hotel.db")
cur=con.cursor()
# if table exist drop table and create(creating the table everytime we are finding sentiment from scrap)
cur.execute("drop table if exists hotelDetails")
# add columns to the table
cur.execute("CREATE TABLE hotelDetails(id INTEGER PRIMARY KEY AUTOINCREMENT,h_name varchar(50),h_price varchar(50),h_text_rating varchar(50),h_star_rating varchar(50),h_site varchar(50))")
# rows=cur.execute("select * from hotelDetails")
# for row in rows:
#     print(row)
# con.commit()
con.close()


# getting checkin and checkout time for the url (getting random )
# checkIn date
checkInDate = date.today() + timedelta(15)
sp_checkInDate=str(checkInDate).split("-")
checkInDate =sp_checkInDate[2]+"/"+sp_checkInDate[1]+"/"+sp_checkInDate[0]
# checkOut date
checkOutDate = date.today() + timedelta(18)
sp_checkOutDate =str(checkOutDate).split("-")
checkOutDate =sp_checkOutDate[2]+"/"+sp_checkOutDate[1]+"/"+sp_checkOutDate[0]


# setting the driver path
chrome_path=r"C:\Users\Shubham\Downloads\chromedriver_win32\chromedriver"
driver= webdriver.Chrome(chrome_path)

# site through which we will loop
# sites=["makemytrip"]
sites=["makemytrip","goibibo","yatra"]


# saving all the text rating of the hotel in total
saving_hotel_text_review={}
saving_hotel_text_review["The_Park_Navi_Mumbai-Navi_Mumbai"]=[]
saving_hotel_text_review["residency hotel"] = []
saving_hotel_text_review["the resort"] = []
saving_hotel_text_review["parle international"] = []
saving_hotel_text_review["goldfinch hotel"] = []
saving_hotel_text_review["sukh hotel"] = []
saving_hotel_text_review["hotel le grande"] = []
saving_hotel_text_review["hotel fortune"] = []
saving_hotel_text_review["Annex Executive"] = []
saving_hotel_text_review["Mango_Hotels_Navi_Mumbai_Airoli-Navi_Mumbai"] = []
saving_hotel_text_review["Hotel_Manama-Mumbai"] = []


# saving all the star rating of the hotel in total
saving_hotel_star_review={}
saving_hotel_star_review["The_Park_Navi_Mumbai-Navi_Mumbai"]=[]
saving_hotel_star_review["residency hotel"] = []
saving_hotel_star_review["the resort"] = []
saving_hotel_star_review["parle international"] = []
saving_hotel_star_review["goldfinch hotel"] = []
saving_hotel_star_review["sukh hotel"] = []
saving_hotel_star_review["hotel le grande"] = []
saving_hotel_star_review["hotel fortune"] = []
saving_hotel_star_review["Annex Executive"] = []
saving_hotel_star_review["Mango_Hotels_Navi_Mumbai_Airoli-Navi_Mumbai"] = []
saving_hotel_star_review["Hotel_Manama-Mumbai"] = []

city_name="mumbai"

# hotel name w.r.t to site
city_hotel = {}
city_hotel["mumbai"] = ["The_Park_Navi_Mumbai-Navi_Mumbai","residency hotel","the resort","parle international",
                        "goldfinch hotel","sukh hotel","hotel le grande",
                        "hotel fortune","Annex Executive","Mango_Hotels_Navi_Mumbai_Airoli-Navi_Mumbai","Hotel_Manama-Mumbai"]



# single loop makemytrip code
# def makemytrip(siteName):
#
#     hotel_id = {}
#     hotel_id["The_Park_Navi_Mumbai-Navi_Mumbai"] = "200704121637479279"
#     hotel_id["residency hotel"] = "201606151546012542"
#     hotel_id["the resort"] = "200707250953377576"
#     hotel_id["parle international"] = "200703161231099195"
#     hotel_id["goldfinch hotel"] = "201301061913516287"
#     hotel_id["sukh hotel"] = "200709241520434648"
#     hotel_id["hotel le grande"] = "20090509111906380"
#     hotel_id["hotel fortune"] = "200711051529003276"
#     hotel_id["Annex Executive"] = "201602021438236409"
#     hotel_id["Mango_Hotels_Navi_Mumbai_Airoli-Navi_Mumbai"] = "201401241221502792"
#     hotel_id["Hotel_Manama-Mumbai"] = "200701101631373674"
#
#     city_code_dict = {}
#     city_code_dict["mumbai"] = "BOM"
#
#     checkinDate = "06282019"
#     checkoutDate = "06292019"
#     city_name = "mumbai"
#     adults = "2"
#     child = "0"
#     child_age = "2"
#     city_code = ""
#     roomStayQualifier=adults+"e"+child+"e"+child_age+"e"
#
#     for hotel in city_hotel:
#         if hotel == city_name:
#             city_hotel_list = city_hotel[hotel]
#
#     # Finding City Code
#     for cty_name in city_code_dict:
#         if cty_name == city_name:
#             city_code = city_code_dict[cty_name]
#
#     # Finding Hotel ID Through the hotel name
#     for get_hotelID in city_hotel_list:
#         hotelId = hotel_id[get_hotelID]
#         chrome_path = r"C:\Users\Shubham\Downloads\chromedriver_win32\chromedriver"
#         driver = webdriver.Chrome(chrome_path)
#
#         url = "https://www.makemytrip.com/hotels/hotel-details/?checkin=" + checkinDate + "&checkout=" + checkoutDate + "&" \
#                                                                                                                         "city=" + city_code + "&country=IN&searchText=" + hotel + "%20Hotel&roomStayQualifier=" + roomStayQualifier + "&hotelId=" + hotelId
#         # url = "https://www.makemytrip.com/hotels/residency_hotel-details-mumbai.html"
#         print(url)
#         main_page_data = driver.get(url)
#         driver.set_window_position(-3000, 0)
#         # loop through all the review pages
#         nextPage = True
#         nextPageCount = 0
#         # loop till end
#         while (nextPage == True):
#             exception = True
#             try:
#                 nextPageCount = nextPageCount + 1  # counting pages
#                 soup = BeautifulSoup(driver.page_source, "lxml")
#                 links1 = soup.find('ul', {"class": "pagination"})  # getting the navigation bar
#                 li = links1.find_all("li")  # getting the navigation button
#                 for i in reversed(li):  # checking the navigation from behind
#                     x = i.get("class")  # get the class name
#                     if (x == ["disabled"]):  # to check if we are on last page
#                         nextPage = False  # if we are on last page end loop
#                         break
#                     break
#                 if (nextPage == False):
#                     break
#                 # press the next page button
#                 if (nextPageCount != 1):
#                     page = str(nextPageCount)
#                     driver.find_element_by_xpath(u'//a[text()="' + page + '"]').click()
#                 soup = BeautifulSoup(driver.page_source, "lxml")
#                 links = soup.find_all('div', {"": ""})
#                 for Residency_scrap in links:
#                     links1 = Residency_scrap.findAll("div", {"class": "reviewRow"})
#                     for review in links1:
#                         review1 = review.find("p", {"class": "latoBold font18 lineHight22 greenText"})  # Review Title
#                         review2 = review.find("span")  # Customer Rating
#                         review3 = review.find("p", {"class": "font14 lineHight22"})  # Review Description
#                             # saving_hotel_text_review[get_hotelID].append(review1.text + " " + review3.text)
#                             # saving_hotel_star_review[get_hotelID].append(review2.text)
#             except:
#                 exception = False

# GOIBIBO

def goibibo(siteName):
    # global variable defined
    global saving_hotel_text_review
    global saving_hotel_star_review

    # Hotel ids for URL
    hotel_id = {}
    hotel_id["The_Park_Navi_Mumbai-Navi_Mumbai"] = "the-park-navi-mumbai-hotel-in-navi-mumbai-6571195111223029170"
    hotel_id["residency hotel"] = "residency-hotel-in-mumbai-3614109768092723331"
    hotel_id["the resort"] = "the-resort-mumbai-hotel-in-mumbai-2362912313949093326"
    hotel_id["parle international"] = "parle-international-hotel-in-mumbai-5773950970688245045"
    hotel_id["goldfinch hotel"] = "goldfinch-hotel-in-mumbai-3284505915249380043"
    hotel_id["sukh hotel"] = "sukh-hotel-in-mumbai-4768950949133964669"
    hotel_id["hotel le grande"] = "le-grande-hotel-in-mumbai-3488104441006598328"
    hotel_id["hotel fortune"] = "fortune-hotel-in-mumbai-6203860387500170863"
    hotel_id["Annex Executive"] = "annex-executive-hotel-in-mumbai-4492873573747394964"
    hotel_id["Mango_Hotels_Navi_Mumbai_Airoli-Navi_Mumbai"] = "mango-hotels-airoli-hotel-in-navi-mumbai-4905261939687894411"
    hotel_id["Hotel_Manama-Mumbai"] = "manama-hotel-in-mumbai-6389032922002493377"

    for h_name in city_hotel[city_name]:
        c_id = hotel_id[h_name] # get the hotel id for each hotel

        #  URL
        url = "https://www.goibibo.com/hotels/" + c_id + "/"

        try:
            main_page_data = driver.get(url)
            driver.set_window_position(-3000, 0)
        except:
            exception = True

        def getRating():
            # rating class in goibibo
            rating_color_class = ["rankingWrapDeepGreen", "rankingWrapRed", "rankingWrapGreen", "rankingWrapLightGreen","rankingWrapOrange"]
            t.sleep(2)
            # loop through all the rating
            for color in rating_color_class:
                soup = BeautifulSoup(driver.page_source, "lxml")
                links = soup.find_all('span', {"class": color})
                # save the rating
                for i in links:
                    rating = i.find("strong").text
                    # if (len(rating) < 3):
                    saving_hotel_star_review[h_name].append(int(rating))

        try:
            soup_ul = BeautifulSoup(driver.page_source, "lxml")
            links_ul = soup_ul.find_all('ul', {"class": "newqnaPagination"})
            total_navigation = len(links_ul[0].find_all("li"))
            last_navigation = links_ul[0].find_all("li")[total_navigation - 1].find("a").find("i")
            go_next_page = True
            nav_page = 0
            count = 1
            # loop through all the pages
            while (go_next_page):

                if (last_navigation != None):
                    for next_page in range(1, total_navigation):
                        count = count + 1
                        driver.find_element_by_xpath(u'//a[text()="' + str(count) + '"]').click()
                        getRating()
                else:
                    getRating()
        except:
            exception = True
            print("issue 2")

# YATRA
def yatra(siteName):

    global saving_hotel_text_review
    global saving_hotel_star_review

    # hotel id's w.r.t to site
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

    for h_name in city_hotel[city_name]:
        print("1")
        c_id = hotel_id[h_name]

        review = "Reviews-"

        main = "https://hotel.yatra.com/hotel-search/dom/details?" \
               "checkinDate=" + checkInDate + "&checkoutDate=" + checkOutDate + "&roomRequests%" \
                "5B0%5D.id=1&roomRequests%5B0%5D.noOfAdults=1&roomRequests%5B0%5D.noOfChildren=0" \
                "&source=BOOKING_ENGINE&tenant=B2C&hotelID=" + c_id + "&pg=1&htlFindMthd=booking%20engine:seo"

        try:
            y = driver.get(main)  # getting the html of yatra site using driver
            t.sleep(2)
            driver.set_window_position(-3000, 0)  # cosing the window
            soup = BeautifulSoup(driver.page_source, "lxml")  # coverting the driver to beautifulsoup
            links = soup.find('a',{"class": "link under-link ng-binding ng-scope"})  # to reach tripadvisor site for reviews
            trip_adviser = links.get("href")  # get the href of tripadvisor
            heading = soup.find('span', {"class": "fl ng-binding"}).text
            new_url = heading.replace(" ", "_") + "_Maharashtra.html"
            url_start = trip_adviser[0:trip_adviser.index("Reviews")]
            driver.get(trip_adviser)
            driver.set_window_position(-3000, 0)
            soup = BeautifulSoup(driver.page_source, "lxml")
            links = soup.find('div', {"class": "pageNumbers"}).find_all("a")
            last_page = int(links[len(links) - 1].text)

            # loop through all the review pages
            # last_page
            for page in range(0,20):
                final_url = ""
                # there is different format for first page
                if (page == 0):
                    final_url = url_start + review + new_url
                if (page != 0):
                    final_url = url_start + review + "or" + str(page * 5) + "-" + new_url

                exception = False
                try:
                    driver.get(final_url)
                    t.sleep(2)
                    inner_soup = BeautifulSoup(driver.page_source, "lxml")
                    t.sleep(2)
                    # star rating
                    inner_div = inner_soup.find_all('div',
                    {"class": "hotels-review-list-parts-SingleReview__mainCol--2XgHm"})
                    for i in inner_div:
                        # the value of rating comes in a class....so we use re to get that star rating
                        data = i.find("span").get("class")
                        match = re.findall("[0-9]{2}", data[1])
                        saving_hotel_star_review[h_name].append(match[0])

                    combined_review_text = ""
                    # text review heading
                    inner_text_ = inner_soup.find_all('a', {
                        "class": "hotels-review-list-parts-ReviewTitle__reviewTitleText--3QrTy"})
                    for i in inner_text_:
                        data = i.find("span").find("span").text
                        combined_review_text = data

                    # text review
                    inner_text = inner_soup.find_all('q', {
                        "class": "hotels-review-list-parts-ExpandableReview__reviewText--3oMkH"})
                    for i in inner_text:
                        data = i.text
                        combined_review_text = combined_review_text + " " + data
                    saving_hotel_text_review[h_name].append(combined_review_text)
                except:
                    exception = True
                    print("issue 1")
        except:
            exception = True
            print("issue 1")

# MAKEMYTRIP
def makemytrip(siteName):

    global saving_hotel_text_review
    global saving_hotel_star_review

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


    sp_checkInDate = str(checkInDate).split("/")
    checkInDate_1 = sp_checkInDate[1] + sp_checkInDate[0] + sp_checkInDate[2]
    sp_checkOutDate = str(checkOutDate).split("/")
    checkOutDate_1 = sp_checkOutDate[1] + sp_checkOutDate[0] + sp_checkOutDate[2]

    city_name = "mumbai"
    adults = "2"
    child = "0"
    child_age = "2"
    roomStayQualifier = adults + "e" + child + "e" + child_age + "e"
    # Finding City Code
    for cty_name in city_code_dict:
        if cty_name == city_name:
            city_code = city_code_dict[cty_name]
    # Finding Hotel Name Through the city name
    for hotel in city_hotel:
        if hotel == city_name:
            city_hotel_list = city_hotel[hotel]
    # Finding Hotel ID Through the hotel name
    for get_hotelID in city_hotel_list:
        hotelId = hotel_id[get_hotelID]

        url = "https://www.makemytrip.com/hotels/hotel-details/?checkin=" + checkInDate_1 + "&checkout=" + checkOutDate_1 + "&" \
        "city=" + city_code + "&country=IN&searchText=" + hotel + "%20Hotel&roomStayQualifier=" + roomStayQualifier + "&hotelId=" + hotelId

        try:
            main_page_data = driver.get(url)
            driver.set_window_position(-3000, 0)
            # loop through all the review pages
            nextPage = True
            nextPageCount = 0
            # loop till end
            while (nextPage == True):
                try:
                    nextPageCount = nextPageCount + 1  # counting pages
                    t.sleep(2)
                    soup = BeautifulSoup(driver.page_source, "lxml")
                    links1 = soup.find('ul', {"class": "pagination"})  # getting the navigation bar
                    li = links1.find_all("li")  # getting the navigation button
                    for i in reversed(li):  # checking the navigation from behind
                        x = i.get("class")  # get the class name
                        if (x == ["disabled"]):  # to check if we are on last page
                            nextPage = False  # if we are on last page end loop
                            break
                        break
                    if (nextPage == False or nextPageCount >10):
                        break
                    # press the next page button
                    if (nextPageCount != 1):
                        page = str(nextPageCount)
                        driver.find_element_by_xpath(u'//a[text()="' + page + '"]').click()
                    soup = BeautifulSoup(driver.page_source, "lxml")
                    links = soup.find_all('div', {"": ""})
                    for Residency_scrap in links:
                        links1 = Residency_scrap.findAll("div", {"class": "reviewRow"})
                        for review in links1:
                            review1 = review.find("p", {"class": "latoBold font18 lineHight22 greenText"})  # Review Title
                            review2 = review.find("span")  # Customer Rating
                            review3 = review.find("p", {"class": "font14 lineHight22"})  # Review Description
                            saving_hotel_text_review[get_hotelID].append(review1.text + " " + review3.text)
                            saving_hotel_star_review[get_hotelID].append(review2.text)
                except:
                    exception = False
        except:
            exception = False

    # driver.quit()
    chrome_path = r"C:\Users\Shubham\Downloads\chromedriver_win32\chromedriver"
    driver = webdriver.Chrome(chrome_path)
    city_hotel = {}
    city_hotel["mumbai"] = ["Hotel_Manama-Mumbai"]
    hotel_id = {}
    hotel_id["Hotel_Manama-Mumbai"] = "200701101631373674"

    # Finding City Code
    for cty_name in city_code_dict:
        if cty_name == city_name:
            city_code = city_code_dict[cty_name]
    # Finding Hotel Name Through the city name
    for hotel in city_hotel:
        if hotel == city_name:
            city_hotel_list = city_hotel[hotel]

    # Finding Hotel ID Through the hotel name
    for get_hotelID in city_hotel_list:
        hotelId = hotel_id[get_hotelID]

        url = "https://www.makemytrip.com/hotels/hotel-details/?checkin=" + checkInDate_1 + "&checkout=" + checkOutDate_1 + "&" \
         "city=" + city_code + "&country=IN&searchText=" + hotel + "%20Hotel&roomStayQualifier=" + roomStayQualifier + "&hotelId=" + hotelId

        try:
            main_page_data = driver.get(url)
            driver.set_window_position(-3000, 0)
            # loop through all the review pages
            nextPage = True
            nextPageCount = 0
            # loop till end
            while (nextPage == True):
                try:
                    nextPageCount = nextPageCount + 1  # counting pages
                    t.sleep(2)
                    soup = BeautifulSoup(driver.page_source, "lxml")
                    links1 = soup.find('ul', {"class": "pagination"})  # getting the navigation bar
                    li = links1.find_all("li")  # getting the navigation button
                    for i in reversed(li):  # checking the navigation from behind
                        x = i.get("class")  # get the class name
                        if (x == ["disabled"]):  # to check if we are on last page
                            nextPage = False  # if we are on last page end loop
                            break
                        break
                    if (nextPage == False or nextPageCount > 10):
                        break
                    # press the next page button
                    if (nextPageCount != 1):
                        page = str(nextPageCount)
                        driver.find_element_by_xpath(u'//a[text()="' + page + '"]').click()
                    soup = BeautifulSoup(driver.page_source, "lxml")
                    links = soup.find_all('div', {"": ""})
                    for Residency_scrap in links:
                        links1 = Residency_scrap.findAll("div", {"class": "reviewRow"})
                        for review in links1:
                            review1 = review.find("p",
                                                  {"class": "latoBold font18 lineHight22 greenText"})  # Review Title
                            review2 = review.find("span")  # Customer Rating
                            review3 = review.find("p", {"class": "font14 lineHight22"})  # Review Description
                            saving_hotel_text_review[get_hotelID].append(review1.text + " " + review3.text)
                            saving_hotel_star_review[get_hotelID].append(review2.text)
                except:
                    exception = False
        except:
            exception = False


    chrome_path = r"C:\Users\Shubham\Downloads\chromedriver_win32\chromedriver"
    driver = webdriver.Chrome(chrome_path)
    city_hotel = {}
    city_hotel["mumbai"] = ["Mango_Hotels_Navi_Mumbai_Airoli-Navi_Mumbai"]
    hotel_id = {}
    hotel_id["Mango_Hotels_Navi_Mumbai_Airoli-Navi_Mumbai"] = "201401241221502792"

    # Finding City Code
    for cty_name in city_code_dict:
        if cty_name == city_name:
            city_code = city_code_dict[cty_name]
    # Finding Hotel Name Through the city name
    for hotel in city_hotel:
        if hotel == city_name:
            city_hotel_list = city_hotel[hotel]
    # Finding Hotel ID Through the hotel name
    for get_hotelID in city_hotel_list:
        hotelId = hotel_id[get_hotelID]

        url = "https://www.makemytrip.com/hotels/hotel-details/?checkin=" + checkInDate_1 + "&checkout=" + checkOutDate_1 + "&" \
                                                                                                                        "city=" + city_code + "&country=IN&searchText=" + hotel + "%20Hotel&roomStayQualifier=" + roomStayQualifier + "&hotelId=" + hotelId

        try:
            main_page_data = driver.get(url)
            driver.set_window_position(-3000, 0)
            # loop through all the review pages
            nextPage = True
            nextPageCount = 0
            # loop till end
            while (nextPage == True):
                try:
                    nextPageCount = nextPageCount + 1  # counting pages
                    t.sleep(2)
                    soup = BeautifulSoup(driver.page_source, "lxml")
                    links1 = soup.find('ul', {"class": "pagination"})  # getting the navigation bar
                    li = links1.find_all("li")  # getting the navigation button
                    for i in reversed(li):  # checking the navigation from behind
                        x = i.get("class")  # get the class name
                        if (x == ["disabled"]):  # to check if we are on last page
                            nextPage = False  # if we are on last page end loop
                            break
                        break
                    if (nextPage == False or nextPageCount > 10):
                        break
                    # press the next page button
                    if (nextPageCount != 1):
                        page = str(nextPageCount)
                        driver.find_element_by_xpath(u'//a[text()="' + page + '"]').click()
                    soup = BeautifulSoup(driver.page_source, "lxml")
                    links = soup.find_all('div', {"": ""})
                    for Residency_scrap in links:
                        links1 = Residency_scrap.findAll("div", {"class": "reviewRow"})
                        for review in links1:
                            review1 = review.find("p",
                                                  {"class": "latoBold font18 lineHight22 greenText"})  # Review Title
                            review2 = review.find("span")  # Customer Rating
                            review3 = review.find("p", {"class": "font14 lineHight22"})  # Review Description
                            saving_hotel_text_review[get_hotelID].append(review1.text + " " + review3.text)
                            saving_hotel_star_review[get_hotelID].append(review2.text)
                except:
                    exception = False
        except:
            exception = False

    chrome_path = r"C:\Users\Shubham\Downloads\chromedriver_win32\chromedriver"
    driver = webdriver.Chrome(chrome_path)
    city_hotel = {}
    city_hotel["mumbai"] = ["hotel fortune"]
    hotel_id = {}
    hotel_id["hotel fortune"] = "200711051529003276"

    # Finding City Code
    for cty_name in city_code_dict:
        if cty_name == city_name:
            city_code = city_code_dict[cty_name]
    # Finding Hotel Name Through the city name
    for hotel in city_hotel:
        if hotel == city_name:
            city_hotel_list = city_hotel[hotel]
    # Finding Hotel ID Through the hotel name
    for get_hotelID in city_hotel_list:
        hotelId = hotel_id[get_hotelID]

        url = "https://www.makemytrip.com/hotels/hotel-details/?checkin=" + checkInDate_1 + "&checkout=" + checkOutDate_1 + "&" \
                                                                                                                        "city=" + city_code + "&country=IN&searchText=" + hotel + "%20Hotel&roomStayQualifier=" + roomStayQualifier + "&hotelId=" + hotelId

        try:
            main_page_data = driver.get(url)
            driver.set_window_position(-3000, 0)
            # loop through all the review pages
            nextPage = True
            nextPageCount = 0
            # loop till end
            while (nextPage == True):
                try:
                    nextPageCount = nextPageCount + 1  # counting pages
                    t.sleep(2)
                    soup = BeautifulSoup(driver.page_source, "lxml")
                    links1 = soup.find('ul', {"class": "pagination"})  # getting the navigation bar
                    li = links1.find_all("li")  # getting the navigation button
                    for i in reversed(li):  # checking the navigation from behind
                        x = i.get("class")  # get the class name
                        if (x == ["disabled"]):  # to check if we are on last page
                            nextPage = False  # if we are on last page end loop
                            break
                        break
                    if (nextPage == False or nextPageCount > 10):
                        break
                    # press the next page button
                    if (nextPageCount != 1):
                        page = str(nextPageCount)
                        driver.find_element_by_xpath(u'//a[text()="' + page + '"]').click()
                    soup = BeautifulSoup(driver.page_source, "lxml")
                    links = soup.find_all('div', {"": ""})
                    for Residency_scrap in links:
                        links1 = Residency_scrap.findAll("div", {"class": "reviewRow"})
                        for review in links1:
                            review1 = review.find("p",
                                                  {"class": "latoBold font18 lineHight22 greenText"})  # Review Title
                            review2 = review.find("span")  # Customer Rating
                            review3 = review.find("p", {"class": "font14 lineHight22"})  # Review Description
                            saving_hotel_text_review[get_hotelID].append(review1.text + " " + review3.text)
                            saving_hotel_star_review[get_hotelID].append(review2.text)
                except:
                    exception = False
        except:
            exception = False

    chrome_path = r"C:\Users\Shubham\Downloads\chromedriver_win32\chromedriver"
    driver = webdriver.Chrome(chrome_path)
    city_hotel = {}
    city_hotel["mumbai"] = ["hotel le grande"]
    hotel_id = {}
    hotel_id["hotel le grande"] = "20090509111906380"

    # Finding City Code
    for cty_name in city_code_dict:
        if cty_name == city_name:
            city_code = city_code_dict[cty_name]
    # Finding Hotel Name Through the city name
    for hotel in city_hotel:
        if hotel == city_name:
            city_hotel_list = city_hotel[hotel]
    # Finding Hotel ID Through the hotel name
    for get_hotelID in city_hotel_list:
        hotelId = hotel_id[get_hotelID]

        url = "https://www.makemytrip.com/hotels/hotel-details/?checkin=" + checkInDate_1 + "&checkout=" + checkOutDate_1 + "&" \
                                                                                                                        "city=" + city_code + "&country=IN&searchText=" + hotel + "%20Hotel&roomStayQualifier=" + roomStayQualifier + "&hotelId=" + hotelId

        try:
            main_page_data = driver.get(url)
            driver.set_window_position(-3000, 0)
            # loop through all the review pages
            nextPage = True
            nextPageCount = 0
            # loop till end
            while (nextPage == True):
                try:
                    nextPageCount = nextPageCount + 1  # counting pages
                    t.sleep(2)
                    soup = BeautifulSoup(driver.page_source, "lxml")
                    links1 = soup.find('ul', {"class": "pagination"})  # getting the navigation bar
                    li = links1.find_all("li")  # getting the navigation button
                    for i in reversed(li):  # checking the navigation from behind
                        x = i.get("class")  # get the class name
                        if (x == ["disabled"]):  # to check if we are on last page
                            nextPage = False  # if we are on last page end loop
                            break
                        break
                    if (nextPage == False or nextPageCount > 10):
                        break
                    # press the next page button
                    if (nextPageCount != 1):
                        page = str(nextPageCount)
                        driver.find_element_by_xpath(u'//a[text()="' + page + '"]').click()
                    soup = BeautifulSoup(driver.page_source, "lxml")
                    links = soup.find_all('div', {"": ""})
                    for Residency_scrap in links:
                        links1 = Residency_scrap.findAll("div", {"class": "reviewRow"})
                        for review in links1:
                            review1 = review.find("p",
                                                  {"class": "latoBold font18 lineHight22 greenText"})  # Review Title
                            review2 = review.find("span")  # Customer Rating
                            review3 = review.find("p", {"class": "font14 lineHight22"})  # Review Description
                            saving_hotel_text_review[get_hotelID].append(review1.text + " " + review3.text)
                            saving_hotel_star_review[get_hotelID].append(review2.text)
                except:
                    exception = False
        except:
            exception = False

    chrome_path = r"C:\Users\Shubham\Downloads\chromedriver_win32\chromedriver"
    driver = webdriver.Chrome(chrome_path)
    city_hotel = {}
    city_hotel["mumbai"] = ["sukh hotel"]
    hotel_id = {}
    hotel_id["sukh hotel"] = "200709241520434648"

    # Finding City Code
    for cty_name in city_code_dict:
        if cty_name == city_name:
            city_code = city_code_dict[cty_name]
    # Finding Hotel Name Through the city name
    for hotel in city_hotel:
        if hotel == city_name:
            city_hotel_list = city_hotel[hotel]
    # Finding Hotel ID Through the hotel name
    for get_hotelID in city_hotel_list:
        hotelId = hotel_id[get_hotelID]

        url = "https://www.makemytrip.com/hotels/hotel-details/?checkin=" + checkInDate_1 + "&checkout=" + checkOutDate_1 + "&" \
                                                                                                                        "city=" + city_code + "&country=IN&searchText=" + hotel + "%20Hotel&roomStayQualifier=" + roomStayQualifier + "&hotelId=" + hotelId

        try:
            main_page_data = driver.get(url)
            driver.set_window_position(-3000, 0)
            # loop through all the review pages
            nextPage = True
            nextPageCount = 0
            # loop till end
            while (nextPage == True):
                try:
                    nextPageCount = nextPageCount + 1  # counting pages
                    t.sleep(2)
                    soup = BeautifulSoup(driver.page_source, "lxml")
                    links1 = soup.find('ul', {"class": "pagination"})  # getting the navigation bar
                    li = links1.find_all("li")  # getting the navigation button
                    for i in reversed(li):  # checking the navigation from behind
                        x = i.get("class")  # get the class name
                        if (x == ["disabled"]):  # to check if we are on last page
                            nextPage = False  # if we are on last page end loop
                            break
                        break
                    if (nextPage == False or nextPageCount > 10):
                        break
                    # press the next page button
                    if (nextPageCount != 1):
                        page = str(nextPageCount)
                        driver.find_element_by_xpath(u'//a[text()="' + page + '"]').click()
                    soup = BeautifulSoup(driver.page_source, "lxml")
                    links = soup.find_all('div', {"": ""})
                    for Residency_scrap in links:
                        links1 = Residency_scrap.findAll("div", {"class": "reviewRow"})
                        for review in links1:
                            review1 = review.find("p",
                                                  {"class": "latoBold font18 lineHight22 greenText"})  # Review Title
                            review2 = review.find("span")  # Customer Rating
                            review3 = review.find("p", {"class": "font14 lineHight22"})  # Review Description
                            saving_hotel_text_review[get_hotelID].append(review1.text + " " + review3.text)
                            saving_hotel_star_review[get_hotelID].append(review2.text)
                except:
                    exception = False
        except:
            exception = False

    chrome_path = r"C:\Users\Shubham\Downloads\chromedriver_win32\chromedriver"
    driver = webdriver.Chrome(chrome_path)
    city_hotel = {}
    city_hotel["mumbai"] = ["goldfinch hotel"]
    hotel_id = {}
    hotel_id["goldfinch hotel"] = "201301061913516287"
    # Finding City Code
    for cty_name in city_code_dict:
        if cty_name == city_name:
            city_code = city_code_dict[cty_name]
    # Finding Hotel Name Through the city name
    for hotel in city_hotel:
        if hotel == city_name:
            city_hotel_list = city_hotel[hotel]
    # Finding Hotel ID Through the hotel name
    for get_hotelID in city_hotel_list:
        hotelId = hotel_id[get_hotelID]

        url = "https://www.makemytrip.com/hotels/hotel-details/?checkin=" + checkInDate_1 + "&checkout=" + checkOutDate_1 + "&" \
                                                                                                                        "city=" + city_code + "&country=IN&searchText=" + hotel + "%20Hotel&roomStayQualifier=" + roomStayQualifier + "&hotelId=" + hotelId

        try:
            main_page_data = driver.get(url)
            driver.set_window_position(-3000, 0)
            # loop through all the review pages
            nextPage = True
            nextPageCount = 0
            # loop till end
            while (nextPage == True):
                try:
                    nextPageCount = nextPageCount + 1  # counting pages
                    t.sleep(2)
                    soup = BeautifulSoup(driver.page_source, "lxml")
                    links1 = soup.find('ul', {"class": "pagination"})  # getting the navigation bar
                    li = links1.find_all("li")  # getting the navigation button
                    for i in reversed(li):  # checking the navigation from behind
                        x = i.get("class")  # get the class name
                        if (x == ["disabled"]):  # to check if we are on last page
                            nextPage = False  # if we are on last page end loop
                            break
                        break
                    if (nextPage == False or nextPageCount > 10):
                        break
                    # press the next page button
                    if (nextPageCount != 1):
                        page = str(nextPageCount)
                        driver.find_element_by_xpath(u'//a[text()="' + page + '"]').click()
                    soup = BeautifulSoup(driver.page_source, "lxml")
                    links = soup.find_all('div', {"": ""})
                    for Residency_scrap in links:
                        links1 = Residency_scrap.findAll("div", {"class": "reviewRow"})
                        for review in links1:
                            review1 = review.find("p",
                                                  {"class": "latoBold font18 lineHight22 greenText"})  # Review Title
                            review2 = review.find("span")  # Customer Rating
                            review3 = review.find("p", {"class": "font14 lineHight22"})  # Review Description
                            saving_hotel_text_review[get_hotelID].append(review1.text + " " + review3.text)
                            saving_hotel_star_review[get_hotelID].append(review2.text)
                except:
                    exception = False
        except:
            exception = False

    chrome_path = r"C:\Users\Shubham\Downloads\chromedriver_win32\chromedriver"
    driver = webdriver.Chrome(chrome_path)
    city_hotel = {}
    city_hotel["mumbai"] = ["parle international"]
    hotel_id = {}
    hotel_id["parle international"] = "200703161231099195"
    # Finding City Code
    for cty_name in city_code_dict:
        if cty_name == city_name:
            city_code = city_code_dict[cty_name]
    # Finding Hotel Name Through the city name
    for hotel in city_hotel:
        if hotel == city_name:
            city_hotel_list = city_hotel[hotel]
    # Finding Hotel ID Through the hotel name
    for get_hotelID in city_hotel_list:
        hotelId = hotel_id[get_hotelID]

        url = "https://www.makemytrip.com/hotels/hotel-details/?checkin=" + checkInDate_1 + "&checkout=" + checkOutDate_1 + "&" \
                                                                                                                        "city=" + city_code + "&country=IN&searchText=" + hotel + "%20Hotel&roomStayQualifier=" + roomStayQualifier + "&hotelId=" + hotelId

        try:
            main_page_data = driver.get(url)
            driver.set_window_position(-3000, 0)
            # loop through all the review pages
            nextPage = True
            nextPageCount = 0
            # loop till end
            while (nextPage == True):
                try:
                    nextPageCount = nextPageCount + 1  # counting pages
                    t.sleep(2)
                    soup = BeautifulSoup(driver.page_source, "lxml")
                    links1 = soup.find('ul', {"class": "pagination"})  # getting the navigation bar
                    li = links1.find_all("li")  # getting the navigation button
                    for i in reversed(li):  # checking the navigation from behind
                        x = i.get("class")  # get the class name
                        if (x == ["disabled"]):  # to check if we are on last page
                            nextPage = False  # if we are on last page end loop
                            break
                        break
                    if (nextPage == False or nextPageCount > 10):
                        break
                    # press the next page button
                    if (nextPageCount != 1):
                        page = str(nextPageCount)
                        driver.find_element_by_xpath(u'//a[text()="' + page + '"]').click()
                    soup = BeautifulSoup(driver.page_source, "lxml")
                    links = soup.find_all('div', {"": ""})
                    for Residency_scrap in links:
                        links1 = Residency_scrap.findAll("div", {"class": "reviewRow"})
                        for review in links1:
                            review1 = review.find("p",
                                                  {"class": "latoBold font18 lineHight22 greenText"})  # Review Title
                            review2 = review.find("span")  # Customer Rating
                            review3 = review.find("p", {"class": "font14 lineHight22"})  # Review Description
                            saving_hotel_text_review[get_hotelID].append(review1.text + " " + review3.text)
                            saving_hotel_star_review[get_hotelID].append(review2.text)
                except:
                    exception = False
        except:
            exception = False


    chrome_path = r"C:\Users\Shubham\Downloads\chromedriver_win32\chromedriver"
    driver = webdriver.Chrome(chrome_path)
    city_hotel = {}
    city_hotel["mumbai"] = ["the resort"]
    hotel_id = {}
    hotel_id["the resort"] = "200707250953377576"
    # Finding City Code
    for cty_name in city_code_dict:
        if cty_name == city_name:
            city_code = city_code_dict[cty_name]
    # Finding Hotel Name Through the city name
    for hotel in city_hotel:
        if hotel == city_name:
            city_hotel_list = city_hotel[hotel]
    # Finding Hotel ID Through the hotel name
    for get_hotelID in city_hotel_list:
        hotelId = hotel_id[get_hotelID]

        url = "https://www.makemytrip.com/hotels/hotel-details/?checkin=" + checkInDate_1 + "&checkout=" + checkOutDate_1 + "&" \
                                                                                                                        "city=" + city_code + "&country=IN&searchText=" + hotel + "%20Hotel&roomStayQualifier=" + roomStayQualifier + "&hotelId=" + hotelId

        try:
            main_page_data = driver.get(url)
            driver.set_window_position(-3000, 0)
            # loop through all the review pages
            nextPage = True
            nextPageCount = 0
            # loop till end
            while (nextPage == True):
                try:
                    nextPageCount = nextPageCount + 1  # counting pages
                    t.sleep(2)
                    soup = BeautifulSoup(driver.page_source, "lxml")
                    links1 = soup.find('ul', {"class": "pagination"})  # getting the navigation bar
                    li = links1.find_all("li")  # getting the navigation button
                    for i in reversed(li):  # checking the navigation from behind
                        x = i.get("class")  # get the class name
                        if (x == ["disabled"]):  # to check if we are on last page
                            nextPage = False  # if we are on last page end loop
                            break
                        break
                    if (nextPage == False or nextPageCount > 10):
                        break
                    # press the next page button
                    if (nextPageCount != 1):
                        page = str(nextPageCount)
                        driver.find_element_by_xpath(u'//a[text()="' + page + '"]').click()
                    soup = BeautifulSoup(driver.page_source, "lxml")
                    links = soup.find_all('div', {"": ""})
                    for Residency_scrap in links:
                        links1 = Residency_scrap.findAll("div", {"class": "reviewRow"})
                        for review in links1:
                            review1 = review.find("p",
                                                  {"class": "latoBold font18 lineHight22 greenText"})  # Review Title
                            review2 = review.find("span")  # Customer Rating
                            review3 = review.find("p", {"class": "font14 lineHight22"})  # Review Description
                            saving_hotel_text_review[get_hotelID].append(review1.text + " " + review3.text)
                            saving_hotel_star_review[get_hotelID].append(review2.text)
                except:
                    exception = False
        except:
            exception = False

    chrome_path = r"C:\Users\Shubham\Downloads\chromedriver_win32\chromedriver"
    driver = webdriver.Chrome(chrome_path)
    city_hotel = {}
    city_hotel["mumbai"] = ["The_Park_Navi_Mumbai-Navi_Mumbai"]
    hotel_id = {}
    hotel_id["The_Park_Navi_Mumbai-Navi_Mumbai"] = "200704121637479279"
    # Finding City Code
    for cty_name in city_code_dict:
        if cty_name == city_name:
            city_code = city_code_dict[cty_name]
    # Finding Hotel Name Through the city name
    for hotel in city_hotel:
        if hotel == city_name:
            city_hotel_list = city_hotel[hotel]
    # Finding Hotel ID Through the hotel name
    for get_hotelID in city_hotel_list:
        hotelId = hotel_id[get_hotelID]

        url = "https://www.makemytrip.com/hotels/hotel-details/?checkin=" + checkInDate_1 + "&checkout=" + checkOutDate_1 + "&" \
                                                                                                                        "city=" + city_code + "&country=IN&searchText=" + hotel + "%20Hotel&roomStayQualifier=" + roomStayQualifier + "&hotelId=" + hotelId

        try:
            main_page_data = driver.get(url)
            driver.set_window_position(-3000, 0)
            # loop through all the review pages
            nextPage = True
            nextPageCount = 0
            # loop till end
            while (nextPage == True):
                try:
                    nextPageCount = nextPageCount + 1  # counting pages
                    t.sleep(2)
                    soup = BeautifulSoup(driver.page_source, "lxml")
                    links1 = soup.find('ul', {"class": "pagination"})  # getting the navigation bar
                    li = links1.find_all("li")  # getting the navigation button
                    for i in reversed(li):  # checking the navigation from behind
                        x = i.get("class")  # get the class name
                        if (x == ["disabled"]):  # to check if we are on last page
                            nextPage = False  # if we are on last page end loop
                            break
                        break
                    if (nextPage == False or nextPageCount > 10):
                        break
                    # press the next page button
                    if (nextPageCount != 1):
                        page = str(nextPageCount)
                        driver.find_element_by_xpath(u'//a[text()="' + page + '"]').click()
                    soup = BeautifulSoup(driver.page_source, "lxml")
                    links = soup.find_all('div', {"": ""})
                    for Residency_scrap in links:
                        links1 = Residency_scrap.findAll("div", {"class": "reviewRow"})
                        for review in links1:
                            review1 = review.find("p",
                                                  {"class": "latoBold font18 lineHight22 greenText"})  # Review Title
                            review2 = review.find("span")  # Customer Rating
                            review3 = review.find("p", {"class": "font14 lineHight22"})  # Review Description
                            saving_hotel_text_review[get_hotelID].append(review1.text + " " + review3.text)
                            saving_hotel_star_review[get_hotelID].append(review2.text)
                except:
                    exception = False
        except:
            exception = False

    chrome_path = r"C:\Users\Shubham\Downloads\chromedriver_win32\chromedriver"
    driver = webdriver.Chrome(chrome_path)
    city_hotel = {}
    city_hotel["mumbai"] = ["Annex Executive"]
    # city_hotel["mumbai"]=["Residency","Centre Point Navi Mumbai"]
    # print(city_hotel)
    hotel_id = {}
    hotel_id["Annex Executive"] = "201602021438236409"
    # Finding City Code
    for cty_name in city_code_dict:
        if cty_name == city_name:
            city_code = city_code_dict[cty_name]
    # Finding Hotel Name Through the city name
    for hotel in city_hotel:
        if hotel == city_name:
            city_hotel_list = city_hotel[hotel]
    # Finding Hotel ID Through the hotel name
    for get_hotelID in city_hotel_list:
        hotelId = hotel_id[get_hotelID]

        url = "https://www.makemytrip.com/hotels/hotel-details/?checkin=" + checkInDate_1 + "&checkout=" + checkOutDate_1 + "&" \
                                                                                                                        "city=" + city_code + "&country=IN&searchText=" + hotel + "%20Hotel&roomStayQualifier=" + roomStayQualifier + "&hotelId=" + hotelId

        try:
            main_page_data = driver.get(url)
            driver.set_window_position(-3000, 0)
            # loop through all the review pages
            nextPage = True
            nextPageCount = 0
            # loop till end
            while (nextPage == True):
                try:
                    nextPageCount = nextPageCount + 1  # counting pages
                    t.sleep(2)
                    soup = BeautifulSoup(driver.page_source, "lxml")
                    links1 = soup.find('ul', {"class": "pagination"})  # getting the navigation bar
                    li = links1.find_all("li")  # getting the navigation button
                    for i in reversed(li):  # checking the navigation from behind
                        x = i.get("class")  # get the class name
                        if (x == ["disabled"]):  # to check if we are on last page
                            nextPage = False  # if we are on last page end loop
                            break
                        break
                    if (nextPage == False or nextPageCount > 10):
                        break
                    # press the next page button
                    if (nextPageCount != 1):
                        page = str(nextPageCount)
                        driver.find_element_by_xpath(u'//a[text()="' + page + '"]').click()
                    soup = BeautifulSoup(driver.page_source, "lxml")
                    links = soup.find_all('div', {"": ""})
                    for Residency_scrap in links:
                        links1 = Residency_scrap.findAll("div", {"class": "reviewRow"})
                        for review in links1:
                            review1 = review.find("p",
                                                  {"class": "latoBold font18 lineHight22 greenText"})  # Review Title
                            review2 = review.find("span")  # Customer Rating
                            review3 = review.find("p", {"class": "font14 lineHight22"})  # Review Description
                            saving_hotel_text_review[get_hotelID].append(review1.text + " " + review3.text)
                            saving_hotel_star_review[get_hotelID].append(review2.text)
                except:
                    exception = False
        except:
            exception = False

import statistics
from textblob import TextBlob
_star_review={}
_star_review["The_Park_Navi_Mumbai-Navi_Mumbai"]=0
_star_review["residency hotel"] = 0
_star_review["the resort"] = 0
_star_review["parle international"] = 0
_star_review["goldfinch hotel"] = 0
_star_review["sukh hotel"] = 0
_star_review["hotel le grande"] = 0
_star_review["hotel fortune"] = 0
_star_review["Annex Executive"] = 0
_star_review["Mango_Hotels_Navi_Mumbai_Airoli-Navi_Mumbai"] = 0
_star_review["Hotel_Manama-Mumbai"] = 0

_text_review={}
_text_review["The_Park_Navi_Mumbai-Navi_Mumbai"]=0
_text_review["residency hotel"] = 0
_text_review["the resort"] = 0
_text_review["parle international"] = 0
_text_review["goldfinch hotel"] = 0
_text_review["sukh hotel"] = 0
_text_review["hotel le grande"] = 0
_text_review["hotel fortune"] = 0
_text_review["Annex Executive"] = 0
_text_review["Mango_Hotels_Navi_Mumbai_Airoli-Navi_Mumbai"] = 0
_text_review["Hotel_Manama-Mumbai"] = 0



# running through all the sites
for site in sites:
    if site == "makemytrip":
        makemytrip(site)
    if site == "goibibo":
        goibibo(site)
    if site == "yatra":
        yatra(site)
# print(saving_hotel_star_review)

con=sqlite3.connect("hotel.db")
cur=con.cursor()

# finding the sentiment for each review for each hotel in each site
for k,text in saving_hotel_text_review.items():
    text_count=len(text)
    count=0
    for i in text:
        count =count+1
        analysis = TextBlob(i)
        _text_review[k]= _text_review[k] + abs(analysis.sentiment.polarity)



# saving the sentiment data in database
for k,v in saving_hotel_star_review.items():
    data=[int(i) for i in v]
    if len(data) == 0:
        mean_data=0
    else:
        mean_data =statistics.mean(data)
    _star_review[k]=mean_data
    text_review_data=str(_text_review[k]* 10)
    cur.execute("INSERT INTO hotelDetails(h_name,h_star_rating,h_text_rating) VALUES(?,?,?)",(k,str(mean_data),text_review_data))

con.commit()
con.close()






