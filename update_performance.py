# Import Modules
from credentials import USERNAME1, PASSWORD1
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from time import sleep
from selenium.webdriver.common.by import By
import json
import re
import datetime
import os
import requests
from webdriver_manager.chrome import ChromeDriverManager
from credentials import USERNAME2, PASSWORD2
# Access credentials
# from credentials import UTAH_API_KEY


# Main Account Table to get data of it's content
mainAccountTableInfo = []
currPATH = os.getcwd() + "/app/routes/Automation/scripts"

print("My Path:" + currPATH)


class Bot:
    # Automation Function
    def __init__(self):
        print("Selenium script started...")
        userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36"

        self.options = webdriver.ChromeOptions()
        self.options.headless = False
        self.options.add_argument("user-agent=" + userAgent)
        self.options.add_argument("--window-size=1920,1080")
        self.options.add_argument('--ignore-certificate-errors')
        self.options.add_argument('--allow-running-insecure-content')
        self.options.add_argument("--disable-extensions")
        self.options.add_argument("--proxy-server='direct://'")
        self.options.add_argument("--proxy-bypass-list=*")
        self.options.add_argument("--start-maximized")
        self.options.add_argument('--disable-gpu')
        self.options.add_argument('--disable-dev-shm-usage')
        self.options.add_argument('--no-sandbox')
        # self.driver = webdriver.Chrome(
        #     executable_path= "drivers/chromedriver_new_linux", options=self.options)
        self.driver = webdriver.Chrome(
            ChromeDriverManager().install(), options=self.options)

        # apiEndpoint = "https://prod.api.sootchy529.com/accounts/utah"

        # headers = {'Content-type': 'application/json',
        #            'Accept': 'text/plain', 'x-api-key': UTAH_API_KEY}

        # DO a API
        # print("Running the API call")
        # infoFile1 = open(currPATH + "/accountNumbers.json", 'r')
        # with open(currPATH + '/jsonFiles/accountNumbers.json') as accountNumberJson:
        #     data = json.load(accountNumberJson)
        # print("data file:", data)
        # accountNumbers = data
         # Create and append AccountInfo to a json file (accountInfos.json)

        apiEndpoint = "https://prod.api.sootchy529.com/accounts/utah"

        headers = {'Content-type': 'application/json',
                   'Accept': 'text/plain', 'x-api-key': 'zHRzQnz0eY4i8iwqRzb2K1guDag98A266j7MXlcf'}

        # DO a API
        print("Running the API call")

        accountNumbers = []
        
        r = requests.get(url=apiEndpoint, headers=headers)
        response = json.loads(r.text)
        accounts = response['data']

        for i in accounts:
            accountNumbers.append(i)

        self.driver.get("https://fa.my529.org/login")
        self.driver.maximize_window()
        sleep(3)
        print("Entering Credentials...")

        self.driver.find_element_by_xpath(
            "/html/body/div/div[1]/div[3]/main/div/div/div/div/div/div[1]/form/div[1]/div/input").send_keys(USERNAME2)

        self.driver.find_element_by_xpath(
            "/html/body/div/div[1]/div[3]/main/div/div/div/div/div/div[1]/form/div[2]/div/input").send_keys(PASSWORD2)

        self.driver.find_element_by_xpath(
            "/html/body/div/div[1]/div[3]/main/div/div/div/div/div/div[1]/form/div[3]/button").click()

        sleep(20)

        # Check if modal exists, if exists run
        if(self.driver.find_elements_by_xpath("/html/body/div[2]/div[3]/div/div/div[2]/button/span[1]")):
            self.driver.find_element_by_xpath(
                "/html/body/div[2]/div[3]/div/div/div[2]/button/span[1]").click()
        print("Navigating to Accounts...")

        sleep(2)

        self.driver.find_element_by_xpath(
            "/html/body/div/div[1]/div[1]/header/div[1]/div[1]/div/button/span[1]/span").click()

        sleep(2)

        self.driver.find_element_by_xpath(
            "/html/body/div[2]/div[3]/div/div[1]/div[3]/div/div/div[2]").click()

        sleep(2)

        self.driver.find_element_by_xpath(
            "/html/body/div[2]/div[3]/div/div[1]/div[3]/div/div[2]/div/div/div/div[1]").click()

        sleep(3)

        # Search and find the data according to the account numbers
        searchButton = True
        for i in accountNumbers:
            if(len(i) != 9 ):
                continue
            if(searchButton == True ):
                # Click on the seach button
                self.driver.find_element_by_xpath(
                    "/html/body/div[1]/div[1]/div[3]/main/div/div/div[1]/div[2]/div/div[1]/div/button[2]").click()

                sleep(1)

            # Pass data to search input
            self.driver.find_element_by_xpath(
                "/html/body/div[1]/div[1]/div[3]/main/div/div/div[1]/div[2]/div/div[1]/div/input").send_keys(i)

            sleep(1)
            print(i)
            # Click on the account number option
            self.driver.find_element_by_css_selector(
                "#Table_searchMenu > li:nth-child(1)").click()
            sleep(1)

            if(self.driver.find_element_by_xpath("/html/body/div/div[1]/div[3]/main/div/div/table/tbody/tr/td").text != "No data to display."):
                # Get data of the first account
                print("Account number", i)

                accountNumber = self.driver.find_element_by_xpath(
                    "/html/body/div[1]/div[1]/div[3]/main/div/div/table/tbody/tr/td[1]").text
                accountOwnerName = self.driver.find_element_by_xpath(
                    "/html/body/div[1]/div[1]/div[3]/main/div/div/table/tbody/tr/td[2]").text
                beneficiaryName = self.driver.find_element_by_xpath(
                    "/html/body/div[1]/div[1]/div[3]/main/div/div/table/tbody/tr/td[3]").text
                marketValue = self.driver.find_element_by_xpath(
                    "/html/body/div[1]/div[1]/div[3]/main/div/div/table/tbody/tr/td[8]").text
                marketValue = marketValue.replace('$', '')
                marketValue = marketValue.replace(',', '')

                # Click on the option button (three dots)
                self.driver.find_element_by_css_selector(
                    "#root > div:nth-child(1) > div.Navigation_featuresContainer > main > div > div > table > tbody > tr > td.Table_iconColumn > div > button").click()

                sleep(1)

                while True:
                    try:
                        self.driver.find_element_by_css_selector(
                            "body > div:nth-child(11) > div.MuiPaper-root.MuiMenu-paper.MuiPaper-elevation8.MuiPopover-paper.MuiPaper-rounded > ul > li:nth-child(1)").click()
                        break
                    except:
                        if(self.driver.find_element_by_css_selector(
                                "body > div:nth-child(10) > div.MuiPaper-root.MuiMenu-paper.MuiPaper-elevation8.MuiPopover-paper.MuiPaper-rounded > ul > li:nth-child(1)")):
                            try:
                                self.driver.find_element_by_css_selector(
                                    "body > div:nth-child(10) > div.MuiPaper-root.MuiMenu-paper.MuiPaper-elevation8.MuiPopover-paper.MuiPaper-rounded > ul > li:nth-child(1)").click()
                                break
                            except:
                                self.driver.find_element_by_css_selector(
                                    "body > div:nth-child(12) > div.MuiPaper-root.MuiMenu-paper.MuiPaper-elevation8.MuiPopover-paper.MuiPaper-rounded > ul > li:nth-child(1)").click()

                                break
                        # else:
                        #     self.driver.find_element_by_css_selector(
                        #         "body > div: nth-child(12) > div.MuiPaper-root.MuiMenu-paper.MuiPaper-elevation8.MuiPopover-paper.MuiPaper-rounded > ul > li: nth-child(1)").click()
                        #     break

                # while True:
                #     try:
                #         self.driver.find_element_by_css_selector(
                #             "body > div:nth-child(10) > div.MuiPaper-root.MuiMenu-paper.MuiPaper-elevation8.MuiPopover-paper.MuiPaper-rounded > ul > li:nth-child(1)").click()
                #         break
                #     except:
                #         print("Error")

                # while True:
                #     try:
                #         self.driver.find_element_by_css_selector(
                #             "body > div.MuiPopover-root > div.MuiPaper-root.MuiMenu-paper.MuiPaper-elevation8.MuiPopover-paper.MuiPaper-rounded > ul > li:nth-child(1)").click()
                #         break
                #     except:
                #         print("Error")

                #         # Click on View Details
                # if(self.driver.find_elements_by_css_selector("body > div:nth-child(11) > div.MuiPaper-root.MuiMenu-paper.MuiPaper-elevation8.MuiPopover-paper.MuiPaper-rounded > ul > li:nth-child(1)")):
                #     self.driver.find_element_by_css_selector(
                #         "body > div:nth-child(11) > div.MuiPaper-root.MuiMenu-paper.MuiPaper-elevation8.MuiPopover-paper.MuiPaper-rounded > ul > li:nth-child(1)").click()
                # elif(self.driver.find_elements_by_css_selector("body > div:nth-child(10) > div.MuiPaper-root.MuiMenu-paper.MuiPaper-elevation8.MuiPopover-paper.MuiPaper-rounded > ul > li:nth-child(1)")):
                #     self.driver.find_element_by_css_selector(
                #         "body > div:nth-child(10) > div.MuiPaper-root.MuiMenu-paper.MuiPaper-elevation8.MuiPopover-paper.MuiPaper-rounded > ul > li:nth-child(1)").click()
                # else:
                #     self.driver.find_element_by_css_selector(
                #         "body > div.MuiPopover-root > div.MuiPaper-root.MuiMenu-paper.MuiPaper-elevation8.MuiPopover-paper.MuiPaper-rounded > ul > li:nth-child(1)").click()

                sleep(5)

                netPrincipal = self.driver.find_element_by_css_selector(
                    "#root > div:nth-child(1) > div.Navigation_featuresContainer > main > div > div > div > div.AccountDetails_accountContainer > div.AccountDetails_detailsCard > div > div > div > div > div.AccountDetails_netPrincipal > div:nth-child(2)").text
                netPrincipal = netPrincipal.replace('$', '')
                netPrincipal = netPrincipal.replace(',', '')

                if(self.driver.find_element_by_xpath("/html/body/div/div[1]/div[3]/main/div/div/div/div[5]/div[4]/div/div/div/div[1]/div[2]/div[2]").text != "Not Available"):
                    personalRateOfReturn = self.driver.find_element_by_xpath(
                        "/html/body/div[1]/div[1]/div[3]/main/div/div/div/div[5]/div[4]/div/div/div/div[1]/div[2]/div[2]").text

                    personalRateOfReturn = personalRateOfReturn.split("\n")[1]
                    personalRateOfReturn = personalRateOfReturn.replace(
                        ' ', '')
                    personalRateOfReturn = personalRateOfReturn.replace(
                        '%', '')

                    try:
                        personalRateOfReturn = float(personalRateOfReturn)
                    except:
                        personalRateOfReturn = 0
                else:
                    personalRateOfReturn = 0

                data = {
                    "accountNumber": accountNumber,
                    "accountOwnerName": accountOwnerName,
                    "beneficiaryName": beneficiaryName,
                    "totalValue": float(marketValue),
                    "netPrincipal": float(netPrincipal),
                    "personalRateOfReturn": personalRateOfReturn,
                }
                print(data)
                mainAccountTableInfo.append(data)

                # Go back to accounts home page
                self.driver.find_element_by_css_selector(
                    "#root > div:nth-child(1) > div.Navigation_featuresContainer > main > div > div > div > div.AccountDetails_pageNav > div > a").click()
                sleep(1)
            else:
                print(i, "Not found")

            # # Again Seach for other accounts

            # # Clear the input
            # self.driver.find_element_by_xpath(
            #     "/html/body/div/div[1]/div[3]/main/div/div/div[1]/div[2]/div/div[1]/div/span[2]/span").click()
            # sleep(0.5)

            # Make searchButton to false
            # searchButton = False

        print("Writing data to the external file.")

        # Create and append AccountInfo to a json file (accountInfos.json)
        infoFile = open(currPATH + "/jsonFiles/extractedAccounts.json", 'w')
        infoFile.write(json.dumps(mainAccountTableInfo, indent=2))

        infoFile.close()


Bot()
