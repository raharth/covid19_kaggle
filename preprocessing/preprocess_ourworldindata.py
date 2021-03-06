from os import listdir
from os.path import isfile, join
import pandas as pd


def preprocess_ourworldindata(data_root, target_path):
    files = [f for f in listdir(data_root) if isfile(join(data_root, f))]
    for file in files:
        try:
            with open(data_root + file, "r") as f:
                country = file[:-4]
                line = True
                property_names = []
                value_list = []
                unit_list = []
                year_list = []

                while line:
                    line_year = f.readline()

                    if line_year == '':
                        break

                    line = f.readline().strip()
                    values = line.split(' ')

                    value = values[0]
                    unit = ''

                    unit_chars = ['%', '$', '£']
                    for dc in unit_chars:
                        if value.find(dc) > -1:
                            unit = dc
                            value = value.replace(dc, '')

                    delete_char = [',', '<', 'Â']
                    for dc in delete_char:
                        if value.find(dc) > -1:
                            value = value.replace(dc, '')

                    if len(values) == 3:
                        unit = values[1]

                    try:
                        float(value)
                        unit_list += [unit]
                        year_list += [int(values[-1][1: -1])]
                        value_list += [float(value)]
                        property_names += [line_year.strip()]
                    except ValueError:
                        print("Not a float")

            data = {p: [v] for p, v, u in zip(property_names, value_list, unit_list)}
            data['country'] = [country]
            data_frame = pd.DataFrame(data)
            data_frame.to_csv(target_path + country + '.csv')
        except Exception as e:
            print(country)
            raise e


def merge_data_frames(data_root, target_path):
    files = [f for f in listdir(data_root) if isfile(join(data_root, f))]
    data_frame = pd.DataFrame()
    for file in files:
        tmp_data_frame = pd.read_csv(data_root + file)
        data_frame = data_frame.append(tmp_data_frame, ignore_index=True)

    # data_frame = data_frame.drop('Unnamed: 0.1', axis=1)
    data_frame = data_frame.rename(columns={"Unnamed: 0": "idx"})
    data_frame.to_csv(target_path + 'merged_ourworldindata.csv')


if __name__ == "__main__":
    preprocess_ourworldindata('./data/raw_data/ourworldindata/', './data/preprocessed_data/ourworldindata/')
    merge_data_frames('./data/preprocessed_data/ourworldindata/', './data/preprocessed_data/')




