from pygmyhdl import *

# initialisation of pygmyhdl
initialize()

# The following function will define a chunk of logic, hence the @chunk decorator precedes it.
# The blinker logic takes three inputs:
#   clk_i:  This is a clock signal input.
#   led_o:  This is an output signal that drives an LED on and off.
#   length: This is the number of bits in the counter that generates the led_o output.
@chunk
def blinker(clk_i, led_o, length):
    
    # Define a multi-bit signal (or bus) with length bits.
    # Assign it a display name of 'cnt' for use during simulation.
    cnt = Bus(length, name='cnt')
    
    # Define a piece of sequential logic. Every time there is a positive
    # edge on the clock input (i.e., it goes from 0 -> 1), the value of
    # cnt is increased by 1. So over a sequence of clock pulses, the
    # cnt value will progress 0, 1, 2, 3, ...
    @seq_logic(clk_i.posedge)
    def counter_logic():
        cnt.next = cnt + 1

    # This is a piece of simple combinational logic. It just connects the
    # most significant bit (MSB) of the counter to the LED output.
    @comb_logic
    def output_logic():
        led_o.next = cnt[length-1]

clk = Wire(name='clk')  # This is a single-bit signal that carries the clock input.
led = Wire(name='led')  # This is another single-bit signal that receives the LED output.

# Attach the clock and LED signals to a 3-bit blinker circuit.
blinker(clk_i=clk, led_o=led, length=3)

# Run a simulation of the LED blinker.
clk_sim(clk, num_cycles=16)

# TEST
#show_waveforms()

# Generation of vhdl file
# Give it the function name, signal connections, and counter size.
toVHDL(blinker, clk_i=clk, led_o=led, length=22)

