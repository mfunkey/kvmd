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


import os
import argparse

from typing import List
from typing import Optional

from .. import init

from ...logging import get_logger

from ...validators import ValidatorError


# =====
def _link_up() -> None:
    get_logger().info("Adding IP and Link Up on usb0")
    os.system("ip link set usb0 up")
    os.system("ip address add 194.168.1.1/24 dev usb0")


def _link_down() -> None:
    get_logger().info("Removing IP and Link Down on usb0")
    os.system("ip address del 194.168.1.1/24 dev usb0")
    os.system("ip link set usb0 down")


def _start_dnsmasq() -> None:
    get_logger().info("Starting dnsmasq on usb0")
    os.system("dnsmasq --interface=usb0 --dhcp-range=194.168.1.2,194.168.1.2,255.255.255.252,1h --dhcp-option=3,194.168.1.1 --leasefile-ro")


def _stop_dnsmasq() -> None:
    get_logger().info("Stopping dnsmasq on usb0")
    os.system("killall dnsmasq")


# =====
def _cmd_start() -> None:
    logger = get_logger()
    _link_up()
    _start_dnsmasq()
    logger.info("Ready to work")


# =====
def _cmd_stop() -> None:
    logger = get_logger()
    _link_down()
    _stop_dnsmasq()
    logger.info("Bye-bye")


# =====
def main(argv: Optional[List[str]]=None) -> None:
    (parent_parser, argv, config) = init(
        add_help=False,
        argv=argv,
        load_msd=True,
    )
    parser = argparse.ArgumentParser(
        prog="kvmd-otgeth",
        description="KVMD OTG-CDC Ethernet low-level hand tool",
        parents=[parent_parser],
    )

    parser.set_defaults(cmd=(lambda *_: parser.print_help()))
    subparsers = parser.add_subparsers()

    cmd_start_parser = subparsers.add_parser("start", help="Start OTG")
    cmd_start_parser.set_defaults(cmd=_cmd_start)

    cmd_stop_parser = subparsers.add_parser("stop", help="Stop OTG")
    cmd_stop_parser.set_defaults(cmd=_cmd_stop)

    options = parser.parse_args(argv[1:])
    try:
        options.cmd()
    except ValidatorError as err:
        raise SystemExit(str(err))
