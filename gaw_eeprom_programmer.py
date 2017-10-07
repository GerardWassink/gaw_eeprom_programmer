#!/usr/bin/python

# ------------------------------------------------------------------------
# Program		:	EEPROM_Programmer.py
# Author		:	Gerard Wassink
# Date			:	October 1, 2017
#
# Function		:	convert values for the micro code for an 8 bit 
#					computer into Arduino code for the content of three
#					parallel EEPROMs
#
# ------------------------------------------------------------------------
# 						GNU LICENSE CONDITIONS
# ------------------------------------------------------------------------
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# ------------------------------------------------------------------------
#				Copyright (C) 2015 Gerard Wassink
# ------------------------------------------------------------------------

#import sys
#from interface import ProgrammerInterface
 
#if len(sys.argv) > 2:
#    rom, serial_port, baud_rate = int(sys.argv[1]), sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 57600
#else:
#    raise Exception("Invalid arguments")
 
#
# Define the values for the control signals
#
 
# EEPROM 2, bits D23 - D16
 
CE      = 1 << 23  # 0x800000 - Count Enable
HLT     = 1 << 22  # 0x400000 - Halt
PCI     = 1 << 21  # 0x200000 - PC In
PCO     = 1 << 20  # 0x100000 - PC Out
MAI     = 1 << 19  # 0x080000 - Memory Address In
MI      = 1 << 18  # 0x040000 - Memory In
MO      = 1 << 17  # 0x020000 - Memory Out
IRI     = 1 << 16  # 0x010000 - Instruction Register In
 
# EEPROM 1, bits D15 - D08
 
EO      = 1 << 15  # 0x008000 - Sigma Out (ALU value)
OI      = 1 << 14  # 0x004000 - Output In
AI      = 1 << 13  # 0x002000 - A Register In
AO      = 1 << 12  # 0x001000 - A register Out
BI      = 1 << 11  # 0x000800 - B register In
BO      = 1 << 10  # 0x000400 - B register Out
ALM     = 1 <<  9  # 0x000200 - ALU Mode
AL0     = 1 <<  8  # 0x000100 - ALU function 0
 
# EEPROM 0, bits D07 - D00
 
AL1     = 1 <<  7  # 0x000080 - ALU function 1
AL2     = 1 <<  6  # 0x000040 - ALU function 2
AL3     = 1 <<  5  # 0x000020 - ALU function 3
ALCI    = 1 <<  4  # 0x000010 - ALU Carry In
n3      = 1 <<  3  # 0x000008 - 
n2      = 1 <<  2  # 0x000004 - 
n1      = 1 <<  1  # 0x000002 - 
RSC     = 1 <<  0  # 0x000001 - Reset Step Counter on CU for Microcode Steps
 
#
#   Constant control words for Fetch cycle in every instruction
#
CW_0    = MAI | PCO
CW_1    = MO | IRI | CE
 
#
# Define the control words per machine code instruction
# 256 instructions x 8 bytes = 2K bytes
#
 
instr = {
#
# === NO Operation
#
  0x00: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
#
# === LOAD instructions
#
  0x01: [ CW_0, CW_1, PCO|MAI,                MO|CE|AI,           RSC,                    0,                          0,  0, ], # LDAi val
  0x02: [ CW_0, CW_1, PCO|MAI,                MO|MAI,             MO|AI|CE,               RSC,                        0,  0, ], # LDAm addr

  0x03: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0x04: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0x05: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0x06: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP

 
  0x07: [ CW_0, CW_1, PCO|MAI,                MO|CE|BI,           RSC,                    0,                          0,  0, ], # LDBi val
  0x08: [ CW_0, CW_1, PCO|MAI,                MO|MAI,             MO|BI|CE,               RSC,                        0,  0, ], # LDBm addr

  0x09: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0x0A: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0x0B: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0x0C: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0x0D: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0x0E: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0x0F: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP

# 
# === STORE instructions
#
  0x10: [ CW_0, CW_1, PCO|MAI,                MO|MAI,             AO|MI|CE,               RSC,                        0,  0, ], # STAm addr
  0x11: [ CW_0, CW_1, PCO|MAI,                MO|MAI,             BO|MI|CE,               RSC,                        0,  0, ], # STBm addr

  0x12: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0x13: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0x14: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0x15: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0x16: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0x17: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0x18: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0x19: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0x1A: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0x1B: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0x1C: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0x1D: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0x1E: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0x1F: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP

#
# === ARITHMETIC instructions
#
  0x20: [ CW_0, CW_1, AL3|AL0|EO|AI|CE,       RSC,                0,                      0,                          0,  0, ], # ADD
  0x21: [ CW_0, CW_1, PCO|MAI,                MO|BI,              AL3|AL0|EO|AI|CE,       RSC,                        0,  0, ], # ADDi val
  0x22: [ CW_0, CW_1, PCO|MAI,                MO|MAI,             MO|BI,                  AL3|AL0|EO|AI|CE,           RSC,0, ], # ADDm addr

  0x23: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP

  0x24: [ CW_0, CW_1, AL2|AL1|EO|AI|CE,       RSC,                0,                      0,                          0,  0, ], # SUB
  0x25: [ CW_0, CW_1, PCO|MAI,                MO|BI,              AL2|AL1|EO|AI|CE,       RSC,                        0,  0, ], # SUBi val
  0x26: [ CW_0, CW_1, PCO|MAI,                MO|MAI,             MO|BI,                  AL2|AL1|EO|AI|CE,           RSC,0, ], # SUBm addr

  0x27: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
 
  0x28: [ CW_0, CW_1, AO|BI,                  ALM|AL3|AL2|EO|AI,  AL3|AL0|EO|AI,          AO|BI,                      RSC,0, ], # INCA
  0x29: [ CW_0, CW_1, ALM|AL3|AL2|EO|AI,      AL3|AL0|EO|AI,      AO|BI,                  RSC,                        0,  0, ], # INCB

  0x2A: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0x2B: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0x2C: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0x2D: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0x2E: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0x2F: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
#
# === LOGIC instructions
#
  0x30: [ CW_0, CW_1, ALM|AL2|AL1|EO|AI|CE,   RSC,                0,                      0,                          0,  0, ], # XOR
  0x31: [ CW_0, CW_1, PCO|MAI,                MO|BI,              ALM|AL2|AL1|EO|AI|CE,   RSC,                        0,  0, ], # XORi val
  0x32: [ CW_0, CW_1, PCO|MAI,                MO|MAI,             MO|BI,                  ALM|AL2|AL1|EO|AI|CE,       RSC,0, ], # 0x32 - XORm mem

  0x33: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
 
  0x34: [ CW_0, CW_1, ALM|AL3|AL1|AL0|EO|AI|CE,   RSC,            0,                      0,                          0,  0, ], # AND
  0x35: [ CW_0, CW_1, PCO|MAI,                MO|BI,              ALM|AL3|AL1|AL0|EO|AI|CE,   RSC,                    0,  0, ], # ANDi val
  0x36: [ CW_0, CW_1, PCO|MAI,                MO|MAI,             MO|BI,                  ALM|AL3|AL1|AL0|EO|AI|CE,   RSC,0, ], # ANDm mem
 
  0x37: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP

  0x38: [ CW_0, CW_1, ALM|AL3|AL2|AL1|EO|AI|CE,   RSC,            0,                      0,                          0,  0, ], # OR
  0x39: [ CW_0, CW_1, PCO|MAI,                MO|BI,              ALM|AL3|AL2|AL1|EO|AI|CE,   RSC,                    0,  0, ], # ORi val
  0x3A: [ CW_0, CW_1, PCO|MAI,                MO|MAI,             MO|BI,                  ALM|AL3|AL2|AL1|EO|AI|CE,   RSC,0, ], # ORm mem
 
  0x3B: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP

  0x3C: [ CW_0, CW_1, ALM|EO|AI,              RSC,                0,                      0,                          0,  0, ], # NOTA
  0x3D: [ CW_0, CW_1, ALM|AL2|AL0|EO|BI,      RSC,                0,                      0,                          0,  0, ], # NOTB
  0x3E: [ CW_0, CW_1, ALM|AL1|AL0|EO|AI,      RSC,                0,                      0,                          0,  0, ], # CLRA
  0x3F: [ CW_0, CW_1, ALM|AL1|AL0|EO|BI,      RSC,                0,                      0,                          0,  0, ], # CLRB
#
# === JUMP instructions
#
  0x40: [ CW_0, CW_1, PCO|MAI,                MO|PCI,             RSC,                    0,                          0,  0, ], # JMPi val
  0x41: [ CW_0, CW_1, PCO|MAI,                MO|MAI,             MO|PCI,                 RSC,                        0,  0, ], # JMPm addr

  0x42: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0x43: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0x44: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0x45: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0x46: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0x47: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0x48: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0x49: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0x4A: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0x4B: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0x4C: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0x4D: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0x4E: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0x4F: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP

#
# === OUTPUT instructions
#
  0x50: [ CW_0, CW_1, AO|OI,                  RSC,                0,                      0,                          0,  0, ], # OUTA
  0x51: [ CW_0, CW_1, BO|OI,                  RSC,                0,                      0,                          0,  0, ], # OUTB
 
  0x52: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0x53: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP

  0x54: [ CW_0, CW_1, PCO|MAI,                MO|OI|CE,           RSC,                    0,                          0,  0, ], # OUTi
  0x55: [ CW_0, CW_1, PCO|MAI,                MO|MAI,             MO|OI|CE,               RSC,                        0,  0, ], # OUTm

  0x56: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0x57: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0x58: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0x59: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0x5A: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0x5B: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0x5C: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0x5D: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0x5E: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0x5F: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
#
# === MOVE instructions
#
  0x60: [ CW_0, CW_1, PCO|MAI,                MO|BI|CE,           PCO|MAI,                BO|MI|CE,                   RSC,0, ], # MOVi val
  0x61: [ CW_0, CW_1, PCO|MAI,                MO|MAI,             MO|BI|CE,               PCO|MAI,            BO|MI|CE, RSC, ], # MOVm ad1, ad2

  0x62: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0x63: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0x64: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0x65: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0x66: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0x67: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0x68: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0x69: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0x6A: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0x6B: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0x6C: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0x6D: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0x6E: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0x6F: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP

  0x70: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0x71: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0x72: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0x73: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0x74: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0x75: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0x76: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0x77: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0x78: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0x79: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0x7A: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0x7B: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0x7C: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0x7D: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0x7E: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0x7F: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP

  0x80: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0x81: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0x82: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0x83: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0x84: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0x85: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0x86: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0x87: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0x88: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0x89: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0x8A: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0x8B: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0x8C: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0x8D: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0x8E: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0x8F: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP

  0x90: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0x91: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0x92: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0x93: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0x94: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0x95: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0x96: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0x97: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0x98: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0x99: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0x9A: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0x9B: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0x9C: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0x9D: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0x9E: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0x9F: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP

  0xA0: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0xA1: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0xA2: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0xA3: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0xA4: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0xA5: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0xA6: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0xA7: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0xA8: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0xA9: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0xAA: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0xAB: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0xAC: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0xAD: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0xAE: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0xAF: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP

  0xB0: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0xB1: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0xB2: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0xB3: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0xB4: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0xB5: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0xB6: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0xB7: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0xB8: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0xB9: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0xBA: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0xBB: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0xBC: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0xBD: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0xBE: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0xBF: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP

  0xC0: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0xC1: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0xC2: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0xC3: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0xC4: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0xC5: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0xC6: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0xC7: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0xC8: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0xC9: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0xCA: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0xCB: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0xCC: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0xCD: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0xCE: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0xCF: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP

  0xD0: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0xD1: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0xD2: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0xD3: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0xD4: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0xD5: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0xD6: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0xD7: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0xD8: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0xD9: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0xDA: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0xDB: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0xDC: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0xDD: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0xDE: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0xDF: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP

  0xE0: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0xE1: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0xE2: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0xE3: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0xE4: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0xE5: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0xE6: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0xE7: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0xE8: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0xE9: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0xEA: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0xEB: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0xEC: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0xED: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0xEE: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0xEF: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP

  0xF0: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0xF1: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0xF2: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0xF3: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0xF4: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0xF5: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0xF6: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0xF7: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0xF8: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0xF9: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0xFA: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0xFB: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0xFC: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0xFD: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
  0xFE: [ CW_0, CW_1, RSC,                    0,                  0,                      0,                          0,  0, ], # NOP
#
# === HALT instruction
#
  0xFF: [ MAI|PCO, MO|IRI|CE, HLT,            RSC,                0,                      0,                          0,  0, ] # HLT
}


#
# === Establish interface
#
#interface = ProgrammerInterface(serial_port, baud_rate)


#
# === Clean the EEPROM
#
#cleanEEPROM():
#	for i in range(0, 8191):
#		interface.write(i, 0)
#		if (i % 64) == 0:
#			print ".",

#
# === Generate commands for the Arduino programmer
#
def writeEEPROM(rom):
	base = rom << 11						# segments of 2048 bytes per 'ROM'
	print "# ==="
	print "# === Contents of ROM ", rom, " base addres is 0x%04X" % base
	print "# ==="
	for op, contr in sorted(instr.iteritems()):	# iterate through instructions
		address = base + (op << 3)			# block of 8 micro code steps
		print "WR 0x%04X" % address,		# base address for this instruction
		for i in range(0, len(contr)):		# iterate through microcode steps and
											# 	print only part
			print "0x%02X" % ((contr[i] >> (rom * 8)) & 0xFF), 	# for this ROM
		print "!"							# comment and line end


#
# === (Un)comment routines to be executed
#

#cleanEEPROM()

writeEEPROM(0)
writeEEPROM(1)
writeEEPROM(2)

exit()

# WR 0X0000 0x01 0x02 0x03 0x04 0x05 0x06 0x07 0x08
# .....+....1....+....2....+....3....+....4....+....5

