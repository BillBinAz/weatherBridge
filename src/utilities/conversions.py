import logging
import datetime as dt
import sys
from math import isnan, log


def c_to_f(c_temp):
    """Convert Celsius to Fahrenheit, rounded to one decimal place."""
    return round(c_to_f_raw(c_temp), 1)


def c_to_f_raw(c_temp):
    """Convert Celsius to Fahrenheit without rounding."""
    return 9.0 / 5.0 * float(c_temp) + 32


def f_to_c(f_temp):
    """Convert Fahrenheit to Celsius, rounded to one decimal place."""
    return round(f_to_c_raw(f_temp), 1)


def f_to_c_raw(f_temp):
    """Convert Fahrenheit to Celsius without rounding."""
    return float(f_temp - 32) * 5.0 / 9.0


def calculate_dew_point(temperature, humidity):
    """Calculate the Fahrenheit dew point from Fahrenheit temperature and relative humidity."""
    humidity = float(humidity)
    if humidity <= 0:
        return 0.0

    temperature_celsius = f_to_c_raw(float(temperature))
    gamma = (17.27 * temperature_celsius) / (237.7 + temperature_celsius) + log(humidity / 100)
    dew_point_celsius = (237.7 * gamma) / (17.27 - gamma)
    return c_to_f(dew_point_celsius)


def format_f(value, places=2):
    """Format a value to specified decimal places.
    
    Args:
        value: The value to format
        places: Number of decimal places (default: 2)
        
    Returns:
        Formatted float value, or 0 if formatting fails
    """
    formatted_value = 0
    try:
        formatted_value = round(float(value), places)
    except (ValueError, TypeError) as e:
        logging.error("Unable to get station:get_weather " + str(e))
        print(dt.datetime.now().time(), "Unable to get station:get_weather " + str(e))
    return formatted_value


def get_average(data, key):
    """Calculate average value from a list of dictionaries.
    
    Args:
        data: List of dictionaries containing sensor data
        key: Dictionary key to average
        
    Returns:
        Average value rounded to 1 decimal place, or 0 if list is empty
    """
    how_many = 0
    sum_temp = 0.0
    for sensor in data:
        how_many += 1
        sum_temp += sensor[key]
    if how_many == 0:
        return 0
    return round(float(sum_temp / how_many), 1)


def convert_str_to_float(value):
    """Convert string to float.
    
    Args:
        value: String value to convert
        
    Returns:
        Converted float value, or 0.0 if conversion fails
    """
    try:
        return float(value)
    except (ValueError, TypeError):
        return 0.0


def get_average_from_list(data_list):
    """Calculate average from list of string values, skipping invalid entries.
    
    Args:
        data_list: List of string values to average
        
    Returns:
        Average value rounded to 1 decimal place, or 0 if no valid values
    """
    how_many = 0
    sum_temp = 0.0
    for sensor in data_list:
        value = convert_str_to_float(sensor)
        if (value == 0.0) or (isnan(value)):
            continue
        how_many += 1
        sum_temp += value
    if how_many == 0:
        return 0
    return round(float(sum_temp / how_many), 1)


def mps_to_mph(mps):
    """Convert meters per second to miles per hour.
    
    Args:
        mps: Speed in meters per second
        
    Returns:
        Speed in miles per hour (rounded to 1 decimal place)
    """
    return round(2.2369 * float(mps), 1)


def mm_to_inches(mm):
    """Convert millimeters to inches.
    
    Args:
        mm: Length in millimeters
        
    Returns:
        Length in inches (rounded to 2 decimal places)
    """
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
