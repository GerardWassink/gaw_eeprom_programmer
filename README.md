# Microcode for 8 bit computer instructions

I am building an 8 bit computer, and for this computer I designed 8 bit instructions, each of which can have up to 8 microcode steps. I defined up to 24 control signals (thus needing 3 bytes per step / Control Word).

## Decoding the Instructions
The way I chose to decode each instruction into Control Words is by offering the contents of the instruction register as part of the address into an EEPROM, that will spit out the control word. The EEPROMs have 8 bit values, so to hold one control word, I need 3 EEPROMs in parallel.

## Programming the EEPROMs
To be able to write the data into EEPROMs I'm using an Arduino EEPROM programmer as suggested by Ben Eater in one of his magnificent video's. To be able to hold my control words I would have to define them as uint32_t variables (which are 4 bytes long).


## Practical solution
I named those 3 EEPROMs CU02, CU01 and CU00, from msb to lsb

Control word CW is spread over the EEPROMs as follows:

- CU02 - (CW >> 16) & 0xFF
- CU01 - (CW >> 8) & 0xFF
- CU00 - CW & 0xFF

so in every memory location:

- CU02 contains bits 23 to 16
- CU01 contains bits 15 to 08
- CU00 contains bits 07 to 00

That's the plan.

But...

## Arduino memory problem
The complete microcode consists of 256 instructions x 8 steps per step. That's 2 KB of memory for that table alone. When choosing the solution mentioned above, this amounts to 8192 bytes of storage for the microcode, because we would have to multiply by 4 bytes to accomodate for the uint32_t variables. 

And alas, this will not fit in Arduino Nano's memory...

## Solution 1
If I would choose to go along this path, I have to chop it up in 8 (eight) parts to be able to program the EEPROMs, but as a programmer I hate that solution, because every programming change would have to be copied 8 times as well...

## Solution 2
Should I choose to program one EEPROM at a time, I would need only byte-sized variables, 256 * 8 of them, which would need 2K bytes of memory. Even this wouldn't fit, The Nano can only process half of that...

So, what else?

## Solution 3
I chose to construct a python program on my laptop to hold all the control words, since the laptop has plenty memory. This python program has to be able to communicate with the Arduino to present commands to it. The function of the Arduino would then be to read and write bytes under control of the python program.

That is what this project is about. I made a start and am still working on it.

