import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime

# Df for the raw data from the json file 
with open('transaction-data-adhoc-analysis.json', 'r') as f:
    data = json.load(f)
df = pd.DataFrame(data)

# --- PART ONE --- 
df_one =  df.copy() # Working df for Part 1 

# Function to split the 'transaction_items' strings from the raw data
def split_items(transaction_items):
    items_list = transaction_items.split(";")
    return items_list
df_one['transaction_list'] = df_one.apply(lambda x: split_items(x["transaction_items"]), axis = 1) # Create new column, applying split_items

# Separate product name (brand and item name) and quantity from each other, then store in new columns
def product_name(transaction_list):
    product_names = []
    for item in transaction_list:
        item_info = item.split(",") # Splits each transaction item into its parts - brand, item name, and quantity
        product_names.append(item_info[0] + " " + item_info[1]) # Appends the product name (brand and item) of each transaction item into the list
    return product_names 

def quantity(transaction_list):
    quantities = []
    for item in transaction_list:
        item_info = item.split(",") # Splits each transaction item into its parts 
        num_filter = filter(str.isdigit, item_info[2]) # Filters the number from the quantity string
        quantities.append(int("".join(num_filter))) # Converts the number into an integer and appends it to list for quantities
    return quantities 
# Apply the functions to 'transaction_list' column, creating separate columns for product name and quantity
df_one['product_name'] = df_one.apply(lambda x: product_name(x['transaction_list']), axis = 1)     
df_one['quantity'] = df_one.apply(lambda x: quantity(x['transaction_list']), axis = 1) 

# Explode the product name and quantity columns so each element becomes a row
df_one = df_one.explode(['product_name','quantity']) 

# Month of each transaction date
df_one['transaction_date']=  pd.to_datetime(df_one['transaction_date'])
df_one['transaction_month'] = df_one['transaction_date'].dt.month
#  List of the months of transaction
months = df_one['transaction_month'].unique()

# Function to get unit price
def unit_price(product):
    price = df_one.loc[(df_one['product_name'] == product) & (df_one['quantity'] == 1) & (df_one['transaction_list'].str.len()==1), 'transaction_value']
    return int(price.unique()) 

# Create a df for product price list
product_list = np.sort(df_one["product_name"].unique()) # Unique list of products sorted alphabetically
pricing = pd.DataFrame(product_list, columns = ['product_name']) # Product price list df
pricing['unit_price'] = pricing.apply(lambda x: unit_price(x['product_name']), axis = 1) # Unit price of each product    

# Merge the original df (df_one) and the price list df (pricing) so that the unit price of each product reflects in each row in df_one 
df_one = pd.merge(df_one, pricing, on ='product_name') 

# Get total sales
df_one['total_sales'] = df_one['unit_price']*df_one['quantity']

# Change column names to make pivot table look cleaner
df_one = df_one.rename(columns = {'product_name':'Product Name', 'transaction_month':'Month', 'quantity':'Quantity', 'total_sales':'Sales'}) 

# Pivot table for breakdown of the quantity and sales of each product per month
transactions_overall_summary = pd.pivot_table(df_one, index ='Product Name', columns = 'Month', values= ['Quantity','Sales'], aggfunc=np.sum, margins = True, margins_name = 'Total')

# --- PART ONE GRAPHING ---

# Style for plotting
plt.style.use('ggplot')

# Monthly sales by product
monthly_sales_product_plot = pd.pivot_table(df_one, index ='Month', columns = 'Product Name', values= 'Sales', aggfunc=np.sum)
plt.figure(figsize=(12, 6))
plt.plot(monthly_sales_product_plot)
plt.title('First Half-Year Monthly Sales by Product')
plt.xticks((1,2,3,4,5,6), ('January', 'February', 'March', 'April', 'May', 'June'))
plt.xlabel("Month")
plt.ylabel("Sales")
plt.legend(product_list, bbox_to_anchor=(1.35,0.825), loc='right')
plt.savefig("monthly_sales_by_product", dpi=400, bbox_inches="tight")

# Monthly total sales
monthly_total_sales_plot = df_one.groupby('Month')['Sales'].sum()
plt.figure(figsize=(12, 6))
plt.plot(monthly_total_sales_plot)
plt.title('First Half-Year Monthly Total Sales')
plt.xticks((1,2,3,4,5,6), ('January', 'February', 'March', 'April', 'May', 'June'))
plt.xlabel("Month")
plt.ylabel("Sales")
plt.savefig("monthly_total_sales", dpi=400, bbox_inches="tight")

# Total sales by product
total_sales_product_plot = df_one.groupby('Product Name')['Sales'].sum()
plt.figure(figsize=(12, 6))
plt.pie(total_sales_product_plot, labels = product_list, autopct='%1.1f%%')
plt.title('First Half-Year Total Sales By Product')
plt.savefig("total_sales_by_product", dpi=400, bbox_inches="tight")

# Total quantity sold by product from Jan to June
total_quantity_product_plot = df_one.groupby('Product Name')['Quantity'].sum()
plt.figure(figsize=(12, 6))
plt.pie(total_quantity_product_plot, labels = product_list, autopct='%1.1f%%')
plt.title('First Half-Year Total Quantity Sold By Product')
plt.savefig("total_quantity_by_product", dpi=400, bbox_inches="tight")

# Product ratio in terms of monthly sales
product_ratio_plot = pd.pivot_table(df_one, index ='Month', columns = 'Product Name', values= 'Sales', aggfunc=np.sum).plot.bar(stacked=True, figsize = (12,6))
product_ratio_plot.set_xlabel("Month")
product_ratio_plot.set_ylabel("Sales")
product_ratio_plot.set_xticks((0,1,2,3,4,5), ('January', 'February', 'March', 'April', 'May', 'June'), rotation=0)
product_ratio_plot.legend(product_list, bbox_to_anchor=(1.35,0.825), loc='right')
product_ratio_plot.set_title("First Half-Year Product Ratio of Monthly Sales")
plt.savefig("product_ratio_of_monthly_sales", dpi=400, bbox_inches="tight")

# --- PART TWO ---

df_two = df[['name','transaction_date']].copy() # New df for Part 2

# Convert transaction date to datetime format and get the transaction month
df_two['transaction_date']= pd.to_datetime(df_two['transaction_date'])
df_two['month'] = df_two['transaction_date'].dt.month_name(locale = 'English')
months = df_two['month'].unique() # List for unique transaction month values

# Create month columns containing boolean values - TRUE: customer has transaction that month OR FALSE: no transaction that month
for i in range(len(months)):
    df_two[months[i]] = (df_two['month'] == months[i])
    
# Number of transactions of each customer monthly
monthly_transactions = df_two.groupby('name')[months].sum()

# Converts the value of each row into a list. The list summarizes the number of transactions each customer has over the transaction months.
monthly_transactions["truths_list"] = monthly_transactions.values.tolist()

# Functions that return lists indicating the months when each customer was a repeater, inactive, and/or engaged customer. 
# Values: 1 if a customer was a repeater/inactive/engaged that month; 0 if not and also 0 for the earliest month in the transactional data (repeater & inactive only) 

def check_repeaters(list): # 'list' refers to the truths_list of each customer
    repeater_truths = [] 
    for i in range(len(list)): # Goes over each month
        if i == next((i for i, x in enumerate(list) if x != 0), None): # Check if first transaction month
            repeater_truths.append(0) 
        elif (list[i] > 0) and (list[i-1] > 0): # If there is transaction that month AND previous month
            repeater_truths.append(1)
        else:
            repeater_truths.append(0)
    return repeater_truths

def check_inactive(list): # 'list' refers to the truths_list of each customer
    inactive_truths = [] 
    for i in range(len(list)): # Goes over each month
        if i == next((i for i, x in enumerate(list) if x != 0), None): # Check if first transaction month
            inactive_truths.append(0)
        elif (list[i] == 0) and (any(list[i] > 0 for i in range(0,i))): # If no transaction that month AND there is at least one transaction for one of the previous months
            inactive_truths.append(1)
        else:
            inactive_truths.append(0)
    return inactive_truths

def check_engaged(list): # 'list' refers to the truths_list of each customer
    engaged_truths = [] 
    for i in range(len(list)): # Goes over each month
        if (all(list[i] > 0 for i in range(0, i+1))): # If there is a transaction from the previous months up to current month
            engaged_truths.append(1)
        else:
            engaged_truths.append(0)
    return engaged_truths

# Lists indicating which months each customer was a repeater
repeaters_truths = monthly_transactions.apply(lambda x: check_repeaters(x['truths_list']), axis = 1).tolist()
# Total number of repeaters each month (index 0 is first month)
repeaters_sum = np.sum(repeaters_truths, 0)

# Lists indicating which months each customer was inactive
inactive_truths = monthly_transactions.apply(lambda x: check_inactive(x['truths_list']), axis = 1).tolist()
# Total number of inactive customers each month (index 0 is first month)
inactive_sum = np.sum(inactive_truths, 0) 

# Lists indicating which months each customer was engaged
engaged_truths = monthly_transactions.apply(lambda x: check_engaged(x['truths_list']), axis = 1).tolist()
# Lists the total number of engaged customers each month (index 0 is first month)
engaged_sum = np.sum(engaged_truths, 0) 

# Dataframe summarizing loyalty data
loyalty_summary = pd.DataFrame([repeaters_sum, inactive_sum, engaged_sum], index = ["Repeaters","Inactive","Engaged"], columns = [months])

# --- PART TWO GRAPHING ---

plt.figure(figsize=(12, 6))
plt.plot(months, repeaters_sum,label = "Repeater")
plt.plot(months, inactive_sum, label = "Inactive")
plt.plot(months, engaged_sum, label = "Engaged")
plt.legend()
plt.xlabel('Month')
plt.ylabel('No. of Customers')
plt.title('Customer Loyalty Statistics per Month')
plt.savefig("customer_loyalty.png", dpi=400, bbox_inches="tight")

# --- ADDITIONAL ---

df_three = df.copy()

# Group by names (names in df_three are unique) 
df_three = df_three.groupby('name')
df_three = df_three.first()

# Male and female count
male = df_three.loc[df_three['sex'] == 'M', 'sex'].count()
female = df_three.loc[df_three['sex'] == 'F', 'sex'].count()

# Sex graph
plt.style.use('ggplot')

plt.figure(figsize=(12, 6))
plt.pie([male, female], labels = ['Male', 'Female'], autopct='%1.1f%%')
plt.title('Market Distribution by Sex')
plt.savefig('sex_distribution', dpi=400, bbox_inches="tight")

# Get age
def convert_to_age(birthdate):
    birthdate = pd.to_datetime(birthdate)
    today = datetime.date.today()
    age = today.year - birthdate.year
    if (today.month, today.day) < (birthdate.month, birthdate.day): age -= 1 
    return age 

df_three['age'] = df_three['birthdate'].apply(convert_to_age)

# Age graph
plt.figure(figsize = (12, 6))
plt.hist(df_three['age'], bins = 20)
plt.title('Market Distribution by Age')
plt.savefig('age_distribution', dpi=400, bbox_inches="tight")