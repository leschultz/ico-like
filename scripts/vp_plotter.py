from matplotlib import pyplot as pl
from ast import literal_eval

import pandas as pd
import argparse
import os

parser = argparse.ArgumentParser(
                                 description='Arguments to plot VP'
                                 )

parser.add_argument(
                    '-d',
                    action='store',
                    type=str,
                    help='directory containing data'
                    )

parser.add_argument(
                    '-l',
                    action='store',
                    type=str,
                    help='list of files'
                    )

args = parser.parse_args()

args.l = literal_eval(args.l)

df = []
for i in args.l:
    df.append(pd.read_csv(os.path.join(args.d, i)))

df = pd.concat(df)
df.to_csv(os.path.join(args.d, 'concated.txt'), index=False)

print(df)

groups = df.groupby(['run'])

for i, j in groups:

    fig, ax = pl.subplots()

    ax.errorbar(
                j['temp'],
                j['fraction_mean'],
                j['fraction_std'],
                ecolor='r',
                marker='.',
                linestyle='none',
                label='STDEV'
                )

    ax.errorbar(
            j['temp'],
            j['fraction_mean'],
            j['fraction_sem'],
            ecolor='y',
            marker='.',
            linestyle='none',
            label='SEM'
            )


    ax.legend()
    ax.grid()

    ax.set_title(i)
    ax.set_xlabel('Temperature [K]')
    ax.set_ylabel('VP Fraction [K]')

    fig.tight_layout()
    fig.savefig(os.path.join(args.d, i))
    pl.close('all')
