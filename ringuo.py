import argparse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'This application searches transcriptions from the Oxford dictionary')
    parser.add_argument('-w', dest = 'word',
            help = 'The word of interest')
    cli_args = parser.parse_args()
    word = str(cli_args.word)

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
