# Explanation of the Control unit and the associated Control words in my 8 bit computer

In my 8 bit computer we can have 256 instructions, they range from 0 to 255, or 0x00 to 0xFF. Instructions can be expressed in 8 bits.

Per instruction we would like to have the possibility of having 8 steps of 'microcode' to perform the actual parts of the instruction in the computer. The number of the 8 possible control words per instruction range from 0 - 7, and can be expressed in 3 bits.

## Example: the instruction 'LDA B'
For every instruction we have to get the value from memory that is being pointed to by the Program Counter (PC); this value must be put into the Instruction Register (IR) and when this is done, the PC must be incremented by 1. To achieve this we need two control words, that work as follows:

##### CW0	

- Put the value of the PC on the common bus
- get the value from the bus and put in into the memory (RAM) address register MAR

##### CW1

- put the contents of RAM pointed to by MAR on the bus
- get the value from the bus and put it into the Instruction Register (IR)
- enable the PC to be incremented at the next clock pulse

Further control words depend on the specifics of each instruction; for example when we want to transfer the contents of register A (RA) to register B (RB), the micro code control word for that could be:

##### CW2	

- put the value in RA on the bus
- get the value from the bus and put it into RB

So this instruction needs three Control Words to do it's job. When we leave it at this, we would have to wait for 5 clock pulses more to be able to get to the next instruction. For this reason I made a new control signal called RSC. This signal in the Control Word will reset the Microcode step Counter (MC).

##### CW3 

- reset the Microcode step Counter to 0
	

## Memory
Now, when we would have 8 bit control words[^1], this setup would already need 2 Kilobytes of memory to store all the control words (256 * 8).

##### Addressing
In my Control Unit, to 'decode' the instruction to it's corresponding Control Words, I store the Control Words in EEPROM. This means that we need an 'address width' of 11 bits (8 + 3). Designations (names) of address bits start counting at zero on the right (least significant) side, let's call them A10 - A0. 

##### Address parts
Instructions are being read into an Instruction Register (IR). They have bits IR7 - IR0.

Per instruction a counter (the Microcode step Counter - MC) is driven by the computer's clock pulse. It is a hardware circuit that starts at 0 and counts up to 7 in three bits. Let's call these MC2 - MC0.

##### The EEPROM address
Now we can establish the address for our EEPROM:

- A10	- instruction register bit IR7
- A9	- instruction register bit IR6
- A8	- instruction register bit IR5
- A7	- instruction register bit IR4
- A6	- instruction register bit IR3
- A5	- instruction register bit IR2
- A4	- instruction register bit IR1
- A3	- instruction register bit IR0
- A2	- microcode counter MC2
- A1	- microcode counter MC1
- A0	- microcode counter MC0

### Not there yet, more EEPROM memory needed...
[^2] - In my 8 bit computer so far I defined a little over 20 Control signals that all have to have a spot in the definition of the Control Word. Those will not fit in the 8 bits we assumed earlier. For the Control Words that I defined up till now, I need 24 bits, which amounts to 3 bytes per Control Word. This will increase the need for memory to 6 K bytes.

##### Parallel EEPROMs
I chose to use parallel EEPROMs to be able to have all 24 possible Control signals available at once. This means that I will be using 3 EEPROMs of 8 K bytes each. This even gives me the opportunity to expand to a width of 32 bits in the future.

Now, to be able to program all these Control Words in these parallel EEPROMs, I'm going to introduces 'sections' of 2 K bytes in every EEPROM. The EEPROMs will be called (from least to most significant part of the Control Word): CU00 - CU02. 

##### Extra addressing
Now we need two more address bits to address these 'sections'. Lets call them SC0 and SC1, with these we can address all four sections that fit in our 8K byte EEPROMs.

##### The final EEPROM address
Now we can establish the final address for our EEPROM:

- A12	- Section number bit SC1
- A11	- Section number bit SC0
- A10	- instruction register bit IR7
- A9	- instruction register bit IR6
- A8	- instruction register bit IR5
- A7	- instruction register bit IR4
- A6	- instruction register bit IR3
- A5	- instruction register bit IR2
- A4	- instruction register bit IR1
- A3	- instruction register bit IR0
- A2	- microcode counter MC2
- A1	- microcode counter MC1
- A0	- microcode counter MC0

##### Hard wiring section numbers
The address bits SC1 and SC0 will be hard wired to '0' or '1' as follows:

- CU00	- SC1 = '0'; SC0 = '0' (points to section 0, address 0x0000)
- CU01	- SC1 = '0'; SC0 = '1' (points to section 1, address 0x0800)
- CU02	- SC1 = '1'; SC0 = '0' (points to section 2, address 0x1000)


[^1]: We don't, look at "Not there yet..." at [^2]

[^2]: See? we need more...