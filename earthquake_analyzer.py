# Earthquake Data Analyzer
#
# This module provides functionality to analyze earthquake data
# from the CSV file containing magnitude, length, and duration data.

import csv
from typing import List, Dict, Tuple
from collections import defaultdict


class EarthquakeAnalyzer:
    """Analyzer for earthquake data."""
    
    def __init__(self, csv_file_path: str):
        """Initialize analyzer with CSV file path."""
        self.csv_file_path = csv_file_path
        self.data = []
        self._load_data()
    
    def _load_data(self) -> None:
        """Load earthquake data from CSV file."""
        try:
            with open(self.csv_file_path, 'r', encoding='utf-8-sig') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    # Convert string values to appropriate types
                    processed_row = {}
                    for key, value in row.items():
                        key = key.strip()
                        value = value.strip()
                        if key in ['magnitude', 'length', 'duration']:
                            try:
                                processed_row[key] = float(value) if '.' in value else int(value)
                            except ValueError:
                                processed_row[key] = value
                        else:
                            processed_row[key] = value
                    self.data.append(processed_row)
        except FileNotFoundError:
            raise FileNotFoundError(f"CSV file not found: {self.csv_file_path}")
        except Exception as e:
            raise Exception(f"Error loading data: {str(e)}")
    
    def get_magnitude_stats(self) -> Dict[str, float]:
        """Calculate statistics for earthquake magnitudes."""
        magnitudes = [row['magnitude'] for row in self.data if isinstance(row.get('magnitude'), (int, float))]
        if not magnitudes:
            return {'count': 0, 'min': 0, 'max': 0, 'avg': 0}
        
        return {
            'count': len(magnitudes),
            'min': min(magnitudes),
            'max': max(magnitudes),
            'avg': sum(magnitudes) / len(magnitudes)
        }
    
    def get_correlation_length_duration(self) -> float:
        """Calculate correlation between earthquake length and duration."""
        lengths = [row['length'] for row in self.data if isinstance(row.get('length'), (int, float))]
        durations = [row['duration'] for row in self.data if isinstance(row.get('duration'), (int, float))]
        
        if len(lengths) != len(durations) or len(lengths) == 0:
            return 0.0
        
        # Simple correlation calculation
        n = len(lengths)
        if n <= 1:
            return 0.0
            
        mean_length = sum(lengths) / n
        mean_duration = sum(durations) / n
        
        numerator = sum((lengths[i] - mean_length) * (durations[i] - mean_duration) for i in range(n))
        denominator_length = sum((lengths[i] - mean_length) ** 2 for i in range(n))
        denominator_duration = sum((durations[i] - mean_duration) ** 2 for i in range(n))
        
        if denominator_length == 0 or denominator_duration == 0:
            return 0.0
            
        return numerator / ((denominator_length * denominator_duration) ** 0.5)
    
    def get_magnitude_distribution(self) -> Dict[float, int]:
        """Get distribution of earthquake magnitudes."""
        magnitude_counts = defaultdict(int)
        for row in self.data:
            mag = row.get('magnitude')
            if isinstance(mag, (int, float)):
                magnitude_counts[mag] += 1
        return dict(magnitude_counts)
    
    def filter_by_magnitude_range(self, min_mag: float, max_mag: float) -> List[Dict]:
        """Filter earthquakes by magnitude range."""
        return [row for row in self.data 
                if isinstance(row.get('magnitude'), (int, float)) 
                and min_mag <= row['magnitude'] <= max_mag]


def main():
    """Main function for demonstration."""
    try:
        analyzer = EarthquakeAnalyzer('quake.csv')
        
        print("Earthquake Data Analysis")
        print("=====================")
        
        # Magnitude statistics
        stats = analyzer.get_magnitude_stats()
        print(f"Magnitude Statistics:")
        print(f"  Count: {stats['count']}")
        print(f"  Min: {stats['min']}")
        print(f"  Max: {stats['max']}")
        print(f"  Average: {stats['avg']:.2f}")
        
        # Correlation
        correlation = analyzer.get_correlation_length_duration()
        print(f"\nCorrelation between Length and Duration: {correlation:.4f}")
        
        # Distribution
        distribution = analyzer.get_magnitude_distribution()
        print(f"\nMagnitude Distribution:")
        for mag, count in sorted(distribution.items()):
            print(f"  Magnitude {mag}: {count} earthquakes")
        
        # Filter example
        strong_quakes = analyzer.filter_by_magnitude_range(7.0, 10.0)
        print(f"\nStrong earthquakes (magnitude 7.0+): {len(strong_quakes)} events")
        
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
