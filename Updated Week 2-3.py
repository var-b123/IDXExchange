#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# Dataset Structuring & Validation


# In[46]:


# Load Week 1 outputs
import pandas as pd
sold = pd.read_csv('Combined_Sold_Residential-Week 1.csv')
listings = pd.read_csv('Combined_Listings_Residential-Week 1.csv')


# In[47]:


# Inspect Structure
print("SOLD DATASET")
print("Rows:", sold.shape[0])
print("Columns:", sold.shape[1])

print("\nLISTINGS DATASET")
print("Rows:", listings.shape[0])
print("Columns:", listings.shape[1])


# In[48]:


print("\nSold data types")
print(sold.dtypes)

print("\nListing data types")
print(listings.dtypes)


# In[23]:


print(sold.head())
print(listings.head())


# In[51]:


print(sold["PropertyType"].unique())
print(listings["PropertyType"].unique())


# In[50]:


# Market analysis fields
market_fields = [
    "ClosePrice",
    "ListPrice",
    "OriginalListPrice",
    "LivingArea",
    "BedroomsTotal",
    "BathroomsTotalInteger",
    "DaysOnMarket",
    "YearBuilt",
    "CountyOrParish",
    "CloseDate"
]

# Metadata fields
metadata_fields = [
    "ListingKey",
    "ListingKeyNumeric",
    "OriginatingSystemName",
    "OriginatingSystemSubName",
    "ListAgentEmail",
    "BuyerAgentMlsId"
]

print("Market analysis fields:")
print(market_fields)

print("\nMetadata fields:")
print(metadata_fields)


# In[52]:


# Missing value counts
sold_missing = sold.isnull().sum()
listing_missing = listings.isnull().sum()
print(sold_missing)
print(listing_missing)


# In[53]:


# Missing percentages
sold_missing_percent = sold.isnull().mean()*100
listing_missing_percent = listings.isnull().mean()*100
print(sold_missing_percent.sort_values(ascending=False))
print(listing_missing_percent.sort_values(ascending=False))


# In[57]:


# Columns with over 90% missing (To be dropped)
print("Sold columns with >90% missing (to be dropped):")
print(sold_missing_percent[sold_missing_percent > 90])

print("\nListing columns with >90% missing (to be dropped):")
print(listing_missing_percent[listing_missing_percent > 90])


# In[59]:


# Columns to Drop vs Retain
drop_columns = sold_missing_percent[
    sold_missing_percent > 90
].index.tolist()

listing_drop_columns = listing_missing_percent[
    listing_missing_percent > 90
].index.tolist()

print("\nCore fields retained for analysis:")
print([
    "ClosePrice",
    "ListPrice",
    "LivingArea",
    "BedroomsTotal",
    "BathroomsTotalInteger",
    "DaysOnMarket",
    "YearBuilt"
])

# Drop the columns
sold = sold.drop(columns=drop_columns, errors="ignore")
listings = listings.drop(columns=listing_drop_columns, errors="ignore")

print("\nSold columns after dropping:", sold.shape[1])
print("Listing columns after dropping:", listings.shape[1])


# In[60]:


# Numeric Distribution
numeric_cols = ['ClosePrice','LivingArea','DaysOnMarket']
for col in numeric_cols:
    print(f"\n{col}")
    print(sold[col].describe(percentiles=[.01,.05,.25,.50,.75,.95,.99]))


# In[15]:


columns = [
    "ClosePrice",
    "ListPrice",
    "OriginalListPrice",
    "LivingArea",
    "LotSizeAcres",
    "BedroomsTotal",
    "BathroomsTotalInteger",
    "DaysOnMarket",
    "YearBuilt"]

print(sold[columns].describe(percentiles=[0.01,0.05,0.25,0.5,0.75,0.95,0.99]))


# In[61]:


# Histograms
import matplotlib.pyplot as plt

for col in columns:
    sold[col].hist(bins=40)
    plt.title(col)
    plt.show()


# In[62]:


# Boxplots
for col in columns:
    sold.boxplot(column=col)
    plt.title(col)
    plt.show()


# In[63]:


# Extreme Outliers
for col in columns:

    Q1 = sold[col].quantile(.25)
    Q3 = sold[col].quantile(.75)

    IQR = Q3 - Q1

    lower = Q1 - 1.5*IQR
    upper = Q3 + 1.5*IQR

    outliers = sold[
        (sold[col] < lower) |
        (sold[col] > upper)
    ]

    print(col)
    print("Outliers:", len(outliers))


# In[64]:


# Residential vs Other Share
print(
    sold["PropertyType"]
    .value_counts(normalize=True)*100
)


# In[65]:


# Average and Median Close Price
print("Average Close Price")
print(sold["ClosePrice"].mean())
print()
print("Median Close Price")
print(sold["ClosePrice"].median())


# In[66]:


# Days on Market Distribution
print(sold["DaysOnMarket"].describe())


# In[67]:


# Percent Sold Above List Price
above = (sold["ClosePrice"] > sold["ListPrice"]).mean()*100
below = (sold["ClosePrice"] < sold["ListPrice"]).mean()*100
equal = (sold["ClosePrice"] == sold["ListPrice"]).mean()*100
print("Above list:", above)
print("Below list:", below)
print("Equal to list:", equal)


# In[68]:


# Date Consistency 
sold["CloseDate"] = pd.to_datetime(sold["CloseDate"])
sold["ListingContractDate"] = pd.to_datetime(sold["ListingContractDate"])
bad_dates = sold[sold["CloseDate"] < sold["ListingContractDate"]]
print("Rows with CloseDate before ListingContractDate")
print(len(bad_dates))


# In[69]:


# Highest Median County Prices
county_prices = (sold.groupby("CountyOrParish")["ClosePrice"].median().sort_values(ascending=False))
print(county_prices)


# In[70]:


sold.to_csv("Week2_Residential_Validated.csv", index=False)


# In[71]:


listings.to_csv("Week2_Listings_Validated.csv",index=False)


# In[ ]:


# Mortgage Rate Enrichment


# In[72]:


# Download Data
import pandas as pd
url = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=MORTGAGE30US"
mortgage = pd.read_csv(url, parse_dates=['observation_date'])
mortgage.columns = ['date', 'rate_30yr_fixed']


# In[73]:


# Resample Weekly Rates to Monthly Averages
mortgage['year_month'] = mortgage['date'].dt.to_period('M')
mortgage_monthly = (
    mortgage.groupby('year_month')['rate_30yr_fixed']
    .mean()
    .reset_index())


# In[74]:


# Create Matching Keys
sold["CloseDate"] = pd.to_datetime(sold["CloseDate"])

sold["year_month"] = sold["CloseDate"].dt.to_period("M")

listings["ListingContractDate"] = pd.to_datetime(
    listings["ListingContractDate"])

listings["year_month"] = (
    listings["ListingContractDate"]
    .dt.to_period("M"))


# In[75]:


# Merge Mortgage Rates
sold_with_rates = sold.merge(mortgage_monthly, on="year_month", how="left")
listings_with_rates = listings.merge(mortgage_monthly, on="year_month", how="left")


# In[78]:


# Validate Merge
print("Missing mortgage rates in sold:", sold_with_rates["rate_30yr_fixed"].isnull().sum())
print("Missing mortgage rates in listings:", listings_with_rates["rate_30yr_fixed"].isnull().sum())
print(sold_with_rates[["CloseDate", "year_month", "ClosePrice", "rate_30yr_fixed"]].head())


# In[79]:


# Save Datasets
sold_with_rates.to_csv(
    "Combined_Sold_Residential_Mortgage-Week 2-3.csv",
    index=False)

listings_with_rates.to_csv(
    "Combined_Listings_Residential_Mortgage-Week 2-3.csv",
    index=False)

