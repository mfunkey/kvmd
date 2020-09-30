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


from aiohttp.web import Request
from aiohttp.web import Response

from ....plugins.eth import BaseEth

from ..http import exposed_http
from ..http import make_json_response


# =====
class EthApi:
    def __init__(self, eth: BaseEth) -> None:
        self.__eth = eth

    # =====

    @exposed_http("GET", "/eth")
    async def __state_handler(self, _: Request) -> Response:
        return make_json_response(await self.__eth.get_state())

    @exposed_http("POST", "/eth/connect")
    async def __connect_handler(self, _: Request) -> Response:
        await self.__eth.connect()
        return make_json_response()
    
    @exposed_http("POST", "/eth/disconnect")
    async def __connect_handler(self, _: Request) -> Response:
        await self.__eth.disconnect()
        return make_json_response()

#    @exposed_http("POST", "/eth/set_params")
#    async def __set_params_handler(self, request: Request) -> Response:
#        params = {
#            key: validator(request.query.get(param))
#            for (param, key, validator) in [
#                ("image", "name", (lambda arg: str(arg).strip() and valid_msd_image_name(arg))),
#                ("cdrom", "cdrom", valid_bool),
#            ]
#            if request.query.get(param) is not None
#        }
#        await self.__msd.set_params(**params)  # type: ignore
#        return make_json_response()
