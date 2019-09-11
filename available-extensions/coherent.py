

# show interfaces transceiver hardware
# show interfaces phy detail
# show interfaces transceiver detail | json
"""
Tech.030    Optical Frequency   (show int trans hardware)
Tech.035    Pre-FEC Error Rate  (show int phy detail)
Tech.036    Post-FEC Error Rate (show int phy detail)
Tech.037    Transmit Power  (show int trans)
Tech.038    Receiver Power  (show int trans)
Tech.039    PMD (show int phy detail reports DGD which is very similar to PMD)
Tech.041    Chromatic Dispersion    (show int phy detail)
Tech.050    Loss of frame   (show int phy detail)
Tech.051    Loss of signal  (show int phy detail)
Tech.052    Optical rx level high/low   (show int trans detail, and compare
                                        power with thresholds)
Tech.053    Module unrecognized (show int stat would not report media type)
Tech.054    Laser fail  (show int trans - best we can do is notice tx power
                        being not correct or dramatically different from
                        configured value)

Tech.056    Transmit wavelength out of range    (show int phy detail - Can get
                                                an idea from carrier frequency
                                                offset)

Tech.057    laser/LO mismatch   probably not too relevant for Oclaro as tx and
                                rx lasers are shared. For other transceivers,
                                best that can be done is to notice channel rx
                                power being low but total rx power being high.

The following attributes are not printed but known for CloudsRest1. We'll need
to update this for CloudsRest2:
---------

Tech.031    Modulation Format   (We only use QPSK)

The following attributes are printed but we'll need to work with ClariPhy to
see if they are accurate. For example, we noticed inconsistent Q-factor
reporting and ClariPhy has not yet resolved this.
--------

Tech.032    Q-factor    (show int phy detail)
Tech.040    PDL         (show int phy detail)

We don't yet report the following values:
--------

Tech.033    Receive SNR (Other properties that we report, like MSE, are good
                        substitutes).
Tech.034    Cycle Slip Rate
Tech.042    Errored-Seconds (will need to get more details on what they want
                            with these attributes)
Tech.043    Severely Errored Seconds
Tech.044    Latency             (Not sure what msft is looking for here)
Tech.055    Payload mismatch	(not sure what msft means by this)
"""
import re
import pprint

POLLING_INTERVAL = 5



TH_DATA = """Name: Et3/1/1
Media Type: 100GBASE-LR4
Wavelength (nm): 1302

Name: Et3/1/2
Media Type: 100GBASE-LR4
Wavelength (nm): 1302

Name: Et3/1/3
Media Type: 100GBASE-LR4
Wavelength (nm): 1302

Name: Et3/1/4
Media Type: 100GBASE-LR4
Wavelength (nm): 1302

Name: Et3/2/1
Media Type: 100GBASE-LR4
Wavelength (nm): 1302

Name: Et3/2/2
Media Type: 100GBASE-LR4
Wavelength (nm): 1302

Name: Et3/2/3
Media Type: 100GBASE-LR4
Wavelength (nm): 1302

Name: Et3/2/4
Media Type: 100GBASE-LR4
Wavelength (nm): 1302

Name: Et4/2/1
Media Type: Unknown

Name: Et4/2/2
Media Type: Unknown

Name: Et4/2/3
Media Type: Unknown

Name: Et4/2/4
Media Type: Unknown

Name: Et4/3/1
Media Type: Unknown

Name: Et4/3/2
Media Type: Unknown

Name: Et4/3/3
Media Type: Unknown

Name: Et4/3/4
Media Type: Unknown

Name: Et4/4/1
Media Type: Unknown

Name: Et4/4/2
Media Type: Unknown

Name: Et4/4/3
Media Type: Unknown

Name: Et4/4/4
Media Type: Unknown

Name: Et4/5/1
Media Type: Unknown

Name: Et4/5/2
Media Type: Unknown

Name: Et4/5/3
Media Type: Unknown

Name: Et4/5/4
Media Type: Unknown

Name: Et4/6/1
Media Type: Unknown

Name: Et4/6/2
Media Type: Unknown

Name: Et4/6/3
Media Type: Unknown

Name: Et4/6/4
Media Type: Unknown

Name: Et4/7/1
Media Type: Unknown

Name: Et4/7/2
Media Type: Unknown

Name: Et4/7/3
Media Type: Unknown

Name: Et4/7/4
Media Type: Unknown

Name: Et4/9/1
Media Type: Unknown

Name: Et4/9/2
Media Type: Unknown

Name: Et4/9/3
Media Type: Unknown

Name: Et4/9/4
Media Type: Unknown

Name: Et4/10/1
Media Type: Unknown

Name: Et4/10/2
Media Type: Unknown

Name: Et4/10/3
Media Type: Unknown

Name: Et4/10/4
Media Type: Unknown

Name: Et4/19/1
Media Type: Unknown

Name: Et4/19/2
Media Type: Unknown

Name: Et4/19/3
Media Type: Unknown

Name: Et4/19/4
Media Type: Unknown

Name: Et4/20/1
Media Type: 40GBASE-AR4
Wavelength (nm): 850

Name: Et4/20/2
Media Type: 40GBASE-AR4
Wavelength (nm): 850

Name: Et4/20/3
Media Type: 40GBASE-AR4
Wavelength (nm): 850

Name: Et4/20/4
Media Type: 40GBASE-AR4
Wavelength (nm): 850

Name: Et4/21/1
Media Type: 40GBASE-AR4
Wavelength (nm): 850

Name: Et4/21/2
Media Type: 40GBASE-AR4
Wavelength (nm): 850

Name: Et4/21/3
Media Type: 40GBASE-AR4
Wavelength (nm): 850

Name: Et4/21/4
Media Type: 40GBASE-AR4
Wavelength (nm): 850

Name: Et4/22/1
Media Type: 40GBASE-AR4
Wavelength (nm): 850

Name: Et4/22/2
Media Type: 40GBASE-AR4
Wavelength (nm): 850

Name: Et4/22/3
Media Type: 40GBASE-AR4
Wavelength (nm): 850

Name: Et4/22/4
Media Type: 40GBASE-AR4
Wavelength (nm): 850

Name: Et4/23/1
Media Type: 40GBASE-AR4
Wavelength (nm): 850

Name: Et4/23/2
Media Type: 40GBASE-AR4
Wavelength (nm): 850

Name: Et4/23/3
Media Type: 40GBASE-AR4
Wavelength (nm): 850

Name: Et4/23/4
Media Type: 40GBASE-AR4
Wavelength (nm): 850

Name: Et4/24/1
Media Type: Unknown

Name: Et4/24/2
Media Type: Unknown

Name: Et4/24/3
Media Type: Unknown

Name: Et4/24/4
Media Type: Unknown

Name: Et4/26/1
Media Type: 40GBASE-AR4
Wavelength (nm): 850

Name: Et4/26/2
Media Type: 40GBASE-AR4
Wavelength (nm): 850

Name: Et4/26/3
Media Type: 40GBASE-AR4
Wavelength (nm): 850

Name: Et4/26/4
Media Type: 40GBASE-AR4
Wavelength (nm): 850

Name: Et4/27/1
Media Type: 40GBASE-AR4
Wavelength (nm): 850

Name: Et4/27/2
Media Type: 40GBASE-AR4
Wavelength (nm): 850

Name: Et4/27/3
Media Type: 40GBASE-AR4
Wavelength (nm): 850

Name: Et4/27/4
Media Type: 40GBASE-AR4
Wavelength (nm): 850

Name: Et4/28/1
Media Type: 40GBASE-AR4
Wavelength (nm): 850

Name: Et4/28/2
Media Type: 40GBASE-AR4
Wavelength (nm): 850

Name: Et4/28/3
Media Type: 40GBASE-AR4
Wavelength (nm): 850

Name: Et4/28/4
Media Type: 40GBASE-AR4
Wavelength (nm): 850

Name: Et4/29/1
Media Type: 40GBASE-AR4
Wavelength (nm): 850

Name: Et4/29/2
Media Type: 40GBASE-AR4
Wavelength (nm): 850

Name: Et4/29/3
Media Type: 40GBASE-AR4
Wavelength (nm): 850

Name: Et4/29/4
Media Type: 40GBASE-AR4
Wavelength (nm): 850

Name: Et4/30/1
Media Type: 40GBASE-AR4
Wavelength (nm): 850

Name: Et4/30/2
Media Type: 40GBASE-AR4
Wavelength (nm): 850

Name: Et4/30/3
Media Type: 40GBASE-AR4
Wavelength (nm): 850

Name: Et4/30/4
Media Type: 40GBASE-AR4
Wavelength (nm): 850

Name: Et4/33/1
Media Type: Unknown

Name: Et4/33/2
Media Type: Unknown

Name: Et4/33/3
Media Type: Unknown

Name: Et4/33/4
Media Type: Unknown

Name: Et4/34/1
Media Type: Unknown

Name: Et4/34/2
Media Type: Unknown

Name: Et4/34/3
Media Type: Unknown

Name: Et4/34/4
Media Type: Unknown

Name: Et4/35/1
Media Type: Unknown

Name: Et4/35/2
Media Type: Unknown

Name: Et4/35/3
Media Type: Unknown

Name: Et4/35/4
Media Type: Unknown

Name: Et5/2
Media Type: 100G-DWDM-E
Configured Channel               : 39
Configured Grid (GHz)            : 50.0
Computed Frequency (GHz)         : 193,100.0
Computed Wavelength (nm)         : 1552.52
Operational Channel              : 39          (Default)
Operational Grid (GHz)           : 50.0        (Default)
Operational Frequency (GHz)      : 193,100.0
Operational Wavelength (nm)      : 1552.52
Configured Tx Power (dBm)        : 0.0         (Default)
Configured Rx Power (dBm)        : 0.0         (Default)
Operational Rx Attenuation (dB)  : 0.0

Name: Et6/1
Media Type: 10GBASE-SR
Wavelength (nm): 850

Name: Et6/2
Media Type: 10GBASE-SR
Wavelength (nm): 850
"""
PD_DATA = """
Current System Time: Tue Jun 14 17:36:41 2016
Ethernet5/2
                              Current State     Changes            Last Change
  PHY state                   linkUp                 43    4 days, 0:45:30 ago
  Interface state             up                     38    4 days, 0:45:30 ago
  HW resets                                           0                  never
  Transceiver                 100G-DWDM-E             4   6 days, 22:02:47 ago
  Transceiver SN              SMD5309.1
  Oper speed                  100Gbps
  Interrupt Count                                    67
  Diags mode                  normalOperation
  Model                       Arad Integrated Phy (0x000af7,0x3f,0x0)
  Loopback                    none
  PMA/PMD RX signal detect    ok                      3   6 days, 22:02:45 ago
  PCS RX link status          up                    439    4 days, 0:45:35 ago
  PCS RX fault                ok                     35    4 days, 0:45:28 ago
  PCS TX fault                ok                     34    4 days, 0:45:33 ago
  PCS block lock              ok                      7   5 days, 18:32:37 ago
  PCS high BER                ok                      2   5 days, 18:32:37 ago
  PCS err blocks              22                          5 days, 18:32:37 ago
  PCS BER                     98                      2   5 days, 18:32:37 ago
  Xcvr EEPROM read timeout                            0                  never
  Spurious xcvr detection                             0                  never
  DOM control/status fail                             0
  Presence indication         xcvrPresent             4   6 days, 22:02:50 ago
  Bad EEPROM checksums                                0                  never
  RX_LOS since system boot    False                  30    4 days, 0:45:39 ago
  RX_LOS since insertion                             15
  TX_FAULT since system boot  False                   0                  never
  TX_FAULT since insertion                            0
MacSec phy
  Model
  System Rx signal            1                       5   6 days, 22:02:46 ago
  systemFault                 0                       6   6 days, 22:02:44 ago
  systemLocalFault            0                       6   6 days, 22:02:44 ago
  systemRemoteFault           0                      42    4 days, 0:45:34 ago
  Network Rx signal           1                      33    4 days, 0:45:38 ago
  networkFault                0                      28   4 days, 19:16:35 ago
  networkLocalFault           0                      34    4 days, 0:45:38 ago
  networkRemoteFault          0                      36    4 days, 0:45:30 ago
Coherent transceiver phy
  HW resets                                           1  12 days, 17:40:36 ago
  Model                       Cl10010 (1.0)
  Host tx pcs signal          1                       1  12 days, 17:38:16 ago
  Host tx pcs lane aligned    1                       5  10 days, 20:37:45 ago
  Host tx lane 0 aligned      1                       5  10 days, 20:37:45 ago
  Host tx lane 1 aligned      1                       5  10 days, 20:37:45 ago
  Host tx lane 2 aligned      1                       5  10 days, 20:37:45 ago
  Host tx lane 3 aligned      1                       5  10 days, 20:37:45 ago
  Host tx lane 4 aligned      1                       5  10 days, 20:37:45 ago
  Host tx lane 5 aligned      1                       5  10 days, 20:37:45 ago
  Host tx lane 6 aligned      1                       5  10 days, 20:37:45 ago
  Host tx lane 7 aligned      1                       5  10 days, 20:37:45 ago
  Host tx lane 8 aligned      1                       5  10 days, 20:37:45 ago
  Host tx lane 9 aligned      1                       5  10 days, 20:37:45 ago
  Host pll locked             1                       1  12 days, 17:39:06 ago
  Host tx data fifo good      1                       1  12 days, 17:38:16 ago
  Host tx out of frame        1                       1  12 days, 17:39:06 ago
  Host tx LOF                 1                       1  12 days, 17:39:06 ago
  Host tx lane aligned        0                       0                  never
  Host tx lane 0 LOF          1                       5  10 days, 20:37:45 ago
  Host tx lane 1 LOF          1                       5  10 days, 20:37:45 ago
  Host tx lane 2 LOF          1                       5  10 days, 20:37:45 ago
  Host tx lane 3 LOF          1                       5  10 days, 20:37:45 ago
  Host tx lane 4 LOF          1                       5  10 days, 20:37:45 ago
  Host tx lane 5 LOF          1                       5  10 days, 20:37:45 ago
  Host tx lane 6 LOF          1                       5  10 days, 20:37:45 ago
  Host tx lane 7 LOF          1                       5  10 days, 20:37:45 ago
  Host tx lane 8 LOF          1                       5  10 days, 20:37:45 ago
  Host tx lane 9 LOF          1                       5  10 days, 20:37:45 ago
  Host rx pcs signal          1                      33    4 days, 0:45:37 ago
  Host rx lane 0 aligned      1                      33    4 days, 0:45:37 ago
  Host rx lane 1 aligned      1                      33    4 days, 0:45:37 ago
  Host rx lane 2 aligned      1                      33    4 days, 0:45:37 ago
  Host rx lane 3 aligned      1                      33    4 days, 0:45:37 ago
  Host rx lane 4 aligned      1                      33    4 days, 0:45:37 ago
  Host rx lane 5 aligned      1                      33    4 days, 0:45:37 ago
  Host rx lane 6 aligned      1                      33    4 days, 0:45:37 ago
  Host rx lane 7 aligned      1                      33    4 days, 0:45:37 ago
  Host rx lane 8 aligned      1                      33    4 days, 0:45:37 ago
  Host rx lane 9 aligned      1                      33    4 days, 0:45:37 ago
  Otu loss of any frame       0                      34    4 days, 0:45:37 ago
  Host rx data fifo good      1                      33    4 days, 0:45:37 ago
  Host rx loss of multi-frame 0                      34    4 days, 0:45:37 ago
  Host rx LOF                 0                       2   6 days, 22:02:37 ago
  Host rx out of frame        0                       4   6 days, 22:02:36 ago
  Otl4 lane aligned           1                      33    4 days, 0:45:37 ago
  Lane hi aligned             1                      33    4 days, 0:45:37 ago
  Lane hq aligned             1                      33    4 days, 0:45:37 ago
  Lane vi aligned             1                      33    4 days, 0:45:37 ago
  Lane vq aligned             1                      33    4 days, 0:45:37 ago
  Timing recovery lock        1                      15   4 days, 20:04:43 ago
  Signal from transceiver     1                       1  12 days, 17:38:16 ago
  Signal detect               1                      29    4 days, 0:45:37 ago
  Custom signal lock          1                       1  12 days, 17:38:16 ago
  Signal lock                 1                      11   5 days, 17:57:25 ago
  Lane hi signal              1                      29    4 days, 0:45:37 ago
  Lane hq signal              1                      29    4 days, 0:45:37 ago
  Lane vi signal              1                      29    4 days, 0:45:37 ago
  Lane vq signal              1                      29    4 days, 0:45:37 ago
  Signal detect summary       1                      29    4 days, 0:45:37 ago
  Dsp firmware state          13                    367    4 days, 0:45:38 ago
  Center of gravity (H*)      216
  Center of gravity (V*)      199
  Total frames                253219645440
  Total LDPC frames           844415623
  Roll-off factor             0.20000000298
                              Current           Average
  Estimated pre-FEC BER       0.0              1.67e-08
  FEC word error rate         0.0                  98.9
  Diff. group delay (ps)      17               16.11394
  Chr. dispersion (ps/nm)     2                -2525.18
  Polarization dep. loss (dB) 0.5              141512.9
  Carrier freq. offset (KHz)  -15106           -43664.1
  Q-factor H                  0                     0.0
  Q-factor V                  0                     0.0
  State of polarization rate  95
                              HI         HQ         VI         VQ
  Amplitude                   0.16812    0.16599    0.16153    0.17111
  Mean square error           -16.779    -16.985    -16.124    -16.486
  AGC gain                    4095       4095       4095       4095
  RX skew                     125        0          98         0
  ADC unit offset             0.40%      0.30%      0.30%      0.30%
  ADC row offset              0.10%      0.10%      0.10%      0.10%
  ADC gain error              0.30%      0.30%      0.40%      0.30%
  ADC timing error            0.10%      0.30%      0.30%      0.20%
  Histogram 0
  | |*| | | | | | | | | | | | | | | |*| | | | | | | | | | | | | | |
  | |*| | | | | | | | | | | | | | | |*| | | | | | | | | | | | | | |
  | |*| | | | | | | | | | | | | | | |*| | | | | | | | | | | | | | |
  | |*| | | | | | | | | | | | | | | |*| | | | | | | | | | | | | | |
  | |*| | | | | | | | | | | | | | | |*| | | | | | | | | | | | | | |
  | |*| | | | | | | | | | | | | | | |*| | | | | | | | | | | | | | |
  | |*| | | | | | | | | | | | | | | |*| | | | | | | | | | | | | | |
  | |*| | | | | | | | | | | | | | | |*| | | | | | | | | | | | | | |
  | |*| | | | | | | | | | | | | | | |*| | | | | | | | | | | | | | |
  | |*| | | | | | | | | | | | | | | |*| | | | | | | | | | | | | | |
  Max 17                      Mean 9
  Histogram 1
  | |*| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
  | |*| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
  | |*| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
  | |*| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
  | |*| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
  | |*| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
  | |*| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
  | |*| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
  | |*| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
  | |*| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
  Max 1                       Mean 1
"""
TD_DATA = {
    "interfaces": {
        "Ethernet5/2": {
            "updateTime": 1465925717.3748772,
            "temperature": 35.89453125,
            "mediaType": "100G-DWDM-E",
            "txBias": 0.0,
            "totalRxPower": -0.3,
            "txPower": 0.41000000000000003,
            "narrowBand": True,
            "details": {
                "txPower": {
                    "highWarn": 3.5,
                    "lowWarn": -11.0,
                    "highAlarm": 5.0,
                    "lowAlarm": -12.0
                },
                "temperature": {
                    "highWarn": 70.0,
                    "lowWarn": 0.0,
                    "highAlarm": 80.0,
                    "lowAlarm": -10.0
                },
                "totalRxPower": {
                    "highWarn": 2.999864361344674,
                    "lowWarn": -24.089353929735008,
                    "highAlarm": 3.9998505610245036,
                    "lowAlarm": -25.086383061657273
                },
                "txBias": {
                    "highWarn": 0.0,
                    "lowWarn": 0.0,
                    "highAlarm": 0.0,
                    "lowAlarm": 0.0
                },
                "rxPower": {
                    "highWarn": 2.999864361344674,
                    "lowWarn": -24.089353929735008,
                    "highAlarm": 3.9998505610245036,
                    "lowAlarm": -25.086383061657273
                },
                "voltage": {
                    "highWarn": 3.5,
                    "lowWarn": 3.1,
                    "highAlarm": 3.6,
                    "lowAlarm": 3.0
                }
            },
            "vendorSn": "SMD5309.1",
            "rxPower": -0.53,
            "voltage": 3.271
        }
    }
}

def numberize(number):
    tmp = re.sub(r",", "", number)
    try:
        return int(tmp)
    except ValueError:
        try:
            return float(tmp)
        except ValueError:
            pass

    return number

def parse_intf_tr_hardware():
    # Tech.030    Optical Frequency   (show int trans hardware)
    # Tech.053    Module unrecognized (show int stat would not report media type)

    # Name: Et5/2
    # Media Type: 100G-DWDM-E
    # Configured Channel               : 39
    # Configured Grid (GHz)            : 50.0
    # Computed Frequency (GHz)         : 193,100.0
    # Computed Wavelength (nm)         : 1552.52
    # Operational Channel              : 39          (Default)
    # Operational Grid (GHz)           : 50.0        (Default)
    # Operational Frequency (GHz)      : 193,100.0
    # Operational Wavelength (nm)      : 1552.52
    # Configured Tx Power (dBm)        : 0.0         (Default)
    # Configured Rx Power (dBm)        : 0.0         (Default)
    # Operational Rx Attenuation (dB)  : 0.0

    data = TH_DATA
    result = {}

    current = None
    for line in data.splitlines():
        match = re.search(r"^Name:\s+([A-Za-z]{2})([^$]+)", line)
        if match:
            if match.group(1) == "Et":
                current = "Ethernet" + match.group(2)
                result[current] = {}
            else:
                current = None

        if current:
            match = re.search(r"(^[\w ]+)(?:\s?\([\w]+\))?\s*:\s*([\S]+)", line, re.I)
            if match:
                key = match.group(1).strip()
                key = key.lower()
                key = re.sub('\s+', '_', key)
                value = numberize(match.group(2))
                result[current][key] = value
    pprint.pprint(result)

def parse_intf_tr():
    # Tech.037    Transmit Power  (show int trans)
    # Tech.038    Receiver Power  (show int trans)
    # Tech.052    Optical rx level high/low   (show int trans detail, and compare
    #                                         power with thresholds)
    # Tech.054    Laser fail  (show int trans - best we can do is notice tx power
    #                         being not correct or dramatically different from
    #                         configured value)
    pass

def parse_intf_phy_detail():
    # Tech.035    Pre-FEC Error Rate  (show int phy detail)
    # Tech.036    Post-FEC Error Rate (show int phy detail) - Where?
    # Tech.039    PMD (show int phy detail reports DGD which is very similar to PMD)
    # Tech.041    Chromatic Dispersion    (show int phy detail)
    # Tech.050    Loss of frame   (show int phy detail)
    # Tech.051    Loss of signal  (show int phy detail)
    # Tech.056    Transmit wavelength out of range    (show int phy detail - Can get
    #                                                 an idea from carrier frequency
    #                                                 offset)
    # Tech.032    Q-factor    (show int phy detail)
    # Tech.040    PDL         (show int phy detail)
    data = PD_DATA
    pass

def update(pp):
    interfaces = parse_intf_tr_hardware()


if __name__ == "__main__":
    update(None)
