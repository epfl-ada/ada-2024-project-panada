# From Hobby to Profession: The Evolution of YouTube as a Career Platform

![Alt text](./youniverse.png "YouNiverse")

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

#### 1. Growth Trends Analysis

- Objective: Quantify how the scale of content creation and audience size has grown over time, reflecting increased professionalization.

- Methods:
   - Channel and Video Counts Over Time: Calculate the cumulative count of channels and videos, observing growth rates and shifts, especially around key dates (e.g., introduction of monetization features, we could find these informations on the web without needed an additional dataset).
   - Time-Series Analysis of Subscribers and Views: For each channel category, use time-series analysis to model growth in average views and subscribers over time, noting periods with significant increases.

#### 2. Content Production and Consistency Analysis

- Objective: Examine whether creators adopted professional practices, such as regular content uploads.

- Methods:
   - Posting Frequency by Category: Track average weekly upload frequency per category over time, identifying categories where consistent posting became prominent.
   - Variance Analysis in Posting Patterns: Lower variance over time can indicate regular posting schedules, a hallmark of professional content creators.
   - Rolling Averages of Posting Frequency: Apply rolling averages to capture trends in posting frequency, showing how channels transitioned to more consistent content schedules.

#### 3. Engagement and Audience Interaction Trends

- Objective: Measure the growth in audience engagement as an indicator of professional interaction strategies.

- Methods:
   - Comment Volume and Unique Commenter Counts Over Time: Track increases in both comment volume and the number of unique commenters, analyzing growth as a sign of professional audience management.
   - Engagement-to-Growth Correlation: Correlate engagement metrics (e.g., likes, comments) with subscriber growth to highlight the impact of active audience interaction.

#### 4. Categorical Growth and Shifts in Content Strategy

- Objective: Identify which categories (e.g., Gaming, Education) led the way in professionalization and how strategies evolved within these categories.

- Methods:
   - Category-Wise Growth Trajectory: Perform categorical trend analysis to identify early-adopting categories and track their growth relative to others.
   - Video Length and Quality Indicators by Category: Analyze the average video length, resolution, and production quality over time for each category, identifying which content types transitioned into more professional formats first.
   - Cluster Analysis on Content Strategy: Cluster channels based on production characteristics (e.g., video length, upload frequency) to reveal content strategy shifts and identify archetypes of professional channels.

#### 5. Impact of YouTube Algorithm and Policy Changes

- Objective: Map YouTube's policy and algorithm updates to shifts in creator behavior and audience engagement, exploring how these changes accelerated professionalization.
We can find the history of YouTube's policy over the years on several web sites so we could then correlate the information found on the internet with our dataset.

- Methods:
   - Event Study Analysis: Identify key policy and algorithm updates (e.g., monetization changes, algorithm adjustments) and conduct pre- and post-analysis of engagement and growth metrics.
   - Statistical Comparison Across Event Intervals: For each identified change, compare key metrics (e.g., views, subscriber growth) across intervals before and after the event.

## Proposed timeline

- 15.11.2024 Data Cleaning and Preprocessing & Initial Exploratory Data Analysis.

- 04.12.2024 Implementation of the analysis that answer the research questions following the methods mentionned above.

- 10.12.2024 Compile the final analysis in a platform/format that the team will think about in the next days. (Create the Data Story)

- 14.12.2024 Write the project report.

- 20.12.2024 Submit the Data Story

## Organization within the team

- Each member can work on one research question.
- Each team member will be responsible for making the final visualization to complete the Data Story.

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

