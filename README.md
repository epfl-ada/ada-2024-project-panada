# From Hobby to Profession: The Evolution of YouTube as a Career Platform

## Abstract

Since its inception in 2005, YouTube has transformed from a casual video-sharing site into
a professional platform supporting countless full-time creators. This project investigates
YouTube’s evolution by examining how the average size of successful channels (measured in
subscribers and views) has changed over time. Using channel metadata and time-series data,
we analyze key indicators of professionalization, such as increased upload frequency, content
consistency, and strategic engagement practices. Additionally, we explore which content categories
(e.g., Gaming, Education) have driven the platform’s growth by tracking shifts in production quality,
audience reach, and upload patterns in the video metadata. Through this lens, we map out YouTube’s
transition into a viable career platform and highlight the broader industry trends that support
the professionalization of digital content creation.

## Research Questions

- How has the frequency and consistency of content creation evolved over time across different channel categories?

- How has creator content strategy evolved to reflect professional monetization approaches?

- Which categories led YouTube's professionalization, and how did professional practices spread?

- How does investment in content production reflect the transition from hobby to profession?

- How has community management evolved from casual interaction to professional engagement strategies?

## Proposed additional datasets (if any)

TODO: Waiting for Valentine's update

## Methods

TODO: Waiting for Adam's update

## Proposed timeline

#### Step 1: Data exploration

#### Step 2: Data cleaning

#### Step 3: Data Analysis

#### Step 4: Compilation of all our analysis

## Organization within the team

## Questions for TA (optional)

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

