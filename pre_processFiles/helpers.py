"""Used to get a dictionary of gague_number"""
directory_name = 'rawFiles'
end_with = '09423350.csv'

fixed_df = pd.read_csv('result_matrix.csv', sep=',', encoding='latin1', dayfirst=False, header=None).dropna(axis=1, how='all')
reference = {}
for gauge in fixed_df:
    gauge_number = gauge[0]
    if int(gauge_number) in gauge_reference_gauges:
        reference[int(gauge_number)] = {'class': gauge_reference_gauges[int(gauge_number)]['class'], 'start':gauge[1], 'end':gauge[2]}
    else:
        print('Gauge not found {}'.format(gauge_number))
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

def create_reference_gauges():
    reference = {}
    with open('gauge.csv', "rt", encoding='utf8') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            if int(row[0]) in gauge_reference_gauges:
                reference[int(row[0])] = {'class': gauge_reference_gauges[int(row[0])]['class'], 'start':int(row[1]), 'end':int(row[2])}
            else:
                print('Gauge not found {}'.format(int(row[0])))
    print(reference)

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
