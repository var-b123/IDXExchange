#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
sold = pd.read_csv("Combined_Sold_Residential_Mortgage-Week 2-3.csv")
listings = pd.read_csv("Combined_Listings_Residential_Mortgage-Week 2-3.csv")


# In[2]:


# Record Row Counts before Cleaning
print("Sold rows before cleaning:", len(sold))
print("Listing rows before cleaning:", len(listings))


# In[3]:


# Convert Date fields to Datetime
# Transformation: Convert date columns from text to datetime because it allows accurate date comparisons and timeline analysis.
date_columns = ["CloseDate", "PurchaseContractDate", "ListingContractDate", "ContractStatusChangeDate"]

for col in date_columns:
    if col in sold.columns:
        sold[col] = pd.to_datetime(sold[col], errors="coerce")

    if col in listings.columns:
        listings[col] = pd.to_datetime(listings[col], errors="coerce")


# In[4]:


# Data Type Confirmation
print("Data Data Types (Sold)")
print(sold[date_columns].dtypes)

print("\nDate Data Types (Listings)")
print(listings[date_columns].dtypes)


# In[5]:


# Remove Unnecessary Columns
# Transformation: Remove fields with >90% missing values because these columns contribute little analytical value.
sold_missing = sold.isnull().mean()*100
listing_missing = listings.isnull().mean()*100

sold_drop = sold_missing[sold_missing > 90].index.tolist()
listing_drop = listing_missing[listing_missing > 90].index.tolist()

print("\nDropping Sold Columns:")
print(sold_drop)

print("\nDropping Listing Columns:")
print(listing_drop)

sold.drop(columns=sold_drop, inplace=True)

listings.drop(columns=listing_drop, inplace=True)


# In[6]:


# Handle Missing Values
# Transformation: Remove rows missing essential fields because these records cannot be used for market analysis.
essential_columns = [
    "ClosePrice",
    "LivingArea",
    "DaysOnMarket"
]

sold_before = len(sold)

sold = sold.dropna(subset=essential_columns)

print("\nRows removed due to missing essential values:",
      sold_before - len(sold))


# In[7]:


# Ensure Numeric Types
numeric_columns = [
    "ClosePrice",
    "ListPrice",
    "LivingArea",
    "DaysOnMarket",
    "BedroomsTotal",
    "BathroomsTotalInteger"
]

for col in numeric_columns:
    if col in sold.columns:
        sold[col] = pd.to_numeric(sold[col], errors="coerce")

    if col in listings.columns:
        listings[col] = pd.to_numeric(listings[col], errors="coerce")

print("\nNUMERIC DATA TYPES")
print(sold[numeric_columns].dtypes)


# In[8]:


# Remove Invalid Numeric Values
# Transformation: Remove impossible values because it prevents inaccurate market statistics.
before_invalid_sold = len(sold)

sold = sold[
    (sold["ClosePrice"] > 0) &
    (sold["LivingArea"] > 0) &
    (sold["DaysOnMarket"] >= 0) &
    (sold["BedroomsTotal"] >= 0) &
    (sold["BathroomsTotalInteger"] >= 0)
].copy()

print(
    "Sold rows removed with invalid numeric values:",
    before_invalid_sold - len(sold)
)

before_invalid_listings = len(listings)

listings = listings[
    (listings["ListPrice"] > 0) &
    (listings["LivingArea"] > 0) &
    (listings["DaysOnMarket"] >= 0) &
    (listings["BedroomsTotal"] >= 0) &
    (listings["BathroomsTotalInteger"] >= 0)
].copy()

print(
    "Listing rows removed with invalid numeric values:",
    before_invalid_listings - len(listings)
)


# In[9]:


# Date Consistency Checks
sold["listing_after_close_flag"] = (
    sold["ListingContractDate"] >
    sold["CloseDate"]
)

sold["purchase_after_close_flag"] = (
    sold["PurchaseContractDate"] >
    sold["CloseDate"]
)

sold["negative_timeline_flag"] = (
    sold["PurchaseContractDate"] <
    sold["ListingContractDate"]
)

print("\nDate Consistency Flag Counts")

print("listing_after_close_flag:",
      sold["listing_after_close_flag"].sum())

print("purchase_after_close_flag:",
      sold["purchase_after_close_flag"].sum())

print("negative_timeline_flag:",
      sold["negative_timeline_flag"].sum())


# In[10]:


# Geographic Data Checks
sold["missing_coordinates_flag"] = (
    sold["Latitude"].isna() |
    sold["Longitude"].isna()
)

sold["zero_coordinates_flag"] = (
    (sold["Latitude"] == 0) |
    (sold["Longitude"] == 0)
)

sold["positive_longitude_flag"] = (
    sold["Longitude"] > 0
)

sold["invalid_state_coordinates_flag"] = (
    (sold["Latitude"] < 32) |
    (sold["Latitude"] > 43) |
    (sold["Longitude"] < -125) |
    (sold["Longitude"] > -114)
)

print("\nGeographic Data Quality Summary")

print("Missing coordinates:", sold["missing_coordinates_flag"].sum())

print("Zero coordinates:", sold["zero_coordinates_flag"].sum())

print("Positive longitude:", sold["positive_longitude_flag"].sum())

print("Implausible coordinates:", sold["invalid_state_coordinates_flag"].sum())


# In[11]:


# After Row Counts
print("\nAfter Cleaning")

print("Sold rows:", len(sold))

print("Listing rows:", len(listings))


# In[12]:


sold.to_csv("Combined Sold Residential Cleaned(Week 4-5).csv", index=False)

listings.to_csv("Combined Listings Residential Cleaned(Week 4-5).csv", index=False)

print("\nCleaned datasets saved.")

