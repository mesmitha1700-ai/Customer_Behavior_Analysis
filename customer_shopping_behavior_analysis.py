import pandas as pd
df = pd.read_csv('customer_shopping_behavior.csv')
df.head()
df.info()
df.describe(include='all')
df.isnull().sum()
df['Review Rating'] = df.groupby('Category')['Review Rating'].transform(lambda x: x.fillna(x.median()))
df.isnull().sum()
df.columns = df.columns.str.lower()
df.columns = df.columns.str.replace(' ','_')
df = df.rename(columns={'purchase_amount_(usd))':'purchase_amount'})
df.columns

#create a column age_group
labels = ['young Adult','Adult','Middle_aged','senior']
df['age_group']=pd.qcut(df['age'], q=4, labels = labels)
df[['age','age_group']].head(10)

#create column purchase_frequency_days
frequency_mapping={
    'fortnightly':14,
    'weekly':7,
    'monthly':30,
    'quarterly':90,
    'bi-weekly':14,
    'annually':365,
    'every 3 months':90
}
df['purchase_frequency_days']=df['frequency_of_purchases'].map(frequency_mapping)
df[['purchase_frequency_days','frequency_of_purchases']].head(10)
df[['discount_applied','promo_code_used']].head(10)
(df['discount_applied']==df['promo_code_used']).all()
df=df.drop('promo_code_used',axis=1)
df.columns

from sqlalchemy import create_engine
#my sql connection
username="root"
password="root"
host="localhost"
port="3306"
database="Mydatabase"
engine = create_engine(f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}")

#write dataframe to ms sql
table_name = "customer"
df.to_sql(table_name, engine, if_exists="replace",index=False)

#READ BACK SAMPLE
pd.read_sql("select * FROM customer LIMIT 5;",engine)
