import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from os.path import exists
from datetime import date

filename = "rl_stats.csv"


def initialise_csv(fname):
    with open(fname, 'w') as f:
        csv_headers = f"DATE,{'MODE,RANK,MMR,' * 8}\n"
        f.write(csv_headers)
        print(f'{fname} created.')


if not exists(filename):
    initialise_csv(filename)
else:
    print(f"{filename} found")

data = ""  # data to write to the csv

with open(filename, 'r+') as f:
    lines = f.readlines()
    last_line = lines[-1]  # read last record in file
    last_date = last_line.split(",")[0]  # date of last record
    today = str(date.today())

    if today != last_date:  # only write to csv if new day

        RL_TRACKER_URL = 'https://rocketleague.tracker.network/rocket-league/profile/steam/76561198149179287/overview'
        user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36"

        # selenium
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--incognito')
        options.add_argument('--headless')
        options.add_argument(f"user-agent={user_agent}")
        options.add_argument('log-level=3')
        options.add_experimental_option('excludeSwitches', ['enable-logging'])

        driver = webdriver.Chrome(
            service=Service('C:\Program Files (x86)\chromedriver.exe'),
            options=options)
        driver.get(RL_TRACKER_URL)
        time.sleep(4)  # let table element load
        source = driver.page_source

        # beautiful soup
        soup = BeautifulSoup(source, 'html.parser')

        table_rows = soup.find("tbody").children
        if table_rows != None:

            for row in table_rows:

                # playlist name (Ranked Doubles 2v2)
                playlist = row.find("div", {"class": "playlist"}).text.strip()

                if playlist != "Un-Ranked":

                    # rank name (Champion II Division I)
                    rank = row.find("div", {"class": "rank"}).text

                    # mmr (1194)
                    mmr_raw = row.find("div", {"class": "value"}).text
                    mmr = mmr_raw.replace(",", "")

                    print(f'Found {playlist} data')
                    data += f'{playlist},{rank},{mmr},'

            last_record_elmnts = last_line.split(",")[1::]  # remove date
            last_record = ",".join(last_record_elmnts)  # rejoin as string

            if last_record.strip() != data.strip():
                print(f"Writing data to {filename}.")
                f.write(f'{str(date.today())},{data}')
                f.write('\n')
            else:
                print("Data hasn't changed since last record.")
        else:
            print("Table element couldn't be found")

        print("Closing ChromeDriver")
        driver.close()
        driver.quit()
    else:
        print(f"Error: Data already found for today.")

print("Done")
print("-" * 40)
