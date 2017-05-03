#! /usr/bin/python
import struct
import binascii
import unittest
from llrp_codec import *


class LLRPCodecTestCases(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_GET_READER_CAPABILITIES(self):
        msg = GET_READER_CAPABILITIES()
        msg['GET_READER_CAPABILITIES']['RequestedData'] = 'All'
        data = encode_message(msg)
        msg = decode_message(data)
        self.assertEqual(msg['GET_READER_CAPABILITIES']['RequestedData'], 'All')

    def test_GET_READER_CAPABILITIES_RESPONSE(self):
        msg = GET_READER_CAPABILITIES_RESPONSE()
        msg['GET_READER_CAPABILITIES_RESPONSE']['LLRPStatus'] = {}
        msg['GET_READER_CAPABILITIES_RESPONSE']['LLRPStatus']['StatusCode'] = 'M_Success'
        msg['GET_READER_CAPABILITIES_RESPONSE']['LLRPStatus']['ErrorDescription'] = 'hellow'
        general_cap = {}
        general_cap["MaxNumberOfAntennaSupported"] = 4
        general_cap["CanSetAntennaProperties"] = True
        general_cap["HasUTCClockCapability"] = True
        general_cap["DeviceManufacturerName"] = 0x02
        general_cap["ModelName"] = 0x03
        general_cap["ReaderFirmwareVersion"] = '\x01\x02'      
        general_cap["ReceiveSensitivityTableEntry"] = []

        t1 = {}
        t1['Index'] = 1
        t1['ReceiveSensitivityValue'] = -50
        general_cap["ReceiveSensitivityTableEntry"].append(t1)
        t2 = {}
        t2['Index'] = 2
        t2['ReceiveSensitivityValue'] = -50
        general_cap["ReceiveSensitivityTableEntry"].append(t2)

        gpio = {}
        gpio["NumGPIs"] = 3
        gpio["NumGPOs"] = 3
        general_cap["GPIOCapabilities"] = gpio

        general_cap['PerAntennaAirProtocol'] = []
        air1 = {}
        air1['AntennaID'] = 1
        air1['ProtocolID'] = []
        air1['ProtocolID'].append('EPCGlobalClass1Gen2')
        general_cap['PerAntennaAirProtocol'].append(air1)

        msg['GET_READER_CAPABILITIES_RESPONSE']['GeneralDeviceCapabilities'] = general_cap
        data = encode_message(msg)
        msg = decode_message(data)
        self.assertEqual(msg['GET_READER_CAPABILITIES_RESPONSE']['LLRPStatus']['StatusCode'], 'M_Success')
        self.assertEqual(msg['GET_READER_CAPABILITIES_RESPONSE']['GeneralDeviceCapabilities']['MaxNumberOfAntennaSupported'], 4)

    def test_ADD_ROSPEC(self):
        msg = ADD_ROSPEC()
        msg['ADD_ROSPEC']['ROSpec'] = {}
        msg['ADD_ROSPEC']['ROSpec']['ROSpecID'] = 1
        msg['ADD_ROSPEC']['ROSpec']['Priority'] = 1
        msg['ADD_ROSPEC']['ROSpec']['CurrentState'] = 'Disabled'
        msg['ADD_ROSPEC']['ROSpec']['ROBoundarySpec'] = {}
        msg['ADD_ROSPEC']['ROSpec']['ROBoundarySpec']['ROSpecStartTrigger'] = {}
        msg['ADD_ROSPEC']['ROSpec']['ROBoundarySpec']['ROSpecStopTrigger'] = {}
        msg['ADD_ROSPEC']['ROSpec']['ROBoundarySpec']['ROSpecStartTrigger']['ROSpecStartTriggerType'] = 'Periodic'
        msg['ADD_ROSPEC']['ROSpec']['ROBoundarySpec']['ROSpecStartTrigger']['PeriodicTriggerValue'] = {}
        msg['ADD_ROSPEC']['ROSpec']['ROBoundarySpec']['ROSpecStartTrigger']['PeriodicTriggerValue']['Offset'] = 0 
        msg['ADD_ROSPEC']['ROSpec']['ROBoundarySpec']['ROSpecStartTrigger']['PeriodicTriggerValue']['Period'] = 1
        msg['ADD_ROSPEC']['ROSpec']['ROBoundarySpec']['ROSpecStopTrigger']['ROSpecStopTriggerType'] = 'Duration'
        msg['ADD_ROSPEC']['ROSpec']['ROBoundarySpec']['ROSpecStopTrigger']['DurationTriggerValue'] = 32
        msg['ADD_ROSPEC']['ROSpec']['AISpec'] = []
        spec1 = {}
        spec1['AntennaIDs'] = [1,2,3,4]
        spec1['AISpecStopTrigger'] = {}
        spec1['InventoryParameterSpec'] = []
        spec1['AISpecStopTrigger']['AISpecStopTriggerType'] = 'Duration'
        spec1['AISpecStopTrigger']['DurationTrigger'] = 32
        parameter1 = {}
        parameter1['InventoryParameterSpecID'] = 1
        parameter1['ProtocolID'] = 'EPCGlobalClass1Gen2'
        spec1['InventoryParameterSpec'].append(parameter1)
        msg['ADD_ROSPEC']['ROSpec']['AISpec'].append(spec1)
        data = encode_message(msg)
        msg = decode_message(data)
        self.assertEqual(msg['ADD_ROSPEC']['ROSpec']['ROSpecID'], 1)
        self.assertEqual(msg['ADD_ROSPEC']['ROSpec']['Priority'], 1)
        self.assertEqual(msg['ADD_ROSPEC']['ROSpec']['CurrentState'], 'Disabled')
        self.assertEqual(msg['ADD_ROSPEC']['ROSpec']['ROBoundarySpec']['ROSpecStartTrigger']['ROSpecStartTriggerType'], 'Periodic')
        self.assertEqual(msg['ADD_ROSPEC']['ROSpec']['ROBoundarySpec']['ROSpecStartTrigger']['PeriodicTriggerValue']['Offset'], 0)
        self.assertEqual(msg['ADD_ROSPEC']['ROSpec']['ROBoundarySpec']['ROSpecStartTrigger']['PeriodicTriggerValue']['Period'], 1)
        self.assertEqual(msg['ADD_ROSPEC']['ROSpec']['ROBoundarySpec']['ROSpecStopTrigger']['ROSpecStopTriggerType'], 'Duration')
        self.assertEqual(msg['ADD_ROSPEC']['ROSpec']['ROBoundarySpec']['ROSpecStopTrigger']['DurationTriggerValue'], 32)


if __name__ == '__main__':
    suite = unittest.TestSuite()
    #suite.addTest(LLRPCodecTestCases('test_GET_READER_CAPABILITIES'))
    #suite.addTest(LLRPCodecTestCases('test_GET_READER_CAPABILITIES_RESPONSE'))
    suite.addTest(LLRPCodecTestCases('test_ADD_ROSPEC'))
    unittest.TextTestRunner().run(suite)
