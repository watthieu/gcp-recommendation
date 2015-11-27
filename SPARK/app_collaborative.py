#!/usr/bin/env python
from __future__ import print_function

import sys
import itertools
from math import sqrt
from operator import add
from os.path import join, isfile, dirname
from pyspark import SparkContext, SparkConf, SQLContext
from pyspark.mllib.recommendation import ALS, MatrixFactorizationModel, Rating
from pyspark.sql.types import StructType
from pyspark.sql.types import StructField
from pyspark.sql.types import StringType

conf = SparkConf().setAppName("app_collaborative")
sc = SparkContext(conf=conf)
sqlContext = SQLContext(sc)

jdbcDriver = 'com.mysql.jdbc.Driver'
jdbcUrl    = 'jdbc:mysql://173.194.227.120:3306/recoom?user=root'

USER_ID = 843025

# Read the data from the Cloud SQL
# Create dataframes
dfAccos = sqlContext.load(source='jdbc', driver=jdbcDriver, url=jdbcUrl, dbtable='Accommodation')
dfRates = sqlContext.load(source='jdbc', driver=jdbcDriver, url=jdbcUrl, dbtable='Rating')

# Get all the ratings rows of our user
dfUserRatings  = dfRates.filter(dfRates.userId == USER_ID).map(lambda r: r.accoId).collect()
print(dfUserRatings)

# Returns only the accos that have not been rated by our user
rddPotential  = dfAccos.rdd.filter(lambda x: x[0] not in dfUserRatings)
pairsPotential = rddPotential.map(lambda x: (USER_ID, x[0]))


rddTraining, rddValidating, rddTesting = dfRates.rdd.randomSplit([6,2,2])
model = ALS.train(rddTraining, 20, 20, 1.0)

"""
predictions = model.predictAll(pairsPotential).collect()
recommendations = sorted(predictions, key=lambda x: x[2], reverse=True)[:10]
print(recommendations)
"""
# Calculate all predictions
# And take the top 5 ones
predictions = model.predictAll(pairsPotential).map(lambda p: (str(p[0]), str(p[1]), str(p[2])))
topPredictions = predictions.takeOrdered(5, key=lambda x: -float(x[2]))

schema = StructType([StructField(field_name, StringType(), True) for field_name in ["userId", "accoId", "prediction"]])

dfToSave = sqlContext.createDataFrame(topPredictions, schema)
dfToSave.write.jdbc(url=jdbcUrl, table='Recommendation', mode='overwrite')



"""
[Rating(user=843025, product=25985, rating=1.9971656196454914), 
Rating(user=843025, product=24243, rating=1.996891742823552), 
Rating(user=843025, product=26791, rating=1.9498923164590205), 
Rating(user=843025, product=13993, rating=1.7266927104897358), 
Rating(user=843025, product=6678, rating=1.7231034541238452), 
Rating(user=843025, product=5272, rating=1.6979594090065298), 
Rating(user=843025, product=17631, rating=1.695564977956851), 
Rating(user=843025, product=1614, rating=1.6885253039462234), 
Rating(user=843025, product=20152, rating=1.6700901145990368), 
Rating(user=843025, product=2782, rating=1.6650575947549144)]
"""