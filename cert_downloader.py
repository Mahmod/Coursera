import requests
import pandas as pd
from urllib.parse import urlparse
import os
import logging
from validators import url as validate_url

# Configure logging to display informative messages
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

def download_pdf(url, save_path):
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        
        # Check if the response status code is 200 (OK)
        if response.status_code == 200:
            # Write the PDF content to a local file
            with open(save_path, 'wb') as file:
                file.write(response.content)
            logging.info(f"PDF downloaded and saved as {save_path}")
        else:
            logging.warning(f"Failed to download PDF from {url}. Status code: {response.status_code}")
    except Exception as e:
        logging.error(f"An error occurred while downloading PDF from {url}: {e}")

def download_pdf_list(urls, save_directory):
    # Create the save_directory if it doesn't exist
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    # Iterate through the list of URLs
    for url in urls:
        if not isinstance(url, str):  # Skip any non-string values
            logging.warning(f"Invalid URL, Non string: {url}")
            continue

        url = url.strip()  # Remove leading and trailing whitespace
        if validate_url(url):  # Validate the URL using the validators library
            pdf_name = os.path.basename(urlparse(url).path)  # Extract the filename from the URL
            save_path = os.path.join(save_directory, pdf_name,".pdf")
            logging.info(f"Downloading {pdf_name} from {url}")
            download_pdf(url, save_path)
        else:
            logging.warning(f"Invalid URL: {url}")

if __name__ == "__main__":
    # Read the Excel file containing URLs
    excel_file = 'accomplishments.xlsx'

    # Read the 'Specializations' sheet into a DataFrame
    logging.info("######### Downloading Specializations ###########")
    specializations_df = pd.read_excel(excel_file, sheet_name='Specializations')
    download_pdf_list(specializations_df['Link'], "certificates/specializations")

    # Read the 'Courses' sheet into a DataFrame
    logging.info("######### Downloading Courses ###########")
    courses_df = pd.read_excel(excel_file, sheet_name='Courses')
    download_pdf_list(courses_df['Link'], "certificates/courses")
