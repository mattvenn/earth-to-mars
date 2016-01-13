import unittest
import os

from mission import Mission
import mission


class TestMission(unittest.TestCase):

    def test_getLocation(self):
        m = Mission(pi=False)
        assert m.getLocation() is None

    def test_rfids(self):
        m = Mission(pi=False)
        assert len(m.rfid_hash.keys()) == 600

    def test_takeSample(self):
        m = Mission(pi=False)
        location_rfid = m.rfid_hash.keys()[0]
        sample = m.takeSample(location_rfid)
        assert type(sample) is dict
        for k in ['temperature', 'humidity', 'oxygen', 'methane', 'x', 'y']:
            assert sample.has_key(k)

    def test_takeSampleBadLocation(self):
        m = Mission(pi=False)
        location_rfid = 'xxxx'
        with self.assertRaises(Exception) as e:
            sample = m.takeSample(location_rfid)
        assert str(e.exception) == 'unknown location'

    def test_save_data(self):
        m = Mission(pi=False)
        m.deleteData()
        assert not os.path.exists(mission.data_file)
        saved_samples = m.loadData()
        assert type(saved_samples) is list
        assert len(saved_samples) == 0

        location_rfid = m.rfid_hash.keys()[0]
        sample = m.takeSample(location_rfid)
        m.saveData(sample)

        assert os.path.exists(mission.data_file)
        
        saved_samples = m.loadData()
        assert type(saved_samples) is list
        assert saved_samples[0] == sample

    # TODO
    def test_upload_data(self):
        m = Mission(pi=False)
        location_rfid = m.rfid_hash.keys()[0]
        sample = m.takeSample(location_rfid)
        m.uploadSample(sample) #, team='earth')
        

if __name__ == '__main__':
    unittest.main()

