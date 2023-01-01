import gspread

from oauth2client.service_account import ServiceAccountCredentials

dic = {}
cities_list = []
cost_list = []
SCOPE = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]
user_email_list = []

CREDS = ServiceAccountCredentials.from_json_keyfile_name("./flight_keys.json", scopes=SCOPE)


# <-------It reads and writes google sheets------->
class ReadWrite:
    def __init__(self):
        self.file = gspread.authorize(CREDS)
        self.workbook = self.file.open("cheapFlights")
        self.flight_sheet = self.workbook.sheet1
        try:
            self.user_sheet = self.workbook.add_worksheet("Sheet2", 100,
                                                          1000)  # create a new one if there is not sheet2
        except gspread.exceptions.APIError:
            self.user_sheet = self.workbook.get_worksheet(1)  # index starts for 0. So it's 1 for sheet2
        self.city_low_cost_dict = self.create_city_dict()

    def create_city_dict(self):  # Creates a dict with info in sheet1. IACA CODE: Desired cheap prize
        a = 1
        for city in self.flight_sheet.range("B2:B11"):
            a += 1
            dic[city.value] = self.flight_sheet.acell(f"C{a}").value
        return dic

    def find_city_name(self, iaca_code: str):  # Takes IACA CODE as input and gives city name as output
        b = 1
        for city in self.flight_sheet.range("B2:B10"):
            b += 1
            if iaca_code == city.value:
                city_name = (self.flight_sheet.acell("A{}".format(b))).value
                return city_name

    def upload_user_info(self, info_tuple):  # Uploads the provided user info to sheet2
        lst = [info for info in info_tuple]
        self.user_sheet.append_row(lst)

    def emails_list(self):  # Takes emails from column 2 (B) and makes a list
        for index, email in enumerate(self.user_sheet.col_values(3)):
            if index == 0:
                pass
            else:
                user_email_list.append(email)
        return user_email_list
