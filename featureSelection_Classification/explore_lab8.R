setwd('/Users/Anna/Documents/HS614/shiyaqi-lab-8')
datalab <- read.table('data.csv', sep = ',')
datalab[, 5] <- as.numeric(rownames(data))
names(datalab) <- c('ctm2','age','los','outcome','ctm1')
cor(datalab)

fit <- glm(outcome~., data = datalab)
summary(fit)

fit1 <- glm(outcome~.-age, data = datalab)
summary(fit1)
