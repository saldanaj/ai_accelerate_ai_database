import json
import datetime
import time
import urllib 
import glob

from azure.core.exceptions import AzureError
from azure.core.credentials import AzureKeyCredential

#Cosmos DB imports
from azure.cosmos import CosmosClient

from azure.cosmos.aio import CosmosClient as CosmosAsyncClient
from azure.cosmos import PartitionKey, exceptions

from openai import AzureOpenAI
from dotenv import load_dotenv


import os
from dotenv import dotenv_values

# Filename: CosmosDB-NoSQL-Vector_DiskANN-FHIR.py 

# Load environment variables from the .env file
def load_env_config(env_filename="localsettings.env"):
    """
    Loads environment variables from a .env file located one directory above the current working directory.
    Returns the config dictionary.
    """
    root_dir = os.path.dirname(os.getcwd())
    env_path = os.path.join(root_dir, env_filename)
    config = dotenv_values(env_path)
    print(f"this is the env file: {env_path}")
    return config

def assign_env_variables(config):
    """
    Assigns environment variables from the config dictionary and returns them as a dictionary.
    """
    env_vars = {
        # Completion Model
        "OPENAI_API_KEY": config.get('openai_api_key'),
        "OPENAI_API_ENDPOINT": config.get('openai_api_endpoint'),
        "OPENAI_API_VERSION": config.get('openai_api_version'),
        "COMPLETIONS_MODEL_DEPLOYMENT_NAME": config.get('completions_model_deployment_name'),

        # Embedding Model
        "EMBEDDING_MODEL_DEPLOYMENT_NAME": config.get('embedding_model_deployment_name'),
        "EMBEDDING_MODEL_ENDPOINT": config.get('embedding_model_endpoint'),
        "EMBEDDING_MODEL_KEY": config.get('embedding_model_key'),
        "EMBEDDING_MODEL_API_VERSION": config.get('embedding_model_api_version'),

        # CosmosDB Information
        "COSMOSDB_NOSQL_ACCOUNT_KEY": config.get('PERSONAL_COSMOSDB_KEY'),
        "COSMOSDB_NOSQL_ACCOUNT_ENDPOINT": config.get('PERSONAL_COSMOSDB_CONNECTION_URI'),
    }
    return env_vars

# Example usage:
# config = load_env_config()
# env_vars = assign_env_variables(config)
# print(env_vars["OPENAI_API_KEY"])

def generate_embeddings(text, embedding_client, embedding_model_deployment_name):
    """
    Generate embeddings from a string of text using the provided embedding client and deployment name.
    """
    embeddingString = str(embedding_model_deployment_name)
    response = embedding_client.embeddings.create(input=text, model=embeddingString)
    embeddings = response.model_dump()
    time.sleep(0.5)
    return embeddings['data'][0]['embedding']


# Simple function to assist with vector search
def vector_search(query, container_client, embedding_client, embedding_model_deployment_name, num_results=5, printQuery=False):
    """
    Performs a vector search using the provided container client and embedding client.
    """
    query_embedding = generate_embeddings(query, embedding_client, embedding_model_deployment_name)

    querystring = (
        "SELECT TOP {} c.id, c.type, c.title, c.rating, c.release_year, c.description, "
        "VectorDistance(c.docVector,{}) AS similarityScore FROM c"
    ).format(num_results, query_embedding)
    
    if printQuery:
        print(querystring)

    results = container_client.query_items(
        query=querystring,
        enable_cross_partition_query=True
    )
    
    return results

# Simple function to assist with vector search
def vector_search_ordered(query, container_client, embedding_client, embedding_model_deployment_name, num_results=3, printQuery=False):
    """
    Performs an ordered vector search using the provided container client and embedding client.
    """
    query_embedding = generate_embeddings(query, embedding_client, embedding_model_deployment_name)

    querystring = (
        "SELECT TOP {} c.id, c.type, c.title, c.rating, c.release_year, c.description, "
        "VectorDistance(c.docVector,{}) AS similarityScore FROM c ORDER BY VectorDistance(c.docVector,{})"
    ).format(num_results, query_embedding, query_embedding)
    
    if printQuery:
        print(querystring)

    results = container_client.query_items(
        query=querystring,
        enable_cross_partition_query=True
    )
    
    return results

# Simple predicate based on the partition key (unfortunatelly I only have one partition as of now)
def vector_search_filterordered(
    query,
    releaseYear,
    container_client,
    embedding_client,
    embedding_model_deployment_name,
    num_results=3,
    printQuery=False
):
    """
    Performs an ordered vector search with a partition key filter using the provided container client and embedding client.
    """
    query_embedding = generate_embeddings(query, embedding_client, embedding_model_deployment_name)

    querystring = (
        "SELECT TOP {} c.id, c.type, c.title, c.rating, c.release_year, c.description, "
        "VectorDistance(c.docVector,{}) AS similarityScore FROM c WHERE c.partKey = '{}' "
        "ORDER BY VectorDistance(c.docVector,{})"
    ).format(num_results, query_embedding, releaseYear, query_embedding)
    
    if printQuery:
        print(querystring)

    results = container_client.query_items(
        query=querystring,
        enable_cross_partition_query=True
    )
    
    return results

def generate_embeddings_for_fhir_files(
    fhir_dir,
    embedding_client,
    embedding_model_deployment_name,
    output_dir=None
):
    """
    Generate embeddings for all FHIR JSON files in the specified directory.
    Optionally saves the output with embeddings to output_dir.
    """
    os.makedirs(output_dir, exist_ok=True) if output_dir else None

    json_files = glob.glob(os.path.join(fhir_dir, "*.json"))
    print(f"Found {len(json_files)} FHIR files in {fhir_dir}")

    for file_path in json_files:
        with open(file_path, "r") as f:
            data = json.load(f)

        # You can customize this to use a specific field or the whole JSON
        text_for_embedding = json.dumps(data)  # or data.get("text", "") or similar

        embedding = generate_embeddings(
            text_for_embedding,
            embedding_client,
            embedding_model_deployment_name
        )
        data["embedding"] = embedding

        if output_dir:
            out_path = os.path.join(output_dir, os.path.basename(file_path))
            with open(out_path, "w") as out_f:
                json.dump(data, out_f, indent=2)
        else:
            print(f"Embedding for {file_path[:50]}...: {embedding[:5]}...")  # Print first 5 values for brevity

# Example usage in your main function:
def main_vector_search():
    config = load_env_config()
    env_vars = assign_env_variables(config)

    embedding_client = AzureOpenAI(
        api_key=env_vars["EMBEDDING_MODEL_KEY"],
        azure_endpoint=env_vars["EMBEDDING_MODEL_ENDPOINT"],
        api_version=env_vars["EMBEDDING_MODEL_API_VERSION"],
    )

    # Generate embeddings for FHIR files
    fhir_dir = os.path.join(os.getcwd(), "fhir_json")
    output_dir = os.path.join(os.getcwd(), "fhir_json_with_embeddings")
    generate_embeddings_for_fhir_files(
        fhir_dir,
        embedding_client,
        env_vars["EMBEDDING_MODEL_DEPLOYMENT_NAME"],
        output_dir=output_dir
    )

    # ...rest of your main logic...

