import pandas as pd
from pandas import ExcelWriter

df = pd.read_excel('training_set_rel3.xls')
df= df.drop(df.columns[3:6],axis=1)

set1=df[df['essay_set']==1]
set1= set1.drop(set1.columns[4:],axis=1)
set1.domain1_score=(set1.domain1_score/12)*10
print (set1.head())
print (set1.columns)

set2=df[df['essay_set']==2]
set2= set2.drop(set2.columns[4:6],axis=1)
set2= set2.drop(set2.columns[5:],axis=1)
set2.domain1_score=set2.domain1_score+set2.domain2_score
set2= set2.drop(set2.columns[4],axis=1)
set2.domain1_score=(set2.domain1_score/10)*10
print (set2.head())
print (set2.columns)

set3=df[df['essay_set']==3]
set3= set3.drop(set3.columns[4:],axis=1)
set3.domain1_score=(set3.domain1_score/3)*10
print (set3.head())
print (set3.columns)

set4=df[df['essay_set']==4]
set4= set4.drop(set4.columns[4:],axis=1)
set4.domain1_score=(set4.domain1_score/3)*10
print (set4.head())
print (set4.columns)

set5=df[df['essay_set']==5]
set5= set5.drop(set5.columns[4:],axis=1)
set5.domain1_score=(set5.domain1_score/4)*10
print (set5.head())
print (set5.columns)

set6=df[df['essay_set']==6]
set6= set6.drop(set6.columns[4:],axis=1)
set6.domain1_score=(set6.domain1_score/4)*10
print (set6.head())
print (set6.columns)

set7=df[df['essay_set']==7]
set7= set7.drop(set7.columns[4:],axis=1)
set7.domain1_score=(set7.domain1_score/25)*10
print (set7.head())
print (set7.columns)

set8=df[df['essay_set']==8]
set8= set8.drop(set8.columns[4:],axis=1)
set8.domain1_score=(set8.domain1_score/60)*10
print (set8.head())
print (set8.columns)

df_final = pd.concat([set1,set2,set3,set4,set5,set6,set7,set8])
writer = ExcelWriter('test2.xlsx')
df_final.to_excel(writer,'Sheet1',index=False)
writer.save()

