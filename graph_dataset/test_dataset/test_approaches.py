from approaches import supervised_approach
from approaches import unsupervised_approach
from neo4JHandler import Neo4JManager
import settings

if __name__ == "__main__":
    neo = Neo4JManager.Neo4JManager()
    if settings.SUPERVISED_APPROACH:
        supervised_approach.start()
    else:
        unsupervised_approach.start()
