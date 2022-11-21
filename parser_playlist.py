from selenium import webdriver
import pandas as pd
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Main settings #

website = "Enter your url"
s = Service('Your path to chromedriver')
driver = webdriver.Chrome(service=s)
driver.get(website)
driver.maximize_window()

# Close advertise #

close_button = driver.find_element(By.XPATH, "//div[@class='pay-promo-close-btn js-close']")
close_button.click()


# Function to get name of artist and song #

def get_song(elem):
    try:
        artist = elem.find_element(By.XPATH, ".//span[@class='d-track__artists']").text
        name = elem.find_element(By.XPATH, ".//a[@class='d-track__title deco-link deco-link_stronger']").text
        song_list = [artist, name]
    except:
        song_list = [' ', ' ']
    return song_list


# Infinite scrolling the page #

artist_data = []
name_data = []

size = 0

scrolling = True
while scrolling:
    songs = WebDriverWait(driver, 5).until(
        EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@class, 'd-track__overflowable-wrapper')]")))

    for song in songs:
        song_list = get_song(song)
        artist_data.append(song_list[0])
        name_data.append(song_list[1])

        # Get the initial scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        # Scroll down to bottom
        size += 2000
        driver.execute_script(f"window.scrollTo(0, {size});")
        # Wait to load page
        time.sleep(2)
        if size < last_height:  # if the new and last height are equal, it means that there isn't any new page to load, so we stop scrolling
            break
        else:
            scrolling = False
            break

driver.quit()

new = []

for i in range(len(artist_data)):
    new.append(str(artist_data[i]) + ' - ' + str(name_data[i]))

a = sorted(set(new), key=new.index)

df_songs = pd.DataFrame({'Songs': list(a)})
df_songs.to_csv('Playlist.csv', index=False, encoding='utf-8-sig')
