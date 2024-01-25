import pandas as pd


def get_top_questions(file_path, top_n):
    df = pd.read_csv(file_path)

    if 'DESCRIPTION' not in df.columns:
        raise ValueError("Column 'DESCRIPTION' not found in the dataframe.")

    question_counts = df['DESCRIPTION'].value_counts()

    question_counts_df = question_counts.reset_index()
    question_counts_df.columns = ['Question', 'Occurrences']

    top_questions_df = question_counts_df.head(top_n)

    return top_questions_df


