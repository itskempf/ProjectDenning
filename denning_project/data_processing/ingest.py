"""
Handles scraping, chunking, and ingesting legal documents into the vector DB.
"""
import requests
from bs4 import BeautifulSoup
import sys
import os
import logging

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from database.vector_db import VectorDB

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def fetch_legislation_text(url: str) -> str:
    logging.info(f"Fetching text from {url}...")
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        content_div = soup.find('div', id='content')
        if not content_div:
            raise ValueError("Could not find the main content div in the page.")
        return content_div.get_text(separator='\n', strip=True)
    except requests.RequestException as e:
        logging.error(f"Error fetching URL: {e}")
        return ""

def chunk_text(text: str, chunk_size: int = 500, overlap: int = 100) -> list[str]:
    logging.info("Chunking text...")
    words = text.split()
    if not words: return []
    chunks = []
    start = 0
    while start < len(words):
        end = start + chunk_size
        chunks.append(" ".join(words[start:end]))
        start += chunk_size - overlap
    logging.info(f"Created {len(chunks)} chunks.")
    return chunks

def main():
    if len(sys.argv) < 2:
        print("Usage: python data_processing/ingest.py <URL>")
        sys.exit(1)
    url = sys.argv[1]
    raw_text = fetch_legislation_text(url)
    if not raw_text:
        logging.error("Failed to retrieve text. Aborting ingestion.")
        return
    text_chunks = chunk_text(raw_text)
    if not text_chunks:
        logging.error("Failed to create chunks. Aborting ingestion.")
        return
    try:
        logging.info("Initializing database for ingestion...")
        vector_db = VectorDB()
        vector_db.add_documents(text_chunks)
        logging.info("Ingestion complete. Data has been added to the database.")
    except Exception as e:
        logging.error(f"An error occurred during database interaction: {e}")

if __name__ == '__main__':
    main()
