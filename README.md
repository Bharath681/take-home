# PubMed Paper Fetcher

**PubMed Paper Fetcher** is a command-line tool that fetches and processes research papers from the PubMed database based on a user-provided query. The tool outputs a CSV file containing details about the papers, including PubMed IDs, titles, publication dates, and information about non-academic authors and company affiliations.

## Features
- Fetch papers from PubMed using the NCBI API.
- Identify non-academic authors and their affiliations (e.g., pharmaceutical or biotech companies).
- Extract metadata such as titles, journals, publication dates, and DOI.
- Save results in a structured CSV format.
- Debug mode for detailed API responses.

## Requirements
- Python 3.8+
- [Poetry](https://python-poetry.org/) for dependency management.

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/Bharath681/take-home.git
cd pubmed-paper-fetcher
```

### 2. Install Dependencies
Ensure you have Poetry installed. Then, run:
```bash
poetry install
```

### 3. Set Up Environment Variables
Create a `.env` file in the project root and add your PubMed API key:
```
PUBMED_API_KEY=your_api_key_here
```

## Usage

Run the program using the command:
```bash
poetry run get-papers-list "QUERY" -f OUTPUT_FILE -d
```

### Example Commands:
1. Fetch papers related to cancer therapy:
   ```bash
   poetry run get-papers-list "cancer therapy" -f cancer_results.csv -d
   ```

2. Fetch papers about diabetes treatment:
   ```bash
   poetry run get-papers-list "diabetes treatment" -f diabetes_results.csv -d
   ```

## Output

The program generates a CSV file with the following columns:
- **PubmedID**: The unique PubMed identifier for the paper.
- **Title**: The title of the paper.
- **Journal**: The name of the journal where the paper is published.
- **DOI**: The Digital Object Identifier, if available.
- **Publication Date**: The year the paper was published.
- **Non-academic Author(s)**: Authors associated with pharmaceutical/biotech companies.
- **Company Affiliation(s)**: Affiliations of non-academic authors.
- **Corresponding Author Email**: The email of the corresponding author, if available.

## Development

### Project Structure:
```
pubmed-paper-fetcher/
├── src/
│   ├── __init__.py
│   ├── fetch_papers.py
├── main.py
├── README.md
├── pyproject.toml
├── .env
└── requirements.txt
```

### Testing
Run tests to validate functionality:
```bash
pytest
```

## Contributing

1. Fork the repository.
2. Create a feature branch:
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add new feature"
   ```
4. Push to the branch:
   ```bash
   git push origin feature-name
   ```
5. Submit a pull request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

