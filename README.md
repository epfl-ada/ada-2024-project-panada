# ada-2024-project-panada

### Project Idea
We want to analyze YouTube’s Evolution into a Professional Platform for Creators.
When YouTube was created in 2005, the platform was not professionalized but it became
now for many people, their main source of income. This project explores how YouTube
evolved from a casual video-sharing site into a professional platform for full-time
creators. Using the channel metadata and time-series data, we would analyze how the
average size of successful channels (subscribers and views) has changed over time and
identify signals of professionalization, such as increased upload frequency and consistent
content themes. Additionally, we would explore which content categories (e.g., Gaming,
Education) have seen the most professional growth, using the video metadata to track
shifts in production quality and upload patterns. We’d correlate these changes with the
introduction of monetization features (e.g., AdSense) and algorithm updates, to map out
the timeline of YouTube’s transformation into a career-driven platform.


## Data Cleaning Pipeline

Our data cleaning process aims to ensure a good quality input for our analysis by handling missing values effectively. The following steps outline the cleaning and preprocessing approach applied to our dataset:

We started by identifying and evaluating missing values across the dataset. We also checked for inconsistencies or unusual entries that may require specific handling.

1. **NaN Removal**:
   - Removal of rows with a high proportion of missing values (>25% NaNs).
   - For entries with low to moderate NaNs, we retained data where possible to preserve dataset integrity.

2. **K-Nearest Neighbors (KNN) Imputation**:
   - For remaining missing values, we used KNN imputation to predict and fill missing entries based on similarities between data points.
   - Each missing value is replaced by the weighted average of its K-nearest neighbors, with K set to an optimal value (5 in our case) after testing for best imputation results.


### Tasks and Responsibilities

| Task Description                                                                                       | Assigned Member |
|--------------------------------------------------------------------------------------------------------|---------------------|
| Select and finalize project topic                                                                      |    Everyone         |
| Define research questions and project goals                                                            |    Koami            |
| Develop data preprocessing pipeline (data cleaning, handling missing values, format adjustments)       |    Koami            |
| Perform initial descriptive analysis (distributions, correlations, etc.)                               |    Koami            |
| Identify potential additional datasets and assess feasibility                                          |    Val              |
| Document proposed methods, including mathematical details and alternatives                             |    Adam                 |
| Structure and organize the GitHub repository                                                           |    Val              |
| Create README with project title, abstract, and research questions                                     |    Antoine          |
| Develop and document code in Jupyter notebook                                                          |    Everyone         |
| Conduct final review and refine README, methods, and notebook documentation                            |    Everyone         |
| Submit finalized GitHub repository                                                                     |                     |


### Task Deadlines

| Task Description                                                                                       | Deadline           |
|--------------------------------------------------------------------------------------------------------|---------------------|
| Select and finalize project topic                                                                      |   06.11                  |
| Define research questions and project goals                                                            |   09.11             |
| Develop data preprocessing pipeline (data cleaning, handling missing values, format adjustments)       |     11.11                |
| Perform initial descriptive analysis (distributions, correlations, etc.)                               |          11.11           |
| Identify potential additional datasets and assess feasibility                                          |          12.11           |
| Document proposed methods, including mathematical details and alternatives                             |          12.11           |
| Structure and organize the GitHub repository                                                           |            13.11         |
| Create README with project title, abstract, and research questions                                     |               13.11      |
| Develop and document code in Jupyter notebook                                                          |   12.11                  |
| Conduct final review and refine README, methods, and notebook documentation                            |        14.11             |
| Submit finalized GitHub repository                                                                     |      14.11               |

