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

The YouNiverse database is extensive but lacks economic data, a key factor in understanding professionalization. Revenue sources like AdSense are relevant but limited by data availability, as Alphabet has only published separate figures since 2019. Additional revenue streams, such as e-books, online courses, crowdfunding, and brand partnerships, lack comprehensive data across regions and stakeholders. Peripheral economies, like gaming and e-sports, offer potential insights but face similar access and cost barriers. For instance, e-sports data and Twitch metrics are costly and restricted, while video game developer revenues may introduce biases.

Key considerations include:
- Primary YouTube revenue sources: AdSense, sponsorships, merchandise, crowdfunding, online courses, and fan support platforms.
- Viewer demographics: ~25% of YouTube viewers are from India, ~10% from the U.S.
- Dominant content: Indian entertainment, children’s content, and music lead YouTube charts.

## Methods

## Research Question 4 : How can we help content creators to evolve their community management evolved from casual interaction to professional engagement strategies ? 

Datasets used in this research question : 
1) youtube_comments.tsv.gz : contains around 8.6 B comments. Each rows corresponds to a comment. It contains an anonymized user id, a video id, the number of replies the comment received, and the number of likes the comment received.
  
2) yt_metadata_en.jsonl.gz : contains metadata data related to ~73M videos. Each rows correponds to a video. It contains the category of the video, the id of the channel related to the video, the crawl date, the description written by the creator under the video, the number of dislikes, the id of the video, the duration, the number of likes, the tags, the title, the upload date and the view count

Data processing : 
1) script process_comments.py : uses the "youtube_comments.tsv.gz" file. We only consider authors who wrote more than 100 comments in total and we keep a list containing the id's of the the videos under which each author commented. We split the "process_comments.py" file in chunks of 100.000.000 lines each and we store each of these chunks in a file named "filtered_comments.csv".

2) process_metadata.py : we read the "yt_metadata_en.jsonl.gz" file. For each row, we only keep the id of the video and the category it belongs to. We store the final data in the "yt_metadata.csv" file.

3) Using the "matrix_contruction.py" file, we open the "filtered_comments_i.csv" and "yt_metadata.csv" files and we create based on them a matrix. Each row of the matrix represents an author and each column a category. Noting the matrix $A$, then $A_{ij}$ would be the number of comments the author i wrote unders videos belonging to the category j. The matrix is then stored in the "my_matrix.npy" file.

Methods : 
1) Before computing whatever with the matrix $A$ described before, we firstly divide each row by it's $l_1$ norm. For each row i :
![Équation LaTeX](https://latex.codecogs.com/svg.image?&space;A_i\leftarrowA_i\||A_i||_{l_1}}). The idea behing this step is to have for each row of the matrix (and thus for each author of comments) a distribution of the themes the author commented. 

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
