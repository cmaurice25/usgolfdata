import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import traceback
import os
from dotenv import load_dotenv

load_dotenv()  # Load variables from .env

# Database imports
import psycopg2
from psycopg2 import Error as Psycopg2Error

# Selenium imports
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    WebDriverException,
    NoSuchElementException,
)

# NEW: Import for webdriver_manager
from webdriver_manager.chrome import ChromeDriverManager


# --- Database Configuration ---
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
# ----------------------------

URL = "https://lakejovita.com/south-course/"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15"
}


# --- get_chrome_driver function: Dynamically configured for Local or Cloud ---
def get_chrome_driver():
    options = webdriver.ChromeOptions()

    # Determine the environment based on an environment variable
    # By default, assume 'local' if RUN_ENV is not explicitly set
    RUN_ENV = os.getenv("RUN_ENV", "local")

    print(f"Detected RUN_ENV: {RUN_ENV}")  # For debugging/confirmation

    # --- ***insert new code here*** ---
    # --- General Chrome Options ---
    options.add_argument(
        "--disable-gpu"
    )  # Recommended for performance, especially headless
    options.add_argument("--no-sandbox")  # Essential for Linux security environments
    options.add_argument("--window-size=1920,1080")  # Consistent rendering size
    options.add_argument(f'user-agent={HEADERS["User-Agent"]}')

    # --- Conditional Configuration based on RUN_ENV ---
    if RUN_ENV == "cloud":
        print("Configuring WebDriver for CLOUD (headless Linux) environment.")
        options.add_argument("--headless=new")  # Run headlessly on cloud
        options.add_argument("--disable-dev-shm-usage")  # Linux-specific optimization
        options.binary_location = "/usr/bin/google-chrome"  # Linux Chrome binary path
        options.add_argument(
            "--enable-logging"
        )  # --- NEW: Add verbose logging for Chrome browser itself ---
        options.add_argument("--v=1")  # Verbosity level 1
        options.add_argument("--log-level=0")  # Set log level to INFO (0)
        # Chrome will typically output these logs to stderr or to a file named 'chrome_debug.log'
        # in the current working directory.
        # --- End NEW Logging Options ---
    else:  # Default to 'local' (Mac) if RUN_ENV is not 'cloud'
        print("Configuring WebDriver for LOCAL (Mac) environment.")
        # By default, local will run with a visible browser (no --headless=new)
        # No --disable-dev-shm-usage needed for Mac
        # No options.binary_location needed for Mac (webdriver_manager finds it automatically)
        # You can add --headless=new here if you want local to also be headless
        # options.add_argument('--headless=new') # Uncomment if you want local to be headless too

    driver = None
    try:
        # ChromeDriverManager handles downloading the CORRECT driver for your OS (Mac or Linux)
        # It automatically detects your Chrome browser version and downloads compatible ChromeDriver.
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        print("Chrome WebDriver initialized.")
        return driver
    except WebDriverException as e:
        print(f"Error initializing WebDriver: {e}")
        print("Please ensure:")
        print("1. Chrome browser is installed on your system.")
        if RUN_ENV == "cloud":
            print("   - For CLOUD: Confirmed at '/usr/bin/google-chrome'.")
            print(
                "   - All required headless dependencies (xvfb, libasound2t64, etc.) are installed system-wide."
            )
        else:  # LOCAL
            print(
                "   - For LOCAL: It should be installed in its standard /Applications path."
            )
        print(
            "2. Check for any network issues preventing webdriver_manager from downloading the driver."
        )
        traceback.print_exc()
        return None


# --- Database Connection and Table Creation Functions ---
def connect_db():
    conn = None
    try:
        conn = psycopg2.connect(
            host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD
        )
        print(f"Successfully connected to PostgreSQL database: {DB_NAME}")
        return conn
    except Psycopg2Error as e:  # Use specific psycopg2 Error
        print(f"Error connecting to database: {e}")
        traceback.print_exc()
        return None


def create_golf_data_table(conn):
    cursor = None
    try:
        cursor = conn.cursor()
        table_creation_sql = """
        CREATE TABLE IF NOT EXISTS golf_data_entries (
            id SERIAL PRIMARY KEY,
            scrape_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            cCourseNumber TEXT,
            CourseTeeNumber TEXT,
            CourseName TEXT,
            StreetAddress TEXT,
            City TEXT,
            StateorRegion TEXT,
            Zip TEXT,
            County TEXT,
            Country TEXT,
            PhoneNumber TEXT,
            FaxNumber TEXT,
            URL TEXT,
            YearBuiltFounded TEXT,
            Architect TEXT,
            StatusPublicPrivateResort TEXT,
            GuestPolicy TEXT,
            TotalHoles INTEGER,
            TeeNumber INTEGER,
            TeeName TEXT,
            Par_Overall INTEGER,
            Holes_Total INTEGER,
            Rating NUMERIC(4,1),
            Slope INTEGER,
            Par_1 INTEGER, Hole_1 INTEGER, Hdcp_1 TEXT,
            Par_2 INTEGER, Hole_2 INTEGER, Hdcp_2 TEXT,
            Par_3 INTEGER, Hole_3 INTEGER, Hdcp_3 TEXT,
            Par_4 INTEGER, Hole_4 INTEGER, Hdcp_4 TEXT,
            Par_5 INTEGER, Hole_5 INTEGER, Hdcp_5 TEXT,
            Par_6 INTEGER, Hole_6 INTEGER, Hdcp_6 TEXT,
            Par_7 INTEGER, Hole_7 INTEGER, Hdcp_7 TEXT,
            Par_8 INTEGER, Hole_8 INTEGER, Hdcp_8 TEXT,
            Par_9 INTEGER, Hole_9 INTEGER, Hdcp_9 TEXT,
            Par_10 INTEGER, Hole_10 INTEGER, Hdcp_10 TEXT,
            Par_11 INTEGER, Hole_11 INTEGER, Hdcp_11 TEXT,
            Par_12 INTEGER, Hole_12 INTEGER, Hdcp_12 TEXT,
            Par_13 INTEGER, Hole_13 INTEGER, Hdcp_13 TEXT,
            Par_14 INTEGER, Hole_14 INTEGER, Hdcp_14 TEXT,
            Par_15 INTEGER, Hole_15 INTEGER, Hdcp_15 TEXT,
            Par_16 INTEGER, Hole_16 INTEGER, Hdcp_16 TEXT,
            Par_17 INTEGER, Hole_17 INTEGER, Hdcp_17 TEXT,
            Par_18 INTEGER, Hole_18 INTEGER, Hdcp_18 TEXT,
            Tot_Out_Par INTEGER, Tot_Out_Ydg INTEGER,
            Tot_In_Par INTEGER, Tot_In_Ydg INTEGER,
            Length_Total INTEGER
        );
        """
        cursor.execute(table_creation_sql)
        conn.commit()
        print("Table 'golf_data_entries' checked/created successfully.")
        return True
    except Psycopg2Error as e:
        print(f"Error creating table: {e}")
        traceback.print_exc()
        return False
    finally:
        if cursor:
            cursor.close()


def insert_golf_data(conn, df_data):
    cursor = None
    try:
        cursor = conn.cursor()
        insert_columns = [
            "cCourseNumber",
            "CourseTeeNumber",
            "CourseName",
            "StreetAddress",
            "City",
            "StateorRegion",
            "Zip",
            "County",
            "Country",
            "PhoneNumber",
            "FaxNumber",
            "URL",
            "YearBuiltFounded",
            "Architect",
            "StatusPublicPrivateResort",
            "GuestPolicy",
            "TotalHoles",
            "TeeNumber",
            "TeeName",
            "Par_Overall",
            "Holes_Total",
            "Rating",
            "Slope",
        ]
        for i in range(1, 19):
            insert_columns.extend([f"Par_{i}", f"Hole_{i}", f"Hdcp_{i}"])
        insert_columns.extend(
            ["Tot_Out_Par", "Tot_Out_Ydg", "Tot_In_Par", "Tot_In_Ydg", "Length_Total"]
        )

        cols = ", ".join(insert_columns)
        placeholders = ", ".join(["%s"] * len(insert_columns))

        insert_sql = f"INSERT INTO golf_data_entries ({cols}) VALUES ({placeholders})"

        data_to_insert = []
        for index, row in df_data.iterrows():
            row_values = []
            for col in insert_columns:
                value = row[col]
                if value == "N/A":
                    row_values.append(None)
                elif col in [
                    "TotalHoles",
                    "TeeNumber",
                    "Par_Overall",
                    "Holes_Total",
                    "Slope",
                    "Tot_Out_Par",
                    "Tot_Out_Ydg",
                    "Tot_In_Par",
                    "Tot_In_Ydg",
                    "Length_Total",
                    *[f"Par_{i}" for i in range(1, 19)],
                    *[f"Hole_{i}" for i in range(1, 19)],
                ]:
                    try:
                        row_values.append(int(value))
                    except ValueError:
                        row_values.append(None)
                elif col == "Rating":
                    try:
                        row_values.append(float(value))
                    except ValueError:
                        row_values.append(None)
                else:
                    row_values.append(value)
            data_to_insert.append(tuple(row_values))

        cursor.executemany(insert_sql, data_to_insert)
        conn.commit()
        print(f"Successfully inserted {len(df_data)} rows into 'golf_data_entries'.")
        return True
    except Psycopg2Error as e:
        print(f"Error inserting data: {e}")
        traceback.print_exc()
        conn.rollback()
        return False
    finally:
        if cursor:
            cursor.close()


if __name__ == "__main__":
    print(f"Starting scraper for: {URL}")
    driver = None
    db_conn = None
    all_golf_data = []

    try:
        driver = get_chrome_driver()
        if not driver:
            exit()

        db_conn = connect_db()
        if not db_conn:
            print("Database connection failed. Exiting.")
            exit()

        if not create_golf_data_table(db_conn):
            print("Failed to create/check database table. Exiting.")
            exit()

        print(f"Navigating to {URL}...")
        driver.get(URL)
        time.sleep(2)

        course_name = "N/A"
        try:
            course_name_element = driver.find_element(
                By.CSS_SELECTOR, "div.fusion-text.fusion-text-1 p"
            )
            course_name = course_name_element.text.strip().replace(".", "").title()
            print(f"Extracted Course Name: {course_name}")
        except NoSuchElementException:
            print(f"Could not extract Course Name: Element not found.")
        except Exception as e:
            print(f"Could not extract Course Name: An unexpected error occurred - {e}")

        hole_tab_links = driver.find_elements(
            By.XPATH,
            "//div[@class='nav']/ul[@class='nav-tabs']//li/a[contains(@class, 'tab-link') and .//h4[contains(text(), 'Hole')]]",
        )

        if not hole_tab_links:
            print(
                "CRITICAL: Could not find any hole tab links. Re-evaluate selector for tabs."
            )
            driver.quit()
            exit()

        print(f"Found {len(hole_tab_links)} potential hole tab links.")

        for i, tab_link in enumerate(hole_tab_links):
            hole_number_text = "N/A"
            try:
                hole_num_h4 = tab_link.find_element(By.TAG_NAME, "h4")
                if hole_num_h4:
                    hole_number_text = hole_num_h4.text.strip()
                    print(f"\nProcessing {hole_number_text}...")

                driver.execute_script("arguments[0].click();", tab_link)
                time.sleep(0.5)

                target_div_id = tab_link.get_attribute("href").split("#")[-1]
                hole_content_div_selector = (By.ID, target_div_id)

                WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located(hole_content_div_selector)
                )

                current_hole_data_container_element = driver.find_element(
                    *hole_content_div_selector
                )
                hole_soup = BeautifulSoup(
                    current_hole_data_container_element.get_attribute("outerHTML"),
                    "html.parser",
                )

                hole_par = "N/A"
                hole_yardages = "N/A"
                hole_handicap = "N/A"

                par_yardage_h3 = hole_soup.find(
                    "h3", class_="fusion-responsive-typography-calculated"
                )
                if par_yardage_h3:
                    par_yardage_text = par_yardage_h3.get_text(strip=True)
                    if "Par" in par_yardage_text:
                        hole_par = (
                            par_yardage_text.split("–")[0].strip().replace("Par ", "")
                        )
                        print(f"  Par: {hole_par}")

                yardage_p_tag = hole_soup.find(
                    "p",
                    string=lambda text: text and "Gold:" in text and "Blue:" in text,
                )
                if yardage_p_tag:
                    hole_yardages = yardage_p_tag.get_text(strip=True)
                    print(f"  Yardages: {hole_yardages}")
                else:
                    print(
                        "  Yardage p tag not found. Inspect HTML for yardages within hole content."
                    )

                all_golf_data.append(
                    {
                        "Course Name": course_name,
                        "Hole Number": hole_number_text.replace("Hole ", ""),
                        "Par per Hole": hole_par,
                        "Raw Tee Yardages": hole_yardages,
                        "Hole Handicap": hole_handicap,
                    }
                )

            except Exception as e:
                print(f"Error processing {hole_number_text} tab: {e}")
                print(f"  Current URL at error: {driver.current_url}")
                traceback.print_exc()
                continue

        print("\n--- Data Processing and Structuring ---")

        tees = ["Gold", "Blue", "White", "Red"]
        final_data_for_df = []

        course_summary_values = {
            "Gold_Rating": "N/A",
            "Gold_Slope": "N/A",
            "Blue_Rating": "N/A",
            "Blue_Slope": "N/A",
            "White_Rating": "N/A",
            "White_Slope": "N/A",
            "Red_Rating": "N/A",
            "Red_Slope": "N/A",
            "Gold_Tot_Out_Par": "N/A",
            "Gold_Tot_Out_Ydg": "N/A",
            "Gold_Tot_In_Par": "N/A",
            "Gold_Tot_In_Ydg": "N/A",
            "Gold_Length": "N/A",
            "Blue_Tot_Out_Par": "N/A",
            "Blue_Tot_Out_Ydg": "N/A",
            "Blue_Tot_In_Par": "N/A",
            "Blue_Tot_In_Ydg": "N/A",
            "Blue_Length": "N/A",
            "White_Tot_Out_Par": "N/A",
            "White_Tot_Out_Ydg": "N/A",
            "White_Tot_In_Par": "N/A",
            "White_Tot_In_Ydg": "N/A",
            "White_Length": "N/A",
            "Red_Tot_Out_Par": "N/A",
            "Red_Tot_Out_Ydg": "N/A",
            "Red_Tot_In_Par": "N/A",
            "Red_Tot_In_Ydg": "N/A",
            "Red_Length": "N/A",
        }

        processed_hole_data = {}
        for hole_info in all_golf_data:
            hole_num = hole_info["Hole Number"]
            par_per_hole = hole_info["Par per Hole"]
            raw_yardages = hole_info["Raw Tee Yardages"]

            parsed_yardages_for_hole = {}
            if raw_yardages and raw_yardages != "N/A":
                for tee_pair in raw_yardages.split("|"):
                    parts = tee_pair.strip().split(":")
                    if len(parts) == 2:
                        tee_name = parts[0].strip()
                        yardage = parts[1].strip()
                        parsed_yardages_for_hole[tee_name] = yardage

            processed_hole_data[hole_num] = {
                "Par": par_per_hole,
                "Yardages": parsed_yardages_for_hole,
            }

        for tee_name in tees:
            tee_row_data = {
                "cCourseNumber": "N/A",
                "CourseTeeNumber": f"N/A-{tee_name}",
                "CourseName": course_name,
                "StreetAddress": "N/A",
                "City": "N/A",
                "StateorRegion": "N/A",
                "Zip": "N/A",
                "County": "N/A",
                "Country": "N/A",
                "PhoneNumber": "N/A",
                "FaxNumber": "N/A",
                "URL": URL,
                "YearBuiltFounded": "N/A",
                "Architect": "N/A",
                "StatusPublicPrivateResort": "N/A",
                "GuestPolicy": "N/A",
                "TotalHoles": 18,
                "TeeNumber": tees.index(tee_name) + 1,
                "TeeName": tee_name,
                "Par_Overall": course_summary_values.get(
                    f"{tee_name}_Total_Par", "N/A"
                ),
                "Holes_Total": 18,
                "Rating": course_summary_values.get(f"{tee_name}_Rating", "N/A"),
                "Slope": course_summary_values.get(f"{tee_name}_Slope", "N/A"),
            }

            total_out_par = 0
            total_out_ydg = 0
            total_in_par = 0
            total_in_ydg = 0

            for hole_num_int in range(1, 19):
                hole_num_str = str(hole_num_int)
                hole_data = processed_hole_data.get(
                    hole_num_str, {"Par": "N/A", "Yardages": {}}
                )

                tee_yardage_for_hole = hole_data["Yardages"].get(tee_name, "N/A")
                par_for_hole = hole_data["Par"]

                tee_row_data[f"Par_{hole_num_str}"] = par_for_hole
                tee_row_data[f"Hole_{hole_num_str}"] = tee_yardage_for_hole
                tee_row_data[f"Hdcp_{hole_num_str}"] = "N/A"

                try:
                    par_val = int(par_for_hole) if par_for_hole != "N/A" else 0
                    ydg_val = (
                        int(tee_yardage_for_hole)
                        if tee_yardage_for_hole != "N/A"
                        else 0
                    )

                    if 1 <= hole_num_int <= 9:
                        total_out_par += par_val
                        total_out_ydg += ydg_val
                    elif 10 <= hole_num_int <= 18:
                        total_in_par += par_val
                        total_in_ydg += ydg_val
                except ValueError:
                    pass

            tee_row_data["Tot_Out_Par"] = str(total_out_par)
            tee_row_data["Tot_Out_Ydg"] = str(total_out_ydg)
            tee_row_data["Tot_In_Par"] = str(total_in_par)
            tee_row_data["Tot_In_Ydg"] = str(total_in_ydg)
            tee_row_data["Length_Total"] = str(total_out_ydg + total_in_ydg)

            final_data_for_df.append(tee_row_data)

        output_columns = [
            "cCourseNumber",
            "CourseTeeNumber",
            "CourseName",
            "StreetAddress",
            "City",
            "StateorRegion",
            "Zip",
            "County",
            "Country",
            "PhoneNumber",
            "FaxNumber",
            "URL",
            "YearBuiltFounded",
            "Architect",
            "StatusPublicPrivateResort",
            "GuestPolicy",
            "TotalHoles",
            "TeeNumber",
            "TeeName",
            "Par_Overall",
            "Holes_Total",
            "Rating",
            "Slope",
        ]
        for i in range(1, 19):
            output_columns.extend([f"Par_{i}", f"Hole_{i}", f"Hdcp_{i}"])
        output_columns.extend(
            ["Tot_Out_Par", "Tot_Out_Ydg", "Tot_In_Par", "Tot_In_Ydg", "Length_Total"]
        )

        df = pd.DataFrame(final_data_for_df, columns=output_columns)
        df = df.fillna("N/A")

        print("\n--- Inserting data into PostgreSQL ---")
        if not insert_golf_data(db_conn, df):
            print("Failed to insert data into database.")

        output_dir = "data"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        output_filename = os.path.join(output_dir, "lake_jovita_south_course_data.csv")
        df.to_csv(output_filename, index=False, encoding="utf-8")
        print(f"\nData successfully structured and saved to CSV: {output_filename}")

        # try:
        #     os.system(f'open "{output_filename}"')
        #     print(f"Could not automatically open CSV: {open_err}")
        # except Exception as open_err:
        #     print(f"Could not automatically open CSV: {open_err}")

    except Exception as main_e:
        print(
            f"\nAn unexpected error occurred during the main scraping process: {main_e}"
        )
        traceback.print_exc()

    finally:
        if driver:
            driver.quit()
            print("\nWebDriver closed.")
        if db_conn:
            db_conn.close()
            print("Database connection closed.")
