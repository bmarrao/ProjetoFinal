library(randomForestSRC) 
library(survival) 
library(pec) 

#Replace all the 1's with 0's (censored)
lcOrig$status <- gsub(pattern = "1", replacement = "0", x = lcOrig$status, fixed = TRUE)
#Replace all the 2's with 1's (death)
lcOrig$status <- gsub (pattern = "2", replacement = "1", x = lcOrig$status, fixed = TRUE)
#Do the same thing for sex (0 = Males, 1 = Females)
lcOrig$sex <- gsub(pattern = "1", replacement = "0", x = lcOrig$sex, fixed = TRUE)
lcOrig$sex <- gsub(pattern = "2", replacement = "1", x = lcOrig$sex, fixed = TRUE)
#Change the class of these variables to factor.
lcOrig$status <- as.integer(lcOrig$status) 
lcOrig$sex <- as.integer(lcOrig$sex) 
lcOrig$ph.ecog <- as.integer(lcOrig$ph.ecog)
#Remove missing values and column with over 20% missing data.
#lcOrig <- lcOrig[, c(1:9, 11)]
lc <- lcOrig[complete.cases(lcOrig), ]

#Kaplan-Meier Survival Curves for Patient Survival based on Gender.
lc$survObj <- with(lc, Surv(time, event = status))
km.by.sex <- survfit(survObj ~ sex, data = lc, conf.type = "log-log") 
plot(km.by.sex, lty = 1:2, col = c("Black", "Red"), xlab = "Days", ylab ="Proportion of Survivors", main =                                                                            "Kaplan Meier Curves by Gender", mark.time = TRUE)
legend(x = 500, y = 1, legend = c("Male", "Female"), lty = 1:2, col =
         c("Black", "Red"), title = "Gender", cex = .95, bty = "n")


km.lc <- survfit(survObj ~ 1, data = lc, conf.type = "log-log") 
plot(km.lc, conf.int = F, col = "black",
     main = "Kaplan-Meier Survival Curve", xlab = "Time (Days)",
     ylab = "Proportion of Survivors")


#############
fitform1 <- Surv(time, status) ~ inst + age + sex + ph.ecog + ph.karno + pat.karno + wt.loss
cox1 <- coxph(fitform1, data = lc)
summary(cox1)
###################
#The output is from a Cox proportional hazards model with 7 predictors (inst, age, sex, ph.ecog, ph.karno, pat.karno, wt.loss) fitted to a data set (lc) with 167 subjects and 120 events. The "coef" column shows the estimated coefficients for each predictor, and the "exp(coef)" column shows the corresponding hazard ratios. The "se(coef)" column gives the standard error of the coefficient estimates. The "z" and "Pr(>|z|)" columns show the test statistic and p-value for testing the null hypothesis of no effect for each predictor. The "Signif. codes" column indicates the level of significance (based on the p-value) for each predictor. The "exp(coef) exp(-coef)" column shows the lower and upper bounds of the 95% confidence interval for the hazard ratios. The concordance index is 0.648 with a standard error of 0.03, which is a measure of the overall goodness of fit of the model. The likelihood ratio test, Wald test, and score (logrank) test all indicate that the model is significant overall, with p-values of 2e-05, 5e-05, and 3e-05, respectively.
#################
plot(km.lc, conf.int = F, col = "black", main = "Comparison of Model Fits", xlab = "Time (Days)", ylab = "Proportion of Survivors")
lines(survfit(cox1, conf.int = F), col = "#238b45")
legend(x = 500, y = 1, legend = c("Kaplan-Meier", "Cox-PH"), lty = 1, 
       col = c("black", "#238b45"),
       cex = 1, bty = "n")

names(survfit(cox1))
survfit(cox1)$surv

#####
#The plot function will create a survival curve based on the Cox proportional hazards model cox1 that you fitted using the coxph function, with the fitform1 formula and the lc data. The argument conf.int = F will turn off the confidence intervals for the survival curve.
###RANDOM SURVIVAL FORESTS###
#############################
set.seed(0692)
rsf1 <- rfsrc(fitform1, data = lc, forest = TRUE, ntree = 1000,
              splitrule = "logrank", importance = TRUE) 


pred_survival_times <- predict(rsf1, newdata = lc, type = "survival")

df <- data.frame(time = lc$time, status = lc$status)

# add the predicted survival times to the data.frame
df$pred_survival_times <- pred_survival_times

# create a survival curve from the predicted survival times
surv_curve <- Surv(df$time, df$status)

# plot the survival curve
plot(surv_curve, xlab = "Time", ylab = "Survival Probability",
     main = "Survival Curve", conf.int = FALSE)
lines(survfit(cox1, conf.int = F), col = "#238b45")


#
# fit the survival model
fit <- survfit(Surv(time, status) ~ pred_survival_times, data = df)

# get the estimated survival probabilities at each time point
surv_probs <- predict(fit, type = "surv")
plot.survival.rfsrc(rsf1, plots.one.page = FALSE, cens.model = "rfsrc")
                                                                           
survfit(rsf1)
plot(rsf1)
plot.survival(rsf1)

names(rsf1)




#############
fitform1 <- Surv(time, status) ~ inst + age + sex + ph.ecog + ph.karno + pat.karno + wt.loss

# Fit a random survival forest model
fit_rsf <- rfsrc(Surv(time, status) ~ inst + age + sex + ph.ecog + ph.karno + pat.karno + wt.loss, data = lc)

pred.surv <- predict(fit_rsf, type="survival")
class(pred.surv$survival)
dim(pred.surv$survival)
# Create a survival curve
plot(pred.surv$time, pred.surv$survival[1,], type="l", 
     xlab="Time", ylab="Survival Probability",
     col="blue", lwd=2) 

matplot(pred.surv$time, t(pred.surv$survival), type="l", 
        xlab="Time", ylab="Survival Probability",
        col="blue", lwd=2, ylim=c(0, 1))
