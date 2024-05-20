from abc import ABC, abstractmethod
from fastapi import APIRouter
import ast
from typing import Any, List, Tuple


class BaseController(ABC):
    '''
    Абстракция класса контроллера. Принимает параметр APIRouter - если не указан, то создаёт собственный.

    1. Создайте экземпляр класса-наследника, например, controller = Controller(router)
    2. Сделайте функции обработчики и зарегистрируйте их в self.router
    3. Зарегистрируйте маршруты в FastAPI() с помощью app.include_router(controller.router)
    '''

    def __init__(self, router: APIRouter = None, routes_prefix: str = ''):
        if router:
            self.router = router
        else:
            self.router = APIRouter()

        self._register_routes()
        self._set_prefix(routes_prefix)

    def _set_prefix(self, routes_prefix: str = ''):
        self.router.prefix = routes_prefix

    @abstractmethod
    def _register_routes(self):
        '''
        Регистрация маршрутов для APIRouter.

        Для этого необходимо объявить функцию внутри _register_routes(self) и определить ей декоратор,
        либо добавить функцию в router с помощью:

        - self.router.add_api_route('<URL>', <function>, methods=['<METHOD>'])
        '''
        pass