__author__ = 'Sumit Bagga'

MIGRATION_COEFF = -1
SF_BAY_AREA = 'San Francisco Bay Area'
USA_CODE = 'us'
INDIA_CODE = 'in'
CHINA_CODE = 'cn'


def calculate_migration_likelihood(connection):
    """Calculates migration coefficient of the connection
    based on location and industry of the connection. Also,
    makes a list of migration parameters to be displayed on
    the front end. Returns a tuple of migration parameters
    and migration coefficient.
    """
    migration_parameters = []
    migration_coefficient = 0
    # based on location
    if connection['location']['name'] == SF_BAY_AREA:
        migration_coefficient += 50
        migration_parameters.append('Bay Area')
    else:
        connection_country_code = \
            connection['location']['country']['code']
        if connection_country_code == USA_CODE:
            migration_coefficient += 20
            migration_parameters.append('United States')
        elif connection_country_code == INDIA_CODE:
            migration_coefficient += 10
            migration_parameters.append('India')
        elif connection_country_code == CHINA_CODE:
            migration_coefficient += 10
            migration_parameters.append('China')
        else:
            migration_parameters.append(None)

    # based on industry
    connection_industry = connection['industry']
    if 'Computer' in connection_industry or \
                    'Information Technology' in connection_industry:
        migration_coefficient += 20
        migration_parameters.append('Computer/IT')
    elif 'Recruiting' in connection_industry:
        migration_coefficient += 10
        migration_parameters.append('Recruiting')
    else:
        migration_parameters.append(None)

    # based on headline
    # No criteria for now, can be added later

    return (migration_parameters, migration_coefficient)

def valid_connection(connection):
    """Checks if the connection object is valid. Specifically, it checks if
    all the required keys are present in connection object.
    """
    connection_key_set = set(connection.keys())
    required_keys = \
        set(['firstName', 'lastName', 'industry', 'location', 'headline'])
    return required_keys.issubset(connection_key_set)

def rank_connections(connections):
    """Calculates migration coefficient for each connection and makes a
    list of tuples having connection object and migration coefficient.
    Returns the list sorted in decreasing order of migration coefficient.
    """
    connection_list = []
    for connection in connections:
        if valid_connection(connection):
            migration_likelihood = calculate_migration_likelihood(connection)
            connection_list.append((connection,) + migration_likelihood)
    # sort the connection list by migration coefficient and return
    return sorted(connection_list,
                  key=lambda connection: connection[MIGRATION_COEFF],
                  reverse=True)