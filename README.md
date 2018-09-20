# stack_tag

This program is an API used to predict tags associated to Stackoverflow questions. The API used non supervised (Negative Matrix factorization) and supervised (SGDClassifier with Linear SVM) models trained on questions extarcted from stackoverflow extraction tool (stackexchange explorer).

The questions have been cleaned using NLP module nltk and then transformed into bags-of-word. Those entries have been vectorized into TF-IDF matrices (Term Frequency Inverse Docmuent Frequency) before modeling.

The API is available at: https://stacktagging.herokuapp.com/question/ and uses json ({'question': 'question at stackoverflow fromat'}) sent by POST http request to the API.

The API return a new json with tags predicted.

The API can be tested with curl command line:
curl -i -H "Content-Type: application/json" -X POST -d '{"question":"<p>I have a collection defined as follows:</p>

                                                                     <pre><code>Public Class cData_X_Collection
                                                                        Inherits ObjectModel.Collection(Of cData_X)
                                                                     End Class
                                                                     </code></pre>

                                                                     <p>This class is used in ListView on a WPF form and works correctly.</p>

                                                                     <p>The cData_X class has an event:</p>

                                                                     <pre><code>Public Event SendCheckBoxChange()
                                                                     </code></pre>

                                                                     <p>How do I catch that event (when it is raised) in cData_X_Collection?</p>"
}' https://stacktagging.herokuapp.com/question/
