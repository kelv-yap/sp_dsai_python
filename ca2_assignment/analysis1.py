from ca2_assignment import mysql_config as config
import sys
import numpy as np
import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt

# DATABASE: MYSQL CONNECTION
user, pw, host, db = config.user, config.pw, config.host, config.db


def retrieve_data_from_mysql():
    connection = mysql.connector.connect(user=user, password=pw, host=host, database=db, use_pure=True)
    cursor = connection.cursor()

    query_table = 'SELECT region, purchase_year, price_per_sqft FROM resale_hdb'

    try:
        cursor.execute(query_table)
        data = pd.DataFrame(cursor.fetchall(),
                            columns=['region', 'purchase_year', 'price_per_sqft'])
        connection.commit()
    except:
        print("Unexpected error:", sys.exc_info()[0])
        exit()
    finally:
        cursor.close()
        connection.close()

    print("Data Count (Saved Data): {}".format(data.shape[0]))
    return data


df = retrieve_data_from_mysql()
df = df.groupby(['region', 'purchase_year'], as_index=False)['price_per_sqft'].mean()
df = df.pivot(index='purchase_year', columns='region', values='price_per_sqft')

df.plot(color=['orange', 'green', 'red', 'purple', 'black'])

years = df.index
legend = plt.legend(loc='upper left', shadow=True, title='Region')
plt.grid(axis='x', alpha=0.5)
plt.grid(axis='y', alpha=0.5)
plt.suptitle("HDB RESALE PRICE \n between Year {} to {}".format(years.min(), years.max()), fontsize=14, fontweight='bold')
plt.title("Average Resale Price per Square Feet (sqft) by Region")
plt.xlabel("Year")
plt.ylabel("Price per sqft (SGD)")
plt.xticks(np.arange(len(years)), years, rotation=45)
plt.yticks(np.arange(0, 700, 100))

plt.show()
