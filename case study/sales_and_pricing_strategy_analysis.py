# -*- coding: utf-8 -*-
"""sales and pricing strategy analysis.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1JAVBi9oAsnZouy-4kz0ZkPjPv04w67iN

# <center><font size=6> **Case Description** 🎯<font><center>

**The client, a leading UK grocery retailer, is keen on accurately forecasting weekly sales volumes based on historical transactional data. Additionally, they are interested in comprehending how pricing strategies impact sales volume and are seeking recommendations in this regard.**

<img src="https://assets.epicurious.com/photos/57eebe2eb382c3c017d3fff0/16:9/w_2560%2Cc_limit/supermarket-shelves.jpg">

# **TABLE OF CONTENTS**

- **[1.Import and Insatll Libraries ⭕](#1)**
    
- **[2. Load Datasets 🧮](#2)**
    
- **[3. Exploratory data analysis](#3)**
    - ***[3.1 Over View](#3.1)***
    - ***[3.2 Missing and Duplicated Data checking](#3.2)***    
    - ***[3.3 Product Analysis](#3.3)***
    - ***[3.4 Price Changes Analysis](#3.4)***
    - ***[3.5 Sales Small Analysis](#3.5)***
    <br>
    <br>
- **[4. Forecasting Weekly sales](#4)**
- **[5. Impact of Pricing on Sales](#5)**
- **[6 Pricing Strategy Recommendations](#6)**

# **Import and Install Libraries** <a id="1"></a>
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt ; plt.rcdefaults()
import seaborn as sns
import missingno as msno
from IPython.display import display

import scipy.stats
import pylab
import datetime
from dateutil.relativedelta import relativedelta
from statsmodels.tsa.vector_ar.var_model import VAR
from sklearn.preprocessing import LabelEncoder
from scipy.stats import shapiro
from statsmodels.stats.diagnostic import acorr_ljungbox

"""# **Load Datasets** <a id="2"></a>"""

# Read Datasets ( price_changes , products , sales_small )
## get paths
price_changes_path = 'price_changes.csv'
products_path = 'products.csv'
sales_small_path = 'sales_small.csv'
## Read data as DataFrame
products = pd.read_csv(products_path)
price_changes = pd.read_csv(price_changes_path)
sales_small = pd.read_csv(sales_small_path)

display(products.sample(3))
display(price_changes.sample(3))
display(sales_small.sample(3))

"""# **Exploratory data analysis** <a id="3"></a>

## ***Dataset Oveview***
<a id="3.1"></a>
"""

products.info()

price_changes.info()

sales_small.info()

# Define a function to rename columns
def rename_columns(df):
    # Create a new DataFrame to store renamed columns
    new_dataframe = pd.DataFrame()
    # Iterate through the columns of the input DataFrame
    for col in df.columns:
        # Split the column name using '.' and take the second part (index 1) as the new name
        new_name = col.split('.')[1]
        # Assign the column to the new DataFrame with the updated name
        new_dataframe[new_name] = df[col]
    # Return the DataFrame with renamed columns
    return new_dataframe


# Renaming columns in the 'products' DataFrame
products = rename_columns(products)

# Renaming columns in the 'price_changes' DataFrame
price_changes = rename_columns(price_changes)

# Renaming columns in the 'sales_small' DataFrame
sales_small = rename_columns(sales_small)

# Display a random sample of 3 rows from the 'products' DataFrame
display(products.sample(3))

# Display a random sample of 3 rows from the 'price_changes' DataFrame
display(price_changes.sample(3))

# Display a random sample of 3 rows from the 'sales_small' DataFrame
display(sales_small.sample(3))

"""
## ***Missing and Duplicated Data checking***
<a id="3.2"></a>"""

# Display a matrix of missing values for the 'products', 'price_changes' and
#'sales_small' DataFrames

display(msno.matrix(products))

display(msno.matrix(price_changes))

display(msno.matrix(sales_small))

# Check for and remove duplicated rows in the 'products' DataFrame
products_duplicates = products[products.duplicated()]
display(f"Number of Duplicated rows in 'products': {len(products_duplicates)}")

# Check for and remove duplicated rows in the 'price_changes' DataFrame
price_changes_duplicates = price_changes[price_changes.duplicated()]
display(f"Number of Duplicated rows in 'price_changes': {len(price_changes_duplicates)}")

# Check for and remove duplicated rows in the 'sales_small' DataFrame
sales_small_duplicates = sales_small[sales_small.duplicated()]
display(f"Number of Duplicated rows in 'sales_small': {len(sales_small_duplicates)}")

"""## ***Products Analysis***
<a id="3.3"></a>
"""

# Display the first few rows of the 'products' DataFrame
products.head()

# Randomly sample 5 rows from the 'products' DataFrame
products.sample(5)

# Get the count of unique values in the 'Season' column of the 'products' DataFrame
count_values = products['Season'].value_counts()

# Display the count of each unique value
display(count_values)

# Plot a pie chart to visualize the distribution of 'Season' values
plt.title('Season Distribution')  # Add a title to the plot
plt.pie(count_values.values, labels=count_values.index, autopct='%1.1f%%', shadow=True, startangle=140)
# 'values' and 'index' are used to get the counts and corresponding labels, autopct formats the percentages,
# shadow adds a shadow to the plot, startangle sets the angle at which the pie chart starts

plt.axis('equal')  # Set the aspect ratio of the plot to be equal, ensuring a circular pie chart
plt.show()  # Display the plot

# Get the count of unique values in the 'Group' column of the 'products' DataFrame
count_values = products['Group'].value_counts()

# Display the total number of unique 'Group' values
display('Number of Groups: {}'.format(len(count_values)))

# Display the count of each unique value
display(count_values)

# Plot a bar chart to visualize the distribution of 'Group' values
plt.figure(figsize=(20,8))  # Set the figure size for better visibility
sns.barplot(x=count_values.index ,y=count_values.values)  # Create a bar plot
plt.xlabel('Groups')  # Set the label for the x-axis
plt.ylabel('Number of Products')  # Set the label for the y-axis
plt.title('Products Group')  # Add a title to the plot
plt.show()  # Display the plot

# Get the count of unique values in the 'SubGroup' column of the 'products' DataFrame
count_values = products['SubGroup'].value_counts()
# Dispaly the total number of unique 'SubGroup' values
display('Number of SubGroups: {}'.format(len(count_values)))

# Display the count of each unique value
display(count_values)

# Plot a bar chart to visualize the distribution of 'SubGroup' values
plt.figure(figsize=(20,8))  # Set the figure size for better visibility
sns.barplot(x=count_values.index ,y=count_values.values)  # Create a bar plot
plt.xlabel('Sub Group')  # Set the label for the x-axis
plt.ylabel('Number of Products')  # Set the label for the y-axis
plt.title('Products Sub Group')  # Add a title to the plot
plt.show()  # Display the plot

# Get the count of unique values in the 'Class' column of the 'products' DataFrame
count_values = products['Class'].value_counts()
# Display the number of unique 'Class' values
display('Number of Classes: {}'.format(len(count_values)))

# Get the count of unique values in the 'Class' column of the 'products' DataFrame
count_values = products['SubClass'].value_counts()
# Display the number of unique 'Class' values
display('Number of SubClass: {}'.format(len(count_values)))

"""## **Price Changes Analysis**
<a id="3.4"></a>
"""

# Display first five rows
price_changes.head()

# Get the count of unique values in the 'Channel' column of the 'price_changes' DataFrame
count_values = price_changes['Channel'].value_counts()
# Display the count of each unique value
display(count_values)
# Plot a pie chart to visualize the distribution of 'Channel' values
plt.title('Number of Changes for Channels')  # Add a title to the plot
plt.pie(count_values.values, labels=count_values.index, autopct='%1.1f%%', shadow=True, startangle=140)
# 'values' and 'index' are used to get the counts and corresponding labels, autopct formats the percentages,
# shadow adds a shadow to the plot, startangle sets the angle at which the pie chart starts
plt.axis('equal')  # Set the aspect ratio of the plot to be equal, ensuring a circular pie chart
plt.show()  # Display the plot

# Get the count of unique values in the 'Channel' column of the 'price_changes' DataFrame
count_values = price_changes['Channel'].value_counts()
# Extract labels and values for the bar chart
labels = count_values.index
values = count_values.values
# Create a bar chart to visualize the distribution of 'Channel' values
plt.figure(figsize=(9, 6))  # Set the figure size for better visibility
plt.bar(labels, values, color=['#1f77b4', '#d62728', 'lightcoral', '#7f7f7f'])  # Create the bar chart
plt.xlabel('Channels')  # Set the label for the x-axis
plt.ylabel('Number of Changes for Channels')  # Set the label for the y-axis
plt.title('Channels')  # Add a title to the plot
plt.show()  # Display the plot

# Get the count of unique values in the 'Country' column of the 'price_changes' DataFrame
count_values = price_changes['Country'].value_counts()
# Display the count of each unique value
display(count_values)
# Plot a pie chart to visualize the distribution of 'Country' values
plt.title('Country')  # Add a title to the plot
plt.pie(count_values.values, labels=count_values.index, autopct='%1.1f%%', shadow=True, startangle=140)
# 'values' and 'index' are used to get the counts and corresponding labels, autopct formats the percentages,
# shadow adds a shadow to the plot, startangle sets the angle at which the pie chart starts
plt.axis('equal')  # Set the aspect ratio of the plot to be equal, ensuring a circular pie chart
plt.show()  # Display the plot

"""## **Sales Small Analysis**
<a id="3.5"></a>
"""

# Display first five rows
sales_small.head()

# Display last five rows
sales_small.tail()

# Get the count of unique values in the 'Channel' column of the 'sales_small' DataFrame
count_values = sales_small['Channel'].value_counts()

# Display the count of each unique value
display(count_values)

# Plot a pie chart to visualize the distribution of 'Channel' values
plt.title('Sales Volume for Channels')  # Add a title to the plot
plt.pie(count_values.values, labels=count_values.index, autopct='%1.1f%%', shadow=True, startangle=140)
# 'values' and 'index' are used to get the counts and corresponding labels, autopct formats the percentages,
# shadow adds a shadow to the plot, startangle sets the angle at which the pie chart starts
plt.axis('equal')  # Set the aspect ratio of the plot to be equal, ensuring a circular pie chart
plt.show()  # Display the plot

# Get the count of unique values in the 'Channel' column of the 'sales_small' DataFrame
count_values = sales_small['Channel'].value_counts()
# Extract labels and values for the bar chart
labels = count_values.index
values = count_values.values
# Create a bar chart to visualize the distribution of 'Channel' values
plt.figure(figsize=(9, 6))  # Set the figure size for better visibility
plt.bar(labels, values, color=['#1f77b4', '#d62728', 'lightcoral', '#7f7f7f'])  # Create the bar chart
plt.xlabel('Channel')  # Set the label for the x-axis
plt.ylabel('Total Sales')  # Set the label for the y-axis
plt.title('Sales Volume For Channels')  # Add a title to the plot
plt.show()  # Display the plot

# Get the count of unique values in the 'Country' column of the 'sales_small' DataFrame
count_values = sales_small['Country'].value_counts()
# Display the count of each unique value
display(count_values)
# Plot a pie chart to visualize the distribution of 'Country' values
plt.title('Sales Volume For Country')  # Add a title to the plot
plt.pie(count_values.values, labels=count_values.index, autopct='%1.1f%%', shadow=True, startangle=140)
# 'values' and 'index' are used to get the counts and corresponding labels, autopct formats the percentages,
# shadow adds a shadow to the plot, startangle sets the angle at which the pie chart starts
plt.axis('equal')  # Set the aspect ratio of the plot to be equal, ensuring a circular pie chart
plt.show()  # Display the plot

# Get the count of unique values in the 'Country' column of the 'sales_small' DataFrame
count_values = sales_small['Country'].value_counts()
# Extract labels and values for the bar chart
labels = count_values.index
values = count_values.values
# Create a bar chart to visualize the distribution of 'Country' values
plt.figure(figsize=(9, 6))  # Set the figure size for better visibility
colors = plt.cm.Paired(range(len(labels)))  # Generate a range of colors automatically
plt.bar(labels, values, color=colors)  # Create the bar chart
plt.xlabel('Country')  # Set the label for the x-axis
plt.ylabel('Total Sales')  # Set the label for the y-axis
plt.title('Sales For Countries')  # Add a title to the plot
plt.show()  # Display the plot

# Get the count of unique values in the 'Channel' column of 'sales_small' for records where 'Country' is 'A'
count_values = sales_small[sales_small['Country'] == 'A']['Channel'].value_counts()
# Display the count of each unique value
display(count_values)
# Plot a pie chart to visualize the distribution of 'Channel' values for Country A
plt.title('Country A: Sales For Channels')  # Add a title to the plot
plt.pie(count_values.values, labels=count_values.index, autopct='%1.1f%%', shadow=True, startangle=140)
# 'values' and 'index' are used to get the counts and corresponding labels, autopct formats the percentages,
# shadow adds a shadow to the plot, startangle sets the angle at which the pie chart starts
plt.axis('equal')  # Set the aspect ratio of the plot to be equal, ensuring a circular pie chart
plt.show()  # Display the plot

# Get the count of unique values in the 'Channel' column of 'sales_small' for records where 'Country' is 'B'
count_values = sales_small[sales_small['Country'] == 'B']['Channel'].value_counts()
# Display the count of each unique value
display(count_values)
# Plot a pie chart to visualize the distribution of 'Channel' values for Country B
plt.title('Country B: Sales For Channels')  # Add a title to the plot
plt.pie(count_values.values, labels=count_values.index, autopct='%1.1f%%', shadow=True, startangle=140)
# 'values' and 'index' are used to get the counts and corresponding labels, autopct formats the percentages,
# shadow adds a shadow to the plot, startangle sets the angle at which the pie chart starts
plt.axis('equal')  # Set the aspect ratio of the plot to be equal, ensuring a circular pie chart
plt.show()  # Display the plot

# Filter 'sales_small' DataFrame for records where 'Country' is 'B', then group by 'Channel' and sum the 'SalesVolume'
df_country_channel_country_B = sales_small.loc[sales_small['Country']=='B',:].groupby(['Channel'])['SalesVolume'].sum()
# Display the first few rows of the result
df_country_channel_country_B.head()

# Filter 'sales_small' DataFrame for records where 'Country' is 'A', then group by 'Channel' and sum the 'SalesVolume'
df_country_channel_country_A = sales_small.loc[sales_small['Country']=='A',:].groupby(['Channel'])['SalesVolume'].sum()
# Count the number of records where both 'Country' is 'A' and 'Channel' is 'Online'
df_country_channel_country_A['Online'] = len(sales_small.loc[(sales_small['Country']=='A') & (sales_small['Channel']=='Online'), :])
# Sort the result by index (Channel)
df_country_channel_country_A = df_country_channel_country_A.sort_index()
# Display the first few rows of the result
df_country_channel_country_A.head()

# Create an empty DataFrame to store sales data by country and channel
sales_country_channel = pd.DataFrame()
# Add columns for 'Country A' and 'Country B' with respective sales data
sales_country_channel['Country A'] = df_country_channel_country_A
sales_country_channel['Country B'] = df_country_channel_country_B
# Add a label column with channel names (taken from 'df_country_channel_country_A' index)
sales_country_channel['label'] = df_country_channel_country_A.index
# Set the 'label' column as the index
sales_country_channel = sales_country_channel.set_index('label')
# Display the resulting DataFrame
display(sales_country_channel)
# Create a bar plot to visualize sales by country and channel
fig, ax = plt.subplots(figsize=(9, 6))  # Set the figure size
plt.xlabel('Countries')  # Set the label for the x-axis
plt.title('Sales of Countries per Channels')  # Add a title to the plot
# Plot the bar chart, specifying various parameters for aesthetics
sales_country_channel.plot.bar(ax=ax, capsize=7, rot=0, legend='upper left', color=['#ff6600', '#006cff'],
                               xlabel='Channels', ylabel='Total sales')
plt.legend(loc='lower left')  # Add a legend
plt.show()  # Display the plot

"""# **Forecasting Weekly sales**<a id="4"></a>"""

# Group 'sales_small' DataFrame by 'WeekKey'
sales_for_weeks = sales_small.groupby(['WeekKey'])
# Calculate the total sales volume for each week
pre_sales = sales_for_weeks['SalesVolume'].sum()
pre_sales = pd.DataFrame(pre_sales.reset_index()) # Get value counts and convert to DataFrame
pre_sales.columns = ['Week', 'Value'] # Rename the columns
display("Weekly Sales", pre_sales.head(3)) # Display the first few rows of the result


# Filter 'sales_small' DataFrame for records where 'Country' is 'A', then group by 'WeekKey' and sum the 'SalesVolume'
pre_sales_per_country_A = sales_small.loc[sales_small['Country'] == 'A'].groupby(['WeekKey'])['SalesVolume'].sum()
pre_sales_per_country_A = pd.DataFrame(pre_sales_per_country_A.reset_index()) # Get value counts and convert to DataFrame
pre_sales_per_country_A.columns = ['Week', 'Value'] # Rename the columns
# Display the first few rows of the result
display("Weekly Sales in Country A:",pre_sales_per_country_A.head(3))


# Filter 'sales_small' DataFrame for records where 'Country' is 'B', then group by 'WeekKey' and sum the 'SalesVolume'
pre_sales_per_country_B = sales_small.loc[sales_small['Country'] == 'B'].groupby(['WeekKey'])['SalesVolume'].sum()
pre_sales_per_country_B = pd.DataFrame(pre_sales_per_country_B.reset_index()) # Get value counts and convert to DataFrame
pre_sales_per_country_B.columns = ['Week', 'Value'] # Rename the columns
# Display the first few rows of the result
display("Weekly Sales in Country B:", pre_sales_per_country_B.head(3))


# Filter 'sales_small' DataFrame for records where 'Channel' is 'Online', then group by 'WeekKey' and sum the 'SalesVolume'
sales_volume_online = sales_small.loc[sales_small['Channel'] == 'Online'].groupby(['WeekKey'])['SalesVolume'].sum()
sales_volume_online = pd.DataFrame(sales_volume_online.reset_index()) # Get value counts and convert to DataFrame
sales_volume_online.columns = ['Week', 'Value'] # Rename the columns
# Display the first few rows of the result
display("Weekly Sales in Channel Online:", sales_volume_online.head(3))


# Filter 'sales_small' DataFrame for records where 'Channel' is 'Stores', then group by 'WeekKey' and sum the 'SalesVolume'
sales_volume_stores = sales_small.loc[sales_small['Channel'] == 'Stores'].groupby(['WeekKey'])['SalesVolume'].sum()
sales_volume_stores = pd.DataFrame(sales_volume_stores.reset_index()) # Get value counts and convert to DataFrame
sales_volume_stores.columns = ['Week', 'Value'] # Rename the columns
# Display the first few rows of the result
display("Weekly Sales in Channel Stores:", sales_volume_stores.head(3))

# Create a DataFrame to store pre-sales information
pre_sales_for_products = pd.DataFrame()

# Assign columns using dictionaries for better organization
pre_sales_for_products['date'] = pre_sales["Week"].astype("str")
pre_sales_for_products['sales_volume_all'] = pre_sales["Value"]
pre_sales_for_products['sales_volume_country_A'] = pre_sales_per_country_A["Value"]
pre_sales_for_products['sales_volume_country_B'] = pre_sales_per_country_B["Value"]
pre_sales_for_products['sales_volume_online'] = sales_volume_online["Value"]
pre_sales_for_products['sales_volume_stores'] = sales_volume_stores["Value"]
pre_sales_for_products.head()

pre_sales_for_products.info()

def convert_date(data_frame):
    # Convert 'Date' column to datetime format
    data_frame['year'] = data_frame['date'].str[:4]
    data_frame['week'] = data_frame['date'].str[4:]
    # Create a new column with formatted dates
    data_frame['formatted_date'] = data_frame['year'] + '-' + data_frame['week'] + '-0'
    # Convert to datetime
    data_frame['date'] = pd.to_datetime(data_frame['formatted_date'], format='%Y-%U-%w')
    # Drop temporary columns
    data_frame.drop(['year', 'week', 'formatted_date'], axis=1, inplace=True)
    # Set 'Date' column as the index
    data_frame.set_index('date', inplace=True)
    return data_frame

pre_sales_for_products = convert_date (pre_sales_for_products)
pre_sales_for_products.head(5)

# Iterate over columns in the DataFrame
for col in pre_sales_for_products.columns:
    # Display the name of the current column
    display(col)
    # Create a probability plot for the data in the current column
    scipy.stats.probplot(pre_sales_for_products[col], plot=pylab)
    # Display the probability plot
    plt.show()
    # Print a separator
    print('----' * 20)

pre_sales_for_products.index.freq = 'W'
train = pre_sales_for_products.head(48)
test = pre_sales_for_products.tail(12)

model = VAR(endog=train)
model_fit = model.fit()

# Forecast sales for the test dataset
forecast = model_fit.forecast(train.values[-model_fit.k_ar:], steps=len(test))

result = list()
for index , row in enumerate(forecast) :
  result.append({"week":index + 1 ,
                  "sales_volume_all":round(forecast[index][0]),
                  "sales_volume_per_country_A":round(forecast[index][1]) ,
                  "sales_volume_per_country_B":round(forecast[index][2]) ,
                  "sales_volume_online":round(forecast[index][3]) ,
                  "sales_volume_stores":round(forecast[index][4])
                  })

results_df = pd.DataFrame(result)
results_df

# Get the residuals
residuals = test.values - forecast
residuals = pd.DataFrame(residuals, columns=test.columns)

# Perform normality test (e.g., Shapiro-Wilk test)
stat, p_value = shapiro(residuals["sales_volume_all"])
print(f'Shapiro-Wilk Test Statistic: {stat:.4f}, p-value: {p_value:.4f}')

# Plot a histogram of the residuals
plt.hist(residuals["sales_volume_all"], bins=20)
plt.title('Residuals Sales Volume All Histogram')
plt.xlabel('Residuals')
plt.ylabel('Frequency')
plt.show()

model = VAR(endog=pre_sales_for_products)
model_fit = model.fit()
# Forecast sales for the next four weeks (4 steps ahead)
forecast = model_fit.forecast(train.values[-model_fit.k_ar:], steps=4)
result = list()
for index , row in enumerate(forecast) :
  result.append({"week":index + 1 ,
                  "sales_volume_all":round(forecast[index][0]),
                  "sales_volume_per_country_A":round(forecast[index][1]) ,
                  "sales_volume_per_country_B":round(forecast[index][2]) ,
                  "sales_volume_online":round(forecast[index][3]) ,
                  "sales_volume_stores":round(forecast[index][4])
                  })

results_df = pd.DataFrame(result)
results_df

results_df.to_csv('forecasting_weekly_sales.csv' , index=False)

"""# **Impact of Pricing on Sales** <a id="5"></a>"""

# Merge 'sales_small' DataFrame with 'products' DataFrame based on the 'ProductID' column
# This operation combines the two DataFrames using a common column as the key
sales_small_and_products = pd.merge(sales_small, products, how="inner", on="ProductID")

# Merge 'sales_small_and_products' DataFrame with 'price_changes' DataFrame based on multiple columns
# This operation combines the two DataFrames using multiple columns as the keys
data = pd.merge(
    sales_small_and_products,
    price_changes,
    how='inner',
    on=['ProductID', 'WeekKey', 'Channel', 'Country'])

data.head()

data["change_amount"] = data['CSP_x']  - data['OSP']
del data['CSP_x']

numerical_columns = data.select_dtypes(include=['integer', 'float'])
plt.figure(figsize=(12,9))
sns.heatmap(numerical_columns.corr(),cmap='RdBu', annot=True,fmt=".0%")
plt.show()

data.sample(5)

count_values = data.groupby(['Group'])['SalesVolume'].sum().sort_values(ascending=False)
print(count_values)
# Plot
plt.figure(figsize=(20,8))
sns.barplot(x=count_values.index ,y=count_values)
plt.xlabel('Group')
plt.ylabel('Sales volume')
plt.title('products Group')
plt.show()
print('Number of Group : {}'.format(len(count_values)))

count_values = data.groupby(['SubGroup'])['SalesVolume'].sum().sort_values(ascending=False)
print(count_values)
# Plot
plt.figure(figsize=(20,8))
sns.barplot(x=count_values.index ,y=count_values)
plt.xlabel('Group')
plt.ylabel('Sales volume')
plt.title('products Sub Group')
plt.show()
print('Number of Group : {}'.format(len(count_values)))

"""# **Pricing Strategy Recommendations** <a id="6"></a>"""

rec_data = data.sort_values(by='ProductID', ascending=False)

rec_data.head(5)

"""> 1- Increase the number of goods in the warehouse in the L season

> 2- Increase the number of products in stock from the following groups ( 26387251 ,606565a1 ,bca94c97 ,c8e7b2df , edf80f3a )

> 3- Do not keep any products in stock from the following groups ( 3bc0de94 , 49e9a58f )

> 4- Addition of the online purchase service in country A

> 5- Developing and improving the marketing of online stores in the country B

> 6- We observed a strong correlation between the number of goods in stock and the volume of sales

> 7- The lower the price of the product, the higher the percentage of sales by 11%

# Conclusion:  **The lower the price of the product, the higher the percentage of sales by 11%**
"""

