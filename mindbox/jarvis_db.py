from mindbox.db_worker import DbWorker
from mindbox.string_operation import join_string, get_list_of_words_from_string
from mindbox.transformer import transform_list_to_truedict

DB_RECORDS = 'DB_RECORDS'
DB_KEYWORDS = 'DB_KEYWORDS'

IS_FILE = 'IS_FILE'
PARENT_OF_RECORD = 'PARENT_OF_RECORD'
KEYWORDS = 'KEYWORDS'
RECORD = 'RECORD'
CHILDREN = 'CHILDREN'


def first_db_create() -> bool:
    db_w = DbWorker(DB_RECORDS)
    db_w.open_db()

    data_for_record = {
            CHILDREN: dict()
        }
    db_w.create_new_element('ROOT', data_for_record)

    db_w.close_db()

    # If DB creating is success
    return True



def is_record_exist(record_name: str) -> bool:
    db_records_worker = DbWorker(DB_RECORDS)
    db_records_worker.open_db()

    is_exist = db_records_worker.has_element(record_name)

    db_records_worker.close_db()

    return is_exist


def record_is_file(record_name: str) -> bool:
    db_records_worker = DbWorker(DB_RECORDS)
    db_records_worker.open_db()

    is_file = db_records_worker.get_data_of_element(record_name)[IS_FILE]

    db_records_worker.close_db()

    return is_file


def get_children(parent_record_name: str) -> list:
    db_records_worker = DbWorker(DB_RECORDS)
    db_records_worker.open_db()

    children_names = list(db_records_worker.get_data_of_element(parent_record_name)[CHILDREN])

    db_records_worker.close_db()

    return children_names


def get_parent(child_record_name: str) -> str:
    db_records_worker = DbWorker(DB_RECORDS)
    db_records_worker.open_db()

    parent_name = db_records_worker.get_data_of_element(child_record_name)[PARENT_OF_RECORD]

    db_records_worker.close_db()

    return parent_name


def get_exist_keywords(keywords: list) -> list:
    db_keywords_worker = DbWorker(DB_KEYWORDS)
    db_keywords_worker.open_db()

    # delete same keywords
    unique_keywords = set(keywords)

    exist_keywords = []

    for keyword in unique_keywords:
        if db_keywords_worker.has_element(keyword):
            exist_keywords.append(keyword)

    db_keywords_worker.close_db()

    return exist_keywords


def find_records_by_keywords(keywords: list) -> list:
    db_keywords_worker = DbWorker(DB_KEYWORDS)
    db_keywords_worker.open_db()

    found_records = []

    first_keyword = keywords[0]
    records = db_keywords_worker.get_data_of_element(first_keyword).keys()

    # If record exist in all keywords -> add current record to found records
    for record in records:
        for index in range(1, len(keywords)):
                current_keyword = keywords[index]

                if db_keywords_worker.get_data_of_element(current_keyword).get(record, False):
                    continue
                else:
                    break

        else:
            found_records.append(record)

    db_keywords_worker.close_db()

    return found_records


def create_empty_record(record_name: str):
    db_records_worker = DbWorker(DB_RECORDS)
    db_records_worker.open_db()

    db_records_worker.create_new_element(record_name, None)

    db_records_worker.close_db()


def create_record(record_name: str, record_keywords: list, is_file: bool, parent_of_record: str) -> bool:
    db_records_worker = DbWorker(DB_RECORDS)
    db_records_worker.open_db()

    db_keywords_worker = DbWorker(DB_KEYWORDS)
    db_keywords_worker.open_db()

    data_for_record = {
        IS_FILE: is_file,
        PARENT_OF_RECORD: parent_of_record,
        KEYWORDS: transform_list_to_truedict(record_keywords)
    }

    # If record is directory -> add children to record
    if not is_file:
        data_for_record.setdefault(CHILDREN, dict())

    db_records_worker.create_new_element(record_name, data_for_record)

    for record_keyword in record_keywords:
        data_for_keyword = {
            record_name: True
        }
        if db_keywords_worker.has_element(record_keyword):
            db_keywords_worker.add_data_to_element(record_keyword, data_for_keyword)
        else:
            db_keywords_worker.create_new_element(record_keyword, data_for_keyword)

    data_for_parent = {
        record_name: True
    }
    db_records_worker.add_data_to_unit_of_element(parent_of_record, CHILDREN, data_for_parent)

    db_records_worker.close_db()
    db_keywords_worker.close_db()

    # If creating record is success
    return True


def get_record_keywords(record_name: str) -> dict:
    db_records_worker = DbWorker(DB_RECORDS)
    db_records_worker.open_db()

    record_keywords = db_records_worker.get_data_of_element(record_name)[KEYWORDS]

    db_records_worker.close_db()

    return record_keywords


def get_all_record_names() -> list:
    db_records_worker = DbWorker(DB_RECORDS)
    db_records_worker.open_db()

    record_names = db_records_worker.get_all_db_elements()

    db_records_worker.close_db()

    return record_names


def copy_record_data(from_record: str, to_record: str) -> bool:
    db_records_worker = DbWorker(DB_RECORDS)
    db_records_worker.open_db()

    data = db_records_worker.get_data_of_element(from_record)
    db_records_worker.create_new_element(to_record, data)

    db_records_worker.close_db()

    return True


def add_record_to_keywords(record_name: str, to_keywords: dict) -> bool:
    db_keywords_worker = DbWorker(DB_KEYWORDS)
    db_keywords_worker.open_db()

    for to_keyword in to_keywords.keys():
        data_for_keyword = {
            record_name: True
        }
        if db_keywords_worker.has_element(to_keyword):
            db_keywords_worker.add_data_to_element(to_keyword, data_for_keyword)
        else:
            db_keywords_worker.create_new_element(to_keyword, data_for_keyword)

    db_keywords_worker.close_db()

    return True


def del_record(record_name: str) -> bool:
    db_records_worker = DbWorker(DB_RECORDS)
    db_records_worker.open_db()

    db_records_worker.del_element(record_name)

    db_records_worker.close_db()

    return True


def del_records(record_names: list) -> bool:
    db_records_worker = DbWorker(DB_RECORDS)
    db_records_worker.open_db()

    for record_name in record_names:
        db_records_worker.del_element(record_name)

    db_records_worker.close_db()

    return True


def del_record_with_keywords(record_name: str) -> bool:
    db_records_worker = DbWorker(DB_RECORDS)
    db_records_worker.open_db()

    keywords = get_record_keywords(record_name)
    del_record_from_keywords(record_name, keywords)

    db_records_worker.del_element(record_name)

    db_records_worker.close_db()

    return True


def big_delete(record_name: str):
    if not record_is_file(record_name):
        children_names = get_children(parent_record_name=record_name)
        for children_name in children_names:
            big_delete(children_name)

    # Del after use get_children()...
    del_record_with_keywords(record_name)


def del_record_from_parent(children_name: str) -> bool:
    db_records_worker = DbWorker(DB_RECORDS)
    db_records_worker.open_db()

    parent_name = get_parent(children_name)
    parent_children = db_records_worker.get_data_of_unit_of_element(parent_name, CHILDREN)

    # Del children from parent children dict.
    parent_children.pop(children_name)

    # Change children in parent record.
    db_records_worker.replace_data_for_unit_of_element(parent_name, CHILDREN, parent_children)

    db_records_worker.close_db()

    return True


def del_records_from_parent(children_names: list) -> bool:
    db_records_worker = DbWorker(DB_RECORDS)
    db_records_worker.open_db()

    parent_name = get_parent(children_names[0])
    parent_children = db_records_worker.get_data_of_unit_of_element(parent_name, CHILDREN)

    # Del current children from parent children dict.
    for children_name in children_names:
        parent_children.pop(children_name)

    # Change children in parent record.
    db_records_worker.replace_data_for_unit_of_element(parent_name, CHILDREN, parent_children)

    db_records_worker.close_db()

    return True


def del_record_from_keywords(record_name: str, from_keywords: dict) -> bool:
    db_keywords_worker = DbWorker(DB_KEYWORDS)
    db_keywords_worker.open_db()

    for from_keyword in from_keywords:
        db_keywords_worker.del_unit_of_element(from_keyword, record_name)

    db_keywords_worker.close_db()

    return True


def change_record_keywords(record_name: str, new_record_keywords: dict) -> bool:
    db_records_worker = DbWorker(DB_RECORDS)
    db_records_worker.open_db()

    db_records_worker.replace_data_for_unit_of_element(record_name, KEYWORDS, new_record_keywords)

    db_records_worker.close_db()

    return True
