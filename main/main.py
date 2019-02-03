#Developed by Trey Walker for The Butterknife 
import dataCollection as data
import pandas as pd
import numpy as np

questions = data.getSheet('B1:AB1')[0]
answers = data.getSheet('B2:AB')
df = pd.DataFrame(np.column_stack(answers),questions)
db = {}