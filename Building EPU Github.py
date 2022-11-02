# Bulding EPU Index

# Membangun index EPU
# Bagian Subset Data
# Langkah 1: Subset data yang hanya mempunyai pattern "uncertainty" or ‘"uncertain"
# Langkah 2: Hasil subset data di langkah 1, kemudian disubset lagi dengan pattern "economic" or "economy"
# Langkah 3: Hasil subset data di langkah 2 kemudian disubset menggunakan pattern pilihan hasil diskusi, pake pattern or


# Bagian standardize and normalize
# Langkah 1: Cari variance dari seluruh berita per jenis portal berita dari seluruh periode standardize
# Langkah 2: Hitung frekuensi dari bagian subset data (per bulan) (berdasarkan prosedur subset data)
# Langkah 3: Bagi hasil langkah 2 dengan variance dari langkah 1 (per bulan)
# Langkah 4: Cari rata2 per bulan dari hasil langkah 3, rata2nya overnewspaper bukan periode bulan
# Langkah 5: Cari seluruh rata2 dari semua bulan dari hasil langkah 4 untuk periode normalisasi


# Ingat! periode standarisasi dan normalisasi berbeda
# Di paper acuan, periode standarisasi dan normalisasi sama.

import re
import pandas as pd
import numpy as np

def subset_obj(input_file, pattern):
    count_pattern = 0
    index_match = []
    for i in input_file:
        input_lower = i.lower()
        count_x = len(re.findall(pattern, input_lower))
        count_pattern += count_x
        index_list = input_file.index(i)
        if count_x==1:
            index_match.append(index_list)

    sub_list = [input_file[i] for i in index_match]
    return sub_list

def count_obj(input_file, pattern):
    count_pattern = 0
    for i in input_file:
        input_lower = i.lower()
        count_x = len(re.findall(pattern, input_lower))
        count_pattern += count_x
        
    return count_pattern

wd = ''

# Langkah 1 bagian standardize dan normalize
def find_frek_total(input_file):
    # Input file adalah dataframe per sheet bulan
    list_input = [input_file.iloc[i,0] for i in range(len(input_file.iloc[:,0]))]
    frek_berita_total = len(list_input)

    return frek_berita_total

def step1_dt_norm(list_sheet):
    # List sheet adalah list yang berisi daftar sheet per bulan
    frek_total_bulan = []
    for b in list_sheet:
      df_input = pd.read_excel(wd+'/kumpulan berita cnbc.xlsx', sheet_name=b)
      frek = find_frek_total(df_input)
      frek_total_bulan.append(frek)
     
    frek_total_bulan_array = np.array(frek_total_bulan)
    var_total = np.var(frek_total_bulan_array())
    return var_total

# Langkah 2 bagian standardize dan normalize
def find_frek(input_file, pattern_1, pattern_2, pattern_3):
    # Input file adalah dataframe per sheet bulan
    list_input = [input_file.iloc[i,0] for i in range(len(input_file.iloc[:,0]))]
    
    subset_step1 = subset_obj(list_input, pattern_1)
    subset_step2 = subset_obj(subset_step1, pattern_2)
    subset_step3 = subset_obj(subset_step2, pattern_3)
    
    frek_berita_subset = len(subset_step3)
    return frek_berita_subset

def step2_dt_norm(list_sheet):
    frek_bulan = []
    for b in list_sheet:
        df_input = pd.read_excel(wd+'/kumpulan berita cnbc.xlsx', sheet_name=b)
        frek = find_frek(df_input)
        frek_bulan.append(frek)
    
    frek_bulan_array = np.array(frek_bulan)
    return frek_bulan_array

# Langkah 3
# variance_total = step1_dt_norm(list_sheet)
# step3_array = step2_dt_norm(list_sheet) / variance_total

# Langkah 4
# Karena disini hanya menggunakan 1 portal berita saja, langkah 4 diskip

# Langkah 5
# mean_step3 = np.mean(step3_array)
# EPU = step3_array * 100/mean_step3

