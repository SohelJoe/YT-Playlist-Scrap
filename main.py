import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class YtPlaylist:
    def __init__(self, playListID=None):
        self.playListData = {}
        self.playlistLink = f"https://www.youtube.com/playlist?list={playListID}"
        self.driver = webdriver.Chrome(service=Service("chromedriver.exe"))
        self.driver.maximize_window()

    def pageOpen(self, url, xpath='//ytd-page-manager[@id="page-manager"]'):
        self.driver.get(url)
        element_present = EC.presence_of_element_located((By.XPATH, xpath))
        WebDriverWait(self.driver, 3).until(element_present)

    def fetchVideoData(self, videoLinksList):
        videosData = []
        for link in videoLinksList:
            self.pageOpen(link,'//tp-yt-paper-button[@id="more"]')
            time.sleep(3)
            self.driver.find_element(By.XPATH, '//tp-yt-paper-button[@id="more"]').click()
            pageData = {
                'tittle': self.driver.find_element(By.XPATH, '//h1[@class="title style-scope ytd-video-primary-info-renderer"]').text,
                'url': link,
                'description': self.driver.find_element(By.XPATH, '//div[@id="description"]').text
            }
            videosData.append(pageData)
        self.playListData["contents"] = videosData

    def fetchListVidURLs(self):
        listVideo = self.driver.find_elements(By.TAG_NAME, "ytd-playlist-video-renderer")
        videoLinksList = []

        for video in listVideo:
            url = video.find_elements(By.ID, 'video-title')[0].get_attribute("href")
            videoLinksList.append(url.split('&')[0])
        
        self.fetchVideoData(videoLinksList)
    
    def openList(self):
        self.pageOpen(self.playlistLink)

        thumbnailVideo = self.driver.find_elements(By.TAG_NAME, "ytd-playlist-video-renderer")[0]
        thumbnailURL = thumbnailVideo.find_element(By.ID, 'video-title').get_attribute("href")
        thumnailId = (thumbnailURL.split('&')[0]).split('v=')[1]

        self.playListData["name"] = self.driver.find_element(By.XPATH, '//h1[@id="title"]').text
        self.playListData["image"] = f"https://i.ytimg.com/vi_webp/{thumnailId}/maxresdefault.webp"
        self.playListData["description"] = self.driver.find_element(By.XPATH, '//yt-formatted-string[@id="description"]').text

    def writeJSON(self):
        # print(self.playListData)
        json_object = json.dumps(self.playListData, indent = 4)
        with open(f"{self.playListData['name'].replace(' ', '_')}.json", "w") as outfile:
            outfile.write(json_object)
        
    

if __name__ == "__main__":
    userID = "TheDrunkenCoder"
    password = "TheDrunkenCoder#Test2"
    YtList = YtPlaylist(playListID="PLRBp0Fe2GpgnexdpGJd0xoHBhffMcYP7n")
    YtList.openList()
    YtList.fetchListVidURLs()
    YtList.writeJSON()
    YtList.driver.quit()
    