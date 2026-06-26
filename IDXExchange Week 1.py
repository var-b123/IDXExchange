#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# Week 1 - Monthly Dataset Aggregation

# Sold rows after concatenation: 615725
# Sold rows before Residential filter: 615725
# Sold rows after Residential filter: 414063

# Listing rows after concatenation: 893594
# Listing rows before Residential filter: 893594
# Listing rows after Residential filter: 567549


# In[22]:


import pandas as pd
sold1 = pd.read_csv('CRMLSSold202401.csv')
sold2 = pd.read_csv('CRMLSSold202402.csv')
sold3 = pd.read_csv('CRMLSSold202403.csv')
sold4 = pd.read_csv('CRMLSSold202404.csv')
sold5f = pd.read_csv('CRMLSSold202405_filled.csv')
sold5f = sold5f.drop(columns=['latfilled', 'lonfilled'])
sold6f = pd.read_csv('CRMLSSold202406_filled.csv')
sold6f = sold6f.drop(columns=['latfilled', 'lonfilled'])
sold7f = pd.read_csv('CRMLSSold202407_filled.csv')
sold7f = sold7f.drop(columns=['latfilled', 'lonfilled'])
sold8 = pd.read_csv('CRMLSSold202408.csv')
sold9 = pd.read_csv('CRMLSSold202409.csv')
sold10 = pd.read_csv('CRMLSSold202410.csv')
sold11 = pd.read_csv('CRMLSSold202411.csv')
sold12 = pd.read_csv('CRMLSSold202412.csv')
sold13f = pd.read_csv('CRMLSSold202501_filled.csv')
sold13f = sold13f.drop(columns=['latfilled', 'lonfilled'])
sold14 = pd.read_csv('CRMLSSold202502.csv')
sold15 = pd.read_csv('CRMLSSold202503.csv')
sold16 = pd.read_csv('CRMLSSold202504.csv')
sold17 = pd.read_csv('CRMLSSold202505.csv')
sold18 = pd.read_csv('CRMLSSold202506.csv')
sold19 = pd.read_csv('CRMLSSold202507.csv')
sold20 = pd.read_csv('CRMLSSold202508.csv')
sold21 = pd.read_csv('CRMLSSold202509.csv')
sold22 = pd.read_csv('CRMLSSold202510.csv')
sold23 = pd.read_csv('CRMLSSold202511.csv')
sold24 = pd.read_csv('CRMLSSold202512.csv')
sold25 = pd.read_csv('CRMLSSold202601.csv')
sold26 = pd.read_csv('CRMLSSold202602.csv')
sold27 = pd.read_csv('CRMLSSold202603.csv')
sold28 = pd.read_csv('CRMLSSold202604.csv')

sold = pd.concat([
    sold1, sold2, sold3, sold4,
    sold5f, sold6f, sold7f,
    sold8, sold9, sold10, sold11, sold12,
    sold13f,
    sold14, sold15, sold16, sold17, sold18,
    sold19, sold20, sold21, sold22, sold23, sold24,
    sold25, sold26, sold27, sold28
], ignore_index=True)

print("Sold rows after concatenation:", len(sold))


# In[7]:


list1 = pd.read_csv('CRMLSListing202401.csv')
list2 = pd.read_csv('CRMLSListing202402.csv')
list3 = pd.read_csv('CRMLSListing202403.csv')
list4 = pd.read_csv('CRMLSListing202404.csv')
list5 = pd.read_csv('CRMLSListing202405.csv')
list6 = pd.read_csv('CRMLSListing202406.csv')
list7 = pd.read_csv('CRMLSListing202407.csv')
list8 = pd.read_csv('CRMLSListing202408.csv')
list9 = pd.read_csv('CRMLSListing202409.csv')
list10 = pd.read_csv('CRMLSListing202410.csv')
list11 = pd.read_csv('CRMLSListing202411.csv')
list12 = pd.read_csv('CRMLSListing202412.csv')

list13 = pd.read_csv('CRMLSListing202501.csv')
list14 = pd.read_csv('CRMLSListing202502.csv')
list15 = pd.read_csv('CRMLSListing202503.csv')
list16 = pd.read_csv('CRMLSListing202504.csv')
list17 = pd.read_csv('CRMLSListing202505.csv')
list18 = pd.read_csv('CRMLSListing202506.csv')
list19 = pd.read_csv('CRMLSListing202507.csv')
list20 = pd.read_csv('CRMLSListing202508.csv')
list21 = pd.read_csv('CRMLSListing202509.csv')
list22 = pd.read_csv('CRMLSListing202510.csv')
list23 = pd.read_csv('CRMLSListing202511.csv')
list24 = pd.read_csv('CRMLSListing202512.csv')

list25 = pd.read_csv('CRMLSListing202601.csv')
list26 = pd.read_csv('CRMLSListing202602.csv')
list27 = pd.read_csv('CRMLSListing202603.csv')
list28 = pd.read_csv('CRMLSListing202604.csv')

listings = pd.concat([
    list1,list2,list3,list4,list5,list6,list7,list8,
    list9,list10,list11,list12,
    list13,list14,list15,list16,list17,list18,
    list19,list20,list21,list22,list23,list24,
    list25,list26,list27,list28
], ignore_index=True)

print("Listing rows after concatenation:", len(listings))


# In[28]:


for col in sold.columns:
    print(col)


# In[24]:


print("Sold rows before Residential filter:", len(sold))
sold_residential = sold[sold['PropertyType'] == 'Residential']
print("Sold rows after Residential filter:", len(sold_residential))


# In[26]:


print("Listing rows before Residential filter:", len(listings))
listings_residential = listings[listings['PropertyType'] == 'Residential']
print("Listing rows after Residential filter:", len(listings_residential))


# In[27]:


sold_residential.to_csv('Combined_Sold_Residential.csv',index=False)
listings_residential.to_csv('Combined_Listings_Residential.csv',index=False)

