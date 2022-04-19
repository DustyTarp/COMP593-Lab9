
import requests

def get_poki_info(name):
    """
    Gets all info about a specified pokemon from poki api

    :param name: Pokemon name
    :returns: Dictionary of pokemon info, if successful. None if not
    """
    print("Getting pokimon information...", end='')

    if name is None:
        print('error: missing name parameter')
        return

    name = name.strip().lower()
    if name == ' ':
        print('error: empty')
        return
    URL = 'https://pokeapi.co/api/v2/pokemon/' + str(name)
    response = requests.get(URL)

    if response.status_code == 200:
        print('success')
        return response.json() #Convert response body to a dictionary
    else:
        print('failed. Response code:', response.status_code)
        return

def get_pokemon_image_url(name):

    pokemon_dict = get_poki_info(name)
    if pokemon_dict:
        return pokemon_dict['sprites']['other']['official-artwork']['front_default']
    


def get_pokemon_list(limit=100, offset=0):
    url = 'https://pokeapi.co/api/v2/pokemon'

    params = {
        'limit' : limit,
        'offset' : offset
    }

    resp_msg = requests.get(url, params=params)

    if resp_msg.status_code == 200:
        dict = resp_msg.json()
        return[p['name'] for p in dict['results']]
    else:
        print('Failed to get Pokemon list.')
        print('Response code: ', resp_msg.status_code)
        print(resp_msg.text)