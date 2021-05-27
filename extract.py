"""Extract data on near-Earth and close approach objects from CSV & JSON files.

The `load_neos` function extracts NEO data from a CSV file, formatted as
described in the project instructions, into a collection of `NearEarthObject`s.

The `load_approaches` function extracts close approach data from a JSON file,
formatted as described in the project instructions, into a collection of
`CloseApproach` objects.

The main module calls these functions with the arguments provided at the
command line, and uses the resulting collections to build an `NEODatabase`.

You'll edit this file in Task 2.
"""
import csv
import json

from models import NearEarthObject, CloseApproach

pdes_dict = dict()


def load_neos(neo_csv_path):
    """Read near-Earth object information from a CSV file.

    :param neo_csv_path: path to aCSV file that has data about NEO objects.
    :return: A collection of `NearEarthObject`s.
    """
    with open(neo_csv_path, 'r') as infile:
        neos = list()
        reader = csv.DictReader(infile)
        for elem in reader:
            # extracting data from an the elements the reader can read
            name = dict(elem).get('name')
            if not name:
                name = None
            pdes = dict(elem).get('pdes')
            if not pdes:
                pdes = "nan"
            dia = dict(elem).get("diameter")
            if not dia:
                dia = float("nan")
            else:
                dia = float(dict(elem).get("diameter"))
            ishaz = dict(elem).get('pha')
            if(ishaz == "Y"):
                ishaz = True
            else:
                ishaz = False
            modelsNEO = create_neo(pdes, name, dia, ishaz)
            print(f"{modelsNEO.name} {modelsNEO.designation} {modelsNEO.diameter} {modelsNEO.hazardous}")
            neos.append(modelsNEO)
            # updatig pdes dict
            pdes_dict[pdes] = modelsNEO
    return neos


def load_approaches(cad_json_path):
    """Read close approach data from a JSON file.

    :param neo_csv_path: A path to a JSON file that has data on CA objects.
    :return: A collection of `CloseApproach`es.
    """
    ca_list = list()
    with open(cad_json_path) as file:
        json_data = json.load(file)
        for key in json_data['data']:
            desig = key[0]
            time = key[3]
            dist = key[4]
            velocity = key[7]
            neo = pdes_dict.get(desig)
            modelsCA = create_ca(desig, time, dist, velocity, neo)
            ca_list.append(modelsCA)
    return ca_list


def create_neo(a, b, c, d):
    """Create a near earth object with the given input."""
    return NearEarthObject(designation=a, name=b, diameter=c, hazardous=d)


def create_ca(a, b, c, d, e):
    """Create a close approach object with the given input."""
    return CloseApproach(pdes=a, time=b, distance=c, velocity=d, neos=e)
