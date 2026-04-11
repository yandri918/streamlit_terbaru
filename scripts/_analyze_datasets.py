import pandas as pd

# === ANALISIS yield_df.csv ===
df = pd.read_csv('yield_df.csv')
print('=== ANALISIS YIELD_DF.CSV ===')
print('Total baris:', len(df))
print('Tahun range:', df['Year'].min(), '-', df['Year'].max())
print('Jumlah negara:', df['Area'].nunique())
print('Jumlah tanaman:', df['Item'].nunique())
print('Daftar tanaman:')
for c in sorted(df['Item'].unique()):
    print('  -', c)
print()
print('Missing values:')
print(df.isnull().sum())
print()
print('Statistik Yield (hg/ha):')
print(df['hg/ha_yield'].describe())
print()

# Cek data Indonesia
has_id = df[df['Area'].str.contains('Indonesia', case=False, na=False)]
print('Data Indonesia:', len(has_id), 'baris')
if len(has_id) > 0:
    print(has_id[['Area','Item','Year','hg/ha_yield']].head(10).to_string())
