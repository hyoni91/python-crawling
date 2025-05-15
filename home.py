from flask import Flask, render_template
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

app = Flask(__name__)

@app.route('/')
def home() : 
    # Initialize the Chrome WebDriver (실제로 창이 열림)
    driver = webdriver.Chrome()
     # Open the target URL
    page = 1
    bukken_list = []

    # 브라우저 창을 열고싶지 않다면 --headless 옵션을 추가
    # options = webdriver.ChromeOptions()
    # options.add_argument('--headless')
    # driver = webdriver.Chrome(options=options)

    while True:
        url = f"https://www.e-uchina.net/jukyo/nagoshi?madori=2LDK,3LDK&page={page}&perPage=50&sort=update"
        driver.get(url)
        time.sleep(5)


        # 요소 찾고 텍스트 추출
        headers = [header.text for header in driver.find_elements(By.CLASS_NAME, "head-content")]
        prices = [price.text for price in driver.find_elements(By.CLASS_NAME, "bukken-data-price")]
        madoris = [madori.text for madori in driver.find_elements(By.CLASS_NAME, "bukken-data-madori")]
        links = [link.get_attribute('href') for link in driver.find_elements(By.CSS_SELECTOR, ".button.detail-button")]

         # 데이터 묶기
        for header, price, madori, link in zip(headers, prices, madoris, links):
            bukken_list.append({
                "header": header[:10],
                "price": price,
                "madori": madori,
                "link": link,
            })

        bukken_list = list({
            (bukken['header'], bukken['price'], bukken['madori']): 
            bukken for bukken in bukken_list}.values())

        try:
            next_button = driver.find_element(By.CLASS_NAME, "pagination-next")
            if next_button.is_enabled():
                page += 1
            else:
                break  
        except Exception as e:
            print(f"Next button not found or not enabled: {e}")
            # 페이지가 더 이상 없으면 루프 종료
            break 

    # Close the WebDriver after scraping
    driver.quit()

    return render_template("listings.html", bukken_list=bukken_list)

if __name__ == '__main__':
    app.run(debug=True)