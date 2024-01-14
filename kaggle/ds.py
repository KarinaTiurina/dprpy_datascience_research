import pandas as pd

file_path = 'ds.kaggle/deeplearning_questions.csv'
df = pd.read_csv(file_path)

question_counts = df['DESCRIPTION'].value_counts()

question_counts_df = question_counts.reset_index()
question_counts_df.columns = ['Question', 'Occurrences']

output_file_path_pandas = 'most_common_dl_questions.csv'
question_counts_df.to_csv(output_file_path_pandas, index=False)
