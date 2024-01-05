from dockerfile_parse import DockerfileParser
import yaml

def check_event_sourcing(images):

        possible_event_sourcing = False
        for image in images:
            if("kafka" in image or "rabbitmq" in image ):
                possible_event_sourcing = True
        return possible_event_sourcing
    
