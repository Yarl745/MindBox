import shelve

from mindbox.not_none import EmptyObject


class DbWorker:
    def __init__(self, table_name: str) -> None:
        self.table_name = "db/{}".format(table_name)
        self.db = None


    def open_db(self):
        self.db = shelve.open(self.table_name)


    def close_db(self):
        self.db.close()


    def create_new_element(self, element_name: str, data_for_element):
        if element_name not in self.db:
            self.db[element_name] = data_for_element


    def add_data_to_element(self, element_name: str, data: dict):
        element = self.db[element_name]
        element.update(data)
        self.db[element_name] = element


    def add_data_to_unit_of_element(self, element_name: str, unit_name: str, unit_data):
        element = self.db[element_name]
        element[unit_name].update(unit_data)
        self.db[element_name] = element


    # def add_unit_of_data_to_element(self, element_name: str, data_of_unit: dict):
    #     dict_element = self.db[element_name]
    #     dict_element.update(data_of_unit)
    #     self.db[element_name] = dict_element


    # def add_unit_of_data_to_element(self, element_name: str, unit_name: str):
    #     element_data = self.db[element_name]
    #     del element_data[unit_name]
    #     self.db[element_name] = element_data


    def replace_data_for_element(self, element_name: str, element_data):
        self.db[element_name] = element_data


    def replace_data_for_unit_of_element(self, element_name: str, unit_name, unit_data):
        element = self.db[element_name]
        element[unit_name] = unit_data
        self.db[element_name] = element


    def has_element(self, element_name: str) -> bool:
        return element_name in self.db


    def get_data_of_element(self, element_name: str):
        if self.has_element(element_name):
            return self.db[element_name]


    def get_data_of_unit_of_element(self, element_name: str, unit_name: str):
        if self.has_element(element_name):
            return self.db[element_name][unit_name]


    def get_all_db_elements(self) -> list:
        # Convert to list, because db can return only
        # KeysView(<shelve.DbfilenameShelf object at 0x0000020F19F59388>),
        # But not dict object
        return list(self.db.keys())


    def del_unit_of_element(self, element_name: str, unit_name: str):
        element = self.db[element_name]
        del element[unit_name]

        if len(element) > 0:
            self.db[element_name] = element
        else:
            self.del_element(element_name)



    def del_element(self, element_name: str):
        del self.db[element_name]
