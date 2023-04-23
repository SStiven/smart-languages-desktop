CREATE SCHEMA IF NOT EXISTS my_schema;

CREATE TABLE my_schema.questions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    statement TEXT NOT NULL,
    statement_hash bytea NOT NULL
);


---  CREATE TABLE my_schema.questions (
---  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
---  statement TEXT NOT NULL,
---  statement_hash bytea NOT NULL
---  );

--- ALTER TABLE my_schema.questions
--- ADD COLUMN statement_hash bytea;

--- UPDATE my_schema.questions
--- SET statement_hash = encode(digest(statement, 'sha256'), 'hex');

--- ALTER TABLE my_schema.questions
--- ALTER COLUMN statement_hash SET NOT NULL;


CREATE EXTENSION IF NOT EXISTS pgcrypto;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
--- SELECT * FROM pg_extension WHERE extname = 'uuid-ossp';


CREATE TABLE my_schema.question_embeddings (
    question_id UUID PRIMARY KEY,
    faiss_id INTEGER NOT NULL,
    embedding REAL[] NOT NULL,
    model VARCHAR,
    prompt_tokens INTEGER,
    total_tokens INTEGER,
    FOREIGN KEY (question_id) REFERENCES my_schema.questions(id)
);

CREATE INDEX idx_question_embeddings_faiss_index ON my_schema.question_embeddings (faiss_index);



CREATE TABLE my_schema.answers (
    id UUID NOT NULL,
    question_id UUID NOT NULL,
    statement TEXT NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY(question_id)
        REFERENCES my_schema.questions (id)
        ON DELETE CASCADE
);


SELECT 
    q.id as question_id,
    q.statement,
    qe.question_id as question_embedding_question_id,
    qe.embedding,
    qe.model,
    qe.prompt_tokens,
    qe.total_tokens
FROM 
    my_schema.questions q
JOIN 
    my_schema.question_embeddings qe
ON 
    q.id = qe.question_id;





SELECT 
    my_schema.questions.id,
    my_schema.questions.statement,
    my_schema.question_embeddings.faiss_id
FROM
    my_schema.questions
JOIN
    my_schema.question_embeddings ON my_schema.questions.id = my_schema.question_embeddings.question_id
WHERE
    my_schema.questions.id = 'your-question-id-here';