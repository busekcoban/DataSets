#!/usr/bin/env python
# coding: utf-8

# In[66]:


#G2M insight for Cab Investment firm
#importing libraries and datasets
import datetime
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
plt.style.use("seaborn-whitegrid")
import seaborn as sns
from collections import Counter 
from functools import reduce
cityd = pd.read_csv("City.csv", sep=";")
cityd
transactiond = pd.read_csv("Transaction_ID.csv", sep=",")
transactiond
customeridd = pd.read_csv("Customer_ID.csv",sep=";")
customeridd
cabd = pd.read_csv('Cab.csv',sep=",")
date= pd.read_csv('Date.csv')
date.info()


# In[3]:


#checking datas
cityd.describe()


# In[4]:


customeridd.describe()


# In[5]:


cabd["Date of Travel"] = date["Date of Travel"]
cabd


# In[6]:


transactiond.info()


# In[7]:


cityd.info()


# In[8]:


cabd.info()


# In[9]:


customeridd.info()


# In[10]:


cabd.describe()
cabd["Date of Travel"] = pd.to_datetime(cabd["Date of Travel"])
cabd


# In[11]:


cityd.head()


# In[12]:


transactiond.head()


# In[13]:


cabd.head()


# In[14]:


customeridd.head()


# In[15]:


cityd.info()


# In[16]:


cityd.isnull().sum()


# In[17]:


transactiond.isnull().sum()


# In[18]:


cabd.isnull().sum()


# In[19]:


customeridd.isnull().sum()


# In[20]:


#merging datas
data_frames = [cabd, transactiond]
df_merged = reduce(lambda  left,right: pd.merge(left,right,on=['Transaction ID'],
                                            how='inner'), data_frames)
data_frames


# In[21]:


data_frames = [df_merged, cityd]
df_merged2 = reduce(lambda  left,right: pd.merge(left,right,on=['City'],
                                            how='inner'), data_frames)


# In[22]:


data_frames = [df_merged2, customeridd]
total = reduce(lambda  left,right: pd.merge(left,right,on=['Customer ID'],
                                            how='inner'), data_frames)


# In[23]:


#"total" data is our final data
total


# In[24]:


#date of travel and month: year and month of transaction
#Price Charged: transaction amount received from the user
#Cost of Trip: taxi fare costs
#Percentage: Users/Population
#Income: income of users
#Gender: gender of users


# In[25]:


total["Transaction ID"] = total["Transaction ID"].astype(str)


# In[26]:


#is there any correlation between features? let's look
sns.heatmap(total.corr(), annot = True)


# In[27]:


#we can say there is a positive correlation between population and users, KM travelled and Cost of Trip


# In[28]:


total["Month"] = total["Date of Travel"].dt.month
total["Date of Travel"] = total["Date of Travel"].dt.year


# In[29]:


total["Date of Travel"] = total["Date of Travel"].astype(str)


# In[30]:


total["Profit"] = (total["Price Charged"]-total["Cost of Trip"])
total


# In[31]:


summ=total["Users"]
sns.barplot(data=total,x="Month",y=summ,hue="Company")


# In[32]:


total["Age"].describe()


# In[33]:


#Ages of users for companies
b=sns.FacetGrid(total,col = "Company")
b.map(sns.distplot,"Age",bins = 25)
plt.show()
#18-40 years old users are using Cab mostly


# In[34]:


#Users count in cities
plt.figure(figsize=(12,6))
sns.countplot(x="City", data = total)
plt.xticks(rotation = 90)
plt.show()


# In[35]:


#User count in City
#Equal amount of payment mode
plt.figure(figsize=(12,6))
sns.barplot(data=total,x="Users",y="City",hue="Payment_Mode")
plt.show()


# In[36]:


#Profit for companies
plt.figure(figsize=(12,6))
total["Sum_Profit"] = total["Profit"].sum()
sns.lineplot(x='Date of Travel' , y='Sum_Profit' ,hue='Company',data=total)
plt.show()


# In[37]:


total["Percentage"] = total["Users"]/total["Population"]*100


# In[38]:


#Users percentage for cities
plt.figure(figsize=(12,8))
total.sort_values('Percentage',inplace=True)
sns.barplot(data = total, x="City",y="Percentage")
plt.xticks(rotation = 90)
plt.ylabel("Percentage(%)")
plt.show()


# In[39]:


#Average price and age
print('Average price:',round(total["Price Charged"].mean(),1),'$')
print('Average age:',round(total["Age"].mean(),1))


# In[59]:


#Count of Users who are above and belove 30 years
agefilter =['18-40' if i <= 40 else '41-65' for i in total.Age]
df = pd.DataFrame({'Age':agefilter})
sns.countplot(x=df.Age)


# In[61]:


#Km travelled and Cost of Trip
sns.lineplot(data=total,x="KM Travelled",y="Cost of Trip")
plt.show()

