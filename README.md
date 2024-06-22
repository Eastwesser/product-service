# Product Service

## Description

Product Service is a microservice for managing products within the Candy-Star application, built using FastAPI,
PostgreSQL, Redis, and RabbitMQ.

## Requirements

- Python 3.10
- PostgreSQL
- Redis
- RabbitMQ
- Docker (for running RabbitMQ)

## Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/Eastwesser/product-service.git
    ```

2. Create and activate a virtual environment:

    ```sh
    python -m venv .venv
    .venv\Scripts\activate
    ```

3. Install dependencies:

    ```sh
    pip install -r requirements.txt
    ```

4. Create and configure the `.env` file based on `.env.example`:

    ```sh
    cp .env.example .env
    ```

## Starting Services

### PostgreSQL

Ensure PostgreSQL is installed and running. Configure the connection in the `.env` file.

### Redis

Install and start the Redis server:

```sh
    # On Ubuntu
    sudo apt update
    sudo apt install redis-server
    sudo systemctl start redis-server
```

Check the status of Redis:

```sh
sudo systemctl status redis-server
```

## RabbitMQ

Start RabbitMQ using Docker:

```sh
docker run -d --hostname my-rabbit --name some-rabbit -p 5672:5672 -p 15672:15672 rabbitmq:3-management
```

### Running the Application

Start the application:

```sh
uvicorn app.main:app --reload
```

The application will be available at http://127.0.0.1:8000.

API documentation will be available at http://127.0.0.1:8000/docs.

## Project Structure

```markdown
product-service/
├── app/
│ ├── __init__.py
│ ├── main.py
│ ├── db/
│ │ ├── __init__.py
│ │ ├── session.py
│ ├── models/
│ │ ├── __init__.py
│ │ ├── product.py
│ ├── routers/
│ │ ├── __init__.py
│ │ ├── product.py
│ └── schemas/
│ ├── __init__.py
│ ├── product.py
├── .env
├── .env.example
├── requirements.txt
└── README.md
```

### API Request Examples

Get All Products

```sh
GET /products
```

Create a New Product

```sh
POST /products
{
  "name": "Candy Star",
  "description": "A delicious candy star.",
  "price": 1.99
}
```

Get a Product by ID

```sh
GET /products/{product_id}
```

Update a Product

```sh
PUT /products/{product_id}
{
  "name": "Updated Candy Star",
  "description": "An even more delicious candy star.",
  "price": 2.99
}
```

Delete a Product

```sh
DELETE /products/{product_id}
```

### Contact

For questions and suggestions:

Me - eastwesser@gmail.com

GitHub - https://github.com/Eastwesser

© 2024 Candy-Star. All rights reserved.
