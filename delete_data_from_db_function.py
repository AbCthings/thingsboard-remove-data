def deleteData(ip, port, user, password, deviceId, keys, startTs, endTs, deleteAll=False, rewrite=False):
    '''
    Current function performs an http delete method and removes the specified timeseries for a time period or all recorded data
    :param ip: ip address of target ThingsBoard
    :param port: port used by the target ThingsBoard
    :param user: username to obtain API authorization
    :param password: password to obtain API authorization
    :param deviceId: id of the device to read
    :param keys: key of the timeseries to read
    :param startTs: first unix timestamp to fetch
    :param endTs: last unix timestamp to fetch
    :param deleteAll: boolean to verify removing all data
    :param rewrite: boolean to verify rewriting removed data
    :return: http requests status
    '''
    # Define the headers of the authorization request
    headersToken = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }

    # Define the body of the authorization request
    data = '{"username":"' + user + '", "password":"' + password + '"}'

    # Perform the POST request to obtain X-Token Authorization
    try:
        response = requests.post('https://' + ip + ':' + port + '/api/auth/login', headers=headersToken, data=data)
        X_AUTH_TOKEN = response.json()['token']
    except Exception as e:
        print("\nAn exception occurred while trying to obtain the authorization from SOURCE Thigsboard: ", e)
        sys.exit(1)

    # Define the headers of the request
    headers = {'Accept': 'application/json', 'X-Authorization': 'Bearer ' + X_AUTH_TOKEN}

    if type(keys) != list:
        keys = [keys]
    # Perform the DELETE request to remove timeseries
    url = 'https://{}:{}/api/plugins/telemetry/DEVICE/{}/timeseries/delete?keys={}&deleteAllDataForKeys={}&startTs={}&endTs={}&rewriteLatestIfDeleted={}'.format(
        ip, port, deviceId, ','.join(keys), json.dumps(deleteAll), startTs, endTs, json.dumps(rewrite))
    try:
        r = requests.delete(url=url, headers=headers)
        print("Request to SOURCE ThingsBoard - response code: ", r.status_code)
    except Exception as e:
        print("\nAn exception occurred while trying to obtain and print the timeseries from SOURCE Thigsboard: ", e)
        logging.error('Timeseries request failed.')
        sys.exit(1)

    return r.status_code


# Delete mode
if MODE == "delete":
    logging.info('Operating mode: delete')

    logging.info('Started deleting data from thingsboard database')
    status = deleteData(TARGET_TB_ADDRESS, TARGET_TB_PORT, SOURCE_TB_USER,SOURCE_TB_PASSWORD,SOURCE_TB_DEVICE_ID,TIMESERIES_KEY,STARTTS,ENDTS)
    logging.info('Finished deleting data from database')
