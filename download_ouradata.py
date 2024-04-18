import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import csv
from pathlib import Path
import os

#csvファイルからユーザのe-mailとpasswordのリストを取得する関数
def read_user_data(path):
    with open(path, "r", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        user_data = [row for row in reader]
    return user_data

#データをダウンロードする関数
def download_data(data,path):
    option = Options()
    Path(path).mkdir()
    option.add_experimental_option("prefs", {"download.default_directory": path})

    driver = webdriver.Chrome(options=option)

    #Oura on the webのサインイン画面へ移動
    driver.get("https://cloud.ouraring.com/user/sign-in")
    time.sleep(2)

    #ログイン処理
    for login_info in data:
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

    

download_path = "~~~~~~~~~~~" #ダウンロード先のpath
user_info_path = "~~~~~~~~~~" #ユーザのe-mailとpasswordをまとめたcsvファイルのpath

user_data = read_user_data(user_info_path)

download_data(user_data,download_path)

#ダウンロードしたファイルを更新時間でソート
download_files = sorted(Path(download_path).glob("*"), key=os.path.getatime)
#omu-userXXXの形式にリネーム
for data, file in zip(user_data, download_files):
    newname = Path(file).with_name("omu-user"+data[1][-3:]+".csv")
    file.rename(newname)
