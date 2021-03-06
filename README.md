# Reddit-Transaction-Analysis

Write up on project [Medium Article][1]

[1]:https://towardsdatascience.com/how-to-use-machine-learning-to-make-predictions-on-reddit-part-i-44cd210ec427

## Project Goals 

The goal of this project is to create a metric to determine the level of risk in transacting with a given Reddit user. There are not a lot of fraudulent activities on Reddit, but they do exist. This project is aimed at discovering the patterns that are associated with the activities of legitimate Redditors, in contrast to those of fraudulent users: scammers.

1. Gather reddit user account information on redditors who have transacted successfully 
2. Gather reddit user account information on redditors who have scammed 
3. Create a Model that will predict a reddit users risk factor using logistic regression 
4. Record pricing trends overtime (still in progress)

## Data 
1. Used Reddit's API to pull data (PRAW).  Pulled Data from submissions the subreddit r/hardwareswap 

Reddit User Attributes 
- Age 
- Karma
- Email (Verified or not)
- Gold (Paid Account)
- Moderator of Subreddit 
- Comments (amount)
- Comments for NLP (Was not used for current model, but will me implimented in the future)

## Redditor Vs Scammer EDA 

To begin, I will identify the two (2) groups who are being studied in the project. These are:

1. Reddit Users/Redditors: These are people who have done genuine transactions on Reddit. They have held up their end of the transaction deals.

2. Reddit Scammers: These are scammers on Reddit who have been involved in various fraudulent activities.

![](https://github.com/Landstein/Reddit-Transaction-Analysis/blob/master/images/age.png)
![](https://github.com/Landstein/Reddit-Transaction-Analysis/blob/master/images/Karma.png)
![](https://github.com/Landstein/Reddit-Transaction-Analysis/blob/master/images/email.png)
![](https://github.com/Landstein/Reddit-Transaction-Analysis/blob/master/images/gold.png)
![](https://github.com/Landstein/Reddit-Transaction-Analysis/blob/master/images/mod.png)
![](https://github.com/Landstein/Reddit-Transaction-Analysis/blob/master/images/comments.png)

Distribution of Data 

![](https://github.com/Landstein/Reddit-Transaction-Analysis/blob/master/images/distribution.png)





## Submission Title EDA (in progress)

![](https://github.com/Landstein/Reddit-Transaction-Analysis/blob/master/images/common_title_numbers.png)

![](https://github.com/Landstein/Reddit-Transaction-Analysis/blob/master/images/common_title_words.png)


## Product_selling_price() function output example (in progress)

![](https://github.com/Landstein/Reddit-Transaction-Analysis/blob/master/images/product_prices.png)