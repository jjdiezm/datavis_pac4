import pandas as pd
import numpy as np
import codecs

# original_file downloaded from https://www.peaceagreements.org/
# GWNO_file Got from http://www.correlatesofwar.org/ (Data Sets > State System Membership (v2016))
original_file = "pax_all_agreements_data.xlsx"
sandkey_file = "sandkey.txt"
chord_file = "chord.csv"

df_original = pd.read_excel(original_file)
# print(df_original.describe())
df_no_con = df_original[df_original["Loc1ISO"].isnull()]
# Assure no one has no Loc1ISO
print("Number of agreements without Loc1ISO: ".format(df_no_con.AgtId.count()))

# Prepare data to SandKeying
# Regions > Conflict Type > Status
# Regions > Agreement Stage > Agreement/Conflict Type
regions = df_original.Reg.unique()
conflict_types = df_original.Contp.unique()
status = df_original.Status.unique()
stages = df_original.Stage.unique()
agreement_types = df_original.Agtp.unique()

print(regions)
print(conflict_types)
print(status)
print(stages)
print(agreement_types)
with codecs.open(sandkey_file, 'w', encoding='utf8') as f:
    f.write('1st SandKey: Regions > Conflict Type \n')
    for continent in regions:
        for conflict in conflict_types:
            counted = df_original[(df_original.Reg == continent) & (df_original.Contp == conflict)].AgtId.count()
            f.write(continent+'['+str(counted)+']'+conflict+'\n')
    f.write('\n\n1st SandKey: Conflict Type > Status \n')
    for conflict in conflict_types:
        for state in status:
            counted = df_original[(df_original.Contp == conflict) & (df_original.Status == state)].AgtId.count()
            f.write(conflict+'['+str(counted)+']'+state+'\n')
    f.write('\n\n2nd SandKey: Regions > Agreement Stage \n')
    for continent in regions:
        for stage in stages:
            counted = df_original[(df_original.Reg == continent) & (df_original.Stage == stage)].AgtId.count()
            f.write(continent+'['+str(counted)+']'+stage+'\n')
    f.write('\n\n2nd SandKey: Agreement Stage > Agreement/Conflict Type \n')
    for stage in stages:
        for agreement_type in agreement_types:
            counted = df_original[(df_original.Stage == stage) & (df_original.Agtp == agreement_type)].AgtId.count()
            f.write(stage+'['+str(counted)+']'+agreement_type+'\n')
print("Data prepared for sandkey at: "+sandkey_file)
df_loc2_con = df_original[df_original["Loc2ISO"].notnull()]
loc1codes = df_loc2_con.Loc1ISO.unique()
loc2codes = df_loc2_con.Loc2ISO.unique()
with codecs.open(chord_file, 'w', encoding='utf8') as f:
    f.write('from,to,count\n')
    for loc1 in loc1codes:
        for loc2 in loc2codes:
            counted = df_loc2_con[(df_loc2_con.Loc1ISO == loc1) & (df_loc2_con.Loc2ISO == loc2)].AgtId.count()
            if int(counted) > 0:
                f.write(loc1+','+loc2+','+str(counted)+'\n')
print("Data prepared for Chord at: "+chord_file)
