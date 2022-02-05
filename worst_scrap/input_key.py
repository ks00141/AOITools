def input_key(elem, key, time, keys, option='ENTER', delay=5):
    elem.send_keys(key)
    if option == 'ENTER':
        time.sleep(delay)
        elem.send_keys(keys.ENTER)
