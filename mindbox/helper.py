from mindbox.db_worker import DbWorker
from mindbox.transformer import transform_list_to_truedict


def print_and_return(object):
    print(object)
    print(object.minimum_height)
    return object.minimum_height




# data_for_record = {
# 		'CHILDREN': dict()
# 	}
# db_w.create_new_element('ROOT', data_for_record)






db_w = DbWorker("DB_RECORDS")
db_w.open_db()

record_names = db_w.get_all_db_elements()


for record_name in record_names:
    data = db_w.get_data_of_element(record_name)
    print(f'record_name={record_name}  data={data}')

db_w.close_db()







# db_w = DbWorker("DB_RECORDS")
# db_w.open_db()
#
# keywords = db_w.get_all_db_elements()
#
# for keyword in keywords:
#     data = db_w.get_data_of_element(keyword)
#     print(f'key={keyword}  data={data}')
#
# db_w.close_db()

# print(record_names)



