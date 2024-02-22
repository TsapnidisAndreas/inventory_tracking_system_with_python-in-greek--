import pandas as pd
import  numpy as np
import openpyxl

path="C:/Users/tsapn/OneDrive/Υπολογιστής/codes/python/finance applications/Αποθέματα/database/"
sales_data=pd.DataFrame(np.zeros((12,1)),index=['Ιαν. ','Φεβ. ','Μαρ. ','Απρ. ','Μα.  ','Ιουν.','Ιουλ.','Αυγ. ','Σεπ. ','Οκτ. ','Νοεμ.','Δεκ. '],columns=['Πωλήσεις'])
print(sales_data)
sales_data.to_excel(path+'Αναλυτικές Πωλήσεις ανά Μήνα.xlsx')

inventory_data=pd.DataFrame(np.zeros((1,2)),columns=['Ποσότητα','Τιμή'])
print(inventory_data)
inventory_data.to_excel(path+'Απόθεμα.xlsx',index=False)
data=pd.DataFrame(np.zeros((5,2)))
data.to_excel(path + 'Στατιστικά Στοιχεία.xlsx',index=False)