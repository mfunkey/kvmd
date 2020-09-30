# ========================================================================== #
#                                                                            #
#    KVMD - The main Pi-KVM daemon.                                          #
#                                                                            #
#    Copyright (C) 2018  Maxim Devaev <mdevaev@gmail.com>                    #
#                                                                            #
#    This program is free software: you can redistribute it and/or modify    #
#    it under the terms of the GNU General Public License as published by    #
#    the Free Software Foundation, either version 3 of the License, or       #
#    (at your option) any later version.                                     #
#                                                                            #
#    This program is distributed in the hope that it will be useful,         #
#    but WITHOUT ANY WARRANTY; without even the implied warranty of          #
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the           #
#    GNU General Public License for more details.                            #
#                                                                            #
#    You should have received a copy of the GNU General Public License       #
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.  #
#                                                                            #
# ========================================================================== #


from typing import Dict
from typing import AsyncGenerator
from typing import Type

from ...errors import OperationError
from ...errors import IsBusyError

from .. import BasePlugin
from .. import get_plugin_class


# =====
class EthError(Exception):
    pass


class EthOperationError(OperationError, EthError):
    pass


class EthIsBusyError(IsBusyError, EthError):
    def __init__(self) -> None:
        super().__init__("Performing another Eth operation, please try again later")


# =====
class BaseEth(BasePlugin):
    async def get_state(self) -> Dict:
        raise NotImplementedError

    async def cleanup(self) -> None:
        pass

    # =====

    async def on(self, wait: bool) -> None:
        raise NotImplementedError

    async def ip(self, wait: bool) -> None:
        raise NotImplementedError

    async def off(self, wait: bool) -> None:
        raise NotImplementedError




# =====
def get_eth_class(name: str) -> Type[BaseEth]:
    return get_plugin_class("eth", name)  # type: ignore
