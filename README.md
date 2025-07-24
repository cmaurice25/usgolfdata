# USGOLFDATA

USGOLFDATA is a backend data pipeline project designed to structure, process, and store U.S. golf course data in a centralized PostgreSQL database hosted on AWS EC2. The system supports both manually collected and automatically extracted data, with future plans for API-based access and integration.

# USGOLFDATA

USGOLFDATA is a backend data pipeline project designed to structure, process, and store U.S. golf course data in a centralized PostgreSQL database hosted on AWS EC2. The system supports both manually collected and automatically extracted data, with future plans for API-based access and integration.

### 🔧 Project Status

> **This project is a work in progress.**  
> Code organization and modular segmentation are ongoing as the system evolves.  
> Future improvements will include clearer separation of scraping, parsing, and database modules to enhance maintainability and reusability.

## 🔍 Overview

The goal of this project is to build a scalable, structured dataset of golf course information across the United States — including course-level metadata, hole-by-hole statistics, and tee configurations.

The system supports:

- 🧱 Normalized schema for golf course records and tee configurations
- 🗃️ Ingestion of data via pandas DataFrames (from scraping or manual entry)
- 🌐 Remote PostgreSQL database hosted on AWS RDS
- 🧪 Dynamic Chrome WebDriver support for optional data collection
- 📦 Export to CSV for backup or reporting
- 🚧 Future-ready architecture for API integration and analytics tooling

## 🛠️ Technologies Used

- **Python** (3.10+)
- **Selenium** + **BeautifulSoup** (optional scraping support)
- **PostgreSQL** (hosted on AWS RDS)
- **pandas** for data processing
- **psycopg2** for database interactions
- **dotenv** for secure configuration
- **ChromeDriverManager** for cross-platform headless browsing

## 🗄️ Database Schema

The database schema captures:

- Course metadata (name, address, architect, status, etc.)
- Tee configurations (Gold, Blue, White, Red)
- Hole-by-hole data: par, yardage, and handicap for up to 18 holes
- Totals for front 9, back 9, and overall length

## 🚀 How It Works

1. **Data is collected** from a target course (manually or via scraping).
2. **Hole-by-hole information is parsed** and organized by tee.
3. The structured data is **inserted into a normalized PostgreSQL table**.
4. A copy of the dataset is optionally exported as a CSV file.

> The data ingestion logic automatically handles missing fields, type conversions, and ensures referential consistency for each course-tee pair.

## 🔐 Environment Configuration

This project uses a `.env` file for secure storage of credentials:
DB_HOST=your-db-host
DB_NAME=your-db-name
DB_USER=your-db-user
DB_PASSWORD=your-db-password

> Be sure to keep `.env` excluded from version control. The repo’s `.gitignore` already includes this rule.

## 📁 Project Structure (Simplified)

usgolfdata/
├── main.py               # Pipeline entry point
├── assets/               # Optional images, visuals, or exports
├── data/                 # Output directory for CSV exports
├── .env                  # (Not committed) Environment variables
└── requirements.txt      # Python dependencies

## 🧭 Roadmap

- [x] Store structured data from a single course
- [x] Normalize tee-level records
- [x] Host database on AWS
- [ ] Build internal API for querying golf course data
- [ ] Add CLI for course ingestion and summary generation
- [ ] Expand coverage to hundreds/thousands of courses

## 🧑‍💻 Author

Built by [Christopher Maurice](https://github.com/cmaurice25) — developer, data architect, and golf enthusiast.

---

> For questions, feature requests, or partnership opportunities, feel free to reach out via GitHub Issues or connect on LinkedIn.

