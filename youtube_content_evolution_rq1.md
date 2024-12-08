# Youtube Content Evolution Over Time Analysis

This file explains the methodology and the algorithms used to answer our first research question: "How has the frequency and consistency of content creation evolved over time across different channel categories?"

This research question is kind of an introduction to our topic about the professionalization of YouTube. If frequency and consistency of content creation evolved over time, it could indicate that the way of thinking to some creators about how YouTube can be used has changed other time and could indicate an evolution of YouTube as a platform, allowing creators to make a living with the creation of videos.

-> need to take the ```yt_metadata_en.jsonl.gz``` file to have access to the "description" field, so we can check if there is an intent from the creators to earn money via some monetization method (if we find some url, or will to earn donation for example). But this might be useful to filter only channels and video that want to generate money and are therefore "professionalized" in some way.


## Step 1: Defining Metrics

Need to define what we mean by frequency and consistency and how that could be relevant to the professionalization of some YouTube channels.

### Frequency Analysis

We can measure the numbers of video uploaded per year or month for each channel or category to see if there are diferent behaviors already of frequency in our dataset.

### Consistency Analysis

We can measure the variance or standard deviation in upload intervals for each channel or category. For example, we can calculate the time difference between consecutive uploads and measure its variability.

### Identify Patterns in categories

Are some categories more consistent than others over time?

Do categories that involve professional content (e.g., "Education", "Gaming", "How-to & Style") show increasing consistency compared to casual ones (e.g., "Comedy", "Entertainment")?


## Step 2: Timeseries Analysis

See if data about timeseries data can be correlated with the frequency and consistency shown above.


## Step 3: Some ML algorithms

Want to use some ML algorithms to do some classification on channels based on the behavior of their creators, and a second algorithm to analyze the shift from casual to professional content (might need the bigger metadata for this one)

### Classify Channels Based on Content Creation Behavior

### Cluster Channels or Videos by Behavior

### Analyze the Shift from Casual to Professional Content

Train a model to detect trends in the transition from casual to professional content creation over time. Use historical data to train a supervised or unsupervised learning model to identify key features (e.g., increase in upload frequency, consistency, and views). Detect categories or time periods when this shift happened.

Example Use Case:
Train a model to predict the likelihood of a channel becoming professionalized based on early upload patterns.