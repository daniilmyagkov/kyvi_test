import asyncio
import json
import logging
import requests
from datetime import datetime



logging.basicConfig(level=logging.DEBUG,
                    # filename=f"logs/{datetime.datetime.now().strftime('%Y-%m-%d_%H#%M#%S')}.log",filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s")

day1 = datetime.now().day

class LibreLinkUp:
    def __init__(self, token, patientId, country, headers):
        self.patient_id = patientId
        self.token = token
        self.country = country
        self.headers = headers


    def get_measurment(self):
        url = "https://api-" + self.country + ".libreview.io/llu/connections/" + self.patient_id + "/graph"

        payload = ""
        self.headers["Authorization"] = "Bearer " + self.token

        response = requests.request("GET", url, data=payload, headers=self.headers)
        if response.ok:
            connection = response.json()["data"]["connection"]
            value = connection["glucoseMeasurement"]["Value"]
            # patient_range_high = round(connection["targetHigh"] / 18, 1)
            # patient_range_low = round(connection["targetLow"] / 18, 1)

            return (value, connection["glucoseMeasurement"]["TrendArrow"])

    def get_trend_arrow(self, trend: int):
        return {
            1: "⬇️",
            2: "↘️",
            3: "➡️",
            4: "↗️",
            5: "⬆️"
        }.get(trend, "")

    def main(self):
        (
        value, 
        trend, 
        ) = self.get_measurment()
        trend_arrow = self.get_trend_arrow(trend)
        return (value, trend_arrow, datetime.now())
    
    def append_dict_to_json(self, new_data):
        with open("glucose_data.json", 'r', encoding='utf-8') as file:
            old_data = list(json.loads(file.read()))
            
        old_data.append(new_data)

        with open("glucose_data.json", 'w', encoding='utf-8') as fh:
            fh.write(json.dumps(old_data, ensure_ascii=False, indent=4))

    def return_data_for_app(self):
        data = self.main()

        value = data[0]
        trend = data[1]
        current_time = data[2]

        d = {
            "value": value,
            "trend": trend, 
            "current_time": f"{current_time.hour}:{current_time.minute} {current_time.day}-{current_time.month}"
        }

        self.append_dict_to_json(d)
        # return (value, trend, f"{current_time.hour}:{current_time.minute} {current_time.day}-{current_time.month}")
        
#f"{current_time.hour}:{current_time.minute} {current_time.day}-{current_time.month}",



# async def run_and_save_main():
#     while True:
#         data = Libre_link_up.main()

#         value = data[0]
#         trend = data[1]
#         current_time = data[2]

#         create_html(value, trend, f"{current_time.hour}:{current_time.minute} {current_time.day}-{current_time.month}", current_time)
        
#         print("DONE, sleeping for 60 sec")
#         await asyncio.sleep(180)


# def create_html(value, trend, current_time, tmp):
#     global day1
    
#     with open("glucose_levels.html", "r", encoding='utf-8') as file:
#         html_content = file.read()
    
#     if value > 13.5:
#         bg_class = "bg-orange"
#     elif 10 <= value <= 13.5:
#         bg_class = "bg-yellow"
#     elif 4 <= value < 10:
#         bg_class = "bg-green"
#     else:
#         bg_class = "bg-red"
    
#     main_s = 1740
#     if int(datetime.now().day) != int(day1):
#         html_content_n = html_content[:main_s] + f"""
#     <div class="item bg-blue">
#     <b class="item-line">{tmp.day}-{tmp.month}</b>
#     </div>
#     """ + html_content[main_s:]



#         html_content_n = html_content_n[:main_s] + f"""
#         <div class="item {bg_class}">
#             <div class="value"><b>{value} <span>{trend}</b><span></div>
#             <div class="time">{current_time}</div>
#         </div>
#         """ + html_content_n[main_s:]

#         day1 = int(datetime.now().day)

#     else:
#         html_content_n = html_content[:main_s] + f"""
#         <div class="item {bg_class}">
#             <div class="value"><b>{value} <span>{trend}</b><span></div>
#             <div class="time">{current_time}</div>
#         </div>
#         """ + html_content[main_s:]
    

#     with open("glucose_levels.html", "w+", encoding='utf-8') as file:
#         file.write(html_content_n)



# @main_router.message(Command("start"))
# async def send_welcome(message: types.Message):

    
#     # await message.reply(FSInputFile('glucose_levels.html'), parse_mode=ParseMode.HTML)
#     await message.answer_document(FSInputFile('glucose_levels.html'))


# async def main():
#     loop = asyncio.get_event_loop()
#     loop.create_task(run_and_save_main())
#     dp.include_router(main_router)
#     await dp.start_polling(bot)
    

        

# if __name__ == "__main__":
#     Libre_link_up = LibreLinkUp(TOKEN, PATIENT_ID, COUNTRY, HEADERS)
#     print(return_data_for_app())
# #     asyncio.run(main())

