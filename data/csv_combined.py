import pandas as pd
input_file = 'merged_file.csv'
output_file = 'filtered_file.csv'

df = pd.read_csv(input_file)
df['price'] = df['price'].replace({'\$': ''}, regex=True).astype(float)

df['quantity'] = df['quantity'].astype(float)
df['sales'] = df['price'] * df['quantity']
filtered_df = df[df['product'].str.contains('pink morsel', case=False)]
filtered_df.drop(columns=['product','price','quantity'], inplace=True)

filtered_df.to_csv(output_file, index=False)


"""
import pandas as pd

file_paths = ['daily_sales_data_0.csv', 'daily_sales_data_1.csv', 'daily_sales_data_2.csv']

dataframes = []

# Loop through the file paths and read each CSV file into a DataFrame
for file_path in file_paths:
    df = pd.read_csv(file_path)
    dataframes.append(df)

merged_df = pd.concat(dataframes, ignore_index=True)



#merged_df['sales'] = merged_df['price'] * merged_df['quantity']
#merged_df.drop(columns=['price', 'quantity'], inplace=True)
print(merged_df)

merged_df.to_csv('merged_file.csv', index=False)
"""
