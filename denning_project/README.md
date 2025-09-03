# Project Denning

**Evolving AI purely on law.**

Project Denning is a Python-based, open-source Legal Research Agent. Its primary design goal is to be a "pure," anti-hallucination system that provides fact-based answers to legal questions by exclusively using a curated library of UK law and a hosted Large Language Model from the Hugging Face API.

## Core Architecture

The agent is built using a **Retrieval-Augmented Generation (RAG)** architecture:

1.  **Retrieval**: When asked a question, the agent searches a local vector database (ChromaDB) to find relevant sections of UK law.
2.  **Generation**: It then sends these retrieved legal texts to the Hugging Face API, instructing a powerful LLM to synthesize a final answer based *only* on the provided text.

This design ensures answers are fact-based and grounded in source documents, while offloading the heavy computational work to the cloud.

---

## Setup Instructions

### 1. Prerequisites

-   Python 3.8 or higher.
-   A Hugging Face account and an [Access Token](https://huggingface.co/settings/tokens) with "write" permissions.

### 2. Set Up the Project

Clone the repository or create the files as described in the project structure.

### 3. Set Up Your API Key

1.  Create a file named `.env` in the root of the `denning_project` folder.
2.  Open the `.env` file and add your Hugging Face Access Token like this:
    ```
    HUGGINGFACE_API_KEY="hf_YourSecretKeyGoesHere"
    ```
3.  The `.gitignore` file is already configured to keep this file private.

### 4. Set Up a Virtual Environment & Install Dependencies

From the `denning_project` root folder:

```bash
# Create and activate a virtual environment
python -m venv venv
# On Windows: venv\Scripts\activate | On macOS/Linux: source venv/bin/activate

# Install all required Python libraries
pip install -r requirements.txt
```

---

## Usage

### Step 1: Ingest Legal Data

Run the `ingest.py` script from the project root, providing it with a URL from `legislation.gov.uk`.

```bash
# Example: Ingesting the Theft Act 1968
python data_processing/ingest.py [https://www.legislation.gov.uk/ukpga/1968/60](https://www.legislation.gov.uk/ukpga/1968/60)
```

### Step 2: Run the CLI

Once data is ingested, start the interactive command-line interface from the project root.

```bash
python cli.py
```

You can now ask legal questions. The agent will use the Hugging Face API to generate answers based on your local legal database.