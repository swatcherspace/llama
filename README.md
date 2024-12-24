# SEC Filings Insights - Django Application

This project allows you to process SEC EDGAR Annual Financial Filings and generate trending insights using the Llama-2 model, which has been trained on 7 billion parameters. The system processes a `.csv` file containing SEC filings and outputs insights about the data.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Setup](#setup)
3. [Dataset](#dataset)
4. [APIs](#apis)
5. [Generating Insights](#generating-insights)
6. [Usage](#usage)
7. [License](#license)

## Prerequisites

Before you start, make sure you have the following installed:

- **Python 3.11+**
- **Django 4.1+**
- **Docker (Optional for Docker setup)**
- **Curl (to interact with APIs)**
- **HuggingFace Llama-2 Model (7B params)**

## Setup

1. **Clone the Repository:**

   First, clone the repository where this Django app is located.

   ```bash
   git clone https://github.com/your-repo/your-django-app.git
   cd your-django-app
   ```

2. **Install Dependencies:**

   Create a virtual environment and install the dependencies.

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Run Migrations:**

   Apply the migrations to set up your database.

   ```bash
   python manage.py migrate
   ```

4. **Start the Django Development Server:**

   Now, you can run the server.

   ```bash
   python manage.py runserver
   ```

   The application will be accessible at `http://127.0.0.1:8000/`.

## Dataset

To download the SEC EDGAR Annual Financial Filings dataset:

1. **Download the Dataset:**
   - Go to the Kaggle dataset page: [SEC EDGAR Annual Financial Filings 2021](https://www.kaggle.com/datasets/pranjalverma08/sec-edgar-annual-financial-filings-2021)
   - Download the dataset file.

2. **Place the Dataset in the Django App Folder:**
   - After downloading, place the `sec_edgar_annual_financial_filings_2021.csv` file in the `secfilings/` folder inside your Django app.

## APIs

### 1. **Generate CSV File of SEC Filings:**

   This API will process the data and generate a `sec_filings.csv` file.

   **Request:**
   ```bash
   curl -X GET http://127.0.0.1:8000/filings/generate-csv/
   ```

   **Response:**
   - The server will generate a `.csv` file that contains the processed SEC filings data. 

---

### 2. **Generate Insights Using Llama-2 Model:**

   This API will accept the `sec_filings.csv` file and generate insights based on the data using the Llama-2 model.

   **Request:**
   ```bash
   curl -X POST -F 'file=@path_to_your_csv_file/sec_filings.csv' http://127.0.0.1:8000/filings/generate-insights/
   ```

   **Response:**
   - The server will process the file using the Llama-2 model, which will analyze the data and generate insights. The results will be saved in a temporary `.txt` file.

---

### 3. **Retrieve Insights (Asynchronously):**

   The generated insights will be retrieved by frontend APIs in chunks. You can implement long-polling or asynchronous fetching based on your infrastructure.

---

## Llama-2 Model

To use the Llama-2 model, download the `.gguf` file from HuggingFace and place it in the `secfilings/` folder. You can download the model from [HuggingFace Llama-2 7B Model](https://huggingface.co/).

Once downloaded, place the `llama-2-7b.Q2_K.gguf` file in the `secfilings/` folder.

---

## Usage

1. **Download the Dataset** from Kaggle.
2. **Place the `.csv` file** in the `secfilings/` folder.
3. **Generate the CSV file** using the provided API:
   ```bash
   curl -X GET http://127.0.0.1:8000/filings/generate-csv/
   ```
4. **Download the Llama-2 model** from HuggingFace and place the `.gguf` file in the `secfilings/` folder.
5. **Generate insights** by sending a POST request:
   ```bash
   curl -X POST -F 'file=@path_to_your_csv_file/sec_filings.csv' http://127.0.0.1:8000/filings/generate-insights/
   ```
6. **Retrieve the insights** from the frontend using asynchronous methods.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
