# Openalex-Research-Dashboard

# AI Research Dashboard

A dashboard to analyze research output in AI-related fields and Deep Learning across the US, China, and Germany using data from OpenAlex.

## Project Structure

```
ai-research-dashboard/
├── data-extraction/
│ ├── config.py # API key storage for OpenAlex
│ ├── extract_openalex_data.py # Data extraction script
│ └── raw_data/ # Directory for storing raw JSON data
├── data-processing/ # Data cleaning and preprocessing scripts
├── data-visualization/ # Scripts for data visualization and analysis
├── README.md # Project documentation
├── .gitignore # Files and directories to be ignored by Git
├── requirements.txt # List of dependencies
└── main.py # Entry point of the dashboard

```

## Dependencies

Install the required libraries:

```bash
pip install -r requirements.txt
```

## Data Processing (PostgreSQL)

- Run the data processing script to insert data into the PostgreSQL database:

```bash
python3 data-processing/process_data.py
```

## Data Analysis

Run the data analysis script to generate publication trend plots for AI and Deep Learning research:

```bash
python3 data-analysis/analyze_data.py
```

## Data Extraction (OpenAlex)

- Fetch data from OpenAlex API:

```bash
python3 data-extraction/extract_openalex_data.py
```
