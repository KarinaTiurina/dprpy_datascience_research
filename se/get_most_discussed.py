from se.ai import AISEQuestionAnalyzer
from se.cs import ComputerScienceSEQuestionAnalyzer
from se.ds import DataScienceSEQuestionAnalyzer
import pandas as pd


def get_most_discussed():
    file_path_ds = "datascience.stackexchange.com/Posts.xml"
    ds_analyzer = DataScienceSEQuestionAnalyzer(file_path_ds)

    file_path_cs = "cs.stackexchange.com/Posts.xml"
    cs_analyzer = ComputerScienceSEQuestionAnalyzer(file_path_cs)

    file_path_ai = "ai.stackexchange.com/Posts.xml"
    ai_analyzer = AISEQuestionAnalyzer(file_path_ai)

    comment_path_ds = "datascience.stackexchange.com/Comments.xml"
    ds_analyzer.load_and_filter_questions()
    ds_comments = ds_analyzer.get_most_discussed_questions(comment_path_ds)
    ds_comments["Source"] = "Data Science"

    comment_path_cs = "cs.stackexchange.com/Comments.xml"
    cs_analyzer.load_and_filter_questions()
    cs_comments = cs_analyzer.get_most_discussed_questions(comment_path_cs)
    cs_comments["Source"] = "Computer Science"

    comment_path_ai = "ai.stackexchange.com/Comments.xml"
    ai_analyzer.load_and_filter_questions()
    ai_comments = ai_analyzer.get_most_discussed_questions(comment_path_ai)
    ai_comments["Source"] = "Artificial Intelligence"

    # merge all dataframes
    merged = pd.concat([ds_comments, cs_comments, ai_comments])
    # sort by count
    merged = merged.sort_values(by="CommentsCount", ascending=False)
    # reset index
    merged = merged.reset_index()[["CleanTitle", "CommentsCount", "Source"]]
    # return top 10
    return merged.head(10)
