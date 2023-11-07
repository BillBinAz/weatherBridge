import logging
from datetime import datetime
from ring_doorbell import Ring, Auth
from Utilities.connect import get_credentials

CONNECT_ITEM_ID = "4entjtskzvjq7ttudeglscrdra"

#  https://github.com/tchellomello/python-ring-doorbell


def get_ring():

    try:
        #
        # Get security data
        credentials = get_credentials(CONNECT_ITEM_ID)
        user_name = credentials[1].value
        password = credentials[0].value
        otp = credentials[3].totp

        auth = Auth("WeatherBridge/Utilities")
        auth.fetch_token(user_name, password, otp)

        ring = Ring(auth)
        ring.update_data()

        return ring
    except Exception as e:
        logging.error("Unable to get credentials " + str(e))
        print(datetime.datetime.now().time(), "Unable to get credentials " + str(e))
    return


def enable_motion():
    try:
        ring = get_ring()

        devices = ring.devices()

        device = ring.get_device_by_name('Backyard Patio')
        device.motion_detection = True
        device.update()

        # All doorbells
        doorbells = devices['doorbots']

        # All chimes
        chimes = devices['chimes']

        # All stickup cams
        stickup_cams = devices['stickup_cams']

        for cam in stickup_cams:
            cam.motion_detection

    except Exception as e:
        logging.error("enable_motion " + str(e))
        print(datetime.datetime.now().time(), "enable_motion " + str(e))
    return


def disable_motion():
    try:
        devices = get_ring()

        for d in devices:
            d.disable_motion_alerts()

    except Exception as e:
        logging.error("enable_motion " + str(e))
        print(datetime.datetime.now().time(), "enable_motion " + str(e))
    return

if __name__ == '__main__':
    enable_motion()

