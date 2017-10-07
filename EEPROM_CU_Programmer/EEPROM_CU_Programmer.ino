/* ------------------------------------------------------------------------- *
 * Name   : EEPROM_Programmer
 * Author : Ben Eater
 *              reworked for python Serial communication  by Gerard Wassink
 * Date   : September 2017
 * Purpose: Program the AT28C64 EEPROM using two 74HC595 shift registers
 * ------------------------------------------------------------------------- *
 *
 * ------------------------------------------------------------------------- *
 *            MIT LICENSE
 * ------------------------------------------------------------------------- *
 * Find info here: https://en.wikipedia.org/wiki/MIT_License
 * ------------------------------------------------------------------------- *
 *            GNU LICENSE CONDITIONS
 * ------------------------------------------------------------------------- *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License along
 * with this program; if not, write to the Free Software Foundation, Inc.,
 * 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
 *
 * ------------------------------------------------------------------------- *
 *       Copyright (C) 2017 Gerard Wassink
 * ------------------------------------------------------------------------- */

#define SHIFT_DATA 2
#define SHIFT_CLK 3
#define SHIFT_LATCH 4
#define EEPROM_D0 5
#define EEPROM_D7 12
#define WRITE_EN 13


/* ------------------------------------------------------------------------------------------ *
 * States enumerated
 * -------------------------------------------------------------------------------------------*/
const char RDY = 0;
const char FIL = 1;
const char CHK = 2;
const char PRC = 3;
const char ERR = 4;
char state = 0;

/* ------------------------------------------------------------------------------------------ *
 * DEBUGGING ON / OFF
 * -------------------------------------------------------------------------------------------*/
// char debug = false;
char debug = true;

/* ------------------------------------------------------------------------------------------ *
 * Various strings, buffers
 * -------------------------------------------------------------------------------------------*/
char errtxt[80} = "";

char buf[80];
int ptr = 0;

char command[80];
char cmd[10];

/* ------------------------------------------------------------------------------------------ *
 * Command codes enumerated
 * -------------------------------------------------------------------------------------------*/
const char CLR = 1;
const char REA = 2;
const char WRI = 3;
const char QUI = 4;
char cc = 0;

char strAdr[10], strOp1[5], strOp2[5], strOp3[5], strOp4[5], strOp5[5], strOp6[5], strOp7[5], strOp8[5];
int adr, op1, op2, op3, op4, op5, op6, op7, op8 = 0;


/* ------------------------------------------------------------------------------------------ *
 * Output the address bits and outputEnable signal using shift registers.
 * -------------------------------------------------------------------------------------------*/
void setAddress(int address, bool outputEnable) {
  shiftOut(SHIFT_DATA, SHIFT_CLK, MSBFIRST, (address >> 8) | (outputEnable ? 0x00 : 0x80));
  shiftOut(SHIFT_DATA, SHIFT_CLK, MSBFIRST, address);

  digitalWrite(SHIFT_LATCH, LOW);
  digitalWrite(SHIFT_LATCH, HIGH);
  digitalWrite(SHIFT_LATCH, LOW);
}


/* ------------------------------------------------------------------------------------------ *
 * Read a byte from the EEPROM at the specified address.
 * -------------------------------------------------------------------------------------------*/
byte readEEPROM(int address) {
  for (int pin = EEPROM_D0; pin <= EEPROM_D7; pin += 1) {
    pinMode(pin, INPUT);
  }
  setAddress(address, /*outputEnable*/ true);

  byte data = 0;
  for (int pin = EEPROM_D7; pin >= EEPROM_D0; pin -= 1) {
    data = (data << 1) + digitalRead(pin);
  }
  return data;
}


/* ------------------------------------------------------------------------------------------ *
 * Write a byte to the EEPROM at the specified address.
 * -------------------------------------------------------------------------------------------*/
void writeEEPROM(int address, byte data) {
  setAddress(address, /*outputEnable*/ false);
  for (int pin = EEPROM_D0; pin <= EEPROM_D7; pin += 1) {
    pinMode(pin, OUTPUT);
  }

  for (int pin = EEPROM_D0; pin <= EEPROM_D7; pin += 1) {
    digitalWrite(pin, data & 1);
    data = data >> 1;
  }
  digitalWrite(WRITE_EN, LOW);
  delayMicroseconds(1);
  digitalWrite(WRITE_EN, HIGH);
  delay(10);
}


/* ------------------------------------------------------------------------------------------ *
 * Read the contents of the EEPROM and print them to the serial monitor.
 * -------------------------------------------------------------------------------------------*/
void printContents(int start, int len) {
  for (int base = start; base <= start+len; base += 16) {
    
    if (base % 256 == 0) {
      Serial.println(" ");
    }
    
    byte data[16];
    for (int offset = 0; offset <= 15; offset += 1) {
      data[offset] = readEEPROM(base + offset);
    }

    char buf[80];
    sprintf(buf, "%04x:  %02x %02x %02x %02x  %02x %02x %02x %02x  -  %02x %02x %02x %02x  %02x %02x %02x %02x",
            base, data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7],
            data[8], data[9], data[10], data[11], data[12], data[13], data[14], data[15]);

    Serial.println(buf);

  }
}


/* ------------------------------------------------------------------------------------------ *
 * Erase the contents of the EEPROM by filling it with all zeroes
 * -------------------------------------------------------------------------------------------*/
void eraseEEPROM() {
  // Erase entire EEPROM
  Serial.print("Erasing EEPROM");
  for (int address = 0; address <= 8191; address += 1) {
    writeEEPROM(address, 0x00);

    if (address % 256 == 0) {
      Serial.print(".");
    }
  }
  Serial.println(" done");
}


/* ------------------------------------------------------------------------------------------ *
 * Hex to int routine
 * -------------------------------------------------------------------------------------------*/
int x2i(char *s) 
{
 int x = 0;
 for(;;) {
   char c = *s;
   if (c >= '0' && c <= '9') {
      x *= 16;
      x += c - '0'; 
   }
   else if (c >= 'a' && c <= 'f') {
      x *= 16;
      x += (c - 'a') + 10; 
   }
   else if (c >= 'A' && c <= 'F') {
      x *= 16;
      x += (c - 'A') + 10; 
   }
   else break;
   s++;
 }
 return x;
}


/* ------------------------------------------------------------------------------------------ *
 * Initial setup routine
 * -------------------------------------------------------------------------------------------*/
void setup() {

  // Set up serial communications:
  Serial.begin(57600);
  Serial.println(" ");
  Serial.println("Start program");

  // Set pins:
  pinMode(SHIFT_DATA, OUTPUT);
  pinMode(SHIFT_CLK, OUTPUT);
  pinMode(SHIFT_LATCH, OUTPUT);
  digitalWrite(WRITE_EN, HIGH);
  pinMode(WRITE_EN, OUTPUT);

  Serial.println("Programmer initialisation complete");

}


/* ------------------------------------------------------------------------------------------ *
 * Repeating routine
 * -------------------------------------------------------------------------------------------*/
void loop() {
  switch (state)
  {
    case RDY:                           // Ready to receive data
      if (debug) Serial.print("> ");
      state = FIL;
      break;
      
    case FIL:                           // Filling the buffer
      if (Serial.available() > 0) {
        char c = Serial.read();
        buf[ptr++] = c;
        buf[ptr] = 0;
      }
      if (ptr > 79) {
        errtxt = "Received more than 80 characters, buffer purged";
        state = ERR;
      } else {
        if ( buf[ptr - 1] == '!' ) {
          buf[--ptr] = 0;
          if (debug) Serial.print("Endfil: ");
          if (debug) Serial.println(buf);
          state = CHK;
        }
      }
      break;
      
    case CHK:                           // Checking buffer contents
      strcpy(command, buf);
      if (strlen(command) >= 2) {
        if (debug) Serial.print("Checking ");
        if (debug) Serial.println(command);
        strncpy(cmd,(command+0),2);
        if (debug) Serial.print("cmd = ");
        if (debug) Serial.println(cmd);
        cc = 0;
        if      (strcmp(cmd, "CL") == 0) cc = CLR;
        else if (strcmp(cmd, "RD") == 0) cc = REA;
        else if (strcmp(cmd, "WR") == 0) cc = WRI;
        else if (strcmp(cmd, "QT") == 0) cc = QUI;
        if (cc != 0) {
          switch (cc) {
            case WRI:
              if (strlen(command) < 49) {
                errtxt = "Insufficient operands for Write command";
                state = ERR;
              } else {
                // get operands (adr plus eight values)
                strncpy(strAdr,(command+5),4);
                strncpy(strOp1,(command+12),2);
                strncpy(strOp2,(command+17),2);
                strncpy(strOp3,(command+22),2);
                strncpy(strOp4,(command+27),2);
                strncpy(strOp5,(command+32),2);
                strncpy(strOp6,(command+37),2);
                strncpy(strOp7,(command+42),2);
                strncpy(strOp8,(command+47),2);
                state = PRC;
              }
              break;
            default:
              state = PRC;
              break;
          }
        } else {
          errtxt = "Invalid command received";
          state = ERR;
        }
      } else {
        errtxt = "Received less than two characters, buffer purged, try again";
        ptr = 0;
        state = ERR;
      }
      break;
      
    case PRC:                           // Processing command
      if (debug) Serial.print("Processing cmd = ");
      if (debug) Serial.println(cmd);
      switch (cc) {
        case CLR:
          eraseEEPROM();
          break;
        
        case REA:
          printContents(0, 8192);
          break;
        
        case WRI:
          Serial.print(x2i(strAdr)); Serial.print(" ");
          Serial.print(x2i(strOp1)); Serial.print(" ");
          Serial.print(x2i(strOp2)); Serial.print(" ");
          Serial.print(x2i(strOp3)); Serial.print(" ");
          Serial.print(x2i(strOp4)); Serial.print(" ");
          Serial.print(x2i(strOp5)); Serial.print(" ");
          Serial.print(x2i(strOp6)); Serial.print(" ");
          Serial.print(x2i(strOp7)); Serial.print(" ");
          Serial.print(x2i(strOp8)); Serial.print(" ");
          Serial.println(" ");
          adr = x2i(strAdr);
          break;
        
        case QUI:
          Serial.println("Programmer ends, reset to restart");
          delay(20);
          exit(0);
          break;
      }
      ptr = 0;
      state = RDY;
      break;
      
    case ERR:                           // Indicating error
      Serial.print("Received: ");
      Serial.println(buf);
      Serial.print("ERROR - ");
      Serial.println(errtxt);
      ptr = 0;
      state = RDY;
      break;
      
  }
      
}
