import os
import glob
import pandas as pd

os.chdir(".")
extension = 'csv'
all_filenames = [i for i in glob.glob('*.{}'.format(extension))]

# Write the columns from the first fileall_filenames
index_list = ['Morphology', 'Volume']

df_names = pd.DataFrame(data={"Image": ["R01-001.nii","R01-001.nii"], "Mask": ["R01-001_roi.nii","R01-001_roi.nii"]})
#df_names.to_csv("out.csv", index=False)

df_first = pd.read_csv("R01-001.nii.csv")
df_first = df_first.T

df = pd.concat([df_names, df_first])
print(df)
df.to_csv("out.csv", mode="a", index=False, header=False)
#combine all files in the list
#csv_df = [pd.read_csv(f) for f in all_filenames ]
#csv_df.T.iloc[2,:].to_csv("out.csv", mode="a", header=False)

#export to csv
#combined_csv.to_csv( "combined_csv.csv", index=False, encoding='utf-8-sig')
