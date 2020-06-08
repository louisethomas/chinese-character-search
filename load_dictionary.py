count = 1
with open('DATA_FILES/cedict_ts.u8') as file:
    line = file.readline()
    while line:
        if (line[0] != '#') and (line.find('surname') == -1):   #skip comment lines and surnames
            print('\n' + line.strip())
            simplified = line.partition(' ')[0]
            print('Simplified: {}'.format(simplified))
            traditional = line.partition(' ')[2].partition(' ')[0]
            print('Traditional: {}'.format(traditional))
            pinyin = line.partition('[')[2].partition(']')[0]
            print('Pinyin: {}'.format(pinyin))
            definition = line.partition('/')[2].replace('/','; ').strip()
            print(definition)

        line = file.readline()
        count += 1
        if count == 100:
            break

