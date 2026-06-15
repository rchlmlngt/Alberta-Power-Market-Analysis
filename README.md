## Alberta Power Market Analysis

This project aims to understand the Alberta power market through data analysis by
identifying trend and relationships that are consistent with the market's underlying structure, 
and using them to feed into modelling.

### Actual Forecast Data
- **Source**: Alberta Electric System Operator (AESO)
- **Period**: January 01, 2023 - Last updated on June 08, 2026
- **Granularity**: Hourly
- **Columns**: date_he, forecast_price, actual_price, forecast_ail, actual_ail, ail_difference

### Market Context
- Alberta's wholesale electricity market runs on merit order structure where generator bids are sorted
 from least to most expensive and dispatched until demand is met, with the 
 marginal generator setting the clearing price. 
- It is an energy only market where generators are paid for the power they produce. 
- Economic withholding (raising offer prices per MWh) is permitted, 
 but physical withholding (holding capacity back from the market) is not.
- Since the coal phase out in mid 2024, the supply stack now consists of gas fired generators
and renewables, wind turbines and solar panels.
- Renewables have near-zero marginal cost, so they are dispatched first and can suppress 
 marginal price when their output is high. 

## Section 1: Exploratory Analysis

Historical price and demand patterns interpreted against market structure

### Demand Pattern

<table>
  <tr>
    <td><img src="img.png" width="100%"></td>
    <td><img src="img_1.png" width="100%"></td>
  </tr>
</table>

- Hourly demand shows a consistent daily shape. Demand ramps sharply out of the early morning trough, 
 climbs steadily through the day to a peak around hour 18, then declines overnight.
- Weekday demand is tightly clustered, sitting at similar volumes, while weekends drop noticeably 
 but follow the same daily shape.
- Residential and commercial consumption drive these observed patterns; however, 
 Alberta's production of oil and gas introduces a substantial baseload component, 
 as oil sands extraction requires continuous electricity regardless of time of day.
- Seasonal variation driven by heating/cooling demand - peaks in winter and summer months
- Annual demand peaks in winter (Dec–Feb) and summer (Jul–Aug) on heating/cooling load, 
- and bottoms out in the milder shoulder months (typically May and September).

### Price

<p align="center">
  <img src="img_2.png" width="600">
</p>

- Average hourly prices fell sharply from 2023 into 2024–2026, driven by lower natural gas prices 
 and new gas-fired and renewable capacity entering the grid.
- Natural gas now sets the price level, since gas fired generators are typically the marginal units in the merit order.
- Prices show a small morning peak around hours 7 to 9, soften through the middle of the day, 
 then ramp up to a strong evening peak. This evening peak holds late, with prices staying elevated even as demand declines.

### Price-Demand Relationship

<p align="center">
  <img src="img_3.png" width="1000">
</p>

The price-demand scatter plots reveal a marginally positive relationship, though the near-flat slopes suggest almost no linear dependence between the two variables. 
The distribution of the observations is heavily concentrated at the lower price levels indicating that for most hours the market is generally well-behaved with some hours settling at the `0/MWh` floor 
, but with isolated hours, where prices drift from the norm even reaching the regulatory price cap of `999.99/MWh`.

This pattern is expected given Alberta's merit order market structure, where generator bids are sorted from least to most expensive, 
dispatched sequentially until demand is met, and the marginal generator sets the price. As a result, prices depend on the available supply stack rather than demand. 
Extreme price events are more likely attributed to supply-side shocks such as unplanned outages, constrained generation capacity or congestion on the power line than to demand alone.

The continuous addition of renewable generators adds further complexity to Alberta's price formation. 
Since renewable generation carries near-zero marginal cost, these units are dispatched first in the merit order when available, 
displacing higher-cost natural gas generators and suppressing the pool price. This reinforces the earlier observation that higher demand does not always translate to higher prices when 
renewables are present on the grid — an hour of high renewable output coinciding with strong demand can yield lower prices, while an hour dominated by expensive marginal units 
under weak demand can produce elevated prices.

## Section 2: Detecting outliers
** Defining spikes**
how are the price aggregated, do certain hours, days, months spike more
is there a relationship between error forecast and spikes, what can we conclude


## Section 3: Demand Forecasting
Time series forecasting model to predict electricity demand patterns.

**Approach:**
- Model: SARIMAX model with and without exogenous variables, XGBoost
- Validation: Train/test split on historical data
- Stasrted with a sarimax model, but this model can only model one seasonality
- Used the correlation/seasonlaity from the sarimax model to guide features in the xgboost model
- compared a naive baseline of lagged 1 week against the xgboost model
*Work in progress*

## Section 4: Price Modelling (incoming)