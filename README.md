# Cassandra Cluster with Python Client

This project sets up a multi-node **Cassandra cluster using Docker Compose** and includes a **Python client** application to interact with the database. It is designed to run entirely inside Docker containers for ease of setup and portability.

---

## 📁 Project Structure

```text
.
├── docker-compose.yaml             # Defines Cassandra nodes and Python client service
├── cassandra_client/              # Python client application
│   ├── cassandraSimpleClientApp.py  # Main script for database operations
│   ├── Dockerfile                 # Dockerfile for building the client image
│   ├── requirements.txt           # Python dependencies
│   ├── .dockerignore              # Docker ignore file
├── start-cassandra-cluster.ps1    # PowerShell script to start the cluster on Windows
├── run-cassandra-cluster.bat      # Batch file to launch the PowerShell script
├── .env                           # Environment variable configuration
├── .gitignore                     # Git ignore rules
├── LICENSE                        # License file
└── README.md                      # Project documentation
```

---

## ✅ Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop)
- Windows PowerShell (for script users)
- On Linux/macOS: Docker and Docker Compose CLI

---

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/mirslivjce/Cassandra_projects.git
cd Cassandra_projects
```

### 2. Configure Environment Variables

Edit the `.env` file to set up cluster-related values:

```env
CLUSTER_HOSTS=cassandra1,cassandra2,cassandra3,cassandra4
CASSANDRA_PORT=9042
```

Ensure the hostnames match those defined in `docker-compose.yaml`.

---

## ▶️ Starting the Cluster

### On Windows

Double-click or run from terminal:

```cmd
run-cassandra-cluster.bat
```

Or run directly via PowerShell:

```powershell
PowerShell -NoProfile -ExecutionPolicy Bypass -File start-cassandra-cluster.ps1
```

### On Linux/macOS

Use Docker Compose directly:

```bash
docker compose up -d
```

---

## 🔍 Health Check Process

Each Cassandra node uses a built-in health check defined in `docker-compose.yaml`:

- **Command**: `cqlsh -e "SELECT release_version FROM system.local"`
- **Interval**: 30 seconds
- **Start Period**: 300 seconds
- **Timeout**: 20 seconds
- **Retries**: 5

The Python client waits for the last Cassandra node to be healthy before starting.

---

## 💻 Using the Python Client

To access and run the client application:

```bash
docker exec -it cassandra-client bash
python cassandraSimpleClientApp.py
```

The client script demonstrates basic CRUD operations using the `cassandra-driver`.

---

## ⛔ Stopping the Cluster

To stop and remove all running containers:

```bash
docker compose down
```

---

## 🧰 Included Scripts

### `start-cassandra-cluster.ps1`

A PowerShell script to start the cluster on Windows. It:

1. Checks if Docker is installed
2. Launches Docker Desktop
3. Waits for Docker to be ready
4. Runs `docker compose up -d`

#### Usage:

```powershell
PowerShell -NoProfile -ExecutionPolicy Bypass -File start-cassandra-cluster.ps1
```

### `run-cassandra-cluster.bat`

Simple `.bat` wrapper to run the PowerShell script. Just double-click it.

---

## 🐍 Python Client Features

- Create keyspaces and tables
- Insert, update, delete records
- Query data from Cassandra using Python

---

## 📌 Notes

- Cluster is configured with **4 nodes** by default. You can increase or reduce this by modifying `docker-compose.yaml`.
- Ensure the `.env` file matches the container hostnames defined in the Compose file.
- Scripts are designed for **Windows users**, but Docker Compose works cross-platform.

---

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for full details.