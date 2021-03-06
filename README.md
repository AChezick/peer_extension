# Peer Extension
## Peer Extension : Twitter Data with PySpark
### Do "Possibly Sensitive" Labels Increase Tweet Reach?  

---
*Still under construction*
---

### Introduction
Recently, [it was shown]( https://github.com/lisapaige/Tweet-for-Reach ) among a collection of 214,936 French tweets from 2017 (during the Macron, Le Pen presidential election) that tweets that were marked as ‘possibly sensitive’ and ‘True’ were significantly more likely to have a larger retweet count as compared to tweets marked as possibly sensitive and ‘False.’ 

Assuming possibly sensitive tweets are more likely to have a higher retweet count to be the case among this particular data set, then understanding, or at least eliminating possible reasons for ‘What’ or ‘Why’ this is the case among these tweets, could be explored* 

*This is primary an exercise in working with nested .json files in PySpark. The results can only be considered relevant to this data set.
  
 ### Tech Stack
 A Docker image containing Apache Spark and PySpark were used. A pre-built* container can be obtained [from Dockerhub]( https://hub.docker.com/r/jupyter/pyspark-notebook ). 

*certain updates and packages would need to be installed to fully replicate this project
 
 
### EDA & NLP

After cleaning text and removing stop words from the following seach:

```SQL
words_true = spark.sql('''
SELECT lang , text,created_at, possibly_sensitive, quoted_status.favorite_count, entities.media.type
FROM temp_view
WHERE lang = 'en' and possibly_sensitive = "True";
''').collect()
```
word clouds were created to show the most popular words among retweets.

Top 15 Wordcloud for Possibly Sensitive tweets marked True

![]( https://github.com/AChezick/peer_extension/blob/main/images/en_cloud_top15.png ) 

Top 15 Wordcloud for Possibly Sensitive tweets marked False
```SQL
words_false = spark.sql('''
SELECT lang , text,created_at, possibly_sensitive, quoted_status.favorite_count, entities.media.type
FROM temp_view
WHERE lang = 'en' and possibly_sensitive = "False";
''').collect()
```

![]( https://github.com/AChezick/peer_extension/blob/main/images/enFAL_cloud_top15.png ) 

One interesting question is when are these sensitive tweets posted? Can we notice any trends ? 

![]( https://github.com/AChezick/peer_extension/blob/main/images/Hourly_Countsa.png )

For reference '0' is 12am and 15 is 3pm. By looking at this graph and comparing it to the tweets which are not sensitive and/or fasely marked sensitive there is overlap in the shapes. This overlap shows that when most tweets are happening there are more senesitive tweets then when less people are tweeting.

![]( https://github.com/AChezick/peer_extension/blob/main/images/hcountsF2.png )

### Hypothesis Testing

--- 

#### Does the addition of media impact retweet status? 



* Ho: Among all Possibly Sensitive tweets marked as True, those with media will Not have significantly different average retweet counts then those without media.
* Ha: Among all Possibly Sensitive tweets marked as True, those with media will have significantly different average retweet counts then those without media.

Insufficient Data to test: sizes are 0 , 512
Given there are no possibly sensitive tweets marked as True with media , there is insufficient evidence to reject the Ho. 


We can now search elsewhere to see if, at any level, there is evidence that would refute the null hypothesis. How about among the possibly sensitive tweets marked False... Are there any significant differences among retweet counts among those with and without media? 

---

* Ho: Among all Possibly Sensitive tweets marked as False, those with media will Not have significantly different average retweet counts then those without media.
* Ha: Among all Possibly Sensitive tweets marked as False, those with media will have significantly different average retweet counts then those without media.

|   | Hypothesis | Count | Average | Standev | Max    | Min | Sig Count |
|---|------------|-------|---------|---------|--------|-----|-----------|
| 0 | Ho         | 6     | 2445.83 | 3666.42 | 10127  | 0   | 1         |
| 1 | Ha         | 14576 | 1277.99 | 5909.58 | 339281 | 0   | 327       |

Ttest_indResult(statistic=0.71 , pvalue=0.51). We still fail to reject the Ho. Sample size among the two test groups is concerning. However, even with the unequal test sizes there was no enough evidence to suggest images have significant impact on retweet rates among Falsely marked possibly senesitive tweets. 

---

What about at the next largest scale? Among ALL quoted satus. 

* Ho: Among retweets those with media will Not have significantly different average retweet counts 
* Ha: Among retweets those with media will have significantly different average retweet count

|   | Hypothesis | Count | Average | Standev | Max    | Min | Sig Count |
|---|------------|-------|---------|---------|--------|-----|-----------|
| 0 | Ho         | 7     | 2096.43 | 3500.68 | 10127  | 0   | 1         |
| 1 | Ha         | 25962 | 863.63  | 4678.19 | 339281 | 0   | 482       |

Ttest_indResult(statistic=0.86 , pvalue=0.42 ). 
We continue fail to reject the Ho.

There Does not seem to be evidence to support the hypothesis that media influences retweet status. Among this data set there is not enough re-tweets with images and this data does not support exploring further into retweet status and images.

--- 

#### Does the trend of media not impacting tweet popularity continue when we switch our dependent variable to Like Count ?

* Ho: Among all Possibly Sensitive tweets marked as True, those with media will Not have significantly different average Like counts then those without media.
* Ha: Among all Possibly Sensitive tweets marked as True, those with media will have significantly different average Like counts then those without media.

Insufficient Data to test: sizes are 0 , 512
Given there are no possibly sensitive tweets marked as True with media , there is insufficient evidence to reject the Ho.

We can now scale our test upwords to see if, at any level, there is evidence that would support the alternative hypotheses and/or allow us to reject the Ho.

* Ho: Among all Possibly Sensitive tweets marked as False, those with media will Not have significantly different average Like Counts then those without media.
* Ha: Among all Possibly Sensitive tweets marked as False, those with media will have significantly different average retweet Counts then those without media.

|   | Hypothesis | Count | Average | Standev | Max    | Min | Sig Count |
|---|------------|-------|---------|---------|--------|-----|-----------|
| 0 | Ho         | 7     | 3124.14 | 6606.76 | 19246  | 0   | 1         |
| 1 | Ha         | 25297 | 959.83  | 7756.5  | 439147 | 0   | 241       |

Ttest_indResult(statistic=0.80 , pvalue=0.45 ). We still fail to reject the Ho.

---

What about at the next largest scale? Among all quoted satus. 

* Ho: Among retweets those with media will Not have significantly different average Like Counts 
* Ha: Among retweets those with media will have significantly different average Like Counts

|   | Hypothesis | Count | Average | Standev | Max    | Min | Sig Count |
|---|------------|-------|---------|---------|--------|-----|-----------|
| 0 | Ho         | 7     | 3124.14 | 6606.76 | 19246  | 0   | 1         |
| 1 | Ha         | 25962 | 949.23  | 7677.08 | 439147 | 0   | 246       |

Ttest_indResult(statistic=0.80 , pvalue=0.45 ). 
We still fail to reject the Ho.

---

Given the lack of evidence a bonferroni correction was not implemented to further validate results.  

A narrative about common sense would not be helpful. However, using certain premises we might be able to construct a reasonable narrative. Which is that among possible social media outlets Twitter is a text based medium that allows media. As compared to Ticktock, Instagram, Snap-chat which all focus on media that allows for text, the inverse of Twitter.
