def ext_func():
    print('popo')


class Me:
    def pri(self):
        print('hi')
        ext_func()



me = Me()
me.pri()