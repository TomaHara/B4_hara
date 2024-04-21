import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import csv
from pathlib import Path
import os

def download_data(data):
    option = Options()
    download_path = "C:\\Users\\透真\\OuraRing\\sleep_data\\睡眠データ保存"
    Path(download_path).mkdir()
    option.add_experimental_option("prefs", {"download.default_directory": download_path})

    driver = webdriver.Chrome(options=option)

    #Oura on the webのサインイン画面へ移動
    driver.get("https://cloud.ouraring.com/user/sign-in")
    time.sleep(2)

    #ログイン処理
    for login_info in data:
        print(login_info[0],login_info[1])
        e_mail = driver.find_element(by=By.NAME, value="email")
        password = driver.find_element(by=By.NAME, value="password")
        e_mail.clear()
        password.clear()
        e_mail.send_keys(login_info[0])
        password.send_keys(login_info[1])
        driver.find_element(by=By.XPATH, value="/html/body/div/div/div[1]/div/main/div/form/div[3]/button").click()
        time.sleep(2)
        driver.get("https://cloud.ouraring.com/profile")
        time.sleep(2)
        #ダウンロード
        driver.get("https://cloud.ouraring.com/account/export/sleep/csv")
        time.sleep(2)
        #ログアウト
        driver.get("https://cloud.ouraring.com/v2/account/logout")
        time.sleep(2)

    driver.quit()

with open("C:\\Users\\透真\\OuraRing\\sleep_data\\実験参加者リスト\\participants.csv", "r", encoding="utf-8") as csvfile:
    reader = csv.reader(csvfile)
    user_data = [row for row in reader]

#download_data(user_data)

#ダウンロードしたファイルを更新時間でソート
download_file = sorted(Path("C:\\Users\\透真\\OuraRing\\sleep_data\\睡眠データ保存").glob("*"), key=os.path.getatime)
#omu-user○○○の形式にリネーム
for name, file in zip(user_data, download_file):
    newname = Path(file).with_name("omu-user"+name[1][-3:]+".csv")
    print(newname)
    file.rename(newname)







