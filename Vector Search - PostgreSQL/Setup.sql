
-- ****************
-- Create schema and table
CREATE SCHEMA IF NOT EXISTS ai;

CREATE TABLE IF NOT EXISTS ai.netflix_titles (
    show_id VARCHAR(10) UNIQUE NOT NULL,
    show_type VARCHAR(20) NOT NULL,
    title VARCHAR(1000) NOT NULL,
    director VARCHAR(250) NULL,
    show_cast TEXT  NULL,
    country VARCHAR(1000) NULL,
    date_added DATE NULL,
    release_year INT  NOT NULL,
    rating VARCHAR(10) NULL,
    duration VARCHAR(10)  NULL,
    listed_in VARCHAR(100) NOT NULL,
    description TEXT  NOT NULL
);

-- ****************
-- Using pgAdmin, import "netflix_titles.csv" files into ai.netflix_titles
-- Sample command:
--  command " "\\copy ai.netflix_titles (show_id, show_type, title, director, show_cast, country, date_added, release_year, rating, duration, listed_in, description) 
--    FROM 'C:/Files/Projects/Datasets/NETFLI~1/NETFLI~1.CSV' DELIMITER ',' CSV HEADER ENCODING 'UTF8' QUOTE '\"' ESCAPE '''';""
SELECT * FROM ai.netflix_titles LIMIT 10;

-- ****************
-- Preparing the extensions
-- Extension pg_diskann has to be enabled first (thru Portal or AZ CLI)
-- Added azure_ai in Portal (under Server Parameters > azure.extensions)

CREATE EXTENSION IF NOT EXISTS pg_diskann CASCADE;
-- NOTICE: installing required extension "vector"
CREATE EXTENSION azure_ai;

SELECT * FROM pg_extension;
-- Now with both extensions
SELECT * FROM pg_extension;

-- Setting up connections
SELECT azure_ai.set_setting('azure_openai.endpoint', 'yourendpoint');
SELECT azure_ai.set_setting('azure_openai.subscription_key', 'yourkeygoeshere');

-- Check setup
SELECT azure_ai.get_setting('azure_openai.endpoint');
SELECT azure_ai.get_setting('azure_openai.subscription_key');

-- Testing API call
SELECT azure_openai.create_embeddings('embeddings', 'PostgreSQL AI day!', max_attempts => 5, retry_delay_ms => 500)

-- ****************
-- Cloning table structure to accomodate vectors
CREATE TABLE IF NOT EXISTS ai.netflix_titles_embeddings (LIKE ai.netflix_titles INCLUDING DEFAULTS INCLUDING CONSTRAINTS INCLUDING INDEXES);

ALTER TABLE ai.netflix_titles_embeddings
ADD COLUMN document_vector VECTOR(1536) NULL;

INSERT INTO ai.netflix_titles_embeddings (show_id, show_type, title, director, show_cast, country, date_added, release_year, rating, duration, listed_in, description)
SELECT show_id, show_type, title, director, show_cast, country, date_added, release_year, rating, duration, listed_in, description FROM ai.netflix_titles;

SELECT * FROM ai.netflix_titles_embeddings LIMIT 10;

-- Clean up
-- DROP TABLE IF EXISTS ai.netflix_titles;


