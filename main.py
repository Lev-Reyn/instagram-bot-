from selenium import webdriver
import time
import pickle
from selenium.webdriver.common.keys import Keys
import random

options = webdriver.ChromeOptions()
options.add_argument(
    'user-agent=Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36')
options.add_argument('disable-blink-features=AutomationControlled')

my_login = 'lv_rey'
my_password = 'LEV60605010Ru'


def instagram_bot(heshteg):
    driver = webdriver.Chrome(
        executable_path='/Users/levreyn/Yandex.Disk.localized/python/selenium/driver/chromedriver',
        options=options)
    try:
        driver.get(url='https://www.instagram.com/')

        # login_input = driver.find_element('name', 'username')
        # login_input.send_keys(my_login)
        # time.sleep(1)
        #
        # password = driver.find_element('name', 'password')
        # password.send_keys(my_password)
        # password.send_keys(Keys.ENTER)
        # driver.implicitly_wait(10)
        # time.sleep(5)
        # pickle.dump(driver.get_cookies(), open(f'{my_login}_cookies', 'wb'))
        for cookie in pickle.load(open(f'{my_login}_cookies', 'rb')):
            driver.add_cookie(cookie)
        time.sleep(1)
        driver.refresh()
        driver.implicitly_wait(10)

        driver.get(url=f'https://www.instagram.com/explore/tags/{heshteg}/')

        for scroll in range(1, 10):
            driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            time.sleep(random.randrange(5, 10))

        posts = driver.find_elements_by_tag_name('a')
        posts_urls = []
        for post in posts:
            link_post = post.get_attribute('href')
            if '/p/' in link_post:
                posts_urls.append(link_post)
        print(posts_urls)

        for url_post in posts_urls:
            try:
                driver.get(url=url_post)
                time.sleep(5)
                button_like = driver.find_element_by_xpath('/html/body/div[1]/section/main/div/div[1]/article/div[3]/section[1]/span[1]/button').click()
                time.sleep(2)
                break
            except Exception as ex:
                print(ex)
        driver.close()
        driver.quit()



        time.sleep(200)

    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()


if __name__ == '__main__':
    instagram_bot('серфинг')
