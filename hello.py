import m5
from m5.objects import *

root = Root(full_system=False)

root.hello = HelloObject()
root.hello.time_to_wait = '2us'
root.hello.number_of_fires = 5
root.hello.goodbye_object = GoodbyeObject(buffer_size='100B')

m5.instantiate()

print "Beinning Simulation!"

exit_event = m5.simulate()

print 'Exiting @ tick %i' % m5.curTick()
