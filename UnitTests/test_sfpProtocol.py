from unittest import TestCase

from sfp import sfpProtocol
from sfpErrors import *
from pids import MAX_FRAME_LENGTH
import pids

sp = sfpProtocol()

# build a test frame
packet = [pids.MEMORY] + list(range(5))
length = 1 + len(packet) + 2
frame = [length, ~length&0xFF] + packet
sum = sumsum = 0
for byte in frame:
    sum += byte
    sumsum += sum
frame += [sum&0xFF, sumsum&0xFF]

class TestSfpProtocol(TestCase):
    def setUp(self):
        sp.resetRx()
        sp.result = NO_ERROR
        sp.message = ""
        sp.VERBOSE = True

    def fail(self):
        pass

    def test_rxBytes(self):
        sp.rxBytes(frame)
        self.assertEqual(sp.receivedPool.qsize(), 1)

    def test_hunting(self):
        self.assertFalse(sp.hunting())

        sp.frame.extend([0])
        self.assertTrue(sp.hunting())
        self.assertEqual(sp.result, LENGTH_IGNORE)
        self.assertEqual(sp.sfpState, sp.hunting)
        self.assertFalse(sp.hunting())

        sp.resetRx()
        sp.frame.extend([1])
        sp.hunting()
        self.assertEqual(sp.result, LENGTH_SHORT)
        self.assertEqual(sp.sfpState, sp.hunting)

        self.setUp()
        sp.frame.extend([MAX_FRAME_LENGTH])
        sp.hunting()
        self.assertEqual(sp.result, LENGTH_OK)
        self.assertEqual(sp.sfpState, sp.syncing)

        if 254 > MAX_FRAME_LENGTH:
            self.setUp()
            sp.frame.extend([254])
            sp.hunting()
            self.assertEqual(sp.result, LENGTH_LONG)
            self.assertEqual(sp.sfpState, sp.hunting)

    def test_syncing(self):
        sp.length = 100
        self.assertFalse(sp.syncing())
        self.assertEqual(sp.sfpState, sp.hunting)

        self.setUp()
        sp.frame.extend([sp.length])
        self.assertTrue(sp.syncing())
        self.assertEqual(sp.result, NOT_SYNCED)
        self.assertEqual(sp.sfpState, sp.hunting)

        self.setUp()
        sp.frame.extend([~sp.length&0xFF])
        self.assertTrue(sp.syncing())
        self.assertEqual(sp.result, FRAME_SYNCED)
        self.assertEqual(sp.sfpState, sp.receiving)

    def test_receiving(self):
        sp.length = 5
        self.assertFalse(sp.receiving())

        self.fail()

    def test_resetRx(self):
        sp.sfpState = None
        sp.frame.extend([254])
        sp.resetRx()
        self.assertEqual(sp.sfpState, sp.hunting)
        self.assertEqual(len(sp.frame), 0)

    def test_initRx(self):
        sp.initRx()
        self.assertEqual(sp.result, RX_RESET)

    def test_checkLength(self):
        sp.length = 0
        self.assertEqual(sp.checkLength(), LENGTH_IGNORE)
        sp.length = 3
        self.assertEqual(sp.checkLength(), LENGTH_SHORT)
        sp.length = MAX_FRAME_LENGTH + 1
        self.assertEqual(sp.checkLength(), LENGTH_LONG)
        sp.length = MAX_FRAME_LENGTH
        self.assertEqual(sp.checkLength(), LENGTH_OK)

    def test_checkSync(self):
        sp.length =100
        for sync in range(256):
            if sync == ~sp.length&0xFF:
                self.assertTrue(sp.checkSync(sync))
            else:
                self.assertFalse(sp.checkSync(sync))

    def test_frameOk(self):
        sp.length = frame[0]
        sp.frame.extend(frame[1:])
        self.assertTrue(sp.frameOk())

    def test_checkSum(self):
        self.assertEqual(sp.checkSum(frame[:-2]), (frame[-2], frame[-1]))

    def test_setHandler(self):
        self.assertEqual(sp.handler.get(pids.MEMORY), None)
        sp.setHandler(pids.MEMORY, 1)
        self.assertEqual(sp.handler[pids.MEMORY], 1)

    def test_removeHandler(self):
        sp.setHandler(pids.MEMORY, 1)
        sp.removeHandler(pids.MEMORY)
        self.assertEqual(sp.handler.get(pids.MEMORY), None)

    def test_distributer(self):
        self.fail()

    def test_sendNPS(self):
        sp.sendNPS(pids.MEMORY, packet[1:])
        self.assertEqual(sp.transmitPool.qsize(), 1)
        self.assertEqual(sp.transmitPool.get(), frame)

    def test_txBytes(self):
        self.fail()
