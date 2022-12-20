import requests
import Constants, web, pickle, sys
import logging
LOGGER = logging.getLogger('Login')

#Login function
def login(session: requests.Session, username, password):
    logged_in = False
    retry = 0
    cookies = None

    try:
        file = pickle.load(open("cookies.p", "rb"))
        try:
            with open('cookies.p', 'rb') as file:
                session.cookies.update(pickle.load(file))
        except Exception as e:
            LOGGER.error(sys.exc_info())


        #Navigate to login page to try/get initial cookies **if you don't do this step it requires an extra post field that I haven't found
        while(retry < 5):
            response = web.get(session, Constants.NEO_LOGIN)
            if web.check_for_announcement(response):
                retry += 1
            else:
                break
        
        if response:
            logged_in = verify_login(username, response)

        if logged_in:
            LOGGER.info("Logged in with cookies")

    except (OSError, IOError) as e:
        file = 3
        pickle.dump(file, open("cookies.p", "wb"))
    except Exception as e:
        LOGGER.error(e)

    #If saved cookies don't work then log in again
    retry = 0
    if not logged_in:
        destination = "" #value for a key:value pair required for POST request login

        #Data for POST request to login
        postFields = {"destination": destination, "username": username, "password": password, }

        #Send POST to login
        while(retry < 5):
            response = web.post(session, Constants.NEO_LOGIN_REQUEST, postFields, Constants.NEO_LOGIN)
            if web.check_for_announcement(response):
                retry += 1
                LOGGER.info(retry)
            else:
                break
        
        # LOGGER.info(response)
        logged_in = verify_login(username, response)

    if not logged_in:
        LOGGER.info("Login Failed")
    else:
        LOGGER.info("Login Successful")

    return logged_in

def verify_login(username, source):
    logged_in = False

    if "/userlookup.phtml?user=" + username in source:
        logged_in = True
    else:
        logged_in = False

    return logged_in

def save_cookies(session):
    with open('cookies.p', 'wb') as f:
        pickle.dump(session.cookies, f)
