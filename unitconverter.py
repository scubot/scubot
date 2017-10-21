from collections import namedtuple

Unit = namedtuple("Unit", "name prefix conversionValue")

Units = [Unit("feet", "ft", 0.3048), Unit("meters", "m", 3.28084), Unit("pounds", "lbs", 0.453592),
         Unit("kilograms", "kg", 2.20462), Unit("fathoms", "fsw", 1.8288)]

UnitPairs = {'feet': 'meters',
             'meters': 'feet',
             'pounds': 'kilograms',
             'kilograms': 'pounds',
             'fathoms': 'meters'}
