# DataFrame creation
df_tweet = spark.read.json("s3a://nrandriamanana/diffusion/formation/data/tweets/tweets20220414-090219.jsonl.gz")
df_tweet_big = spark.read.json("s3a://nrandriamanana/diffusion/formation/data/tweets/")

# caching
df_tweet.cache()
df_tweet_big.cache()