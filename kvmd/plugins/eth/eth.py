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


import asyncio

from typing import Dict
from typing import AsyncGenerator

from ...logging import get_logger

from ... import aiotools
from ... import gpio

from ...yamlconf import Option

from ...validators.basic import valid_bool
from ...validators.basic import valid_float_f01

from ...validators.hw import valid_gpio_pin


from . import EthIsBusyError
from . import BaseEth


# =====
class Plugin(BaseEth):  # pylint: disable=too-many-instance-attributes
    def __init__(  # pylint: disable=too-many-arguments,super-init-not-called
        
    ) -> None:



    @classmethod
    def get_plugin_options(cls) -> Dict:
        return {
            "on":      Option(-1,    type=valid_gpio_pin),
            "off":        Option(-1,    type=valid_gpio_pin),
        }



    # =====

    async def on(self, wait: bool) -> None:
        if not (await self.__get_power()):
            await self.click_power(wait)

    async def off(self, wait: bool) -> None:
        if (await self.__get_power()):
            await self.click_power(wait)
