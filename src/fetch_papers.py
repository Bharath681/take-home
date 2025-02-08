import requests
import pandas as pd
from dotenv import load_dotenv
import os
from typing import List, Dict, Optional
from xml.etree import ElementTree as ET


load_dotenv()
API_KEY = os.getenv("PUBMED_API_KEY")

def fetch_papers(query: str, debug: bool = False, api_key: Optional[str] = API_KEY) -> List[Dict]:
    esearch_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    search_params = {
        "db": "pubmed",
        "term": query,
        "retmode": "json",
        "retmax": 2,
    }
    if api_key:
        search_params["api_key"] = api_key

    response = requests.get(esearch_url, params=search_params)
    if debug:
        print(f"Request URL: {response.url}")
        print(f"Raw Response (esearch): {response.json()}")

    response.raise_for_status()
    data = response.json()
    paper_ids = data.get("esearchresult", {}).get("idlist", [])

    if not paper_ids:
        print("No papers found for the given query.")
        return []

    return fetch_paper_details(paper_ids, debug, api_key)

def fetch_paper_details(paper_ids: List[str], debug: bool = False, api_key: Optional[str] = API_KEY) -> List[Dict]:
    efetch_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    fetch_params = {
        "db": "pubmed",
        "id": ",".join(paper_ids),
        "retmode": "xml",
    }
    if api_key:
        fetch_params["api_key"] = api_key

    response = requests.get(efetch_url, params=fetch_params)
    response.raise_for_status()

    if debug:
        print(f"Request URL (efetch): {response.url}")

    root = ET.fromstring(response.text)
    papers = []

    for article in root.findall(".//PubmedArticle"):
        pmid = article.find(".//PMID").text
        title = article.find(".//ArticleTitle").text
        journal = article.find(".//Title").text if article.find(".//Title") is not None else "N/A"
        pubdate = article.find(".//PubDate/Year")
        pubdate_text = pubdate.text if pubdate is not None else "N/A"
        doi = None
        for el in article.findall(".//ELocationID"):
            if el.attrib.get("EIdType") == "doi":
                doi = el.text
                break

        authors = article.findall(".//Author")
        author_list = []
        non_academic_authors = []
        for author in authors:
            last_name = author.find("LastName")
            fore_name = author.find("ForeName")
            affiliation = author.find("AffiliationInfo/Affiliation")

            if last_name is not None and fore_name is not None:
                name = f"{fore_name.text} {last_name.text}"
                author_list.append(name)

            if affiliation is not None and any(keyword in affiliation.text.lower() for keyword in ["pharma", "biotech", "company", "inc", "corp"]):
                non_academic_authors.append(name)

        papers.append({
            "uid": pmid,
            "title": title,
            "journal": journal,
            "pubdate": pubdate_text,
            "doi": doi if doi else "N/A",
            "authors": "; ".join(author_list),
            "non_academic_authors": "; ".join(non_academic_authors),
        })

    return papers

def filter_papers(papers: List[Dict]) -> pd.DataFrame:
    filtered = []
    for paper in papers:
        filtered.append({
            "PubmedID": paper.get("uid", "N/A"),
            "Title": paper.get("title", "N/A"),
            "Journal": paper.get("journal", "N/A"),
            "DOI": paper.get("doi", "N/A"),
            "Publication Date": paper.get("pubdate", "N/A"),
            "Non-academic Author(s)": paper.get("non_academic_authors", "N/A"),
            "Authors": paper.get("authors", "N/A"),
        })
    return pd.DataFrame(filtered)

def save_to_csv(dataframe: pd.DataFrame, filename: str) -> None:
    output_path = os.path.abspath(filename)
    print(f"Saving to {output_path}...")
    if not dataframe.empty:
        dataframe.to_csv(output_path, index=False)
        print(f"CSV saved successfully at {output_path}.")
    else:
        print("No data available to save.")
