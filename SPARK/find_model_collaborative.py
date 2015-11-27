#!/usr/bin/env python
from __future__ import print_function

import sys
import itertools
from math import sqrt
from operator import add
from os.path import join, isfile, dirname
from pyspark import SparkContext, SparkConf, SQLContext
from pyspark.mllib.recommendation import ALS, MatrixFactorizationModel, Rating

conf = SparkConf().setAppName("app_collaborative")
sc = SparkContext(conf=conf)
sqlContext = SQLContext(sc)

jdbcDriver = 'com.mysql.jdbc.Driver'
jdbcUrl    = 'jdbc:mysql://173.194.227.120:3306/recoom?user=root'


def howFarAreWe(model, against, sizeAgainst):
	# Compare the model against validation data (the lower, the better)
	# We predict the rating and compare with the actual one
	# Switch 1 and 0 because needs a (user, product) pair
	againstNoRatings = against.map(lambda x: (int(x[0]), int(x[1])) ) #Only keep the accomodation and user columns
	againstWiRatings = against.map(lambda x: ((int(x[0]),int(x[1])), int(x[2])) ) #(accommodation, user), rating columns

	# Do the prediction and map to (accommodation, user), rating columns
	# Here p[2] is our predicted rating
	# Need a (user,product) not (product,user)
	predictions = model.predictAll(againstNoRatings).map(lambda p: ( (p[0],p[1]), p[2]) )
	#print("predictions")
	#print(predictions.take(10))

	#print("validatingWiRatings")
	#print(validatingWiRatings.take(10))

	# It gives us the pais (prediction, rating) out of ( (user, acco), (prediction, rating))
	predictionsAndRatings = predictions.join(againstWiRatings).values()
	#print("predictionsAndRatings")
	#print(predictionsAndRatings.take(10))

	# Mean
	#rmse1 = predictionsAndRatings.map(lambda r: (r[0] - r[1]) ** 2).mean()
	#print("Rmse " + str(rmse1))

	# Variance
	return sqrt(predictionsAndRatings.map(lambda s: (s[0] - s[1]) ** 2).reduce(add) / float(sizeAgainst))
	#print ("Rmse " + str(rmse2))


# Read the data from the Cloud SQL
# Create dataframes
dfRates = sqlContext.load(source='jdbc', driver=jdbcDriver, url=jdbcUrl, dbtable='RatingT')

#nbRates = dfRates.count()
# Our user is 843025, they have 8 ratings
rddUserRatings = dfRates.filter(dfRates.userId == 0).rdd
print(rddUserRatings.count())

# Split the data in 3 non-overlapping sets : training, validating, testing
# It is the best way to get a subset of an RDD
# This is 1/3, we should do a a 80/20 training/testing then 80/20 of training in training/validation
# We switch the columns product, user as the predict needs a (user, product)
rddRates = dfRates.rdd
rddTraining, rddValidating, rddTesting = rddRates.randomSplit([6,2,2])

#Add user ratings in the training model
rddTraining.union(rddUserRatings)
"""
rddTraining   = dfRates.filter(dfRates.accoId % 10 <= 6).rdd
rddValidating = dfRates.filter(dfRates.accoId % 10 == 7 or dfRates.accoId % 10 == 8).rdd
rddTesting    = dfRates.filter(dfRates.accoId % 10 > 8).rdd
"""
"""
rddRates = dfRates.rdd
rddTraining   = rddRates.filter(lambda x : int(x[1]) % 3 == 0).values().repartition(4).cache()
rddValidating = rddRates.filter(lambda x : int(x[1]) % 3 == 1).values().repartition(4).cache()
rddTesting    = rddRates.filter(lambda x : int(x[1]) % 3 == 2).values().cache()
"""
nbValidating = rddValidating.count()
nbTesting    = rddTesting.count()

print("Training: %d, validation: %d, test: %d" % (rddTraining.count(), nbValidating, rddTesting.count()))

# Training
# Build the recommendation model using Alternating Least Squares
#http://spark.apache.org/docs/latest/mllib-collaborative-filtering.html
# This is one model but we need more combination

# Best results are not commented
ranks  = [5,10,15,20]
reguls = [0.1, 1,10]
iters  = [5,10,20]

finalModel = None
finalRank  = 0
finalRegul = float(0)
finalIter  = -1
finalDist   = float(100)

for cRank, cRegul, cIter in itertools.product(ranks, reguls, iters):

	model = ALS.train(rddTraining, cRank, cIter, float(cRegul))
	dist = howFarAreWe(model, rddValidating, nbValidating)
	print(str(dist))
	if dist < finalDist:
		finalModel = model
		finalRank  = cRank
		finalRegul = cRegul
		finalIter  = cIter
		finalDist  = dist

print("Rank " + str(finalRank))  # best is 20
print("Regul " + str(finalRegul)) # best is 1
print("Iter " + str(finalIter))  # best is 20
print("Dist " + str(finalDist))  # best is 2.45935601578 (It is bad!!!)



















