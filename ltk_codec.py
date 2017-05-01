#! /usr/bin/python

import struct


class LLRPError(Exception):
    def __str__(self, message = ""):
        return message

class LLRPResponseError(LLRPError):
    def __str__(self, message = ""):
        return message

class LLRPMessage(dict):
    def __repr__(self):
        return llrp_data2xml(self)

def reverse_dict(data):
    atad = {}
    for m in data:
        i = data[m]
        atad[i] = m
    return atad

def decode(data):
    return Parameter_struct[data]['decode']


def encode(data):
    return Parameter_struct[data]['encode']

def llrp_data2xml(msg):
    def __llrp_data2xml(msg, name, level=0):
        tabs = '\t' * level
        str = tabs + '<%s>\n' % name
        if Message_struct.has_key(name):
            fields = Message_struct[name]['fields']
        else:
            fields = Parameter_struct[name]['fields']
        for p in fields:
            try:
                sub = msg[p]
            except KeyError:
                continue

            if type(sub) == DictionaryType:
                str += __llrp_data2xml(sub, p, level + 1)
            elif type(sub) == ListType and len(sub) > 0 and\
                    type(sub[0]) == DictionaryType:
                for e in sub:
                    str += __llrp_data2xml(e, p, level + 1)
            else:
                str += tabs + '\t<%s>%s</%s>\n' % (p, sub, p)
                
        str += tabs + '</%s>\n' % name
        return str
    ans = ''
    for p in msg:
        ans += __llrp_data2xml(msg[p], p)
    return ans[: -1]

Message_struct = {}
Parameter_struct = {}


AirProtocols_Name2Type = {
	'Unspecified' : 0,
	'EPCGlobalClass1Gen2' : 1,
}

AirProtocols_Type2Name = reverse_dict(AirProtocols_Name2Type)

GetReaderCapabilitiesRequestedData_Name2Type = {
	'All' : 0,
	'General_Device_Capabilities' : 1,
	'LLRP_Capabilities' : 2,
	'Regulatory_Capabilities' : 3,
	'LLRP_Air_Protocol_Capabilities' : 4,
}

GetReaderCapabilitiesRequestedData_Type2Name = reverse_dict(GetReaderCapabilitiesRequestedData_Name2Type)

CommunicationsStandard_Name2Type = {
	'Unspecified' : 0,
	'US_FCC_Part_15' : 1,
	'ETSI_302_208' : 2,
	'ETSI_300_220' : 3,
	'Australia_LIPD_1W' : 4,
	'Australia_LIPD_4W' : 5,
	'Japan_ARIB_STD_T89' : 6,
	'Hong_Kong_OFTA_1049' : 7,
	'Taiwan_DGT_LP0002' : 8,
	'Korea_MIC_Article_5_2' : 9,
}

CommunicationsStandard_Type2Name = reverse_dict(CommunicationsStandard_Name2Type)

ROSpecState_Name2Type = {
	'Disabled' : 0,
	'Inactive' : 1,
	'Active' : 2,
}

ROSpecState_Type2Name = reverse_dict(ROSpecState_Name2Type)

ROSpecStartTriggerType_Name2Type = {
	'Null' : 0,
	'Immediate' : 1,
	'Periodic' : 2,
	'GPI' : 3,
}

ROSpecStartTriggerType_Type2Name = reverse_dict(ROSpecStartTriggerType_Name2Type)

ROSpecStopTriggerType_Name2Type = {
	'Null' : 0,
	'Duration' : 1,
	'GPI_With_Timeout' : 2,
}

ROSpecStopTriggerType_Type2Name = reverse_dict(ROSpecStopTriggerType_Name2Type)

AISpecStopTriggerType_Name2Type = {
	'Null' : 0,
	'Duration' : 1,
	'GPI_With_Timeout' : 2,
	'Tag_Observation' : 3,
}

AISpecStopTriggerType_Type2Name = reverse_dict(AISpecStopTriggerType_Name2Type)

TagObservationTriggerType_Name2Type = {
	'Upon_Seeing_N_Tags_Or_Timeout' : 0,
	'Upon_Seeing_No_More_New_Tags_For_Tms_Or_Timeout' : 1,
	'N_Attempts_To_See_All_Tags_In_FOV_Or_Timeout' : 2,
}

TagObservationTriggerType_Type2Name = reverse_dict(TagObservationTriggerType_Name2Type)

RFSurveySpecStopTriggerType_Name2Type = {
	'Null' : 0,
	'Duration' : 1,
	'N_Iterations_Through_Frequency_Range' : 2,
}

RFSurveySpecStopTriggerType_Type2Name = reverse_dict(RFSurveySpecStopTriggerType_Name2Type)

AccessSpecState_Name2Type = {
	'Disabled' : 0,
	'Active' : 1,
}

AccessSpecState_Type2Name = reverse_dict(AccessSpecState_Name2Type)

AccessSpecStopTriggerType_Name2Type = {
	'Null' : 0,
	'Operation_Count' : 1,
}

AccessSpecStopTriggerType_Type2Name = reverse_dict(AccessSpecStopTriggerType_Name2Type)

GetReaderConfigRequestedData_Name2Type = {
	'All' : 0,
	'Identification' : 1,
	'AntennaProperties' : 2,
	'AntennaConfiguration' : 3,
	'ROReportSpec' : 4,
	'ReaderEventNotificationSpec' : 5,
	'AccessReportSpec' : 6,
	'LLRPConfigurationStateValue' : 7,
	'KeepaliveSpec' : 8,
	'GPIPortCurrentState' : 9,
	'GPOWriteData' : 10,
	'EventsAndReports' : 11,
}

GetReaderConfigRequestedData_Type2Name = reverse_dict(GetReaderConfigRequestedData_Name2Type)

IdentificationType_Name2Type = {
	'MAC_Address' : 0,
	'EPC' : 1,
}

IdentificationType_Type2Name = reverse_dict(IdentificationType_Name2Type)

KeepaliveTriggerType_Name2Type = {
	'Null' : 0,
	'Periodic' : 1,
}

KeepaliveTriggerType_Type2Name = reverse_dict(KeepaliveTriggerType_Name2Type)

GPIPortState_Name2Type = {
	'Low' : 0,
	'High' : 1,
	'Unknown' : 2,
}

GPIPortState_Type2Name = reverse_dict(GPIPortState_Name2Type)

ROReportTriggerType_Name2Type = {
	'None' : 0,
	'Upon_N_Tags_Or_End_Of_AISpec' : 1,
	'Upon_N_Tags_Or_End_Of_ROSpec' : 2,
}

ROReportTriggerType_Type2Name = reverse_dict(ROReportTriggerType_Name2Type)

AccessReportTriggerType_Name2Type = {
	'Whenever_ROReport_Is_Generated' : 0,
	'End_Of_AccessSpec' : 1,
}

AccessReportTriggerType_Type2Name = reverse_dict(AccessReportTriggerType_Name2Type)

NotificationEventType_Name2Type = {
	'Upon_Hopping_To_Next_Channel' : 0,
	'GPI_Event' : 1,
	'ROSpec_Event' : 2,
	'Report_Buffer_Fill_Warning' : 3,
	'Reader_Exception_Event' : 4,
	'RFSurvey_Event' : 5,
	'AISpec_Event' : 6,
	'AISpec_Event_With_Details' : 7,
	'Antenna_Event' : 8,
}

NotificationEventType_Type2Name = reverse_dict(NotificationEventType_Name2Type)

ROSpecEventType_Name2Type = {
	'Start_Of_ROSpec' : 0,
	'End_Of_ROSpec' : 1,
	'Preemption_Of_ROSpec' : 2,
}

ROSpecEventType_Type2Name = reverse_dict(ROSpecEventType_Name2Type)

RFSurveyEventType_Name2Type = {
	'Start_Of_RFSurvey' : 0,
	'End_Of_RFSurvey' : 1,
}

RFSurveyEventType_Type2Name = reverse_dict(RFSurveyEventType_Name2Type)

AISpecEventType_Name2Type = {
	'End_Of_AISpec' : 0,
}

AISpecEventType_Type2Name = reverse_dict(AISpecEventType_Name2Type)

AntennaEventType_Name2Type = {
	'Antenna_Disconnected' : 0,
	'Antenna_Connected' : 1,
}

AntennaEventType_Type2Name = reverse_dict(AntennaEventType_Name2Type)

ConnectionAttemptStatusType_Name2Type = {
	'Success' : 0,
	'Failed_A_Reader_Initiated_Connection_Already_Exists' : 1,
	'Failed_A_Client_Initiated_Connection_Already_Exists' : 2,
	'Failed_Reason_Other_Than_A_Connection_Already_Exists' : 3,
	'Another_Connection_Attempted' : 4,
}

ConnectionAttemptStatusType_Type2Name = reverse_dict(ConnectionAttemptStatusType_Name2Type)

StatusCode_Name2Type = {
	'M_Success' : 0,
	'M_ParameterError' : 100,
	'M_FieldError' : 101,
	'M_UnexpectedParameter' : 102,
	'M_MissingParameter' : 103,
	'M_DuplicateParameter' : 104,
	'M_OverflowParameter' : 105,
	'M_OverflowField' : 106,
	'M_UnknownParameter' : 107,
	'M_UnknownField' : 108,
	'M_UnsupportedMessage' : 109,
	'M_UnsupportedVersion' : 110,
	'M_UnsupportedParameter' : 111,
	'P_ParameterError' : 200,
	'P_FieldError' : 201,
	'P_UnexpectedParameter' : 202,
	'P_MissingParameter' : 203,
	'P_DuplicateParameter' : 204,
	'P_OverflowParameter' : 205,
	'P_OverflowField' : 206,
	'P_UnknownParameter' : 207,
	'P_UnknownField' : 208,
	'P_UnsupportedParameter' : 209,
	'A_Invalid' : 300,
	'A_OutOfRange' : 301,
	'R_DeviceError' : 401,
}

StatusCode_Type2Name = reverse_dict(StatusCode_Name2Type)

C1G2DRValue_Name2Type = {
	'DRV_8' : 0,
	'DRV_64_3' : 1,
}

C1G2DRValue_Type2Name = reverse_dict(C1G2DRValue_Name2Type)

C1G2MValue_Name2Type = {
	'MV_FM0' : 0,
	'MV_2' : 1,
	'MV_4' : 2,
	'MV_8' : 3,
}

C1G2MValue_Type2Name = reverse_dict(C1G2MValue_Name2Type)

C1G2ForwardLinkModulation_Name2Type = {
	'PR_ASK' : 0,
	'SSB_ASK' : 1,
	'DSB_ASK' : 2,
}

C1G2ForwardLinkModulation_Type2Name = reverse_dict(C1G2ForwardLinkModulation_Name2Type)

C1G2SpectralMaskIndicator_Name2Type = {
	'Unknown' : 0,
	'SI' : 1,
	'MI' : 2,
	'DI' : 3,
}

C1G2SpectralMaskIndicator_Type2Name = reverse_dict(C1G2SpectralMaskIndicator_Name2Type)

C1G2TruncateAction_Name2Type = {
	'Unspecified' : 0,
	'Do_Not_Truncate' : 1,
	'Truncate' : 2,
}

C1G2TruncateAction_Type2Name = reverse_dict(C1G2TruncateAction_Name2Type)

C1G2StateAwareTarget_Name2Type = {
	'SL' : 0,
	'Inventoried_State_For_Session_S0' : 1,
	'Inventoried_State_For_Session_S1' : 2,
	'Inventoried_State_For_Session_S2' : 3,
	'Inventoried_State_For_Session_S3' : 4,
}

C1G2StateAwareTarget_Type2Name = reverse_dict(C1G2StateAwareTarget_Name2Type)

C1G2StateAwareAction_Name2Type = {
	'AssertSLOrA_DeassertSLOrB' : 0,
	'AssertSLOrA_Noop' : 1,
	'Noop_DeassertSLOrB' : 2,
	'NegateSLOrABBA_Noop' : 3,
	'DeassertSLOrB_AssertSLOrA' : 4,
	'DeassertSLOrB_Noop' : 5,
	'Noop_AssertSLOrA' : 6,
	'Noop_NegateSLOrABBA' : 7,
}

C1G2StateAwareAction_Type2Name = reverse_dict(C1G2StateAwareAction_Name2Type)

C1G2StateUnawareAction_Name2Type = {
	'Select_Unselect' : 0,
	'Select_DoNothing' : 1,
	'DoNothing_Unselect' : 2,
	'Unselect_DoNothing' : 3,
	'Unselect_Select' : 4,
	'DoNothing_Select' : 5,
}

C1G2StateUnawareAction_Type2Name = reverse_dict(C1G2StateUnawareAction_Name2Type)

C1G2TagInventoryStateAwareI_Name2Type = {
	'State_A' : 0,
	'State_B' : 1,
}

C1G2TagInventoryStateAwareI_Type2Name = reverse_dict(C1G2TagInventoryStateAwareI_Name2Type)

C1G2TagInventoryStateAwareS_Name2Type = {
	'SL' : 0,
	'Not_SL' : 1,
}

C1G2TagInventoryStateAwareS_Type2Name = reverse_dict(C1G2TagInventoryStateAwareS_Name2Type)

C1G2LockPrivilege_Name2Type = {
	'Read_Write' : 0,
	'Perma_Lock' : 1,
	'Perma_Unlock' : 2,
	'Unlock' : 3,
}

C1G2LockPrivilege_Type2Name = reverse_dict(C1G2LockPrivilege_Name2Type)

C1G2LockDataField_Name2Type = {
	'Kill_Password' : 0,
	'Access_Password' : 1,
	'EPC_Memory' : 2,
	'TID_Memory' : 3,
	'User_Memory' : 4,
}

C1G2LockDataField_Type2Name = reverse_dict(C1G2LockDataField_Name2Type)

C1G2ReadResultType_Name2Type = {
	'Success' : 0,
	'Nonspecific_Tag_Error' : 1,
	'No_Response_From_Tag' : 2,
	'Nonspecific_Reader_Error' : 3,
}

C1G2ReadResultType_Type2Name = reverse_dict(C1G2ReadResultType_Name2Type)

C1G2WriteResultType_Name2Type = {
	'Success' : 0,
	'Tag_Memory_Overrun_Error' : 1,
	'Tag_Memory_Locked_Error' : 2,
	'Insufficient_Power' : 3,
	'Nonspecific_Tag_Error' : 4,
	'No_Response_From_Tag' : 5,
	'Nonspecific_Reader_Error' : 6,
}

C1G2WriteResultType_Type2Name = reverse_dict(C1G2WriteResultType_Name2Type)

C1G2KillResultType_Name2Type = {
	'Success' : 0,
	'Zero_Kill_Password_Error' : 1,
	'Insufficient_Power' : 2,
	'Nonspecific_Tag_Error' : 3,
	'No_Response_From_Tag' : 4,
	'Nonspecific_Reader_Error' : 5,
}

C1G2KillResultType_Type2Name = reverse_dict(C1G2KillResultType_Name2Type)

C1G2LockResultType_Name2Type = {
	'Success' : 0,
	'Insufficient_Power' : 1,
	'Nonspecific_Tag_Error' : 2,
	'No_Response_From_Tag' : 3,
	'Nonspecific_Reader_Error' : 4,
}

C1G2LockResultType_Type2Name = reverse_dict(C1G2LockResultType_Name2Type)

C1G2BlockEraseResultType_Name2Type = {
	'Success' : 0,
	'Tag_Memory_Overrun_Error' : 1,
	'Tag_Memory_Locked_Error' : 2,
	'Insufficient_Power' : 3,
	'Nonspecific_Tag_Error' : 4,
	'No_Response_From_Tag' : 5,
	'Nonspecific_Reader_Error' : 6,
}

C1G2BlockEraseResultType_Type2Name = reverse_dict(C1G2BlockEraseResultType_Name2Type)

C1G2BlockWriteResultType_Name2Type = {
	'Success' : 0,
	'Tag_Memory_Overrun_Error' : 1,
	'Tag_Memory_Locked_Error' : 2,
	'Insufficient_Power' : 3,
	'Nonspecific_Tag_Error' : 4,
	'No_Response_From_Tag' : 5,
	'Nonspecific_Reader_Error' : 6,
}

C1G2BlockWriteResultType_Type2Name = reverse_dict(C1G2BlockWriteResultType_Name2Type)

Parameter_struct['UTCTimestamp'] = {
    'type' : 128,
    'fields':  [ 
        'Type', 
        'Microseconds',
     ],
    'encode' : encode_UTCTimestamp,
    'decode' : decode_UTCTimestamp,

}

Parameter_struct['Uptime'] = {
    'type' : 129,
    'fields':  [ 
        'Type', 
        'Microseconds',
     ],
    'encode' : encode_Uptime,
    'decode' : decode_Uptime,

}

Parameter_struct['Custom'] = {
    'type' : 1023,
    'fields':  [ 
        'Type', 
        'VendorIdentifier',
         'ParameterSubtype',
         'Data',
     ],
    'encode' : encode_Custom,
    'decode' : decode_Custom,

}

Parameter_struct['GeneralDeviceCapabilities'] = {
    'type' : 137,
    'fields':  [ 
        'Type', 
        'MaxNumberOfAntennaSupported',
         'CanSetAntennaProperties',
         'HasUTCClockCapability',
         'DeviceManufacturerName',
         'ModelName',
         'ReaderFirmwareVersion',
         'ReceiveSensitivityTableEntry',
         'PerAntennaReceiveSensitivityRange',
         'GPIOCapabilities',
         'PerAntennaAirProtocol',
     ],
    'encode' : encode_GeneralDeviceCapabilities,
    'decode' : decode_GeneralDeviceCapabilities,

}

Parameter_struct['ReceiveSensitivityTableEntry'] = {
    'type' : 139,
    'fields':  [ 
        'Type', 
        'Index',
         'ReceiveSensitivityValue',
     ],
    'encode' : encode_ReceiveSensitivityTableEntry,
    'decode' : decode_ReceiveSensitivityTableEntry,

}

Parameter_struct['PerAntennaReceiveSensitivityRange'] = {
    'type' : 149,
    'fields':  [ 
        'Type', 
        'AntennaID',
         'ReceiveSensitivityIndexMin',
         'ReceiveSensitivityIndexMax',
     ],
    'encode' : encode_PerAntennaReceiveSensitivityRange,
    'decode' : decode_PerAntennaReceiveSensitivityRange,

}

Parameter_struct['PerAntennaAirProtocol'] = {
    'type' : 140,
    'fields':  [ 
        'Type', 
        'AntennaID',
         'ProtocolID',
     ],
    'encode' : encode_PerAntennaAirProtocol,
    'decode' : decode_PerAntennaAirProtocol,

}

Parameter_struct['GPIOCapabilities'] = {
    'type' : 141,
    'fields':  [ 
        'Type', 
        'NumGPIs',
         'NumGPOs',
     ],
    'encode' : encode_GPIOCapabilities,
    'decode' : decode_GPIOCapabilities,

}

Parameter_struct['LLRPCapabilities'] = {
    'type' : 142,
    'fields':  [ 
        'Type', 
        'CanDoRFSurvey',
         'CanReportBufferFillWarning',
         'SupportsClientRequestOpSpec',
         'CanDoTagInventoryStateAwareSingulation',
         'SupportsEventAndReportHolding',
         'MaxNumPriorityLevelsSupported',
         'ClientRequestOpSpecTimeout',
         'MaxNumROSpecs',
         'MaxNumSpecsPerROSpec',
         'MaxNumInventoryParameterSpecsPerAISpec',
         'MaxNumAccessSpecs',
         'MaxNumOpSpecsPerAccessSpec',
     ],
    'encode' : encode_LLRPCapabilities,
    'decode' : decode_LLRPCapabilities,

}

Parameter_struct['RegulatoryCapabilities'] = {
    'type' : 143,
    'fields':  [ 
        'Type', 
        'CountryCode',
         'CommunicationsStandard',
         'UHFBandCapabilities',
         'Custom',
     ],
    'encode' : encode_RegulatoryCapabilities,
    'decode' : decode_RegulatoryCapabilities,

}

Parameter_struct['UHFBandCapabilities'] = {
    'type' : 144,
    'fields':  [ 
        'Type', 
        'TransmitPowerLevelTableEntry',
         'FrequencyInformation',
         'AirProtocolUHFRFModeTable',
     ],
    'encode' : encode_UHFBandCapabilities,
    'decode' : decode_UHFBandCapabilities,

}

Parameter_struct['TransmitPowerLevelTableEntry'] = {
    'type' : 145,
    'fields':  [ 
        'Type', 
        'Index',
         'TransmitPowerValue',
     ],
    'encode' : encode_TransmitPowerLevelTableEntry,
    'decode' : decode_TransmitPowerLevelTableEntry,

}

Parameter_struct['FrequencyInformation'] = {
    'type' : 146,
    'fields':  [ 
        'Type', 
        'Hopping',
         'FrequencyHopTable',
         'FixedFrequencyTable',
     ],
    'encode' : encode_FrequencyInformation,
    'decode' : decode_FrequencyInformation,

}

Parameter_struct['FrequencyHopTable'] = {
    'type' : 147,
    'fields':  [ 
        'Type', 
        'HopTableID',
         'Frequency',
     ],
    'encode' : encode_FrequencyHopTable,
    'decode' : decode_FrequencyHopTable,

}

Parameter_struct['FixedFrequencyTable'] = {
    'type' : 148,
    'fields':  [ 
        'Type', 
        'Frequency',
     ],
    'encode' : encode_FixedFrequencyTable,
    'decode' : decode_FixedFrequencyTable,

}

Parameter_struct['ROSpec'] = {
    'type' : 177,
    'fields':  [ 
        'Type', 
        'ROSpecID',
         'Priority',
         'CurrentState',
         'ROBoundarySpec',
         'SpecParameter',
         'ROReportSpec',
     ],
    'encode' : encode_ROSpec,
    'decode' : decode_ROSpec,

}

Parameter_struct['ROBoundarySpec'] = {
    'type' : 178,
    'fields':  [ 
        'Type', 
        'ROSpecStartTrigger',
         'ROSpecStopTrigger',
     ],
    'encode' : encode_ROBoundarySpec,
    'decode' : decode_ROBoundarySpec,

}

Parameter_struct['ROSpecStartTrigger'] = {
    'type' : 179,
    'fields':  [ 
        'Type', 
        'ROSpecStartTriggerType',
         'PeriodicTriggerValue',
         'GPITriggerValue',
     ],
    'encode' : encode_ROSpecStartTrigger,
    'decode' : decode_ROSpecStartTrigger,

}

Parameter_struct['PeriodicTriggerValue'] = {
    'type' : 180,
    'fields':  [ 
        'Type', 
        'Offset',
         'Period',
         'UTCTimestamp',
     ],
    'encode' : encode_PeriodicTriggerValue,
    'decode' : decode_PeriodicTriggerValue,

}

Parameter_struct['GPITriggerValue'] = {
    'type' : 181,
    'fields':  [ 
        'Type', 
        'GPIPortNum',
         'GPIEvent',
         'Timeout',
     ],
    'encode' : encode_GPITriggerValue,
    'decode' : decode_GPITriggerValue,

}

Parameter_struct['ROSpecStopTrigger'] = {
    'type' : 182,
    'fields':  [ 
        'Type', 
        'ROSpecStopTriggerType',
         'DurationTriggerValue',
         'GPITriggerValue',
     ],
    'encode' : encode_ROSpecStopTrigger,
    'decode' : decode_ROSpecStopTrigger,

}

Parameter_struct['AISpec'] = {
    'type' : 183,
    'fields':  [ 
        'Type', 
        'AntennaIDs',
         'AISpecStopTrigger',
         'InventoryParameterSpec',
         'Custom',
     ],
    'encode' : encode_AISpec,
    'decode' : decode_AISpec,

}

Parameter_struct['AISpecStopTrigger'] = {
    'type' : 184,
    'fields':  [ 
        'Type', 
        'AISpecStopTriggerType',
         'DurationTrigger',
         'GPITriggerValue',
         'TagObservationTrigger',
     ],
    'encode' : encode_AISpecStopTrigger,
    'decode' : decode_AISpecStopTrigger,

}

Parameter_struct['TagObservationTrigger'] = {
    'type' : 185,
    'fields':  [ 
        'Type', 
        'TriggerType',
         'NumberOfTags',
         'NumberOfAttempts',
         'T',
         'Timeout',
     ],
    'encode' : encode_TagObservationTrigger,
    'decode' : decode_TagObservationTrigger,

}

Parameter_struct['InventoryParameterSpec'] = {
    'type' : 186,
    'fields':  [ 
        'Type', 
        'InventoryParameterSpecID',
         'ProtocolID',
         'AntennaConfiguration',
         'Custom',
     ],
    'encode' : encode_InventoryParameterSpec,
    'decode' : decode_InventoryParameterSpec,

}

Parameter_struct['RFSurveySpec'] = {
    'type' : 187,
    'fields':  [ 
        'Type', 
        'AntennaID',
         'StartFrequency',
         'EndFrequency',
         'RFSurveySpecStopTrigger',
         'Custom',
     ],
    'encode' : encode_RFSurveySpec,
    'decode' : decode_RFSurveySpec,

}

Parameter_struct['RFSurveySpecStopTrigger'] = {
    'type' : 188,
    'fields':  [ 
        'Type', 
        'StopTriggerType',
         'DurationPeriod',
         'N',
     ],
    'encode' : encode_RFSurveySpecStopTrigger,
    'decode' : decode_RFSurveySpecStopTrigger,

}

Parameter_struct['AccessSpec'] = {
    'type' : 207,
    'fields':  [ 
        'Type', 
        'AccessSpecID',
         'AntennaID',
         'ProtocolID',
         'CurrentState',
         'ROSpecID',
         'AccessSpecStopTrigger',
         'AccessCommand',
         'AccessReportSpec',
         'Custom',
     ],
    'encode' : encode_AccessSpec,
    'decode' : decode_AccessSpec,

}

Parameter_struct['AccessSpecStopTrigger'] = {
    'type' : 208,
    'fields':  [ 
        'Type', 
        'AccessSpecStopTrigger',
         'OperationCountValue',
     ],
    'encode' : encode_AccessSpecStopTrigger,
    'decode' : decode_AccessSpecStopTrigger,

}

Parameter_struct['AccessCommand'] = {
    'type' : 209,
    'fields':  [ 
        'Type', 
        'AirProtocolTagSpec',
         'AccessCommandOpSpec',
         'Custom',
     ],
    'encode' : encode_AccessCommand,
    'decode' : decode_AccessCommand,

}

Parameter_struct['LLRPConfigurationStateValue'] = {
    'type' : 217,
    'fields':  [ 
        'Type', 
        'LLRPConfigurationStateValue',
     ],
    'encode' : encode_LLRPConfigurationStateValue,
    'decode' : decode_LLRPConfigurationStateValue,

}

Parameter_struct['Identification'] = {
    'type' : 218,
    'fields':  [ 
        'Type', 
        'IDType',
         'ReaderID',
     ],
    'encode' : encode_Identification,
    'decode' : decode_Identification,

}

Parameter_struct['GPOWriteData'] = {
    'type' : 219,
    'fields':  [ 
        'Type', 
        'GPOPortNumber',
         'GPOData',
     ],
    'encode' : encode_GPOWriteData,
    'decode' : decode_GPOWriteData,

}

Parameter_struct['KeepaliveSpec'] = {
    'type' : 220,
    'fields':  [ 
        'Type', 
        'KeepaliveTriggerType',
         'PeriodicTriggerValue',
     ],
    'encode' : encode_KeepaliveSpec,
    'decode' : decode_KeepaliveSpec,

}

Parameter_struct['AntennaProperties'] = {
    'type' : 221,
    'fields':  [ 
        'Type', 
        'AntennaConnected',
         'AntennaID',
         'AntennaGain',
     ],
    'encode' : encode_AntennaProperties,
    'decode' : decode_AntennaProperties,

}

Parameter_struct['AntennaConfiguration'] = {
    'type' : 222,
    'fields':  [ 
        'Type', 
        'AntennaID',
         'RFReceiver',
         'RFTransmitter',
         'AirProtocolInventoryCommandSettings',
     ],
    'encode' : encode_AntennaConfiguration,
    'decode' : decode_AntennaConfiguration,

}

Parameter_struct['RFReceiver'] = {
    'type' : 223,
    'fields':  [ 
        'Type', 
        'ReceiverSensitivity',
     ],
    'encode' : encode_RFReceiver,
    'decode' : decode_RFReceiver,

}

Parameter_struct['RFTransmitter'] = {
    'type' : 224,
    'fields':  [ 
        'Type', 
        'HopTableID',
         'ChannelIndex',
         'TransmitPower',
     ],
    'encode' : encode_RFTransmitter,
    'decode' : decode_RFTransmitter,

}

Parameter_struct['GPIPortCurrentState'] = {
    'type' : 225,
    'fields':  [ 
        'Type', 
        'GPIPortNum',
         'Config',
         'State',
     ],
    'encode' : encode_GPIPortCurrentState,
    'decode' : decode_GPIPortCurrentState,

}

Parameter_struct['EventsAndReports'] = {
    'type' : 226,
    'fields':  [ 
        'Type', 
        'HoldEventsAndReportsUponReconnect',
     ],
    'encode' : encode_EventsAndReports,
    'decode' : decode_EventsAndReports,

}

Parameter_struct['ROReportSpec'] = {
    'type' : 237,
    'fields':  [ 
        'Type', 
        'ROReportTrigger',
         'N',
         'TagReportContentSelector',
         'Custom',
     ],
    'encode' : encode_ROReportSpec,
    'decode' : decode_ROReportSpec,

}

Parameter_struct['TagReportContentSelector'] = {
    'type' : 238,
    'fields':  [ 
        'Type', 
        'EnableROSpecID',
         'EnableSpecIndex',
         'EnableInventoryParameterSpecID',
         'EnableAntennaID',
         'EnableChannelIndex',
         'EnablePeakRSSI',
         'EnableFirstSeenTimestamp',
         'EnableLastSeenTimestamp',
         'EnableTagSeenCount',
         'EnableAccessSpecID',
         'AirProtocolEPCMemorySelector',
     ],
    'encode' : encode_TagReportContentSelector,
    'decode' : decode_TagReportContentSelector,

}

Parameter_struct['AccessReportSpec'] = {
    'type' : 239,
    'fields':  [ 
        'Type', 
        'AccessReportTrigger',
     ],
    'encode' : encode_AccessReportSpec,
    'decode' : decode_AccessReportSpec,

}

Parameter_struct['TagReportData'] = {
    'type' : 240,
    'fields':  [ 
        'Type', 
        'EPCParameter',
         'ROSpecID',
         'SpecIndex',
         'InventoryParameterSpecID',
         'AntennaID',
         'PeakRSSI',
         'ChannelIndex',
         'FirstSeenTimestampUTC',
         'FirstSeenTimestampUptime',
         'LastSeenTimestampUTC',
         'LastSeenTimestampUptime',
         'TagSeenCount',
         'AirProtocolTagData',
         'AccessSpecID',
         'AccessCommandOpSpecResult',
         'Custom',
     ],
    'encode' : encode_TagReportData,
    'decode' : decode_TagReportData,

}

Parameter_struct['EPCData'] = {
    'type' : 241,
    'fields':  [ 
        'Type', 
        'EPC',
     ],
    'encode' : encode_EPCData,
    'decode' : decode_EPCData,

}

Parameter_struct['EPC_96'] = {
    'type' : 13,
    'fields':  [ 
        'Type', 
        'EPC',
     ],
    'encode' : encode_EPC_96,
    'decode' : decode_EPC_96,

}

Parameter_struct['ROSpecID'] = {
    'type' : 9,
    'fields':  [ 
        'Type', 
        'ROSpecID',
     ],
    'encode' : encode_ROSpecID,
    'decode' : decode_ROSpecID,

}

Parameter_struct['SpecIndex'] = {
    'type' : 14,
    'fields':  [ 
        'Type', 
        'SpecIndex',
     ],
    'encode' : encode_SpecIndex,
    'decode' : decode_SpecIndex,

}

Parameter_struct['InventoryParameterSpecID'] = {
    'type' : 10,
    'fields':  [ 
        'Type', 
        'InventoryParameterSpecID',
     ],
    'encode' : encode_InventoryParameterSpecID,
    'decode' : decode_InventoryParameterSpecID,

}

Parameter_struct['AntennaID'] = {
    'type' : 1,
    'fields':  [ 
        'Type', 
        'AntennaID',
     ],
    'encode' : encode_AntennaID,
    'decode' : decode_AntennaID,

}

Parameter_struct['PeakRSSI'] = {
    'type' : 6,
    'fields':  [ 
        'Type', 
        'PeakRSSI',
     ],
    'encode' : encode_PeakRSSI,
    'decode' : decode_PeakRSSI,

}

Parameter_struct['ChannelIndex'] = {
    'type' : 7,
    'fields':  [ 
        'Type', 
        'ChannelIndex',
     ],
    'encode' : encode_ChannelIndex,
    'decode' : decode_ChannelIndex,

}

Parameter_struct['FirstSeenTimestampUTC'] = {
    'type' : 2,
    'fields':  [ 
        'Type', 
        'Microseconds',
     ],
    'encode' : encode_FirstSeenTimestampUTC,
    'decode' : decode_FirstSeenTimestampUTC,

}

Parameter_struct['FirstSeenTimestampUptime'] = {
    'type' : 3,
    'fields':  [ 
        'Type', 
        'Microseconds',
     ],
    'encode' : encode_FirstSeenTimestampUptime,
    'decode' : decode_FirstSeenTimestampUptime,

}

Parameter_struct['LastSeenTimestampUTC'] = {
    'type' : 4,
    'fields':  [ 
        'Type', 
        'Microseconds',
     ],
    'encode' : encode_LastSeenTimestampUTC,
    'decode' : decode_LastSeenTimestampUTC,

}

Parameter_struct['LastSeenTimestampUptime'] = {
    'type' : 5,
    'fields':  [ 
        'Type', 
        'Microseconds',
     ],
    'encode' : encode_LastSeenTimestampUptime,
    'decode' : decode_LastSeenTimestampUptime,

}

Parameter_struct['TagSeenCount'] = {
    'type' : 8,
    'fields':  [ 
        'Type', 
        'TagCount',
     ],
    'encode' : encode_TagSeenCount,
    'decode' : decode_TagSeenCount,

}

Parameter_struct['AccessSpecID'] = {
    'type' : 16,
    'fields':  [ 
        'Type', 
        'AccessSpecID',
     ],
    'encode' : encode_AccessSpecID,
    'decode' : decode_AccessSpecID,

}

Parameter_struct['RFSurveyReportData'] = {
    'type' : 242,
    'fields':  [ 
        'Type', 
        'ROSpecID',
         'SpecIndex',
         'FrequencyRSSILevelEntry',
         'Custom',
     ],
    'encode' : encode_RFSurveyReportData,
    'decode' : decode_RFSurveyReportData,

}

Parameter_struct['FrequencyRSSILevelEntry'] = {
    'type' : 243,
    'fields':  [ 
        'Type', 
        'Frequency',
         'Bandwidth',
         'AverageRSSI',
         'PeakRSSI',
         'Timestamp',
     ],
    'encode' : encode_FrequencyRSSILevelEntry,
    'decode' : decode_FrequencyRSSILevelEntry,

}

Parameter_struct['ReaderEventNotificationSpec'] = {
    'type' : 244,
    'fields':  [ 
        'Type', 
        'EventNotificationState',
     ],
    'encode' : encode_ReaderEventNotificationSpec,
    'decode' : decode_ReaderEventNotificationSpec,

}

Parameter_struct['EventNotificationState'] = {
    'type' : 245,
    'fields':  [ 
        'Type', 
        'EventType',
         'NotificationState',
     ],
    'encode' : encode_EventNotificationState,
    'decode' : decode_EventNotificationState,

}

Parameter_struct['ReaderEventNotificationData'] = {
    'type' : 246,
    'fields':  [ 
        'Type', 
        'Timestamp',
         'HoppingEvent',
         'GPIEvent',
         'ROSpecEvent',
         'ReportBufferLevelWarningEvent',
         'ReportBufferOverflowErrorEvent',
         'ReaderExceptionEvent',
         'RFSurveyEvent',
         'AISpecEvent',
         'AntennaEvent',
         'ConnectionAttemptEvent',
         'ConnectionCloseEvent',
         'Custom',
     ],
    'encode' : encode_ReaderEventNotificationData,
    'decode' : decode_ReaderEventNotificationData,

}

Parameter_struct['HoppingEvent'] = {
    'type' : 247,
    'fields':  [ 
        'Type', 
        'HopTableID',
         'NextChannelIndex',
     ],
    'encode' : encode_HoppingEvent,
    'decode' : decode_HoppingEvent,

}

Parameter_struct['GPIEvent'] = {
    'type' : 248,
    'fields':  [ 
        'Type', 
        'GPIPortNumber',
         'GPIEvent',
     ],
    'encode' : encode_GPIEvent,
    'decode' : decode_GPIEvent,

}

Parameter_struct['ROSpecEvent'] = {
    'type' : 249,
    'fields':  [ 
        'Type', 
        'EventType',
         'ROSpecID',
         'PreemptingROSpecID',
     ],
    'encode' : encode_ROSpecEvent,
    'decode' : decode_ROSpecEvent,

}

Parameter_struct['ReportBufferLevelWarningEvent'] = {
    'type' : 250,
    'fields':  [ 
        'Type', 
        'ReportBufferPercentageFull',
     ],
    'encode' : encode_ReportBufferLevelWarningEvent,
    'decode' : decode_ReportBufferLevelWarningEvent,

}

Parameter_struct['ReportBufferOverflowErrorEvent'] = {
    'type' : 251,
    'fields':  [ 
        'Type', 
    ],
    'encode' : encode_ReportBufferOverflowErrorEvent,
    'decode' : decode_ReportBufferOverflowErrorEvent,

}

Parameter_struct['ReaderExceptionEvent'] = {
    'type' : 252,
    'fields':  [ 
        'Type', 
        'Message',
         'ROSpecID',
         'SpecIndex',
         'InventoryParameterSpecID',
         'AntennaID',
         'AccessSpecID',
         'OpSpecID',
         'Custom',
     ],
    'encode' : encode_ReaderExceptionEvent,
    'decode' : decode_ReaderExceptionEvent,

}

Parameter_struct['OpSpecID'] = {
    'type' : 17,
    'fields':  [ 
        'Type', 
        'OpSpecID',
     ],
    'encode' : encode_OpSpecID,
    'decode' : decode_OpSpecID,

}

Parameter_struct['RFSurveyEvent'] = {
    'type' : 253,
    'fields':  [ 
        'Type', 
        'EventType',
         'ROSpecID',
         'SpecIndex',
     ],
    'encode' : encode_RFSurveyEvent,
    'decode' : decode_RFSurveyEvent,

}

Parameter_struct['AISpecEvent'] = {
    'type' : 254,
    'fields':  [ 
        'Type', 
        'EventType',
         'ROSpecID',
         'SpecIndex',
         'AirProtocolSingulationDetails',
     ],
    'encode' : encode_AISpecEvent,
    'decode' : decode_AISpecEvent,

}

Parameter_struct['AntennaEvent'] = {
    'type' : 255,
    'fields':  [ 
        'Type', 
        'EventType',
         'AntennaID',
     ],
    'encode' : encode_AntennaEvent,
    'decode' : decode_AntennaEvent,

}

Parameter_struct['ConnectionAttemptEvent'] = {
    'type' : 256,
    'fields':  [ 
        'Type', 
        'Status',
     ],
    'encode' : encode_ConnectionAttemptEvent,
    'decode' : decode_ConnectionAttemptEvent,

}

Parameter_struct['ConnectionCloseEvent'] = {
    'type' : 257,
    'fields':  [ 
        'Type', 
    ],
    'encode' : encode_ConnectionCloseEvent,
    'decode' : decode_ConnectionCloseEvent,

}

Parameter_struct['LLRPStatus'] = {
    'type' : 287,
    'fields':  [ 
        'Type', 
        'StatusCode',
         'ErrorDescription',
         'FieldError',
         'ParameterError',
     ],
    'encode' : encode_LLRPStatus,
    'decode' : decode_LLRPStatus,

}

Parameter_struct['FieldError'] = {
    'type' : 288,
    'fields':  [ 
        'Type', 
        'FieldNum',
         'ErrorCode',
     ],
    'encode' : encode_FieldError,
    'decode' : decode_FieldError,

}

Parameter_struct['ParameterError'] = {
    'type' : 289,
    'fields':  [ 
        'Type', 
        'ParameterType',
         'ErrorCode',
         'FieldError',
         'ParameterError',
     ],
    'encode' : encode_ParameterError,
    'decode' : decode_ParameterError,

}

Parameter_struct['C1G2LLRPCapabilities'] = {
    'type' : 327,
    'fields':  [ 
        'Type', 
        'CanSupportBlockErase',
         'CanSupportBlockWrite',
         'MaxNumSelectFiltersPerQuery',
     ],
    'encode' : encode_C1G2LLRPCapabilities,
    'decode' : decode_C1G2LLRPCapabilities,

}

Parameter_struct['C1G2UHFRFModeTable'] = {
    'type' : 328,
    'fields':  [ 
        'Type', 
        'C1G2UHFRFModeTableEntry',
     ],
    'encode' : encode_C1G2UHFRFModeTable,
    'decode' : decode_C1G2UHFRFModeTable,

}

Parameter_struct['C1G2UHFRFModeTableEntry'] = {
    'type' : 329,
    'fields':  [ 
        'Type', 
        'ModeIdentifier',
         'DRValue',
         'EPCHAGTCConformance',
         'MValue',
         'ForwardLinkModulation',
         'SpectralMaskIndicator',
         'BDRValue',
         'PIEValue',
         'MinTariValue',
         'MaxTariValue',
         'StepTariValue',
     ],
    'encode' : encode_C1G2UHFRFModeTableEntry,
    'decode' : decode_C1G2UHFRFModeTableEntry,

}

Parameter_struct['C1G2InventoryCommand'] = {
    'type' : 330,
    'fields':  [ 
        'Type', 
        'TagInventoryStateAware',
         'C1G2Filter',
         'C1G2RFControl',
         'C1G2SingulationControl',
         'Custom',
     ],
    'encode' : encode_C1G2InventoryCommand,
    'decode' : decode_C1G2InventoryCommand,

}

Parameter_struct['C1G2Filter'] = {
    'type' : 331,
    'fields':  [ 
        'Type', 
        'T',
         'C1G2TagInventoryMask',
         'C1G2TagInventoryStateAwareFilterAction',
         'C1G2TagInventoryStateUnawareFilterAction',
     ],
    'encode' : encode_C1G2Filter,
    'decode' : decode_C1G2Filter,

}

Parameter_struct['C1G2TagInventoryMask'] = {
    'type' : 332,
    'fields':  [ 
        'Type', 
        'MB',
         'Pointer',
         'TagMask',
     ],
    'encode' : encode_C1G2TagInventoryMask,
    'decode' : decode_C1G2TagInventoryMask,

}

Parameter_struct['C1G2TagInventoryStateAwareFilterAction'] = {
    'type' : 333,
    'fields':  [ 
        'Type', 
        'Target',
         'Action',
     ],
    'encode' : encode_C1G2TagInventoryStateAwareFilterAction,
    'decode' : decode_C1G2TagInventoryStateAwareFilterAction,

}

Parameter_struct['C1G2TagInventoryStateUnawareFilterAction'] = {
    'type' : 334,
    'fields':  [ 
        'Type', 
        'Action',
     ],
    'encode' : encode_C1G2TagInventoryStateUnawareFilterAction,
    'decode' : decode_C1G2TagInventoryStateUnawareFilterAction,

}

Parameter_struct['C1G2RFControl'] = {
    'type' : 335,
    'fields':  [ 
        'Type', 
        'ModeIndex',
         'Tari',
     ],
    'encode' : encode_C1G2RFControl,
    'decode' : decode_C1G2RFControl,

}

Parameter_struct['C1G2SingulationControl'] = {
    'type' : 336,
    'fields':  [ 
        'Type', 
        'Session',
         'TagPopulation',
         'TagTransitTime',
         'C1G2TagInventoryStateAwareSingulationAction',
     ],
    'encode' : encode_C1G2SingulationControl,
    'decode' : decode_C1G2SingulationControl,

}

Parameter_struct['C1G2TagInventoryStateAwareSingulationAction'] = {
    'type' : 337,
    'fields':  [ 
        'Type', 
        'I',
         'S',
     ],
    'encode' : encode_C1G2TagInventoryStateAwareSingulationAction,
    'decode' : decode_C1G2TagInventoryStateAwareSingulationAction,

}

Parameter_struct['C1G2TagSpec'] = {
    'type' : 338,
    'fields':  [ 
        'Type', 
        'C1G2TargetTag',
     ],
    'encode' : encode_C1G2TagSpec,
    'decode' : decode_C1G2TagSpec,

}

Parameter_struct['C1G2TargetTag'] = {
    'type' : 339,
    'fields':  [ 
        'Type', 
        'MB',
         'Match',
         'Pointer',
         'TagMask',
         'TagData',
     ],
    'encode' : encode_C1G2TargetTag,
    'decode' : decode_C1G2TargetTag,

}

Parameter_struct['C1G2Read'] = {
    'type' : 341,
    'fields':  [ 
        'Type', 
        'OpSpecID',
         'AccessPassword',
         'MB',
         'WordPointer',
         'WordCount',
     ],
    'encode' : encode_C1G2Read,
    'decode' : decode_C1G2Read,

}

Parameter_struct['C1G2Write'] = {
    'type' : 342,
    'fields':  [ 
        'Type', 
        'OpSpecID',
         'AccessPassword',
         'MB',
         'WordPointer',
         'WriteData',
     ],
    'encode' : encode_C1G2Write,
    'decode' : decode_C1G2Write,

}

Parameter_struct['C1G2Kill'] = {
    'type' : 343,
    'fields':  [ 
        'Type', 
        'OpSpecID',
         'KillPassword',
     ],
    'encode' : encode_C1G2Kill,
    'decode' : decode_C1G2Kill,

}

Parameter_struct['C1G2Lock'] = {
    'type' : 344,
    'fields':  [ 
        'Type', 
        'OpSpecID',
         'AccessPassword',
         'C1G2LockPayload',
     ],
    'encode' : encode_C1G2Lock,
    'decode' : decode_C1G2Lock,

}

Parameter_struct['C1G2LockPayload'] = {
    'type' : 345,
    'fields':  [ 
        'Type', 
        'Privilege',
         'DataField',
     ],
    'encode' : encode_C1G2LockPayload,
    'decode' : decode_C1G2LockPayload,

}

Parameter_struct['C1G2BlockErase'] = {
    'type' : 346,
    'fields':  [ 
        'Type', 
        'OpSpecID',
         'AccessPassword',
         'MB',
         'WordPointer',
         'WordCount',
     ],
    'encode' : encode_C1G2BlockErase,
    'decode' : decode_C1G2BlockErase,

}

Parameter_struct['C1G2BlockWrite'] = {
    'type' : 347,
    'fields':  [ 
        'Type', 
        'OpSpecID',
         'AccessPassword',
         'MB',
         'WordPointer',
         'WriteData',
     ],
    'encode' : encode_C1G2BlockWrite,
    'decode' : decode_C1G2BlockWrite,

}

Parameter_struct['C1G2EPCMemorySelector'] = {
    'type' : 348,
    'fields':  [ 
        'Type', 
        'EnableCRC',
         'EnablePCBits',
     ],
    'encode' : encode_C1G2EPCMemorySelector,
    'decode' : decode_C1G2EPCMemorySelector,

}

Parameter_struct['C1G2_PC'] = {
    'type' : 12,
    'fields':  [ 
        'Type', 
        'PC_Bits',
     ],
    'encode' : encode_C1G2_PC,
    'decode' : decode_C1G2_PC,

}

Parameter_struct['C1G2_CRC'] = {
    'type' : 11,
    'fields':  [ 
        'Type', 
        'CRC',
     ],
    'encode' : encode_C1G2_CRC,
    'decode' : decode_C1G2_CRC,

}

Parameter_struct['C1G2SingulationDetails'] = {
    'type' : 18,
    'fields':  [ 
        'Type', 
        'NumCollisionSlots',
         'NumEmptySlots',
     ],
    'encode' : encode_C1G2SingulationDetails,
    'decode' : decode_C1G2SingulationDetails,

}

Parameter_struct['C1G2ReadOpSpecResult'] = {
    'type' : 349,
    'fields':  [ 
        'Type', 
        'Result',
         'OpSpecID',
         'ReadData',
     ],
    'encode' : encode_C1G2ReadOpSpecResult,
    'decode' : decode_C1G2ReadOpSpecResult,

}

Parameter_struct['C1G2WriteOpSpecResult'] = {
    'type' : 350,
    'fields':  [ 
        'Type', 
        'Result',
         'OpSpecID',
         'NumWordsWritten',
     ],
    'encode' : encode_C1G2WriteOpSpecResult,
    'decode' : decode_C1G2WriteOpSpecResult,

}

Parameter_struct['C1G2KillOpSpecResult'] = {
    'type' : 351,
    'fields':  [ 
        'Type', 
        'Result',
         'OpSpecID',
     ],
    'encode' : encode_C1G2KillOpSpecResult,
    'decode' : decode_C1G2KillOpSpecResult,

}

Parameter_struct['C1G2LockOpSpecResult'] = {
    'type' : 352,
    'fields':  [ 
        'Type', 
        'Result',
         'OpSpecID',
     ],
    'encode' : encode_C1G2LockOpSpecResult,
    'decode' : decode_C1G2LockOpSpecResult,

}

Parameter_struct['C1G2BlockEraseOpSpecResult'] = {
    'type' : 353,
    'fields':  [ 
        'Type', 
        'Result',
         'OpSpecID',
     ],
    'encode' : encode_C1G2BlockEraseOpSpecResult,
    'decode' : decode_C1G2BlockEraseOpSpecResult,

}

Parameter_struct['C1G2BlockWriteOpSpecResult'] = {
    'type' : 354,
    'fields':  [ 
        'Type', 
        'Result',
         'OpSpecID',
         'NumWordsWritten',
     ],
    'encode' : encode_C1G2BlockWriteOpSpecResult,
    'decode' : decode_C1G2BlockWriteOpSpecResult,

}

Message_struct['CUSTOM_MESSAGE'] = {
    'type' :  1023,
    'fields':  [ 'deviceSN', 'Ver', 'Type', 'ID',  
    'VendorIdentifier',
     'MessageSubtype',
     'Data',
     ],
    'encode' : encode_CUSTOM_MESSAGE,
    'decode' : decode_CUSTOM_MESSAGE,

}

Message_struct['GET_READER_CAPABILITIES'] = {
    'type' :  1,
    'fields':  [ 'deviceSN', 'Ver', 'Type', 'ID',  
    'RequestedData',
     'Custom',
     ],
    'encode' : encode_GET_READER_CAPABILITIES,
    'decode' : decode_GET_READER_CAPABILITIES,

}

Message_struct['GET_READER_CAPABILITIES_RESPONSE'] = {
    'type' :  11,
    'fields':  [ 'deviceSN', 'Ver', 'Type', 'ID',  
    'LLRPStatus',
     'GeneralDeviceCapabilities',
     'LLRPCapabilities',
     'RegulatoryCapabilities',
     'AirProtocolLLRPCapabilities',
     'Custom',
     ],
    'encode' : encode_GET_READER_CAPABILITIES_RESPONSE,
    'decode' : decode_GET_READER_CAPABILITIES_RESPONSE,

}

Message_struct['ADD_ROSPEC'] = {
    'type' :  20,
    'fields':  [ 'deviceSN', 'Ver', 'Type', 'ID',  
    'ROSpec',
     ],
    'encode' : encode_ADD_ROSPEC,
    'decode' : decode_ADD_ROSPEC,

}

Message_struct['ADD_ROSPEC_RESPONSE'] = {
    'type' :  30,
    'fields':  [ 'deviceSN', 'Ver', 'Type', 'ID',  
    'LLRPStatus',
     ],
    'encode' : encode_ADD_ROSPEC_RESPONSE,
    'decode' : decode_ADD_ROSPEC_RESPONSE,

}

Message_struct['DELETE_ROSPEC'] = {
    'type' :  21,
    'fields':  [ 'deviceSN', 'Ver', 'Type', 'ID',  
    'ROSpecID',
     ],
    'encode' : encode_DELETE_ROSPEC,
    'decode' : decode_DELETE_ROSPEC,

}

Message_struct['DELETE_ROSPEC_RESPONSE'] = {
    'type' :  31,
    'fields':  [ 'deviceSN', 'Ver', 'Type', 'ID',  
    'LLRPStatus',
     ],
    'encode' : encode_DELETE_ROSPEC_RESPONSE,
    'decode' : decode_DELETE_ROSPEC_RESPONSE,

}

Message_struct['START_ROSPEC'] = {
    'type' :  22,
    'fields':  [ 'deviceSN', 'Ver', 'Type', 'ID',  
    'ROSpecID',
     ],
    'encode' : encode_START_ROSPEC,
    'decode' : decode_START_ROSPEC,

}

Message_struct['START_ROSPEC_RESPONSE'] = {
    'type' :  32,
    'fields':  [ 'deviceSN', 'Ver', 'Type', 'ID',  
    'LLRPStatus',
     ],
    'encode' : encode_START_ROSPEC_RESPONSE,
    'decode' : decode_START_ROSPEC_RESPONSE,

}

Message_struct['STOP_ROSPEC'] = {
    'type' :  23,
    'fields':  [ 'deviceSN', 'Ver', 'Type', 'ID',  
    'ROSpecID',
     ],
    'encode' : encode_STOP_ROSPEC,
    'decode' : decode_STOP_ROSPEC,

}

Message_struct['STOP_ROSPEC_RESPONSE'] = {
    'type' :  33,
    'fields':  [ 'deviceSN', 'Ver', 'Type', 'ID',  
    'LLRPStatus',
     ],
    'encode' : encode_STOP_ROSPEC_RESPONSE,
    'decode' : decode_STOP_ROSPEC_RESPONSE,

}

Message_struct['ENABLE_ROSPEC'] = {
    'type' :  24,
    'fields':  [ 'deviceSN', 'Ver', 'Type', 'ID',  
    'ROSpecID',
     ],
    'encode' : encode_ENABLE_ROSPEC,
    'decode' : decode_ENABLE_ROSPEC,

}

Message_struct['ENABLE_ROSPEC_RESPONSE'] = {
    'type' :  34,
    'fields':  [ 'deviceSN', 'Ver', 'Type', 'ID',  
    'LLRPStatus',
     ],
    'encode' : encode_ENABLE_ROSPEC_RESPONSE,
    'decode' : decode_ENABLE_ROSPEC_RESPONSE,

}

Message_struct['DISABLE_ROSPEC'] = {
    'type' :  25,
    'fields':  [ 'deviceSN', 'Ver', 'Type', 'ID',  
    'ROSpecID',
     ],
    'encode' : encode_DISABLE_ROSPEC,
    'decode' : decode_DISABLE_ROSPEC,

}

Message_struct['DISABLE_ROSPEC_RESPONSE'] = {
    'type' :  35,
    'fields':  [ 'deviceSN', 'Ver', 'Type', 'ID',  
    'LLRPStatus',
     ],
    'encode' : encode_DISABLE_ROSPEC_RESPONSE,
    'decode' : decode_DISABLE_ROSPEC_RESPONSE,

}

Message_struct['GET_ROSPECS'] = {
    'type' :  26,
    'fields':  [ 'deviceSN', 'Ver', 'Type', 'ID',  
    ],
    'encode' : encode_GET_ROSPECS,
    'decode' : decode_GET_ROSPECS,

}

Message_struct['GET_ROSPECS_RESPONSE'] = {
    'type' :  36,
    'fields':  [ 'deviceSN', 'Ver', 'Type', 'ID',  
    'LLRPStatus',
     'ROSpec',
     ],
    'encode' : encode_GET_ROSPECS_RESPONSE,
    'decode' : decode_GET_ROSPECS_RESPONSE,

}

Message_struct['ADD_ACCESSSPEC'] = {
    'type' :  40,
    'fields':  [ 'deviceSN', 'Ver', 'Type', 'ID',  
    'AccessSpec',
     ],
    'encode' : encode_ADD_ACCESSSPEC,
    'decode' : decode_ADD_ACCESSSPEC,

}

Message_struct['ADD_ACCESSSPEC_RESPONSE'] = {
    'type' :  50,
    'fields':  [ 'deviceSN', 'Ver', 'Type', 'ID',  
    'LLRPStatus',
     ],
    'encode' : encode_ADD_ACCESSSPEC_RESPONSE,
    'decode' : decode_ADD_ACCESSSPEC_RESPONSE,

}

Message_struct['DELETE_ACCESSSPEC'] = {
    'type' :  41,
    'fields':  [ 'deviceSN', 'Ver', 'Type', 'ID',  
    'AccessSpecID',
     ],
    'encode' : encode_DELETE_ACCESSSPEC,
    'decode' : decode_DELETE_ACCESSSPEC,

}

Message_struct['DELETE_ACCESSSPEC_RESPONSE'] = {
    'type' :  51,
    'fields':  [ 'deviceSN', 'Ver', 'Type', 'ID',  
    'LLRPStatus',
     ],
    'encode' : encode_DELETE_ACCESSSPEC_RESPONSE,
    'decode' : decode_DELETE_ACCESSSPEC_RESPONSE,

}

Message_struct['ENABLE_ACCESSSPEC'] = {
    'type' :  42,
    'fields':  [ 'deviceSN', 'Ver', 'Type', 'ID',  
    'AccessSpecID',
     ],
    'encode' : encode_ENABLE_ACCESSSPEC,
    'decode' : decode_ENABLE_ACCESSSPEC,

}

Message_struct['ENABLE_ACCESSSPEC_RESPONSE'] = {
    'type' :  52,
    'fields':  [ 'deviceSN', 'Ver', 'Type', 'ID',  
    'LLRPStatus',
     ],
    'encode' : encode_ENABLE_ACCESSSPEC_RESPONSE,
    'decode' : decode_ENABLE_ACCESSSPEC_RESPONSE,

}

Message_struct['DISABLE_ACCESSSPEC'] = {
    'type' :  43,
    'fields':  [ 'deviceSN', 'Ver', 'Type', 'ID',  
    'AccessSpecID',
     ],
    'encode' : encode_DISABLE_ACCESSSPEC,
    'decode' : decode_DISABLE_ACCESSSPEC,

}

Message_struct['DISABLE_ACCESSSPEC_RESPONSE'] = {
    'type' :  53,
    'fields':  [ 'deviceSN', 'Ver', 'Type', 'ID',  
    'LLRPStatus',
     ],
    'encode' : encode_DISABLE_ACCESSSPEC_RESPONSE,
    'decode' : decode_DISABLE_ACCESSSPEC_RESPONSE,

}

Message_struct['GET_ACCESSSPECS'] = {
    'type' :  44,
    'fields':  [ 'deviceSN', 'Ver', 'Type', 'ID',  
    ],
    'encode' : encode_GET_ACCESSSPECS,
    'decode' : decode_GET_ACCESSSPECS,

}

Message_struct['GET_ACCESSSPECS_RESPONSE'] = {
    'type' :  54,
    'fields':  [ 'deviceSN', 'Ver', 'Type', 'ID',  
    'LLRPStatus',
     'AccessSpec',
     ],
    'encode' : encode_GET_ACCESSSPECS_RESPONSE,
    'decode' : decode_GET_ACCESSSPECS_RESPONSE,

}

Message_struct['GET_READER_CONFIG'] = {
    'type' :  2,
    'fields':  [ 'deviceSN', 'Ver', 'Type', 'ID',  
    'AntennaID',
     'RequestedData',
     'GPIPortNum',
     'GPOPortNum',
     'Custom',
     ],
    'encode' : encode_GET_READER_CONFIG,
    'decode' : decode_GET_READER_CONFIG,

}

Message_struct['GET_READER_CONFIG_RESPONSE'] = {
    'type' :  12,
    'fields':  [ 'deviceSN', 'Ver', 'Type', 'ID',  
    'LLRPStatus',
     'Identification',
     'AntennaProperties',
     'AntennaConfiguration',
     'ReaderEventNotificationSpec',
     'ROReportSpec',
     'AccessReportSpec',
     'LLRPConfigurationStateValue',
     'KeepaliveSpec',
     'GPIPortCurrentState',
     'GPOWriteData',
     'EventsAndReports',
     'Custom',
     ],
    'encode' : encode_GET_READER_CONFIG_RESPONSE,
    'decode' : decode_GET_READER_CONFIG_RESPONSE,

}

Message_struct['SET_READER_CONFIG'] = {
    'type' :  3,
    'fields':  [ 'deviceSN', 'Ver', 'Type', 'ID',  
    'ResetToFactoryDefault',
     'ReaderEventNotificationSpec',
     'AntennaProperties',
     'AntennaConfiguration',
     'ROReportSpec',
     'AccessReportSpec',
     'KeepaliveSpec',
     'GPOWriteData',
     'GPIPortCurrentState',
     'EventsAndReports',
     'Custom',
     ],
    'encode' : encode_SET_READER_CONFIG,
    'decode' : decode_SET_READER_CONFIG,

}

Message_struct['SET_READER_CONFIG_RESPONSE'] = {
    'type' :  13,
    'fields':  [ 'deviceSN', 'Ver', 'Type', 'ID',  
    'LLRPStatus',
     ],
    'encode' : encode_SET_READER_CONFIG_RESPONSE,
    'decode' : decode_SET_READER_CONFIG_RESPONSE,

}

Message_struct['CLOSE_CONNECTION'] = {
    'type' :  14,
    'fields':  [ 'deviceSN', 'Ver', 'Type', 'ID',  
    ],
    'encode' : encode_CLOSE_CONNECTION,
    'decode' : decode_CLOSE_CONNECTION,

}

Message_struct['CLOSE_CONNECTION_RESPONSE'] = {
    'type' :  4,
    'fields':  [ 'deviceSN', 'Ver', 'Type', 'ID',  
    'LLRPStatus',
     ],
    'encode' : encode_CLOSE_CONNECTION_RESPONSE,
    'decode' : decode_CLOSE_CONNECTION_RESPONSE,

}

Message_struct['GET_REPORT'] = {
    'type' :  60,
    'fields':  [ 'deviceSN', 'Ver', 'Type', 'ID',  
    ],
    'encode' : encode_GET_REPORT,
    'decode' : decode_GET_REPORT,

}

Message_struct['RO_ACCESS_REPORT'] = {
    'type' :  61,
    'fields':  [ 'deviceSN', 'Ver', 'Type', 'ID',  
    'TagReportData',
     'RFSurveyReportData',
     'Custom',
     ],
    'encode' : encode_RO_ACCESS_REPORT,
    'decode' : decode_RO_ACCESS_REPORT,

}

Message_struct['KEEPALIVE'] = {
    'type' :  62,
    'fields':  [ 'deviceSN', 'Ver', 'Type', 'ID',  
    ],
    'encode' : encode_KEEPALIVE,
    'decode' : decode_KEEPALIVE,

}

Message_struct['KEEPALIVE_ACK'] = {
    'type' :  72,
    'fields':  [ 'deviceSN', 'Ver', 'Type', 'ID',  
    ],
    'encode' : encode_KEEPALIVE_ACK,
    'decode' : decode_KEEPALIVE_ACK,

}

Message_struct['READER_EVENT_NOTIFICATION'] = {
    'type' :  63,
    'fields':  [ 'deviceSN', 'Ver', 'Type', 'ID',  
    'ReaderEventNotificationData',
     ],
    'encode' : encode_READER_EVENT_NOTIFICATION,
    'decode' : decode_READER_EVENT_NOTIFICATION,

}

Message_struct['ENABLE_EVENTS_AND_REPORTS'] = {
    'type' :  64,
    'fields':  [ 'deviceSN', 'Ver', 'Type', 'ID',  
    ],
    'encode' : encode_ENABLE_EVENTS_AND_REPORTS,
    'decode' : decode_ENABLE_EVENTS_AND_REPORTS,

}

Message_struct['ERROR_MESSAGE'] = {
    'type' :  100,
    'fields':  [ 'deviceSN', 'Ver', 'Type', 'ID',  
    'LLRPStatus',
     ],
    'encode' : encode_ERROR_MESSAGE,
    'decode' : decode_ERROR_MESSAGE,

}

def encode_UTCTimestamp(par):
    data = ''
    data += struct.pack("!Q", par["Microseconds"])
    type = Parameter_struct['UTCTimestamp']['type']
    data = struct.pack('!HH', type, (4+len(data))) + data
    return data

def encode_Uptime(par):
    data = ''
    data += struct.pack("!Q", par["Microseconds"])
    type = Parameter_struct['Uptime']['type']
    data = struct.pack('!HH', type, (4+len(data))) + data
    return data

def encode_Custom(par):
    data = ''
    data += struct.pack("!I", par["VendorIdentifier"])
    data += struct.pack("!I", par["ParameterSubtype"])
    Data = par["Data"]
    data += struct.pack('!H', len(Data))
    for x in Data:
        data += struct.pack('!s', x)

    type = Parameter_struct['Custom']['type']
    data = struct.pack('!HH', type, (4+len(data))) + data
    return data

def encode_GeneralDeviceCapabilities(par):
    data = ''
    data += struct.pack("!H", par["MaxNumberOfAntennaSupported"])
    e = par["CanSetAntennaProperties"]<<7|par["HasUTCClockCapability"]<<6|0
    data += struct.pack("!B", e)
    data += struct.pack("!I", par["DeviceManufacturerName"])
    data += struct.pack("!I", par["ModelName"])
    ReaderFirmwareVersion = par["ReaderFirmwareVersion"]
    data += struct.pack('!H', len(ReaderFirmwareVersion))
    for x in ReaderFirmwareVersion:
        data += struct.pack('!B', x)

    for x in par["ReceiveSensitivityTableEntry"]:
        data += encode("ReceiveSensitivityTableEntry")(x)
    if par.has_key("PerAntennaReceiveSensitivityRange"):
        for x in par["PerAntennaReceiveSensitivityRange"]:
            data += encode("PerAntennaReceiveSensitivityRange")(x)
    data += encode("GPIOCapabilities")(par["GPIOCapabilities"])
    for x in par["PerAntennaAirProtocol"]:
        data += encode("PerAntennaAirProtocol")(x)
    type = Parameter_struct['GeneralDeviceCapabilities']['type']
    data = struct.pack('!HH', type, (4+len(data))) + data
    return data

def encode_ReceiveSensitivityTableEntry(par):
    data = ''
    data += struct.pack("!H", par["Index"])
    data += struct.pack("!h", par["ReceiveSensitivityValue"])
    type = Parameter_struct['ReceiveSensitivityTableEntry']['type']
    data = struct.pack('!HH', type, (4+len(data))) + data
    return data

def encode_PerAntennaReceiveSensitivityRange(par):
    data = ''
    data += struct.pack("!H", par["AntennaID"])
    data += struct.pack("!H", par["ReceiveSensitivityIndexMin"])
    data += struct.pack("!H", par["ReceiveSensitivityIndexMax"])
    type = Parameter_struct['PerAntennaReceiveSensitivityRange']['type']
    data = struct.pack('!HH', type, (4+len(data))) + data
    return data

def encode_PerAntennaAirProtocol(par):
    data = ''
    data += struct.pack("!H", par["AntennaID"])
    ProtocolID = par["ProtocolID"]
    data += struct.pack('!H', len(ProtocolID))
    for x in ProtocolID:
        data += struct.pack('!B', x)

    type = Parameter_struct['PerAntennaAirProtocol']['type']
    data = struct.pack('!HH', type, (4+len(data))) + data
    return data

def encode_GPIOCapabilities(par):
    data = ''
    data += struct.pack("!H", par["NumGPIs"])
    data += struct.pack("!H", par["NumGPOs"])
    type = Parameter_struct['GPIOCapabilities']['type']
    data = struct.pack('!HH', type, (4+len(data))) + data
    return data

def encode_LLRPCapabilities(par):
    data = ''
    e = par["CanDoRFSurvey"]<<7|par["CanReportBufferFillWarning"]<<6|par["SupportsClientRequestOpSpec"]<<5|par["CanDoTagInventoryStateAwareSingulation"]<<4|par["SupportsEventAndReportHolding"]<<3|0
    data += struct.pack("!B", e)
    data += struct.pack("!B", par["MaxNumPriorityLevelsSupported"])
    data += struct.pack("!H", par["ClientRequestOpSpecTimeout"])
    data += struct.pack("!I", par["MaxNumROSpecs"])
    data += struct.pack("!I", par["MaxNumSpecsPerROSpec"])
    data += struct.pack("!I", par["MaxNumInventoryParameterSpecsPerAISpec"])
    data += struct.pack("!I", par["MaxNumAccessSpecs"])
    data += struct.pack("!I", par["MaxNumOpSpecsPerAccessSpec"])
    type = Parameter_struct['LLRPCapabilities']['type']
    data = struct.pack('!HH', type, (4+len(data))) + data
    return data

def encode_RegulatoryCapabilities(par):
    data = ''
    data += struct.pack("!H", par["CountryCode"])
    data += struct.pack("!H", CommunicationsStandard_Name2Type[par["CommunicationsStandard"]])
    if par.has_key("UHFBandCapabilities"):
        data += encode("UHFBandCapabilities")(par["UHFBandCapabilities"])
    if par.has_key("Custom"):
        for x in par["Custom"]:
            data += encode("Custom")(x)
    type = Parameter_struct['RegulatoryCapabilities']['type']
    data = struct.pack('!HH', type, (4+len(data))) + data
    return data

def encode_UHFBandCapabilities(par):
    data = ''
    for x in par["TransmitPowerLevelTableEntry"]:
        data += encode("TransmitPowerLevelTableEntry")(x)
    data += encode("FrequencyInformation")(par["FrequencyInformation"])
    if par.has_key("C1G2UHFRFModeTable"):
        for x in par["C1G2UHFRFModeTable"]:
            data += encode("C1G2UHFRFModeTable")(x)
    type = Parameter_struct['UHFBandCapabilities']['type']
    data = struct.pack('!HH', type, (4+len(data))) + data
    return data

def encode_TransmitPowerLevelTableEntry(par):
    data = ''
    data += struct.pack("!H", par["Index"])
    data += struct.pack("!h", par["TransmitPowerValue"])
    type = Parameter_struct['TransmitPowerLevelTableEntry']['type']
    data = struct.pack('!HH', type, (4+len(data))) + data
    return data

def encode_FrequencyInformation(par):
    data = ''
    e = par["Hopping"]<<7|0
    data += struct.pack("!B", e)
    if par.has_key("FrequencyHopTable"):
        for x in par["FrequencyHopTable"]:
            data += encode("FrequencyHopTable")(x)
    if par.has_key("FixedFrequencyTable"):
        data += encode("FixedFrequencyTable")(par["FixedFrequencyTable"])
    type = Parameter_struct['FrequencyInformation']['type']
    data = struct.pack('!HH', type, (4+len(data))) + data
    return data

def encode_FrequencyHopTable(par):
    data = ''
    data += struct.pack("!B", par["HopTableID"])
    Frequency = par["Frequency"]
    data += struct.pack('!H', len(Frequency))
    for x in Frequency:
        data += struct.pack('!I', x)

    type = Parameter_struct['FrequencyHopTable']['type']
    data = struct.pack('!HH', type, (4+len(data))) + data
    return data

def encode_FixedFrequencyTable(par):
    data = ''
    Frequency = par["Frequency"]
    data += struct.pack('!H', len(Frequency))
    for x in Frequency:
        data += struct.pack('!I', x)

    type = Parameter_struct['FixedFrequencyTable']['type']
    data = struct.pack('!HH', type, (4+len(data))) + data
    return data

def encode_ROSpec(par):
    data = ''
    data += struct.pack("!I", par["ROSpecID"])
    data += struct.pack("!B", par["Priority"])
    data += struct.pack("!B", ROSpecState_Name2Type[par["CurrentState"]])
    data += encode("ROBoundarySpec")(par["ROBoundarySpec"])
    if par.has_key("AISpec"):
        for x in par["AISpec"]:
            data += encode("AISpec")(x)
    if par.has_key("RFSurveySpec"):
        for x in par["RFSurveySpec"]:
            data += encode("RFSurveySpec")(x)
    if par.has_key("Custom"):
        for x in par["Custom"]:
            data += encode("Custom")(x)
    if par.has_key("ROReportSpec"):
        data += encode("ROReportSpec")(par["ROReportSpec"])
    type = Parameter_struct['ROSpec']['type']
    data = struct.pack('!HH', type, (4+len(data))) + data
    return data

def encode_ROBoundarySpec(par):
    data = ''
    data += encode("ROSpecStartTrigger")(par["ROSpecStartTrigger"])
    data += encode("ROSpecStopTrigger")(par["ROSpecStopTrigger"])
    type = Parameter_struct['ROBoundarySpec']['type']
    data = struct.pack('!HH', type, (4+len(data))) + data
    return data

def encode_ROSpecStartTrigger(par):
    data = ''
    data += struct.pack("!B", ROSpecStartTriggerType_Name2Type[par["ROSpecStartTriggerType"]])
    if par.has_key("PeriodicTriggerValue"):
        data += encode("PeriodicTriggerValue")(par["PeriodicTriggerValue"])
    if par.has_key("GPITriggerValue"):
        data += encode("GPITriggerValue")(par["GPITriggerValue"])
    type = Parameter_struct['ROSpecStartTrigger']['type']
    data = struct.pack('!HH', type, (4+len(data))) + data
    return data

def encode_PeriodicTriggerValue(par):
    data = ''
    data += struct.pack("!I", par["Offset"])
    data += struct.pack("!I", par["Period"])
    if par.has_key("UTCTimestamp"):
        data += encode("UTCTimestamp")(par["UTCTimestamp"])
    type = Parameter_struct['PeriodicTriggerValue']['type']
    data = struct.pack('!HH', type, (4+len(data))) + data
    return data

def encode_GPITriggerValue(par):
    data = ''
    data += struct.pack("!H", par["GPIPortNum"])
    e = par["GPIEvent"]<<7|0
    data += struct.pack("!B", e)
    data += struct.pack("!I", par["Timeout"])
    type = Parameter_struct['GPITriggerValue']['type']
    data = struct.pack('!HH', type, (4+len(data))) + data
    return data

def encode_ROSpecStopTrigger(par):
    data = ''
    data += struct.pack("!B", ROSpecStopTriggerType_Name2Type[par["ROSpecStopTriggerType"]])
    data += struct.pack("!I", par["DurationTriggerValue"])
    if par.has_key("GPITriggerValue"):
        data += encode("GPITriggerValue")(par["GPITriggerValue"])
    type = Parameter_struct['ROSpecStopTrigger']['type']
    data = struct.pack('!HH', type, (4+len(data))) + data
    return data

def encode_AISpec(par):
    data = ''
    AntennaIDs = par["AntennaIDs"]
    data += struct.pack('!H', len(AntennaIDs))
    for x in AntennaIDs:
        data += struct.pack('!H', x)

    data += encode("AISpecStopTrigger")(par["AISpecStopTrigger"])
    for x in par["InventoryParameterSpec"]:
        data += encode("InventoryParameterSpec")(x)
    if par.has_key("Custom"):
        for x in par["Custom"]:
            data += encode("Custom")(x)
    type = Parameter_struct['AISpec']['type']
    data = struct.pack('!HH', type, (4+len(data))) + data
    return data

def encode_AISpecStopTrigger(par):
    data = ''
    data += struct.pack("!B", AISpecStopTriggerType_Name2Type[par["AISpecStopTriggerType"]])
    data += struct.pack("!I", par["DurationTrigger"])
    if par.has_key("GPITriggerValue"):
        data += encode("GPITriggerValue")(par["GPITriggerValue"])
    if par.has_key("TagObservationTrigger"):
        data += encode("TagObservationTrigger")(par["TagObservationTrigger"])
    type = Parameter_struct['AISpecStopTrigger']['type']
    data = struct.pack('!HH', type, (4+len(data))) + data
    return data

def encode_TagObservationTrigger(par):
    data = ''
    data += struct.pack("!B", TagObservationTriggerType_Name2Type[par["TriggerType"]])
    data += struct.pack("!H", par["NumberOfTags"])
    data += struct.pack("!H", par["NumberOfAttempts"])
    data += struct.pack("!H", par["T"])
    data += struct.pack("!I", par["Timeout"])
    type = Parameter_struct['TagObservationTrigger']['type']
    data = struct.pack('!HH', type, (4+len(data))) + data
    return data

def encode_InventoryParameterSpec(par):
    data = ''
    data += struct.pack("!H", par["InventoryParameterSpecID"])
    data += struct.pack("!B", AirProtocols_Name2Type[par["ProtocolID"]])
    if par.has_key("AntennaConfiguration"):
        for x in par["AntennaConfiguration"]:
            data += encode("AntennaConfiguration")(x)
    if par.has_key("Custom"):
        for x in par["Custom"]:
            data += encode("Custom")(x)
    type = Parameter_struct['InventoryParameterSpec']['type']
    data = struct.pack('!HH', type, (4+len(data))) + data
    return data

def encode_RFSurveySpec(par):
    data = ''
    data += struct.pack("!H", par["AntennaID"])
    data += struct.pack("!I", par["StartFrequency"])
    data += struct.pack("!I", par["EndFrequency"])
    data += encode("RFSurveySpecStopTrigger")(par["RFSurveySpecStopTrigger"])
    if par.has_key("Custom"):
        for x in par["Custom"]:
            data += encode("Custom")(x)
    type = Parameter_struct['RFSurveySpec']['type']
    data = struct.pack('!HH', type, (4+len(data))) + data
    return data

def encode_RFSurveySpecStopTrigger(par):
    data = ''
    data += struct.pack("!B", RFSurveySpecStopTriggerType_Name2Type[par["StopTriggerType"]])
    data += struct.pack("!I", par["DurationPeriod"])
    data += struct.pack("!I", par["N"])
    type = Parameter_struct['RFSurveySpecStopTrigger']['type']
    data = struct.pack('!HH', type, (4+len(data))) + data
    return data

def encode_AccessSpec(par):
    data = ''
    data += struct.pack("!I", par["AccessSpecID"])
    data += struct.pack("!H", par["AntennaID"])
    data += struct.pack("!B", AirProtocols_Name2Type[par["ProtocolID"]])
    e = AccessSpecState_Name2Type[par["CurrentState"]]<<7|0
    data += struct.pack("!B", e)
    data += struct.pack("!I", par["ROSpecID"])
    data += encode("AccessSpecStopTrigger")(par["AccessSpecStopTrigger"])
    data += encode("AccessCommand")(par["AccessCommand"])
    if par.has_key("AccessReportSpec"):
        data += encode("AccessReportSpec")(par["AccessReportSpec"])
    if par.has_key("Custom"):
        for x in par["Custom"]:
            data += encode("Custom")(x)
    type = Parameter_struct['AccessSpec']['type']
    data = struct.pack('!HH', type, (4+len(data))) + data
    return data

def encode_AccessSpecStopTrigger(par):
    data = ''
    data += struct.pack("!B", AccessSpecStopTriggerType_Name2Type[par["AccessSpecStopTrigger"]])
    data += struct.pack("!H", par["OperationCountValue"])
    type = Parameter_struct['AccessSpecStopTrigger']['type']
    data = struct.pack('!HH', type, (4+len(data))) + data
    return data

def encode_AccessCommand(par):
    data = ''
    if par.has_key("C1G2TagSpec"):
        data += encode("C1G2TagSpec")(par["C1G2TagSpec"])
    if par.has_key("C1G2Read"):
        for x in par["C1G2Read"]:
            data += encode("C1G2Read")(x)
    if par.has_key("C1G2Write"):
        for x in par["C1G2Write"]:
            data += encode("C1G2Write")(x)
    if par.has_key("C1G2Kill"):
        for x in par["C1G2Kill"]:
            data += encode("C1G2Kill")(x)
    if par.has_key("C1G2Lock"):
        for x in par["C1G2Lock"]:
            data += encode("C1G2Lock")(x)
    if par.has_key("C1G2BlockErase"):
        for x in par["C1G2BlockErase"]:
            data += encode("C1G2BlockErase")(x)
    if par.has_key("C1G2BlockWrite"):
        for x in par["C1G2BlockWrite"]:
            data += encode("C1G2BlockWrite")(x)
    if par.has_key("Custom"):
        for x in par["Custom"]:
            data += encode("Custom")(x)
    if par.has_key("Custom"):
        for x in par["Custom"]:
            data += encode("Custom")(x)
    type = Parameter_struct['AccessCommand']['type']
    data = struct.pack('!HH', type, (4+len(data))) + data
    return data

def encode_LLRPConfigurationStateValue(par):
    data = ''
    data += struct.pack("!I", par["LLRPConfigurationStateValue"])
    type = Parameter_struct['LLRPConfigurationStateValue']['type']
    data = struct.pack('!HH', type, (4+len(data))) + data
    return data

def encode_Identification(par):
    data = ''
    data += struct.pack("!B", IdentificationType_Name2Type[par["IDType"]])
    ReaderID = par["ReaderID"]
    data += struct.pack('!H', len(ReaderID))
    for x in ReaderID:
        data += struct.pack('!B', x)

    type = Parameter_struct['Identification']['type']
    data = struct.pack('!HH', type, (4+len(data))) + data
    return data

def encode_GPOWriteData(par):
    data = ''
    data += struct.pack("!H", par["GPOPortNumber"])
    e = par["GPOData"]<<7|0
    data += struct.pack("!B", e)
    type = Parameter_struct['GPOWriteData']['type']
    data = struct.pack('!HH', type, (4+len(data))) + data
    return data

def encode_KeepaliveSpec(par):
    data = ''
    data += struct.pack("!B", KeepaliveTriggerType_Name2Type[par["KeepaliveTriggerType"]])
    data += struct.pack("!I", par["PeriodicTriggerValue"])
    type = Parameter_struct['KeepaliveSpec']['type']
    data = struct.pack('!HH', type, (4+len(data))) + data
    return data

def encode_AntennaProperties(par):
    data = ''
    e = par["AntennaConnected"]<<7|0
    data += struct.pack("!B", e)
    data += struct.pack("!H", par["AntennaID"])
    data += struct.pack("!h", par["AntennaGain"])
    type = Parameter_struct['AntennaProperties']['type']
    data = struct.pack('!HH', type, (4+len(data))) + data
    return data

def encode_AntennaConfiguration(par):
    data = ''
    data += struct.pack("!H", par["AntennaID"])
    if par.has_key("RFReceiver"):
        data += encode("RFReceiver")(par["RFReceiver"])
    if par.has_key("RFTransmitter"):
        data += encode("RFTransmitter")(par["RFTransmitter"])
    if par.has_key("C1G2InventoryCommand"):
        for x in par["C1G2InventoryCommand"]:
            data += encode("C1G2InventoryCommand")(x)
    type = Parameter_struct['AntennaConfiguration']['type']
    data = struct.pack('!HH', type, (4+len(data))) + data
    return data

def encode_RFReceiver(par):
    data = ''
    data += struct.pack("!H", par["ReceiverSensitivity"])
    type = Parameter_struct['RFReceiver']['type']
    data = struct.pack('!HH', type, (4+len(data))) + data
    return data

def encode_RFTransmitter(par):
    data = ''
    data += struct.pack("!H", par["HopTableID"])
    data += struct.pack("!H", par["ChannelIndex"])
    data += struct.pack("!H", par["TransmitPower"])
    type = Parameter_struct['RFTransmitter']['type']
    data = struct.pack('!HH', type, (4+len(data))) + data
    return data

def encode_GPIPortCurrentState(par):
    data = ''
    data += struct.pack("!H", par["GPIPortNum"])
    e = par["Config"]<<7|0
    data += struct.pack("!B", e)
    data += struct.pack("!B", GPIPortState_Name2Type[par["State"]])
    type = Parameter_struct['GPIPortCurrentState']['type']
    data = struct.pack('!HH', type, (4+len(data))) + data
    return data

def encode_EventsAndReports(par):
    data = ''
    e = par["HoldEventsAndReportsUponReconnect"]<<7|0
    data += struct.pack("!B", e)
    type = Parameter_struct['EventsAndReports']['type']
    data = struct.pack('!HH', type, (4+len(data))) + data
    return data

def encode_ROReportSpec(par):
    data = ''
    data += struct.pack("!B", ROReportTriggerType_Name2Type[par["ROReportTrigger"]])
    data += struct.pack("!H", par["N"])
    data += encode("TagReportContentSelector")(par["TagReportContentSelector"])
    if par.has_key("Custom"):
        for x in par["Custom"]:
            data += encode("Custom")(x)
    type = Parameter_struct['ROReportSpec']['type']
    data = struct.pack('!HH', type, (4+len(data))) + data
    return data

def encode_TagReportContentSelector(par):
    data = ''
    e = par["EnableROSpecID"]<<7|par["EnableSpecIndex"]<<6|par["EnableInventoryParameterSpecID"]<<5|par["EnableAntennaID"]<<4|par["EnableChannelIndex"]<<3|par["EnablePeakRSSI"]<<2|par["EnableFirstSeenTimestamp"]<<1|par["EnableLastSeenTimestamp"]<<0|0
    data += struct.pack("!B", e)
    e = par["EnableTagSeenCount"]<<7|par["EnableAccessSpecID"]<<6|0
    data += struct.pack("!B", e)
    if par.has_key("C1G2EPCMemorySelector"):
        for x in par["C1G2EPCMemorySelector"]:
            data += encode("C1G2EPCMemorySelector")(x)
    type = Parameter_struct['TagReportContentSelector']['type']
    data = struct.pack('!HH', type, (4+len(data))) + data
    return data

def encode_AccessReportSpec(par):
    data = ''
    data += struct.pack("!B", AccessReportTriggerType_Name2Type[par["AccessReportTrigger"]])
    type = Parameter_struct['AccessReportSpec']['type']
    data = struct.pack('!HH', type, (4+len(data))) + data
    return data

def encode_TagReportData(par):
    data = ''
    if par.has_key("EPCData"):
        data += encode("EPCData")(par["EPCData"])
    if par.has_key("EPC_96"):
        data += encode("EPC_96")(par["EPC_96"])
    if par.has_key("ROSpecID"):
        data += encode("ROSpecID")(par["ROSpecID"])
    if par.has_key("SpecIndex"):
        data += encode("SpecIndex")(par["SpecIndex"])
    if par.has_key("InventoryParameterSpecID"):
        data += encode("InventoryParameterSpecID")(par["InventoryParameterSpecID"])
    if par.has_key("AntennaID"):
        data += encode("AntennaID")(par["AntennaID"])
    if par.has_key("PeakRSSI"):
        data += encode("PeakRSSI")(par["PeakRSSI"])
    if par.has_key("ChannelIndex"):
        data += encode("ChannelIndex")(par["ChannelIndex"])
    if par.has_key("FirstSeenTimestampUTC"):
        data += encode("FirstSeenTimestampUTC")(par["FirstSeenTimestampUTC"])
    if par.has_key("FirstSeenTimestampUptime"):
        data += encode("FirstSeenTimestampUptime")(par["FirstSeenTimestampUptime"])
    if par.has_key("LastSeenTimestampUTC"):
        data += encode("LastSeenTimestampUTC")(par["LastSeenTimestampUTC"])
    if par.has_key("LastSeenTimestampUptime"):
        data += encode("LastSeenTimestampUptime")(par["LastSeenTimestampUptime"])
    if par.has_key("TagSeenCount"):
        data += encode("TagSeenCount")(par["TagSeenCount"])
    if par.has_key("C1G2_PC"):
        for x in par["C1G2_PC"]:
            data += encode("C1G2_PC")(x)
    if par.has_key("C1G2_CRC"):
        for x in par["C1G2_CRC"]:
            data += encode("C1G2_CRC")(x)
    if par.has_key("AccessSpecID"):
        data += encode("AccessSpecID")(par["AccessSpecID"])
    if par.has_key("C1G2ReadOpSpecResult"):
        for x in par["C1G2ReadOpSpecResult"]:
            data += encode("C1G2ReadOpSpecResult")(x)
    if par.has_key("C1G2WriteOpSpecResult"):
        for x in par["C1G2WriteOpSpecResult"]:
            data += encode("C1G2WriteOpSpecResult")(x)
    if par.has_key("C1G2KillOpSpecResult"):
        for x in par["C1G2KillOpSpecResult"]:
            data += encode("C1G2KillOpSpecResult")(x)
    if par.has_key("C1G2LockOpSpecResult"):
        for x in par["C1G2LockOpSpecResult"]:
            data += encode("C1G2LockOpSpecResult")(x)
    if par.has_key("C1G2BlockEraseOpSpecResult"):
        for x in par["C1G2BlockEraseOpSpecResult"]:
            data += encode("C1G2BlockEraseOpSpecResult")(x)
    if par.has_key("C1G2BlockWriteOpSpecResult"):
        for x in par["C1G2BlockWriteOpSpecResult"]:
            data += encode("C1G2BlockWriteOpSpecResult")(x)
    if par.has_key("Custom"):
        for x in par["Custom"]:
            data += encode("Custom")(x)
    if par.has_key("Custom"):
        for x in par["Custom"]:
            data += encode("Custom")(x)
    type = Parameter_struct['TagReportData']['type']
    data = struct.pack('!HH', type, (4+len(data))) + data
    return data

def encode_EPCData(par):
    data = ''
    data += struct.pack("!H", par["EPC"]["BitLen"])
    data += par['EPC']['Data']
    type = Parameter_struct['EPCData']['type']
    data = struct.pack('!HH', type, (4+len(data))) + data
    return data

def encode_EPC_96(par):
    data = ''
    EPC = par["EPC"]
    data += struct.pack('!H', len(EPC))
    for x in EPC:
        data += struct.pack('!s', x)

    type = Parameter_struct['EPC_96']['type']
    data = struct.pack('!HH', type, (4+len(data))) + data
    return data

def encode_ROSpecID(par):
    data = ''
    data += struct.pack("!I", par["ROSpecID"])
    type = Parameter_struct['ROSpecID']['type']
    data = struct.pack('!HH', type, (4+len(data))) + data
    return data

def encode_SpecIndex(par):
    data = ''
    data += struct.pack("!H", par["SpecIndex"])
    type = Parameter_struct['SpecIndex']['type']
    data = struct.pack('!HH', type, (4+len(data))) + data
    return data

def encode_InventoryParameterSpecID(par):
    data = ''
    data += struct.pack("!H", par["InventoryParameterSpecID"])
    type = Parameter_struct['InventoryParameterSpecID']['type']
    data = struct.pack('!HH', type, (4+len(data))) + data
    return data

def encode_AntennaID(par):
    data = ''
    data += struct.pack("!H", par["AntennaID"])
    type = Parameter_struct['AntennaID']['type']
    data = struct.pack('!HH', type, (4+len(data))) + data
    return data

def encode_PeakRSSI(par):
    data = ''
    data += struct.pack("!b", par["PeakRSSI"])
    type = Parameter_struct['PeakRSSI']['type']
    data = struct.pack('!HH', type, (4+len(data))) + data
    return data

def encode_ChannelIndex(par):
    data = ''
    data += struct.pack("!H", par["ChannelIndex"])
    type = Parameter_struct['ChannelIndex']['type']
    data = struct.pack('!HH', type, (4+len(data))) + data
    return data

def encode_FirstSeenTimestampUTC(par):
    data = ''
    data += struct.pack("!Q", par["Microseconds"])
    type = Parameter_struct['FirstSeenTimestampUTC']['type']
    data = struct.pack('!HH', type, (4+len(data))) + data
    return data

def encode_FirstSeenTimestampUptime(par):
    data = ''
    data += struct.pack("!Q", par["Microseconds"])
    type = Parameter_struct['FirstSeenTimestampUptime']['type']
    data = struct.pack('!HH', type, (4+len(data))) + data
    return data

def encode_LastSeenTimestampUTC(par):
    data = ''
    data += struct.pack("!Q", par["Microseconds"])
    type = Parameter_struct['LastSeenTimestampUTC']['type']
    data = struct.pack('!HH', type, (4+len(data))) + data
    return data

def encode_LastSeenTimestampUptime(par):
    data = ''
    data += struct.pack("!Q", par["Microseconds"])
    type = Parameter_struct['LastSeenTimestampUptime']['type']
    data = struct.pack('!HH', type, (4+len(data))) + data
    return data

def encode_TagSeenCount(par):
    data = ''
    data += struct.pack("!H", par["TagCount"])
    type = Parameter_struct['TagSeenCount']['type']
    data = struct.pack('!HH', type, (4+len(data))) + data
    return data

def encode_AccessSpecID(par):
    data = ''
    data += struct.pack("!I", par["AccessSpecID"])
    type = Parameter_struct['AccessSpecID']['type']
    data = struct.pack('!HH', type, (4+len(data))) + data
    return data

def encode_RFSurveyReportData(par):
    data = ''
    if par.has_key("ROSpecID"):
        data += encode("ROSpecID")(par["ROSpecID"])
    if par.has_key("SpecIndex"):
        data += encode("SpecIndex")(par["SpecIndex"])
    for x in par["FrequencyRSSILevelEntry"]:
        data += encode("FrequencyRSSILevelEntry")(x)
    if par.has_key("Custom"):
        for x in par["Custom"]:
            data += encode("Custom")(x)
    type = Parameter_struct['RFSurveyReportData']['type']
    data = struct.pack('!HH', type, (4+len(data))) + data
    return data

def encode_FrequencyRSSILevelEntry(par):
    data = ''
    data += struct.pack("!I", par["Frequency"])
    data += struct.pack("!I", par["Bandwidth"])
    data += struct.pack("!b", par["AverageRSSI"])
    data += struct.pack("!b", par["PeakRSSI"])
    if par.has_key("UTCTimestamp"):
        data += encode("UTCTimestamp")(par["UTCTimestamp"])
    if par.has_key("Uptime"):
        data += encode("Uptime")(par["Uptime"])
    type = Parameter_struct['FrequencyRSSILevelEntry']['type']
    data = struct.pack('!HH', type, (4+len(data))) + data
    return data

def encode_ReaderEventNotificationSpec(par):
    data = ''
    for x in par["EventNotificationState"]:
        data += encode("EventNotificationState")(x)
    type = Parameter_struct['ReaderEventNotificationSpec']['type']
    data = struct.pack('!HH', type, (4+len(data))) + data
    return data

def encode_EventNotificationState(par):
    data = ''
    data += struct.pack("!H", NotificationEventType_Name2Type[par["EventType"]])
    e = par["NotificationState"]<<7|0
    data += struct.pack("!B", e)
    type = Parameter_struct['EventNotificationState']['type']
    data = struct.pack('!HH', type, (4+len(data))) + data
    return data

def encode_ReaderEventNotificationData(par):
    data = ''
    if par.has_key("UTCTimestamp"):
        data += encode("UTCTimestamp")(par["UTCTimestamp"])
    if par.has_key("Uptime"):
        data += encode("Uptime")(par["Uptime"])
    if par.has_key("HoppingEvent"):
        data += encode("HoppingEvent")(par["HoppingEvent"])
    if par.has_key("GPIEvent"):
        data += encode("GPIEvent")(par["GPIEvent"])
    if par.has_key("ROSpecEvent"):
        data += encode("ROSpecEvent")(par["ROSpecEvent"])
    if par.has_key("ReportBufferLevelWarningEvent"):
        data += encode("ReportBufferLevelWarningEvent")(par["ReportBufferLevelWarningEvent"])
    if par.has_key("ReportBufferOverflowErrorEvent"):
        data += encode("ReportBufferOverflowErrorEvent")(par["ReportBufferOverflowErrorEvent"])
    if par.has_key("ReaderExceptionEvent"):
        data += encode("ReaderExceptionEvent")(par["ReaderExceptionEvent"])
    if par.has_key("RFSurveyEvent"):
        data += encode("RFSurveyEvent")(par["RFSurveyEvent"])
    if par.has_key("AISpecEvent"):
        data += encode("AISpecEvent")(par["AISpecEvent"])
    if par.has_key("AntennaEvent"):
        data += encode("AntennaEvent")(par["AntennaEvent"])
    if par.has_key("ConnectionAttemptEvent"):
        data += encode("ConnectionAttemptEvent")(par["ConnectionAttemptEvent"])
    if par.has_key("ConnectionCloseEvent"):
        data += encode("ConnectionCloseEvent")(par["ConnectionCloseEvent"])
    if par.has_key("Custom"):
        for x in par["Custom"]:
            data += encode("Custom")(x)
    type = Parameter_struct['ReaderEventNotificationData']['type']
    data = struct.pack('!HH', type, (4+len(data))) + data
    return data

def encode_HoppingEvent(par):
    data = ''
    data += struct.pack("!H", par["HopTableID"])
    data += struct.pack("!H", par["NextChannelIndex"])
    type = Parameter_struct['HoppingEvent']['type']
    data = struct.pack('!HH', type, (4+len(data))) + data
    return data

def encode_GPIEvent(par):
    data = ''
    data += struct.pack("!H", par["GPIPortNumber"])
    e = par["GPIEvent"]<<7|0
    data += struct.pack("!B", e)
    type = Parameter_struct['GPIEvent']['type']
    data = struct.pack('!HH', type, (4+len(data))) + data
    return data

def encode_ROSpecEvent(par):
    data = ''
    data += struct.pack("!B", ROSpecEventType_Name2Type[par["EventType"]])
    data += struct.pack("!I", par["ROSpecID"])
    data += struct.pack("!I", par["PreemptingROSpecID"])
    type = Parameter_struct['ROSpecEvent']['type']
    data = struct.pack('!HH', type, (4+len(data))) + data
    return data

def encode_ReportBufferLevelWarningEvent(par):
    data = ''
    data += struct.pack("!B", par["ReportBufferPercentageFull"])
    type = Parameter_struct['ReportBufferLevelWarningEvent']['type']
    data = struct.pack('!HH', type, (4+len(data))) + data
    return data

def encode_ReportBufferOverflowErrorEvent(par):
    data = ''
    type = Parameter_struct['ReportBufferOverflowErrorEvent']['type']
    data = struct.pack('!HH', type, (4+len(data))) + data
    return data

def encode_ReaderExceptionEvent(par):
    data = ''
    Message = par["Message"]
    data += struct.pack('!H', len(Message))
    for x in Message:
        data += struct.pack('!B', x)

    if par.has_key("ROSpecID"):
        data += encode("ROSpecID")(par["ROSpecID"])
    if par.has_key("SpecIndex"):
        data += encode("SpecIndex")(par["SpecIndex"])
    if par.has_key("InventoryParameterSpecID"):
        data += encode("InventoryParameterSpecID")(par["InventoryParameterSpecID"])
    if par.has_key("AntennaID"):
        data += encode("AntennaID")(par["AntennaID"])
    if par.has_key("AccessSpecID"):
        data += encode("AccessSpecID")(par["AccessSpecID"])
    if par.has_key("OpSpecID"):
        data += encode("OpSpecID")(par["OpSpecID"])
    if par.has_key("Custom"):
        for x in par["Custom"]:
            data += encode("Custom")(x)
    type = Parameter_struct['ReaderExceptionEvent']['type']
    data = struct.pack('!HH', type, (4+len(data))) + data
    return data

def encode_OpSpecID(par):
    data = ''
    data += struct.pack("!H", par["OpSpecID"])
    type = Parameter_struct['OpSpecID']['type']
    data = struct.pack('!HH', type, (4+len(data))) + data
    return data

def encode_RFSurveyEvent(par):
    data = ''
    data += struct.pack("!B", RFSurveyEventType_Name2Type[par["EventType"]])
    data += struct.pack("!I", par["ROSpecID"])
    data += struct.pack("!H", par["SpecIndex"])
    type = Parameter_struct['RFSurveyEvent']['type']
    data = struct.pack('!HH', type, (4+len(data))) + data
    return data

def encode_AISpecEvent(par):
    data = ''
    data += struct.pack("!B", AISpecEventType_Name2Type[par["EventType"]])
    data += struct.pack("!I", par["ROSpecID"])
    data += struct.pack("!H", par["SpecIndex"])
    if par.has_key("C1G2SingulationDetails"):
        data += encode("C1G2SingulationDetails")(par["C1G2SingulationDetails"])
    type = Parameter_struct['AISpecEvent']['type']
    data = struct.pack('!HH', type, (4+len(data))) + data
    return data

def encode_AntennaEvent(par):
    data = ''
    data += struct.pack("!B", AntennaEventType_Name2Type[par["EventType"]])
    data += struct.pack("!H", par["AntennaID"])
    type = Parameter_struct['AntennaEvent']['type']
    data = struct.pack('!HH', type, (4+len(data))) + data
    return data

def encode_ConnectionAttemptEvent(par):
    data = ''
    data += struct.pack("!H", ConnectionAttemptStatusType_Name2Type[par["Status"]])
    type = Parameter_struct['ConnectionAttemptEvent']['type']
    data = struct.pack('!HH', type, (4+len(data))) + data
    return data

def encode_ConnectionCloseEvent(par):
    data = ''
    type = Parameter_struct['ConnectionCloseEvent']['type']
    data = struct.pack('!HH', type, (4+len(data))) + data
    return data

def encode_LLRPStatus(par):
    data = ''
    data += struct.pack("!H", StatusCode_Name2Type[par["StatusCode"]])
    ErrorDescription = par["ErrorDescription"]
    data += struct.pack('!H', len(ErrorDescription))
    for x in ErrorDescription:
        data += struct.pack('!B', x)

    if par.has_key("FieldError"):
        data += encode("FieldError")(par["FieldError"])
    if par.has_key("ParameterError"):
        data += encode("ParameterError")(par["ParameterError"])
    type = Parameter_struct['LLRPStatus']['type']
    data = struct.pack('!HH', type, (4+len(data))) + data
    return data

def encode_FieldError(par):
    data = ''
    data += struct.pack("!H", par["FieldNum"])
    data += struct.pack("!H", StatusCode_Name2Type[par["ErrorCode"]])
    type = Parameter_struct['FieldError']['type']
    data = struct.pack('!HH', type, (4+len(data))) + data
    return data

def encode_ParameterError(par):
    data = ''
    data += struct.pack("!H", par["ParameterType"])
    data += struct.pack("!H", StatusCode_Name2Type[par["ErrorCode"]])
    if par.has_key("FieldError"):
        data += encode("FieldError")(par["FieldError"])
    if par.has_key("ParameterError"):
        data += encode("ParameterError")(par["ParameterError"])
    type = Parameter_struct['ParameterError']['type']
    data = struct.pack('!HH', type, (4+len(data))) + data
    return data

def encode_C1G2LLRPCapabilities(par):
    data = ''
    e = par["CanSupportBlockErase"]<<7|par["CanSupportBlockWrite"]<<6|0
    data += struct.pack("!B", e)
    data += struct.pack("!H", par["MaxNumSelectFiltersPerQuery"])
    type = Parameter_struct['C1G2LLRPCapabilities']['type']
    data = struct.pack('!HH', type, (4+len(data))) + data
    return data

def encode_C1G2UHFRFModeTable(par):
    data = ''
    for x in par["C1G2UHFRFModeTableEntry"]:
        data += encode("C1G2UHFRFModeTableEntry")(x)
    type = Parameter_struct['C1G2UHFRFModeTable']['type']
    data = struct.pack('!HH', type, (4+len(data))) + data
    return data

def encode_C1G2UHFRFModeTableEntry(par):
    data = ''
    data += struct.pack("!I", par["ModeIdentifier"])
    e = C1G2DRValue_Name2Type[par["DRValue"]]<<7|par["EPCHAGTCConformance"]<<6|0
    data += struct.pack("!B", e)
    data += struct.pack("!B", C1G2MValue_Name2Type[par["MValue"]])
    data += struct.pack("!B", C1G2ForwardLinkModulation_Name2Type[par["ForwardLinkModulation"]])
    data += struct.pack("!B", C1G2SpectralMaskIndicator_Name2Type[par["SpectralMaskIndicator"]])
    data += struct.pack("!I", par["BDRValue"])
    data += struct.pack("!I", par["PIEValue"])
    data += struct.pack("!I", par["MinTariValue"])
    data += struct.pack("!I", par["MaxTariValue"])
    data += struct.pack("!I", par["StepTariValue"])
    type = Parameter_struct['C1G2UHFRFModeTableEntry']['type']
    data = struct.pack('!HH', type, (4+len(data))) + data
    return data

def encode_C1G2InventoryCommand(par):
    data = ''
    e = par["TagInventoryStateAware"]<<7|0
    data += struct.pack("!B", e)
    if par.has_key("C1G2Filter"):
        for x in par["C1G2Filter"]:
            data += encode("C1G2Filter")(x)
    if par.has_key("C1G2RFControl"):
        data += encode("C1G2RFControl")(par["C1G2RFControl"])
    if par.has_key("C1G2SingulationControl"):
        data += encode("C1G2SingulationControl")(par["C1G2SingulationControl"])
    if par.has_key("Custom"):
        for x in par["Custom"]:
            data += encode("Custom")(x)
    type = Parameter_struct['C1G2InventoryCommand']['type']
    data = struct.pack('!HH', type, (4+len(data))) + data
    return data

def encode_C1G2Filter(par):
    data = ''
    T = par["T"]
    data += struct.pack('!H', len(T))
    for x in T:
        data += struct.pack('!s', x)

    data += encode("C1G2TagInventoryMask")(par["C1G2TagInventoryMask"])
    if par.has_key("C1G2TagInventoryStateAwareFilterAction"):
        data += encode("C1G2TagInventoryStateAwareFilterAction")(par["C1G2TagInventoryStateAwareFilterAction"])
    if par.has_key("C1G2TagInventoryStateUnawareFilterAction"):
        data += encode("C1G2TagInventoryStateUnawareFilterAction")(par["C1G2TagInventoryStateUnawareFilterAction"])
    type = Parameter_struct['C1G2Filter']['type']
    data = struct.pack('!HH', type, (4+len(data))) + data
    return data

def encode_C1G2TagInventoryMask(par):
    data = ''
    MB = par["MB"]
    data += struct.pack('!H', len(MB))
    for x in MB:
        data += struct.pack('!s', x)

    data += struct.pack("!H", par["Pointer"])
    data += struct.pack("!H", par["TagMask"]["BitLen"])
    data += par['TagMask']['Data']
    type = Parameter_struct['C1G2TagInventoryMask']['type']
    data = struct.pack('!HH', type, (4+len(data))) + data
    return data

def encode_C1G2TagInventoryStateAwareFilterAction(par):
    data = ''
    data += struct.pack("!B", C1G2StateAwareTarget_Name2Type[par["Target"]])
    data += struct.pack("!B", C1G2StateAwareAction_Name2Type[par["Action"]])
    type = Parameter_struct['C1G2TagInventoryStateAwareFilterAction']['type']
    data = struct.pack('!HH', type, (4+len(data))) + data
    return data

def encode_C1G2TagInventoryStateUnawareFilterAction(par):
    data = ''
    data += struct.pack("!B", C1G2StateUnawareAction_Name2Type[par["Action"]])
    type = Parameter_struct['C1G2TagInventoryStateUnawareFilterAction']['type']
    data = struct.pack('!HH', type, (4+len(data))) + data
    return data

def encode_C1G2RFControl(par):
    data = ''
    data += struct.pack("!H", par["ModeIndex"])
    data += struct.pack("!H", par["Tari"])
    type = Parameter_struct['C1G2RFControl']['type']
    data = struct.pack('!HH', type, (4+len(data))) + data
    return data

def encode_C1G2SingulationControl(par):
    data = ''
    Session = par["Session"]
    data += struct.pack('!H', len(Session))
    for x in Session:
        data += struct.pack('!s', x)

    data += struct.pack("!H", par["TagPopulation"])
    data += struct.pack("!I", par["TagTransitTime"])
    if par.has_key("C1G2TagInventoryStateAwareSingulationAction"):
        data += encode("C1G2TagInventoryStateAwareSingulationAction")(par["C1G2TagInventoryStateAwareSingulationAction"])
    type = Parameter_struct['C1G2SingulationControl']['type']
    data = struct.pack('!HH', type, (4+len(data))) + data
    return data

def encode_C1G2TagInventoryStateAwareSingulationAction(par):
    data = ''
    e = C1G2TagInventoryStateAwareI_Name2Type[par["I"]]<<7|C1G2TagInventoryStateAwareS_Name2Type[par["S"]]<<6|0
    data += struct.pack("!B", e)
    type = Parameter_struct['C1G2TagInventoryStateAwareSingulationAction']['type']
    data = struct.pack('!HH', type, (4+len(data))) + data
    return data

def encode_C1G2TagSpec(par):
    data = ''
    for x in par["C1G2TargetTag"]:
        data += encode("C1G2TargetTag")(x)
    type = Parameter_struct['C1G2TagSpec']['type']
    data = struct.pack('!HH', type, (4+len(data))) + data
    return data

def encode_C1G2TargetTag(par):
    data = ''
    MB = par["MB"]
    data += struct.pack('!H', len(MB))
    for x in MB:
        data += struct.pack('!s', x)

    e = par["Match"]<<7|0
    data += struct.pack("!B", e)
    data += struct.pack("!H", par["Pointer"])
    data += struct.pack("!H", par["TagMask"]["BitLen"])
    data += par['TagMask']['Data']
    data += struct.pack("!H", par["TagData"]["BitLen"])
    data += par['TagData']['Data']
    type = Parameter_struct['C1G2TargetTag']['type']
    data = struct.pack('!HH', type, (4+len(data))) + data
    return data

def encode_C1G2Read(par):
    data = ''
    data += struct.pack("!H", par["OpSpecID"])
    data += struct.pack("!I", par["AccessPassword"])
    MB = par["MB"]
    data += struct.pack('!H', len(MB))
    for x in MB:
        data += struct.pack('!s', x)

    data += struct.pack("!H", par["WordPointer"])
    data += struct.pack("!H", par["WordCount"])
    type = Parameter_struct['C1G2Read']['type']
    data = struct.pack('!HH', type, (4+len(data))) + data
    return data

def encode_C1G2Write(par):
    data = ''
    data += struct.pack("!H", par["OpSpecID"])
    data += struct.pack("!I", par["AccessPassword"])
    MB = par["MB"]
    data += struct.pack('!H', len(MB))
    for x in MB:
        data += struct.pack('!s', x)

    data += struct.pack("!H", par["WordPointer"])
    WriteData = par["WriteData"]
    data += struct.pack('!H', len(WriteData))
    for x in WriteData:
        data += struct.pack('!H', x)

    type = Parameter_struct['C1G2Write']['type']
    data = struct.pack('!HH', type, (4+len(data))) + data
    return data

def encode_C1G2Kill(par):
    data = ''
    data += struct.pack("!H", par["OpSpecID"])
    data += struct.pack("!I", par["KillPassword"])
    type = Parameter_struct['C1G2Kill']['type']
    data = struct.pack('!HH', type, (4+len(data))) + data
    return data

def encode_C1G2Lock(par):
    data = ''
    data += struct.pack("!H", par["OpSpecID"])
    data += struct.pack("!I", par["AccessPassword"])
    for x in par["C1G2LockPayload"]:
        data += encode("C1G2LockPayload")(x)
    type = Parameter_struct['C1G2Lock']['type']
    data = struct.pack('!HH', type, (4+len(data))) + data
    return data

def encode_C1G2LockPayload(par):
    data = ''
    data += struct.pack("!B", C1G2LockPrivilege_Name2Type[par["Privilege"]])
    data += struct.pack("!B", C1G2LockDataField_Name2Type[par["DataField"]])
    type = Parameter_struct['C1G2LockPayload']['type']
    data = struct.pack('!HH', type, (4+len(data))) + data
    return data

def encode_C1G2BlockErase(par):
    data = ''
    data += struct.pack("!H", par["OpSpecID"])
    data += struct.pack("!I", par["AccessPassword"])
    MB = par["MB"]
    data += struct.pack('!H', len(MB))
    for x in MB:
        data += struct.pack('!s', x)

    data += struct.pack("!H", par["WordPointer"])
    data += struct.pack("!H", par["WordCount"])
    type = Parameter_struct['C1G2BlockErase']['type']
    data = struct.pack('!HH', type, (4+len(data))) + data
    return data

def encode_C1G2BlockWrite(par):
    data = ''
    data += struct.pack("!H", par["OpSpecID"])
    data += struct.pack("!I", par["AccessPassword"])
    MB = par["MB"]
    data += struct.pack('!H', len(MB))
    for x in MB:
        data += struct.pack('!s', x)

    data += struct.pack("!H", par["WordPointer"])
    WriteData = par["WriteData"]
    data += struct.pack('!H', len(WriteData))
    for x in WriteData:
        data += struct.pack('!H', x)

    type = Parameter_struct['C1G2BlockWrite']['type']
    data = struct.pack('!HH', type, (4+len(data))) + data
    return data

def encode_C1G2EPCMemorySelector(par):
    data = ''
    e = par["EnableCRC"]<<7|par["EnablePCBits"]<<6|0
    data += struct.pack("!B", e)
    type = Parameter_struct['C1G2EPCMemorySelector']['type']
    data = struct.pack('!HH', type, (4+len(data))) + data
    return data

def encode_C1G2_PC(par):
    data = ''
    data += struct.pack("!H", par["PC_Bits"])
    type = Parameter_struct['C1G2_PC']['type']
    data = struct.pack('!HH', type, (4+len(data))) + data
    return data

def encode_C1G2_CRC(par):
    data = ''
    data += struct.pack("!H", par["CRC"])
    type = Parameter_struct['C1G2_CRC']['type']
    data = struct.pack('!HH', type, (4+len(data))) + data
    return data

def encode_C1G2SingulationDetails(par):
    data = ''
    data += struct.pack("!H", par["NumCollisionSlots"])
    data += struct.pack("!H", par["NumEmptySlots"])
    type = Parameter_struct['C1G2SingulationDetails']['type']
    data = struct.pack('!HH', type, (4+len(data))) + data
    return data

def encode_C1G2ReadOpSpecResult(par):
    data = ''
    data += struct.pack("!B", C1G2ReadResultType_Name2Type[par["Result"]])
    data += struct.pack("!H", par["OpSpecID"])
    ReadData = par["ReadData"]
    data += struct.pack('!H', len(ReadData))
    for x in ReadData:
        data += struct.pack('!H', x)

    type = Parameter_struct['C1G2ReadOpSpecResult']['type']
    data = struct.pack('!HH', type, (4+len(data))) + data
    return data

def encode_C1G2WriteOpSpecResult(par):
    data = ''
    data += struct.pack("!B", C1G2WriteResultType_Name2Type[par["Result"]])
    data += struct.pack("!H", par["OpSpecID"])
    data += struct.pack("!H", par["NumWordsWritten"])
    type = Parameter_struct['C1G2WriteOpSpecResult']['type']
    data = struct.pack('!HH', type, (4+len(data))) + data
    return data

def encode_C1G2KillOpSpecResult(par):
    data = ''
    data += struct.pack("!B", C1G2KillResultType_Name2Type[par["Result"]])
    data += struct.pack("!H", par["OpSpecID"])
    type = Parameter_struct['C1G2KillOpSpecResult']['type']
    data = struct.pack('!HH', type, (4+len(data))) + data
    return data

def encode_C1G2LockOpSpecResult(par):
    data = ''
    data += struct.pack("!B", C1G2LockResultType_Name2Type[par["Result"]])
    data += struct.pack("!H", par["OpSpecID"])
    type = Parameter_struct['C1G2LockOpSpecResult']['type']
    data = struct.pack('!HH', type, (4+len(data))) + data
    return data

def encode_C1G2BlockEraseOpSpecResult(par):
    data = ''
    data += struct.pack("!B", C1G2BlockEraseResultType_Name2Type[par["Result"]])
    data += struct.pack("!H", par["OpSpecID"])
    type = Parameter_struct['C1G2BlockEraseOpSpecResult']['type']
    data = struct.pack('!HH', type, (4+len(data))) + data
    return data

def encode_C1G2BlockWriteOpSpecResult(par):
    data = ''
    data += struct.pack("!B", C1G2BlockWriteResultType_Name2Type[par["Result"]])
    data += struct.pack("!H", par["OpSpecID"])
    data += struct.pack("!H", par["NumWordsWritten"])
    type = Parameter_struct['C1G2BlockWriteOpSpecResult']['type']
    data = struct.pack('!HH', type, (4+len(data))) + data
    return data

def encode_CUSTOM_MESSAGE(par):
    data = ''
    data += struct.pack("!I", par["VendorIdentifier"])
    data += struct.pack("!B", par["MessageSubtype"])
    Data = par["Data"]
    data += struct.pack('!H', len(Data))
    for x in Data:
        data += struct.pack('!s', x)

    return data

def encode_GET_READER_CAPABILITIES(par):
    data = ''
    data += struct.pack("!B", GetReaderCapabilitiesRequestedData_Name2Type[par["RequestedData"]])
    if par.has_key("Custom"):
        for x in par["Custom"]:
            data += encode("Custom")(x)
    return data

def encode_GET_READER_CAPABILITIES_RESPONSE(par):
    data = ''
    data += encode("LLRPStatus")(par["LLRPStatus"])
    if par.has_key("GeneralDeviceCapabilities"):
        data += encode("GeneralDeviceCapabilities")(par["GeneralDeviceCapabilities"])
    if par.has_key("LLRPCapabilities"):
        data += encode("LLRPCapabilities")(par["LLRPCapabilities"])
    if par.has_key("RegulatoryCapabilities"):
        data += encode("RegulatoryCapabilities")(par["RegulatoryCapabilities"])
    if par.has_key("C1G2LLRPCapabilities"):
        data += encode("C1G2LLRPCapabilities")(par["C1G2LLRPCapabilities"])
    if par.has_key("Custom"):
        for x in par["Custom"]:
            data += encode("Custom")(x)
    return data

def encode_ADD_ROSPEC(par):
    data = ''
    data += encode("ROSpec")(par["ROSpec"])
    return data

def encode_ADD_ROSPEC_RESPONSE(par):
    data = ''
    data += encode("LLRPStatus")(par["LLRPStatus"])
    return data

def encode_DELETE_ROSPEC(par):
    data = ''
    data += struct.pack("!I", par["ROSpecID"])
    return data

def encode_DELETE_ROSPEC_RESPONSE(par):
    data = ''
    data += encode("LLRPStatus")(par["LLRPStatus"])
    return data

def encode_START_ROSPEC(par):
    data = ''
    data += struct.pack("!I", par["ROSpecID"])
    return data

def encode_START_ROSPEC_RESPONSE(par):
    data = ''
    data += encode("LLRPStatus")(par["LLRPStatus"])
    return data

def encode_STOP_ROSPEC(par):
    data = ''
    data += struct.pack("!I", par["ROSpecID"])
    return data

def encode_STOP_ROSPEC_RESPONSE(par):
    data = ''
    data += encode("LLRPStatus")(par["LLRPStatus"])
    return data

def encode_ENABLE_ROSPEC(par):
    data = ''
    data += struct.pack("!I", par["ROSpecID"])
    return data

def encode_ENABLE_ROSPEC_RESPONSE(par):
    data = ''
    data += encode("LLRPStatus")(par["LLRPStatus"])
    return data

def encode_DISABLE_ROSPEC(par):
    data = ''
    data += struct.pack("!I", par["ROSpecID"])
    return data

def encode_DISABLE_ROSPEC_RESPONSE(par):
    data = ''
    data += encode("LLRPStatus")(par["LLRPStatus"])
    return data

def encode_GET_ROSPECS(par):
    data = ''
    return data

def encode_GET_ROSPECS_RESPONSE(par):
    data = ''
    data += encode("LLRPStatus")(par["LLRPStatus"])
    if par.has_key("ROSpec"):
        for x in par["ROSpec"]:
            data += encode("ROSpec")(x)
    return data

def encode_ADD_ACCESSSPEC(par):
    data = ''
    data += encode("AccessSpec")(par["AccessSpec"])
    return data

def encode_ADD_ACCESSSPEC_RESPONSE(par):
    data = ''
    data += encode("LLRPStatus")(par["LLRPStatus"])
    return data

def encode_DELETE_ACCESSSPEC(par):
    data = ''
    data += struct.pack("!I", par["AccessSpecID"])
    return data

def encode_DELETE_ACCESSSPEC_RESPONSE(par):
    data = ''
    data += encode("LLRPStatus")(par["LLRPStatus"])
    return data

def encode_ENABLE_ACCESSSPEC(par):
    data = ''
    data += struct.pack("!I", par["AccessSpecID"])
    return data

def encode_ENABLE_ACCESSSPEC_RESPONSE(par):
    data = ''
    data += encode("LLRPStatus")(par["LLRPStatus"])
    return data

def encode_DISABLE_ACCESSSPEC(par):
    data = ''
    data += struct.pack("!I", par["AccessSpecID"])
    return data

def encode_DISABLE_ACCESSSPEC_RESPONSE(par):
    data = ''
    data += encode("LLRPStatus")(par["LLRPStatus"])
    return data

def encode_GET_ACCESSSPECS(par):
    data = ''
    return data

def encode_GET_ACCESSSPECS_RESPONSE(par):
    data = ''
    data += encode("LLRPStatus")(par["LLRPStatus"])
    if par.has_key("AccessSpec"):
        for x in par["AccessSpec"]:
            data += encode("AccessSpec")(x)
    return data

def encode_GET_READER_CONFIG(par):
    data = ''
    data += struct.pack("!H", par["AntennaID"])
    data += struct.pack("!B", GetReaderConfigRequestedData_Name2Type[par["RequestedData"]])
    data += struct.pack("!H", par["GPIPortNum"])
    data += struct.pack("!H", par["GPOPortNum"])
    if par.has_key("Custom"):
        for x in par["Custom"]:
            data += encode("Custom")(x)
    return data

def encode_GET_READER_CONFIG_RESPONSE(par):
    data = ''
    data += encode("LLRPStatus")(par["LLRPStatus"])
    if par.has_key("Identification"):
        data += encode("Identification")(par["Identification"])
    if par.has_key("AntennaProperties"):
        for x in par["AntennaProperties"]:
            data += encode("AntennaProperties")(x)
    if par.has_key("AntennaConfiguration"):
        for x in par["AntennaConfiguration"]:
            data += encode("AntennaConfiguration")(x)
    if par.has_key("ReaderEventNotificationSpec"):
        data += encode("ReaderEventNotificationSpec")(par["ReaderEventNotificationSpec"])
    if par.has_key("ROReportSpec"):
        data += encode("ROReportSpec")(par["ROReportSpec"])
    if par.has_key("AccessReportSpec"):
        data += encode("AccessReportSpec")(par["AccessReportSpec"])
    if par.has_key("LLRPConfigurationStateValue"):
        data += encode("LLRPConfigurationStateValue")(par["LLRPConfigurationStateValue"])
    if par.has_key("KeepaliveSpec"):
        data += encode("KeepaliveSpec")(par["KeepaliveSpec"])
    if par.has_key("GPIPortCurrentState"):
        for x in par["GPIPortCurrentState"]:
            data += encode("GPIPortCurrentState")(x)
    if par.has_key("GPOWriteData"):
        for x in par["GPOWriteData"]:
            data += encode("GPOWriteData")(x)
    if par.has_key("EventsAndReports"):
        data += encode("EventsAndReports")(par["EventsAndReports"])
    if par.has_key("Custom"):
        for x in par["Custom"]:
            data += encode("Custom")(x)
    return data

def encode_SET_READER_CONFIG(par):
    data = ''
    e = par["ResetToFactoryDefault"]<<7|0
    data += struct.pack("!B", e)
    if par.has_key("ReaderEventNotificationSpec"):
        data += encode("ReaderEventNotificationSpec")(par["ReaderEventNotificationSpec"])
    if par.has_key("AntennaProperties"):
        for x in par["AntennaProperties"]:
            data += encode("AntennaProperties")(x)
    if par.has_key("AntennaConfiguration"):
        for x in par["AntennaConfiguration"]:
            data += encode("AntennaConfiguration")(x)
    if par.has_key("ROReportSpec"):
        data += encode("ROReportSpec")(par["ROReportSpec"])
    if par.has_key("AccessReportSpec"):
        data += encode("AccessReportSpec")(par["AccessReportSpec"])
    if par.has_key("KeepaliveSpec"):
        data += encode("KeepaliveSpec")(par["KeepaliveSpec"])
    if par.has_key("GPOWriteData"):
        for x in par["GPOWriteData"]:
            data += encode("GPOWriteData")(x)
    if par.has_key("GPIPortCurrentState"):
        for x in par["GPIPortCurrentState"]:
            data += encode("GPIPortCurrentState")(x)
    if par.has_key("EventsAndReports"):
        data += encode("EventsAndReports")(par["EventsAndReports"])
    if par.has_key("Custom"):
        for x in par["Custom"]:
            data += encode("Custom")(x)
    return data

def encode_SET_READER_CONFIG_RESPONSE(par):
    data = ''
    data += encode("LLRPStatus")(par["LLRPStatus"])
    return data

def encode_CLOSE_CONNECTION(par):
    data = ''
    return data

def encode_CLOSE_CONNECTION_RESPONSE(par):
    data = ''
    data += encode("LLRPStatus")(par["LLRPStatus"])
    return data

def encode_GET_REPORT(par):
    data = ''
    return data

def encode_RO_ACCESS_REPORT(par):
    data = ''
    if par.has_key("TagReportData"):
        for x in par["TagReportData"]:
            data += encode("TagReportData")(x)
    if par.has_key("RFSurveyReportData"):
        for x in par["RFSurveyReportData"]:
            data += encode("RFSurveyReportData")(x)
    if par.has_key("Custom"):
        for x in par["Custom"]:
            data += encode("Custom")(x)
    return data

def encode_KEEPALIVE(par):
    data = ''
    return data

def encode_KEEPALIVE_ACK(par):
    data = ''
    return data

def encode_READER_EVENT_NOTIFICATION(par):
    data = ''
    data += encode("ReaderEventNotificationData")(par["ReaderEventNotificationData"])
    return data

def encode_ENABLE_EVENTS_AND_REPORTS(par):
    data = ''
    return data

def encode_ERROR_MESSAGE(par):
    data = ''
    data += encode("LLRPStatus")(par["LLRPStatus"])
    return data

def decode_UTCTimestamp(data):
    par = {}

    if len(data) == 0:
        return None, data
    type, length = struct.unpack("!HH", data[0:4])

    if type != Parameter_struct["UTCTimestamp"]["type"]:
        return None, data

    body = data[4:length]
    (Microseconds,) = struct.unpack("!Q", body[0:8])
    par["Microseconds"] = Microseconds
    body = body[8:]
    return par, data[length:]

def decode_Uptime(data):
    par = {}

    if len(data) == 0:
        return None, data
    type, length = struct.unpack("!HH", data[0:4])

    if type != Parameter_struct["Uptime"]["type"]:
        return None, data

    body = data[4:length]
    (Microseconds,) = struct.unpack("!Q", body[0:8])
    par["Microseconds"] = Microseconds
    body = body[8:]
    return par, data[length:]

def decode_Custom(data):
    par = {}

    if len(data) == 0:
        return None, data
    type, length = struct.unpack("!HH", data[0:4])

    if type != Parameter_struct["Custom"]["type"]:
        return None, data

    body = data[4:length]
    (VendorIdentifier,) = struct.unpack("!I", body[0:4])
    par["VendorIdentifier"] = VendorIdentifier
    body = body[4:]
    (ParameterSubtype,) = struct.unpack("!I", body[0:4])
    par["ParameterSubtype"] = ParameterSubtype
    body = body[4:]
    (arrayLen, ) = struct.unpack("!H", body[0:2])
    body = body[2:]
    par["Data"] = body[0:arrayLen*1]
    body = body[arrayLen*1:]
    return par, data[length:]

def decode_GeneralDeviceCapabilities(data):
    par = {}

    if len(data) == 0:
        return None, data
    type, length = struct.unpack("!HH", data[0:4])

    if type != Parameter_struct["GeneralDeviceCapabilities"]["type"]:
        return None, data

    body = data[4:length]
    (MaxNumberOfAntennaSupported,) = struct.unpack("!H", body[0:2])
    par["MaxNumberOfAntennaSupported"] = MaxNumberOfAntennaSupported
    body = body[2:]
    (e,) = struct.unpack("!B", body[0:1])
    par["CanSetAntennaProperties"] = (e>>7)&1
    par["HasUTCClockCapability"] = (e>>6)&1
    body = body[1:]
    (DeviceManufacturerName,) = struct.unpack("!I", body[0:4])
    par["DeviceManufacturerName"] = DeviceManufacturerName
    body = body[4:]
    (ModelName,) = struct.unpack("!I", body[0:4])
    par["ModelName"] = ModelName
    body = body[4:]
    (arrayLen, ) = struct.unpack("!H", body[0:2])
    body = body[2:]
    par["ReaderFirmwareVersion"] = body[0:arrayLen*1]
    body = body[arrayLen*1:]
    par["ReceiveSensitivityTableEntry"] = []
    while True:
        ret, body = decode("ReceiveSensitivityTableEntry")(body)
        if ret:
            par["ReceiveSensitivityTableEntry"].append(ret)
        else:
            break
    par["PerAntennaReceiveSensitivityRange"] = []
    while True:
        ret, body = decode("PerAntennaReceiveSensitivityRange")(body)
        if ret:
            par["PerAntennaReceiveSensitivityRange"].append(ret)
        else:
            break
    ret, body = decode("GPIOCapabilities")(body)
    if ret:
        par["GPIOCapabilities"] = ret
    else:
        raise LLRPError("missing GPIOCapabilities parameter")
    par["PerAntennaAirProtocol"] = []
    while True:
        ret, body = decode("PerAntennaAirProtocol")(body)
        if ret:
            par["PerAntennaAirProtocol"].append(ret)
        else:
            break
    return par, data[length:]

def decode_ReceiveSensitivityTableEntry(data):
    par = {}

    if len(data) == 0:
        return None, data
    type, length = struct.unpack("!HH", data[0:4])

    if type != Parameter_struct["ReceiveSensitivityTableEntry"]["type"]:
        return None, data

    body = data[4:length]
    (Index,) = struct.unpack("!H", body[0:2])
    par["Index"] = Index
    body = body[2:]
    (ReceiveSensitivityValue,) = struct.unpack("!h", body[0:2])
    par["ReceiveSensitivityValue"] = ReceiveSensitivityValue
    body = body[2:]
    return par, data[length:]

def decode_PerAntennaReceiveSensitivityRange(data):
    par = {}

    if len(data) == 0:
        return None, data
    type, length = struct.unpack("!HH", data[0:4])

    if type != Parameter_struct["PerAntennaReceiveSensitivityRange"]["type"]:
        return None, data

    body = data[4:length]
    (AntennaID,) = struct.unpack("!H", body[0:2])
    par["AntennaID"] = AntennaID
    body = body[2:]
    (ReceiveSensitivityIndexMin,) = struct.unpack("!H", body[0:2])
    par["ReceiveSensitivityIndexMin"] = ReceiveSensitivityIndexMin
    body = body[2:]
    (ReceiveSensitivityIndexMax,) = struct.unpack("!H", body[0:2])
    par["ReceiveSensitivityIndexMax"] = ReceiveSensitivityIndexMax
    body = body[2:]
    return par, data[length:]

def decode_PerAntennaAirProtocol(data):
    par = {}

    if len(data) == 0:
        return None, data
    type, length = struct.unpack("!HH", data[0:4])

    if type != Parameter_struct["PerAntennaAirProtocol"]["type"]:
        return None, data

    body = data[4:length]
    (AntennaID,) = struct.unpack("!H", body[0:2])
    par["AntennaID"] = AntennaID
    body = body[2:]
    (arrayLen, ) = struct.unpack("!H", body[0:2])
    body = body[2:]
    par["ProtocolID"] = body[0:arrayLen*1]
    body = body[arrayLen*1:]
    return par, data[length:]

def decode_GPIOCapabilities(data):
    par = {}

    if len(data) == 0:
        return None, data
    type, length = struct.unpack("!HH", data[0:4])

    if type != Parameter_struct["GPIOCapabilities"]["type"]:
        return None, data

    body = data[4:length]
    (NumGPIs,) = struct.unpack("!H", body[0:2])
    par["NumGPIs"] = NumGPIs
    body = body[2:]
    (NumGPOs,) = struct.unpack("!H", body[0:2])
    par["NumGPOs"] = NumGPOs
    body = body[2:]
    return par, data[length:]

def decode_LLRPCapabilities(data):
    par = {}

    if len(data) == 0:
        return None, data
    type, length = struct.unpack("!HH", data[0:4])

    if type != Parameter_struct["LLRPCapabilities"]["type"]:
        return None, data

    body = data[4:length]
    (e,) = struct.unpack("!B", body[0:1])
    par["CanDoRFSurvey"] = (e>>7)&1
    par["CanReportBufferFillWarning"] = (e>>6)&1
    par["SupportsClientRequestOpSpec"] = (e>>5)&1
    par["CanDoTagInventoryStateAwareSingulation"] = (e>>4)&1
    par["SupportsEventAndReportHolding"] = (e>>3)&1
    body = body[1:]
    (MaxNumPriorityLevelsSupported,) = struct.unpack("!B", body[0:1])
    par["MaxNumPriorityLevelsSupported"] = MaxNumPriorityLevelsSupported
    body = body[1:]
    (ClientRequestOpSpecTimeout,) = struct.unpack("!H", body[0:2])
    par["ClientRequestOpSpecTimeout"] = ClientRequestOpSpecTimeout
    body = body[2:]
    (MaxNumROSpecs,) = struct.unpack("!I", body[0:4])
    par["MaxNumROSpecs"] = MaxNumROSpecs
    body = body[4:]
    (MaxNumSpecsPerROSpec,) = struct.unpack("!I", body[0:4])
    par["MaxNumSpecsPerROSpec"] = MaxNumSpecsPerROSpec
    body = body[4:]
    (MaxNumInventoryParameterSpecsPerAISpec,) = struct.unpack("!I", body[0:4])
    par["MaxNumInventoryParameterSpecsPerAISpec"] = MaxNumInventoryParameterSpecsPerAISpec
    body = body[4:]
    (MaxNumAccessSpecs,) = struct.unpack("!I", body[0:4])
    par["MaxNumAccessSpecs"] = MaxNumAccessSpecs
    body = body[4:]
    (MaxNumOpSpecsPerAccessSpec,) = struct.unpack("!I", body[0:4])
    par["MaxNumOpSpecsPerAccessSpec"] = MaxNumOpSpecsPerAccessSpec
    body = body[4:]
    return par, data[length:]

def decode_RegulatoryCapabilities(data):
    par = {}

    if len(data) == 0:
        return None, data
    type, length = struct.unpack("!HH", data[0:4])

    if type != Parameter_struct["RegulatoryCapabilities"]["type"]:
        return None, data

    body = data[4:length]
    (CountryCode,) = struct.unpack("!H", body[0:2])
    par["CountryCode"] = CountryCode
    body = body[2:]
    (CommunicationsStandard,) = struct.unpack("!H", body[0:2])
    par["CommunicationsStandard"] = CommunicationsStandard_Type2Name[CommunicationsStandard]
    body = body[2:]
    ret, body = decode("UHFBandCapabilities")(body)
    if ret:
        par["UHFBandCapabilities"] = ret
    par["Custom"] = []
    while True:
        ret, body = decode("Custom")(body)
        if ret:
            par["Custom"].append(ret)
        else:
            break
    return par, data[length:]

def decode_UHFBandCapabilities(data):
    par = {}

    if len(data) == 0:
        return None, data
    type, length = struct.unpack("!HH", data[0:4])

    if type != Parameter_struct["UHFBandCapabilities"]["type"]:
        return None, data

    body = data[4:length]
    par["TransmitPowerLevelTableEntry"] = []
    while True:
        ret, body = decode("TransmitPowerLevelTableEntry")(body)
        if ret:
            par["TransmitPowerLevelTableEntry"].append(ret)
        else:
            break
    ret, body = decode("FrequencyInformation")(body)
    if ret:
        par["FrequencyInformation"] = ret
    else:
        raise LLRPError("missing FrequencyInformation parameter")
    par["C1G2UHFRFModeTable"] = []
    flag = True
    while flag:
        flag = False
        ret, body = decode("C1G2UHFRFModeTable")(body)
        if ret:
            par["C1G2UHFRFModeTable"].append(ret)
            flag = True
        
    return par, data[length:]

def decode_TransmitPowerLevelTableEntry(data):
    par = {}

    if len(data) == 0:
        return None, data
    type, length = struct.unpack("!HH", data[0:4])

    if type != Parameter_struct["TransmitPowerLevelTableEntry"]["type"]:
        return None, data

    body = data[4:length]
    (Index,) = struct.unpack("!H", body[0:2])
    par["Index"] = Index
    body = body[2:]
    (TransmitPowerValue,) = struct.unpack("!h", body[0:2])
    par["TransmitPowerValue"] = TransmitPowerValue
    body = body[2:]
    return par, data[length:]

def decode_FrequencyInformation(data):
    par = {}

    if len(data) == 0:
        return None, data
    type, length = struct.unpack("!HH", data[0:4])

    if type != Parameter_struct["FrequencyInformation"]["type"]:
        return None, data

    body = data[4:length]
    (e,) = struct.unpack("!B", body[0:1])
    par["Hopping"] = (e>>7)&1
    body = body[1:]
    par["FrequencyHopTable"] = []
    while True:
        ret, body = decode("FrequencyHopTable")(body)
        if ret:
            par["FrequencyHopTable"].append(ret)
        else:
            break
    ret, body = decode("FixedFrequencyTable")(body)
    if ret:
        par["FixedFrequencyTable"] = ret
    return par, data[length:]

def decode_FrequencyHopTable(data):
    par = {}

    if len(data) == 0:
        return None, data
    type, length = struct.unpack("!HH", data[0:4])

    if type != Parameter_struct["FrequencyHopTable"]["type"]:
        return None, data

    body = data[4:length]
    (HopTableID,) = struct.unpack("!B", body[0:1])
    par["HopTableID"] = HopTableID
    body = body[1:]
    (arrayLen, ) = struct.unpack("!H", body[0:2])
    body = body[2:]
    par["Frequency"] = body[0:arrayLen*4]
    body = body[arrayLen*4:]
    return par, data[length:]

def decode_FixedFrequencyTable(data):
    par = {}

    if len(data) == 0:
        return None, data
    type, length = struct.unpack("!HH", data[0:4])

    if type != Parameter_struct["FixedFrequencyTable"]["type"]:
        return None, data

    body = data[4:length]
    (arrayLen, ) = struct.unpack("!H", body[0:2])
    body = body[2:]
    par["Frequency"] = body[0:arrayLen*4]
    body = body[arrayLen*4:]
    return par, data[length:]

def decode_ROSpec(data):
    par = {}

    if len(data) == 0:
        return None, data
    type, length = struct.unpack("!HH", data[0:4])

    if type != Parameter_struct["ROSpec"]["type"]:
        return None, data

    body = data[4:length]
    (ROSpecID,) = struct.unpack("!I", body[0:4])
    par["ROSpecID"] = ROSpecID
    body = body[4:]
    (Priority,) = struct.unpack("!B", body[0:1])
    par["Priority"] = Priority
    body = body[1:]
    (CurrentState,) = struct.unpack("!B", body[0:1])
    par["CurrentState"] = ROSpecState_Type2Name[CurrentState]
    body = body[1:]
    ret, body = decode("ROBoundarySpec")(body)
    if ret:
        par["ROBoundarySpec"] = ret
    else:
        raise LLRPError("missing ROBoundarySpec parameter")
    par["AISpec"] = []
    par["RFSurveySpec"] = []
    par["Custom"] = []
    flag = True
    while flag:
        flag = False
        ret, body = decode("AISpec")(body)
        if ret:
            par["AISpec"].append(ret)
            flag = True
        ret, body = decode("RFSurveySpec")(body)
        if ret:
            par["RFSurveySpec"].append(ret)
            flag = True
        ret, body = decode("Custom")(body)
        if ret:
            par["Custom"].append(ret)
            flag = True
        
    ret, body = decode("ROReportSpec")(body)
    if ret:
        par["ROReportSpec"] = ret
    return par, data[length:]

def decode_ROBoundarySpec(data):
    par = {}

    if len(data) == 0:
        return None, data
    type, length = struct.unpack("!HH", data[0:4])

    if type != Parameter_struct["ROBoundarySpec"]["type"]:
        return None, data

    body = data[4:length]
    ret, body = decode("ROSpecStartTrigger")(body)
    if ret:
        par["ROSpecStartTrigger"] = ret
    else:
        raise LLRPError("missing ROSpecStartTrigger parameter")
    ret, body = decode("ROSpecStopTrigger")(body)
    if ret:
        par["ROSpecStopTrigger"] = ret
    else:
        raise LLRPError("missing ROSpecStopTrigger parameter")
    return par, data[length:]

def decode_ROSpecStartTrigger(data):
    par = {}

    if len(data) == 0:
        return None, data
    type, length = struct.unpack("!HH", data[0:4])

    if type != Parameter_struct["ROSpecStartTrigger"]["type"]:
        return None, data

    body = data[4:length]
    (ROSpecStartTriggerType,) = struct.unpack("!B", body[0:1])
    par["ROSpecStartTriggerType"] = ROSpecStartTriggerType_Type2Name[ROSpecStartTriggerType]
    body = body[1:]
    ret, body = decode("PeriodicTriggerValue")(body)
    if ret:
        par["PeriodicTriggerValue"] = ret
    ret, body = decode("GPITriggerValue")(body)
    if ret:
        par["GPITriggerValue"] = ret
    return par, data[length:]

def decode_PeriodicTriggerValue(data):
    par = {}

    if len(data) == 0:
        return None, data
    type, length = struct.unpack("!HH", data[0:4])

    if type != Parameter_struct["PeriodicTriggerValue"]["type"]:
        return None, data

    body = data[4:length]
    (Offset,) = struct.unpack("!I", body[0:4])
    par["Offset"] = Offset
    body = body[4:]
    (Period,) = struct.unpack("!I", body[0:4])
    par["Period"] = Period
    body = body[4:]
    ret, body = decode("UTCTimestamp")(body)
    if ret:
        par["UTCTimestamp"] = ret
    return par, data[length:]

def decode_GPITriggerValue(data):
    par = {}

    if len(data) == 0:
        return None, data
    type, length = struct.unpack("!HH", data[0:4])

    if type != Parameter_struct["GPITriggerValue"]["type"]:
        return None, data

    body = data[4:length]
    (GPIPortNum,) = struct.unpack("!H", body[0:2])
    par["GPIPortNum"] = GPIPortNum
    body = body[2:]
    (e,) = struct.unpack("!B", body[0:1])
    par["GPIEvent"] = (e>>7)&1
    body = body[1:]
    (Timeout,) = struct.unpack("!I", body[0:4])
    par["Timeout"] = Timeout
    body = body[4:]
    return par, data[length:]

def decode_ROSpecStopTrigger(data):
    par = {}

    if len(data) == 0:
        return None, data
    type, length = struct.unpack("!HH", data[0:4])

    if type != Parameter_struct["ROSpecStopTrigger"]["type"]:
        return None, data

    body = data[4:length]
    (ROSpecStopTriggerType,) = struct.unpack("!B", body[0:1])
    par["ROSpecStopTriggerType"] = ROSpecStopTriggerType_Type2Name[ROSpecStopTriggerType]
    body = body[1:]
    (DurationTriggerValue,) = struct.unpack("!I", body[0:4])
    par["DurationTriggerValue"] = DurationTriggerValue
    body = body[4:]
    ret, body = decode("GPITriggerValue")(body)
    if ret:
        par["GPITriggerValue"] = ret
    return par, data[length:]

def decode_AISpec(data):
    par = {}

    if len(data) == 0:
        return None, data
    type, length = struct.unpack("!HH", data[0:4])

    if type != Parameter_struct["AISpec"]["type"]:
        return None, data

    body = data[4:length]
    (arrayLen, ) = struct.unpack("!H", body[0:2])
    body = body[2:]
    par["AntennaIDs"] = body[0:arrayLen*2]
    body = body[arrayLen*2:]
    ret, body = decode("AISpecStopTrigger")(body)
    if ret:
        par["AISpecStopTrigger"] = ret
    else:
        raise LLRPError("missing AISpecStopTrigger parameter")
    par["InventoryParameterSpec"] = []
    while True:
        ret, body = decode("InventoryParameterSpec")(body)
        if ret:
            par["InventoryParameterSpec"].append(ret)
        else:
            break
    par["Custom"] = []
    while True:
        ret, body = decode("Custom")(body)
        if ret:
            par["Custom"].append(ret)
        else:
            break
    return par, data[length:]

def decode_AISpecStopTrigger(data):
    par = {}

    if len(data) == 0:
        return None, data
    type, length = struct.unpack("!HH", data[0:4])

    if type != Parameter_struct["AISpecStopTrigger"]["type"]:
        return None, data

    body = data[4:length]
    (AISpecStopTriggerType,) = struct.unpack("!B", body[0:1])
    par["AISpecStopTriggerType"] = AISpecStopTriggerType_Type2Name[AISpecStopTriggerType]
    body = body[1:]
    (DurationTrigger,) = struct.unpack("!I", body[0:4])
    par["DurationTrigger"] = DurationTrigger
    body = body[4:]
    ret, body = decode("GPITriggerValue")(body)
    if ret:
        par["GPITriggerValue"] = ret
    ret, body = decode("TagObservationTrigger")(body)
    if ret:
        par["TagObservationTrigger"] = ret
    return par, data[length:]

def decode_TagObservationTrigger(data):
    par = {}

    if len(data) == 0:
        return None, data
    type, length = struct.unpack("!HH", data[0:4])

    if type != Parameter_struct["TagObservationTrigger"]["type"]:
        return None, data

    body = data[4:length]
    (TriggerType,) = struct.unpack("!B", body[0:1])
    par["TriggerType"] = TagObservationTriggerType_Type2Name[TriggerType]
    body = body[1:]
    (NumberOfTags,) = struct.unpack("!H", body[0:2])
    par["NumberOfTags"] = NumberOfTags
    body = body[2:]
    (NumberOfAttempts,) = struct.unpack("!H", body[0:2])
    par["NumberOfAttempts"] = NumberOfAttempts
    body = body[2:]
    (T,) = struct.unpack("!H", body[0:2])
    par["T"] = T
    body = body[2:]
    (Timeout,) = struct.unpack("!I", body[0:4])
    par["Timeout"] = Timeout
    body = body[4:]
    return par, data[length:]

def decode_InventoryParameterSpec(data):
    par = {}

    if len(data) == 0:
        return None, data
    type, length = struct.unpack("!HH", data[0:4])

    if type != Parameter_struct["InventoryParameterSpec"]["type"]:
        return None, data

    body = data[4:length]
    (InventoryParameterSpecID,) = struct.unpack("!H", body[0:2])
    par["InventoryParameterSpecID"] = InventoryParameterSpecID
    body = body[2:]
    (ProtocolID,) = struct.unpack("!B", body[0:1])
    par["ProtocolID"] = AirProtocols_Type2Name[ProtocolID]
    body = body[1:]
    par["AntennaConfiguration"] = []
    while True:
        ret, body = decode("AntennaConfiguration")(body)
        if ret:
            par["AntennaConfiguration"].append(ret)
        else:
            break
    par["Custom"] = []
    while True:
        ret, body = decode("Custom")(body)
        if ret:
            par["Custom"].append(ret)
        else:
            break
    return par, data[length:]

def decode_RFSurveySpec(data):
    par = {}

    if len(data) == 0:
        return None, data
    type, length = struct.unpack("!HH", data[0:4])

    if type != Parameter_struct["RFSurveySpec"]["type"]:
        return None, data

    body = data[4:length]
    (AntennaID,) = struct.unpack("!H", body[0:2])
    par["AntennaID"] = AntennaID
    body = body[2:]
    (StartFrequency,) = struct.unpack("!I", body[0:4])
    par["StartFrequency"] = StartFrequency
    body = body[4:]
    (EndFrequency,) = struct.unpack("!I", body[0:4])
    par["EndFrequency"] = EndFrequency
    body = body[4:]
    ret, body = decode("RFSurveySpecStopTrigger")(body)
    if ret:
        par["RFSurveySpecStopTrigger"] = ret
    else:
        raise LLRPError("missing RFSurveySpecStopTrigger parameter")
    par["Custom"] = []
    while True:
        ret, body = decode("Custom")(body)
        if ret:
            par["Custom"].append(ret)
        else:
            break
    return par, data[length:]

def decode_RFSurveySpecStopTrigger(data):
    par = {}

    if len(data) == 0:
        return None, data
    type, length = struct.unpack("!HH", data[0:4])

    if type != Parameter_struct["RFSurveySpecStopTrigger"]["type"]:
        return None, data

    body = data[4:length]
    (StopTriggerType,) = struct.unpack("!B", body[0:1])
    par["StopTriggerType"] = RFSurveySpecStopTriggerType_Type2Name[StopTriggerType]
    body = body[1:]
    (DurationPeriod,) = struct.unpack("!I", body[0:4])
    par["DurationPeriod"] = DurationPeriod
    body = body[4:]
    (N,) = struct.unpack("!I", body[0:4])
    par["N"] = N
    body = body[4:]
    return par, data[length:]

def decode_AccessSpec(data):
    par = {}

    if len(data) == 0:
        return None, data
    type, length = struct.unpack("!HH", data[0:4])

    if type != Parameter_struct["AccessSpec"]["type"]:
        return None, data

    body = data[4:length]
    (AccessSpecID,) = struct.unpack("!I", body[0:4])
    par["AccessSpecID"] = AccessSpecID
    body = body[4:]
    (AntennaID,) = struct.unpack("!H", body[0:2])
    par["AntennaID"] = AntennaID
    body = body[2:]
    (ProtocolID,) = struct.unpack("!B", body[0:1])
    par["ProtocolID"] = AirProtocols_Type2Name[ProtocolID]
    body = body[1:]
    (e,) = struct.unpack("!B", body[0:1])
    par["CurrentState"] = (e>>7)&1
    body = body[1:]
    (ROSpecID,) = struct.unpack("!I", body[0:4])
    par["ROSpecID"] = ROSpecID
    body = body[4:]
    ret, body = decode("AccessSpecStopTrigger")(body)
    if ret:
        par["AccessSpecStopTrigger"] = ret
    else:
        raise LLRPError("missing AccessSpecStopTrigger parameter")
    ret, body = decode("AccessCommand")(body)
    if ret:
        par["AccessCommand"] = ret
    else:
        raise LLRPError("missing AccessCommand parameter")
    ret, body = decode("AccessReportSpec")(body)
    if ret:
        par["AccessReportSpec"] = ret
    par["Custom"] = []
    while True:
        ret, body = decode("Custom")(body)
        if ret:
            par["Custom"].append(ret)
        else:
            break
    return par, data[length:]

def decode_AccessSpecStopTrigger(data):
    par = {}

    if len(data) == 0:
        return None, data
    type, length = struct.unpack("!HH", data[0:4])

    if type != Parameter_struct["AccessSpecStopTrigger"]["type"]:
        return None, data

    body = data[4:length]
    (AccessSpecStopTrigger,) = struct.unpack("!B", body[0:1])
    par["AccessSpecStopTrigger"] = AccessSpecStopTriggerType_Type2Name[AccessSpecStopTrigger]
    body = body[1:]
    (OperationCountValue,) = struct.unpack("!H", body[0:2])
    par["OperationCountValue"] = OperationCountValue
    body = body[2:]
    return par, data[length:]

def decode_AccessCommand(data):
    par = {}

    if len(data) == 0:
        return None, data
    type, length = struct.unpack("!HH", data[0:4])

    if type != Parameter_struct["AccessCommand"]["type"]:
        return None, data

    body = data[4:length]
    ret, body = decode("C1G2TagSpec")(body)
    if ret:
        par["C1G2TagSpec"] = ret
    
    par["C1G2Read"] = []
    par["C1G2Write"] = []
    par["C1G2Kill"] = []
    par["C1G2Lock"] = []
    par["C1G2BlockErase"] = []
    par["C1G2BlockWrite"] = []
    par["Custom"] = []
    flag = True
    while flag:
        flag = False
        ret, body = decode("C1G2Read")(body)
        if ret:
            par["C1G2Read"].append(ret)
            flag = True
        ret, body = decode("C1G2Write")(body)
        if ret:
            par["C1G2Write"].append(ret)
            flag = True
        ret, body = decode("C1G2Kill")(body)
        if ret:
            par["C1G2Kill"].append(ret)
            flag = True
        ret, body = decode("C1G2Lock")(body)
        if ret:
            par["C1G2Lock"].append(ret)
            flag = True
        ret, body = decode("C1G2BlockErase")(body)
        if ret:
            par["C1G2BlockErase"].append(ret)
            flag = True
        ret, body = decode("C1G2BlockWrite")(body)
        if ret:
            par["C1G2BlockWrite"].append(ret)
            flag = True
        ret, body = decode("Custom")(body)
        if ret:
            par["Custom"].append(ret)
            flag = True
        
    par["Custom"] = []
    while True:
        ret, body = decode("Custom")(body)
        if ret:
            par["Custom"].append(ret)
        else:
            break
    return par, data[length:]

def decode_LLRPConfigurationStateValue(data):
    par = {}

    if len(data) == 0:
        return None, data
    type, length = struct.unpack("!HH", data[0:4])

    if type != Parameter_struct["LLRPConfigurationStateValue"]["type"]:
        return None, data

    body = data[4:length]
    (LLRPConfigurationStateValue,) = struct.unpack("!I", body[0:4])
    par["LLRPConfigurationStateValue"] = LLRPConfigurationStateValue
    body = body[4:]
    return par, data[length:]

def decode_Identification(data):
    par = {}

    if len(data) == 0:
        return None, data
    type, length = struct.unpack("!HH", data[0:4])

    if type != Parameter_struct["Identification"]["type"]:
        return None, data

    body = data[4:length]
    (IDType,) = struct.unpack("!B", body[0:1])
    par["IDType"] = IdentificationType_Type2Name[IDType]
    body = body[1:]
    (arrayLen, ) = struct.unpack("!H", body[0:2])
    body = body[2:]
    par["ReaderID"] = body[0:arrayLen*1]
    body = body[arrayLen*1:]
    return par, data[length:]

def decode_GPOWriteData(data):
    par = {}

    if len(data) == 0:
        return None, data
    type, length = struct.unpack("!HH", data[0:4])

    if type != Parameter_struct["GPOWriteData"]["type"]:
        return None, data

    body = data[4:length]
    (GPOPortNumber,) = struct.unpack("!H", body[0:2])
    par["GPOPortNumber"] = GPOPortNumber
    body = body[2:]
    (e,) = struct.unpack("!B", body[0:1])
    par["GPOData"] = (e>>7)&1
    body = body[1:]
    return par, data[length:]

def decode_KeepaliveSpec(data):
    par = {}

    if len(data) == 0:
        return None, data
    type, length = struct.unpack("!HH", data[0:4])

    if type != Parameter_struct["KeepaliveSpec"]["type"]:
        return None, data

    body = data[4:length]
    (KeepaliveTriggerType,) = struct.unpack("!B", body[0:1])
    par["KeepaliveTriggerType"] = KeepaliveTriggerType_Type2Name[KeepaliveTriggerType]
    body = body[1:]
    (PeriodicTriggerValue,) = struct.unpack("!I", body[0:4])
    par["PeriodicTriggerValue"] = PeriodicTriggerValue
    body = body[4:]
    return par, data[length:]

def decode_AntennaProperties(data):
    par = {}

    if len(data) == 0:
        return None, data
    type, length = struct.unpack("!HH", data[0:4])

    if type != Parameter_struct["AntennaProperties"]["type"]:
        return None, data

    body = data[4:length]
    (e,) = struct.unpack("!B", body[0:1])
    par["AntennaConnected"] = (e>>7)&1
    body = body[1:]
    (AntennaID,) = struct.unpack("!H", body[0:2])
    par["AntennaID"] = AntennaID
    body = body[2:]
    (AntennaGain,) = struct.unpack("!h", body[0:2])
    par["AntennaGain"] = AntennaGain
    body = body[2:]
    return par, data[length:]

def decode_AntennaConfiguration(data):
    par = {}

    if len(data) == 0:
        return None, data
    type, length = struct.unpack("!HH", data[0:4])

    if type != Parameter_struct["AntennaConfiguration"]["type"]:
        return None, data

    body = data[4:length]
    (AntennaID,) = struct.unpack("!H", body[0:2])
    par["AntennaID"] = AntennaID
    body = body[2:]
    ret, body = decode("RFReceiver")(body)
    if ret:
        par["RFReceiver"] = ret
    ret, body = decode("RFTransmitter")(body)
    if ret:
        par["RFTransmitter"] = ret
    par["C1G2InventoryCommand"] = []
    flag = True
    while flag:
        flag = False
        ret, body = decode("C1G2InventoryCommand")(body)
        if ret:
            par["C1G2InventoryCommand"].append(ret)
            flag = True
        
    return par, data[length:]

def decode_RFReceiver(data):
    par = {}

    if len(data) == 0:
        return None, data
    type, length = struct.unpack("!HH", data[0:4])

    if type != Parameter_struct["RFReceiver"]["type"]:
        return None, data

    body = data[4:length]
    (ReceiverSensitivity,) = struct.unpack("!H", body[0:2])
    par["ReceiverSensitivity"] = ReceiverSensitivity
    body = body[2:]
    return par, data[length:]

def decode_RFTransmitter(data):
    par = {}

    if len(data) == 0:
        return None, data
    type, length = struct.unpack("!HH", data[0:4])

    if type != Parameter_struct["RFTransmitter"]["type"]:
        return None, data

    body = data[4:length]
    (HopTableID,) = struct.unpack("!H", body[0:2])
    par["HopTableID"] = HopTableID
    body = body[2:]
    (ChannelIndex,) = struct.unpack("!H", body[0:2])
    par["ChannelIndex"] = ChannelIndex
    body = body[2:]
    (TransmitPower,) = struct.unpack("!H", body[0:2])
    par["TransmitPower"] = TransmitPower
    body = body[2:]
    return par, data[length:]

def decode_GPIPortCurrentState(data):
    par = {}

    if len(data) == 0:
        return None, data
    type, length = struct.unpack("!HH", data[0:4])

    if type != Parameter_struct["GPIPortCurrentState"]["type"]:
        return None, data

    body = data[4:length]
    (GPIPortNum,) = struct.unpack("!H", body[0:2])
    par["GPIPortNum"] = GPIPortNum
    body = body[2:]
    (e,) = struct.unpack("!B", body[0:1])
    par["Config"] = (e>>7)&1
    body = body[1:]
    (State,) = struct.unpack("!B", body[0:1])
    par["State"] = GPIPortState_Type2Name[State]
    body = body[1:]
    return par, data[length:]

def decode_EventsAndReports(data):
    par = {}

    if len(data) == 0:
        return None, data
    type, length = struct.unpack("!HH", data[0:4])

    if type != Parameter_struct["EventsAndReports"]["type"]:
        return None, data

    body = data[4:length]
    (e,) = struct.unpack("!B", body[0:1])
    par["HoldEventsAndReportsUponReconnect"] = (e>>7)&1
    body = body[1:]
    return par, data[length:]

def decode_ROReportSpec(data):
    par = {}

    if len(data) == 0:
        return None, data
    type, length = struct.unpack("!HH", data[0:4])

    if type != Parameter_struct["ROReportSpec"]["type"]:
        return None, data

    body = data[4:length]
    (ROReportTrigger,) = struct.unpack("!B", body[0:1])
    par["ROReportTrigger"] = ROReportTriggerType_Type2Name[ROReportTrigger]
    body = body[1:]
    (N,) = struct.unpack("!H", body[0:2])
    par["N"] = N
    body = body[2:]
    ret, body = decode("TagReportContentSelector")(body)
    if ret:
        par["TagReportContentSelector"] = ret
    else:
        raise LLRPError("missing TagReportContentSelector parameter")
    par["Custom"] = []
    while True:
        ret, body = decode("Custom")(body)
        if ret:
            par["Custom"].append(ret)
        else:
            break
    return par, data[length:]

def decode_TagReportContentSelector(data):
    par = {}

    if len(data) == 0:
        return None, data
    type, length = struct.unpack("!HH", data[0:4])

    if type != Parameter_struct["TagReportContentSelector"]["type"]:
        return None, data

    body = data[4:length]
    (e,) = struct.unpack("!B", body[0:1])
    par["EnableROSpecID"] = (e>>7)&1
    par["EnableSpecIndex"] = (e>>6)&1
    par["EnableInventoryParameterSpecID"] = (e>>5)&1
    par["EnableAntennaID"] = (e>>4)&1
    par["EnableChannelIndex"] = (e>>3)&1
    par["EnablePeakRSSI"] = (e>>2)&1
    par["EnableFirstSeenTimestamp"] = (e>>1)&1
    par["EnableLastSeenTimestamp"] = (e>>0)&1
    body = body[1:]
    (e,) = struct.unpack("!B", body[0:1])
    par["EnableTagSeenCount"] = (e>>7)&1
    par["EnableAccessSpecID"] = (e>>6)&1
    body = body[1:]
    par["C1G2EPCMemorySelector"] = []
    flag = True
    while flag:
        flag = False
        ret, body = decode("C1G2EPCMemorySelector")(body)
        if ret:
            par["C1G2EPCMemorySelector"].append(ret)
            flag = True
        
    return par, data[length:]

def decode_AccessReportSpec(data):
    par = {}

    if len(data) == 0:
        return None, data
    type, length = struct.unpack("!HH", data[0:4])

    if type != Parameter_struct["AccessReportSpec"]["type"]:
        return None, data

    body = data[4:length]
    (AccessReportTrigger,) = struct.unpack("!B", body[0:1])
    par["AccessReportTrigger"] = AccessReportTriggerType_Type2Name[AccessReportTrigger]
    body = body[1:]
    return par, data[length:]

def decode_TagReportData(data):
    par = {}

    if len(data) == 0:
        return None, data
    type, length = struct.unpack("!HH", data[0:4])

    if type != Parameter_struct["TagReportData"]["type"]:
        return None, data

    body = data[4:length]
    ret, body = decode("EPCData")(body)
    if ret:
        par["EPCData"] = ret
    ret, body = decode("EPC_96")(body)
    if ret:
        par["EPC_96"] = ret
    
    ret, body = decode("ROSpecID")(body)
    if ret:
        par["ROSpecID"] = ret
    ret, body = decode("SpecIndex")(body)
    if ret:
        par["SpecIndex"] = ret
    ret, body = decode("InventoryParameterSpecID")(body)
    if ret:
        par["InventoryParameterSpecID"] = ret
    ret, body = decode("AntennaID")(body)
    if ret:
        par["AntennaID"] = ret
    ret, body = decode("PeakRSSI")(body)
    if ret:
        par["PeakRSSI"] = ret
    ret, body = decode("ChannelIndex")(body)
    if ret:
        par["ChannelIndex"] = ret
    ret, body = decode("FirstSeenTimestampUTC")(body)
    if ret:
        par["FirstSeenTimestampUTC"] = ret
    ret, body = decode("FirstSeenTimestampUptime")(body)
    if ret:
        par["FirstSeenTimestampUptime"] = ret
    ret, body = decode("LastSeenTimestampUTC")(body)
    if ret:
        par["LastSeenTimestampUTC"] = ret
    ret, body = decode("LastSeenTimestampUptime")(body)
    if ret:
        par["LastSeenTimestampUptime"] = ret
    ret, body = decode("TagSeenCount")(body)
    if ret:
        par["TagSeenCount"] = ret
    par["C1G2_PC"] = []
    par["C1G2_CRC"] = []
    flag = True
    while flag:
        flag = False
        ret, body = decode("C1G2_PC")(body)
        if ret:
            par["C1G2_PC"].append(ret)
            flag = True
        ret, body = decode("C1G2_CRC")(body)
        if ret:
            par["C1G2_CRC"].append(ret)
            flag = True
        
    ret, body = decode("AccessSpecID")(body)
    if ret:
        par["AccessSpecID"] = ret
    par["C1G2ReadOpSpecResult"] = []
    par["C1G2WriteOpSpecResult"] = []
    par["C1G2KillOpSpecResult"] = []
    par["C1G2LockOpSpecResult"] = []
    par["C1G2BlockEraseOpSpecResult"] = []
    par["C1G2BlockWriteOpSpecResult"] = []
    par["Custom"] = []
    flag = True
    while flag:
        flag = False
        ret, body = decode("C1G2ReadOpSpecResult")(body)
        if ret:
            par["C1G2ReadOpSpecResult"].append(ret)
            flag = True
        ret, body = decode("C1G2WriteOpSpecResult")(body)
        if ret:
            par["C1G2WriteOpSpecResult"].append(ret)
            flag = True
        ret, body = decode("C1G2KillOpSpecResult")(body)
        if ret:
            par["C1G2KillOpSpecResult"].append(ret)
            flag = True
        ret, body = decode("C1G2LockOpSpecResult")(body)
        if ret:
            par["C1G2LockOpSpecResult"].append(ret)
            flag = True
        ret, body = decode("C1G2BlockEraseOpSpecResult")(body)
        if ret:
            par["C1G2BlockEraseOpSpecResult"].append(ret)
            flag = True
        ret, body = decode("C1G2BlockWriteOpSpecResult")(body)
        if ret:
            par["C1G2BlockWriteOpSpecResult"].append(ret)
            flag = True
        ret, body = decode("Custom")(body)
        if ret:
            par["Custom"].append(ret)
            flag = True
        
    par["Custom"] = []
    while True:
        ret, body = decode("Custom")(body)
        if ret:
            par["Custom"].append(ret)
        else:
            break
    return par, data[length:]

def decode_EPCData(data):
    par = {}

    if len(data) == 0:
        return None, data
    type, length = struct.unpack("!HH", data[0:4])

    if type != Parameter_struct["EPCData"]["type"]:
        return None, data

    body = data[4:length]
    (bitArrayLen, ) = struct.unpack("!H", body[0:2])
    par["EPC"]["BitLen"] = bitArrayLen
    body = body[2:]
    if (bitArrayLen%8) == 0:
        bitArrayLen  = bitArrayLen/8
    else:
        bitArrayLen = bitArrayLen/8 + 1
    par["EPC"]["Data"] = body[0:bitArrayLen]
    body = body[bitArrayLen:]
    return par, data[length:]

def decode_EPC_96(data):
    par = {}

    if len(data) == 0:
        return None, data
    type, length = struct.unpack("!HH", data[0:4])

    if type != Parameter_struct["EPC_96"]["type"]:
        return None, data

    body = data[4:length]
    (arrayLen, ) = struct.unpack("!H", body[0:2])
    body = body[2:]
    par["EPC"] = body[0:arrayLen*1]
    body = body[arrayLen*1:]
    return par, data[length:]

def decode_ROSpecID(data):
    par = {}

    if len(data) == 0:
        return None, data
    type, length = struct.unpack("!HH", data[0:4])

    if type != Parameter_struct["ROSpecID"]["type"]:
        return None, data

    body = data[4:length]
    (ROSpecID,) = struct.unpack("!I", body[0:4])
    par["ROSpecID"] = ROSpecID
    body = body[4:]
    return par, data[length:]

def decode_SpecIndex(data):
    par = {}

    if len(data) == 0:
        return None, data
    type, length = struct.unpack("!HH", data[0:4])

    if type != Parameter_struct["SpecIndex"]["type"]:
        return None, data

    body = data[4:length]
    (SpecIndex,) = struct.unpack("!H", body[0:2])
    par["SpecIndex"] = SpecIndex
    body = body[2:]
    return par, data[length:]

def decode_InventoryParameterSpecID(data):
    par = {}

    if len(data) == 0:
        return None, data
    type, length = struct.unpack("!HH", data[0:4])

    if type != Parameter_struct["InventoryParameterSpecID"]["type"]:
        return None, data

    body = data[4:length]
    (InventoryParameterSpecID,) = struct.unpack("!H", body[0:2])
    par["InventoryParameterSpecID"] = InventoryParameterSpecID
    body = body[2:]
    return par, data[length:]

def decode_AntennaID(data):
    par = {}

    if len(data) == 0:
        return None, data
    type, length = struct.unpack("!HH", data[0:4])

    if type != Parameter_struct["AntennaID"]["type"]:
        return None, data

    body = data[4:length]
    (AntennaID,) = struct.unpack("!H", body[0:2])
    par["AntennaID"] = AntennaID
    body = body[2:]
    return par, data[length:]

def decode_PeakRSSI(data):
    par = {}

    if len(data) == 0:
        return None, data
    type, length = struct.unpack("!HH", data[0:4])

    if type != Parameter_struct["PeakRSSI"]["type"]:
        return None, data

    body = data[4:length]
    (PeakRSSI,) = struct.unpack("!b", body[0:1])
    par["PeakRSSI"] = PeakRSSI
    body = body[1:]
    return par, data[length:]

def decode_ChannelIndex(data):
    par = {}

    if len(data) == 0:
        return None, data
    type, length = struct.unpack("!HH", data[0:4])

    if type != Parameter_struct["ChannelIndex"]["type"]:
        return None, data

    body = data[4:length]
    (ChannelIndex,) = struct.unpack("!H", body[0:2])
    par["ChannelIndex"] = ChannelIndex
    body = body[2:]
    return par, data[length:]

def decode_FirstSeenTimestampUTC(data):
    par = {}

    if len(data) == 0:
        return None, data
    type, length = struct.unpack("!HH", data[0:4])

    if type != Parameter_struct["FirstSeenTimestampUTC"]["type"]:
        return None, data

    body = data[4:length]
    (Microseconds,) = struct.unpack("!Q", body[0:8])
    par["Microseconds"] = Microseconds
    body = body[8:]
    return par, data[length:]

def decode_FirstSeenTimestampUptime(data):
    par = {}

    if len(data) == 0:
        return None, data
    type, length = struct.unpack("!HH", data[0:4])

    if type != Parameter_struct["FirstSeenTimestampUptime"]["type"]:
        return None, data

    body = data[4:length]
    (Microseconds,) = struct.unpack("!Q", body[0:8])
    par["Microseconds"] = Microseconds
    body = body[8:]
    return par, data[length:]

def decode_LastSeenTimestampUTC(data):
    par = {}

    if len(data) == 0:
        return None, data
    type, length = struct.unpack("!HH", data[0:4])

    if type != Parameter_struct["LastSeenTimestampUTC"]["type"]:
        return None, data

    body = data[4:length]
    (Microseconds,) = struct.unpack("!Q", body[0:8])
    par["Microseconds"] = Microseconds
    body = body[8:]
    return par, data[length:]

def decode_LastSeenTimestampUptime(data):
    par = {}

    if len(data) == 0:
        return None, data
    type, length = struct.unpack("!HH", data[0:4])

    if type != Parameter_struct["LastSeenTimestampUptime"]["type"]:
        return None, data

    body = data[4:length]
    (Microseconds,) = struct.unpack("!Q", body[0:8])
    par["Microseconds"] = Microseconds
    body = body[8:]
    return par, data[length:]

def decode_TagSeenCount(data):
    par = {}

    if len(data) == 0:
        return None, data
    type, length = struct.unpack("!HH", data[0:4])

    if type != Parameter_struct["TagSeenCount"]["type"]:
        return None, data

    body = data[4:length]
    (TagCount,) = struct.unpack("!H", body[0:2])
    par["TagCount"] = TagCount
    body = body[2:]
    return par, data[length:]

def decode_AccessSpecID(data):
    par = {}

    if len(data) == 0:
        return None, data
    type, length = struct.unpack("!HH", data[0:4])

    if type != Parameter_struct["AccessSpecID"]["type"]:
        return None, data

    body = data[4:length]
    (AccessSpecID,) = struct.unpack("!I", body[0:4])
    par["AccessSpecID"] = AccessSpecID
    body = body[4:]
    return par, data[length:]

def decode_RFSurveyReportData(data):
    par = {}

    if len(data) == 0:
        return None, data
    type, length = struct.unpack("!HH", data[0:4])

    if type != Parameter_struct["RFSurveyReportData"]["type"]:
        return None, data

    body = data[4:length]
    ret, body = decode("ROSpecID")(body)
    if ret:
        par["ROSpecID"] = ret
    ret, body = decode("SpecIndex")(body)
    if ret:
        par["SpecIndex"] = ret
    par["FrequencyRSSILevelEntry"] = []
    while True:
        ret, body = decode("FrequencyRSSILevelEntry")(body)
        if ret:
            par["FrequencyRSSILevelEntry"].append(ret)
        else:
            break
    par["Custom"] = []
    while True:
        ret, body = decode("Custom")(body)
        if ret:
            par["Custom"].append(ret)
        else:
            break
    return par, data[length:]

def decode_FrequencyRSSILevelEntry(data):
    par = {}

    if len(data) == 0:
        return None, data
    type, length = struct.unpack("!HH", data[0:4])

    if type != Parameter_struct["FrequencyRSSILevelEntry"]["type"]:
        return None, data

    body = data[4:length]
    (Frequency,) = struct.unpack("!I", body[0:4])
    par["Frequency"] = Frequency
    body = body[4:]
    (Bandwidth,) = struct.unpack("!I", body[0:4])
    par["Bandwidth"] = Bandwidth
    body = body[4:]
    (AverageRSSI,) = struct.unpack("!b", body[0:1])
    par["AverageRSSI"] = AverageRSSI
    body = body[1:]
    (PeakRSSI,) = struct.unpack("!b", body[0:1])
    par["PeakRSSI"] = PeakRSSI
    body = body[1:]
    ret, body = decode("UTCTimestamp")(body)
    if ret:
        par["UTCTimestamp"] = ret
    ret, body = decode("Uptime")(body)
    if ret:
        par["Uptime"] = ret
    
    return par, data[length:]

def decode_ReaderEventNotificationSpec(data):
    par = {}

    if len(data) == 0:
        return None, data
    type, length = struct.unpack("!HH", data[0:4])

    if type != Parameter_struct["ReaderEventNotificationSpec"]["type"]:
        return None, data

    body = data[4:length]
    par["EventNotificationState"] = []
    while True:
        ret, body = decode("EventNotificationState")(body)
        if ret:
            par["EventNotificationState"].append(ret)
        else:
            break
    return par, data[length:]

def decode_EventNotificationState(data):
    par = {}

    if len(data) == 0:
        return None, data
    type, length = struct.unpack("!HH", data[0:4])

    if type != Parameter_struct["EventNotificationState"]["type"]:
        return None, data

    body = data[4:length]
    (EventType,) = struct.unpack("!H", body[0:2])
    par["EventType"] = NotificationEventType_Type2Name[EventType]
    body = body[2:]
    (e,) = struct.unpack("!B", body[0:1])
    par["NotificationState"] = (e>>7)&1
    body = body[1:]
    return par, data[length:]

def decode_ReaderEventNotificationData(data):
    par = {}

    if len(data) == 0:
        return None, data
    type, length = struct.unpack("!HH", data[0:4])

    if type != Parameter_struct["ReaderEventNotificationData"]["type"]:
        return None, data

    body = data[4:length]
    ret, body = decode("UTCTimestamp")(body)
    if ret:
        par["UTCTimestamp"] = ret
    ret, body = decode("Uptime")(body)
    if ret:
        par["Uptime"] = ret
    
    ret, body = decode("HoppingEvent")(body)
    if ret:
        par["HoppingEvent"] = ret
    ret, body = decode("GPIEvent")(body)
    if ret:
        par["GPIEvent"] = ret
    ret, body = decode("ROSpecEvent")(body)
    if ret:
        par["ROSpecEvent"] = ret
    ret, body = decode("ReportBufferLevelWarningEvent")(body)
    if ret:
        par["ReportBufferLevelWarningEvent"] = ret
    ret, body = decode("ReportBufferOverflowErrorEvent")(body)
    if ret:
        par["ReportBufferOverflowErrorEvent"] = ret
    ret, body = decode("ReaderExceptionEvent")(body)
    if ret:
        par["ReaderExceptionEvent"] = ret
    ret, body = decode("RFSurveyEvent")(body)
    if ret:
        par["RFSurveyEvent"] = ret
    ret, body = decode("AISpecEvent")(body)
    if ret:
        par["AISpecEvent"] = ret
    ret, body = decode("AntennaEvent")(body)
    if ret:
        par["AntennaEvent"] = ret
    ret, body = decode("ConnectionAttemptEvent")(body)
    if ret:
        par["ConnectionAttemptEvent"] = ret
    ret, body = decode("ConnectionCloseEvent")(body)
    if ret:
        par["ConnectionCloseEvent"] = ret
    par["Custom"] = []
    while True:
        ret, body = decode("Custom")(body)
        if ret:
            par["Custom"].append(ret)
        else:
            break
    return par, data[length:]

def decode_HoppingEvent(data):
    par = {}

    if len(data) == 0:
        return None, data
    type, length = struct.unpack("!HH", data[0:4])

    if type != Parameter_struct["HoppingEvent"]["type"]:
        return None, data

    body = data[4:length]
    (HopTableID,) = struct.unpack("!H", body[0:2])
    par["HopTableID"] = HopTableID
    body = body[2:]
    (NextChannelIndex,) = struct.unpack("!H", body[0:2])
    par["NextChannelIndex"] = NextChannelIndex
    body = body[2:]
    return par, data[length:]

def decode_GPIEvent(data):
    par = {}

    if len(data) == 0:
        return None, data
    type, length = struct.unpack("!HH", data[0:4])

    if type != Parameter_struct["GPIEvent"]["type"]:
        return None, data

    body = data[4:length]
    (GPIPortNumber,) = struct.unpack("!H", body[0:2])
    par["GPIPortNumber"] = GPIPortNumber
    body = body[2:]
    (e,) = struct.unpack("!B", body[0:1])
    par["GPIEvent"] = (e>>7)&1
    body = body[1:]
    return par, data[length:]

def decode_ROSpecEvent(data):
    par = {}

    if len(data) == 0:
        return None, data
    type, length = struct.unpack("!HH", data[0:4])

    if type != Parameter_struct["ROSpecEvent"]["type"]:
        return None, data

    body = data[4:length]
    (EventType,) = struct.unpack("!B", body[0:1])
    par["EventType"] = ROSpecEventType_Type2Name[EventType]
    body = body[1:]
    (ROSpecID,) = struct.unpack("!I", body[0:4])
    par["ROSpecID"] = ROSpecID
    body = body[4:]
    (PreemptingROSpecID,) = struct.unpack("!I", body[0:4])
    par["PreemptingROSpecID"] = PreemptingROSpecID
    body = body[4:]
    return par, data[length:]

def decode_ReportBufferLevelWarningEvent(data):
    par = {}

    if len(data) == 0:
        return None, data
    type, length = struct.unpack("!HH", data[0:4])

    if type != Parameter_struct["ReportBufferLevelWarningEvent"]["type"]:
        return None, data

    body = data[4:length]
    (ReportBufferPercentageFull,) = struct.unpack("!B", body[0:1])
    par["ReportBufferPercentageFull"] = ReportBufferPercentageFull
    body = body[1:]
    return par, data[length:]

def decode_ReportBufferOverflowErrorEvent(data):
    par = {}

    if len(data) == 0:
        return None, data
    type, length = struct.unpack("!HH", data[0:4])

    if type != Parameter_struct["ReportBufferOverflowErrorEvent"]["type"]:
        return None, data

    body = data[4:length]
    return par, data[length:]

def decode_ReaderExceptionEvent(data):
    par = {}

    if len(data) == 0:
        return None, data
    type, length = struct.unpack("!HH", data[0:4])

    if type != Parameter_struct["ReaderExceptionEvent"]["type"]:
        return None, data

    body = data[4:length]
    (arrayLen, ) = struct.unpack("!H", body[0:2])
    body = body[2:]
    par["Message"] = body[0:arrayLen*1]
    body = body[arrayLen*1:]
    ret, body = decode("ROSpecID")(body)
    if ret:
        par["ROSpecID"] = ret
    ret, body = decode("SpecIndex")(body)
    if ret:
        par["SpecIndex"] = ret
    ret, body = decode("InventoryParameterSpecID")(body)
    if ret:
        par["InventoryParameterSpecID"] = ret
    ret, body = decode("AntennaID")(body)
    if ret:
        par["AntennaID"] = ret
    ret, body = decode("AccessSpecID")(body)
    if ret:
        par["AccessSpecID"] = ret
    ret, body = decode("OpSpecID")(body)
    if ret:
        par["OpSpecID"] = ret
    par["Custom"] = []
    while True:
        ret, body = decode("Custom")(body)
        if ret:
            par["Custom"].append(ret)
        else:
            break
    return par, data[length:]

def decode_OpSpecID(data):
    par = {}

    if len(data) == 0:
        return None, data
    type, length = struct.unpack("!HH", data[0:4])

    if type != Parameter_struct["OpSpecID"]["type"]:
        return None, data

    body = data[4:length]
    (OpSpecID,) = struct.unpack("!H", body[0:2])
    par["OpSpecID"] = OpSpecID
    body = body[2:]
    return par, data[length:]

def decode_RFSurveyEvent(data):
    par = {}

    if len(data) == 0:
        return None, data
    type, length = struct.unpack("!HH", data[0:4])

    if type != Parameter_struct["RFSurveyEvent"]["type"]:
        return None, data

    body = data[4:length]
    (EventType,) = struct.unpack("!B", body[0:1])
    par["EventType"] = RFSurveyEventType_Type2Name[EventType]
    body = body[1:]
    (ROSpecID,) = struct.unpack("!I", body[0:4])
    par["ROSpecID"] = ROSpecID
    body = body[4:]
    (SpecIndex,) = struct.unpack("!H", body[0:2])
    par["SpecIndex"] = SpecIndex
    body = body[2:]
    return par, data[length:]

def decode_AISpecEvent(data):
    par = {}

    if len(data) == 0:
        return None, data
    type, length = struct.unpack("!HH", data[0:4])

    if type != Parameter_struct["AISpecEvent"]["type"]:
        return None, data

    body = data[4:length]
    (EventType,) = struct.unpack("!B", body[0:1])
    par["EventType"] = AISpecEventType_Type2Name[EventType]
    body = body[1:]
    (ROSpecID,) = struct.unpack("!I", body[0:4])
    par["ROSpecID"] = ROSpecID
    body = body[4:]
    (SpecIndex,) = struct.unpack("!H", body[0:2])
    par["SpecIndex"] = SpecIndex
    body = body[2:]
    ret, body = decode("C1G2SingulationDetails")(body)
    if ret:
        par["C1G2SingulationDetails"] = ret
    
    return par, data[length:]

def decode_AntennaEvent(data):
    par = {}

    if len(data) == 0:
        return None, data
    type, length = struct.unpack("!HH", data[0:4])

    if type != Parameter_struct["AntennaEvent"]["type"]:
        return None, data

    body = data[4:length]
    (EventType,) = struct.unpack("!B", body[0:1])
    par["EventType"] = AntennaEventType_Type2Name[EventType]
    body = body[1:]
    (AntennaID,) = struct.unpack("!H", body[0:2])
    par["AntennaID"] = AntennaID
    body = body[2:]
    return par, data[length:]

def decode_ConnectionAttemptEvent(data):
    par = {}

    if len(data) == 0:
        return None, data
    type, length = struct.unpack("!HH", data[0:4])

    if type != Parameter_struct["ConnectionAttemptEvent"]["type"]:
        return None, data

    body = data[4:length]
    (Status,) = struct.unpack("!H", body[0:2])
    par["Status"] = ConnectionAttemptStatusType_Type2Name[Status]
    body = body[2:]
    return par, data[length:]

def decode_ConnectionCloseEvent(data):
    par = {}

    if len(data) == 0:
        return None, data
    type, length = struct.unpack("!HH", data[0:4])

    if type != Parameter_struct["ConnectionCloseEvent"]["type"]:
        return None, data

    body = data[4:length]
    return par, data[length:]

def decode_LLRPStatus(data):
    par = {}

    if len(data) == 0:
        return None, data
    type, length = struct.unpack("!HH", data[0:4])

    if type != Parameter_struct["LLRPStatus"]["type"]:
        return None, data

    body = data[4:length]
    (StatusCode,) = struct.unpack("!H", body[0:2])
    par["StatusCode"] = StatusCode_Type2Name[StatusCode]
    body = body[2:]
    (arrayLen, ) = struct.unpack("!H", body[0:2])
    body = body[2:]
    par["ErrorDescription"] = body[0:arrayLen*1]
    body = body[arrayLen*1:]
    ret, body = decode("FieldError")(body)
    if ret:
        par["FieldError"] = ret
    ret, body = decode("ParameterError")(body)
    if ret:
        par["ParameterError"] = ret
    return par, data[length:]

def decode_FieldError(data):
    par = {}

    if len(data) == 0:
        return None, data
    type, length = struct.unpack("!HH", data[0:4])

    if type != Parameter_struct["FieldError"]["type"]:
        return None, data

    body = data[4:length]
    (FieldNum,) = struct.unpack("!H", body[0:2])
    par["FieldNum"] = FieldNum
    body = body[2:]
    (ErrorCode,) = struct.unpack("!H", body[0:2])
    par["ErrorCode"] = StatusCode_Type2Name[ErrorCode]
    body = body[2:]
    return par, data[length:]

def decode_ParameterError(data):
    par = {}

    if len(data) == 0:
        return None, data
    type, length = struct.unpack("!HH", data[0:4])

    if type != Parameter_struct["ParameterError"]["type"]:
        return None, data

    body = data[4:length]
    (ParameterType,) = struct.unpack("!H", body[0:2])
    par["ParameterType"] = ParameterType
    body = body[2:]
    (ErrorCode,) = struct.unpack("!H", body[0:2])
    par["ErrorCode"] = StatusCode_Type2Name[ErrorCode]
    body = body[2:]
    ret, body = decode("FieldError")(body)
    if ret:
        par["FieldError"] = ret
    ret, body = decode("ParameterError")(body)
    if ret:
        par["ParameterError"] = ret
    return par, data[length:]

def decode_C1G2LLRPCapabilities(data):
    par = {}

    if len(data) == 0:
        return None, data
    type, length = struct.unpack("!HH", data[0:4])

    if type != Parameter_struct["C1G2LLRPCapabilities"]["type"]:
        return None, data

    body = data[4:length]
    (e,) = struct.unpack("!B", body[0:1])
    par["CanSupportBlockErase"] = (e>>7)&1
    par["CanSupportBlockWrite"] = (e>>6)&1
    body = body[1:]
    (MaxNumSelectFiltersPerQuery,) = struct.unpack("!H", body[0:2])
    par["MaxNumSelectFiltersPerQuery"] = MaxNumSelectFiltersPerQuery
    body = body[2:]
    return par, data[length:]

def decode_C1G2UHFRFModeTable(data):
    par = {}

    if len(data) == 0:
        return None, data
    type, length = struct.unpack("!HH", data[0:4])

    if type != Parameter_struct["C1G2UHFRFModeTable"]["type"]:
        return None, data

    body = data[4:length]
    par["C1G2UHFRFModeTableEntry"] = []
    while True:
        ret, body = decode("C1G2UHFRFModeTableEntry")(body)
        if ret:
            par["C1G2UHFRFModeTableEntry"].append(ret)
        else:
            break
    return par, data[length:]

def decode_C1G2UHFRFModeTableEntry(data):
    par = {}

    if len(data) == 0:
        return None, data
    type, length = struct.unpack("!HH", data[0:4])

    if type != Parameter_struct["C1G2UHFRFModeTableEntry"]["type"]:
        return None, data

    body = data[4:length]
    (ModeIdentifier,) = struct.unpack("!I", body[0:4])
    par["ModeIdentifier"] = ModeIdentifier
    body = body[4:]
    (e,) = struct.unpack("!B", body[0:1])
    par["DRValue"] = (e>>7)&1
    par["EPCHAGTCConformance"] = (e>>6)&1
    body = body[1:]
    (MValue,) = struct.unpack("!B", body[0:1])
    par["MValue"] = C1G2MValue_Type2Name[MValue]
    body = body[1:]
    (ForwardLinkModulation,) = struct.unpack("!B", body[0:1])
    par["ForwardLinkModulation"] = C1G2ForwardLinkModulation_Type2Name[ForwardLinkModulation]
    body = body[1:]
    (SpectralMaskIndicator,) = struct.unpack("!B", body[0:1])
    par["SpectralMaskIndicator"] = C1G2SpectralMaskIndicator_Type2Name[SpectralMaskIndicator]
    body = body[1:]
    (BDRValue,) = struct.unpack("!I", body[0:4])
    par["BDRValue"] = BDRValue
    body = body[4:]
    (PIEValue,) = struct.unpack("!I", body[0:4])
    par["PIEValue"] = PIEValue
    body = body[4:]
    (MinTariValue,) = struct.unpack("!I", body[0:4])
    par["MinTariValue"] = MinTariValue
    body = body[4:]
    (MaxTariValue,) = struct.unpack("!I", body[0:4])
    par["MaxTariValue"] = MaxTariValue
    body = body[4:]
    (StepTariValue,) = struct.unpack("!I", body[0:4])
    par["StepTariValue"] = StepTariValue
    body = body[4:]
    return par, data[length:]

def decode_C1G2InventoryCommand(data):
    par = {}

    if len(data) == 0:
        return None, data
    type, length = struct.unpack("!HH", data[0:4])

    if type != Parameter_struct["C1G2InventoryCommand"]["type"]:
        return None, data

    body = data[4:length]
    (e,) = struct.unpack("!B", body[0:1])
    par["TagInventoryStateAware"] = (e>>7)&1
    body = body[1:]
    par["C1G2Filter"] = []
    while True:
        ret, body = decode("C1G2Filter")(body)
        if ret:
            par["C1G2Filter"].append(ret)
        else:
            break
    ret, body = decode("C1G2RFControl")(body)
    if ret:
        par["C1G2RFControl"] = ret
    ret, body = decode("C1G2SingulationControl")(body)
    if ret:
        par["C1G2SingulationControl"] = ret
    par["Custom"] = []
    while True:
        ret, body = decode("Custom")(body)
        if ret:
            par["Custom"].append(ret)
        else:
            break
    return par, data[length:]

def decode_C1G2Filter(data):
    par = {}

    if len(data) == 0:
        return None, data
    type, length = struct.unpack("!HH", data[0:4])

    if type != Parameter_struct["C1G2Filter"]["type"]:
        return None, data

    body = data[4:length]
    (arrayLen, ) = struct.unpack("!H", body[0:2])
    body = body[2:]
    par["T"] = body[0:arrayLen*1]
    body = body[arrayLen*1:]
    ret, body = decode("C1G2TagInventoryMask")(body)
    if ret:
        par["C1G2TagInventoryMask"] = ret
    else:
        raise LLRPError("missing C1G2TagInventoryMask parameter")
    ret, body = decode("C1G2TagInventoryStateAwareFilterAction")(body)
    if ret:
        par["C1G2TagInventoryStateAwareFilterAction"] = ret
    ret, body = decode("C1G2TagInventoryStateUnawareFilterAction")(body)
    if ret:
        par["C1G2TagInventoryStateUnawareFilterAction"] = ret
    return par, data[length:]

def decode_C1G2TagInventoryMask(data):
    par = {}

    if len(data) == 0:
        return None, data
    type, length = struct.unpack("!HH", data[0:4])

    if type != Parameter_struct["C1G2TagInventoryMask"]["type"]:
        return None, data

    body = data[4:length]
    (arrayLen, ) = struct.unpack("!H", body[0:2])
    body = body[2:]
    par["MB"] = body[0:arrayLen*1]
    body = body[arrayLen*1:]
    (Pointer,) = struct.unpack("!H", body[0:2])
    par["Pointer"] = Pointer
    body = body[2:]
    (bitArrayLen, ) = struct.unpack("!H", body[0:2])
    par["TagMask"]["BitLen"] = bitArrayLen
    body = body[2:]
    if (bitArrayLen%8) == 0:
        bitArrayLen  = bitArrayLen/8
    else:
        bitArrayLen = bitArrayLen/8 + 1
    par["TagMask"]["Data"] = body[0:bitArrayLen]
    body = body[bitArrayLen:]
    return par, data[length:]

def decode_C1G2TagInventoryStateAwareFilterAction(data):
    par = {}

    if len(data) == 0:
        return None, data
    type, length = struct.unpack("!HH", data[0:4])

    if type != Parameter_struct["C1G2TagInventoryStateAwareFilterAction"]["type"]:
        return None, data

    body = data[4:length]
    (Target,) = struct.unpack("!B", body[0:1])
    par["Target"] = C1G2StateAwareTarget_Type2Name[Target]
    body = body[1:]
    (Action,) = struct.unpack("!B", body[0:1])
    par["Action"] = C1G2StateAwareAction_Type2Name[Action]
    body = body[1:]
    return par, data[length:]

def decode_C1G2TagInventoryStateUnawareFilterAction(data):
    par = {}

    if len(data) == 0:
        return None, data
    type, length = struct.unpack("!HH", data[0:4])

    if type != Parameter_struct["C1G2TagInventoryStateUnawareFilterAction"]["type"]:
        return None, data

    body = data[4:length]
    (Action,) = struct.unpack("!B", body[0:1])
    par["Action"] = C1G2StateUnawareAction_Type2Name[Action]
    body = body[1:]
    return par, data[length:]

def decode_C1G2RFControl(data):
    par = {}

    if len(data) == 0:
        return None, data
    type, length = struct.unpack("!HH", data[0:4])

    if type != Parameter_struct["C1G2RFControl"]["type"]:
        return None, data

    body = data[4:length]
    (ModeIndex,) = struct.unpack("!H", body[0:2])
    par["ModeIndex"] = ModeIndex
    body = body[2:]
    (Tari,) = struct.unpack("!H", body[0:2])
    par["Tari"] = Tari
    body = body[2:]
    return par, data[length:]

def decode_C1G2SingulationControl(data):
    par = {}

    if len(data) == 0:
        return None, data
    type, length = struct.unpack("!HH", data[0:4])

    if type != Parameter_struct["C1G2SingulationControl"]["type"]:
        return None, data

    body = data[4:length]
    (arrayLen, ) = struct.unpack("!H", body[0:2])
    body = body[2:]
    par["Session"] = body[0:arrayLen*1]
    body = body[arrayLen*1:]
    (TagPopulation,) = struct.unpack("!H", body[0:2])
    par["TagPopulation"] = TagPopulation
    body = body[2:]
    (TagTransitTime,) = struct.unpack("!I", body[0:4])
    par["TagTransitTime"] = TagTransitTime
    body = body[4:]
    ret, body = decode("C1G2TagInventoryStateAwareSingulationAction")(body)
    if ret:
        par["C1G2TagInventoryStateAwareSingulationAction"] = ret
    return par, data[length:]

def decode_C1G2TagInventoryStateAwareSingulationAction(data):
    par = {}

    if len(data) == 0:
        return None, data
    type, length = struct.unpack("!HH", data[0:4])

    if type != Parameter_struct["C1G2TagInventoryStateAwareSingulationAction"]["type"]:
        return None, data

    body = data[4:length]
    (e,) = struct.unpack("!B", body[0:1])
    par["I"] = (e>>7)&1
    par["S"] = (e>>6)&1
    body = body[1:]
    return par, data[length:]

def decode_C1G2TagSpec(data):
    par = {}

    if len(data) == 0:
        return None, data
    type, length = struct.unpack("!HH", data[0:4])

    if type != Parameter_struct["C1G2TagSpec"]["type"]:
        return None, data

    body = data[4:length]
    par["C1G2TargetTag"] = []
    while True:
        ret, body = decode("C1G2TargetTag")(body)
        if ret:
            par["C1G2TargetTag"].append(ret)
        else:
            break
    return par, data[length:]

def decode_C1G2TargetTag(data):
    par = {}

    if len(data) == 0:
        return None, data
    type, length = struct.unpack("!HH", data[0:4])

    if type != Parameter_struct["C1G2TargetTag"]["type"]:
        return None, data

    body = data[4:length]
    (arrayLen, ) = struct.unpack("!H", body[0:2])
    body = body[2:]
    par["MB"] = body[0:arrayLen*1]
    body = body[arrayLen*1:]
    (e,) = struct.unpack("!B", body[0:1])
    par["Match"] = (e>>7)&1
    body = body[1:]
    (Pointer,) = struct.unpack("!H", body[0:2])
    par["Pointer"] = Pointer
    body = body[2:]
    (bitArrayLen, ) = struct.unpack("!H", body[0:2])
    par["TagMask"]["BitLen"] = bitArrayLen
    body = body[2:]
    if (bitArrayLen%8) == 0:
        bitArrayLen  = bitArrayLen/8
    else:
        bitArrayLen = bitArrayLen/8 + 1
    par["TagMask"]["Data"] = body[0:bitArrayLen]
    body = body[bitArrayLen:]
    (bitArrayLen, ) = struct.unpack("!H", body[0:2])
    par["TagData"]["BitLen"] = bitArrayLen
    body = body[2:]
    if (bitArrayLen%8) == 0:
        bitArrayLen  = bitArrayLen/8
    else:
        bitArrayLen = bitArrayLen/8 + 1
    par["TagData"]["Data"] = body[0:bitArrayLen]
    body = body[bitArrayLen:]
    return par, data[length:]

def decode_C1G2Read(data):
    par = {}

    if len(data) == 0:
        return None, data
    type, length = struct.unpack("!HH", data[0:4])

    if type != Parameter_struct["C1G2Read"]["type"]:
        return None, data

    body = data[4:length]
    (OpSpecID,) = struct.unpack("!H", body[0:2])
    par["OpSpecID"] = OpSpecID
    body = body[2:]
    (AccessPassword,) = struct.unpack("!I", body[0:4])
    par["AccessPassword"] = AccessPassword
    body = body[4:]
    (arrayLen, ) = struct.unpack("!H", body[0:2])
    body = body[2:]
    par["MB"] = body[0:arrayLen*1]
    body = body[arrayLen*1:]
    (WordPointer,) = struct.unpack("!H", body[0:2])
    par["WordPointer"] = WordPointer
    body = body[2:]
    (WordCount,) = struct.unpack("!H", body[0:2])
    par["WordCount"] = WordCount
    body = body[2:]
    return par, data[length:]

def decode_C1G2Write(data):
    par = {}

    if len(data) == 0:
        return None, data
    type, length = struct.unpack("!HH", data[0:4])

    if type != Parameter_struct["C1G2Write"]["type"]:
        return None, data

    body = data[4:length]
    (OpSpecID,) = struct.unpack("!H", body[0:2])
    par["OpSpecID"] = OpSpecID
    body = body[2:]
    (AccessPassword,) = struct.unpack("!I", body[0:4])
    par["AccessPassword"] = AccessPassword
    body = body[4:]
    (arrayLen, ) = struct.unpack("!H", body[0:2])
    body = body[2:]
    par["MB"] = body[0:arrayLen*1]
    body = body[arrayLen*1:]
    (WordPointer,) = struct.unpack("!H", body[0:2])
    par["WordPointer"] = WordPointer
    body = body[2:]
    (arrayLen, ) = struct.unpack("!H", body[0:2])
    body = body[2:]
    par["WriteData"] = body[0:arrayLen*2]
    body = body[arrayLen*2:]
    return par, data[length:]

def decode_C1G2Kill(data):
    par = {}

    if len(data) == 0:
        return None, data
    type, length = struct.unpack("!HH", data[0:4])

    if type != Parameter_struct["C1G2Kill"]["type"]:
        return None, data

    body = data[4:length]
    (OpSpecID,) = struct.unpack("!H", body[0:2])
    par["OpSpecID"] = OpSpecID
    body = body[2:]
    (KillPassword,) = struct.unpack("!I", body[0:4])
    par["KillPassword"] = KillPassword
    body = body[4:]
    return par, data[length:]

def decode_C1G2Lock(data):
    par = {}

    if len(data) == 0:
        return None, data
    type, length = struct.unpack("!HH", data[0:4])

    if type != Parameter_struct["C1G2Lock"]["type"]:
        return None, data

    body = data[4:length]
    (OpSpecID,) = struct.unpack("!H", body[0:2])
    par["OpSpecID"] = OpSpecID
    body = body[2:]
    (AccessPassword,) = struct.unpack("!I", body[0:4])
    par["AccessPassword"] = AccessPassword
    body = body[4:]
    par["C1G2LockPayload"] = []
    while True:
        ret, body = decode("C1G2LockPayload")(body)
        if ret:
            par["C1G2LockPayload"].append(ret)
        else:
            break
    return par, data[length:]

def decode_C1G2LockPayload(data):
    par = {}

    if len(data) == 0:
        return None, data
    type, length = struct.unpack("!HH", data[0:4])

    if type != Parameter_struct["C1G2LockPayload"]["type"]:
        return None, data

    body = data[4:length]
    (Privilege,) = struct.unpack("!B", body[0:1])
    par["Privilege"] = C1G2LockPrivilege_Type2Name[Privilege]
    body = body[1:]
    (DataField,) = struct.unpack("!B", body[0:1])
    par["DataField"] = C1G2LockDataField_Type2Name[DataField]
    body = body[1:]
    return par, data[length:]

def decode_C1G2BlockErase(data):
    par = {}

    if len(data) == 0:
        return None, data
    type, length = struct.unpack("!HH", data[0:4])

    if type != Parameter_struct["C1G2BlockErase"]["type"]:
        return None, data

    body = data[4:length]
    (OpSpecID,) = struct.unpack("!H", body[0:2])
    par["OpSpecID"] = OpSpecID
    body = body[2:]
    (AccessPassword,) = struct.unpack("!I", body[0:4])
    par["AccessPassword"] = AccessPassword
    body = body[4:]
    (arrayLen, ) = struct.unpack("!H", body[0:2])
    body = body[2:]
    par["MB"] = body[0:arrayLen*1]
    body = body[arrayLen*1:]
    (WordPointer,) = struct.unpack("!H", body[0:2])
    par["WordPointer"] = WordPointer
    body = body[2:]
    (WordCount,) = struct.unpack("!H", body[0:2])
    par["WordCount"] = WordCount
    body = body[2:]
    return par, data[length:]

def decode_C1G2BlockWrite(data):
    par = {}

    if len(data) == 0:
        return None, data
    type, length = struct.unpack("!HH", data[0:4])

    if type != Parameter_struct["C1G2BlockWrite"]["type"]:
        return None, data

    body = data[4:length]
    (OpSpecID,) = struct.unpack("!H", body[0:2])
    par["OpSpecID"] = OpSpecID
    body = body[2:]
    (AccessPassword,) = struct.unpack("!I", body[0:4])
    par["AccessPassword"] = AccessPassword
    body = body[4:]
    (arrayLen, ) = struct.unpack("!H", body[0:2])
    body = body[2:]
    par["MB"] = body[0:arrayLen*1]
    body = body[arrayLen*1:]
    (WordPointer,) = struct.unpack("!H", body[0:2])
    par["WordPointer"] = WordPointer
    body = body[2:]
    (arrayLen, ) = struct.unpack("!H", body[0:2])
    body = body[2:]
    par["WriteData"] = body[0:arrayLen*2]
    body = body[arrayLen*2:]
    return par, data[length:]

def decode_C1G2EPCMemorySelector(data):
    par = {}

    if len(data) == 0:
        return None, data
    type, length = struct.unpack("!HH", data[0:4])

    if type != Parameter_struct["C1G2EPCMemorySelector"]["type"]:
        return None, data

    body = data[4:length]
    (e,) = struct.unpack("!B", body[0:1])
    par["EnableCRC"] = (e>>7)&1
    par["EnablePCBits"] = (e>>6)&1
    body = body[1:]
    return par, data[length:]

def decode_C1G2_PC(data):
    par = {}

    if len(data) == 0:
        return None, data
    type, length = struct.unpack("!HH", data[0:4])

    if type != Parameter_struct["C1G2_PC"]["type"]:
        return None, data

    body = data[4:length]
    (PC_Bits,) = struct.unpack("!H", body[0:2])
    par["PC_Bits"] = PC_Bits
    body = body[2:]
    return par, data[length:]

def decode_C1G2_CRC(data):
    par = {}

    if len(data) == 0:
        return None, data
    type, length = struct.unpack("!HH", data[0:4])

    if type != Parameter_struct["C1G2_CRC"]["type"]:
        return None, data

    body = data[4:length]
    (CRC,) = struct.unpack("!H", body[0:2])
    par["CRC"] = CRC
    body = body[2:]
    return par, data[length:]

def decode_C1G2SingulationDetails(data):
    par = {}

    if len(data) == 0:
        return None, data
    type, length = struct.unpack("!HH", data[0:4])

    if type != Parameter_struct["C1G2SingulationDetails"]["type"]:
        return None, data

    body = data[4:length]
    (NumCollisionSlots,) = struct.unpack("!H", body[0:2])
    par["NumCollisionSlots"] = NumCollisionSlots
    body = body[2:]
    (NumEmptySlots,) = struct.unpack("!H", body[0:2])
    par["NumEmptySlots"] = NumEmptySlots
    body = body[2:]
    return par, data[length:]

def decode_C1G2ReadOpSpecResult(data):
    par = {}

    if len(data) == 0:
        return None, data
    type, length = struct.unpack("!HH", data[0:4])

    if type != Parameter_struct["C1G2ReadOpSpecResult"]["type"]:
        return None, data

    body = data[4:length]
    (Result,) = struct.unpack("!B", body[0:1])
    par["Result"] = C1G2ReadResultType_Type2Name[Result]
    body = body[1:]
    (OpSpecID,) = struct.unpack("!H", body[0:2])
    par["OpSpecID"] = OpSpecID
    body = body[2:]
    (arrayLen, ) = struct.unpack("!H", body[0:2])
    body = body[2:]
    par["ReadData"] = body[0:arrayLen*2]
    body = body[arrayLen*2:]
    return par, data[length:]

def decode_C1G2WriteOpSpecResult(data):
    par = {}

    if len(data) == 0:
        return None, data
    type, length = struct.unpack("!HH", data[0:4])

    if type != Parameter_struct["C1G2WriteOpSpecResult"]["type"]:
        return None, data

    body = data[4:length]
    (Result,) = struct.unpack("!B", body[0:1])
    par["Result"] = C1G2WriteResultType_Type2Name[Result]
    body = body[1:]
    (OpSpecID,) = struct.unpack("!H", body[0:2])
    par["OpSpecID"] = OpSpecID
    body = body[2:]
    (NumWordsWritten,) = struct.unpack("!H", body[0:2])
    par["NumWordsWritten"] = NumWordsWritten
    body = body[2:]
    return par, data[length:]

def decode_C1G2KillOpSpecResult(data):
    par = {}

    if len(data) == 0:
        return None, data
    type, length = struct.unpack("!HH", data[0:4])

    if type != Parameter_struct["C1G2KillOpSpecResult"]["type"]:
        return None, data

    body = data[4:length]
    (Result,) = struct.unpack("!B", body[0:1])
    par["Result"] = C1G2KillResultType_Type2Name[Result]
    body = body[1:]
    (OpSpecID,) = struct.unpack("!H", body[0:2])
    par["OpSpecID"] = OpSpecID
    body = body[2:]
    return par, data[length:]

def decode_C1G2LockOpSpecResult(data):
    par = {}

    if len(data) == 0:
        return None, data
    type, length = struct.unpack("!HH", data[0:4])

    if type != Parameter_struct["C1G2LockOpSpecResult"]["type"]:
        return None, data

    body = data[4:length]
    (Result,) = struct.unpack("!B", body[0:1])
    par["Result"] = C1G2LockResultType_Type2Name[Result]
    body = body[1:]
    (OpSpecID,) = struct.unpack("!H", body[0:2])
    par["OpSpecID"] = OpSpecID
    body = body[2:]
    return par, data[length:]

def decode_C1G2BlockEraseOpSpecResult(data):
    par = {}

    if len(data) == 0:
        return None, data
    type, length = struct.unpack("!HH", data[0:4])

    if type != Parameter_struct["C1G2BlockEraseOpSpecResult"]["type"]:
        return None, data

    body = data[4:length]
    (Result,) = struct.unpack("!B", body[0:1])
    par["Result"] = C1G2BlockEraseResultType_Type2Name[Result]
    body = body[1:]
    (OpSpecID,) = struct.unpack("!H", body[0:2])
    par["OpSpecID"] = OpSpecID
    body = body[2:]
    return par, data[length:]

def decode_C1G2BlockWriteOpSpecResult(data):
    par = {}

    if len(data) == 0:
        return None, data
    type, length = struct.unpack("!HH", data[0:4])

    if type != Parameter_struct["C1G2BlockWriteOpSpecResult"]["type"]:
        return None, data

    body = data[4:length]
    (Result,) = struct.unpack("!B", body[0:1])
    par["Result"] = C1G2BlockWriteResultType_Type2Name[Result]
    body = body[1:]
    (OpSpecID,) = struct.unpack("!H", body[0:2])
    par["OpSpecID"] = OpSpecID
    body = body[2:]
    (NumWordsWritten,) = struct.unpack("!H", body[0:2])
    par["NumWordsWritten"] = NumWordsWritten
    body = body[2:]
    return par, data[length:]

def decode_CUSTOM_MESSAGE(body):
    par = LLRPMessage()

    (VendorIdentifier,) = struct.unpack("!I", body[0:4])
    par["VendorIdentifier"] = VendorIdentifier
    body = body[4:]
    (MessageSubtype,) = struct.unpack("!B", body[0:1])
    par["MessageSubtype"] = MessageSubtype
    body = body[1:]
    (arrayLen, ) = struct.unpack("!H", body[0:2])
    body = body[2:]
    par["Data"] = body[0:arrayLen*1]
    body = body[arrayLen*1:]
    return par

def decode_GET_READER_CAPABILITIES(body):
    par = LLRPMessage()

    (RequestedData,) = struct.unpack("!B", body[0:1])
    par["RequestedData"] = GetReaderCapabilitiesRequestedData_Type2Name[RequestedData]
    body = body[1:]
    par["Custom"] = []
    while True:
        ret, body = decode("Custom")(body)
        if ret:
            par["Custom"].append(ret)
        else:
            break
    return par

def decode_GET_READER_CAPABILITIES_RESPONSE(body):
    par = LLRPMessage()

    ret, body = decode("LLRPStatus")(body)
    if ret:
        par["LLRPStatus"] = ret
    else:
        raise LLRPError("missing LLRPStatus parameter")
    ret, body = decode("GeneralDeviceCapabilities")(body)
    if ret:
        par["GeneralDeviceCapabilities"] = ret
    ret, body = decode("LLRPCapabilities")(body)
    if ret:
        par["LLRPCapabilities"] = ret
    ret, body = decode("RegulatoryCapabilities")(body)
    if ret:
        par["RegulatoryCapabilities"] = ret
    ret, body = decode("C1G2LLRPCapabilities")(body)
    if ret:
        par["C1G2LLRPCapabilities"] = ret
    
    par["Custom"] = []
    while True:
        ret, body = decode("Custom")(body)
        if ret:
            par["Custom"].append(ret)
        else:
            break
    return par

def decode_ADD_ROSPEC(body):
    par = LLRPMessage()

    ret, body = decode("ROSpec")(body)
    if ret:
        par["ROSpec"] = ret
    else:
        raise LLRPError("missing ROSpec parameter")
    return par

def decode_ADD_ROSPEC_RESPONSE(body):
    par = LLRPMessage()

    ret, body = decode("LLRPStatus")(body)
    if ret:
        par["LLRPStatus"] = ret
    else:
        raise LLRPError("missing LLRPStatus parameter")
    return par

def decode_DELETE_ROSPEC(body):
    par = LLRPMessage()

    (ROSpecID,) = struct.unpack("!I", body[0:4])
    par["ROSpecID"] = ROSpecID
    body = body[4:]
    return par

def decode_DELETE_ROSPEC_RESPONSE(body):
    par = LLRPMessage()

    ret, body = decode("LLRPStatus")(body)
    if ret:
        par["LLRPStatus"] = ret
    else:
        raise LLRPError("missing LLRPStatus parameter")
    return par

def decode_START_ROSPEC(body):
    par = LLRPMessage()

    (ROSpecID,) = struct.unpack("!I", body[0:4])
    par["ROSpecID"] = ROSpecID
    body = body[4:]
    return par

def decode_START_ROSPEC_RESPONSE(body):
    par = LLRPMessage()

    ret, body = decode("LLRPStatus")(body)
    if ret:
        par["LLRPStatus"] = ret
    else:
        raise LLRPError("missing LLRPStatus parameter")
    return par

def decode_STOP_ROSPEC(body):
    par = LLRPMessage()

    (ROSpecID,) = struct.unpack("!I", body[0:4])
    par["ROSpecID"] = ROSpecID
    body = body[4:]
    return par

def decode_STOP_ROSPEC_RESPONSE(body):
    par = LLRPMessage()

    ret, body = decode("LLRPStatus")(body)
    if ret:
        par["LLRPStatus"] = ret
    else:
        raise LLRPError("missing LLRPStatus parameter")
    return par

def decode_ENABLE_ROSPEC(body):
    par = LLRPMessage()

    (ROSpecID,) = struct.unpack("!I", body[0:4])
    par["ROSpecID"] = ROSpecID
    body = body[4:]
    return par

def decode_ENABLE_ROSPEC_RESPONSE(body):
    par = LLRPMessage()

    ret, body = decode("LLRPStatus")(body)
    if ret:
        par["LLRPStatus"] = ret
    else:
        raise LLRPError("missing LLRPStatus parameter")
    return par

def decode_DISABLE_ROSPEC(body):
    par = LLRPMessage()

    (ROSpecID,) = struct.unpack("!I", body[0:4])
    par["ROSpecID"] = ROSpecID
    body = body[4:]
    return par

def decode_DISABLE_ROSPEC_RESPONSE(body):
    par = LLRPMessage()

    ret, body = decode("LLRPStatus")(body)
    if ret:
        par["LLRPStatus"] = ret
    else:
        raise LLRPError("missing LLRPStatus parameter")
    return par

def decode_GET_ROSPECS(body):
    par = LLRPMessage()

    return par

def decode_GET_ROSPECS_RESPONSE(body):
    par = LLRPMessage()

    ret, body = decode("LLRPStatus")(body)
    if ret:
        par["LLRPStatus"] = ret
    else:
        raise LLRPError("missing LLRPStatus parameter")
    par["ROSpec"] = []
    while True:
        ret, body = decode("ROSpec")(body)
        if ret:
            par["ROSpec"].append(ret)
        else:
            break
    return par

def decode_ADD_ACCESSSPEC(body):
    par = LLRPMessage()

    ret, body = decode("AccessSpec")(body)
    if ret:
        par["AccessSpec"] = ret
    else:
        raise LLRPError("missing AccessSpec parameter")
    return par

def decode_ADD_ACCESSSPEC_RESPONSE(body):
    par = LLRPMessage()

    ret, body = decode("LLRPStatus")(body)
    if ret:
        par["LLRPStatus"] = ret
    else:
        raise LLRPError("missing LLRPStatus parameter")
    return par

def decode_DELETE_ACCESSSPEC(body):
    par = LLRPMessage()

    (AccessSpecID,) = struct.unpack("!I", body[0:4])
    par["AccessSpecID"] = AccessSpecID
    body = body[4:]
    return par

def decode_DELETE_ACCESSSPEC_RESPONSE(body):
    par = LLRPMessage()

    ret, body = decode("LLRPStatus")(body)
    if ret:
        par["LLRPStatus"] = ret
    else:
        raise LLRPError("missing LLRPStatus parameter")
    return par

def decode_ENABLE_ACCESSSPEC(body):
    par = LLRPMessage()

    (AccessSpecID,) = struct.unpack("!I", body[0:4])
    par["AccessSpecID"] = AccessSpecID
    body = body[4:]
    return par

def decode_ENABLE_ACCESSSPEC_RESPONSE(body):
    par = LLRPMessage()

    ret, body = decode("LLRPStatus")(body)
    if ret:
        par["LLRPStatus"] = ret
    else:
        raise LLRPError("missing LLRPStatus parameter")
    return par

def decode_DISABLE_ACCESSSPEC(body):
    par = LLRPMessage()

    (AccessSpecID,) = struct.unpack("!I", body[0:4])
    par["AccessSpecID"] = AccessSpecID
    body = body[4:]
    return par

def decode_DISABLE_ACCESSSPEC_RESPONSE(body):
    par = LLRPMessage()

    ret, body = decode("LLRPStatus")(body)
    if ret:
        par["LLRPStatus"] = ret
    else:
        raise LLRPError("missing LLRPStatus parameter")
    return par

def decode_GET_ACCESSSPECS(body):
    par = LLRPMessage()

    return par

def decode_GET_ACCESSSPECS_RESPONSE(body):
    par = LLRPMessage()

    ret, body = decode("LLRPStatus")(body)
    if ret:
        par["LLRPStatus"] = ret
    else:
        raise LLRPError("missing LLRPStatus parameter")
    par["AccessSpec"] = []
    while True:
        ret, body = decode("AccessSpec")(body)
        if ret:
            par["AccessSpec"].append(ret)
        else:
            break
    return par

def decode_GET_READER_CONFIG(body):
    par = LLRPMessage()

    (AntennaID,) = struct.unpack("!H", body[0:2])
    par["AntennaID"] = AntennaID
    body = body[2:]
    (RequestedData,) = struct.unpack("!B", body[0:1])
    par["RequestedData"] = GetReaderConfigRequestedData_Type2Name[RequestedData]
    body = body[1:]
    (GPIPortNum,) = struct.unpack("!H", body[0:2])
    par["GPIPortNum"] = GPIPortNum
    body = body[2:]
    (GPOPortNum,) = struct.unpack("!H", body[0:2])
    par["GPOPortNum"] = GPOPortNum
    body = body[2:]
    par["Custom"] = []
    while True:
        ret, body = decode("Custom")(body)
        if ret:
            par["Custom"].append(ret)
        else:
            break
    return par

def decode_GET_READER_CONFIG_RESPONSE(body):
    par = LLRPMessage()

    ret, body = decode("LLRPStatus")(body)
    if ret:
        par["LLRPStatus"] = ret
    else:
        raise LLRPError("missing LLRPStatus parameter")
    ret, body = decode("Identification")(body)
    if ret:
        par["Identification"] = ret
    par["AntennaProperties"] = []
    while True:
        ret, body = decode("AntennaProperties")(body)
        if ret:
            par["AntennaProperties"].append(ret)
        else:
            break
    par["AntennaConfiguration"] = []
    while True:
        ret, body = decode("AntennaConfiguration")(body)
        if ret:
            par["AntennaConfiguration"].append(ret)
        else:
            break
    ret, body = decode("ReaderEventNotificationSpec")(body)
    if ret:
        par["ReaderEventNotificationSpec"] = ret
    ret, body = decode("ROReportSpec")(body)
    if ret:
        par["ROReportSpec"] = ret
    ret, body = decode("AccessReportSpec")(body)
    if ret:
        par["AccessReportSpec"] = ret
    ret, body = decode("LLRPConfigurationStateValue")(body)
    if ret:
        par["LLRPConfigurationStateValue"] = ret
    ret, body = decode("KeepaliveSpec")(body)
    if ret:
        par["KeepaliveSpec"] = ret
    par["GPIPortCurrentState"] = []
    while True:
        ret, body = decode("GPIPortCurrentState")(body)
        if ret:
            par["GPIPortCurrentState"].append(ret)
        else:
            break
    par["GPOWriteData"] = []
    while True:
        ret, body = decode("GPOWriteData")(body)
        if ret:
            par["GPOWriteData"].append(ret)
        else:
            break
    ret, body = decode("EventsAndReports")(body)
    if ret:
        par["EventsAndReports"] = ret
    par["Custom"] = []
    while True:
        ret, body = decode("Custom")(body)
        if ret:
            par["Custom"].append(ret)
        else:
            break
    return par

def decode_SET_READER_CONFIG(body):
    par = LLRPMessage()

    (e,) = struct.unpack("!B", body[0:1])
    par["ResetToFactoryDefault"] = (e>>7)&1
    body = body[1:]
    ret, body = decode("ReaderEventNotificationSpec")(body)
    if ret:
        par["ReaderEventNotificationSpec"] = ret
    par["AntennaProperties"] = []
    while True:
        ret, body = decode("AntennaProperties")(body)
        if ret:
            par["AntennaProperties"].append(ret)
        else:
            break
    par["AntennaConfiguration"] = []
    while True:
        ret, body = decode("AntennaConfiguration")(body)
        if ret:
            par["AntennaConfiguration"].append(ret)
        else:
            break
    ret, body = decode("ROReportSpec")(body)
    if ret:
        par["ROReportSpec"] = ret
    ret, body = decode("AccessReportSpec")(body)
    if ret:
        par["AccessReportSpec"] = ret
    ret, body = decode("KeepaliveSpec")(body)
    if ret:
        par["KeepaliveSpec"] = ret
    par["GPOWriteData"] = []
    while True:
        ret, body = decode("GPOWriteData")(body)
        if ret:
            par["GPOWriteData"].append(ret)
        else:
            break
    par["GPIPortCurrentState"] = []
    while True:
        ret, body = decode("GPIPortCurrentState")(body)
        if ret:
            par["GPIPortCurrentState"].append(ret)
        else:
            break
    ret, body = decode("EventsAndReports")(body)
    if ret:
        par["EventsAndReports"] = ret
    par["Custom"] = []
    while True:
        ret, body = decode("Custom")(body)
        if ret:
            par["Custom"].append(ret)
        else:
            break
    return par

def decode_SET_READER_CONFIG_RESPONSE(body):
    par = LLRPMessage()

    ret, body = decode("LLRPStatus")(body)
    if ret:
        par["LLRPStatus"] = ret
    else:
        raise LLRPError("missing LLRPStatus parameter")
    return par

def decode_CLOSE_CONNECTION(body):
    par = LLRPMessage()

    return par

def decode_CLOSE_CONNECTION_RESPONSE(body):
    par = LLRPMessage()

    ret, body = decode("LLRPStatus")(body)
    if ret:
        par["LLRPStatus"] = ret
    else:
        raise LLRPError("missing LLRPStatus parameter")
    return par

def decode_GET_REPORT(body):
    par = LLRPMessage()

    return par

def decode_RO_ACCESS_REPORT(body):
    par = LLRPMessage()

    par["TagReportData"] = []
    while True:
        ret, body = decode("TagReportData")(body)
        if ret:
            par["TagReportData"].append(ret)
        else:
            break
    par["RFSurveyReportData"] = []
    while True:
        ret, body = decode("RFSurveyReportData")(body)
        if ret:
            par["RFSurveyReportData"].append(ret)
        else:
            break
    par["Custom"] = []
    while True:
        ret, body = decode("Custom")(body)
        if ret:
            par["Custom"].append(ret)
        else:
            break
    return par

def decode_KEEPALIVE(body):
    par = LLRPMessage()

    return par

def decode_KEEPALIVE_ACK(body):
    par = LLRPMessage()

    return par

def decode_READER_EVENT_NOTIFICATION(body):
    par = LLRPMessage()

    ret, body = decode("ReaderEventNotificationData")(body)
    if ret:
        par["ReaderEventNotificationData"] = ret
    else:
        raise LLRPError("missing ReaderEventNotificationData parameter")
    return par

def decode_ENABLE_EVENTS_AND_REPORTS(body):
    par = LLRPMessage()

    return par

def decode_ERROR_MESSAGE(body):
    par = LLRPMessage()

    ret, body = decode("LLRPStatus")(body)
    if ret:
        par["LLRPStatus"] = ret
    else:
        raise LLRPError("missing LLRPStatus parameter")
    return par

