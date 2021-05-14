from selenium import webdriver
import time
import pickle
from selenium.webdriver.common.keys import Keys
import random
from selenium.common.exceptions import NoSuchElementException
import json
from bs4 import BeautifulSoup
from colorama import Fore, Style
import requests
import os.path
from different_ussers import ussers_setting_dict


class InstagramBot:
    __inf_src_img_1 = 0
    __inf_src_img_2 = 0
    __inf_src_img_3 = 0
    __inf_scr_img_lst = []

    def __init__(self, username, password, window=None):
        self.username = username
        self.password = password
        options = webdriver.ChromeOptions()
        if window:
            options.add_argument(f'--window-size={window}')
        options.add_argument(
            'user-agent=Mozilla/5.0 (Windows NT 6.1; rv:80.0) Gecko/20100101 Firefox/80.0')
        options.add_argument('disable-blink-features=AutomationControlled')
        self.driver = webdriver.Chrome(
            executable_path='/Users/levreyn/Yandex.Disk.localized/python/selenium/driver/chromedriver',
            options=options)

    #
    #
    #
    #
    #
    #
    #
    #
    # закрываем браузер
    def close_browser(self):
        self.driver.close()
        self.driver.quit()

    #
    #
    #
    #
    #
    #
    #
    #
    # войти в аккаунт
    def login(self):

        driver = self.driver
        driver.get(url='https://www.instagram.com/')
        driver.implicitly_wait(10)
        login_input = driver.find_element('name', 'username')
        login_input.send_keys(self.username)
        time.sleep(1)

        password = driver.find_element('name', 'password')
        password.send_keys(self.password)
        password.send_keys(Keys.ENTER)
        driver.implicitly_wait(10)
        time.sleep(5)
        pickle.dump(driver.get_cookies(), open(f'{self.username}_cookies', 'wb'))

    #
    #
    #
    #
    #
    #
    #
    #
    # войти в аккаунт с помощью куки файлов
    def login_cookies(self):
        driver = self.driver
        driver.get(url='https://www.instagram.com/')
        for cookie in pickle.load(open(f'{self.username}_cookies', 'rb')):
            driver.add_cookie(cookie)
        time.sleep(1)
        driver.refresh()
        driver.implicitly_wait(10)

    #
    #
    #
    #
    #
    #
    #
    #
    # лайкаем фотграфии по хештегу
    def like_photo_by_hesteg(self, heshteg):
        driver = self.driver
        driver.get(url=f'https://www.instagram.com/explore/tags/{heshteg}/')

        for scroll in range(1, 3):
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
                driver.implicitly_wait(10)
                button_like = driver.find_element_by_xpath(
                    '/html/body/div[1]/section/main/div/div[1]/article/div[3]/section[1]/span[1]/button').click()
                time.sleep(random.randrange(80, 100))
            except Exception as ex:
                print(ex)
                self.close_browser()
        self.close_browser()

    #
    #
    #
    #
    #
    #
    #
    #
    # проверка существует ли элемент на странице, проверяем по xpath
    # то есть туда зауидываем не ссылку, а xpath
    def xpath_exists(self, xpath_url):
        driver = self.driver
        try:
            driver.find_element_by_xpath(xpath_url)
            exist = True
        except NoSuchElementException:
            exist = False
        return exist

    #
    #
    #
    #
    #
    #
    #
    #
    # ставим лайк на данный пост
    def put_exacttly_like(self, userpost):
        driver = self.driver
        driver.get(userpost)
        time.sleep(4)

        wrong_post = '//*[@id="react-root"]/section/main/div/h2'

        if self.xpath_exists(wrong_post):
            print('Такого поста нет, проверьте URL')
            self.close_browser()
        else:
            print('пост успешно найден, ставим лайк')
            button_like = driver.find_element_by_xpath(
                '/html/body/div[1]/section/main/div/div[1]/article/div[3]/section[1]/span[1]/button').click()
            print(f'лайк поставлен на {userpost}')
            time.sleep(2)

    #
    #
    #
    #
    #
    #
    #
    #
    # собираем ccылки на посты
    def get_links_posts(self, userpage, username):

        driver = self.driver
        try:
            post_count = int(driver.find_element_by_xpath(
                '/html/body/div[1]/section/main/div/header/section/ul/li[1]/span/span').text)
            print(post_count)
            links_lst = []
            count_scroll = int(post_count / 12)
            if count_scroll == 0:
                count_scroll = 1
            print(f'начинаем скролинг {count_scroll} раз')
            for scroll in range(count_scroll):
                time.sleep(random.randrange(2, 3))
                driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
                html = driver.page_source
                soup = BeautifulSoup(html, 'lxml')
                posts = soup.find_all('a')
                for post in posts:
                    if '/p/' in post['href']:
                        links_lst.append(
                            'https://www.instagram.com' + post['href']
                        )
            links_lst = set(links_lst)
            links_lst = list(links_lst)
            if os.path.exists(f'users_data/{username}_directory') == False:
                os.mkdir(f'users_data/{username}_directory')

            with open(f'users_data/{username}_directory/{username}_links_on_posts.json', 'w') as file:
                json.dump(links_lst, file, indent=2, ensure_ascii=False)
        except Exception as ex:
            print(Fore.RED + 'ошибка вышла в get_links_posts' + Style.RESET_ALL, ex)

    #
    #
    #
    #
    #
    #
    #
    #
    # не работает, должна скачивать видосы по ссылке
    def save_one_video(self, url_video, username):
        HEADERS = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36',
            'accept': '*/*'}
        r = requests.get(url_video, headers=HEADERS, stream=True)
        if os.path.exists(f'users_data/{username}_directory/media') == False:
            os.mkdir(f'users_data/{username}_directory/media')
        if os.path.exists(f'users_data/{username}_directory/media/video') == False:
            os.mkdir(f'users_data/{username}_directory/media/video')
        name_video = url_video.split('/')[-1]
        with open(f'users_data/{username}_directory/media/photo/{name_video}.mp4', 'wb') as file:
            for chunk in r.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    file.write(chunk)

    #
    #
    #
    #
    #
    #
    #
    #
    # скачивает фотографию по ссылке
    def save_one_photo(self, url_photo, username):
        HEADERS = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36',
            'accept': '*/*'}
        r = requests.get(url_photo, headers=HEADERS)
        if os.path.exists(f'users_data/{username}_directory/media') == False:
            os.mkdir(f'users_data/{username}_directory/media')
        if os.path.exists(f'users_data/{username}_directory/media/photo') == False:
            os.mkdir(f'users_data/{username}_directory/media/photo')
        name_photo = url_photo.split('.jpg')[0].split('/')[-1]
        with open(f'users_data/{username}_directory/media/photo/{name_photo}.jpg', 'wb') as file:
            file.write(r.content)

    #
    #
    #
    #
    #
    #
    #
    #
    # скачивает фотографии по ссылкам из json (которые уже собраны)
    def save_photos_from_directory(self, username):
        with open(f'users_data/{username}_directory/{username}_lst_links_photo.json') as file:
            lst_links_photo = json.load(file)
            count = 0
            for url_photo in lst_links_photo:
                self.save_one_photo(url_photo=url_photo, username=username)
                count += 1
                print(f'скаченно {count} фотографий из {len(lst_links_photo)} а точнее эта {url_photo}')

    #
    #
    #
    #
    #
    #
    #
    #
    # скачиваем фотографии  по ссылкам и скачивание видео по ссылкам в разработке
    def save_photo_and_video(self, userpage):
        print('делаем проверкку для img_src')
        self.proverka_img_src()
        print('закончили проверкку для img_src')
        driver = self.driver
        driver.get(url=userpage)
        driver.implicitly_wait(10)
        wrong_post = '//*[@id="react-root"]/section/main/div/h2'

        if self.xpath_exists(wrong_post):
            print('Такого пользователя нет, проверьте URL')
            self.close_browser()
        try:
            if self.xpath_exists('/html/body/div[1]/section/main/div/header/section/div[1]/h2'):
                username = driver.find_element_by_xpath(
                    '/html/body/div[1]/section/main/div/header/section/div[1]/h2').text
            elif self.xpath_exists('/html/body/div[1]/section/main/div/header/section/div[1]/h1'):
                username = driver.find_element_by_xpath(
                    '/html/body/div[1]/section/main/div/header/section/div[1]/h1').text

            self.get_links_posts(userpage=userpage, username=username)
            print(username, 'нашли...')
            with open(f'users_data/{username}_directory/{username}_links_on_posts.json') as file:
                links_lst = json.load(file)
            lst_links_photo = []
            lst_links_video = []
            print(links_lst)
            count_okey = 0
            for url_post in links_lst:
                driver.get(url=url_post)
                driver.implicitly_wait(10)

                img_src = '/html/body/div[1]/section/main/div/div[1]/article/div[2]/div/div[1]/div[2]/div/div/div/ul/li[2]/div/div/div/div[1]/div[1]/img'
                img_src_2 = '/html/body/div[1]/section/main/div/div[1]/article/div[2]/div/div/div[1]/img'
                img_src_3 = '/html/body/div[1]/section/main/div/div[1]/article/div[2]/div/div[1]/div[2]/div/div/div/ul/li[2]/div/div/div/div[1]/img'
                video_src = '/html/body/div[1]/section/main/div/div[1]/article/div[2]/div/div/div[1]/div/div/video'
                count_okey += 1
                if self.xpath_exists(img_src):
                    link_photo = driver.find_element_by_xpath(img_src).get_attribute('src')
                    lst_links_photo.append(link_photo)
                    InstagramBot.__inf_src_img_1 += 1
                    print(f'собрали ссылку с поста {url_post} собранно {count_okey} из {len(links_lst)}')
                elif self.xpath_exists(img_src_2):
                    link_photo = driver.find_element_by_xpath(img_src_2).get_attribute('src')
                    lst_links_photo.append(link_photo)
                    print(f'собрали ссылку с поста {url_post} собранно {count_okey} из {len(links_lst)}')
                    InstagramBot.__inf_src_img_2 += 1
                elif self.xpath_exists(img_src_3):
                    link_photo = driver.find_element_by_xpath(img_src_3).get_attribute('src')
                    lst_links_photo.append(link_photo)
                    print(f'собрали ссылку с поста {url_post} собранно {count_okey} из {len(links_lst)}')
                    InstagramBot.__inf_src_img_3 += 1
                elif self.xpath_exists(video_src):
                    link_video = driver.find_element_by_xpath(video_src).get_attribute('src')
                    lst_links_video.append(link_video)
                    print(f'собрали ссылку с поста видео {url_post} собранно {count_okey} из {len(links_lst)}')
                else:
                    print(Fore.GREEN + f'что-то пошло не по плану в посте по ссылке {url_post}' + Style.RESET_ALL)

            print(lst_links_photo)
            # закинули все ссылки фотографий в json, что бы если что случиться, то они есть
            with open(f'users_data/{username}_directory/{username}_lst_links_photo.json', 'w') as file:
                json.dump(lst_links_photo, file, indent=2, ensure_ascii=False)

            # идём по ссылкам этим и скачиваем фотографии
            for url_photo in lst_links_photo:
                self.save_one_photo(url_photo=url_photo, username=username)

            print(lst_links_video)
            # закинули все ссылки видосов в json, что бы если что случиться, то они есть
            with open(f'users_data/{username}_directory/{username}_lst_links_video.json', 'w') as file:
                json.dump(lst_links_video, file, indent=2, ensure_ascii=False)

            self.proverka_save_img_src()

            self.close_browser()



        except Exception as ex:
            print(Fore.CYAN + 'ошибка в методе save_photo_and_video' + Style.RESET_ALL, ex)
            self.close_browser()

    #
    #
    #
    #
    #
    #
    #
    #
    # ставим лайки по ссылке на аккаунт пользователя
    def put_many_like(self, userpage):
        driver = self.driver
        driver.get(url=userpage)
        driver.implicitly_wait(10)
        wrong_post = '//*[@id="react-root"]/section/main/div/h2'

        if self.xpath_exists(wrong_post):
            print('Такого пользователя нет, проверьте URL')
            self.close_browser()
        else:
            try:
                username = driver.find_element_by_xpath(
                    '/html/body/div[1]/section/main/div/header/section/div[1]/h2').text
                print(f'пользователь {username} успешно найден, собираем посты')

                self.get_links_posts(userpage=userpage, username=username)
                with open(f'users_data/{username}.json') as file:
                    links_lst = json.load(file)
                for url_post in links_lst:
                    self.put_exacttly_like(url_post)

            except Exception as ex:
                print(ex)
            finally:
                self.close_browser()

    #
    #
    #
    #
    #
    #
    #
    #
    # функция для анализа программы, а точнее функции  save_photo_and_video, для того что бы ускорить процесс
    def proverka_img_src(self):

        InstagramBot.__inf_scr_img_lst.append(InstagramBot.__inf_src_img_1)
        InstagramBot.__inf_scr_img_lst.append(InstagramBot.__inf_src_img_2)
        InstagramBot.__inf_scr_img_lst.append(InstagramBot.__inf_src_img_3)

        if os.path.exists('inf_src_img.json') == False:
            with open('inf_src_img.json', 'w') as file:
                json.dump(InstagramBot.__inf_scr_img_lst, file, indent=2, ensure_ascii=False)
        else:
            with open('inf_src_img.json') as file:
                InstagramBot.__inf_scr_img_lst = json.load(file)
                InstagramBot.__inf_src_img_1 = InstagramBot.__inf_scr_img_lst[0]
                InstagramBot.__inf_src_img_2 = InstagramBot.__inf_scr_img_lst[1]
                InstagramBot.__inf_src_img_3 = InstagramBot.__inf_scr_img_lst[2]

    #
    #
    #
    #
    #
    #
    #
    #
    # функция для анализа программы, а точнее функции  save_photo_and_video, для того что бы ускорить процесс
    def proverka_save_img_src(self):
        InstagramBot.__inf_scr_img_lst = []
        InstagramBot.__inf_scr_img_lst.append(InstagramBot.__inf_src_img_1)
        InstagramBot.__inf_scr_img_lst.append(InstagramBot.__inf_src_img_2)
        InstagramBot.__inf_scr_img_lst.append(InstagramBot.__inf_src_img_3)

        with open('inf_src_img.json', 'w') as file:
            json.dump(InstagramBot.__inf_scr_img_lst, file, indent=2, ensure_ascii=False)

    #
    #
    #
    #
    #
    #
    #
    #
    # сбор ссылок на подписчиков и сохранение в json, так же ставит лайки
    # принимает на вход ссылку на пользователя
    # если в only_get_followers передать значенеи True, то только сохранит ссылки на подписчиков, и
    # не будет раставлять лайки
    def get_all_subscribers(self, userpage, only_get_followers=False):
        driver = self.driver
        driver.get(url=userpage)
        driver.implicitly_wait(10)
        wrong_post = '//*[@id="react-root"]/section/main/div/h2'

        if self.xpath_exists(wrong_post):
            print('Такого пользователя нет, проверьте URL')
            self.close_browser()

        else:
            try:

                count_followers = driver.find_element_by_xpath(
                    '/html/body/div[1]/section/main/div/header/section/ul/li[2]/a/span').get_attribute('title')
                count_followers = count_followers.replace(' ', '')
                # print(f'нашли колличество подписчиков, их {count_followers}')
                if self.xpath_exists('/html/body/div[1]/section/main/div/header/section/div[1]/h1'):
                    user_name = driver.find_element_by_xpath(
                        '/html/body/div[1]/section/main/div/header/section/div[1]/h1').text
                elif self.xpath_exists('/html/body/div[1]/section/main/div/header/section/div[1]/h2'):
                    user_name = driver.find_element_by_xpath(
                        '/html/body/div[1]/section/main/div/header/section/div[1]/h2').text

                print(f'{count_followers} подписчиков у пользователя {user_name}')
                button_folowers = driver.find_element_by_xpath(
                    '/html/body/div[1]/section/main/div/header/section/ul/li[2]/a').click()
                driver.implicitly_wait(10)
                window_with_followers = driver.find_element_by_xpath('/html/body/div[5]/div/div/div[2]')

                for scroll in range(int(count_followers) // 12 + 1):
                    driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', window_with_followers)
                    print(f'скрол {scroll}')
                    time.sleep((random.randrange(1, 3)))
                all_followers_code_lst = window_with_followers.find_elements_by_tag_name('li')
                followers_urls_lst = []
                for follower in all_followers_code_lst:
                    followers_urls_lst.append(follower.find_element_by_tag_name('a').get_attribute('href'))
                print(f'сохраняем данные о сылках на подписчиков в  json')
                if os.path.exists(f'users_data/{user_name}') == False:
                    os.mkdir(f'users_data/{user_name}')
                with open(f'users_data/{user_name}/followers_lst.json', 'w') as file:
                    json.dump(followers_urls_lst, file, indent=2, ensure_ascii=False)
                print('сохранили в Json')
                with open(f'users_data/{user_name}/followers_lst.json') as file:
                    self.followers_urls_lst = json.load(file)
                if only_get_followers == True:
                    print('зашли в only_get_followers ')
                    return self.followers_urls_lst
                self.count_men = 0
                for url_men in self.followers_urls_lst:
                    self.count_men += 1
                    self.follow_on_the_men(url_men)
                    time.sleep(random.randrange(120, 180))



            except Exception as ex:
                print(Fore.RED + str(ex) + Style.RESET_ALL)
            finally:
                self.close_browser()

    #
    #
    #
    #
    #
    #
    #
    #
    # подписываемся на аккаунт по ссылке
    def follow_on_the_men(self, url):
        driver = self.driver
        driver.get(url)
        driver.implicitly_wait(10)
        if self.xpath_exists('/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/a'):
            return None
        elif self.xpath_exists(
                '/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/div/div[2]/div/span/span[1]/button'):
            return False
        elif self.xpath_exists(
                '/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/div/div/div/span/span[1]/button'):
            button_follow = driver.find_element_by_xpath(
                '/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/div/div/div/span/span[1]/button').click()
            print(f'подписались на открытый аккаунт {url} это {self.count_men} из {len(self.followers_urls_lst)}')

        # если приватный аккаунт
        elif self.xpath_exists('/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/div/div/button'):
            button_follow = driver.find_element_by_xpath(
                '/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/div/div/button').click()
            print(f'подписались на приватный аккаунт {url} это {self.count_men} из {len(self.followers_urls_lst)}')
        else:
            print(Fore.LIGHTRED_EX + f'опа, не нашли кнопки подписаться на аккаунте {url}' + Style.RESET_ALL)

    #
    #
    #
    #
    #
    #
    #
    #
    # отправляем сообщение пользлвателю по ссылке на пользователя
    # можно добавить фотографию, просто закидываем полный путь до фотографии в
    # аргумент img_path
    def send_a_message(self, userpage, text_message='тестовое сообщение', img_path=None):
        try:
            driver = self.driver
            driver.get(userpage)
            if self.xpath_exists(
                    '/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/div/div[1]/div/button'):
                button_message = driver.find_element_by_xpath(
                    '/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/div/div[1]/div/button').click()
                print('кликнули на отправку сообщения')
                driver.implicitly_wait(10)
                # time.sleep(120)
            else:
                print('blet, the send message button was not found')
                return None
            # если есть окно, которое спрашивает про уведомленя, тогда нажимаем на кнопку "не сечас"
            if self.xpath_exists('/html/body/div[5]/div/div/div'):
                print('window about notification found')
                # time.sleep(120)
                # ищем кнопку "не сейчас"  и нажимаем её
                button_not_now_notifications = driver.find_element_by_xpath(
                    '/html/body/div[5]/div/div/div/div[3]/button[2]')
                button_not_now_notifications.click()
                driver.implicitly_wait(10)

            input_text = driver.find_element_by_xpath(
                '/html/body/div[1]/section/div/div[2]/div/div/div[2]/div[2]/div/div[2]/div/div/div[2]/textarea')
            # вставляем текс в поле ввода сообщения
            input_text.send_keys(text_message)
            button_send = driver.find_element_by_xpath(
                '/html/body/div[1]/section/div/div[2]/div/div/div[2]/div[2]/div/div[2]/div/div/div[3]/button').click()
            username = userpage.split('/')[-2]
            print(f'сообщение пользоватерю {username} отправленно')
            if img_path:
                input_img = driver.find_element_by_xpath(
                    '/html/body/div[1]/section/div/div[2]/div/div/div[2]/div[2]/div/div[2]/div/div/form/input')
                input_img.send_keys(img_path)
                print(f'фотография пользоватерю {username} отправленно')
                time.sleep(3)


        except Exception as ex:
            print(f'ошибка в send_a_message по url: {userpage} {ex}')

    #
    #
    #
    #
    #
    #
    #
    #
    # массовая рассылка сообщений, принимает на вход список с ссылками по которым отправлять сообщения
    def mass_malling_of_messages(self, lst_with_links_pages):
        for userpage in lst_with_links_pages[1:50]:
            time.sleep(random.randrange(1, 4))
            self.send_a_message(userpage=userpage,
                                text_message='привет, это тестовый бот с рассылкой сообщений, так что не парся и не отвечай на данное сообщение')
            time.sleep(random.randrange(150, 200))
        self.close_browser()

    #
    #
    #
    #
    #
    #
    #
    #
    # получаем ссылки на мои подписчиков и закидываем их в 'my_subscriptions.json'
    # если указать take_from_json = True, то берёт ссылки из файла
    def get_urls_my_subscriptions(self, take_from_json=None):
        #  на данный момент будет просто брать подписчиков с аккаунта  lv_rey, потом доработаю
        if take_from_json:
            with open('my_subscriptions.json') as file:
                self.urls_my_subscriptions_lst = json.load(file)
                return self.urls_my_subscriptions_lst
        try:
            driver = self.driver
            driver.get('https://www.instagram.com/lv_rey/')
            count_my_subscriptions = driver.find_element_by_xpath(
                '/html/body/div[1]/section/main/div/header/section/ul/li[3]/a/span').text
            button_my_subscriptions = driver.find_element_by_xpath(
                '/html/body/div[1]/section/main/div/header/section/ul/li[3]/a').click()
            driver.implicitly_wait(10)
            window_my_subscriptions = driver.find_element_by_xpath('/html/body/div[5]/div/div/div[2]')

            for scroll in range(int(count_my_subscriptions) // 12 + 1):
                driver.execute_script('arguments[0].scrollTop=arguments[0].scrollHeight', window_my_subscriptions)
                time.sleep(random.randrange(1, 4))
            tags_a = window_my_subscriptions.find_elements_by_tag_name('a')
            self.urls_my_subscriptions_lst = []
            for item in tags_a:
                self.urls_my_subscriptions_lst.append(item.get_attribute('href'))

            # дальше код для того что бы убрать повторяющиеся ссылки
            self.urls_my_subscriptions_lst = set(self.urls_my_subscriptions_lst)
            self.urls_my_subscriptions_lst = list(self.urls_my_subscriptions_lst)
            with open('my_subscriptions.json', 'w') as file:
                json.dump(self.urls_my_subscriptions_lst, file, indent=2, ensure_ascii=False)

            return self.urls_my_subscriptions_lst  # тепер этот атрибут класса является списком на моих подписчиков

            time.sleep(5)
        except Exception as ex:
            print(f'ошибка в get_urls_my_followers {ex}')
        finally:
            self.close_browser()

    #
    #
    #
    #
    #
    #
    #
    #
    # получить ссылки аккаунтов на мои ПОДПИСКИ (то есть на тоех людей, на кого я подписан)
    # userpage это ссылка на мой аккаунт
    # закидываем в json, а так же возврвщвет список со ссылками на мои подписки
    def get_my_followers(self, userpage: str):
        try:
            driver = self.driver
            driver.get(userpage)
            count_my_followers = int(
                driver.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/ul/li[3]/a/span').text)
            print(count_my_followers)
            followers = driver.find_element_by_xpath(
                '/html/body/div[1]/section/main/div/header/section/ul/li[3]/a').click()
            driver.implicitly_wait(10)
            window_with_my_followers = driver.find_element_by_xpath('/html/body/div[5]/div/div/div[2]')
            count_scroll = 0
            for scroll in range(count_my_followers // 12 + 1):
                driver.execute_script('arguments[0].scrollTop=arguments[0].scrollHeight', window_with_my_followers)
                count_scroll += 1
                print(f'scroll {count_scroll}')
                time.sleep(random.randrange(2, 5))
            lst_with_followers = window_with_my_followers.find_elements_by_tag_name('li')
            lst_with_links_followers = []
            for follower in lst_with_followers:
                lst_with_links_followers.append(follower.find_element_by_tag_name('a').get_attribute('href'))

            with open('lst_with_links_followers.json', 'w') as file:
                json.dump(lst_with_links_followers, file, indent=2, ensure_ascii=False)
            return lst_with_links_followers
        except Exception as ex:
            print(Fore.CYAN + f'ошибка в get_my_followers {ex}' + Style.RESET_ALL)

    #
    #
    #
    #
    #
    #
    #
    #
    # отписка от всех моих подписок , что бы от всех, воспользуйтесь следующим методом
    def unsubscribe_my_followers(self, userpage):
        try:
            driver = self.driver
            driver.get(userpage)
            count_my_followers = int(
                driver.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/ul/li[3]/a/span').text)
            print(count_my_followers)
            for i in range(count_my_followers // 7 + 1):
                followers = driver.find_element_by_xpath(
                    '/html/body/div[1]/section/main/div/header/section/ul/li[3]/a').click()
                driver.implicitly_wait(10)
                window_with_my_followers = driver.find_element_by_xpath('/html/body/div[5]/div/div/div[2]/ul/div')
                lst_with_unsubscribe = []
                lst_with_followers = window_with_my_followers.find_elements_by_tag_name('li')
                for follower in lst_with_followers:
                    link_follower = follower.find_element_by_tag_name('a').get_attribute('href')
                    lst_with_unsubscribe.append(link_follower)
                    time.sleep(random.randrange(3, 7))
                    follower.find_element_by_tag_name('button').click()
                    driver.implicitly_wait(10)
                    time.sleep(random.randrange(1, 3))
                    try:
                        window_confirmation = driver.find_element_by_xpath('/html/body/div[6]/div/div/div')
                        window_confirmation.find_element_by_tag_name('button').click()
                        time.sleep(random.randrange(1, 5))
                    except Exception as ex:
                        print(link_follower, ex)

                # сохраняем всех, от кого мы отписались
                username = userpage.split('/')[-2]
                if os.path.exists(f'lst_with_unsubscribe_{username}.json'):
                    with open(f'lst_with_unsubscribe_{username}.json') as file:
                        lst_with_unsubscribe.extend(json.load(file))
                lst_with_unsubscribe = set(lst_with_unsubscribe)
                lst_with_unsubscribe = list(lst_with_unsubscribe)
                with open(f'lst_with_unsubscribe_{username}.json', 'w') as file:
                    json.dump(lst_with_unsubscribe, file, indent=2, ensure_ascii=False)
                driver.get(url=userpage)

        except Exception as ex:
            print(f'error in {ex}')

    #
    #
    #
    #
    #
    #
    #
    #
    def unsubscribe_my_followers_if_not_reciprocity(self, userpage, take_from_files_my_sub=False):
        try:
            driver = self.driver
            driver.get(url=userpage)
            driver.implicitly_wait(10)
            # получаем ссылки на моих подписчиков
            if take_from_files_my_sub == False:
                lst_with_my_subscribers = self.get_all_subscribers(userpage=userpage, only_get_followers=True)
            else:
                with open('users_data/lev_for_you/followers_lst.json') as file:
                    lst_with_my_subscribers = json.load(file)

            # получаем ссылки на мои подписки
            if take_from_files_my_sub == False:
                lst_with_my_followers = self.get_my_followers(userpage=userpage)
            else:
                with open('lst_with_links_followers.json') as file:
                    lst_with_my_followers = json.load(file)
            lst_need_unsubscribe = []
            for my_followers in lst_with_my_followers:
                if my_followers not in lst_with_my_subscribers:
                    lst_need_unsubscribe.append(my_followers)
                    self.unsubscribe_one(my_followers)


        except Exception as ex:
            print(Fore.CYAN + f'ошибка в unsubscribe_my_followers_if_not_reciprocity {ex}' + Style.RESET_ALL)

    #
    #
    #
    #
    #
    #
    #
    #
    def unsubscribe_one(self, userpage):
        try:
            driver = self.driver
            driver.get(url=userpage)
            driver.implicitly_wait(10)
            button_unsub = driver.find_element_by_xpath(
                '/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/div/div[2]/div/span/span[1]').click()
            window_unsub = driver.find_element_by_xpath('/html/body/div[5]/div/div')
            time.sleep(random.randrange(1, 3))
            button_unsub_confirmation = window_unsub.find_element_by_tag_name('button').click()
            time.sleep(random.randrange(2, 5))
        except Exception as ex:
            print(Fore.LIGHTGREEN_EX + f'ошибка в unsubscribe_one {ex}' + Style.RESET_ALL)


my_login = 'lv_rey'
my_password = 'LEV60605010ru'

for user, data_dict in ussers_setting_dict.items():
    if user == 'user2': continue
    try:
        my_bot = InstagramBot(data_dict['login'], data_dict['password'], window=data_dict['window_size'])
        my_bot.login()
        # my_bot.count_men = 0
        # my_bot.followers_urls_lst = json.load(open('lst_with_unsubscribe_lev_for_you.json'))
        # my_bot.unsubscribe_my_followers('https://www.instagram.com/lev_for_you/')
        # for url in json.load(open('lst_with_unsubscribe_lev_for_you.json')):
        #     my_bot.count_men += 1
        #     # что-то было
        #     time.sleep(random.randrange(1, 5))
        my_bot.unsubscribe_my_followers_if_not_reciprocity(userpage='https://www.instagram.com/lev_for_you/',
                                                           take_from_files_my_sub=True)
    except Exception as ex:
        print('ошибка в принципе', ex)
    finally:
        my_bot.close_browser()
