# Event Experience Analytics

## Overview

**Event Experience Analytics** is a comprehensive platform designed to empower event organizers with actionable insights in real time. By leveraging data from IoT sensors, social media feeds, feedback forms, and vendor sales, this system provides an integrated dashboard to monitor key metrics, optimize resources, and enhance attendee satisfaction dynamically.

---

## Features

- **IoT-Driven Crowd Monitoring**: Tracks crowd density in event zones to ensure comfort and safety.
- **Sentiment Analysis**: Processes social media posts to gauge attendee satisfaction.
- **Feedback Aggregation**: Analyzes structured feedback to identify improvement areas.
- **Vendor Sales Insights**: Monitors inventory and sales to prevent stockouts.
- **Dynamic Visualization**: Presents real-time metrics on a QuickSight dashboard for actionable insights.

---

## Architecture
![architecture-diagram](https://github.com/user-attachments/assets/074ee225-667d-4406-846b-dc5d468bf06e)


### Key Components

1. **Data Sources**:
   - IoT Sensors: Zone-specific crowd density data.
   - Social Media: Mocked posts for sentiment analysis.
   - Feedback Forms: Ratings and comments categorized by attendee feedback.
   - Vendor Sales: Real-time inventory and sales metrics.

2. **Data Processing**:
   - **Apache Flink**:
     - Aggregates IoT data for average crowd density.
     - Performs sentiment analysis on social media.
     - Computes average ratings for feedback categories.
     - Tracks inventory levels and sales trends.

3. **Data Storage**:
   - **Amazon S3**: Centralized storage for processed data organized by source.

4. **Visualization**:
   - **Amazon QuickSight**:
     - Interactive dashboards to visualize key metrics.
     - Conditional formatting for critical insights (e.g., overcrowded zones).

---

## Getting Started

### Prerequisites

- **Apache Flink** (latest version)
- **AWS CLI** for syncing data to S3
- **Amazon QuickSight** for visualization

### Setup Instructions

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-repo-name/event-experience-analytics.git
   cd event-experience-analytics
   ```

2. **Configure AWS**:
   - Set up your AWS credentials:
     ```bash
     aws configure
     ```
   - Ensure your S3 bucket is ready:
     ```bash
     aws s3 mb s3://eventanalytics/
     ```

3. **Start Flink Jobs**:
   - Run individual Flink jobs for each data source:
     ```bash
     sbt run IoTJob
     sbt run FeedbackJob
     sbt run SalesJob
     sbt run SocialMediaJob
     ```

4. **Sync Data to S3**:
   ```bash
   aws s3 sync /path/to/local/data s3://eventanalytics/
   ```

5. **Visualize in QuickSight**:
   - Create datasets using the provided JSON manifest files.
   - Build dashboards for metrics like crowd density, sentiment analysis, feedback ratings, and inventory levels.

---

## Sample Outputs

### Dashboard Screenshots

<img width="1409" alt="image" src="https://github.com/user-attachments/assets/9cbf9ebf-5ccb-4ccf-8378-71ccc14f5970" />

<img width="1392" alt="image" src="https://github.com/user-attachments/assets/af6d8baa-52f2-44ef-845c-4707ded6d5f9" />


### Code Snippets

#### Sample IoT Data Processing in Flink:
```scala
val averageIoTDensity = iotSource
  .map(data => (data.zone_id, (data.crowd_density.toDouble, 1)))
  .keyBy(_._1)
  .timeWindow(Time.seconds(20))
  .reduce((a, b) => (a._1, (a._2._1 + b._2._1, a._2._2 + b._2._2)))
  .map(entry => {
    val zoneId = entry._1
    val (totalDensity, count) = entry._2
    val averageDensity = if (count == 0) 0.0 else totalDensity / count
    SimplifiedIoT(zoneId, averageDensity, java.time.Instant.now.toString)
  })
```
