# DataFrame creation
df_tweet = spark.read.json("s3a://nrandriamanana/diffusion/formation/data/tweets/tweets20220414-090219.jsonl.gz")
df_tweet_big = spark.read.json("s3a://nrandriamanana/diffusion/formation/data/tweets/")

# caching
df_tweet.cache()
df_tweet_big.cache()

df_tweet.show(5)
df_tweet.printSchema()
df_tweet_big.show(5)
df_tweet_big.printSchema()

print(f'the small DF has {df_tweet.count()} rows')
print(f'the big DF has {df_tweet_big.count()} rows')

df_tweet_sampled = df_tweet_big.sample(fraction=0.1)

tweet_author_hashtags = df_tweet_big.select("auteur", "hashtags")
tweet_author_hashtags.show(5)

df_tweet_big.select("auteur", "entities.urls", "entities.mentions").show(5)

df_tweet_big.filter(df_tweet_big.like_count > 0).show(5)

df_tweet_big_interation = df_tweet_big.withColumn("interaction_count", df_tweet_big.like_count+df_tweet_big.reply_count+df_tweet_big.retweet_count )
df_tweet_big_interation.show(5)

df_tweet_big = df_tweet_big.drop("other")

df_tweet_big.filter(size("hashtags") > 0).withColumn("hashtag", explode("hashtags")).show(5)

df_tweet_big.withColumn("word_count", size(split("contenu", " "))).show(5)

df_tweet_big.filter(array_contains("hashtags", "COVID19")).count()

# pure python functions
def word_count(string):
    return len(string.split(" "))

# user definid function
word_count_udf = udf(
    lambda x: word_count(x), IntegerType()
) #we use a lambda function to create the udf.

# df manipulation
df_tweet_big\
  .withColumn("word_count", word_count_udf("contenu")).show(10)

df_tweet_big_interation.select(min("interaction_count"),max("interaction_count"),avg("interaction_count")).first()

df_tweet_big.select(count("hashtags"), countDistinct("hashtags"), approx_count_distinct("hashtags", 0.1), approx_count_distinct("hashtags",0.01)).show()

from pyspark.sql.functions import desc
df_tweet_big.groupBy("auteur").agg(min("retweet_count").alias("min_RT"), max("retweet_count").alias("max_RT"), avg("retweet_count").alias("avg_RT")).orderBy(desc("max_RT")).show(5)

df_tweet_big.select("contenu", "hashtags").createOrReplaceTempView("view_hashtag_content")

spark.sql("""
SELECT COUNT(*), COUNT(DISTINCT(contenu))
FROM view_hashtag_content
WHERE size(hashtags) > 0
""").show(5)

df_tweet_big.createOrReplaceTempView("view_tweet_big")
spark.sql("""
SELECT min(retweet_count), max(retweet_count), avg(retweet_count)
FROM view_tweet_big
GROUP BY auteur
ORDER BY MAX(retweet_count) DESC
""").show(5)

schema = StructType([ \
    StructField("created_at",TimestampType(),True), \
    StructField("id",StringType(),True), \
    StructField("name",StringType(),True), \
    StructField("username", StringType(), True), \
    StructField("withheld",StructType([ 
        StructField("country_codes", ArrayType(StringType(),True)),\
        StructField("scope", StringType(), True)  \
    ])),
    StructField("verified",BooleanType(),True)             
  ])

df_user_big = spark.read.json("s3a://nrandriamanana/diffusion/formation/data/user")
df_user_big.cache()
df_user_big.show(5)

df_user_big.printSchema()

df_user_big.filter("created_at" > to_date(lit("2019-01-01"))).count()

df_user_big.filter("verified").count()

joinExpression=df_user_big["username"]==df_tweet_big['data.author_id']
df_user_big.join(df_tweet_big, joinExpression).show()

df_user_big.join(df_tweet_big, joinExpression).filter("verified").count()