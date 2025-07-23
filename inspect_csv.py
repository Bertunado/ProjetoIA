import pandas as pd

for peça in ['parafuso', 'correia', 'ventosa']:
    path = f'dados_{peça}.csv'
    print(f"\n=== {path} ===")
    df = pd.read_csv(path)
    print("Colunas:", df.columns.tolist())
