import asyncio
import json
import sys
import os
from bs4 import BeautifulSoup
from pyppeteer import launch
from fake_useragent import UserAgent


async def scrap_js_website(url, selected_tags):
    # Read the executable path from the file
    if os.path.exists('chrome_path.txt'):
        with open('chrome_path.txt', 'r') as f:
            chrome_exe_path = f.read().strip()
    else:
        print("Warning: You need to put the file path chrome.exe")
        return
    browser = await launch(executablePath=chrome_exe_path)
    page = await browser.newPage()

    # Set the user agent
    ua = UserAgent()
    await page.setUserAgent(ua.random)

    await page.goto(url)
    content = await page.content()
    soup = BeautifulSoup(content, 'html.parser')

    data = {}
    for tag in selected_tags:
        elements = soup.find_all(tag)
        data[tag] = [element.text for element in elements]

    try:
        with open('scraped_data.json', 'w') as f:
            json.dump(data, f)
    except Exception as e:
        print("Error recording data: ", str(e))

    await browser.close()

    # Checking if the file exists before opening it for reading
    if os.path.exists('scraped_data.json'):
        with open('scraped_data.json', 'r') as f:
            try:
                data_loaded = json.load(f)
                print(f"Data loaded:\n{data_loaded}")
            except Exception as e:
                print("Error reading data: ", str(e))
    else:
        print("The scraped_data.json file doesn't yet exist.")

    return data

# Get the arguments from the command line
args = json.loads(sys.argv[1])
url = args["url"]
selected_tags = args["tags"]

# Run the function with the arguments
asyncio.get_event_loop().run_until_complete(scrap_js_website(url, selected_tags))