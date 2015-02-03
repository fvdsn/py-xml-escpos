#!/usr/bin/python

import usb.core
import usb.util
import serial
import socket

from escpos import *
from constants import *
from exceptions import *
from time import sleep

class Usb(Escpos):
    """ Define USB printer """

    def __init__(self, idVendor, idProduct, interface=0, in_ep=0x82, out_ep=0x01):
        """
        @param idVendor  : Vendor ID
        @param idProduct : Product ID
        @param interface : USB device interface
        @param in_ep     : Input end point
        @param out_ep    : Output end point
        """

        self.errorText = ":: Error Ticket :: \n------------------\nAnother ticket going to be printed\n\n\n\n\n\n"+PAPER_FULL_CUT

        self.idVendor  = idVendor
        self.idProduct = idProduct
        self.interface = interface
        self.in_ep     = in_ep
        self.out_ep    = out_ep
        self.open()


    def open(self):
        """ Search device on USB tree and set is as escpos device """
        self.device = usb.core.find(idVendor=self.idVendor, idProduct=self.idProduct)
        if self.device is None:
            print "Cable isn't plugged in"

        if self.device.is_kernel_driver_active(self.interface):
            try:
                self.device.detach_kernel_driver(self.interface)
            except usb.core.USBError as e:
                print "Could not detatch kernel driver: %s" % str(e)
        try:
            self.device.set_configuration()
        except usb.core.USBError as e:
            print "Could not set configuration: %s" % str(e)
        try:
            usb.util.claim_interface(self.device, self.interface)
        except usb.core.USBError as e:
            print "Impossible to claim the interface %s" % str(e)


    def close(self):
        i = 0
        while not self.device.is_kernel_driver_active(self.interface):
            try:
                usb.util.release_interface(self.device, self.interface)
                self.device.attach_kernel_driver(self.interface)
                usb.util.dispose_resources(self.device)
            except usb.core.USBError as e:
                i += 1
                if i > 50:
                    print "Impossible to attach kernel driver %s" % str(e)
                    return False

            sleep(0.1)
        self.device = None
        print "Printer released\n"
        return True

    def _raw(self, msg):
        """ Print any command sent in raw format """
        if len(msg) != self.device.write(self.out_ep, msg, self.interface):
            self.device.write(self.out_ep, self.errorText, self.interface)
            raise TicketNotPrinted()


    def get_status(self):
        status = {
            'printer': {}, 
            'offline': {}, 
            'error'  : {}, 
            'paper'  : {},
        }
        self.device.write(self.out_ep, DLE_EOT_PRINTER, self.interface)
        self.device.write(self.out_ep, DLE_EOT_OFFLINE, self.interface)
        self.device.write(self.out_ep, DLE_EOT_ERROR, self.interface)
        self.device.write(self.out_ep, DLE_EOT_PAPER, self.interface)
        rep = []
        maxiterate = 0
        while len(rep) < 4:
            maxiterate += 1
            if maxiterate > 10000:
                raise NoStatusError()
            r = self.device.read(self.in_ep, 20, self.interface).tolist()
            while len(r):
                rep.append(r.pop())
        print rep

        status['printer']['status_code']     = rep[0]
        status['printer']['status_error']    = not ((rep[0] & 147) == 18)
        status['printer']['online']          = not bool(rep[0] & 8)
        status['printer']['recovery']        = bool(rep[0] & 32)
        status['printer']['paper_feed_on']   = bool(rep[0] & 64)
        status['printer']['drawer_pin_high'] = bool(rep[0] & 4)
        status['offline']['status_code']     = rep[1]
        status['offline']['status_error']    = not ((rep[1] & 147) == 18)
        status['offline']['cover_open']      = bool(rep[1] & 4)
        status['offline']['paper_feed_on']   = bool(rep[1] & 8)
        status['offline']['paper']           = not bool(rep[1] & 32)
        status['offline']['error']           = bool(rep[1] & 64)
        status['error']['status_code']       = rep[2]
        status['error']['status_error']      = not ((rep[2] & 147) == 18)
        status['error']['recoverable']       = bool(rep[2] & 4)
        status['error']['autocutter']        = bool(rep[2] & 8)
        status['error']['unrecoverable']     = bool(rep[2] & 32)
        status['error']['auto_recoverable']  = not bool(rep[2] & 64)
        status['paper']['status_code']       = rep[3]
        status['paper']['status_error']      = not ((rep[3] & 147) == 18)
        status['paper']['near_end']          = bool(rep[3] & 12)
        status['paper']['present']           = not bool(rep[3] & 96)

        return status

    def __del__(self):
        """ Release USB interface """
        if self.device:
            self.close()
        self.device = None



class Serial(Escpos):
    """ Define Serial printer """

    def __init__(self, devfile="/dev/ttyS0", baudrate=9600, bytesize=8, timeout=1):
        """
        @param devfile  : Device file under dev filesystem
        @param baudrate : Baud rate for serial transmission
        @param bytesize : Serial buffer size
        @param timeout  : Read/Write timeout
        """
        self.devfile  = devfile
        self.baudrate = baudrate
        self.bytesize = bytesize
        self.timeout  = timeout
        self.open()


    def open(self):
        """ Setup serial port and set is as escpos device """
        self.device = serial.Serial(port=self.devfile, baudrate=self.baudrate, bytesize=self.bytesize, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, timeout=self.timeout, dsrdtr=True)

        if self.device is not None:
            print "Serial printer enabled"
        else:
            print "Unable to open serial printer on: %s" % self.devfile


    def _raw(self, msg):
        """ Print any command sent in raw format """
        self.device.write(msg)


    def __del__(self):
        """ Close Serial interface """
        if self.device is not None:
            self.device.close()



class Network(Escpos):
    """ Define Network printer """

    def __init__(self,host,port=9100):
        """
        @param host : Printer's hostname or IP address
        @param port : Port to write to
        """
        self.host = host
        self.port = port
        self.open()


    def open(self):
        """ Open TCP socket and set it as escpos device """
        self.device = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.device.connect((self.host, self.port))

        if self.device is None:
            print "Could not open socket for %s" % self.host


    def _raw(self, msg):
        self.device.send(msg)


    def __del__(self):
        """ Close TCP connection """
        self.device.close()
