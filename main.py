# <-------IMPORT STATEMENTS------->
from datetime import datetime as dt
from datetime import timedelta as time_change
import requests
from write_read_gsheets import ReadWrite
from email_sender import MailMan
from user_reg import RegisterUser
from passcode import API_KEY

# <-------CONSTANTS------->
TRAVEL_API_ENDPOINT = "https://tequila-api.kiwi.com/v2/search"

# <-------Instance of Read_Write Object------->
editor = ReadWrite()
cities_low_cost = editor.city_low_cost_dict
input_bot = RegisterUser()


def opening_lines():
    print(input_bot.welcome, end="\n")
    print(input_bot.proclaimation, end="\n")


class FlightTrackerBot:
    def __init__(self):
        today = dt.now()
        after_10_days = today + (time_change(days=15))
        formated_today_date = today.date().strftime("%d/%m/%Y")
        formated_after_10days = after_10_days.date().strftime("%d/%m/%Y")

        self.travel_parameters = {
            "fly_from": "LON",
            "fly_to": "",
            "dateFrom": "{}".format(formated_today_date),
            "dateTo": "{}".format(formated_after_10days),
        }

        self.travel_header = {
            "Content-Type": "application/json",
            "apikey": API_KEY
        }
        self.general_message = 'Current Lowest Prizes\n\n'

        self.cheap_flight_message = ""

    def input_process(self):
        user_input = input_bot.take_input()
        editor.upload_user_info(user_input)
        not_end_reg = input("\nAre there any other users? Yes(y) or No(n): ")
        if not_end_reg == "y":
            self.input_process()
        else:
            pass

    def create_via_message(self, a: int, via_cities: list):  # sentence creator
        end_message = ''
        if len(via_cities) > 3:
            while a <= len(via_cities) - 1 - 1 - 2:
                end_message += f"{via_cities[a]}, {self.create_via_message(a + 1, via_cities)}"
                return end_message
            end_message += "{} and {}.".format(via_cities[-3], via_cities[-2])
            return end_message

        elif len(via_cities) == 3:
            end_message = f"{via_cities[0]} and {via_cities[1]}."
            return end_message
        elif len(via_cities) == 2:
            end_message = f"{via_cities[0]}."
            return end_message
        else:
            end_message = ""
            return end_message

    def check_prizes(self, exchange_rate: int, currency: str):
        self.cheap_flight_message = ''

        for city, our_low_cost in cities_low_cost.items():
            self.travel_parameters["fly_to"] = city
            response = requests.get(url=TRAVEL_API_ENDPOINT, params=self.travel_parameters, headers=self.travel_header)
            response.raise_for_status()
            data = response.json()  # Want to see API json data? Print this.
            print(data)
            try:
                data_low_price = int(
                    data['data'][0]['price'] * exchange_rate)
            except IndexError:
                continue
            flight_route = [route_dict['cityTo'] for route_dict in data['data'][0]['route']]
            print(f"{city} route is {flight_route}")

            if not len(flight_route) <= 1:
                via_end_message = f"via {self.create_via_message(0, via_cities=flight_route)}"
                print(via_end_message)
            else:
                via_end_message = ''

            l_departure_date = data['data'][0]['local_departure'][:10]
            date_time_sentence = "Local date of departure: {}\n".format(l_departure_date)

            l_departure_time = data['data'][0]['local_departure'][11:16]
            date_time_sentence += "Time of departure: {}".format(l_departure_time)
            print(date_time_sentence)

            flight_duration = "{:.2f}".format((data['data'][0]['duration']['total'] / 60) / 60)
            duration_sentence = "Flight duration: {} hrs\n\n".format(flight_duration)
            print(duration_sentence)

            if (int(our_low_cost) * exchange_rate) >= data_low_price:
                self.cheap_flight_message += "{} flight is lowest ever! cost: {} {}\nRoute: From London to {} {}\n{}\n{}".format(
                    editor.find_city_name(city).upper(),
                    data_low_price,
                    currency,
                    editor.find_city_name(city).title(),
                    via_end_message,
                    date_time_sentence,
                    duration_sentence
                )
            else:
                self.general_message += "London to {} at {} {}\nRoute: From London to {} {}\n{}\n{}".format(
                    str(editor.find_city_name(city)).title(),
                    data_low_price,
                    currency,
                    editor.find_city_name(city),
                    via_end_message,
                    date_time_sentence,
                    duration_sentence
                )

    def email_initiator(self):
        email_sender = MailMan()

        if len(self.cheap_flight_message) == 0:
            email_sender.send_email(sending_message=f"Subject:Cheap Flight Rates\n\n{self.general_message}",
                                    to_email_list=editor.emails_list())
        elif len(self.cheap_flight_message) != 0:
            email_sender.send_email(
                sending_message=f"Subject:Found an All Time Cheap Flight Offer\n\n{self.cheap_flight_message}\nAlso check these\n"
                                f"{self.general_message}", to_email_list=editor.emails_list()
            )


# <-------Instance of FlightTrackerBot Object------->
flight_bot = FlightTrackerBot()
opening_lines()
flight_bot.input_process()

flight_bot.check_prizes(exchange_rate=1, currency="EUROS")
flight_bot.email_initiator()
