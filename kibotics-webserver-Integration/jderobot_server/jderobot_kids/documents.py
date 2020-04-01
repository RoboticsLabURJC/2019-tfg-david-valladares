from django_elasticsearch_dsl import Document, Text, Date, Double


class SessionDocument(Document):
    username = Text()
    start_date = Date()
    end_date = Date()
    duration = Double()
    client_ip = Text()
    browser = Text()
    os = Text()
    device = Text()

    class Index:
        # Name of the Elasticsearch index
        name = 'kibotics_session_log'
        # See Elasticsearch Indices API reference for available settings
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0
        }


class SimulationDocument(Document):
    username = Text()
    start_date = Date()
    end_date = Date()
    duration = Double()
    client_ip = Text()
    simulation_type = Text()
    exercise_id = Text()
    browser = Text()
    os = Text()
    device = Text()

    class Index:
        # Name of the Elasticsearch index
        name = 'kibotics_simulation_log'
        # See Elasticsearch Indices API reference for available settings
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0
        }


class ErrorDocument(Document):
    type = Text()
    date = Date()
    username = Text()
    client_ip = Text()
    browser = Text()
    os = Text()
    device = Text()

    class Index:
        # Name of the Elasticsearch index
        name = 'kibotics_error_log'
        # See Elasticsearch Indices API reference for available settings
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0
        }


class VisitDocument(Document):
    date = Date()
    client_ip = Text()
    browser = Text()
    os = Text()
    device = Text()

    class Index:
        # Name of the Elasticsearch index
        name = 'kibotics_visit_log'
        # See Elasticsearch Indices API reference for available settings
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0
        }
