
from mkc.type import Type

class BaseType(Type):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def type_name(self) -> str:
        return self.name
    
    def feild_declaration(self, name):
        return f'{self.name} {name}'

float = BaseType('float')
double = BaseType('double')
llong = BaseType('long long')
ullong = BaseType('unsigned long long')
long = BaseType('long')
ulong = BaseType('unsigned long')
int = BaseType('int')
uint = BaseType('unsigned int')
short = BaseType('short')
ushort = BaseType('unsigned short')
char = BaseType('char')
uchar = BaseType('unsigned char')