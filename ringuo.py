import argparse
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Sets up Chrome and returns its webdriver to be used by Selenium
def setup_chrome():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=%s" % '800,600')
    return webdriver.Chrome(options = chrome_options)

# Gets transcription of a word with the help of the driver
def get_transcription(driver, word):
    # Open the website
    driver.get('https://www.oxfordlearnersdictionaries.com/definition/english/')
    # Select the search box
    search_box = driver.find_element_by_id('q')
    # Send search information
    search_box.send_keys(word)
    # Find the search button
    search_button = driver.find_element_by_id('search-btn')
    # Click search
    search_button.click()
    # Find transcriptions
    transcriptions = driver.find_elements_by_class_name("phon")
    if len(transcriptions) == 0:
        return transcriptions.text
    else:
        return transcriptions[0].text

# Formats transcription from being bounded by \ to being bounded by \[\]
def format_transcription(transcription):
    formated_transcription = transcription[1:-1]
    formated_transcription = '[' + transcription + ']'
    return formated_transcription

# A function that does translation (doesn't work as expected sometimes)
def translate_rus_to_eng(driver, word):
    # Open the website
    driver.get('https://www.multitran.com/m.exe?s=' + word + '&l1=2&l2=1')
    # Find transcriptions
    translation = driver.find_elements_by_class_name("trans")
    if len(translation) == 0:
        return translation.text
    else:
        return translation[0].text

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'This application searches transcriptions from the Oxford dictionary')
    parser.add_argument('-w', dest = 'word',
            help = 'The word of interest')
    parser.add_argument('-i', dest = 'input_filename',
            help = 'Input Excel filename with words of interest')
    cli_args = parser.parse_args()
    word = cli_args.word
    input_filename = cli_args.input_filename
    # Using Chrome to access web
    driver = setup_chrome()
    if word is not None:
        print(format_transcription(get_transcription(driver, word)))
    elif input_filename is not None:
        dfs = pd.read_excel(input_filename, sheet_name = "Sheet1")
        for i in range(len(dfs)):
            word = dfs.iloc[i, 0] # every entry from the 1st column
            word_rus = dfs.iloc[i, 1] # every entry from the 2nd column
            transcription = get_transcription(driver, word)
            transcription = format_transcription(transcription)
            print(word + ' ' +  transcription + ' – ' + word_rus)
    else:
        raise ValueError('No input is provided')

                                                          
        
