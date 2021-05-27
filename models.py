"""Represent models for near-Earth objects and their close approaches.

The `NearEarthObject` class represents a near-Earth object. Each has a unique
primary designation, an optional unique name, an optional diameter, and a flag
for whether the object is potentially hazardous.

The `CloseApproach` class represents a close approach to Earth by an NEO. Each
has an approach datetime, a nominal approach distance, and a relative approach
velocity.

A `NearEarthObject` maintains a collection of its close approaches, and a
`CloseApproach` maintains a reference to its NEO.

The functions that construct these objects use information extracted from the
data files from NASA, so these objects should be able to handle all of the
quirks of the data set, such as missing names and unknown diameters.

You'll edit this file in Task 1.
"""
from helpers import cd_to_datetime, datetime_to_str


class NearEarthObject:
    """A near-Earth object (NEO).

    An NEO encapsulates semantic and physical parameters about the object, such
    as its primary designation (required, unique), IAU name (optional),
    diameter in km (optional - sometimes unknown), and whether it's marked as
    potentially hazardous to Earth.

    A `NearEarthObject` also maintains a collection of its close approaches -
    initialized to an empty collection, but eventually populated in the
    `NEODatabase` constructor.
    """

    def __init__(self, **info):
        """Init method to get elements from provided info/data."""
        # Create an empty initial collection of linked approaches.
        self.approaches = []
        try:
            self.designation = str(info.get("designation"))
        except Exception:
            self.designation = ''
        try:
            self.name = info.get("name")
        except Exception:
            self.name = None
        try:
            diameter = info.get("diameter")
            self.diameter = float(diameter)
        except Exception:
            self.diameter = float("nan")
        try:
            self.hazardous = info.get("hazardous")
        except Exception:
            self.hazardous = False

    @property
    def fullname(self):
        """Return the full name of the neo with designation and name."""
        if self.name:
            return f'{self.designation} ({self.name})'
        else:
            return f'{self.designation}'

    def __str__(self):
        """Return str that states fullname, diameter, and if it's hazardous."""
        isHazardous = ""
        if self.hazardous:
            isHazardous = "is potentially hazardous"
        else:
            isHazardous = "is not potentially hazardous"

        fn = self.fullname
        dia = self.diameter
        return f"NEO {fn} has a diameter of {dia} km and {isHazardous}."

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation."""
        desig = self.designation
        name = self.name
        return (f"NearEarthObject(designation={desig!r}, name={name!r}, "
                f"diameter={self.diameter:.3f}, hazardous={self.hazardous!r})")


class CloseApproach:
    """A close approach to Earth by an NEO.

    A `CloseApproach` encapsulates information about the NEO's close approach
    to Earth, such as the date and time (in UTC) of closest approach,
    the nominal approach distance in astronomical units, and the relative
    approach velocity in kilometers per second.

    A `CloseApproach` also maintains a reference to its `NearEarthObject` -
    initally, this information (the NEO's primary designation) is saved in a
    private attribute, but the referenced NEO is eventually replaced in the
    `NEODatabase` constructor.
    """

    def __init__(self, **data):
        """Init method to get elements from data provided."""
        try:
            self.designation = str(data.get("pdes"))
        except Exception:
            self.designation = ''
        try:
            self.time = cd_to_datetime(data.get("time"))
        except Exception:
            self.time = None
        try:
            self.distance = float(data.get("distance"))
        except Exception:
            self.distance = 0.0
        try:
            self.velocity = float(data.get("velocity"))
        except Exception:
            self.velocity = 0.0
        try:
            self.neo = data.get("neos")
        except Exception:
            self.neo = None

    @property
    def time_str(self):
        """Return a formatted representation of this object's approach time.

        The value in `self.time` should be a Python `datetime` object. While a
        `datetime` object has a string representation,
        the default representation includes seconds - significant
        figures that don't exist in our input data set.

        The `datetime_to_str` method converts a `datetime` object to a
        formatted string that can be used in human-readable representations and
        in serialization to CSV and JSON files.
        """
        return datetime_to_str(self.time)

    def __str__(self):
        """Return `str(self)` with info about the close approach object."""
        ts = self.time_str
        fn = self.neo.fullname
        dis = self.distance
        vel = self.velocity
        str_part_one = f"At {ts}, {fn} approaches Earth at a distance of {dis}"
        return f"{str_part_one} au and a velocity of {vel} km/s."

    def __repr__(self):
        """Return `repr(self)`, a string representation of this object."""
        time = self.time_str
        return (f"CloseApproach(time={time!r}, distance={self.distance:.2f}, "
                f"velocity={self.velocity:.2f}, neo={self.neo!r})")
