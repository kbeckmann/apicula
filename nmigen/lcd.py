from nmigen import *
from nmigen.build import *

import os
import subprocess
import itertools

# Depends on pergola_projects. To install:
# python3 -m pip install --user git+https://github.com/kbeckmann/pergola_projects
from pergola.gateware.vga import *
from pergola.gateware.vga_testimage import *

from tangnano import TangNanoPlatform

class LCDExample(Elaboratable):
    def elaborate(self, platform):
        m = Module()

        def get_all_resources(name):
            resources = []
            for number in itertools.count():
                try:
                    resources.append(platform.request(name, number))
                except ResourceError:
                    break
            return resources
        
        def get_all_outputs(name):
            return Cat([res.o for res in get_all_resources(name)])


        leds = get_all_outputs("led")

        clk_freq = platform.default_clk_frequency
        timer = Signal(range(int(clk_freq//2)), reset=int(clk_freq//2) - 1)
        flops = Signal(len(leds))

        m.d.comb += Cat(leds).eq(flops)
        with m.If(timer == 0):
            m.d.sync += timer.eq(timer.reset)
            m.d.sync += flops.eq(~flops)
        with m.Else():
            m.d.sync += timer.eq(timer - 1)

        lcd_r = platform.request("lcd_r", 0)
        lcd_g = platform.request("lcd_g", 0)
        lcd_b = platform.request("lcd_b", 0)
        lcd_vs = platform.request("lcd_vs", 0)
        lcd_hs = platform.request("lcd_hs", 0)
        lcd_den = platform.request("lcd_den", 0)
        lcd_pclk = platform.request("lcd_pclk", 0)

        vga_output = Record([
            ('hs', 1),
            ('vs', 1),
            ('blank', 1),
        ])
        vga_parameters = VGAParameters(
                h_front=24,
                h_sync=72,
                h_back=96,
                h_active=800,
                v_front=3,
                v_sync=7,
                v_back=10,
                v_active=480,
            )
        m.submodules.vga = VGAOutputSubtarget(vga_output, vga_parameters)

        r = Signal(8)
        g = Signal(8)
        b = Signal(8)
        m.submodules.imagegen = TestImageGenerator(
                vsync=vga_output.vs,
                h_ctr=m.submodules.vga.h_ctr,
                v_ctr=m.submodules.vga.v_ctr,
                r=r,
                g=g,
                b=b,
                speed=0
            )

        m.d.comb += [
            lcd_den.eq(~vga_output.blank),
            lcd_pclk.eq(ClockSignal()),
            lcd_hs.eq(vga_output.hs),
            lcd_vs.eq(vga_output.vs),
            lcd_r.eq(r[-5:]),
            lcd_g.eq(g[-6:]),
            lcd_b.eq(b[-5:]),
        ]

        return m

if __name__ == "__main__":
    p = TangNanoPlatform()
    p.build(LCDExample(), do_program=True)
