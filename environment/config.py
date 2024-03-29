# -*- coding: utf-8 -*-
import os
import logging


class ProductionConfig(object):
    def configure(self):
        logging.getLogger('sqlalchemy.engine').setLevel(logging.ERROR)
        os.environ['SALT'] = '\xda9\xa3\xee^kK\r2U\xbf\xef\x95`\x18\x90\xaf\xd8\x07\t'
        os.environ['SECRET_KEY'] = 'Q\xee[z\xd5\x17y\xec\x92*\xb7l~us\xec\xb7\xd7BM\x90\xa9%\xeb'

        os.environ['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:KGG4m5MGIAl24pnn@/miocardiopediatra?unix_socket=/cloudsql/miocardio-pediatra:us-east1:miocardio-sql'
        os.environ['RESPONSE_STRUCT'] = '{"data": [], "errors": []}'


class DevelopmentConfig(object):
    def configure(self):
        logging.getLogger('sqlalchemy.engine').setLevel(logging.DEBUG)
        os.environ['SALT'] = '\xda9\xa3\xee^kK\r2U\xbf\xef\x95`\x18\x90\xaf\xd8\x07\t'
        os.environ['SECRET_KEY'] = 'Q\xee[z\xd5\x17y\xec\x92*\xb7l~us\xec\xb7\xd7BM\x90\xa9%\xeb'

        os.environ['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:KGG4m5MGIAl24pnn@/miocardiopediatra?unix_socket=/cloudsql/miocardio-pediatra:us-east1:miocardio-sql'
        os.environ['RESPONSE_STRUCT'] = '{"data": [], "errors": []}'


class DefaultConfig(object):

    def configure(self):
        logging.getLogger('sqlalchemy.engine').setLevel(logging.DEBUG)
        os.environ['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:KGG4m5MGIAl24pnn@35.229.102.116/miocardiopediatra'
        os.environ['RESPONSE_STRUCT'] = '{"data": [], "errors": []}'
        os.environ['SALT'] = '\xda9\xa3\xee^kK\r2U\xbf\xef\x95`\x18\x90\xaf\xd8\x07\t'
        os.environ['SECRET_KEY'] = 'Q\xee[z\xd5\x17y\xec\x92*\xb7l~us\xec\xb7\xd7BM\x90\xa9%\xeb'


class Config(object):
    logging.basicConfig()
    if 'ENVIRONMENT' in os.environ:
        if os.environ['ENVIRONMENT'] == 'dev' or os.environ['ENVIRONMENT'] == 'qa':
            DevelopmentConfig().configure()
        elif os.environ['ENVIRONMENT'] == 'prod':
            ProductionConfig().configure()
        else:
            DefaultConfig().configure()
    else:
        DefaultConfig().configure()
