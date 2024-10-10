# Centralize-Ethiopian-medical-business-data

## Project Overview

This project aims to build a comprehensive data warehouse that stores and processes data on Ethiopian medical businesses scraped from Telegram channels. The data is collected, cleaned, transformed, and then exposed through an API for easy access and analysis. Additionally, object detection is performed on images scraped from specific Telegram channels using YOLO, enhancing data insights.

### Key Components:

1. **Data Scraping**: 
   - Scraping data from Telegram channels using Telethon, Scrapy, and Selenium.
   - Storing the raw data in temporary storage for further processing.

2. **Data Cleaning & Transformation**: 
   - Cleaning the raw data by handling missing values, duplicates, and formatting issues using Pandas.
   - Utilizing DBT for ELT/ETL processes to transform and load data into a PostgreSQL data warehouse.

3. **Object Detection with YOLO**: 
   - Detecting objects in images from Telegram channels using YOLO.
   - Storing bounding box coordinates, confidence scores, and class labels in the data warehouse.

4. **API Development (FastAPI)**: 
   - Exposing the collected data using a FastAPI-based REST API for data retrieval and interaction.


## Features

1. **Telegram Scraping**: Custom scripts for scraping data from various Telegram channels focused on Ethiopian medical businesses.
2. **Data Warehouse**: PostgreSQL data warehouse storing cleaned and transformed data for analysis.
3. **Object Detection**: YOLO integration to detect objects in images scraped from Telegram, with results stored in the warehouse.
4. **API Exposure**: FastAPI application for data access through defined endpoints.


## Setup Instructions
#### Prerequisites
Ensure you have the following installed:

- Python 3.8+
- PostgreSQL
- Git

1. **Clone the Repository**
git clone <repository_url>
cd project_name

2. **Install Dependencies**
pip install -r requirements.txt

3. **Set Up PostgreSQL Database**
Create a PostgreSQL database for storing your data. Update the database.py file with your credentials.

4. **Scrape Data** : Run the scraping scripts to collect data from Telegram
python src/scraping/telegram_scraper.py

5. **Clean & Transform Data** : Run the data cleaning and transformation pipelines
dbt run

6. **Object Detection** : Run the YOLO object detection script
python src/object_detection/run_yolo.py

7. **Start the FastAPI Application** : Run the FastAPI application to expose your data via API
uvicorn src.api.main:app --reload

- API Endpoint
GET /data - Retrieve cleaned and transformed data
POST /detect - Submit an image for object detection

- Testing  : Run tests using pytest:
pytest.