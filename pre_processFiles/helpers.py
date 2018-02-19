"""Used to get a dictionary of gague_number"""
directory_name = 'rawFiles'
end_with = '09423350.csv'

fixed_df = pd.read_csv('result_matrix.csv', sep=',', encoding='latin1', dayfirst=False, header=None).dropna(axis=1, how='all')
reference = {}
index = 0
for gague_number in fixed_df.iloc[1,:]:
    reference[int(gague_number)] = fixed_df.iloc[0,index]
    index = index + 1

print(reference)


"""Used to find gague number"""
new_reference = {}
for root,dirs,files in os.walk('rawFiles'):
    for file in files:
       if file.endswith('csv'):
           if not int(file[0:-4]) in combined_gauges:
               new_reference[int(file[0:-4])] = 999
           else:
               new_reference[int(file[0:-4])] = combined_gauges[int(file[0:-4])]


print(new_reference)



with open('combined_gauges.csv', 'w') as csv_file:
    writer = csv.writer(csv_file)
    for key, value in combined_gauges.items():
       writer.writerow([key, value])

with open('old_gauges.csv', 'w') as csv_file:
    writer = csv.writer(csv_file)
    for key, value in old_gauges.items():
       writer.writerow([key, value])

with open('new_gauges.csv', 'w') as csv_file:
    writer = csv.writer(csv_file)
    for key, value in new_gauges.items():
       writer.writerow([key, value])
