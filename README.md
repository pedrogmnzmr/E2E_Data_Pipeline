# E2E_Data_Pipeline
End-to-End Data Pipeline / Data Engineering

## Introduction

In today’s data-driven world, businesses need robust, scalable, and efficient systems to handle the ever-growing volume of data. This project demonstrates how to build a production-grade end-to-end data engineering pipeline  that seamlessly integrates data ingestion, real-time streaming, processing, and storage. Leveraging cutting-edge technologies like Apache Airflow , Apache Kafka , Apache Spark , and Cassandra , this solution is designed to meet the demands of modern enterprises.

## System Architecture

![System Architecture](https://github.com/pedrogmnzmr/pipeline_end_to_end/blob/main/E2E.jpg)

Our architecture is designed to deliver a seamless flow of data across the pipeline: 

1. Data Source :   
    Fetches random user data from the randomuser.me API to simulate real-world data ingestion scenarios.
        

2. Apache Airflow :   
    Acts as the orchestrator , automating the pipeline workflow.  
    Extracts data from the API and stores it in a PostgreSQL database  for initial persistence.
        

3. Apache Kafka & Zookeeper :   
    Streams data from PostgreSQL to downstream systems in real-time.  
    Ensures reliable message delivery and distributed synchronization with Zookeeper.
        

4. Control Center & Schema Registry :   
    Monitors Kafka streams and enforces schema validation for consistent data formats.
        

5. Apache Spark :   
    Processes data at scale using distributed computing.  
    Transforms raw data into actionable insights with its master-worker architecture .
        

6. Cassandra :   
    Stores processed data in a highly scalable, distributed NoSQL database optimized for high availability and performance.
         

## What You'll Learn

- Orchestration : Learn how to automate complex workflows with Apache Airflow .
- Streaming : Master real-time data streaming with Apache Kafka  and Zookeeper .
- Processing : Unlock the power of distributed computing with Apache Spark .
- Storage : Discover how to store and query large datasets efficiently using Cassandra  and PostgreSQL .
- DevOps : Understand how to containerize your entire pipeline with Docker  for seamless deployment and scalability.

## Technologies Used

- Apache Airflow : Workflow orchestration and scheduling.
- Python : Scripting and automation.
- Apache Kafka : Real-time data streaming.
- Apache Zookeeper : Distributed coordination and synchronization.
- Apache Spark : Distributed data processing.
- Cassandra : Scalable NoSQL database for high-velocity data.
- PostgreSQL : Relational database for structured data storage.
- Docker : Containerization for portability and scalability.
    

