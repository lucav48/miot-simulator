# script execution settings
SUPERVISED_APPROACH = 1
PROPERTY_TRANSACTION_TO_WATCH = ['context', 'source', 'destination']
TRANSACTION_CONTEXT_FIELD = "context"
# add edges to connect completely the graph
ADD_MORE_EDGES = 1
# add edges through a dfs algorithm
ADD_EDGES_THROUGH_DFS = 1
DEPTH_INFORMATION_FLOW = 2
NUMBER_EXPERIMENT_INFORMATION_FLOW = 0

# supervised settings
TOPIC_SUPERVISED_APPROACH = ["Engineering", "Gardening"]#, "Math", "DataScience", "AI", "Economics", "Chemistry", "Cooking"]
THRESHOLD_SUPERVISED = 0.01
# unsupervised settings
ALPHA_COEFFICIENT = 0.02
