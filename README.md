# Scrape Latest News from Websites
This project is a Scrapy-based web scraper designed to extract the latest news from moneycontrol.com and livemint.com. The scraped data is then stored in a MongoDB database. The project is set up to run every 15 minutes using GitHub Actions.

## Project Structure

- `news_scraper/` - Contains the Scrapy project files and spiders.
- `requirements.txt` - Lists the dependencies for the project.
- `.github/workflows/` - Contains the GitHub Actions workflow configuration.

## Prerequisites

- Python 3.8 or higher
- Scrapy
- MongoDB
- dotenv package for managing environment variables

## Installation

1. **Clone the repository:**

    ```sh
    git clone https://github.com/Varadharavi/scrap-news.git
    cd news_scraper
    ```

2. **Create a virtual environment and activate it:**

    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required packages:**

    ```sh
    pip install --upgrade pip
    pip install -r requirements.txt
    ```

4. **Set up environment variables:**

   Create a `.env` file in the root directory of the project and add your MongoDB credentials:

    ```env
    MONGO_URI=your_mongo_uri
    MONGO_DATABASE=your_mongo_database_name
    ```

## Running the Scrapy Project Locally

1. **Navigate to the Scrapy project directory:**

    ```sh
    cd news_scraper
    ```

2. **Run the spiders:**

    ```sh
    scrapy crawl scrape_mc
    scrapy crawl livemint_scraper
    ```

## GitHub Actions Setup

The GitHub Actions workflow is configured to run the scraper every 15 minutes and push the data to MongoDB. Below is the configuration:

```yaml
name: Update News from MC & LiveMint

on:
  push:
    branches:
      - main
  schedule:
    - cron: '*/15 0-17 * * *'

jobs:
  run-script:
    runs-on: ubuntu-latest

    env:
      MONGO_URI: ${{ secrets.MONGO_URI }}
      MONGO_DATABASE: ${{ vars.MONGO_DATABASE }}

    steps:
      - name: Checkout code
        uses: actions/checkout@v2

      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.8

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Change directory and run script
        run: |
          cd news_scraper
          scrapy crawl scrape_mc
          scrapy crawl livemint_scraper
```
## Steps to Deploy
1. **Commit and Push to Main Branch**
```sh
git add .
git commit -m "Initial commit"
git push origin main
```

2. **Add MongoDB credentials to GitHub Secrets:**
    
   - Go to your GitHub repository.
   - Click on Settings.
   - Click on Secrets in the left sidebar.
   - Click on New repository secret.
   - Add MONGO_URI with your MongoDB URI.
   - Add MONGO_DATABASE with your MongoDB database name.

## License
**This project is licensed under the MIT License.**

## Contributing
- Fork the repository.
- Create a new branch (git checkout -b feature-branch).
- Make your changes.
- Commit your changes (git commit -am 'Add new feature').
- Push to the branch (git push origin feature-branch).
- Create a new Pull Request.

Feel free to reach out if you have any questions or need further assistance!
