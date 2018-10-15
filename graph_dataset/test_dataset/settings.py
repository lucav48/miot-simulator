# script execution settings

PROPERTY_TRANSACTION_TO_WATCH = ['context', 'source', 'destination']
TRANSACTION_CONTEXT_FIELD = "context"
# add edges to connect completely the graph
ADD_MORE_EDGES = 1
# add edges through a dfs algorithm
ADD_EDGES_THROUGH_DFS = 1
DEPTH_INFORMATION_FLOW = 4
NUMBER_EXPERIMENT_INFORMATION_FLOW = 100

# supervised settings
# topics "Engineering", "Gardening", "Math", "DataScience", "AI", "Economics", "Chemistry", "Cooking"
#        "Android", "Aviation", "Economics", "Earth", "Electronics", "OpenData", "Movies", "Music"
#        "Politics", "Space", "Security", "Earth", "Electronics", "Economics", "Chemistry", "History"
#        "Android", "Gardening", "AI", "Earth", "DataScience", "Math", "Cooking", "Health"
SUPERVISED_APPROACH = 1
TOPIC_SUPERVISED_APPROACH = ["Engineering", "Gardening", "Math", "DataScience", "AI", "Economics", "Chemistry", "Cooking"]


THRESHOLD_SUPERVISED = 0.01
# unsupervised settings
ALPHA_COEFFICIENT = 0.02
