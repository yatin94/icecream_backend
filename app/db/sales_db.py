from pathlib import Path
import pickle

class SalesPickle:
    def __init__(self):
        self.db_path = Path('db/sales_db.pkl')
        self.existing_data = []
        if not self.db_path.exists():
            with open(self.db_path, 'wb') as f1:
                self.existing_data = []
        else:
            with open(self.db_path, 'rb') as f1:
                self.existing_data = pickle.load(f1)
    
    def write(self, data):
        self.existing_data.append(data)
        with open(self.db_path, 'wb') as f1:
                pickle.dump(self.existing_data, f1)
    
    def next_billing(self):
         return len(self.existing_data) + 1
