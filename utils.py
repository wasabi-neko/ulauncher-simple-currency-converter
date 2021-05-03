import requests
import re

class syntaxError(Exception):
    pass

class typeNotFoundError(Exception):
    pass

class CurrencyConv:
    """A class contain currency conversion method
    Attributes
    ----------------------------------------------------------------
    exrate_table : dict
        exchange rate table
    default_type : str
        the default target type of currency
    """

    def __init__(self):
        self.exrate_table = dict()
        self.default_target = 'TWD'
        self.request_exrate_table()


    def request_exrate_table(self):
        r = requests.get('https://tw.rter.info/capi.php')
        self.exrate_table = r.json()
    

    def update_default_type(self):
        pass # TODO:


    def has_type(self, type_name):
        return 'USD' + type_name in self.exrate_table


    def get_exrate(self, cu_type):
        """get exchange rate (from USD to cu_type) from self.exrate_table

        Args:
            cu_type (str): the source currency type
        Returns: dict, error
        """
        if cu_type == 'USD':
            return 1
        if not ('USD' + cu_type) in self.exrate_table:
            raise typeNotFoundError(cu_type)
        return self.exrate_table['USD' + cu_type]['Exrate']


    def convert(self, src_type, dst_type, value):
        rate_usd_src = self.get_exrate(src_type)
        rate_usd_dst = self.get_exrate(dst_type)
        return (value / rate_usd_src) * rate_usd_dst
    
    
    def parse(self, input_string):
        m_1 = re.match(r'(-?\d+)\s*([a-zA-Z]+) +to +([a-zA-Z]+)', input_string)
        m_2 = re.match(r'(-?\d+)\s*([a-zA-Z]+) +([a-zA-Z]+)', input_string)
        m_3 = re.match(r'(-?\d+)\s*([a-zA-Z]+)', input_string)

        if m_1 != None:
            m = m_1
        elif m_2 != None:
            m = m_2
        elif m_3 != None:
            m = m_3
        else:
            m = None
        
        if m == None:
            raise syntaxError

        value = int(m.group(1))
        src_type = m.group(2).upper()
        if m.lastindex >= 3:
            dst_type = m.group(3).upper()
        else:
            dst_type = self.default_target

        return value, src_type, dst_type

