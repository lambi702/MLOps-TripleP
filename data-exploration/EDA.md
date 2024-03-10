# Exploratory Data Analysis (EDA)

Exploratory Data Analysis (EDA) is a crucial step in understanding the underlying patterns, relationships, and anomalies within datasets. The following analysis is based on solar power generation data, weather conditions, and their interplay over time.

## 1. Overview of the Data

We start by examining the `merged_df` and `cleaned_df` datasets, identifying missing values, and calculating the p/n ratio, which indicates the proportion of samples to features. Despite significant missing values in `merged_df`, the p/n ratio is comfortably high, ensuring robust statistical analysis.

## 2. Data Cleaning and Preparation

The initial focus was on handling missing values, leading to the selection of a complete case analysis. The cleaned dataset (`cleaned_df`) exhibits a healthy p/n ratio, suggesting a solid foundation for further analysis.

## 3. Power Generation Analysis

### Raw Data Visualization

The visualization of raw data unveiled anomalies in power generation, particularly with `Power_8`. Cross-referencing with satellite imagery hinted at possible sensor malfunctions.

### Boxplots

Boxplots of power generation across different power plants indicated a significant discrepancy in energy production, especially between plants 1-4 and 5-8.

## 4. Seasonal Energy Production

Analysis of energy generation over time highlighted seasonal variations, with higher energy production in summer, aligning with longer daylight hours.

## 5. Weather Conditions Impact

Investigating weather-related data revealed insights into relative humidity, snowfall, temperature, precipitation, and wind speed, all of which have implications for energy production.

## 6. Outlier Detection

Outlier analysis using z-scores and the Mahalanobis distance helped identify and handle anomalous data points, ensuring a cleaner dataset for modeling.

## 7. Descriptive Statistics

Descriptive statistics offered a comprehensive view of each variable, highlighting aspects like kurtosis, skewness, means, and standard deviations, which are crucial for understanding data distribution and central tendencies.

## 8. Correlations

Correlation analysis between different variables unearthed significant relationships, particularly between solar irradiance, temperature, and power production.

## 9. Daily Production Analysis

Daily analysis demonstrated a strong correlation between solar irradiance and energy production, emphasizing the influence of sunlight on power generation.

## 10. Hourly Power Production

Examining power production across different hours of the day showed a Gaussian distribution, with peaks during midday, reflecting the solar irradiance pattern.

## 11. Monthly Variations

Monthly analysis highlighted the seasonal impact on power production, with significant differences in energy generation patterns across different months.

## 12. Key Takeaways

- Sensor data accuracy is crucial for reliable analysis.
- Weather conditions significantly influence solar power generation.
- Seasonal and diurnal patterns are evident in power production data.
- Outlier detection and handling are essential for data integrity.
- Understanding these patterns and relationships is vital for optimizing and forecasting solar energy production.

This comprehensive EDA provides a solid foundation for predictive modeling and further analysis, aiming to enhance the efficiency and reliability of solar power generation systems.
