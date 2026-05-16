# Test suite for Earthquake Data Analyzer
#
# This module contains tests for the earthquake_analyzer module.

import unittest
import os
import tempfile
import csv
from earthquake_analyzer import EarthquakeAnalyzer


class TestEarthquakeAnalyzer(unittest.TestCase):
    """Test cases for EarthquakeAnalyzer class."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create a temporary CSV file for testing
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv')
        self.temp_file.write('magnitude,length,duration\n')
        self.temp_file.write('7.8,360,130\n')
        self.temp_file.write('7.7,400,110\n')
        self.temp_file.write('6.5,25,6\n')
        self.temp_file.write('5.8,5,2\n')
        self.temp_file.close()
        
        self.analyzer = EarthquakeAnalyzer(self.temp_file.name)
    
    def tearDown(self):
        """Clean up test fixtures."""
        os.unlink(self.temp_file.name)
    
    def test_load_data(self):
        """Test that data is loaded correctly."""
        self.assertEqual(len(self.analyzer.data), 4)
        self.assertEqual(self.analyzer.data[0]['magnitude'], 7.8)
        self.assertEqual(self.analyzer.data[0]['length'], 360)
        self.assertEqual(self.analyzer.data[0]['duration'], 130)
    
    def test_magnitude_stats(self):
        """Test magnitude statistics calculation."""
        stats = self.analyzer.get_magnitude_stats()
        
        self.assertEqual(stats['count'], 4)
        self.assertEqual(stats['min'], 5.8)
        self.assertEqual(stats['max'], 7.8)
        self.assertAlmostEqual(stats['avg'], 6.95, places=2)
    
    def test_magnitude_stats_empty_data(self):
        """Test magnitude statistics with empty data."""
        # Create empty file
        empty_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv')
        empty_file.write('magnitude,length,duration\n')
        empty_file.close()
        
        try:
            analyzer = EarthquakeAnalyzer(empty_file.name)
            stats = analyzer.get_magnitude_stats()
            self.assertEqual(stats['count'], 0)
            self.assertEqual(stats['min'], 0)
            self.assertEqual(stats['max'], 0)
            self.assertEqual(stats['avg'], 0)
        finally:
            os.unlink(empty_file.name)
    
    def test_correlation_length_duration(self):
        """Test correlation calculation between length and duration."""
        correlation = self.analyzer.get_correlation_length_duration()
        # Correlation should be positive (longer earthquakes tend to last longer)
        self.assertGreater(correlation, 0)
        # Correlation should be between -1 and 1
        self.assertGreaterEqual(correlation, -1)
        self.assertLessEqual(correlation, 1)
    
    def test_correlation_empty_data(self):
        """Test correlation with empty data."""
        empty_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv')
        empty_file.write('magnitude,length,duration\n')
        empty_file.close()
        
        try:
            analyzer = EarthquakeAnalyzer(empty_file.name)
            correlation = analyzer.get_correlation_length_duration()
            self.assertEqual(correlation, 0.0)
        finally:
            os.unlink(empty_file.name)
    
    def test_magnitude_distribution(self):
        """Test magnitude distribution."""
        distribution = self.analyzer.get_magnitude_distribution()
        
        self.assertEqual(distribution[7.8], 1)
        self.assertEqual(distribution[7.7], 1)
        self.assertEqual(distribution[6.5], 1)
        self.assertEqual(distribution[5.8], 1)
    
    def test_filter_by_magnitude_range(self):
        """Test filtering earthquakes by magnitude range."""
        # Filter for strong earthquakes (7.0+)
        strong_quakes = self.analyzer.filter_by_magnitude_range(7.0, 10.0)
        self.assertEqual(len(strong_quakes), 2)
        
        # Filter for moderate earthquakes (6.0-7.0)
        moderate_quakes = self.analyzer.filter_by_magnitude_range(6.0, 7.0)
        self.assertEqual(len(moderate_quakes), 1)
        
        # Filter for small earthquakes (< 6.0)
        small_quakes = self.analyzer.filter_by_magnitude_range(0, 6.0)
        self.assertEqual(len(small_quakes), 1)
    
    def test_filter_by_magnitude_range_no_results(self):
        """Test filtering with range that returns no results."""
        no_quakes = self.analyzer.filter_by_magnitude_range(10.0, 15.0)
        self.assertEqual(len(no_quakes), 0)
    
    def test_file_not_found(self):
        """Test handling of non-existent file."""
        with self.assertRaises(FileNotFoundError):
            EarthquakeAnalyzer('nonexistent_file.csv')
    
    def test_integer_values(self):
        """Test handling of integer values in CSV."""
        temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv')
        temp_file.write('magnitude,length,duration\n')
        temp_file.write('7,100,50\n')
        temp_file.write('6,50,25\n')
        temp_file.close()
        
        try:
            analyzer = EarthquakeAnalyzer(temp_file.name)
            self.assertEqual(len(analyzer.data), 2)
            self.assertEqual(analyzer.data[0]['magnitude'], 7)
            self.assertEqual(analyzer.data[0]['length'], 100)
            self.assertEqual(analyzer.data[0]['duration'], 50)
        finally:
            os.unlink(temp_file.name)


class TestEarthquakeAnalyzerWithRealData(unittest.TestCase):
    """Test cases using the actual quake.csv file."""
    
    @classmethod
    def setUpClass(cls):
        """Set up test fixtures using real data."""
        if os.path.exists('quake.csv'):
            cls.analyzer = EarthquakeAnalyzer('quake.csv')
            cls.has_real_data = True
        else:
            cls.has_real_data = False
    
    def test_real_data_loaded(self):
        """Test that real data is loaded."""
        if not self.has_real_data:
            self.skipTest("Real data file not available")
        
        self.assertGreater(len(self.analyzer.data), 0)
    
    def test_real_data_magnitude_stats(self):
        """Test magnitude statistics on real data."""
        if not self.has_real_data:
            self.skipTest("Real data file not available")
        
        stats = self.analyzer.get_magnitude_stats()
        self.assertGreater(stats['count'], 0)
        self.assertGreater(stats['max'], stats['min'])
        self.assertGreater(stats['avg'], 0)
    
    def test_real_data_correlation(self):
        """Test correlation on real data."""
        if not self.has_real_data:
            self.skipTest("Real data file not available")
        
        correlation = self.analyzer.get_correlation_length_duration()
        self.assertGreaterEqual(correlation, -1)
        self.assertLessEqual(correlation, 1)


if __name__ == '__main__':
    unittest.main()
