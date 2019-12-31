def teardown(*args):
    for arg in args:
        arg.close()
    return True
