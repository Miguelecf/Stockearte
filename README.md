# Stockearte

## Setting Up the Project

### 1. Set Up the Database

First, execute the following SQL script to set up the database schema:

```sql
create schema store_system;
use store_system;
```

### 2. Install Python Dependencies(SERVER)

Install the required Python packages listed in `requirements.txt`:

```bash
cd server
pip install -r requirements.txt
```

### 3. Set Up the Database

Before running the following script, **remember to modify the `DATABASE_URL` in `entities/base.py`** to match your database credentials:

```python
DATABASE_URL = "mysql+pymysql://user:password@localhost:3306/store_system"
```

#### Environment Variables

Define the following environment variables in a `.env` file at the root of the server project:

```bash
DB_USER=root
DB_PASSWORD=1612
DB_HOST=localhost
DB_PORT=3306
DB_NAME=store_system
```

After updating, run the following command to create the necessary database tables:

- pip install cryptography
- pip install python-dotenv

```bash
cd /stockearte
python -m server.utils.create_db
```

### 4. Generate gRPC Code

Generate the gRPC code from your `.proto` files:

```bash
cd server
cd utils
python generates_proto.py
```

### 5. Run the gRPC Server

Start the gRPC server:

```bash
cd /stockearte
python -m server.grpc.grpc_server
```

### 6. Set Up and Run the TypeScript Client

1. **Navigate to the client directory:**

   ```bash
   cd client
   ```

2. **Install the required Node.js packages:**

   Ensure that you have Node.js(node v.21) and npm installed. Then, install the dependencies listed in `package.json`:

   ```bash
   npm install
   ```

3. **Start the client:**

   ```bash
   npm start
   ```

This will start the TypeScript client, which will connect to the gRPC server running on your machine.

### Notes

- Make sure that the gRPC server is running before starting the client.
- If you encounter any issues with the installation or running the server/client, please check the respective documentation for additional troubleshooting.
