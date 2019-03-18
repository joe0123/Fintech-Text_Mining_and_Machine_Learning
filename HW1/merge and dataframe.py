import pandas as pd
import os

Folder_Path = r'/Users/julieta/Desktop/ETFs'         
SaveFile_Path =  r'/Users/julieta/Desktop/rename'       
SaveFile_Name = r'all.csv'

os.chdir(Folder_Path)

#資料夾下所有檔名存成list
file_list = os.listdir()

print(file_list)   

#保留col(Date adj_price)
def keep_cols(DataFrame, keep_these):
        
    drop_these = list(set(list(DataFrame)) - set(keep_these))
    return DataFrame.drop(drop_these, axis = 1)

#整理每個CSV, 另存
for i in range(1,len(file_list)):
    df = pd.read_csv(Folder_Path + '/'+ file_list[i])
    new_data = df.pipe(keep_cols, ['Date', 'Adj Close'])
    rename = new_data.rename(columns={'Adj Close': file_list[i].split('.')[0]})
    
    rename.to_csv(SaveFile_Path+'/'+'new'+file_list[i],encoding="utf_8_sig",index=False, header=True, mode='a+')

#merge
path = '/Users/julieta/Desktop/rename'     #設定所在資料夾
files = os.listdir(path)  #get all files name

df1 = pd.read_csv(path + '/' + files[0],encoding='gbk')  #讀第一個csv文件，存到df1

#df1.head()

files.remove('.DS_Store')
#print(files)

for file in files[1:]:
    df2 = pd.read_csv(path +'/' + file) 
    df1 = df1.merge(df2, on='Date', how='left')

df1.head()

df1.to_csv(path + '/' + 'total.csv') #存新檔