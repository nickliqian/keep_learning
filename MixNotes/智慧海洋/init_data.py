import os
import pandas as pd
pd.set_option('display.max_columns', 100)

train_path = "/Users/nick/Documents/dataset/智慧海洋/hy_round1_train_20200102"
test_path = "/Users/nick/Documents/dataset/智慧海洋/hy_round1_testA_20200102"

train_df = pd.DataFrame()
len_train = len(os.listdir(train_path))
for index, tp in enumerate(os.listdir(train_path)):
    print("{}/{}".format(index+1, len_train))
    file_path = os.path.join(train_path, tp)
    df_read = pd.read_csv(file_path)

    df_read['time'] = pd.to_datetime(df_read['time'], format='%m%d %H:%M:%S')
    df_read['speed_time'] = (df_read['time'].shift(1) - df_read['time']).dt.seconds

    train_df = train_df.append(df_read)

print(train_df.shape)  # (2699638, 7)

test_df = pd.DataFrame()
len_test = len(os.listdir(test_path))
for index, tp in enumerate(os.listdir(test_path)):
    print("{}/{}".format(index+1, len_test))
    file_path = os.path.join(test_path, tp)
    df_read = pd.read_csv(file_path)

    df_read['time'] = pd.to_datetime(df_read['time'], format='%m%d %H:%M:%S')
    df_read['speed_time'] = (df_read['time'].shift(1) - df_read['time']).dt.seconds

    test_df = test_df.append(df_read)

print(test_df.shape)  # (782378, 6)

train_df.to_csv(r"D:\dataset\智慧海洋\train_v2.csv")
test_df.to_csv(r"D:\dataset\智慧海洋\test_v2.csv")