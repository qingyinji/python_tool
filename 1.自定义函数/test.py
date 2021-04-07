#!python
from functools import wraps

class cfg:
    def __init__(self, func):
        self.func = func
        self.cfg_func = None

    def config_init(self):
        with open("test.config") as cfg:
            code = cfg.read()
            exec(code)
        self.cfg_func = locals()['cfg_func']

    def __call__(self):
        try:
            self.func(self.cfg_func)
        except TypeError:
            self.config_init()
            self.func(self.cfg_func)


@cfg
def main(func):
    func['a']()

@cfg
def test(func):
    func['b']()

if __name__ == '__main__':
    main()
    test()