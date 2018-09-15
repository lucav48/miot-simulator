from approaches import supervised_approach
from approaches import unsupervised_approach
from neo4JHandler import Neo4JManager
import BuildProfiles
import settings


if __name__ == "__main__":
    neo = Neo4JManager.Neo4JManager()
    profiles = BuildProfiles.BuildProfiles(neo)
    profiles.start()
    if settings.SUPERVISED_APPROACH:
        supervised_approach.start(profiles, neo)
    else:
        unsupervised_approach.start()
