from nmigen.build import *
# from nmigen.vendor.gowin_gw1n import *
from nmigen_boards.resources import *

import os
import subprocess

from gowin_gw1n import *

class TangNanoPlatform(GowinGW1NPlatform):
    default_clk = "clk24"
    device = "gw1n-1"
    package = "qfn48"
    resources   = [
        Resource("clk24", 0, Pins("R5C20_IOBA", dir="i"),
                 Clock(24e6), Attrs(GLOBAL=True, IO_TYPE="LVCMOS33")),

        # LEDs (R, G, B)
        # *LEDResources(pins="18 16 17", invert=True),
        # *LEDResources(pins="R11C10_IOBB R11C10_IOBA R11C7_IOBA", invert=True),
        *LEDResources(pins="R11C7_IOBA R11C10_IOBA R11C10_IOBB", invert=True),

        # LCD connector (with pin numbers, save for later...)
        # Resource("lcd_r",    0, Pins("27 28 29 30 31")),
        # Resource("lcd_g",    0, Pins("32 33 34 38 39")),
        # Resource("lcd_b",    0, Pins("41 42 43 44 45")),
        # Resource("lcd_vs",   0, Pins("46")),
        # Resource("lcd_hs",   0, Pins("10")),
        # Resource("lcd_den",  0, Pins("5")),
        # Resource("lcd_pclk", 0, Pins("11")),

        # LCD connector
        Resource("lcd_r",    0, Pins("R7C20_IOBA R6C20_IOBH R6C20_IOBG R6C20_IOBF R6C20_IOBD", dir="o")),
        Resource("lcd_g",    0, Pins("R6C20_IOBC R6C20_IOBB R6C20_IOBA R1C17_IOBB R1C17_IOBA R1C14_IOBB", dir="o")),
        Resource("lcd_b",    0, Pins("R1C14_IOBA R1C10_IOBB R1C10_IOBA R1C7_IOBB  R1C7_IOBA", dir="o")),
        Resource("lcd_vs",   0, Pins("R1C5_IOBB", dir="o")),
        Resource("lcd_hs",   0, Pins("R7C1_IOBA", dir="o")),
        Resource("lcd_den",  0, Pins("R6C1_IOBC", dir="o")),
        Resource("lcd_pclk", 0, Pins("R7C1_IOBB", dir="o")),

        # 14=IOB3B, 15=IOB6B
        # *ButtonResources(pins="14 15", invert=True),

        # 9=IOL6G, 8=IOL6F
        # UARTResource(0,
        #     rx="9", tx="8",
        #     attrs=Attrs(IO_TYPE="LVCMOS33", PULLUP=1)
        # ),

        # cs=IOB11A, clk=IOB11B, mosi=IOB14B, miso=IOB16A, wp=IOB14A, hold=IOB16B
        # *SPIFlashResources(0,
        #     cs="19", clk="20", mosi="22", miso="23", wp="21", hold="24",
        # ),
    ]
    connectors = [
    ]

    def toolchain_program(self, products, name):
        openFPGALoader = os.environ.get("OPENFPGALOADER", "openFPGALoader")
        with products.extract("{}.fs".format(name)) as (bitstream):
            print(subprocess.check_call([
                openFPGALoader, "-m", "-b", "tangnano", bitstream
            ]))
