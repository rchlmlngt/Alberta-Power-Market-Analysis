# Alberta Power Market Analysis

An analysis of Alberta's wholesale electricity market using 3 years of hourly data from the Alberta Electric System Operator (AESO).

## Data Source

### Actual Forecast Data
- **Provider**: Alberta Electric System Operator (AESO)
- **Period**: January 2023 - December 2025
- **Granularity**: Hourly
- **Key Variables**: Pool price ($/MWh), Alberta Internal Load (MW)

### Power Generation Data
- **Provider**: Statistics Canada
- **Period**: January 2023 - November 2025
- **Granularity**: Monthly

## Section 1: Exploratory Data Analysis (EDA)

Analysis of historical price and demand patterns to understand market dynamics.

**Key Findings:**
- Hourly demand shows consistent daily patterns with morning (6-8 AM) and evening (5-6 PM) peaks during weekdays
- Seasonal variation driven by heating/cooling demand - peaks in winter and summer months
- Higher demand does not always result in higher prices dues to merit order market structure
- Inverse relationship between pool price and wind generation, wind generation has near zero marginal cost

## Section 2: Demand Forecasting
Time series forecasting model to predict electricity demand patterns.

**Approach:**
- Model: SARIMAX model with and without exogenous variables, XGBoost
- Validation: Train/test split on historical data

*Work in progress*
