import boto3
import os
import praw
import textwrap
import time
from selenium import webdriver
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont


def generateAudio(title, text, id):
    """This function generates an audio file based on the text"""
    if len(title) > 0 and len(text) > 0:
        polly = boto3.client("polly")
        if len(text) > 2950:
            output = textwrap.wrap(text, 3000)
            count = 0
            for res in output:
                count = count + 1
                spoken_text = polly.synthesize_speech(
                    Text=res, OutputFormat="mp3", VoiceId="Matthew")
                with open(id + '-part-' + str(count) + '.mp3', 'wb') as f:
                    f.write(spoken_text['AudioStream'].read())
                    f.close()
        else:
            spoken_text = polly.synthesize_speech(
                Text=text, OutputFormat="mp3", VoiceId="Matthew")
            with open(id + '.mp3', 'wb') as f:
                f.write(spoken_text['AudioStream'].read())
                f.close()


def createImage(uri, id):
    """Creates an text image"""
    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.default_content_setting_values.notifications": 2}
    chrome_options.add_experimental_option("prefs", prefs)
    chrome = webdriver.Chrome(chrome_options=chrome_options)
    chrome.get(uri)

    submitBtn = chrome.find_element_by_xpath('//button[text()="I Agree"]')
    submitBtn.click()

    element = chrome.find_element_by_id('t3_' + id)
    location = element.location
    size = element.size
    png = chrome.get_screenshot_as_png()
    chrome.quit()

    im = Image.open(BytesIO(png))

    left = location['x']
    top = location['y']
    right = location['x'] + size['width']
    bottom = location['y'] + size['height']

    im = im.crop((left, top, right, bottom))
    im.save(id + '.png')


def formatText(input):
    output = ""
    return output
