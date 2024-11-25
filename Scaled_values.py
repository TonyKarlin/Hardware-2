from filefifo import Filefifo

class Samples:
    def __init__(self, initial, scaling):
        self.data = Filefifo(10, name = 'capture_250Hz_01.txt')
        self.sample_rate = 250
        self.initial_duration = initial * self.sample_rate
        self.scaling_duration = scaling * self.sample_rate
        self.min_value = float("inf")
        self.max_value = float("-inf")
        
    
    def calc_min_max(self):
        for _ in range(self.initial_duration):
            value = self.data.get()
            if value > self.max_value:
                self.max_value = value
            elif value < self.min_value:
                self.min_value = value
                
                
    def scaling(self):
        for _ in range(self.scaling_duration):
            scaled_value = self.data.get()
            scaled_number = (scaled_value - self.min_value) / (self.max_value - self.min_value) * 100
            print(f"Scaled value: {scaled_number:.2f}")
        print(f"Min value: {self.min_value}\nMax value: {self.max_value}")            
            
            
exec = Samples(2, 10)

def main():
    exec.calc_min_max()
    exec.scaling()
        
        
if __name__ == "__main__":
    main()
        
        
    
        
        
        
    
            

        
        

