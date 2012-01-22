from geopy import geocoders
import sys

__orig_raw_input__ = raw_input
def raw_input(prompt):
    text = __orig_raw_input__(prompt).decode(sys.stdin.encoding)
    return text.encode('utf-8')

def input_coordinates(prompt):
    position = raw_input(prompt)
    g = geocoders.Google()
    results = g.geocode(position, exactly_one=False)
    while len(results)!=1:
        if len(results)==0:
            print("No places found under this name, try again")
            position = raw_input(prompt)
            results = g.geocode(position, exactly_one=False)
        else:
            print("Multiple options found:")
            for (idx, item) in enumerate(results):
                print("%3u - %s" % (idx+1, item[0]))
            selection = raw_input("Choose one or type 'n' to enter a new place")
            if selection=="n":
                position = raw_input(prompt)
                results = g.geocode(position, exactly_one=False)
            else:
                # TODO: catch entry of 0 which results in -1
                if selection.isdigit() and int(selection)-1 < len(results):
                    results = [ results[int(selection)-1]]
                else:
                    print "Wrong selection, try again"
                    # Uuh, this is evil, the user can't choose again, he
                    # must renter his selection
                    position = raw_input(prompt)
                    results = g.geocode(position, exactly_one=False)
    return results[0][1]

from math import pi, cos, sin, acos, asin

def deg2rad(deg):
    return pi * deg / 180.0

def rad2deg(rad):
    return 180.0 * rad / pi

def gps2decimal(gps_tuple):
    degree = float(gps_tuple[0])
    degree += float(gps_tuple[1] / 60.0)
    degree += float(gps_tuple[2] / 3600.0)
    return degree

def spherical_beta(angle_alpha, side_b, side_c):
    #print("Angle alpha: %f" % rad2deg(angle_alpha))
    #print("Side b in degree: %f" % rad2deg(side_b))
    #print("Side c in degree: %f" % rad2deg(side_c))
    side_a = acos( cos(side_b)*cos(side_c) + sin(side_b)*sin(side_c)*cos(angle_alpha) )
    #print("Side a in degree: %f" % rad2deg(side_a))
    angle_beta = asin( ( sin(angle_alpha)*sin(side_b) ) / sin(side_a) )
    return angle_beta

def bearing(location, target):
    loc_N = location[0]
    loc_E = location[1]

    tgt_N = target[0]
    tgt_E = target[1]

    alpha = deg2rad( tgt_E - loc_E )
    b = deg2rad( 90 - tgt_N )
    c = deg2rad( 90 - loc_N )

    alpha = spherical_beta( alpha, b, c )
    return 180 - rad2deg(alpha)

location = input_coordinates("Your position: ")
target   = input_coordinates("Target for bearing: ")
print( "Bearing from your position to the target: %f" % bearing( location, target ) )
