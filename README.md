# Cassandra Cluster with Python Client

This project sets up a Cassandra cluster using Docker and provides a Python client application to interact with the cluster. The setup includes multiple Cassandra nodes and a Python client for database operations, designed to run inside the Docker environment.

## Project Structure

```
.
├── docker-compose.yaml       # Docker Compose file to define the cluster and client services
├── cassandra_client/         # Directory containing the Python client application
│   ├── cassandraSimpleClientApp.py  # Main Python script for database operations
│   ├── Dockerfile            # Dockerfile for the Python client
│   ├── requirements.txt      # Python dependencies for the client
│   ├── .dockerignore         # Docker ignore file for the Python client
├── .env                      # Environment variables for configuration
├── .gitignore                # Git ignore file
```

## Prerequisites

- Docker and Docker Compose installed on your system.

## Setup Instructions

### 1. Clone the Repository

```bash
git https://github.com/mirslivjce/Cassandra_projects.git
cd Cassandra_projects
```

### 2. Configure Environment Variables

Update the `.env` file with your desired configuration. For example:

```
CLUSTER_HOSTS=cassandra1,cassandra2,cassandra3,cassandra4
CASSANDRA_PORT=9042
```

### 3. Start the Cluster

Run the following command to start the Cassandra cluster and the Python client:

```bash
docker-compose up -d
```

### 4. Health Check Process

Each Cassandra node is configured with a health check to ensure it is ready before dependent services start. The health check uses the `cqlsh` command to query the Cassandra system table. The health check parameters are defined in the `docker-compose.yaml` file:

- **Test Command**: `cqlsh -e "SELECT release_version FROM system.local"`
- **Interval**: 30 seconds
- **Start Period**: 300 seconds
- **Timeout**: 20 seconds
- **Retries**: 5

The `depends_on` directive in the `docker-compose.yaml` file ensures that each node waits for the previous node to pass its health check before starting. Similarly, the Python client waits for the last Cassandra node to be healthy before starting.

### 5. Interact with the Cluster

The Python client application (`cassandraSimpleClientApp.py`) is designed to run inside the Docker environment. To access the client container:

```bash
docker exec -it cassandra-client bash
```

Once inside the container, you can run the Python script to perform CRUD operations on the Cassandra database:

```bash
python cassandraSimpleClientApp.py
```

### 6. Stop the Cluster

To stop and remove the containers, run:

```bash
docker-compose down
```

## Python Client

The Python client uses the `cassandra-driver` library to connect to the Cassandra cluster. It supports the following operations:

- Create keyspaces and tables.
- Insert, update, and delete records.
- Query data from the database.

## Notes

- The cluster is configured with 4 nodes. You can modify the `docker-compose.yaml` file to adjust the number of nodes.
- Ensure that the `CLUSTER_HOSTS` environment variable matches the node hostnames defined in the `docker-compose.yaml` file.

## License

This project is licensed under the MIT License. See the LICENSE file for details.