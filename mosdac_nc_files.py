import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# --- Configuration ---
# 1. The URL of the MOSDAC download page you want to scrape.
DOWNLOAD_PAGE_URL = "https://mosdac.gov.in/download/#/?cd=%2FOrder%2FJul25_136805%2Fimages"

# 2. The local directory where you want to save the downloaded files.
#    The script will create this directory if it doesn't exist.
#    Use an absolute path to be safe.
SAVE_DIRECTORY = os.path.join(os.getcwd(), "mosdac_aod_pics")
# ---------------------


def create_driver():
    """Sets up the Chrome WebDriver with options for automatic downloads."""
    chrome_options = Options()
    
    # Set preferences for downloading files
    prefs = {
        "download.default_directory": SAVE_DIRECTORY,
        "download.prompt_for_download": False, # To auto download the file
        "download.directory_upgrade": True,
        "plugins.always_open_pdf_externally": True # It will not show PDF directly in chrome
    }
    chrome_options.add_experimental_option("prefs", prefs)
    
    # Install and set up the Chrome driver automatically
    service = ChromeService(ChromeDriverManager().install())
    
    print("🚀 Starting Chrome browser...")
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def download_nc_files_with_selenium():
    """
    Navigates to the MOSDAC page, waits for manual login,
    and then downloads all .nc files.
    """
    # Create the save directory if it doesn't exist
    if not os.path.exists(SAVE_DIRECTORY):
        os.makedirs(SAVE_DIRECTORY)
        print(f"📁 Directory created: {SAVE_DIRECTORY}")

    driver = create_driver()
    driver.get("https://mosdac.gov.in/auth/realms/Mosdac/protocol/openid-connect/auth?response_type=code&scope=openid%20email&client_id=mosdac&state=e2L2D0dUKfYlOQ_kPvA5b-k9ChM&redirect_uri=https%3A%2F%2Fmosdac.gov.in%2Fuops%2Fredirect_uri&nonce=swYkttVTU4xpHZJ6Vjl0XQpFsSjeO7OtGUaNtYtDGS4") # Go to the main login page first

    # --- Manual Login Step ---
    print("\n" + "="*50)
    print("🛑 ACTION REQUIRED: Please log in to MOSDAC in the browser window that just opened.")
    print("   The script will wait for you to complete the login.")
    input("   After you have successfully logged in, press Enter in this terminal to continue...")
    print("="*50 + "\n")

    print(f" navigatating to download page: {DOWNLOAD_PAGE_URL}")
    driver.get(DOWNLOAD_PAGE_URL)

    try:
        # --- Wait for File List to Load ---
        # We will wait for the file links to be present on the page.
        # The links are inside a div with a specific structure.
        # We will wait for at least one file link to appear.
        wait = WebDriverWait(driver, 60) # Wait up to 60 seconds
        
        print("⏳ Waiting for the file list to load on the page...")
        # This XPath looks for links that contain '.nc' in their text content
        wait.until(EC.presence_of_element_located((By.XPATH, "//a[contains(text(), '.nc')]")))
        print("✅ File list loaded.")

        # --- Find all .nc File Links ---
        # Find all anchor tags whose text contains '.nc'
        file_links = driver.find_elements(By.XPATH, "//a[contains(text(), '.nc')]")
        
        if not file_links:
            print("❌ No .nc files found on the page. Please check the URL.")
            return

        total_files = len(file_links)
        print(f"🔎 Found {total_files} .nc files to download.")

        # --- Download Loop ---
        for i, link in enumerate(file_links):
            file_name = link.text
            file_path = os.path.join(SAVE_DIRECTORY, file_name)

            # Check if the file already exists to avoid re-downloading
            if os.path.exists(file_path):
                print(f"🟡 Skipping [{i+1}/{total_files}] {file_name} (already exists).")
                continue
            
            print(f"Downloading [{i+1}/{total_files}]: {file_name}...")
            try:
                # Just click the link. The browser is configured to download automatically.
                link.click()
                # Add a small delay to allow the download to start
                time.sleep(2) 
            except Exception as e:
                print(f"❗️Could not click link for {file_name}. Error: {e}")
        
        print("\n⏳ Waiting for all downloads to complete... This might take a while.")
        # This is a simple way to wait. It checks if any .crdownload files exist.
        while any(".crdownload" in f for f in os.listdir(SAVE_DIRECTORY)):
            time.sleep(5)
            print("   ...still downloading...")

        print("\n🎉 All files have been downloaded successfully!")

    except Exception as e:
        print(f"❌ An error occurred: {e}")
        print("   This could be due to a timeout (page took too long to load) or an incorrect URL.")
    finally:
        print("Closing the browser.")
        driver.quit()


if __name__ == "__main__":
    download_nc_files_with_selenium()
