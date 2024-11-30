import threading
from contextlib import closing
from typing import NewType

from dishka import (
    Container,
    Provider,
    Scope,
    from_context,
    make_container,
    provide,
)

EnvName = NewType("EnvName", str)

Dependent = NewType("Dependent", str)

Sub = NewType("Sub", str)


Mess = NewType("Mess", str)


class NestingFunProvider(Provider):
    envname = from_context(EnvName, scope=Scope.APP)

    @provide(scope=Scope.APP)
    def dependent(self, env: EnvName) -> Dependent:
        return Dependent(EnvName)

    @provide(scope=Scope.REQUEST)
    def sub(self, dep: Dependent) -> Sub:
        return Sub(dep)

    @provide(scope=Scope.APP)
    def mess(self, appc: Container) -> Mess:
        with appc() as reqc:
            return Mess(reqc.get(Sub))


# the lock should warn
c = make_container(
    NestingFunProvider(),
    context={EnvName: "stage"},
    lock_factory=threading.RLock,
)
with closing(c):
    c.get(Mess)
