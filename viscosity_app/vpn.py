"""
This module provides procedures to interact in a programmatic way with the
application "Viscosity" from http://www.sparklabs.com/viscosity/ using the
OS X applescripting interface.
"""

import logging
import time
import applescript


from .observer import Subject

EVT_VPN_STOPPED = 100
EVT_VPN_STARTED = 101


def connect(connection_name):
    thescript = """tell application "Viscosity" to connect \"%s\"""" % connection_name
    logging.info("VPN: connecting to '%s'", connection_name)
    return applescript.AppleScript(thescript).run()


def disconnect_all():
    thescript = """tell application "Viscosity" to disconnectall\n"""
    return applescript.AppleScript(thescript).run()


def disconnect(connection_name):
    thescript = """tell application "Viscosity" to disconnect \"%s\"\n""" % connection_name
    return applescript.AppleScript(thescript).run()


def get_active_connection_names():
    thescript = """tell application "Viscosity"
    set connames to name of connections where state is equal to "Connected"
    return connames
    end tell"""
    return applescript.AppleScript(thescript).run()


def get_all_connection_names():
    thescript = """tell application "Viscosity"
    set connames to name of connections
    end tell
    return connames"""
    return applescript.AppleScript(thescript).run()


class VpnConnection(object):
    '''
    An Applescript based controller for Viscosity.app
    (http://www.sparklabs.com/viscosity/)
    '''
    def __init__(self, connection_name):
        super(VpnConnection, self).__init__()
        if connection_name not in get_all_connection_names():
            raise ValueError("Connection '%s' not found in Viscosity!" % connection_name)
        self.__connection_name = connection_name

    @property
    def name(self):
        return self.__connection_name

    def connect(self):
        _cur_conns = get_active_connection_names()
        if self.__connection_name in _cur_conns:
            return True
        elif len(_cur_conns) > 0:
            logging.info("VPN connect(%s): already connected to non-preferred VPN(s): %r", self.__connection_name, _cur_conns)

        connect(self.__connection_name)
        # wait for it to connect
        max_wait = 30  # seconds
        current_wait = 0
        while current_wait < max_wait:
            _cur_conns = get_active_connection_names()
            if self.__connection_name in _cur_conns:
                break
            time.sleep(0.5)
        if self.__connection_name in _cur_conns:
            logging.info("VPN: connected to '%s'", self.__connection_name)
            return True
        else:
            logging.warn("VPN: failed to connect to '%s'", self.__connection_name)
            return False

    def disconnect(self):
        if self.is_connected():
            disconnect(self.__connection_name)

    def is_connected(self):
        return self.__connection_name in get_active_connection_names()


class VpnControllerSubject(Subject):
    '''
    A class capable of monitoring a specific Viscosity VPN connection and
    notifying observers about changes in the status of the connection.
    '''
    def __init__(self, vpn):
        super(VpnControllerSubject, self).__init__()
        self.connection = vpn

    def refresh(self):
        self.connected = self.connection.is_connected()

    @property
    def connected(self):
        if not hasattr(self, '_connected'):
            return None
        else:
            return self._connected

    @connected.setter
    def connected(self, value):
        oldvalue = self.connected
        self._connected = value  # pylint: disable=W0201
        if oldvalue != value:
            if value is True:
                self.notifyObservers(EVT_VPN_STARTED, "VPN('%s') is connected" % self.connection.name)
            else:
                self.notifyObservers(EVT_VPN_STOPPED, "VPN('%s') is disconnected" % self.connection.name)
