# Accelerating Your AI Journey Workshop

This repository contains resources, datasets, and scripts for hands-on labs and demonstrations focused on leveraging AI capabilities in modern data workloads. The content covers vector search and embeddings with Azure SQL, Azure Cosmos DB, and PostgreSQL, using the Netflix Titles dataset.

## Repository Structure

- **Datasets/**
  - `netflix_titles.csv`, `netflix_titles.json`: Source data for the labs, containing metadata about Netflix titles.
- **Vector Search - Azure SQL/**
  - `Procedure_generate_embeddings.sql`: SQL Server stored procedure for generating embeddings using Azure OpenAI.
  - `VectorBasics_AzureSQL.sql`: Scripts for creating tables, generating embeddings, and running vector search queries in Azure SQL.
- **Vector Search - Cosmos DB/**
  - `CosmosDB-NoSQL-Vector_AzureOpenAI_DiskANN.ipynb`: Jupyter notebook demonstrating how to use Azure Cosmos DB for NoSQL with vector search and Azure OpenAI embeddings.
- **Vector Search - PostgreSQL/**
  - `Setup.sql`: SQL scripts to set up schema, tables, and extensions for vector search in PostgreSQL.
  - `VectorBasics_PostgreSQL.sql`: Scripts for generating embeddings and running vector search queries in PostgreSQL.
- **requirements.txt**: Python dependencies for running the Cosmos DB notebook and related scripts.
- **.devcontainer/**: Configuration for running the workspace in a Dev Container (VS Code).

## Getting Started

### 1. Clone the Repository

```sh
git clone <repo-url>
cd "Accelerating Your AI Journey Workshop"
```

### 2. Install Python Requirements

If you plan to run the Cosmos DB notebook or any Python scripts, install the dependencies:

```sh
pip install -r requirements.txt
```

### 3. Using the Dev Container (Recommended)

If using VS Code, open the folder in a Dev Container for a pre-configured environment.

### 4. Data Preparation

Import the Netflix Titles dataset into your target database (Azure SQL, Cosmos DB, or PostgreSQL) as described in the respective SQL scripts or notebook.

### 5. Running the Labs

#### Azure SQL

1. Use [Vector Search - Azure SQL/VectorBasics_AzureSQL.sql](Vector Search - Azure SQL/VectorBasics_AzureSQL.sql) to create tables and generate embeddings.
2. Use [Vector Search - Azure SQL/Procedure_generate_embeddings.sql](Vector Search - Azure SQL/Procedure_generate_embeddings.sql) to set up the embedding generation procedure.

#### Cosmos DB

1. Open [Vector Search - Cosmos DB/CosmosDB-NoSQL-Vector_AzureOpenAI_DiskANN.ipynb](Vector Search - Cosmos DB/CosmosDB-NoSQL-Vector_AzureOpenAI_DiskANN.ipynb) in Jupyter or VS Code.
2. Follow the notebook instructions to load data, generate embeddings, and perform vector search.

#### PostgreSQL

1. Run [Vector Search - PostgreSQL/Setup.sql](Vector Search - PostgreSQL/Setup.sql) to set up the schema and extensions.
2. Use [Vector Search - PostgreSQL/VectorBasics_PostgreSQL.sql](Vector Search - PostgreSQL/VectorBasics_PostgreSQL.sql) for embedding generation and vector search queries.

## Presentations

- `7-Leveraging_AI-capabilities-in-your-modern-data-workload - Final.pptx`
- `9-Hands-on-Labs-FinalRemarks.pptx`
- `AcceleratingYourAIJourneybyModernizing-OneSlider.pptx`

These PowerPoint files provide background, instructions, and context for the workshop.

## Notes

- You will need access to Azure OpenAI and appropriate database services (Azure SQL, Cosmos DB, PostgreSQL) to run the full labs.
- Update API keys and endpoints in scripts and notebooks as needed.
- For more details, refer to comments within each script or notebook.

---