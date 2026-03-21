-- Create the database
CREATE DATABASE contextid_db;

-- Create the user
CREATE USER contextid_user WITH PASSWORD 'strongpassword';

-- Grant database-level privileges
GRANT ALL PRIVILEGES ON DATABASE contextid_db TO contextid_user;

-- IMPORTANT: Connect to the new database to grant schema permissions
-- If running manually in psql, type: \c contextid_db
\c contextid_db

-- Grant schema-level privileges (Fixes the "Permission Denied" error)
GRANT ALL ON SCHEMA public TO contextid_user;

-- Optional: Make the user the owner of the schema for full control
ALTER SCHEMA public OWNER TO contextid_user;

-- To run `python manage.py test`, able to create a temporary test database
ALTER ROLE contextid_user CREATEDB;