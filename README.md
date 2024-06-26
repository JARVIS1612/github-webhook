# github-webhook

This project demonstrates a Flask application connected to MongoDB using pymongo. It includes webhook event handling from GitHub and fetching data based on timestamps.

## Prerequisites

Before running the application, ensure you have the following installed:

-   Python (3.x recommended)
-   MongoDB
-   pip package manager

## Setup

1. **Clone the repository:**

    ```bash
    git clone <repository_url>
    cd <project_directory>
    ```

2. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

3. **Set up environment variables:**
   Create a `.env` file in the root directory of your project and add the following:

    ```plaintext
     MONGO_URL=<your_mongodb_connection_string>
     DB_NAME=<your_database_name>
    ```

    Replace <your_mongodb_connection_string> with your MongoDB connection string and <your_database_name> with the name of your MongoDB database.

4. **Run the application:**

    ```bash
    python app.py
    ```

    The Flask application will start running locally on http://localhost:5000 by default.

## Features

-   **Webhook Event Handling:** Receive events from GitHub (push, pull_request) and store them in MongoDB.
-   **Data Fetching:** Fetch data from MongoDB based on timestamp parameters.

## Project Structure

````bash
├── templates
   └── index.html             # Main html file to display actions
├── app.py                    # Main Flask application file
├── db.py                     # MongoDB connection setup
├── requirements.txt          # Python dependencies
├── .env                      # Environment variables configuration
└── README.md                 # Project documentation
````

## Usage
- **Event Receiver Endpoint:**
    - **URL:** */recieveEvents*
    - **Method:** POST
    - **Description:** Receives webhook events from GitHub and stores them in MongoDB.

- **Fetch Data Endpoint:**

    - **URL:** */fetch_data*
    - **Method:** GET
    - **Parameters:** last_time (timestamp in "%a, %d %b %Y %H:%M:%S %Z" format)
    - **Description:** Retrieves data from MongoDB based on the provided timestamp.