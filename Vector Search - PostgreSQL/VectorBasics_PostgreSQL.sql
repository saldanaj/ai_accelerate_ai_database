-- ******** setup.sql should be executed first

-- Checking which records doesn't have embedding
SELECT COUNT(*) 
FROM ai.netflix_titles_embeddings 
WHERE document_vector IS NULL;

-- Loop thru all records without embedding and create embedding for each record
DO $$ 
DECLARE 
    r RECORD;
    batch_size INT := 10;
BEGIN
    LOOP
        FOR r IN
            SELECT show_id
            FROM ai.netflix_titles_embeddings 
            WHERE document_vector IS NULL
            LIMIT batch_size
        LOOP
            -- Assuming you have a function `generate_embedding` that generates the embedding for the document_text
            UPDATE ai.netflix_titles_embeddings
            SET document_vector = azure_openai.create_embeddings('embeddings', title || ' ' || description, max_attempts => 5, retry_delay_ms => 500)
            WHERE show_id = r.show_id;

            COMMIT;
        END LOOP;
    
 
        -- Exit the loop if no more rows are found
        EXIT WHEN NOT FOUND;
    END LOOP;
END $$;


-- Check if all records have embedding and sample a few records
SELECT COUNT(*) 
FROM ai.netflix_titles_embeddings 
WHERE document_vector IS NULL;

SELECT *
FROM ai.netflix_titles_embeddings 
WHERE document_vector IS NOT NULL
LIMIT 10;

-- Create DiskANN index
CREATE INDEX idx_diskann 
ON ai.netflix_titles_embeddings 
USING diskann (document_vector vector_cosine_ops);


-- **************** 
-- Execute queries similar to the ones at CosmosDB-NoSQL-Vector_AzureOpenAI_DiskANN.ipynb
WITH params AS (
--   SELECT azure_openai.create_embeddings('embeddings', 'Best romantic comedy movies to watch in family with kids coming to tenage years')::vector AS query_vector
--   SELECT azure_openai.create_embeddings('embeddings', 'Action movie with zombies and a lot of blood')::vector AS query_vector
  SELECT azure_openai.create_embeddings('embeddings', 'Sports movie that shows the struggle of a team to win the championship')::vector AS query_vector
)
SELECT s.show_id, s.title, s.description,
       s.document_vector <#> params.query_vector AS distance
FROM ai.netflix_titles_embeddings as s, params
ORDER BY document_vector <#> params.query_vector  -- cosine distance
LIMIT 3;


WITH params AS (
--   SELECT azure_openai.create_embeddings('embeddings', 'Best romantic comedy movies to watch in family with kids coming to tenage years')::vector AS query_vector
--   SELECT azure_openai.create_embeddings('embeddings', 'Action movie with zombies and a lot of blood')::vector AS query_vector
  SELECT azure_openai.create_embeddings('embeddings', 'Sports movie that shows the struggle of a team to win the championship')::vector AS query_vector
)
SELECT s.show_id, s.title, s.description,
       s.document_vector <#> params.query_vector AS distance
FROM ai.netflix_titles_embeddings as s, params
WHERE release_year = 2016 --2011
ORDER BY document_vector <#> params.query_vector  -- cosine distance
LIMIT 3;
