# Experiments
Dataset is split into
- Training set from 2022-03-03 to 2024-06-31 (28 months) (70%)
- Validation set from 2024-07-01 to 2024-12-31 (6 months) (15%)
- Test set from 2025-01-01 to 2025-06-30 (6 months) (15%)

Every experiment consists of 3 input components:
1. A set of feature groups to evaluate
2. A set of window sizes of 16, 32, and 48 days to represent 1 day, 2 days, and 3 days.
3. A set of models of GaussianNB, RandomForestClassifier, XGBClassifier, and LGBMClassifier.

- This first 3 experiments will use training set and validation set only to find the best feature set.
- The last experiment will use training set combined with validation set as the new training set to train the models and test set to evaluate the final model performance.

- First experiment is about checking which price features to include so that later experiments can build on top of the best price feature set which will be used in the next experiments.
- The second experiment is about checking which market context features to include on top of the best price feature set found in the first experiment.
- The third experiment is about checking if technical indicators, sentiment scores, and insider trading features can further improve the model performance when added on top of the best feature set found in the first experiment **(not second experiment, 1 -> (2, 3) -> 4)**.
- The fourth experiment is about checking which model performs the best with the best feature set that we handpicked from the previous experiments through analysis.


## Experiment 1: What price features to include?
Normally, close price is the main feature used for stock trend prediction. However, other price features such as volume, open, high, and low prices may also contain useful information. In this experiment, we will evaluate the impact of including different combinations of price features on the model's performance. Since we are going to predict the trend of NVDA stock, we will consider the following combinations of 4 price feature groups:
1. NVDA close price only
2. NVDA close and volume prices
3. NVDA open, high, low, close prices
4. NVDA open, high, low, close prices, and volume

### Results
- Figure showing average accuracy by price feature group and model of the validation set.
  ![Experiment 1 Results Mean](assets/exp1_mean_acc.png)
- Figure showing max accuracy by price feature group and model of the validation set.
  ![Experiment 1 Results Max](assets/exp1_max_acc.png)
- Figure showing top 10 results sorted by accuracy.
  ![Experiment 1 Results Top 10](assets/exp1_top10.png)
- From the results, we can see that including volume price along with close price gives the best performance across all models. Therefore, we will use close prices and volume as the base feature set for the next experiments.
- LightGBM performed the best among all models when using close price and volume features with maximum accuracy of 0.57 on the validation set.
- Looking into feature importance of the best LightGBM model, it might be a bit hard to interpret since there are only 2 features, but we can look into another model with OHLCV features to see how important each feature is.
- Figure showing feature importance of the best model (LightGBM) with close price and volume features.
  ![Experiment 1 Best model's Feature Importance](assets/exp1_fimp1.png)
- Figure showing feature importance of the 5th best model (LightGBM) with OHLCV features. This figure clearly shows that volume is significantly more important than the other price features.
  ![Experiment 1 5th Best model's Feature Importance with OHLCV](assets/exp1_fimp2.png)
- Conclusion: For the next experiments, we will use NVDA close price and volume as the base feature set.

## Experiment 2: What market context features to include?
In addition to NVDA stock price features, market context features such as competitors and market index prices in the form of ETFs that track the index may also provide valuable information for predicting NVDA stock trends. In this experiment, we will evaluate the impact of including different market context features on top of the best price feature set found in Experiment 1 (NVDA close price and volume). We will consider the following combinations of market context features:
1. NVDA close price and volume + AMD close price and volume
2. NVDA close price and volume + INTC close price and volume
3. NVDA close price and volume + SPY close price and volume
4. NVDA close price and volume + DIA close price and volume
5. NVDA close price and volume + IWM close price and volume
6. NVDA close price and volume + BTC close price and volume
7. NVDA close price and volume + GOLD close price and volume
8. NVDA close price and volume + AMD, INTC
9. NVDA close price and volume + SPY, DIA, IWM
10. NVDA close price and volume + BTC, GOLD
11. NVDA close price and volume + all market context features (AMD, INTC, SPY, DIA, IWM, BTC, GOLD)

### Results
- Figure showing average accuracy by feature group and model of the validation set.
  ![Experiment 2 Results Mean](assets/exp2_mean_acc.png)
- Figure showing max accuracy by feature group and model of the validation set.
  ![Experiment 2 Results Max](assets/exp2_max_acc.png)
- Figure showing top 10 results sorted by accuracy.
  ![Experiment 2 Results Top 10](assets/exp2_top10.png)
- From the results, we can see that including IWM and Gold close price and volume along with NVDA close price and volume gives the best performance across all models. The maximum accuracy is reduced by a bit compared to Experiment 1, but the precision for the "up" class has improved significantly for all the models, which is more important for our use case since we want to identify potential upward trends in NVDA stock price.
- LightGBM still performed the best among all models when using NVDA, IWM, and Gold close price and volume features with maximum accuracy of 0.56 and precision for "up" class up to 0.61 on the validation set.
- For feature importance from the best model, we can see that Gold volume, especially at the same time step (lag 0), is the most important feature, followed by NVDA close price and volume features. This indicates that Gold market activity has a significant influence on NVDA stock trends, which could be due to investors moving funds between tech stocks and precious metals as safe-haven assets during market volatility as they tend to have an inverse relationship in the short term.
  ![Experiment 2 Best model's Feature Importance](assets/exp2_fimp1.png)
- For feature importance from the 2nd best model, we can see that IWM close price features are also important, especially at lag 2 and lag 3, indicating that the overall market trend has a delayed effect on NVDA stock trends.
  ![Experiment 2 2nd Best model's Feature Importance](assets/exp2_fimp2.png)

## Experiment 3: Can technical indicators, sentiment scores, and insider trading features further improve the model performance?
- In addition to price features and market context features, technical indicators, sentiment scores, and insider trading features may also provide valuable information for predicting NVDA stock trends. In this experiment, we will evaluate the impact of including these additional feature groups on top of the best feature set found in Experiment 1 (NVDA close price and volume). The reason why we are not building on top of Experiment 2's best feature set is to see the isolated effect of adding these additional feature groups without the influence of market context features. We will consider the following combinations of feature groups:
1. NVDA close price and volume + technical indicators
2. NVDA close price and volume + sentiment scores
3. NVDA close price and volume + insider trading features (shares amount from Form 4 filings 3 days prior)

### Results
- Figure showing average accuracy by feature group and model of the validation set.
  ![Experiment 3 Results Mean](assets/exp3_mean_acc.png)
- Figure showing max accuracy by feature group and model of the validation set.
  ![Experiment 3 Results Max](assets/exp3_max_acc.png)
- Figure showing top 10 results sorted by accuracy.
  ![Experiment 3 Results Top 10](assets/exp3_top10.png)
  - From the results, we can see that including sentiment scores, technical indicators, or insider trading features along with NVDA close price and volume does not improve the model accuracy compared to using only NVDA close price and volume from Experiment 1. So they might not be useful to include in the final model, but we have to look into feature importance to see if any of these additional features are important.
- Feature importance from the best model with sentiment scores shows that sentiment scores are not very important compared to NVDA volume as it is not dominantly evident on the top like in previous experiments.
  ![Experiment 3 Best model's Feature Importance with Sentiment Scores](assets/exp3_fimp1.png)
- Feature importance from the 2nd best model with technical indicators shows that one of the technical indicators, Stochastic %K at lag 0, is actually the most important feature, even more important than NVDA close price and volume features. The Stochastic %K indicator measures the current closing price relative to the price range over a specified period, indicating potential overbought or oversold conditions. This suggests that technical indicators can provide valuable insights into short-term price movements and should be considered in the final model.
  ![Experiment 3 2nd Best model's Feature Importance with Technical Indicators](assets/exp3_fimp2.png)
- Feature importance from the 4th best model with insider trading features shows that insider trading features are not very important as it has very low importance compared to NVDA close price and volume features. By looking at other models with insider trading features, we can see that insider trading features are generally not very important.
  ![Experiment 3 4th Best model's Feature Importance with Insider Trading Features](assets/exp3_fimp3.png)
  ![Experiment 3 6th Best model's Feature Importance with Insider Trading Features](assets/exp3_fimp4.png)

## Experiment 4: Which model performs the best with the best feature set that we handpicked from the previous experiments through analysis?

Based on the analysis from the previous experiments, we have handpicked the best feature set to be NVDA close price and volume, IWM close price and volume, Gold close price and volume, and Stochastic %K technical indicator. In this experiment, we will evaluate the performance of different models using this feature set on the **test set** to determine which model performs the best for predicting NVDA stock trends. We will consider the following models:

1. NVDA close price and volume
2. NVDA close price and volume + IWM close price and volume
3. NVDA close price and volume + Gold close price and volume
4. NVDA close price and volume + Stochastic %K technical indicator
5. NVDA close price and volume + All handpicked features (IWM, Gold, Stochastic %K)
6. All features without selection

### Results
- Figure showing average accuracy by feature group and model of the test set.
  ![Experiment 4 Results Mean](assets/exp4_mean_acc.png)
- Figure showing max accuracy by feature group and model of the test set.
  ![Experiment 4 Results Max](assets/exp4_max_acc.png)
- Figure showing top 10 results sorted by precision for "up" class.
  ![Experiment 4 Results Top 10 by Precision Up](assets/exp4_mean_f1.png)
- Figure showing top 10 results sorted by accuracy.
  ![Experiment 4 Results Top 10](assets/exp4_top10.png)
- From the results of the test set, we can see that the top 10 models achieve accuracy around 0.55 to maximum of 0.5689 from Random Forest with the features have been finalized to be just NVDA close price and volume and Stochastic %K technical indicator. With the precision for "up" class and macro F1 scores also being quite good. Even though the accuracy of most models are similar, our best model uses only 3 features rather then using all features, which is much more efficient.
