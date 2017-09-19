import m5
from m5.objects import *

from cache import *

from optparse import OptionParser

parser = OptionParser()
parser.add_option('--l1i_size', help="L1 inst. cache size");
parser.add_option('--l1d_size', help="L2 data cache size");
parser.add_option('--l2_size',  help="Unified L2 cache size");

(options, args) = parser.parse_args()

system = System()

system.clk_domain = SrcClockDomain()
system.clk_domain.clock = '1GHz'
system.clk_domain.voltage_domain = VoltageDomain()

system.mem_mode = 'timing'
system.mem_ranges = [AddrRange('512MB')]

system.cpu = TimingSimpleCPU()

system.cpu.icache = L1ICache(options)
system.cpu.dcache = L1DCache(options)

system.cpu.icache.connectCPU(system.cpu)
system.cpu.dcache.connectCPU(system.cpu)

system.l2bus = L2XBar()
system.cpu.icache.connectBus(system.l2bus)
system.cpu.dcache.connectBus(system.l2bus)

system.membus2 = SystemXBar()

system.l2cache = L2Cache(options)
system.l2cache.connectCPUSideBus(system.l2bus)
system.l2cache.connectMemSideBus(system.membus2)

system.cpu.createInterruptController()
system.cpu.interrupts[0].pio = system.membus2.master
system.cpu.interrupts[0].int_master = system.membus2.slave
system.cpu.interrupts[0].int_slave = system.membus2.master
system.system_port = system.membus2.slave


system.mem_ctrl = DDR3_1600_8x8()
system.mem_ctrl.range = system.mem_ranges[0]
system.mem_ctrl.port = system.membus2.master

process = Process()
process.cmd = ['tests/test-progs/hello/bin/x86/linux/hello']
#process.cmd = ['tests/test-progs/hello/bin/x86/linux/loop']
system.cpu.workload = process
system.cpu.createThreads()

root = Root(full_system = False, system = system)
m5.instantiate()

print "Beginning Simulation"
exit_event = m5.simulate()
	
print 'Exiting @ tick %i' % (m5.curTick())


