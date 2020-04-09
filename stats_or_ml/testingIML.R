data("Boston", package  = "MASS")
head(Boston)


set.seed(42)
library("iml")
library("randomForest")



data("Boston", package  = "MASS")
rf = randomForest(medv ~ ., data = Boston, ntree = 50)


X = Boston[which(names(Boston) != "medv")]
predictor = Predictor$new(rf, data = X, y = Boston$medv)


library(corrplot)
M<-cor(Boston)
corrplot(M, method="number")
pairs(Boston)



ale = FeatureEffect$new(predictor, feature = "lstat")
ale$plot()


interact = Interaction$new(predictor)
plot(interact)
