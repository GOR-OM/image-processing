from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import io
from PIL import Image
import os
import time

def create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def get_images_for_breed(wd, delay, max_images, breed_query, breed_directory):
    create_directory(breed_directory)

    def scroll_down(wd):
        wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(delay)

    search_url = f"https://www.google.com/search?q={breed_query}&tbm=isch"
    wd.get(search_url)

    image_urls = set()
    skips = 0

    while len(image_urls) + skips < max_images:
        scroll_down(wd)

        thumbnails = wd.find_elements(By.CSS_SELECTOR, '[jsname="Q4LuWd"]')

        for img in thumbnails[len(image_urls) + skips:max_images]:
            try:
                img.click()
                time.sleep(delay)
            except:
                continue

            images = wd.find_elements(By.CSS_SELECTOR, '[jsname="kn3ccd"]')
            for image in images:
                if image.get_attribute('src') in image_urls:
                    max_images += 1
                    skips += 1
                    break

                if image.get_attribute('src') and 'http' in image.get_attribute('src'):
                    image_urls.add(image.get_attribute('src'))
                    print(f"Found {len(image_urls)}")

    return image_urls

def download_images(download_path, breed_directory, urls):
    for i, url in enumerate(urls):
        download_image(os.path.join(download_path, breed_directory), url, str(i) + ".jpg")

def download_image(download_path, url, file_name):
    try:
        image_content = requests.get(url).content
        image_file = io.BytesIO(image_content)
        image = Image.open(image_file)
        file_path = os.path.join(download_path, file_name)

        with open(file_path, "wb") as f:
            image.save(f, "JPEG")

        print("Success")
    except Exception as e:
        print('FAILED -', e)

wd = webdriver.Chrome("D:\project\python\WoC\practice\chromedriver-win64\chromedriver.exe")  
download_path = "imgs"

breeds = {
    "germanshepherd": "German Shepherd",
    "beagle": "Beagle",
    "goldenretriever": "Golden Retriever",
    "bulldog": "Bulldog",
    "labrador": "Labrador Retriever"
}

create_directory(download_path)

for breed_query, breed_directory in breeds.items():
    urls = get_images_for_breed(wd, 1, 100, breed_query, os.path.join(download_path, breed_directory))
    download_images(download_path, breed_directory, urls)

wd.quit()
