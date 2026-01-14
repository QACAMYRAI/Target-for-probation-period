import allure



class BasePage:

    @allure.step('Проверить не равенство двух переменных')
    def check_for_no_equality_two_variables(self, before, after):
        assert before != after, f'Переменная "{before}" равна переменной  "{after}"'


    @allure.step('Проверить равенство двух переменных')
    def check_for_equality_two_variables(self, before, after):
        try:
            assert before == after, f'Переменная "{before}" не равна переменной "{after}"'
        except AssertionError as e:
            allure.attach(str(before), name='Значение before', attachment_type=allure.attachment_type.TEXT)
            allure.attach(str(after), name='Значение after', attachment_type=allure.attachment_type.TEXT)
            allure.attach(f'Ожидалось: {before}\nФактически: {after}',
                          name='Разница значений',
                          attachment_type=allure.attachment_type.TEXT)
            raise

    @allure.step('Проверить что в словарь есть определенный ключ с определенным значением')
    def check_all_have_key(self, data_list, key_path, expected_value=None):
        for item in data_list:
            value = item
            for key in key_path.split('.'):
                if '[' in key:
                    arr_key, idx = key.split('[')
                    idx = int(idx[:-1])
                    value = value[arr_key][idx]
                else:
                    value = value[key]

            if expected_value is not None:
                assert value == expected_value, f'Значение {value} != {expected_value}'

        return True
