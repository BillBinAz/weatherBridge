import logging
import datetime
import sys


def c_to_f(c_temp):
    #
    # Convert from Celsius to Fahrenheit
    return round(9.0 / 5.0 * float(c_temp) + 32, 1)


def f_to_c(f_temp):
    #
    # Convert from Fahrenheit to Celsius
    return round(float(f_temp - 32) * 5.0 / 9.0, 1)


def format_f(value, source):
    #
    # add decimal place
    formatted_value = 0
    try:
        formatted_value = round(float(value), 2)
    except:
        e = sys.exc_info()[0]
        logging.error("Unable to get station:get_weather " + str(e))
        print(datetime.datetime.now().time(), "Unable to get station:get_weather " + str(e))
    return formatted_value


def get_average(data, key):
    how_many = 0
    sum_temp = 0.0
    for sensor in data:
        how_many += 1
        sum_temp += sensor[key]
    if how_many == 0:
        return 0
    return round(float(sum_temp / how_many), 1)


def mps_to_mph(mps):
    #
    # Convert from meters per second to miles per hour
    return round(2.2369 * float(mps), 1)


def mm_to_inches(mm):
    #
    # convert from mm to inches
    return round(float(mm) * 0.0393700787, 2)


def deg_to_compass(direction):
    #
    # degrees to compass direction
    compass = ""
    degrees = float(direction)

    if (degrees >= 0) and (degrees < 11.25):
        compass = " N "
    elif (degrees >= 11.25) and (degrees < 33.75):
        compass = "NNE"
    elif (degrees >= 33.75) and (degrees < 56.25):
        compass = " NE"
    elif (degrees >= 56.25) and (degrees < 78.75):
        compass = "ENE"
    elif (degrees >= 78.75) and (degrees < 101.25):
        compass = " E "
    elif (degrees >= 101.25) and (degrees < 123.75):
        compass = "ESE"
    elif (degrees >= 123.75) and (degrees < 146.25):
        compass = " SE"
    elif (degrees >= 146.25) and (degrees < 168.75):
        compass = "SSE"
    elif (degrees >= 168.75) and (degrees < 191.25):
        compass = " S "
    elif (degrees >= 191.25) and (degrees < 213.75):
        compass = "SSW"
    elif (degrees >= 213.75) and (degrees < 236.25):
        compass = " SW"
    elif (degrees >= 236.25) and (degrees < 258.75):
        compass = "WSW"
    elif (degrees >= 258.75) and (degrees < 281.25):
        compass = " W "
    elif (degrees >= 281.25) and (degrees < 303.75):
        compass = "WNW"
    elif (degrees >= 303.75) and (degrees < 326.25):
        compass = " NW"
    elif (degrees >= 326.25) and (degrees < 348.75):
        compass = "NNW"
    elif degrees >= 348.75:
        compass = " N "

    return compass
