# Netflix Content Recommendation System
### **Coursework: Deploying Analytics Pipeline**

![](https://github.com/SnehaEkka/BA882-Netflix-Analytics-Pipeline/blob/main/Netflix-banner-image.png)

A repository for a team project on "Deploying Analytics Pipelines" that involves three phases:
- Phase 1: Data Ops (ETL/ELT and Warehousing)
- Phase 2: ML Ops
- Phase 3: LLM Ops

## 📌 Project Overview
### Motivation
With the rise of streaming platforms, content recommendation has become crucial for improving user experience. This project focuses on enhancing Netflix's recommendation system by integrating Machine Learning (ML) techniques with Large Language Models (LLMs) to provide more personalized and data-driven recommendations.

### Business Problem
The project aims to explore several key business problems:
1. **Content Performance Analysis:** How do Netflix's most popular shows and movies perform over time, and what factors contribute to their success?
2. **Marketing Effectiveness:** Is there a correlation between Netflix's YouTube promotional activities and content performance on the Netflix platform?
3. **Audience Engagement:** How does audience engagement on YouTube (likes, comments, shares) relate to a show or movie's popularity on Netflix?
4. **Content Trend Prediction:** Can we use historical data from both sources to predict future trends in content popularity?
5. **Regional Preferences:** How do content preferences differ across regions, and how does Netflix tailor its YouTube marketing to different geographical audiences?
6. **Genre Analysis:** Which genres perform best on Netflix, and how does this align with the genre focus in their YouTube marketing?

Netflix offers a vast catalog of content, making it difficult for users to discover new shows and movies. Traditional recommendation systems rely on watch history, but our approach extends beyond that by leveraging content metadata and user feedback. We aim to develop a hybrid recommendation engine that improves content discoverability and engagement.

### Data Sources
Our project incorporates multiple data feeds:
- **Netflix Top 10 Weekly Data** – Provides insights into trending content. \
   *Link: https://www.netflix.com/tudum/top10/*
- **Netflix API Data** – Contains metadata about Netflix content. \
   *Link: https://rapidapi.com/movie-of-the-night-movie-of-the-night-default/api/streaming-availability*
- **YouTube API Data** – Captures engagement metrics from trailers and promotional videos. \
   *Link: https://console.cloud.google.com/marketplace/product/google/youtube.googleapis.com?project=ba882-inclass-project*

---

## 🚀 Phase 1: Data Collection & Initial ETL
### Accomplishments
- **Data Extraction & Storage:**
  - Integrated Netflix, YouTube, and other datasets.
  - Stored data in **DuckDB via MotherDuck** for efficient querying.
- **Entity-Relationship Diagram (ERD) Creation:**
  - Designed a schema to map relationships between datasets.
    ![ERD](Data_Model_ERD.png)
- **ETL Pipeline Development:**
  - Built an **EtLT** (Extract, Transform, Load, then Transform) pipeline.
  - Converted date formats and extracted relevant features from unstructured data.
- **Visualization with Superset:**
  - Created dashboards for analyzing viewership trends.
    ![Dashboard](Superset_Dashboard.jpeg)

### Challenges & Solutions
- **Data Inconsistencies:** Some datasets lacked unique identifiers, requiring fuzzy matching techniques.
- **Storage Optimization:** Transitioned from CSV-based storage to **MotherDuck** for better scalability.

🔗 [Phase 1 Presentation Deck](https://www.canva.com/design/DAGUIVPifwA/-WOV-uiLMT-rBssArXQrYw/edit)

---

## 🔄 Phase 2: Enhancing ETL & Building Machine Learning Models
### Accomplishments
- **ETL Optimization:**
  - Transitioned from **EtLT to ETL**, ensuring transformations occurred before loading.
  - Standardized title formatting to align across datasets.
- **Data Upsertion Strategy:**
  - Introduced **Insert Logic** to prevent missing historical records.
- **Machine Learning Model Development:**
  - Built a **KNN-based recommendation system** using cosine similarity.
  - Engineered features such as **cast, director, genre, and descriptions** for content similarity.
- **Prefect Pipeline Deployment:**
  - Automated daily ETL and model training flows using **Prefect Cloud**.
  - 📌 **Add Prefect Pipeline Screenshot Here**
- **Dataset Expansion:**
  - Backfilled data for 2020-2021 to enhance model accuracy.

### Challenges & Solutions
- **Prefect Deployment Errors:** Fixed entrypoint issues by restructuring folders.
- **Feature Bias:** Removed runtime as a feature to prevent duration-based recommendations.

🔗 [Phase 2 Presentation Deck](https://www.canva.com/design/DAGWRog81pI/aznUdOi6MgHU1gRZUSaA_g/edit)

---

## 🤖 Phase 3: LLM Integration & UI Development
### Accomplishments
- **LLM Integration for Personalized Recommendations:**
  - Incorporated **Gemini 1.5 Pro** to refine recommendations based on user feedback.
  - Users can enter preferences to enhance recommendations dynamically.
- **Automated ML Pipeline:**
  - Integrated model training and storage into **MotherDuck**.
  - Archived model metrics for tracking improvements.
  - 📌 **Add Netflix Pipeline Image**
- **Streamlit Application Development:**
  - Built an interactive UI for users to receive recommendations and provide feedback to enhance the recommendations further.
  - Added interactive visualizations to showcase content trends.
  - 📌 **Add Netflix Analytics Page Screenshot Here**

### Challenges & Solutions
- **Model Overfitting:** High accuracy suggested potential overfitting; addressed by balancing feature weights.
- **Scalability Concerns:** Used **Google Cloud Run & Prefect** to streamline ML deployment.

🔗 [Phase 3 Presentation Deck](https://www.canva.com/design/DAGY5lGoI4o/MsgTkczwbwXbCAuP1FvooQ/edit)

---

## 🔮 Future Scope
- Complete **Streamlit UI** development for an intuitive recommendation experience.
- Implement **Sentiment Analysis** on movie descriptions and user reviews.
- Explore **LLM-based summarization** to enhance metadata for recommendations.
- Compare **custom ML models vs. LLM-generated recommendations** for performance evaluation.

---

## 🛠️ Tools Used
| Tool/Platform | Purpose |
|--------------|---------|
| **Python** | Data Processing & ML Development |
| **DuckDB / MotherDuck** | Data Storage & Querying |
| **Google Cloud Storage** | Storing Data & Model Artifacts |
| **Google Cloud Run** | Deploying Recommendation Models |
| **Google Cloud Secret Manager** | Securing API Keys & Credentials |
| **YouTube API** | Extracting Trailer & Engagement Data |
| **Netflix API** | Fetching Movie & Show Metadata |
| **Prefect Cloud** | Automating ETL & ML Pipelines |
| **Streamlit** | Building User Interface |
| **Lucidchart** | ERD Diagram |
| **Apache Superset** | Data Visualization & Analytics |
| **Gemini 1.5 Pro LLM** | Generating Personalized Recommendations |

---

## 📌 Project Links
- **GitHub Repository:** [GitHub-Team05](#) (Attach Link)
- **Streamlit Application:** [Streamlit-Team05](https://streamlit-poc-614716406197.us-central1.run.app/)
