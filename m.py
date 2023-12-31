from __future__ import annotations


class Record:
    def __init__(self, workflow_type: str = "") -> None:
        self.workflow_type: str = workflow_type
        self.data: dict[str, object] = {}
        self.id: int = -1
        self.id2: str = None
        self.linked_records: Records = Records()

    def find_record_by_workflow_type(self, workflow_type: str) -> Record:
        if self.workflow_type == workflow_type:
            return self
        if self.linked_records.rows_count == 0:
            return None
        linked_record: Record
        for linked_record in self.linked_records.rows:
            return linked_record.find_record_by_workflow_type(workflow_type)


    def assign_id(self, field_name) -> None:
        if self.has_field(field_name):
            value = self.data[field_name]
            if type(value) is int:
                self.id = value

    def assign_id2(self, field_name) -> None:
        if self.has_field(field_name):
            value = self.data[field_name]
            if type(value) is str:
                self.id2 = value

    def is_valid_value_type(self, value) -> bool:
        return (value == None or type(value) is str or type(value) is int or (value and all(isinstance(s, str) for s in value) == True))

    
    def add_or_set(self, **kwargs: dict[str,]) -> None:
        for key, value in kwargs.items():
            if self.is_valid_value_type(value):
                self.data[key] = value

        
    def remove(self, field_name: str) -> None:
        if field_name in self.field_names:
            del self.data[field_name]

    def has_field(self, field_name) -> bool:
        return field_name in self.field_names
    
    def any(self, field_name: str, value: object) -> bool:
        return self.has_field(field_name) and self.data[field_name] == value

    @property
    def fields_count(self) -> int:
        return len(self.data.keys())
    
    @property
    def field_names(self) -> set:
        return set(self.data.keys())

        
    def field(self, field_name: str) -> str:
        if field_name not in self.field_names:
            raise ValueError("Field not in dictionary!")
        val: object = self.data[field_name]
        if (val is None):
            return None
        if (type(val) is str):
            return val
        if (type(val) is int):
            return str(val)
        if (type(val) is list):
            return ";".join(val)

class Records:
    def __init__(self, rows: list[Record] = []) -> None:
        self.rows: list[Record] = rows

    @staticmethod
    def create_records(records_list: list[Record]) -> None:
        records: Records = Records()
        records.rows = records_list
        
    @property
    def ids(self) -> set[int]:
        ids: set[int] = set()
        row: Record
        for row in self.rows:
            ids.add(row.id)
        return ids
    
    @property
    def id2s(self) -> set[str]:
        id2s: set[str] = set()
        row: Record
        for row in self.rows:
            id2s.add(row.id2)
        return id2s

    @property
    def all_fields(self) -> set[str]:
        all_fields: set[str] = set()
        row: Record
        for row in self.rows:
            all_fields = all_fields.union(row.field_names)
        return all_fields
    
    @property
    def all_fields_count(self) -> int:
        return len(self.all_fields)
    
    @property
    def rows_count(self) -> int:
        return len(self.rows)
    
    def add(self, *args: Record) -> None:
        for item in args:
            self.rows.append(item)

    def assign_ids(self, field_name: str) -> None:
        row: Record
        for row in self.rows:
            row.assign_id(field_name)

    def assign_id2s(self, field_name: str) -> None:
        row: Record
        for row in self.rows:
            row.assign_id2(field_name)

    def find_record_by_id(self, id: int) -> Record:
        row: Record
        for row in self.rows:
            if row.id == id:
                return row
        return None
    
    def find_record_by_id2(self, id2: str) -> Record:
        row: Record
        for row in self.rows:
            if row.id2 == id2:
                return row
        return None

    def find_records_by_value(self, field_name: str, value: object) -> list[Record]:
        result: list[Record] = [row for row in self.rows if (row.has_field(field_name) and row.data[field_name] == value)]
        return result

    def find_record_by_value(self, field_name: str, value: object) -> Record | None:
        result: list[Record] = self.find_records_by_value(field_name, value)
        if len(result) == 0:
            return None
        else:
            return result[0]
        
    def get_all_values_of_a_column(self, field_name) -> list[str]:
        result: list[str] = list()
        row: Record
        for row in self.rows:
            if (row.has_field(field_name)):
                result.append(row.field(field_name))
            else:
                print('has not field')
                result.append(None)
        return result

    @property
    def rows_count(self) -> int:
        return len(self.rows)

def testing_record() -> None:

    test: Record = Record("test")
    #record.add_or_set_field("id", 23)
    test.add_or_set(id=1, run=["towel", "bath", "test"], **{"id": 25}, description="hello")
    #print(test.field("description")


    design_step: Record = Record("d")
    design_step.add_or_set(id=45, name="Step 1")

    test_config: Record = Record("t")
    test_config.add_or_set(id=2, config1=2)

    test.linked_records.add(design_step, test_config)

    my_result_record = test.find_record_by_workflow_type("d")
    # print(my_result_record)
    my_result_record.assign_id("id")
    print(my_result_record.id)



def testing_records() -> None:
    record1: Record = Record()
    record1.add_or_set(id=1, **{"id": 25}, description="hello")

    record2: Record = Record()
    record2.add_or_set(id=2, **{"id": 25}, description="test")

    record3: Record = Record()
    record3.add_or_set(id=4, **{"id": 56}, description="cc")

    record4: Record = Record()
    record4.add_or_set(id = 5, **{"uv": "a"})

    records: Records = Records()
    records.add(record1, record2, record3, record4)


    result: list[Record] = records.find_records_by_value("id", 25)
    result_record: Record
    for result_record in result:
        print(result_record.id)


    xxx: Record = records.find_record_by_value("id", 25)
    print(xxx.id)

    vvv: list[str] = records.get_all_values_of_a_column("id")
    for i in vvv:
        print(i)

    print(record3.any("id", 56))

    records.assign_ids("id")
    print(records.find_record_by_id(4).field("d"))

    print(records.all_fields)
    print(records.ids)


testing_records()


