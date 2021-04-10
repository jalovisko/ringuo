import argparse
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'This application searches transcriptions from the Oxford dictionary')
    parser.add_argument('-w', dest = 'word',
            help = 'The word of interest')
    parser.add_argument('-i', dest = 'input_filename',
            help = 'Input Excel filename with words of interest')
    cli_args = parser.parse_args()
    if cli_args.word is not None:
        word = str(cli_args.word)
    elif cli_args.input_filename is not None:
        dfs = pd.read_excel(input_filename, sheet_name = "Sheet1")
        word = dfs.iloc[i, 0] # every entry from the 1st column
    else:
        raise ValueError('No input is provided')

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=%s" % '800,600')

    # Using Chrome to access web
    driver = webdriver.Chrome(options=chrome_options)
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
        print(transcriptions.text)
    else:
        print(transcriptions[0].text)
