import os
import time
import base64
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

DOWNLOAD_PAGE_URL = "https://mosdac.gov.in/download/#/?cd=%2FOrder%2FJul25_136805%2Fimages"
SAVE_DIRECTORY = os.path.join(os.getcwd(), "mosdac_aod_pics")

def create_driver():
    chrome_options = Options()
    prefs = {
        "download.default_directory": SAVE_DIRECTORY,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "plugins.always_open_pdf_externally": True
    }
    chrome_options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
    driver.set_window_size(1400, 1000)
    return driver

def is_download_complete(folder):
    return not any(f.endswith(".crdownload") for f in os.listdir(folder))

def decode_href(href):
    """Extract and decode the 'path' value from the href parameter."""
    import urllib.parse
    try:
        encoded = href.split("path=")[1]
        decoded_bytes = base64.b64decode(encoded)
        return decoded_bytes.decode("utf-8")
    except Exception:
        return None

def download_images():
    os.makedirs(SAVE_DIRECTORY, exist_ok=True)
    driver = create_driver()
    driver.get("https://mosdac.gov.in/login.do")
    input("🛑 Log in to MOSDAC and then press Enter here to continue...")

    driver.get(DOWNLOAD_PAGE_URL)
    time.sleep(5)

    rows = driver.find_elements(By.XPATH, "//tr[contains(@class, 'file-row')]")
    print(f"🔍 Total rows found: {len(rows)}")

    downloaded = set(os.listdir(SAVE_DIRECTORY))

    for idx, row in enumerate(rows, start=1):
        try:
            # Extract filename
            name_cell = row.find_element(By.XPATH, ".//td[@data-label='Name']")
            file_name = name_cell.text.strip()

            if not file_name or file_name in downloaded:
                print(f"[{idx}] ⚠️ Skipping: {file_name}")
                continue

            print(f"[{idx}] 🔽 Downloading: {file_name}")

            # Find anchor with download link
            anchor = row.find_element(By.XPATH, ".//a[contains(@href, 'path=')]")
            href = anchor.get_attribute("href")
            path_info = decode_href(href)

            if not href or not path_info:
                print(f"   ❌ No valid href found for {file_name}")
                continue

            # Trigger the download directly in the browser
            download_url = f"https://mosdac.gov.in/download/?r=/download&path={href.split('path=')[1]}"
            driver.execute_script(f"window.open('{download_url}', '_blank');")
            time.sleep(5)  # Let the file start downloading

            # Wait for download to finish
            wait_time = 0
            while not is_download_complete(SAVE_DIRECTORY):
                time.sleep(2)
                wait_time += 2
                if wait_time > 30:
                    print(f"   ⚠️ Timeout waiting for {file_name} to finish downloading")
                    break

            downloaded.add(file_name)
            print(f"   ✅ Finished: {file_name}\n")

        except Exception as e:
            print(f"[{idx}] ❌ Error: {e}")
            continue

    print("🎉 All downloads completed.")
    driver.quit()

if __name__ == "__main__":
    download_images()
