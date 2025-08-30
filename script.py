import pandas as pd 
  
n = 5

df = pd.read_csv('freqrnc2011.csv',  sep='\t') 

result = df[(df['PoS'] == "s") & (df['Lemma'].str.len() == n) & (df['Lemma'].notna())]

result_sorted = result.sort_values('Freq(ipm)', ascending=False)

lemmas = result_sorted['Lemma'].head(1000)

with open(f'{n}_world.txt', 'w', encoding='UTF-8') as f:
    for lemma in lemmas:
        f.write(lemma + '\n')
