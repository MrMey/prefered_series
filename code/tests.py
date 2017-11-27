# Authors: Elodie Ikkache, Romain Meynard, Jessica Cohen
#
# version 1.0
# -*- coding: utf-8 -*-

import test_request_api as trapi
import test_request_database as trdb

# testing the API requests with Travis
test_api = trapi.MyTestCase()
test_api.test_request_api()


# test_db = trdb.MyTestCase()
# test_db.test_request_database()