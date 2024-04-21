import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import csv
from pathlib import Path
import os
import sys
import pandas as pd

#csvファイルからユーザのe-mailとpasswordのリストを取得する関数
def read_user_data(path):
    
    try:
        with open(path, "r", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            user_data = [row for row in reader]
            return user_data
    except FileNotFoundError:
        sys.exit("File not found")

#データをダウンロードする関数
def download_data(user_info_path, download_path):
    option = Options()
    try:
        Path(download_path).mkdir()
    except FileExistsError:
        sys.exit("File Exists Error")
    option.add_experimental_option("prefs", {"download.default_directory": download_path})

    driver = webdriver.Chrome(options=option)
    driver.implicitly_wait(10)

    #Oura on the webのサインイン画面へ移動
    driver.get("https://cloud.ouraring.com/user/sign-in")
    time.sleep(5)

    user_data = read_user_data(user_info_path)

    #ログイン処理
    for login_info in user_data:
        e_mail = driver.find_element(by=By.NAME, value="email")
        password = driver.find_element(by=By.NAME, value="password")
        e_mail.clear()
        password.clear()
        e_mail.send_keys(login_info['account_mailadress'])
        password.send_keys(login_info['password'])
        driver.find_element(by=By.XPATH, value="/html/body/div/div/div[1]/div/main/div/form/div[3]/button").click()
        time.sleep(2)
        #ログインに失敗した場合、処理をスキップ
        if "error=invalid_credentials" in driver.current_url:
            print("Login failed for:", login_info['account_mailadress'])
            driver.get("https://cloud.ouraring.com/user/sign-in")
            time.sleep(2)
            continue
        driver.get("https://cloud.ouraring.com/profile")
        time.sleep(2)
        #ダウンロード
        driver.get("https://cloud.ouraring.com/account/export/sleep/csv")
        time.sleep(2)
        #ログアウト
        driver.get("https://cloud.ouraring.com/v2/account/logout")
        time.sleep(2)
    driver.quit()

    #ダウンロードしたファイルを更新時間でソート
    files = sorted(Path(download_path).glob("*"), key=os.path.getatime)
    #omu-userXXXの形式にリネーム
    for data, file in zip(user_data, files):
        newname = Path(file).with_name("omu-user"+data['password'][-3:]+".csv")
        file.rename(newname)


download_path = "~~~~~~~~~~~~~~~~" #ダウンロード先のpath
user_info_path = "~~~~~~~~~~~~~~~" #ユーザのe-mailとpasswordをまとめたcsvファイルのpath

download_data(user_info_path,download_path)
