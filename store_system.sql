-- Create the database
CREATE DATABASE IF NOT EXISTS store_system;
USE store_system;

-- Create the Stores (Tiendas) table
CREATE TABLE stores (
    store_id VARCHAR(20) PRIMARY KEY,  -- Unique store identifier
    code VARCHAR(20) UNIQUE NOT NULL,  -- Unique alphanumeric store code
    address VARCHAR(255) NOT NULL,
    city VARCHAR(100) NOT NULL,
    province VARCHAR(100) NOT NULL,
    enabled BOOLEAN NOT NULL DEFAULT TRUE  -- Enabled/disabled store
);

-- Create the Users (Usuarios) table
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,  -- Unique user identifier
    username VARCHAR(50) UNIQUE NOT NULL,  -- Unique username
    password VARCHAR(255) NOT NULL,  -- Password (should be hashed in real implementations)
    role INT NOT NULL,  -- Role (1 for admin, 2 for store user, etc.)
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    enabled BOOLEAN NOT NULL DEFAULT TRUE,  -- Enabled/disabled user
    store_id VARCHAR(20),  -- Foreign key to the Stores table
    FOREIGN KEY (store_id) REFERENCES stores(store_id)  -- Store assignment, nullable for central office
);

-- Create the Products (Productos) table
CREATE TABLE products (
    product_id INT AUTO_INCREMENT PRIMARY KEY,  -- Unique product identifier
    code CHAR(10) UNIQUE NOT NULL,  -- Unique product code, 10 characters
    name VARCHAR(255) NOT NULL,
    photo VARCHAR(255),  -- Optional product image
    color VARCHAR(50),
    size VARCHAR(10)  -- Product size
);

-- Create the Products_Stores (Productos_Tienda) table (for product inventory in each store)
CREATE TABLE product_store (
    product_code CHAR(10),  -- Foreign key to the Products table
    store_id VARCHAR(20),  -- Foreign key to the Stores table
    stock INT NOT NULL DEFAULT 0,  -- Stock in the store, default is 0
    PRIMARY KEY (product_code, store_id),  -- Composite primary key: one product in many stores
    FOREIGN KEY (product_code) REFERENCES products(code),
    FOREIGN KEY (store_id) REFERENCES stores(store_id)
);

INSERT INTO stores (store_id, code, address, city, province, enabled)
VALUES ('store001', 'S001', '123 Main St', 'Metropolis', 'Central', TRUE);

INSERT INTO stores (store_id, code, address, city, province, enabled)
VALUES ('normal002', 'S002', '2222 St', '222', 'NORMAL', TRUE);

INSERT INTO users (user_id, username, password, role, first_name, last_name, enabled, store_id)
VALUES (2, 'normal', 'normal', 1, 'normal', 'normal', 1, 'normal002');

SELECT * FROM stores;
SELECT * FROM users;

