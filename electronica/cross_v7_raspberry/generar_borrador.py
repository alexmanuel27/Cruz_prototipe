from skidl import *
set_default_tool(KICAD9)
base='/Applications/KiCad/KiCad.app/Contents/SharedSupport/footprints'
conn='Connector_PinHeader_2.54mm:PinHeader_1x{}_P2.54mm_Vertical'
res='Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P7.62mm_Horizontal'
cap='Capacitor_THT:C_Disc_D5.0mm_W2.5mm_P5.00mm'
ecap='Capacitor_THT:CP_Radial_D6.3mm_P2.50mm'
N={x:Net(x) for x in ['GND','3V3_PI','5V_PI_EXT','VBAT_SW','9V_OPT','SDA','SCL','TEMP_1WIRE','M_STEP','M_DIR','M_ENABLE_N','WHITE_EN','BLUE_EN','BAT_SENSE','M1A','M1B','M2A','M2B','WHITE_A','WHITE_K','WHITE_REG_OUT','WHITE_BASE','BLUE_LED_A','BLUE_LED_K','VBAT_RAW','VBAT_FUSED','CHG_FUSED','CHG_PLUS','CHG_MINUS','5V_AON','RELAY_LOW','CHARGE_CTRL','RELAY_GATE','PILOT_LED_A','PILOT_LOOP','PILOT_SENSE','5V_PI','UART_TX','UART_RX','RS485_A','RS485_B','RS485_REF','3V3_AON','RTC_SDA','RTC_SCL','WAKE_N','MAG_N','SW_SENSE','HOLD_PI','POWER_ON','PNP_BASE','SET_NODE','Q5_BASE','PILOT_ACTIVE_N','BLUE_CTRL','BLUE_GATE']}
def net(n,*pins):
 for p in pins: N[n] += p

def part(lib,name,ref,value,fp): return Part(lib,name,ref=ref,value=value,footprint=fp)
def r(ref,value,a,b):
 p=part('Device','R',ref,value,res);net(a,p[1]);net(b,p[2]);return p
def connector(ref,value,count,labels):
 p=part('Connector_Generic','Conn_01x%02d'%count,ref,value,conn.format('%02d'%count))
 for pin,n in enumerate(labels,1):
  if n is None: p[pin] += NC
  else: net(n,p[pin])
 return p
# Pi GPIO breakout is a 2x20 header for a ribbon to the Pi; Pi powered separately via USB-C.
p=part('Connector_Generic','Conn_02x20_Odd_Even','J1','RASPBERRY_PI_GPIO','Connector_PinHeader_2.54mm:PinHeader_2x20_P2.54mm_Vertical')
for pin,n in {1:'3V3_PI',3:'SDA',5:'SCL',6:'GND',7:'TEMP_1WIRE',8:'UART_TX',9:'GND',10:'UART_RX',11:'M_STEP',12:'M_DIR',13:'M_ENABLE_N',14:'GND',15:'WHITE_EN',16:'BLUE_EN',18:'CHARGE_CTRL',20:'GND',22:'PILOT_SENSE',25:'GND',29:'SW_SENSE',30:'GND',34:'GND',37:'HOLD_PI',39:'GND'}.items(): net(n,p[pin])
for pin in [2,4,17,19,21,23,24,26,27,28,31,32,33,35,36,38,40]: p[pin] += NC
# Driver carrier has Pololu-compatible pin order: confirm physical red carrier before insertion.
m=part('Connector_Generic','Conn_02x08_Counter_Clockwise','U1','A4988_CARRIER_VERIFY_PINOUT','Module:Pololu_Breakout-16_15.2x20.3mm')
for pin,n in {1:'M_ENABLE_N',2:'GND',3:'GND',4:'GND',5:'3V3_PI',6:'3V3_PI',7:'M_STEP',8:'M_DIR',9:'GND',10:'3V3_PI',11:'M1B',12:'M1A',13:'M2A',14:'M2B',15:'GND',16:'VBAT_SW'}.items(): net(n,m[pin])
r('R1','10k','M_ENABLE_N','3V3_PI');r('R2','10k','M_STEP','GND');r('R3','10k','M_DIR','GND')
c=part('Device','C_Polarized','C1','100uF 50V','Capacitor_THT:CP_Radial_D8.0mm_P3.50mm');net('VBAT_SW',c[1]);net('GND',c[2])
c=part('Device','C','C2','100nF',cap);net('3V3_PI',c[1]);net('GND',c[2])
connector('J2','MOTOR_COILS_VERIFY',4,['M1A','M1B','M2A','M2B'])
# White LED constant current source. Pin mapping fixed by KiCad LM317 TO-220 symbol.
u=part('Regulator_Linear','LM317_TO-220','U2','LM317_TO220','Package_TO_SOT_THT:TO-220-3_Vertical')
net('9V_OPT',u['VI']);net('WHITE_REG_OUT',u['VO']);net('WHITE_A',u['ADJ'])
r('R4','20R 1% 0.25W','WHITE_REG_OUT','WHITE_A')
q=part('Transistor_BJT','2N3904','Q1','2N3904','Package_TO_SOT_THT:TO-92_Inline')
net('WHITE_BASE',q['B']);net('WHITE_K',q['C']);net('GND',q['E'])
r('R5','330R','WHITE_EN','WHITE_BASE');r('R6','47k','WHITE_BASE','GND')
connector('J3','WHITE_LED',2,['WHITE_A','WHITE_K'])
# Blue driver interface ONLY: connector positions and pin order are unknown, use individually labelled pads.
connector('J4','BLUE_DRIVER_9V_IN',2,['9V_OPT','GND'])
connector('J5','BLUE_DRIVER_CTRL',2,['BLUE_CTRL','GND'])

# ADS1115 uses a placeholder header: PCB ordering MUST be checked against physical board.
connector('J6','ADS1115_INTERFACE_VERIFY',4,['3V3_PI','GND','SDA','SCL'])
connector('J7','ADS1115_A0_VERIFY',2,['BAT_SENSE','GND'])
r('R8','100k 1%','VBAT_SW','BAT_SENSE');r('R9','10k 1%','BAT_SENSE','GND')
c=part('Device','C','C3','100nF',cap);net('BAT_SENSE',c[1]);net('GND',c[2])
connector('J8','I2C_AS7265X',4,['3V3_PI','GND','SDA','SCL'])
atlas=connector('J9','ATLAS_GEN2_SOCKET_VERIFY',5,['3V3_PI',None,'GND','SDA','SCL']);atlas.footprint='Connector_PinSocket_2.54mm:PinSocket_1x05_P2.54mm_Vertical'
connector('J10','DS18B20',3,['3V3_PI','GND','TEMP_1WIRE'])
r('R10','4k7','TEMP_1WIRE','3V3_PI')
# Power entry connectors model switched rails only; distribution, charge and wake are not designed yet.
connector('J11','INPUT_SWITCHED_BATTERY',2,['VBAT_SW','GND'])


# Common battery pair and dual isolated charging contacts; fuse ratings to be selected.
connector('J13','BATTERY_COMMON_PAIR',2,['VBAT_RAW','GND'])
connector('J14','TO_SWITCH_INPUT_FUSED',2,['VBAT_FUSED','GND'])
connector('J18','EN3_8PIN_ASSIGNMENT_VERIFY',8,['CHG_PLUS','CHG_MINUS',None,'GND','RS485_A','RS485_B','RS485_REF','PILOT_LOOP'])
connector('J19','RS485_DFR0845_UART_ADAPTER',4,['UART_RX','UART_TX','GND','3V3_PI'])
connector('J20','RS485_DFR0845_BUS_ADAPTER',4,[None,'RS485_REF','RS485_A','RS485_B'])
connector('J23','PI_5V_USBC_LEAD_VERIFY',2,['5V_PI','GND'])
fusefp='Fuse:Fuseholder_Clip-5x20mm_Littelfuse_111_Inline_P20.00x5.00mm_D1.05mm_Horizontal'
f=part('Device','Fuse','F1','F1_LOAD_RATING_TBD',fusefp);net('VBAT_RAW',f[1]);net('VBAT_FUSED',f[2])
f=part('Device','Fuse','F2','F2_CHARGE_RATING_TBD',fusefp);net('VBAT_RAW',f[1]);net('CHG_FUSED',f[2])
k=part('Relay','G2RL-2','K1','G2RL-2_DC5','Relay_THT:Relay_DPDT_Omron_G2RL-2')
for pin,n in {'A1':'5V_AON','A2':'RELAY_LOW','11':'CHG_FUSED','14':'CHG_PLUS','21':'GND','24':'CHG_MINUS'}.items():net(n,k[pin])
k['12'] += NC
k['22'] += NC
q2=part('Transistor_FET','AO3400A','Q2','AO3400A','Package_TO_SOT_SMD:SOT-23')
net('RELAY_GATE',q2['G']);net('RELAY_LOW',q2['D']);net('GND',q2['S'])
r('R11','1k','CHARGE_CTRL','RELAY_GATE');r('R12','47k','RELAY_GATE','GND')
d=part('Diode','1N4007','D1','1N4007','Diode_THT:D_DO-41_SOD81_P10.16mm_Horizontal');net('5V_AON',d['K']);net('RELAY_LOW',d['A'])
# Presence input is read by Pi; it is NOT an independent hardware charge interlock.
r('R13','680R','5V_AON','PILOT_LED_A');r('R14','10k','3V3_PI','PILOT_SENSE')
u=part('Isolator','LTV-817','U3','LTV-817','Package_DIP:DIP-4_W7.62mm')
net('PILOT_LED_A',u[1]);net('PILOT_LOOP',u[2]);net('GND',u[3]);net('PILOT_ACTIVE_N',u[4])
d=part('Diode','1N4007','D2','1N4007_PILOT_REVERSE','Diode_THT:D_DO-41_SOD81_P10.16mm_Horizontal');net('PILOT_LED_A',d['K']);net('PILOT_LOOP',d['A'])


# DFR1015: input + / input - / selected output + / output -.
# The local footprint position and two pads per signal are interpreted from supplier drawing; VERIFY actual board.
for ref,value,input_net,output_net in [('U4','DFR1015_5V_AON','VBAT_FUSED','5V_AON'),('U5','DFR1015_5V_PI','VBAT_SW','5V_PI'),('U6','DFR1015_9V_OPT','VBAT_SW','9V_OPT')]:
 p=connector(ref,value,4,[input_net,'GND',output_net,'GND'])
 p.footprint='Cross:DFR1015_8pad_BORRADOR'


# Programmable wake candidate: DS3231 alarm, magnet, PNP level conversion and Pi power-hold.
# All parts are provisional; Pi hold must remain asserted until Linux shutdown finishes.
ldo=part('Regulator_Linear','MCP1700x-330xxTO','U7','MCP1700_3V3_AON','Package_TO_SOT_THT:TO-92_Inline')
net('5V_AON',ldo['VI']);net('3V3_AON',ldo['VO']);net('GND',ldo['GND'])
for ref,n in [('C4','5V_AON'),('C5','3V3_AON')]:
 p=part('Device','C',ref,'1uF',cap);net(n,p[1]);net('GND',p[2])
# RTC module interface logical order; no compatible physical module or socket has been confirmed.
connector('J24','RTC_3V3_GND_SDA_SCL_INT_VERIFY',5,['3V3_AON','GND','RTC_SDA','RTC_SCL','WAKE_N'])
for ref,lo,hi in [('Q3','SDA','RTC_SDA'),('Q4','SCL','RTC_SCL')]:
 p=part('Transistor_FET','BSS138',ref,'BSS138','Package_TO_SOT_SMD:SOT-23')
 net('3V3_PI',p['G']);net(lo,p['S']);net(hi,p['D'])
r('R15','10k','RTC_SDA','3V3_AON');r('R16','10k','RTC_SCL','3V3_AON')
r('R17','10k','WAKE_N','3V3_AON')
r('R18','10k','SET_NODE','3V3_AON');r('R19','100k','Q5_BASE','WAKE_N')
p=part('Transistor_BJT','2N3904','Q5','2N3904_WAKE_INVERTER','Package_TO_SOT_THT:TO-92_Inline')
net('Q5_BASE',p['B']);net('GND',p['E']);net('SET_NODE',p['C'])
r('R20','100k','POWER_ON','GND');r('R23','100k','HOLD_PI','GND')
u=part('4xxx','4013','U8','CD4013_LATCH_PROVISIONAL','Package_DIP:DIP-14_W7.62mm')
for pin,n in {5:'GND',3:'GND',6:'SET_NODE',4:'HOLD_PI',1:'POWER_ON',9:'GND',11:'GND',8:'GND',10:'GND',14:'3V3_AON',7:'GND'}.items():net(n,u[pin])
for pin in [2,12,13]:u[pin] += NC
p=part('Device','C','C6','100nF',cap);net('3V3_AON',p[1]);net('GND',p[2])
# Hardware charge interlock; independent of Pi command when pilot loop is open.
r('R24','10k','PILOT_ACTIVE_N','3V3_AON')
p=part('Transistor_FET','AO3400A','Q6','PILOT_GATE_INHIBIT','Package_TO_SOT_SMD:SOT-23');net('PILOT_ACTIVE_N',p['G']);net('RELAY_GATE',p['D']);net('GND',p['S'])
for ref,anode in [('D6','WAKE_N'),('D7','PILOT_SENSE')]:
 d=part('Diode','1N5819',ref,'PILOT_SIGNAL','Diode_THT:D_DO-41_SOD81_P10.16mm_Horizontal');net(anode,d['A']);net('PILOT_ACTIVE_N',d['K'])
# Blue driver is disabled during Pi boot by a pull-up and shunt FET; active-low GPIO.
r('R25','4k7','BLUE_GATE','3V3_PI')
p=part('Transistor_FET','AO3400A','Q7','BLUE_DISABLE_FET','Package_TO_SOT_SMD:SOT-23');net('BLUE_GATE',p['G']);net('BLUE_CTRL',p['D']);net('GND',p['S'])
d=part('Diode','1N5819','D8','BLUE_GPIO_INVERT','Diode_THT:D_DO-41_SOD81_P10.16mm_Horizontal');net('BLUE_GATE',d['A']);net('BLUE_EN',d['K'])
# Magnet N/O reed is read by Pi and can request wake. Separate diodes avoid powering unpowered Pi GPIO.
connector('J25','MAGNETIC_REED_NORMALLY_OPEN',2,['MAG_N','GND'])
r('R21','10k','MAG_N','3V3_AON');r('R22','10k','SW_SENSE','3V3_PI')
for ref,anode in [('D4','WAKE_N'),('D5','SW_SENSE')]:
 d=part('Diode','1N5819',ref,'1N5819_REED','Diode_THT:D_DO-41_SOD81_P10.16mm_Horizontal');net(anode,d['A']);net('MAG_N',d['K'])
connector('J26','SWITCH_MODULE_ON_CONTROL_VERIFY',2,['POWER_ON','GND'])

# Label-based generated schematic. All copper remains unrouted until verified.
generate_schematic(filepath='.',top_name='cross_v7_draft',title='CROSS V2 — PARTIAL / NOT FOR FABRICATION',auto_stub=True,do_backup=False)
generate_netlist(file_='cross_v7_draft.net',do_backup=False)
