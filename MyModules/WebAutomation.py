from MyModules import utils
import os
import msedge.selenium_tools
import shutil
import time

class COOsite:

    def __init__(self):
        self.user_id = utils.global_variable().login()
        self.browser = self.get_edge()

    def get_edge(self):
        options = msedge.selenium_tools.EdgeOptions()
        options.use_chromium = True
        if not os.path.isdir("C:\\Users\\" + self.user_id + "\\AppData\\Local\\Microsoft\\Edge\\User Data2"):
            print("Please, make sure MS Edge is closed")
            time.sleep(5)
            shutil.copytree("C:\\Users\\" + self.user_id + "\\AppData\\Local\\Microsoft\\Edge\\User Data",
                            "C:\\Users\\" + self.user_id + "\\AppData\\Local\\Microsoft\\Edge\\User Data2")

        options.add_argument(
            "user-data-dir=C:\\Users\\" + self.user_id + "\\AppData\\Local\\Microsoft\\Edge\\User Data2")
        driver = msedge.selenium_tools.Edge(
            executable_path=("C:\\Users\\" + self.user_id + "\\Downloads\\msedgedriver.exe"),
            options=options)
        driver.maximize_window()
        return driver

    # login to web site
    def logingtoSIte(self):

        self.browser.get('https://vientiasiakirjat.fi/auth/login?lang=en')
        time.sleep(1)
        button = self.browser.find_element_by_xpath("/html/body/div/div/div/div/form/button/span")
        button.click()
        time.sleep(1)
        self.browser.quit()
        # self.browser.get('https://vientiasiakirjat.fi/customer/certificates-of-origin/new')
        # time.sleep(1)

    # Fill ine 1. Consignor (exporter)
    def fillConsignor(self):
        element = self.browser.find_element_by_xpath("//*[@id='consignor']")
        element.send_keys("Kemira Oyj")
        element = self.browser.find_element_by_xpath("//*[@id='consignorAddress']")
        element.send_keys("P.O.Box 330 \n00101 Helsinki \nFinland")

    # fill 2. Consignee
    def fillConsignee(self, name, address, country):
        self.browser.find_element_by_xpath('/html/body/div[1]/div/div/div/form/div/div[2]/div[4]/div/div').click()
        # select Consignee country
        CntrNr = 0
        Country = country
        while CntrNr < 249:
            xpath = "//*[@id='react-select-4-option-" + str(CntrNr) + "']"
            if self.browser.find_element_by_xpath(xpath).text == Country:
                self.browser.find_element_by_xpath(xpath).click()
                break
            else:
                CntrNr += 1

        ConsigName = self.browser.find_element_by_xpath("//*[@id='consignee']")
        ConsigName.send_keys(name)

        ConsigAddress = self.browser.find_element_by_xpath("//*[@id='consigneeAddress']")
        ConsigAddress.send_keys(address)

        if __name__ == "__main__":
            COOsite()

    # 3 Country of origin
    def fillCOO(self, country):
        country = str(country)
        self.browser.find_element_by_xpath(
            "/html/body/div[1]/div/div/div/form/div/div[3]/div[2]/div/div/div/div/div/div[1]").click()
        CntrNr = 1
        while CntrNr < 249:
            xpath = '/html/body/div[1]/div/div/div/form/div/div[2]/div[4]/div/div/div[2]/div/div[' + str(CntrNr) + ']'
            if self.browser.find_element_by_xpath(xpath).text == "European Union - " + country:
                self.browser.find_element_by_xpath(xpath).click()
                break
            elif self.browser.find_element_by_xpath(xpath).text == country:
                self.browser.find_element_by_xpath(xpath).click()
                break

            CntrNr += 1

    # 4 Transport - always select sea
    def fillTranportMode(self):

        self.browser.find_element_by_xpath("//*[@id='select-transportDetails']").click()
        self.browser.find_element_by_xpath('/html/body/div[4]/div[3]/ul/li[2]').click()

    # 5. Remarks
    def fillRemarks(self, text):
        refNr = self.browser.find_element_by_xpath("//*[@id='remarks']")
        refNr.send_keys(text)

        refNr = self.browser.find_element_by_xpath("//*[@id='customerReference']")
        refNr.send_keys(text)

    # 6. Description of goods
    def fillGoodsDiscrp(self, tradename, pakpal, net, gross):
        self.browser.find_element_by_xpath('//*[@id="items"]').send_keys(tradename, "\n", pakpal, "\n\n\n")

        self.browser.find_element_by_xpath('//*[@id="quantity"]').send_keys(str(net), "\n", str(gross))

    def restofclicks(self):
        # click - Company's own production
        self.browser.find_element_by_xpath("/html/body/div[1]/div/div/div/form/div/div[7]/div[2]/fieldset/div/label["
                                           "1]/span[1]").click()
        # click - I will print by myself
        self.browser.find_element_by_xpath("/html/body/div[1]/div/div/div/form/div/div[8]/div[3]/fieldset/div/label["
                                           "1]/span[2]").click()

        # click attachment for Invoice
        self.browser.find_element_by_xpath("/html/body/div[1]/div/div/div/form/div/div[7]/div[3]/div[1]/div").click()

        # english
        self.browser.find_element_by_xpath("/html/body/div[1]/div/header/div/div[1]/span[3]").click()


class JenkarPortal:

    def __init__(self):
        self.browser = self.open_browser()

    def open_browser(self):
        UserLogin = utils.global_variable().login()
        browser = msedge.selenium_tools.Edge(
            executable_path='C:\\Users\\' + UserLogin + '\\Downloads\\msedgedriver.exe')
        return browser

    # login to web site
    def logingtoSIte(self):
        print("Login to the Jenkar Portal")
        self.browser.maximize_window()
        self.browser.get(
            'https://www.jenkar.systems/Jenkarportal/login.cfm?CFID=2611&CFTOKEN=5bdb78059960fa00-E6410375-F897-BFD2'
            '-67A4BDF2531F64ED')
        time.sleep(1)
        # Insert Login and Password to account

        username = self.browser.find_element_by_id("fld_userEmail")
        username.send_keys('shipments.export@kemira.com')

        userpasword = self.browser.find_element_by_id("fld_userPassword")
        userpasword.send_keys('K3m1raT3mpPwd')
        self.browser.find_element_by_id("fld_submitLogin").click()
        print("Logged in as shipments.export@kemira.com")
        time.sleep(1)
        self.browser.find_element_by_id("btnCDS").click()

    def upload_excel(self, file_name):
        # Excel upload
        self.browser.get('https://www.jenkar.systems/JenkarPortal/cds/uploadkemiraXLfile.cfm')
        time.sleep(1)
        self.browser.find_element_by_id("body").click()
        time.sleep(1)

        utils.Jenkar_automation().handle_popup_Jenkar(text=utils.global_variable().file_path() + file_name)
        time.sleep(2)
        self.browser.find_element_by_xpath("/html/body/div/div/div[2]/div/div/div/div[2]/form/div[3]/button").click()
        print("Excel was loaded")

    def upload_invoice(self, ship_nr, file_name="83616510 Inv.pdf"):
        print("Shipment ", ship_nr)
        self.browser.find_element_by_xpath(
            "/html/body/div[2]/div/div[2]/div/div[1]/div/div[2]/div/div[2]/div/div[2]/label/input").send_keys(ship_nr)
        # check lines where there is no Invoice
        for line in range(0, 7):
            try:
                if not self.browser.find_element_by_xpath(
                        "/html/body/div[2]/div/div[2]/div/div[1]/div/div[2]/div/div[2]/div/table/tbody/tr[" + str(
                            line) + "]/td[9]/input").is_selected():
                    self.browser.find_element_by_xpath(
                        "/html/body/div[2]/div/div[2]/div/div[1]/div/div[2]/div/div[2]/div/table/tbody/tr[2]/td[1]/a/u").click()
                    self.browser.find_element_by_xpath(
                        "/html/body/div[2]/div/div[2]/div[4]/div/div/div/form/div/div/button").click()
                    time.sleep(2)
                    self.browser.find_element_by_xpath(
                        "/html/body/div[3]/div/div/div[2]/div/form/div[2]/input").send_keys(
                        "Invoice O19664075")
                    print("File name Invoice O19664075")
                    self.browser.find_element_by_id("body").click()

                    time.sleep(1)

                    utils.Jenkar_automation().handle_popup_Jenkar(text=utils.global_variable().file_path() + file_name)
                    self.browser.find_element_by_xpath(
                        "/html/body/div[3]/div/div/div[2]/div/form/div[6]/button").click()

            except:
                # reached end of the list
                continue
