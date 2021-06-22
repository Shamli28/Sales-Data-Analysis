#!/usr/bin/env python
# coding: utf-8

# # Preparing Data for Analysis

# - Perform Analysis & basically derive insights from the data

# ## Data Preparation

# In[2]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os  # whenever we have to deal with like,say,whenever we have to create some folder/directory/remove the directory/modify


# - Using os,you can fetch all the files available in particular location

# In[4]:


files=[file for file in os.listdir('/home/shamli/Downloads/Datasets/Sales_Data/')]  #append each n every file in my list
for file in files:
    print(file)


# In[5]:


path='/home/shamli/Downloads/Datasets/Sales_Data/' # deine a variable(path with location)
all_data=pd.DataFrame() #Declared blank dataframe & concatenate all the data in all_data

for file in files: #iterate over my list(file)
    current_df=pd.read_csv(path+"/"+file) #path+threshold(say where my file/wht is file)
    all_data=pd.concat([all_data,current_df])#concatenate dataframe 

all_data.shape


# In[6]:


all_data.to_csv('/home/shamli/Downloads/Datasets/Sales_Data/all_data.csv', index=False) #convert this data into csv,set the index-False dont want the index.all_data file has created


# In[7]:


all_data.head()


# In[8]:


# checking missing values
all_data.isnull().sum()


# In[9]:


# droping missing values
all_data=all_data.dropna(how='all')
all_data.shape


# # Analyzing Monthly Sales

# ## What is best month of sales

# In[10]:


'12/30/19 00:01'.split('/')[0] #separate it on basis of operator


# In[12]:


def month(x):
    return x.split('/')[0]


# In[13]:


all_data['month']=all_data['Order Date'].apply(month) #apply function using apply 


# In[14]:


all_data.head()


# In[15]:


# datatype of entire dataframe
all_data.dtypes


# In[16]:


# change the datatypes of three columns
all_data['month']=all_data['month'].astype(int)


# In[17]:


# check the unique value
all_data['month'].unique()


# In[18]:


filter=all_data['month']=='Order Date'
all_data=all_data[~filter] #applied negation for this filter
all_data.head()


# - Now we can easily convert datadrame to int

# In[19]:


all_data['month']=all_data['month'].astype(int)


# In[20]:


all_data.dtypes


# In[21]:


all_data['Quantity Ordered']=all_data['Quantity Ordered'].astype(int)
all_data['Price Each']=all_data['Price Each'].astype(float)


# In[22]:


all_data.dtypes


# In[23]:


# add fifth column 
all_data['Sales']=all_data['Quantity Ordered']*all_data['Price Each']


# In[24]:


all_data.head()


# In[25]:


all_data.groupby('month')['Sales'].sum()


# In[26]:


months=range(1,13)
plt.bar(months, all_data.groupby('month')['Sales'].sum())
plt.xticks(months) # setup xaxis
plt.xlabel('month')
plt.ylabel('Sales in USD')


# # Analyzing Maximum Order & Hour Analysis

# ## Which city has max order

# In[27]:


all_data.head()


# In[28]:


# fetch city from purchase address and add column city 
'136 Church St, New York City, NY 10001'.split(',')[1] #access first index from list


# In[29]:


def city(x):
    return x.split(',')[1]


# In[30]:


all_data['City']=all_data['Purchase Address'].apply(city)


# In[31]:


all_data.head()


# In[32]:


all_data.groupby('City')['City'].count().plot.bar()


# - Max value is for San Franchisco

# In[33]:


all_data['Order Date'].dtype


# In[34]:


# Convert column to daytime
all_data['Hour']=pd.to_datetime(all_data['Order Date']).dt.hour


# In[35]:


all_data.head()


# In[43]:


keys=[] # Define list
hour=[] # define hourlist
for key,hour_df in all_data.groupby('Hour'):
    keys.append(key)
    hour.append(len(hour_df))


# In[44]:


keys


# In[45]:


hour


# In[47]:


plt.grid()
plt.plot(keys,hour)


# # Analyzing Most Sold Products

# ## What product sold the most & why?

# In[49]:


# need to groupby on product bcz have to define what products sold the most
all_data.groupby('Product')['Quantity Ordered'].sum().plot(kind='bar')


# In[50]:


# analyze why this product has a max set selective 
all_data.groupby('Product')['Price Each'].mean() # mean price of each n every product


# In[51]:


# Visualize all this stuff
products=all_data.groupby('Product')['Quantity Ordered'].sum().index
quantity=all_data.groupby('Product')['Quantity Ordered'].sum()
price=all_data.groupby('Product')['Price Each'].mean()


# In[55]:


fig,ax1=plt.subplots()
ax2=ax1.twinx()  #create a twin axis sharing the xaxis
ax1.bar(products,quantity,color='g')
ax2.plot(products,price)
ax1.set_xticklabels(products,rotation='vertical',size=8) # deal with xaxis


# - top selling products seem to have a correlation with the price of the product.
# 
# - Cheaper the product, the higher the quantity ordered as well as vice versa.

# ## What products are most often sold together?

# In[56]:


all_data.head()


# - Here,you have to keep that orders that have same order ids because that are basically that products that are mostly sold together.

# In[60]:


# Keep all the order IDs that has some duplicate values
df=all_data['Order ID'].duplicated(keep=False)
df2=all_data[df]  # pass the filter in dataframe
df2.head()


# - Right Now,it means you have to do some of the transformation on this dataframe to reach to ur problem statement.

# In[64]:


# perform join operation
df2['Grouped']=df2.groupby('Order ID')['Product'].transform(lambda x:','.join(x))


# In[65]:


df2.head()


# In[66]:


df2.drop_duplicates(subset=['Order ID'])
df2.head()


# In[68]:


df2['Grouped'].value_counts()[0:5].plot.pie()


# In[ ]:




