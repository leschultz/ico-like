from ast import literal_eval

import pandas as pd
import argparse

parser = argparse.ArgumentParser(
                                 description='Arguments for ICO analysis'
                                 )

parser.add_argument(
                    '-s',
                    action='store',
                    type=str,
                    help='the file with fraction data'
                    )

parser.add_argument(
                    '-p',
                    action='store',
                    type=str,
                    help='parent directory name'
                    )

parser.add_argument(
                    '-d',
                    action='store',
                    type=str,
                    help='list of temperatures of interest'
                    )

args = parser.parse_args()
args.d = literal_eval(args.d)

df = pd.read_csv(args.s)

# Filter the data by temperatures and composition
df['run'] = df['run'].apply(lambda x: x.split(args.p)[-1].split('/')[1:])
df['run'] = df['run'].apply(lambda x: [x[0], x[-1]])  # First and last
df[['system', 'temp']] = pd.DataFrame(df['run'].values.tolist(), index= df.index)
df['temp'] = df['temp'].astype(int)
df = df.loc[:, df.columns != 'run']
df = df[df['temp'].isin(args.d)]

groups = df.groupby(['temp', 'system'])

mean = groups.mean().add_suffix('_mean').reset_index()
std = groups.std().add_suffix('_std').reset_index()
sem = groups.sem().add_suffix('_sem').reset_index()
count = groups.count().add_suffix('_count').reset_index()

df = mean.merge(std)
df = df.merge(sem)
df = df.merge(count)

#df.to_csv(os.path.join(export_dir, 'tg_mean_df.txt'), index=False)
