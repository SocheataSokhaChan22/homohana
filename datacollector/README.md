# Usage
Ensure you have Python 3.8+ installed.


Create a virtual environment

```text
python -m venv venv
source pythonenv.sh
```

Install dependencies

```text
pip install -r requirements.txt
```
## Create a .env File

You need to set up your environment variables by copy the `.env.example` file and rename it to
`.env`. Then, fill in the required values such as mongo_uri and mongo_db_name.

# Run Spider Scraping 

If you want to see the output as in text file please change the spider file (e.g. newsroom.py)
on the **custom_setting** to following code:

```text
    custom_settings = {
        "FEEDS": {
            f"output/{name}.jsonl":
            {
                "format": "jsonlines"
            },
        },
        "FEED_EXPORT_ENCODING": "utf-8"
    }
```
and

```text
cd url_khmer_scraping/jsonl_scraper
```

```text
scrapy crawl spider_name
```

### example 

```text
scrapy crawl newsroom
```
Install jsonl_format: generate your tokens and replace the below cmd with your actual tokens
You be able to download the fasstext first in order install the jsonl_format

- for window please install fastext from this link : https://github.com/mdrehan4all/fasttext_wheels_for_windows/blob/main/fasttext-0.9.2-cp310-cp310-win_amd64.whl

Or 
```text
pip install fasttext
```

```text
pip install jsonl-format --extra-index-url https://__token__:<your_personal_token>@git.anakotlab.com/api/v4/projects/134/packages/pypi/simple

```
## Set Up MongoDB

Ensure MongoDB is running on your local machine or server. Update your configuration files with the appropriate MongoDB connection details.

## Run the Backend

```text
cd backend
```

Run FastAPI

```text
pip install fastapi uvicorn
fastapi dev app.py
```
Once the server is running, you can access it at:

- API Endpoint: http://127.0.0.1:8000/
- Interactive API Documentation: http://127.0.0.1:8000/docs

# Test

```text
pip install -r requirements-test.txt
```

Please find the more on the `.gitlab-ci.yml` file on how to run the test stages as follow :
  - Static Analysis
  - Unit Test
# Structure

Lets take a look at the structure of this project:

```text
SCRAPPER/
│
├── backend/
│   ├── .coverage                # Coverage report file
│   ├── app.py                   # FastAPI application entry point
│   ├── constants.py             # Constants used in the backend
│   ├── spider_manager.py        # Manages spider tasks
│   └── db/                      # The directory for Database
│       ├── database.py          # Database connection and operations
│       └── mongodb.yaml         # MongoDB configuration
│
├── tests/                       # The directory for unit test codes
│   ├── backend/
│   │   ├── test_app_route.py    # Tests for API routes
│   │   └── test_spider_manager.py # Tests for spider manager
│   └── db/
│       └── test_database.py     # Tests for database operations
│
├── url_khmer_scraping/          # Main package for Scrapy Spider
│   ├── scrapy.cfg               # Scrapy project configuration
│   ├── __init__.py              
│   └── jsonl_scraper/           # Scrapy project directory
│       ├── items.py             # Scrapy item definitions
│       ├── middlewares.py       # Scrapy middlewares
│       ├── pipelines.py         # Scrapy pipelines for data processing
│       ├── settings.py          # Scrapy settings
│       ├── __init__.py          
│       └── spiders/             # Directory for Scrapy spiders
│           ├── newsroom.py      # Scrapy spider for newsroom data
│           ├── parse.py         # parsing data to jsonl format
│           ├── prescom.py       # Scrapy spider for prescom data
│           ├── test_quote.py    # Test spider
│           └── __init__.py      
│
├── .coveragerc                   # Coverage configuration file
├── .flake8                       # Flake8 configuration file
├── .gitignore                    # Git ignore file
├── .gitlab-ci.yml                # GitLab CI/CD configuration file
├── .pylintrc                     # Pylint configuration file
├── flake8-report                 # Flake8 report
├── LICENSE                       # License file
├── pyproject.toml                # Project configuration file
├── pythonenv.sh                  # Script for setting up Python environment
├── README.md                     # Project documentation
├── requirements-test.txt         # Test dependencies
├── requirements.txt              # Project dependencies
├── run.py                        # Script to run the application
├── sonar-project.properties      # SonarQube project configuration file

```

# Features

- [ ] Backend Development
    - **FastAPI Application**: Provides API endpoints to manage spider tasks and interact with the backend.
    - **Spider Management**: Handles operations related to starting, stopping, and monitoring spiders.
    - **Database Integration**: Connects to MongoDB for storing and retrieving data.
- [ ] Web Scraping
    - **Scrapy Integration**: Utilizes Scrapy to crawl and scrape Khmer text data from various sources.
    - **Custom Spiders**: Implements specific spiders for different data sources (newsroom.py, prescom.py).
    - **Data Processing Pipelines**: Processes scraped data using custom pipelines.
    - **Middleware Support**: Uses middlewares for handling requests with duplicated URL.
- [ ] Frontend Development
    - **Dashboard**: Provides a user interface for interacting with the backend and displaying scraped data.
- [ ] Testing
    - **Unit Tests**: Includes tests for backend logic, spider management, and database operations.
    - **Coverage Reports**: Generates coverage reports to ensure code quality.

# License

Distributed under the MIT License. See [LICENSE](./LICENSE) for more information.
