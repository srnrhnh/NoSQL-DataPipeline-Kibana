<div align='center'>
    <h1><b>NoSQL-DataPipeline-Kibana</b></h1>
</div>

This repository showcases a comprehensive data workflow, featuring pipeline automation with Apache Airflow, data validation using Great Expectations, data preparation and integration for NoSQL databases, and data visualization with Kibana. It highlights an efficient approach to managing, validating, and analyzing data.

## Data Sources 📊
- The dataset used in this project comes from [Kaggle](https://www.kaggle.com/datasets/aungpyaeap/supermarket-sales).

## Technologies Used ⚙️
- **Python** (data preprocessing and workflow management)
- **Apache Airflow** (pipeline automation and orchestration)
- **PostgreSQL** (data extraction)
- **Elasticsearch** (data indexing and search)
- **Kibana** (data visualization)
- **Pandas** (data cleaning and manipulation)

## Method 🚀
- Data Extraction: 
    - Retrieve data from PostgreSQL using SQL queries
- Data Cleaning: 
    - Remove duplicates and normalize column names
    - Handle missing values by imputing medians for numerical data and modes for categorical data.
- Data Loading: 
    - Send cleaned data to Elasticsearch for indexing.
- Data Visualization: 
    - Use Kibana to create dashboards and visualize trends in the indexed data.
- Pipeline Automation:
    - Schedule and orchestrate tasks using Apache Airflow.    

## **Key Insights & Conclusions 🧠**
1. **Workflow Automation:**
   - Airflow automates the entire ETL process, minimizing manual effort and ensuring consistency.

2. **Enhanced Data Insights:**
   - Kibana dashboards provide actionable insights and easy-to-understand visualizations

3. **Areas for Improvement:**
   - Expand Kibana visualizations with more advanced analytics

## Directory 📦

NoSQL-DataPipeline-Kibana
|
├── airflow
      ├── dags
           ├── Airflow_DAG.py
           └── data_raw.csv
      ├── env
      └── airflow_ES.yaml
├── /images
      ├── introduction & objective (1).png
      ├── introduction & objective (2).png
      ├── introduction & objective (3).png
      ├── plot & insight 01.png
      ├── plot & insight 02 (1).png
      ├── plot & insight 02 (2).png
      ├── plot & insight 03.png
      ├── plot & insight 04.png
      ├── plot & insight 05.png
      ├── plot & insight 06.png
      ├── plot & insight 07.png
      └── kesimpulan.png      
├── great_expectation.ipynb
└── query_SQL.txt

---

💡Feel free to open an issue or submit a pull request if you have suggestions for improvements!