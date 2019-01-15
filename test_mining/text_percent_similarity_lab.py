from sklearn.feature_extraction.text import TfidfVectorizer
"""
패키지 설치 : 
easy_install --upgrade scikit-learn
easy_install --upgrade scipy

텍스트 유사도가 정확하지 않음. 
유사도 분석을 위한  2x2
[[1.         0.29121942]
 [0.29121942 1.        ]]
"""
result_text_list = ['예 맞아요 네 고객님 실례지만 몇년생 이십니까',
                    '예 맞아요네 고객님 실례지만 몇 년생입니까']

tfidf_vectorizer = TfidfVectorizer(min_df=1)
tfidf_matrix = tfidf_vectorizer.fit_transform(result_text_list)

document_distances = (tfidf_matrix * tfidf_matrix.T)
print('유사도 분석을 위한 ', str(document_distances.get_shape()[0]) + 'x' + str(document_distances.get_shape()[1]))
print(document_distances.toarray(()))
