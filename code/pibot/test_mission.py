import unittest
import os

from mission import Mission
import mission

os.environ["NO_PI_TEST"] = 'False'

class TestMission(unittest.TestCase):

    def test_getLocation(self):
        m = Mission()
        assert m.getLocation() is None

    def test_rfids(self):
        m = Mission()
        assert len(m.rfid_hash.keys()) == 600

    def test_takeSample(self):
        m = Mission()
        location_rfid = m.rfid_hash.keys()[0]
        sample = m.takeSample(location_rfid)
        assert type(sample) is dict
        for k in ['temperature', 'humidity', 'methane', 'x', 'y']:
            assert sample.has_key(k)

    def test_takeSampleBadLocation(self):
        m = Mission()
        location_rfid = 'xxxx'
        with self.assertRaises(Exception) as e:
            sample = m.takeSample(location_rfid)
        assert 'unknown location' in str(e.exception)

    def test_save_data(self):
        m = Mission()
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

    def test_upload_data(self):
        m = Mission()
        location_rfid = m.rfid_hash.keys()[0]
        sample = m.takeSample(location_rfid)
        new_sample = m.uploadSample(sample, team='AuRoRa')
        for k in ['temperature', 'humidity', 'methane', 'x', 'y']:
            assert new_sample[k] == sample[k]

    def test_upload_bad_team(self):
        m = Mission()
        location_rfid = m.rfid_hash.keys()[0]
        sample = m.takeSample(location_rfid)
        with self.assertRaises(Exception) as e:
            m.uploadSample(sample, team='arth')

        assert 'no team of that name found' in str(e.exception)

    def test_upload_bad_data(self):
        m = Mission()
        location_rfid = m.rfid_hash.keys()[0]
        sample = m.takeSample(location_rfid)
        sample['methane'] = 1000
        with self.assertRaises(Exception) as e:
            m.uploadSample(sample, team='Aurora')

        assert 'must be between' in str(e.exception)

    @unittest.skip("skipping random data")
    def test_upload_random_data(self):
        from random import sample
        m = Mission()
        for rfid in sample(m.rfid_hash,200):
            sample = m.takeSample(rfid)
            m.uploadSample(sample, team='Aurora')

    @unittest.skip("skipping all data")
    def test_upload_all_data(self):
        m = Mission()
        for rfid in m.rfid_hash:
            sample = m.takeSample(rfid)
            m.uploadSample(sample, team='Aurora')

    
    def test_get_all_samples(self):
        m = Mission()
        samples = m.getAllSamples()
        assert type(samples) == list
        assert len(samples) > 0
        assert type(samples[0]) == dict
        assert samples[0].has_key('temperature')

if __name__ == '__main__':
    unittest.main()

