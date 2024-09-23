import pandas as pd
import spacy
# Load the CSV file
file_path = r'.\scopus\scopus_20k.csv'
data = pd.read_csv(file_path)

nlp = spacy.load('en_core_web_sm')


def lemmatize_keyword(keyword):
    doc = nlp(keyword)
    return " ".join([token.lemma_ for token in doc])


#################################### keywords author
# Extract the 'Author Keywords' column
keywords_author = data['Author Keywords']


# Initialize a dictionary to store keyword counts for author
keywords_counts_author = {}

# Iterate through the column to split by ';' and count keywords
for keywords in keywords_author.dropna():  
    keywords_list = keywords.split(';')
    for keyword in keywords_list:
        keyword = keyword.strip().lower()  # Normalize by stripping spaces and converting to lowercase
        keyword = lemmatize_keyword(keyword)
        
        if keyword in keywords_counts_author:
            keywords_counts_author[keyword] += 1
        else:
            keywords_counts_author[keyword] = 1

# Convert the dictionary to a DataFrame 
keywords_counts_author_df = pd.DataFrame(list(keywords_counts_author.items()), columns=['Keyword', 'Count'])
keywords_counts_author_df.sort_values(by='Count', ascending=False, inplace=True)  # descending

keywords_counts_author_df['Keyword'] = keywords_counts_author_df['Keyword'].astype(str)


# Convert the dictionary to a DataFrame 
keywords_counts_author_df = pd.DataFrame(list(keywords_counts_author.items()), columns=['Keyword', 'Count'])
keywords_counts_author_df.sort_values(by='Count', ascending=False, inplace=True)  # descending

keywords_counts_author_df['Keyword'] = keywords_counts_author_df['Keyword'].astype(str)


keywords_counts_author_df.to_csv(r'.\scopus\keyword_counts_author.csv',
                        index=False )


##################    keywords index
# Initialize a dictionary to store keyword counts for index
keywords_index = data['Index Keywords']

keywords_counts_index = {}

# Iterate through the column to split by ';' and count keywords
for keywords in keywords_index.dropna():  
    keywords_list_index = keywords.split(';')
    for keyword_index in keywords_list_index:
        keyword_index = keyword_index.strip().lower()  # Normalize by stripping spaces and converting to lowercase
        keyword_index = lemmatize_keyword(keyword_index)

        if keyword_index in keywords_counts_index:
            keywords_counts_index[keyword_index] += 1
        else:
            keywords_counts_index[keyword_index] = 1


# Convert the dictionary to a DataFrame 
keywords_counts_index_df = pd.DataFrame(list(keywords_counts_index.items()), columns=['Keyword', 'Count'])
keywords_counts_index_df.sort_values(by='Count', ascending=False, inplace=True)  # descending

keywords_counts_index_df['Keyword'] = keywords_counts_index_df['Keyword'].astype(str)


# Convert the dictionary to a DataFrame 
keywords_counts_index_df = pd.DataFrame(list(keywords_counts_index.items()), columns=['Keyword', 'Count'])
keywords_counts_index_df.sort_values(by='Count', ascending=False, inplace=True)  # descending

keywords_counts_index_df['Keyword'] = keywords_counts_index_df['Keyword'].astype(str)


keywords_counts_index_df.to_csv(r'.\scopus\keyword_counts_index.csv',
                        index=False )