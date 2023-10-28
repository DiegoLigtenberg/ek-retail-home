class MyIterator:
    def __init__(self, data):
        self.data = data
        self.index = 0

    def __iter__(self):
        return self  # Returning 'self' as the iterator object.

    def __next__(self):
        import time
        time.sleep(1)
        print(self.index, "data deleted")
        
        if self.index >= len(self.data):
            print(self.index)
            raise StopIteration
        value = self.data[self.index]
        self.index += 1
        # print(value)  # Print the value during each iteration
        # print("end")  # Print "end" after each __next__ is fully done
        return value

for i in range(1,5):
    print(i)
asd
# Example usage:
my_data = [1, 2, 3, 4, 5]
my_iterator = MyIterator(my_data)

for item in my_iterator:
    
    import time
    time.sleep(1)
    print('boo')
    # print(item,"woot")
    pass
