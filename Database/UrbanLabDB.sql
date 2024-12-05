-- Create the database
CREATE DATABASE IF NOT EXISTS URBANLAB_DB;
USE URBANLAB_DB;

-- Create the standalone grants table
CREATE TABLE grants (
    id INT AUTO_INCREMENT PRIMARY KEY,            -- Unique identifier for the grant
    grant_name VARCHAR(100) NOT NULL,             -- Name or title of the grant
    purpose TEXT NOT NULL,                        -- Detailed description or purpose of the grant
    amount DECIMAL(10, 2) NOT NULL,               -- Amount of the grant
    frequency ENUM('One-time', 'Daily', 'Weekly', 'Monthly', 'Quarterly', 'Annually') NOT NULL, -- Fixed frequency options
    start_date DATE NOT NULL,                     -- Start date of the grant
    end_date DATE,                                -- End date of the grant (nullable for indefinite grants)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- Timestamp of record creation
);

-- Create table for student types (student_types)
CREATE TABLE student_types (
    id INT AUTO_INCREMENT PRIMARY KEY,            -- Unique identifier for student type
    type_name VARCHAR(50) NOT NULL UNIQUE,        -- Name of the student type (e.g., Current Student, Alumni)
    description TEXT                              -- Description of the student type
);

-- Insert initial values for student_types
INSERT INTO student_types (type_name, description) VALUES
('Current Student', 'Currently enrolled student'),
('Alumni', 'Graduated student');

-- Create table for students (students)
CREATE TABLE students (
    id INT AUTO_INCREMENT PRIMARY KEY,            -- Unique identifier for student
    first_name VARCHAR(100) NOT NULL,             -- First name of the student
    last_name VARCHAR(100) NOT NULL,              -- Last name of the student
    email VARCHAR(100) UNIQUE NOT NULL,           -- Email address of the student
    phone VARCHAR(15),                            -- Phone number of the student
    course VARCHAR(255),                          -- Course or program the student is enrolled in
    city VARCHAR(100),                            -- City of the student
    country VARCHAR(100),                         -- Country of the student
    student_type_id INT,                          -- Foreign key referencing student type
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Timestamp of record creation
    FOREIGN KEY (student_type_id) REFERENCES student_types(id) ON DELETE SET NULL -- Cascade deletion behavior for student type
);

-- Create table for roles (roles)
CREATE TABLE roles (
    id INT AUTO_INCREMENT PRIMARY KEY,            -- Unique identifier for role
    role_name VARCHAR(50) NOT NULL UNIQUE,        -- Name of the role (e.g., Professor, Staff)
    description TEXT                              -- Description of the role
);

-- Insert initial values for roles
INSERT INTO roles (role_name, description) VALUES
('Professor', 'University professor'),
('Staff', 'University staff'),
('Industry Representative', 'Representatives from industry partners'),
('Sponsor', 'Event or project sponsors'),
('Customer', 'External customers'),
('Collaborator', 'Collaborating individuals or organizations');

-- Create table for contacts (contacts)
CREATE TABLE contacts (
    id INT AUTO_INCREMENT PRIMARY KEY,            -- Unique identifier for contact
    first_name VARCHAR(100) NOT NULL,             -- First name of the contact
    last_name VARCHAR(100) NOT NULL,              -- Last name of the contact
    email VARCHAR(100) UNIQUE NOT NULL,           -- Email address of the contact
    phone VARCHAR(15),                            -- Phone number of the contact
    role_id INT,                                  -- Foreign key referencing role
    organization VARCHAR(255),                    -- Organization the contact is affiliated with
    city VARCHAR(100),                            -- City of the contact
    country VARCHAR(100),                         -- Country of the contact
    notes TEXT,                                   -- Additional notes about the contact
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Timestamp of record creation
    FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE SET NULL -- Cascade deletion behavior for roles
);

-- Create table for event types (event_types)
CREATE TABLE event_types (
    id INT AUTO_INCREMENT PRIMARY KEY,            -- Unique identifier for event type
    type_name VARCHAR(50) NOT NULL UNIQUE,        -- Name of the event type (e.g., Seminar, Workshop)
    description TEXT                              -- Description of the event type
);

-- Insert initial values for event_types
INSERT INTO event_types (type_name, description) VALUES
('Seminar', 'A seminar event'),
('Workshop', 'A hands-on workshop'),
('Field Trip', 'An educational field trip'),
('Lecture', 'A lecture by a professor or guest speaker'),
('Meeting', 'Various types of meetings');

-- Create table for events (events)
CREATE TABLE events (
    id INT AUTO_INCREMENT PRIMARY KEY,            -- Unique identifier for event
    event_name VARCHAR(100) NOT NULL,             -- Name of the event
    event_date DATE NOT NULL,                     -- Date of the event
    location VARCHAR(255),                        -- Location of the event
    event_type_id INT,                            -- Foreign key referencing event type
    content TEXT,                                 -- Content or notes related to the event
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Timestamp of record creation
    FOREIGN KEY (event_type_id) REFERENCES event_types(id) ON DELETE SET NULL -- Cascade deletion behavior for event types
);

-- Create table for interaction types (interaction_types)
CREATE TABLE interaction_types (
    id INT AUTO_INCREMENT PRIMARY KEY,            -- Unique identifier for interaction type
    type_name VARCHAR(50) NOT NULL UNIQUE,        -- Name of the interaction type (e.g., Participant, Speaker)
    description TEXT                              -- Description of the interaction type
);

-- Insert initial values for interaction_types
INSERT INTO interaction_types (type_name, description) VALUES
('Participant', 'Participated in the event'),
('Speaker', 'Delivered a speech or presentation'),
('Organizer', 'Organized or coordinated the event');

-- Create table for interactions (interactions)
CREATE TABLE interactions (
    id INT AUTO_INCREMENT PRIMARY KEY,            -- Unique identifier for interaction
    student_id INT,                               -- Foreign key referencing student
    contact_id INT,                               -- Foreign key referencing contact
    event_id INT NOT NULL,                        -- Foreign key referencing event
    interaction_type_id INT,                      -- Foreign key referencing interaction type
    notes TEXT,                                   -- Notes about the interaction
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Timestamp of record creation
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE, -- Cascade deletion behavior for students
    FOREIGN KEY (contact_id) REFERENCES contacts(id) ON DELETE CASCADE, -- Cascade deletion behavior for contacts
    FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE,     -- Cascade deletion behavior for events
    FOREIGN KEY (interaction_type_id) REFERENCES interaction_types(id) ON DELETE SET NULL -- Cascade deletion behavior for interaction types
);
