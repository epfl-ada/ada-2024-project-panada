# From Hobby to Profession: The Evolution of YouTube as a Career Platform

![Alt text](./youniverse.png "YouNiverse")


### How to start the project
```bash
# clone project
git clone <project link>
cd <project repo>

# install requirements
pip install -r pip_requirements.txt
```



### How to use the library
The heart of our code is in ```results.ipynb```. You will find our data visualisation methods to study our dataset and extract interesting features and data.
in ```src/data``` you will find the files for the different data cleaning methods we have implemented for each different file as liabilities are different from one file to another.

### How to load the dataset
Because the size of the dataset is too important, it is not included in the ```/data``` folder, in order to load the dataset,  download it from this link : https://zenodo.org/records/4650046 and load it into the folder, the file names are in the ```.gitignore```.

## Project Structure

The directory structure of new project looks like this:

```
├── data                        <- Project data files
│
├── src                         <- Source code
│   ├── data                            <- Data directory
│   ├── models                          <- Model directory
│   ├── utils                           <- Utility directory
│   ├── scripts                         <- Shell scripts
│
├── tests                       <- Tests of any kind
│
├── results.ipynb               <- a well-structured notebook showing the results
│
├── .gitignore                  <- List of files ignored by git
├── pip_requirements.txt        <- File for installing python dependencies
└── README.md
```



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

## Website

You can find the data story of our project on our [website](https://webpanada.vercel.app/).

## Research Questions

- How has the frequency and consistency of content creation evolved over time across different channel categories? 

- How has creator content strategy evolved to reflect professional monetization approaches?

- Which categories led YouTube's professionalization, and how did professional practices spread?

- How can we help content creators to evolve their community management evolved from casual interaction to professional engagement strategies?

In the Milestone 2, we had 5 research questions but we decided to remove one of them since it was highly correlated to another research question we already had.

## Proposed additional datasets

The YouNiverse database, while extensive, lacks crucial economic data that's essential for understanding creator professionalization. To address this gap, we augmented the dataset with monetization indicators obtained through the YouTube API. This additional dataset includes three key monetization columns:
- has_affiliate: Indicates affiliation with third-party companies
- has_sponsorships: Shows content sponsored by companies/brands in exchange for product promotion
- has_merchandise: Reflects use of merchant platforms for selling branded goods to fans

While YouTube's API typically provides detailed monetization data through various indicators (e.g., 'affiliate link', 'ref=', 'partner link', 'sponsored by', 'merch', etc.), we consolidated these into three main categories to work within the API's daily request limitations.
To complement this API data, we conducted additional analysis of revenue streams by extracting monetization indicators from video descriptions in the yt_metadata_en.jsonl.gz dataset. Our keyword detection system identified five distinct monetization categories:
- Membership : "subscription," "member," "join button," "channel member," "membership," "premium content"
- Crowdfunding : "patreon," "ko-fi," "donation," "support us," "buy me a coffee," "gofundme," "paypal," "tip jar," "patron"
- Merchandise : "merchandise," "merch," "shop," "store," "tshirt," "t-shirt," "hoodie," "apparel," "limited edition"
- Sponsorship : "sponsor," "sponsored," "partnership," "partner," "paid promotion," "#ad," "#sponsored," "promotion"
- Affiliate Marketing : "affiliate," "amazon link," "discount code," "promo code," "referral," "use code," "commission"

## Methods

### Research Question 1: How has the frequency and consistency of content creation evolved over time across different channel categories?

Datasets used in this research question:

- yt_metada_helper.feather: contains metadata data related to ~73M videos between 2005 and 2019 from ~137k channels. Each row corresponds to a video. It contains its category, its channel, its uploaded date, its number of likes, views and dislikes and its title.

- df_channels_en.tsv.gz: contains data related to channels. It aggregates both basic stats from channels obtained from ```channelcrawler.com```, as well as rankings obtained from ```socialblade.com```. Each row corresponds to a channel where we can find its category, the date when he joined YouTube, its name, its number of subscribers and videos.


Data processing:

- We removed the rows containing NaN values for the two files and we then merged the two datasets using channel IDs as the key. We grouped the data by channel IDs to enable efficient analysis of video and channel metadata together.

Methods:

1. **Trend Analysis**:
   - **Upload Frequency Over Time**:
     - Aggregated video upload counts per year and per category to identify growth trends.
     - Generated line plots to observe how upload frequencies evolved for each category between 2006 and 2018.

2. **Consistency Analysis**:
   - **Active Months Definition**:
     - Defined an active month as a month with at least 2 video uploads.
   - **Channel-Level Consistency**:
     - Calculated the proportion of active months for each channel relative to the total months in the dataset.
     - Aggregated these proportions to calculate the average consistency for each category.
   - **Category-Level Consistency**:
     - Generated time-series line plots to track the evolution of consistency across categories.

3. **Long-Tail Distribution Analysis**:
   - **Cumulative Distribution**:
     - Analyzed the contribution of channels to total uploads and views within each category.
     - Plotted cumulative distributions to reveal that a small proportion of channels generate the majority of views.

4. **Correlation Analysis**:
   - Computed correlation matrices between:
     - Engagement metrics (views, likes, dislikes, and subscribers).
     - Consistency metrics (proportion of active months and total active months).
   - Visualized correlations using heatmaps to identify relationships between consistency and engagement.

5. **Visualization**:
   - Generated multiple plots to support the analysis:
     - Line plots for trends in upload frequency and consistency.
     - Box plots for consistency distribution.
     - Bar plots for upload frequency by category and year.
     - Heatmaps for correlation matrices.

### Research Question 2: Which content categories drive YouTube's professionalization, and how have their practices evolved?

NB: This part was initially computed using Plotly, but the overly heavy plots generated made the results.ipynb submission complex. In the notebook, the plots are displayed using Matplotlib or Seaborn, but the interactive displays have been preserved in the website.

Datasets used in this research question:
1) yt_metadata_en.jsonl.gz: A large dataset of ~14 GB containing information from the YouNiverse videos dataset, including category, channel ID, crawl date, description, dislike count, display ID, duration, like count, tags, title, upload date, and view count. This dataset was used to analyze video descriptions while considering their upload date and category.  

2) df_channels_en.tsv.gz: This dataset contains information on 136,470 English-speaking video channels. It includes the category, join date, channel ID, and characteristics such as the subscriber rank.  

3) youtube_monetization_api.csv: An additional dataset obtained from the YouTube API, indicating whether videos use merchandise, affiliation, or sponsorship. These details are linked through the channel ID.  

Data processing:

1) generate_df_channel_monetization.py:  
   - Removes NaN values or unexpected duplicate lines if present.  
   - Extracts only the columns of interest: the category and channel ID.  

2) generate_clean_professionalization_in_description.py:  
   - Processes the large JSON file in chunks to extract relevant elements from video descriptions.  
   - Extracts the video upload dates and categories.  
   - Skips rows with NaN values in any of the relevant columns.  

3) generate_clean_df_cross_analysis.py:  
   - Similar to the previous script, but instead extracts the video ID rather than the upload date.  
   - Merges the extracted data with information from the API dataset using the channel ID as a key.  
   - Groups all columns (e.g., words of interest in descriptions, monetization usage from the API) by categories.  
   - Provides a count of values of interest for each category in an additional file containing the size of each group before aggregating everything to generate accurate plots later.  

/!\ Caution /!\
Chunks are set to 20,000 in scripts (2) and (3), but should be adjusted based on RAM availability:  
- **For 8 GB RAM**: Set `chunk_size` to around 10,000–20,000 rows.  
- **For 16 GB RAM**: Set `chunk_size` to around 20,000–40,000 rows.  
- **For 32 GB RAM**: Set `chunk_size` to around 40,000–80,000 rows.  


Methods:
1) Category Distribution Analysis:
   - Used pandas for data aggregation and counting category frequencies
   - Implemented color mapping function (`create_color_mapping`) to maintain consistent category colors across visualizations
   - Calculated percentages of each category's representation in the dataset

2) Temporal Evolution Analysis:
   - Created time series analysis of professionalization markers in video descriptions (http, ad, shop, support)
   - Applied rolling means (30-day window) to smooth daily fluctuations
   - Calculated daily percentages of videos containing each term
   - Separated analysis by category to track evolution patterns

3) Cross-Analysis and Correlation:
   - Implemented weighted linear regression to account for category size differences
   - Used log-log representation for handling large data variances
   - Calculated correlation coefficients between different monetization methods
   - Applied statistical significance testing (p-values) to validate relationships

Visualizations:
1) Category Distribution:
   - Bar plot showing category proportions with percentage labels
   - Pie charts displaying monetization method shares by category
   - Stacked histograms showing frequency distributions of monetization methods
   - Used consistent color scheme across all visualizations for easy category identification

2) Temporal Evolution:
   - Line plots showing trends over time with confidence intervals
   - Grid layout (2x2) comparing different professionalization markers
   - Dual visualization approach:
      - Overall trends (with rolling averages)
      - Category-specific evolution patterns
       
3) Correlation Analysis:
   - Bubble plots showing relationships between variables
   - Size of bubbles representing category weight
   - Heat maps displaying correlation coefficients between:
      - Different monetization methods
      - Different professionalization markers in descriptions
      - Log-scale scatter plots with regression lines

Appendices:
A.1 Correlation Heatmaps:
- Heatmap 1: Correlation between monetization methods (merchandise, affiliate, and sponsorship)
- Heatmap 2: Correlation between word usage in descriptions (URLs, Ad, Shop, Support)

A.2 Distribution Plots:
- Four-panel grid showing the distribution of term occurrences by year (2005-2019)
- Terms analyzed: 'http', 'ad', 'shop', 'support'
- Log-scale representation with average trend line in red


### Research Question 4: How can we help content creators to evolve their community management evolved from casual interaction to professional engagement strategies ? 

Datasets used in this research question : 
1) youtube_comments.tsv.gz : contains around 8.6 B comments. Each rows corresponds to a comment. It contains an anonymized user id, a video id, the number of replies the comment received, and the number of likes the comment received.
  
2) yt_metadata_en.jsonl.gz : contains metadata data related to ~73M videos. Each rows correponds to a video. It contains the category of the video, the id of the channel related to the video, the crawl date, the description written by the creator under the video, the number of dislikes, the id of the video, the duration, the number of likes, the tags, the title, the upload date and the view count

Data processing : 
1) script process_comments.py : uses the "youtube_comments.tsv.gz" file. We only consider authors who wrote more than 100 comments in total and we keep a list containing the id's of the the videos under which each author commented. We split the "process_comments.py" file in chunks of 100.000.000 lines each and we store each of these chunks in a file named "filtered_comments.csv".

2) process_metadata.py : we read the "yt_metadata_en.jsonl.gz" file. For each row, we only keep the id of the video and the category it belongs to. We store the final data in the "yt_metadata.csv" file.

3) Using the "matrix_contruction.py" file, we open the "filtered_comments_i.csv" and "yt_metadata.csv" files and we create based on them a matrix. Each row of the matrix represents an author and each column a category. Noting the matrix $A$, then $A_{ij}$ would be the number of comments the author i wrote unders videos belonging to the category j. The matrix is then stored in the "my_matrix.npy" file.

Methods : 
1) Before computing whatever with the matrix $A$ described before, we firstly divide each row by it's $l_1$ norm. For each row i :
![Équation LaTeX](https://latex.codecogs.com/svg.image?&space;A_i\leftarrow&space;A_i/||A_i||_{l_1}). The idea behing this step is to have for each row of the matrix (and thus for each author of comments) a distribution of the themes the author commented.

2) At this step, we know have a matrix A such that ![Équation LaTeX](https://latex.codecogs.com/svg.image?A_{ij}=) distribution of comments written by the author i under videos belonging to the category j. The goal is now to establish a notion of distance between the categories based on this matrix. Let's note ![Équation LaTeX](https://latex.codecogs.com/svg.image?A_{:i}) the i'th column of the matrix A, we describe the distance between the category i and the category j as : ![ÉquationLaTeX](https://latex.codecogs.com/svg.image?dist(cat_i,cat_j)=1-\frac{A_{:i}\cdot&space;A_{j:}}{||A_{:i}||||A_{:j}||}). We can also talk about a similarity metric between two categories wich is simply 1 - distance. 

3) Now that we have distances between categories, we can establish clusters of categories. We use a simple hierarchy clustering based on the ward metric to create the clusters.

Visualization : 
1) To visualize distances between the categories, we use a heatmap animation done with plotly.
2) We also visualize the similarity metric using a network animation. The nodes are the categories and the links between two categories are proporitionnaly wider with the similarity between these.
3) Finally, we use a dendogramm to visualize the clusters. We can easily see low-level, mid-level or high level clusters. 




## Data Cleaning Pipeline

Our data cleaning process aims to ensure a good quality input for our analysis by handling missing values effectively. After a preliminary analysis of our data, we noticed that there were a very small proportion of missing values for every file of our dataset. Therefore, we decided to remove the samples that have missing values in our dataset, as it won't remove a significant proportion of the dataset.

## Proposed timeline

- 15.11.2024 Data Cleaning and Preprocessing & Initial Exploratory Data Analysis.

- 04.12.2024 Implementation of the analysis that answer the research questions following the methods mentionned above.

- 10.12.2024 Compile the final analysis in a platform/format that the team will think about in the next days. (Create the Data Story)

- 14.12.2024 Write the project report.

- 20.12.2024 Submit the Data Story


## Tasks and Responsibilities

- Imane: Created and developed the website, wrote the datastory on the website.

- Koami: Preliminary data analysis during M2, analyzation and plotting graphs for the second research question, found additional datasets for monetization data, merging final results in the result notebook.

- Antoine: Problem formulation, analyzation and plotting graphs for the first research question, merging final results in the result notebook, wrote the README.

- Adam: Analyzation and plotting graphs of the the fourth research question about how we can help the content creator to enhance its community management. Merging final results in the result notebook.

- Valentine: Analyzation and plotting graphs of the third research question, merging final results in the result notebook.
