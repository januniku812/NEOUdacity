"""Write a stream of close approaches to CSV or to JSON.

This module exports two functions: `write_to_csv` and `write_to_json`, each of
which accept an `results` stream of close approaches and a path to which to
write the data.

These functions are invoked by the main module with the output of the `limit`
function and the filename supplied by the user at the command line. The file's
extension determines which of these functions is used.

You'll edit this file in Part 4.
"""
import csv
import json

dt_utc = 'datetime_utc'
dis_au = 'distance_au'
vel_km = 'velocity_km_s'
des = 'designation'
name = 'name'
dia_km = 'diameter_km'
haz = 'potentially_hazardous'
fieldnames = (dt_utc, dis_au, vel_km, des, name, dia_km, haz)


def write_to_csv(results, filename):
    """Write an iterable of `CloseApproach` objects to a CSV file.

    The precise output specification is in `README.md`.Roughly, each output row
    corresponds to the information in a single close approach from the
    `results` stream and its associated near-Earth object.

    :param results: An iterable of `CloseApproach` objects.
    :param filename:Path-like object pointing to where the data should be saved
    """
    with open(filename, "w") as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        dict = iter(results)
        print(results)
        # while True loop encasing try and except
        # so break can be used without syntax error
        while True:
            try:
                next_dict = next(dict)
                t = next_dict.time
                d = next_dict.distance
                v = next_dict.velocity
                de = next_dict.designation
                n = next_dict.neo.name
                dia = next_dict.neo.diameter
                h = next_dict.neo.hazardous
                # renaming the global var to shorten and meet pep8 style
                du = dt_utc
                da = dis_au
                vk = vel_km
                dk = dia_km
                row = {du: t, da: d, vk: v, des: de, name: n, dk: dia, haz: h}
                writer.writerow(row)

            except StopIteration:
                break


def write_to_json(results, filename):
    """Write an iterable of `CloseApproach` objects to a JSON file.

    The precise output specification is in `README.md`. Roughly, the output is
    a list containing dictionaries, each mapping `CloseApproach` attributes to
    their values and the 'neo' key mapping to a dictionary of the associated
    NEO's attributes.

    :param results: An iterable of `CloseApproach` objects.
    :param filename:path-like object pointing to where the data should be saved
    """
    json_to_dump = list()
    with open(filename, "w") as json_outfile:
        json_dict = iter(results)
        # while True loop encasing try and except
        # so break can be used without syntax error
        while True:
            try:
                next_json_dict = next(json_dict)
                # creating var to shorten keys & values for the dict to append
                # so it can meet pep8 style
                ts = next_json_dict.time_str
                d_au = next_json_dict.distance
                vel = next_json_dict.velocity
                desi = next_json_dict.designation
                na = next_json_dict.neo.name
                dia = next_json_dict.neo.diameter
                neo_haz = next_json_dict.neo.hazardous
                neo = {name: na, dia_km: dia, haz: neo_haz, des: desi}
                n = "neo"
                di = {dt_utc: ts, dis_au: d_au, vel_km: vel, des: desi, n: neo}
                json_to_dump.append(di)
            except StopIteration:
                
                break
    json.dump(json_to_dump, json_outfile, indent=5)
