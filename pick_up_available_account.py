import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import csv
from pathlib import Path
import sys

#csvファイルからユーザのe-mailとpasswordのリストを取得する関数
def read_user_data(path):
    try:
        with open(path, "r", encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile)
            user_data = [row for row in reader]
            return user_data
    except FileNotFoundError:
        sys.exit("File not found")

#生きているアカウントをまとめる関数
def pick_up_available_account(user_info_path, output_path):

    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    #Oura on the webのサインイン画面へ移動
    driver.get("https://cloud.ouraring.com/user/sign-in")
    time.sleep(5)

    user_data = read_user_data(user_info_path)
    available_account_list = [['account_mailadress', 'password']]

    #ログイン処理
    for login_info in user_data:
        e_mail = driver.find_element(by=By.NAME, value="email")
        password = driver.find_element(by=By.NAME, value="password")
        e_mail.clear()
        password.clear()
        e_mail.send_keys(login_info['account_mailadress'])
        password.send_keys(login_info['password'])
        driver.find_element(by=By.XPATH, value="/html/body/div/div/div[1]/div/main/div/form/div[3]/button").click()
        time.sleep(5)
        # ログインが失敗した場合は処理をスキップ
        if "error=invalid_credentials" in driver.current_url:
            print("Login failed for:", login_info['account_mailadress'])
            driver.get("https://cloud.ouraring.com/user/sign-in")
            time.sleep(5)
            continue

        driver.get("https://cloud.ouraring.com/v2/account/logout")
        time.sleep(5)
        available_account_list.append([login_info['account_mailadress'], login_info['password']])
    driver.quit()

    with open(output_path, 'w', newline="") as f:
        writer = csv.writer(f)
        writer.writerows(available_account_list)


output_path = "~~~~~~~~~~~~~~~"   #available_account.csvを出力するpath
user_info_path = "~~~~~~~~~~~~" #ユーザのe-mailとpasswordをまとめたcsvファイルのpath

pick_up_available_account(user_info_path, output_path)