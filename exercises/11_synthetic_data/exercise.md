# Synthetic Data Generation with Copilot: Creating Realistic Test Data

## Learning Objective
Learn how to use GitHub Copilot to generate large-scale synthetic data for testing, development, and machine learning applications, understanding different generation strategies and data quality considerations.

## Instructions
1. Create a new Python file called `data_generator.py`
1. Use Copilot to implement various data generation approaches
1. Learn about data distributions and correlations
1. Generate realistic, privacy-safe test data
1. Export data in multiple formats

## Your Task

### Part 1: Basic Data Generation

#### Step 1: Simple Random Generation
Start with a basic implementation:

```python
#!/usr/bin/env python3
"""
Synthetic data generator for creating realistic person records.
Generates 1 million records with demographic information.
"""

import random
import csv
import json
from datetime import datetime, timedelta
from typing import Dict, List, Tuple

# Basic implementation
def generate_simple_person() -> Dict:
    """Generate a single person record with basic random data."""
    first_names = ["John", "Jane", "Michael", "Sarah", "David", "Emily"]
    last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones"]

    return {
        "name": random.choice(first_names),
        "family_name": random.choice(last_names),
        "marital_status": random.choice(["single", "married", "divorced", "widowed"]),
        "age": random.randint(18, 90),
        "number_of_children": random.randint(0, 5)
    }

# Generate 10 sample records
for i in range(10):
    print(generate_simple_person())
```

#### Step 2: Realistic Name Generation
Enhance with more realistic names:

```python
# Ask Copilot: "Create lists of realistic first and last names by gender and ethnicity"

class NameGenerator:
    def __init__(self):
        # Realistic name distributions
        self.male_first_names = [
            "James", "Robert", "John", "Michael", "David", "William", "Richard",
            "Joseph", "Thomas", "Christopher", "Charles", "Daniel", "Matthew"
        ]

        self.female_first_names = [
            "Mary", "Patricia", "Jennifer", "Linda", "Elizabeth", "Barbara",
            "Susan", "Jessica", "Sarah", "Karen", "Lisa", "Nancy", "Betty"
        ]

        self.last_names = [
            "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller",
            "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez"
        ]

        # Add weighted probabilities for more realistic distribution
        self.name_weights = {
            "Smith": 0.7, "Johnson": 0.6, "Williams": 0.5,
            # Let Copilot complete the weights
        }

    def generate_name(self, gender: str = None) -> Tuple[str, str]:
        """Generate a realistic first and last name."""
        # Let Copilot implement realistic name generation
```

### Part 2: Correlated Data Generation

#### Step 1: Age-Dependent Attributes
Create realistic correlations:

```python
class CorrelatedDataGenerator:
    """Generate data with realistic correlations between fields."""

    def generate_marital_status(self, age: int) -> str:
        """Generate marital status based on age with realistic probabilities."""
        if age < 18:
            return "single"
        elif age < 25:
            # 90% single, 10% married
            return random.choices(["single", "married"], weights=[0.9, 0.1])[0]
        elif age < 35:
            # 40% single, 50% married, 10% divorced
            return random.choices(
                ["single", "married", "divorced"],
                weights=[0.4, 0.5, 0.1]
            )[0]
        elif age < 50:
            # Let Copilot implement realistic distributions
            pass
        else:
            # Consider widowed status for older ages
            pass

    def generate_children_count(self, age: int, marital_status: str) -> int:
        """Generate number of children based on age and marital status."""
        if age < 20 or marital_status == "single":
            # Lower probability of children
            return random.choices([0, 1], weights=[0.9, 0.1])[0]
        elif marital_status == "married":
            if age < 30:
                # Young married couples
                return random.choices([0, 1, 2], weights=[0.3, 0.4, 0.3])[0]
            elif age < 40:
                # Peak childbearing years
                return random.choices([0, 1, 2, 3, 4], weights=[0.1, 0.2, 0.4, 0.2, 0.1])[0]
            else:
                # Let Copilot complete the logic
                pass
        # Continue with other cases
```

#### Step 2: Geographic and Cultural Correlations

```python
class GeographicDataGenerator:
    """Generate location-aware demographic data."""

    def __init__(self):
        # Regional name distributions
        self.regions = {
            "northeast": {
                "common_surnames": ["Sullivan", "Murphy", "O'Brien"],
                "cities": ["Boston", "New York", "Philadelphia"]
            },
            "south": {
                "common_surnames": ["Johnson", "Williams", "Jackson"],
                "cities": ["Atlanta", "Houston", "Miami"]
            },
            # Let Copilot add more regions
        }

    def generate_location_aware_person(self) -> Dict:
        """Generate person with location-appropriate attributes."""
        # Select region
        region = random.choice(list(self.regions.keys()))

        # Generate attributes based on region
        # Let Copilot implement location-aware generation
```

### Part 3: Advanced Data Generation Techniques

#### Using Faker Library

```python
from faker import Faker
from faker.providers import person, address, job, date_time

fake = Faker()

class AdvancedPersonGenerator:
    """Use Faker for more sophisticated data generation."""

    def __init__(self, locale='en_US'):
        self.fake = Faker(locale)
        # Add custom providers if needed

    def generate_person(self) -> Dict:
        """Generate a complete person record with Faker."""
        # Generate correlated age and dates
        birth_date = self.fake.date_of_birth(minimum_age=18, maximum_age=90)
        age = (datetime.now().date() - birth_date).days // 365

        # Marriage date should be after 18th birthday
        marriage_age = random.randint(18, min(age, 50))
        marriage_date = birth_date + timedelta(days=marriage_age*365)

        person = {
            "id": self.fake.uuid4(),
            "name": self.fake.first_name(),
            "family_name": self.fake.last_name(),
            "full_name": self.fake.name(),
            "age": age,
            "birth_date": birth_date.isoformat(),
            "email": self.fake.email(),
            "phone": self.fake.phone_number(),
            "address": self.fake.address(),
            "marital_status": self.generate_marital_status(age),
            "marriage_date": marriage_date.isoformat() if random.random() > 0.5 else None,
            "occupation": self.fake.job(),
            "income": self.generate_income(age),
            "number_of_children": self.generate_children(age),
            # Let Copilot add more fields
        }
        return person

    def generate_income(self, age: int) -> int:
        """Generate realistic income based on age."""
        # Income tends to increase with age until retirement
        if age < 25:
            base_income = 30000
            variance = 15000
        elif age < 40:
            base_income = 50000
            variance = 30000
        elif age < 55:
            base_income = 70000
            variance = 40000
        else:
            base_income = 60000
            variance = 35000

        return max(0, int(random.gauss(base_income, variance)))
```

### Part 4: Performance Optimization

#### Batch Generation with Multiprocessing

```python
import multiprocessing as mp
from typing import List
import numpy as np

class BulkDataGenerator:
    """Efficiently generate large amounts of data."""

    def __init__(self, num_workers: int = None):
        self.num_workers = num_workers or mp.cpu_count()

    def generate_batch(self, batch_size: int) -> List[Dict]:
        """Generate a batch of records."""
        return [self.generate_person() for _ in range(batch_size)]

    def generate_parallel(self, total_records: int) -> List[Dict]:
        """Generate records in parallel using multiprocessing."""
        batch_size = total_records // self.num_workers

        with mp.Pool(self.num_workers) as pool:
            results = pool.map(self.generate_batch,
                             [batch_size] * self.num_workers)

        # Flatten results
        return [record for batch in results for record in batch]

    def generate_with_numpy(self, count: int) -> np.ndarray:
        """Use NumPy for efficient numerical data generation."""
        # Generate ages using normal distribution
        ages = np.random.normal(40, 15, count)
        ages = np.clip(ages, 18, 90).astype(int)

        # Generate correlated data
        # Let Copilot implement NumPy-based generation
```

### Part 5: Data Quality and Validation

#### Data Validation and Statistics

```python
class DataQualityChecker:
    """Validate and analyze generated data."""

    def __init__(self, data: List[Dict]):
        self.data = data

    def validate_constraints(self) -> Dict:
        """Check if data meets all constraints."""
        issues = []

        for record in self.data:
            # Age constraints
            if record['age'] < 18 or record['age'] > 90:
                issues.append(f"Invalid age: {record['age']}")

            # Logical constraints
            if record['marital_status'] == 'single' and record['number_of_children'] > 2:
                issues.append("Unlikely: single with many children")

            # Let Copilot add more validation rules

        return {
            "total_records": len(self.data),
            "issues_found": len(issues),
            "issue_samples": issues[:10]
        }

    def generate_statistics(self) -> Dict:
        """Generate statistical summary of the data."""
        import pandas as pd

        df = pd.DataFrame(self.data)

        stats = {
            "age": {
                "mean": df['age'].mean(),
                "median": df['age'].median(),
                "std": df['age'].std()
            },
            "marital_status": df['marital_status'].value_counts().to_dict(),
            "children": {
                "mean": df['number_of_children'].mean(),
                "max": df['number_of_children'].max(),
                "distribution": df['number_of_children'].value_counts().to_dict()
            }
            # Let Copilot add more statistics
        }

        return stats
```

### Part 6: Export Functionality

#### Multiple Export Formats

```python
class DataExporter:
    """Export generated data in various formats."""

    def __init__(self, data: List[Dict]):
        self.data = data

    def export_csv(self, filename: str):
        """Export data to CSV file."""
        if not self.data:
            return

        keys = self.data[0].keys()
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=keys)
            writer.writeheader()
            writer.writerows(self.data)

    def export_json(self, filename: str, pretty: bool = False):
        """Export data to JSON file."""
        with open(filename, 'w') as jsonfile:
            if pretty:
                json.dump(self.data, jsonfile, indent=2)
            else:
                json.dump(self.data, jsonfile)

    def export_parquet(self, filename: str):
        """Export data to Parquet format for big data applications."""
        import pandas as pd
        import pyarrow.parquet as pq

        df = pd.DataFrame(self.data)
        df.to_parquet(filename, compression='snappy')

    def export_sql(self, filename: str, table_name: str = 'persons'):
        """Generate SQL INSERT statements."""
        # Let Copilot implement SQL export
        pass
```

### Part 7: Complete Implementation

#### Main Generator Class

```python
class SyntheticDataGenerator:
    """Complete synthetic data generation system."""

    def __init__(self, use_faker: bool = True, locale: str = 'en_US'):
        self.use_faker = use_faker
        if use_faker:
            self.faker = Faker(locale)
        self.generated_data = []

    def generate_million_records(self) -> List[Dict]:
        """Generate 1 million person records efficiently."""
        print("Generating 1,000,000 records...")

        # Use batch processing for memory efficiency
        batch_size = 10000
        total_batches = 100

        for batch_num in range(total_batches):
            batch = []
            for _ in range(batch_size):
                batch.append(self.generate_realistic_person())

            self.generated_data.extend(batch)

            # Progress indicator
            if (batch_num + 1) % 10 == 0:
                print(f"Progress: {(batch_num + 1) * batch_size:,} records generated")

        print("Generation complete!")
        return self.generated_data

    def generate_realistic_person(self) -> Dict:
        """Generate a single realistic person record."""
        # Implement the complete generation logic
        # Let Copilot help combine all the techniques
        pass
```

## What You'll Learn
- Data generation strategies and techniques
- Statistical distributions and correlations
- Performance optimization for large-scale generation
- Data validation and quality assurance
- Multiple export format handling
- Privacy-safe synthetic data creation
- Realistic data modeling

## Success Criteria
- [ ] Generated 1 million records successfully
- [ ] Data has realistic correlations (age/marriage/children)
- [ ] Names are diverse and realistic
- [ ] Performance is acceptable (< 5 minutes for 1M records)
- [ ] Data passes validation checks
- [ ] Multiple export formats work correctly
- [ ] Statistics show realistic distributions

## Advanced Challenges

### Challenge 1: Time Series Data
Generate people with life events over time:

```python
class LifeEventGenerator:
    """Generate time series of life events."""

    def generate_life_timeline(self, person: Dict) -> List[Dict]:
        """Create a timeline of major life events."""
        events = []
        birth_year = datetime.now().year - person['age']

        # Education events
        events.append({
            "year": birth_year + 18,
            "event": "high_school_graduation",
            "description": "Graduated from high school"
        })

        # Let Copilot add more life events
        # Marriage, children, job changes, etc.
```

### Challenge 2: Relationship Networks
Create interconnected family structures:

```python
class FamilyNetworkGenerator:
    """Generate connected family relationships."""

    def generate_family(self, size: int) -> List[Dict]:
        """Generate a connected family tree."""
        # Create parents, children, siblings
        # Ensure consistent ages and relationships
        # Let Copilot implement family generation
```

### Challenge 3: Geographic Distribution
Generate population with realistic geographic distribution:

```python
class GeographicPopulationGenerator:
    """Generate population with realistic geographic distribution."""

    def __init__(self):
        # Population density by region
        self.population_centers = {
            "New York": {"lat": 40.7128, "lon": -74.0060, "population": 8000000},
            "Los Angeles": {"lat": 34.0522, "lon": -118.2437, "population": 4000000},
            # Let Copilot add more cities
        }

    def generate_with_location(self) -> Dict:
        """Generate person with realistic location."""
        # Use population density for realistic distribution
        # Let Copilot implement location-based generation
```

### Challenge 4: Industry-Specific Data
Generate domain-specific synthetic data:

```python
# Healthcare data
class PatientDataGenerator:
    """Generate synthetic healthcare records."""

    def generate_patient(self) -> Dict:
        # Medical history, conditions, medications
        # HIPAA-compliant synthetic data
        pass

# Financial data
class FinancialDataGenerator:
    """Generate synthetic financial records."""

    def generate_transaction(self) -> Dict:
        # Account numbers, transactions, balances
        # PCI-compliant synthetic data
        pass
```

## Performance Benchmarks

Test your implementation:

```python
import time

def benchmark_generation():
    """Benchmark different generation methods."""

    # Method 1: Simple random
    start = time.time()
    simple_data = [generate_simple_person() for _ in range(10000)]
    print(f"Simple: {time.time() - start:.2f}s for 10,000 records")

    # Method 2: Faker
    start = time.time()
    faker_data = [faker_generator.generate() for _ in range(10000)]
    print(f"Faker: {time.time() - start:.2f}s for 10,000 records")

    # Method 3: NumPy batch
    start = time.time()
    numpy_data = numpy_generator.generate_batch(10000)
    print(f"NumPy: {time.time() - start:.2f}s for 10,000 records")
```

## Data Analysis Tasks

After generation, analyze your data:

```python
import matplotlib.pyplot as plt
import seaborn as sns

def analyze_generated_data(data: List[Dict]):
    """Analyze and visualize generated data."""

    df = pd.DataFrame(data)

    # Age distribution
    plt.figure(figsize=(12, 4))

    plt.subplot(1, 3, 1)
    plt.hist(df['age'], bins=30)
    plt.title('Age Distribution')

    plt.subplot(1, 3, 2)
    df['marital_status'].value_counts().plot(kind='bar')
    plt.title('Marital Status Distribution')

    plt.subplot(1, 3, 3)
    plt.scatter(df['age'], df['number_of_children'], alpha=0.1)
    plt.title('Age vs Number of Children')

    plt.tight_layout()
    plt.show()
```

## Reflection Questions
1. How did you ensure data realism?
1. What correlations were most important?
1. How did you optimize for performance?
1. What validation rules did you implement?
1. How would you generate even more complex relationships?

## Real-World Applications
- Testing database applications
- Machine learning training data
- Load testing systems
- Privacy-preserving analytics
- Demonstration and training environments
- Statistical analysis and research

## Expected Learning Outcomes
By completing this exercise, you should understand:
- Synthetic data generation principles
- Statistical distributions and correlations
- Performance optimization techniques
- Data validation and quality metrics
- Privacy and compliance considerations
- Real-world data modeling
