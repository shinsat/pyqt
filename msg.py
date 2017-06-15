from struct import unpack
import datetime, time
from datetime import timezone, timedelta
import logging

LOG_FORMAT = '%(levelname) -10s %(asctime)s %(name) -30s %(funcName) -35s %(lineno) -5d: %(message)s'
LOGGER = logging.getLogger(__name__)
# time is string value not contains locale, so need to be 18 to convert to JST
JST = timezone(timedelta(hours=+18), 'JST')

class Message(object):

    class TypeValue(object):
        def __init__(self, value_type, value):
            self.value_type = value_type
            self.value = value

        def __repr__(self):
            return "{" + self.value_type.__str__() + ": " + self.value.__str__() + "}"

    def __init__(self):  # コンストラクタ
        self._whole_record = dict()

    def __str__(self):
        return self.whole_record.__str__()

    def __len__(self):
        return self.whole_record.__len__()

    @property
    def whole_record(self):
        return self._whole_record

    @whole_record.setter
    def whole_record(self, record):
        self._whole_record = record

    def get_i16(self, key_str):
        if key_str in self.whole_record:
            if 2 in self.whole_record[key_str]:
                return self.whole_record[key_str][2]
            else:
                LOGGER.warning("%s is NOT key for I16." % key_str)
                return None
        else:
            LOGGER.warning("%s does NOT exist." % key_str)
            return None

    def set_i16(self, key_str, record):
        self.whole_record.update({key_str: Message.TypeValue(2, record)})

    def get_i32(self, key_str):
        if key_str in self.whole_record:
            if 3 in self.whole_record[key_str]:
                return self.whole_record[key_str][3]
            else:
                LOGGER.warning("%s is NOT key for I32." % key_str)
                return None
        else:
            LOGGER.warning("%s does NOT exist." % key_str)
            return None

    def set_i32(self, key_str, record):
        self.whole_record.update({key_str: Message.TypeValue(3, record)})

    def get_i64(self, key_str):
        if key_str in self.whole_record:
            if 4 in self.whole_record[key_str]:
                return self.whole_record[key_str][4]
            else:
                LOGGER.warning("%s is NOT key for I64." % key_str)
                return None
        else:
            LOGGER.warning("%s does NOT exist." % key_str)
            return None

    def set_i64(self, key_str, record):
        self.whole_record.update({key_str: Message.TypeValue(4, record)})

    def get_ui8(self, key_str):
        if key_str in self.whole_record:
            if 11 in self.whole_record[key_str]:
                return self.whole_record[key_str][11]
            else:
                LOGGER.warning("%s is NOT key for UI8." % key_str)
                return None
        else:
            LOGGER.warning("%s does NOT exist." % key_str)
            return None

    def set_ui8(self, key_str, record):
        self.whole_record.update({key_str: Message.TypeValue(11, record)})

    def get_ui16(self, key_str):
        if key_str in self.whole_record:
            if 12 in self.whole_record[key_str]:
                return self.whole_record[key_str][12]
            else:
                LOGGER.warning("%s is NOT key for UI16." % key_str)
                return None
        else:
            LOGGER.warning("%s does NOT exist." % key_str)
            return None

    def set_ui16(self, key_str, record):
        self.whole_record.update({key_str: Message.TypeValue(12, record)})

    def get_ui32(self, key_str):
        if key_str in self.whole_record:
            if 13 in self.whole_record[key_str]:
                return self.whole_record[key_str][13]
            else:
                LOGGER.warning("%s is NOT key for UI32." % key_str)
                return None
        else:
            LOGGER.warning("%s does NOT exist." % key_str)
            return None

    def set_ui32(self, key_str, record):
        self.whole_record.update({key_str: Message.TypeValue(13, record)})

    def get_ui64(self, key_str):
        if key_str in self.whole_record:
            if 14 in self.whole_record[key_str]:
                return self.whole_record[key_str][14]
            else:
                LOGGER.warning("%s is NOT key for UI64." % key_str)
                return None
        else:
            LOGGER.warning("%s does NOT exist." % key_str)
            return None

    def set_ui64(self, key_str, record):
        self.whole_record.update({key_str: Message.TypeValue(21, record)})

    def get_f64(self, key_str):
        if key_str in self.whole_record:
            if 22 in self.whole_record[key_str]:
                return self.whole_record[key_str][22]
            else:
                LOGGER.warning("%s is NOT key for F64." % key_str)
                return None
        else:
            LOGGER.warning("%s does NOT exist." % key_str)
            return None

    def set_f64(self, key_str, record):
        self.whole_record.update({key_str: Message.TypeValue(22, record)})

    def get_string(self, key_str):
        if key_str in self.whole_record:
            if 31 in self.whole_record[key_str]:
                return self.whole_record[key_str][31]
            else:
                LOGGER.warning("%s is NOT key for STRING." % key_str)
                return None
        else:
            LOGGER.warning("%s does NOT exist." % key_str)
            return None

    def set_string(self, key_str, record):
        self.whole_record.update({key_str: Message.TypeValue(31, record)})

    def get_timestamp(self, key_str):
        if key_str in self.whole_record:
            if 41 in self.whole_record[key_str]:
                return self.whole_record[key_str][41]
            else:
                LOGGER.warning("%s is NOT key for timestamp." % key_str)
                return None
        else:
            LOGGER.warning("%s does NOT exist." % key_str)
            return None

    def set_timestamp(self, key_str, record):
        self.whole_record.update({key_str: Message.TypeValue(41, record)})

    def get_nano_timestamp(self, key_str):
        if key_str in self.whole_record:
            if self.whole_record[key_str].value_type == 42:
                return self.whole_record[key_str].value
            else:
                LOGGER.warning("%s is NOT key for nano timestamp." % key_str)
                return None
        else:
            LOGGER.warning("%s does NOT exist." % key_str)
            return None

    def set_nano_timestamp(self, key_str, record):
        self.whole_record.update({key_str: Message.TypeValue(42, record)})

    def get_array(self, key_str):
        if key_str in self.whole_record:
            if 60 in self.whole_record[key_str]:
                return self.whole_record[key_str][60]
            else:
                LOGGER.warning("%s is NOT key for array." % key_str)
                return None
        else:
            LOGGER.warning("%s does NOT exist." % key_str)
            return None

    def set_array(self, key_str, record):
        self.whole_record.update({key_str: Message.TypeValue(60, record)})

    def get_message(self, key_str):
        if key_str in self.whole_record:
            if 51 in self.whole_record[key_str]:
                return self.whole_record[key_str][51]
            else:
                LOGGER.warning("%s is NOT key for sub message." % key_str)
                return None
        else:
            LOGGER.warning("%s does NOT exist." % key_str)
            return None

    def set_message(self, key_str, record):
        self.whole_record.update({key_str: Message.TypeValue(51, record)})

    # private method in order to put data from binary
    def __set_from_binary(key_str, data_type, record, obj):
        mapped = Message.TypeValue(data_type, record)
        if key_str is None:
            obj.append(mapped)
        else:
            obj.update({key_str: mapped})

    def __set_array_from_binary(type_int, record, obj):
        mapped = Message.TypeValue(type_int, record)
        obj.append(mapped)

    data_type = {
        1: [1, "I08"],
        2: [2, "I16"],
        3: [4, "I32"],
        4: [8, "I64"],
        11: [1, "UI08"],
        12: [2, "UI16"],
        13: [4, "UI32"],
        14: [8, "UI64"],
        21: [4, "F32"],
        22: [8, "F64"],
        31: [8, "STR"],
        41: [4, "TIMESTAMP"],
        42: [8, "NANO_TIMESTAMP"],
        51: [0, "MSG"],
        60: [0, "ARRAY"]
    }

    # can be used for recursive read
    def read_message(self, msg_body, idx=0, obj=None):
        if idx == 0:
            obj = self.whole_record
        field_count = int.from_bytes(msg_body[idx:idx+4], 'little')
        LOGGER.debug("FieldCount[" + field_count.__str__() + "]")
        idx += 4
        # loop for field count
        for i in range(field_count):
            # extracting key string
            idx, key_str = self.read_key(msg_body=msg_body, idx=idx)
            # extracting value type
            type_int = int.from_bytes(msg_body[idx:idx+1], 'little')
            idx += 1  # increment for after type_int retrieve
            #
            if int.from_bytes(msg_body[idx:idx+1], 'little') == 0:
                idx += 1
                Message.__set_from_binary(key_str, data_type=type_int, record=None, obj=obj)
                continue
            idx += 1  # increment for after null flag retrieve
            if type_int == 60:
                arr_obj = list()
                idx = self.read_array(msg_body, idx=idx, obj=arr_obj)
                Message.__set_from_binary(key_str, type_int, arr_obj, obj)
            elif type_int == 51:
                msg_obj = dict()
                idx = self.read_message(msg_body, idx=idx, obj=msg_obj)
                Message.__set_from_binary(key_str, type_int, msg_obj, obj)
            else:
                idx = self.read_standard(msg_body, idx=idx, type_int=type_int, obj=obj, key=key_str)
        return idx

    def read_array(self, msg_body, idx, obj):
        field_count = int.from_bytes(msg_body[idx:idx + 8], 'little')
        LOGGER.debug("ArraySize:[" + field_count.__str__() + "]from[" + repr(msg_body[idx:idx+8]) + "]")
        idx += 8
        for i in range(field_count):
            type_int = int.from_bytes(msg_body[idx:idx + 1], 'little')
            LOGGER.debug("DataType:[" + self.data_type[type_int][1] + "]from[" + repr(msg_body[idx:idx + 1]) + "]")
            idx += 1  # increment for after type_int retrieve
            if int.from_bytes(msg_body[idx:idx + 1], 'little') == 0:
                idx += 1
                Message.__set_array_from_binary(type_int=type_int, record=None, obj=obj)
                continue
            idx += 1  # increment for after null flag retrieve
            # switch for data type
            if type_int == 60:
                arr_obj = list()
                idx = self.read_array(msg_body, idx=idx, obj=arr_obj)
                Message.__set_array_from_binary(type_int=type_int, record=arr_obj, obj=obj)
            elif type_int == 51:
                new_obj = dict()
                idx = self.read_message(msg_body, idx=idx, obj=new_obj)
                Message.__set_array_from_binary(type_int=type_int, record=new_obj, obj=obj)
            else:
                idx = self.read_standard(msg_body, idx=idx, type_int=type_int, obj=obj, key=None)
        return idx

    def read_key(self, msg_body, idx):
        end_idx = idx+8
        str_size = int.from_bytes(msg_body[idx:end_idx], 'little')  # magic number 8
        LOGGER.debug("KeySize:[" + str_size.__str__() + "]from[" + repr(msg_body[idx:idx + 8]) + "]")
        start_index = end_idx
        idx = end_idx + str_size  # dynamic length(string)
        LOGGER.debug("Key=["+msg_body[start_index:idx].decode('utf-8')+"]")
        return idx, msg_body[start_index:idx].decode('utf8')

    def read_standard(self, msg_body, idx, type_int, obj, key):
        value_size = self.data_type[type_int][0]
        LOGGER.debug("ValueSize:[" + value_size.__str__() + "]from[" + repr(msg_body[idx:idx + value_size]) + "]")
        end_idx = idx + value_size
        value = None
        if type_int == 1:
            LOGGER.debug("value="+int.from_bytes(msg_body[idx:end_idx], 'little', signed=True).__str__())
            LOGGER.error("Does not support 1 byte signed integer. Use I16 instead.")
        elif type_int in (2, 3, 4):
            LOGGER.debug("value="+int.from_bytes(msg_body[idx:end_idx], 'little', signed=True).__str__())
            value = int.from_bytes(msg_body[idx:end_idx], 'little', signed=True)
        elif type_int in (11, 12, 13, 14):
            LOGGER.debug("value="+int.from_bytes(msg_body[idx:end_idx], 'little', signed=False).__str__())
            value = int.from_bytes(msg_body[idx:end_idx], 'little', signed=False)
        elif type_int == 21:
            LOGGER.debug("value=" + unpack('d', msg_body[idx:end_idx])[0].__str__())
            LOGGER.error("Does not support F32. Use F64 instead.")
        elif type_int == 22:
            LOGGER.debug("value=" + unpack('d', msg_body[idx:end_idx])[0].__str__())
            value = unpack('d', msg_body[idx:end_idx])[0]
        elif type_int == 31:
            str_size = int.from_bytes(msg_body[idx:end_idx], 'little')
            idx = end_idx
            end_idx += str_size
            LOGGER.debug("value="+msg_body[idx:end_idx].decode('utf8'))
            value = msg_body[idx:end_idx].decode('utf8')
        elif type_int == 41:
            time_now = datetime.datetime.utcfromtimestamp(
                int.from_bytes(msg_body[idx:end_idx], 'little', signed=False))
            LOGGER.debug("value="+time_now.__str__())
            value = time_now.strftime('%Y-%m-%d %H:%M:%S')
        elif type_int == 42:
            time_now = datetime.datetime.utcfromtimestamp(
                int.from_bytes(msg_body[idx:end_idx], 'little', signed=False)/1000000000)
            LOGGER.debug("value="+time_now.__str__() + int.from_bytes(msg_body[idx+4:end_idx], 'little', signed=False).__str__())
            value = time_now.strftime('%Y-%m-%d %H:%M:%S') + "." + int.from_bytes(msg_body[idx:end_idx], 'little', signed=False).__str__()[12:19]
        elif type_int == 51:
            new_obj = dict()
            end_idx = self.read_message(msg_body=msg_body, idx=end_idx, obj=new_obj)
            value = new_obj
        elif type_int == 60:
            new_obj = list()
            end_idx = self.read_array(msg_body=msg_body, idx=end_idx, obj=new_obj)
            value = new_obj
        else:
            LOGGER.error('DATA_TYPE is wrong. Check incoming binary message!!!!!')

        Message.__set_from_binary(key, type_int, value, obj=obj)
        return end_idx

    def py_to_bin(self, py_msg=None):
        if py_msg == None:
            py_msg = self.whole_record
        bin_msg = py_msg.__len__().to_bytes(length=4, byteorder='little', signed=False)
        for item in py_msg:
            tmp = item.encode('utf-8')
            bin_msg += len(tmp).to_bytes(length=8, byteorder='little', signed=True)
            bin_msg += tmp
            bin_msg += py_msg[item].value_type.to_bytes(length=1, byteorder='little', signed=False)
            flag = 1
            bin_msg += flag.to_bytes(length=1, byteorder='little', signed=False)
            if py_msg[item].value_type == 2:
                bin_msg += py_msg[item].value.to_bytes(length=2, byteorder='little', signed=True)
            elif py_msg[item].value_type == 3:
                bin_msg += py_msg[item].value.to_bytes(length=4, byteorder='little', signed=True)
            elif py_msg[item].value_type == 4:
                bin_msg += py_msg[item].value.to_bytes(length=8, byteorder='little', signed=True)
            elif py_msg[item].value_type == 11:
                bin_msg += py_msg[item].value.to_bytes(length=1, byteorder='little', signed=False)
            elif py_msg[item].value_type == 12:
                bin_msg += py_msg[item].value.to_bytes(length=2, byteorder='little', signed=False)
            elif py_msg[item].value_type == 13:
                bin_msg += py_msg[item].value.to_bytes(length=4, byteorder='little', signed=False)
            elif py_msg[item].value_type == 14:
                bin_msg += py_msg[item].value.to_bytes(length=8, byteorder='little', signed=False)
            elif py_msg[item].value_type == 22:
                bin_msg += py_msg[item].value.to_bytes(length=8, byteorder='little', signed=True)
            elif py_msg[item].value_type == 31:
                tmp = py_msg[item].value.encode('utf-8')
                bin_msg += len(tmp).to_bytes(length=8, byteorder='little', signed=True)
                bin_msg += tmp
            elif py_msg[item].value_type == 41:
                bin_msg += int(time.mktime(datetime.datetime.strptime(py_msg[item].value, '%Y-%m-%d %H:%M:%S').astimezone(JST).timetuple())).to_bytes(length=4, byteorder='little', signed=False)
            elif py_msg[item].value_type == 42:
                time_long = int(time.mktime(datetime.datetime.strptime(py_msg[item].value[:19], '%Y-%m-%d %H:%M:%S').astimezone(JST).timetuple())) * 1000000000
                time_long += int(py_msg[item].value[20:])
                bin_msg += time_long.to_bytes(length=8, byteorder='little', signed=False)
            elif py_msg[item].value_type == 51:
                bin_msg += self.py_to_bin(py_msg[item].value.whole_record)
            elif py_msg[item].value_type == 60:
                bin_msg += self.py_arr_to_bin(py_msg[item].value)
            else:
                return None
        return bin_msg

    def py_arr_to_bin(self, py_msg):
        bin_msg = py_msg.__len__().to_bytes(length=8, byteorder='little', signed=False)
        for item in py_msg:
            # value
            bin_msg += item.value_type.to_bytes(length=1, byteorder='little', signed=False)
            flag = 1
            bin_msg += flag.to_bytes(length=1, byteorder='little', signed=False)
            if item.value_type == 2:
                bin_msg += item.value.to_bytes(length=2, byteorder='little', signed=True)
            elif item.value_type == 3:
                bin_msg += item.value.to_bytes(length=4, byteorder='little', signed=True)
            elif item.value_type == 4:
                bin_msg += item.value.to_bytes(length=8, byteorder='little', signed=True)
            elif item.value_type == 11:
                bin_msg += item.value.to_bytes(length=1, byteorder='little', signed=False)
            elif item.value_type == 12:
                bin_msg += item.value.to_bytes(length=2, byteorder='little', signed=False)
            elif item.value_type == 13:
                bin_msg += item.value.to_bytes(length=4, byteorder='little', signed=False)
            elif item.value_type == 14:
                bin_msg += item.value.to_bytes(length=8, byteorder='little', signed=False)
            elif item.value_type == 22:
                bin_msg += item.value.to_bytes(length=8, byteorder='little', signed=True)
            elif item.value_type == 31:
                tmp = item.value.encode('utf-8')
                bin_msg += len(tmp).to_bytes(length=8, byteorder='little', signed=True)
                bin_msg += tmp
            elif item.value_type == 41:
                bin_msg += time.mktime(datetime.datetime.strptime(item.value, '%Y-%m-%d %H:%M:%S').astimezone(JST).timetuple())(length=4, byteorder='little', signed=False)
            elif item.value_type == 42:
                time_long = int(time.mktime(datetime.datetime.strptime(item.value[:19], '%Y-%m-%d %H:%M:%S').astimezone(JST).timetuple())) * 1000000000
                time_long += int(item.value[20:])
                bin_msg += time_long.to_bytes(length=8, byteorder='little', signed=False)
            elif item.value_type == 51:
                bin_msg += self.py_to_bin(item.value.whole_record)
            elif item.value_type == 60:
                bin_msg += self.py_arr_to_bin(item.value)
            else:
                return None

        return bin_msg


if __name__ == '__main__':
    test = Message()
    test.set_ui32("Unsigned_INT", 12)
    test.set_string("STRING", "strong string!!!!")
    test.set_string('日本', "Japanese")
    test.set_string('かん', "ノドク")
    test.set_timestamp("TIME", "2018-01-01 01:01:01")
    test.set_nano_timestamp("NANO_TIME", "2018-01-01 01:00:01.1000011")
    arr = list()
    arr.append(Message.TypeValue(12, 3))
    arr.append(Message.TypeValue(13, 31))
    arr.append(Message.TypeValue(14, 334))
    arr1 = list()
    arr1.append(Message.TypeValue(12, 6))
    arr1.append(Message.TypeValue(13, 7))
    arr1.append(Message.TypeValue(14, 8))
    arr.append(Message.TypeValue(60, arr1))
    test1 = Message()
    test1.set_ui32("intintintintint", 1234)
    test1.set_string("STRING_INER", "loading image was failed")
    test.set_message("sub_msg", test1)
    test.set_array("array_with_array", arr)
    print(test)
    string_bin = test.py_to_bin()
    print(string_bin)
    ttt = Message()
    ttt.read_message(string_bin)
    print(ttt)
