# OpenClassroomProject2
Books to Scrape - Price Monitoring System
Project Overview
This Python-based project is designed to monitor and extract pricing information from the "Books to Scrape" website. It scrapes book details across all categories and saves the data into category-specific CSV files for easy analysis and monitoring.

Features
Extracts details for each book, including title, price, stock availability, product description, category, rating, and image URL.
Handles pagination within categories to ensure complete data extraction.
Saves extracted book details for each category in separate CSV files.
Prerequisites
Before running this project, ensure you have Python 3.6 or later installed on your system. This project uses the following Python libraries:

requests
beautifulsoup4
pandas
lxml
Installation
Clone the repository:

sh
Copy code
git clone https://github.com/yourusername/book-scraper.git
cd book-scraper
Set up a virtual environment (optional but recommended):

On macOS/Linux:
sh
Copy code
python3 -m venv env
source env/bin/activate
On Windows:
cmd
Copy code
python -m venv env
env\Scripts\activate
Install the required packages:

sh
Copy code
pip install -r requirements.txt
Usage
To run the script and scrape book details from the "Books to Scrape" website, execute the following command in your terminal or command prompt:

sh
Copy code
python book_scraper.py
This command will start the scraping process. The script will automatically create CSV files on your desktop, each named after a book category, containing the extracted book details.

Output
The output CSV files will be located on your desktop. Each file will be named according to its book category (e.g., travel.csv, fiction.csv) and will contain the following columns:

title
price
stock
description
category
rating
image_url
