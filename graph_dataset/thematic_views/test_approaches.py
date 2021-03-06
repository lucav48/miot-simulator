from approaches import supervised_approach
from approaches import unsupervised_approach
from tools import Performance, utilities
from neo4JHandler import Neo4JManager
import BuildProfiles
import settings


if __name__ == "__main__":
    performance = Performance.Performance()
    performance.get_start_time()
    neo = Neo4JManager.Neo4JManager()
    performance.set_neo4j(neo)
    profiles = BuildProfiles.BuildProfiles(neo)
    profiles.start()
    performance.set_profiles(profiles.p_content_single_instance)
    # performance.get_network_characteristic()
    if settings.SUPERVISED_APPROACH:
        graph = supervised_approach.start(profiles, neo, performance)
    else:
        graph = unsupervised_approach.start(profiles, neo, performance)
