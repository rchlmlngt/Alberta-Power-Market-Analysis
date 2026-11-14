"""
Build a clean hourly supply + demand dataset

supply_demand_v1 = [date_he, actual_price, actual_ail, coal, cogeneration, ..., wind]

"""

import pandas as pd
import duckdb as ddb

#------------------------ DEMAND --------------------------------------------------------------
demand = pd.read_csv('ActualForecastData.csv', parse_dates=['date_he'])
demand = demand[['date_he', 'actual_price', 'actual_ail']]

#------------------------ SUPPLY: relabel OTHER, and then one column per sub-fuel type --------

supply = ddb.sql('''
    with other as (
        select
            date_mpt_he as date_he,
            volume,
            case
                when fuel_type = 'OTHER' then 'OTHER'   -- if fuel_type is OTHER, the new value is 'OTHER'
                else sub_fuel_type                      -- otherwise, keep the original sub_fuel_type
            end as sub_fuel_type                        -- name the resulting column sub_fuel_type
        from
            'data/supply_data.csv'
        )
    pivot                   -- which table to reshape
        other
    on                      -- whose values become the new column headers?
        sub_fuel_type
    using                   -- what goes in each cell?, needs an aggregate function
        round(sum(volume), 2)
    group by
        date_he
    order by
        date_he
''').df()
supply = supply.fillna(0)
print(supply)


#------- DST fix: on spring-forward days, relabel supply's 02:00 as 03:00 to match demand ------
full_range = pd.date_range(supply['date_he'].min(), supply['date_he'].max(), freq='h')

supply_gap = full_range.difference(supply['date_he'])
demand_gap = full_range.difference(demand['date_he'])
print(supply_gap)
print(demand_gap)
print(supply_gap.equals(demand_gap))

print(len(full_range))                  # hours in the complete range


print(supply['date_he'].nunique())      # distinct hours present in supply
print(len(supply_gap))                  # hours missing from supply

in_range = demand['date_he'].isin(full_range)
print(demand.loc[in_range, 'date_he'].nunique())   # demand hours within supply's range
print(len(demand_gap))

# replace supply gap with demand gap
if not supply_gap.equals(demand_gap):
    for s_gap, d_gap in zip(supply_gap, demand_gap):
        supply.loc[supply['date_he'] == d_gap, 'date_he'] = s_gap

supply_gap = full_range.difference(supply['date_he'])
print(supply_gap.equals(demand_gap))   # True

# check if the range are equal
s = supply['date_he'][supply['date_he'].isin(full_range)].sort_values().reset_index(drop=True)
d = demand['date_he'][demand['date_he'].isin(full_range)].sort_values().reset_index(drop=True)

print(s.equals(d))


#------------------------ Join and save -----------------------------------------------------------
supply_demand_v1 = demand.merge(supply, on='date_he', how='inner', validate='one_to_one')
print(supply_demand_v1)

#supply_demand_v1.to_csv('data/supply_demand_v1.csv', index=False)