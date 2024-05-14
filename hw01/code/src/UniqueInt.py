class UniqueInt:
    @staticmethod
    def processFile(input_file_path, output_file_path):
        """
        Reads an input file, finds the unique integers, and writes the results to an output file.
        
        Args:
            input_file_path (str): The path to the input file.
            output_file_path (str): The path to the output file.
        """
        unique_integers = UniqueInt.findUniqueIntegers(input_file_path)
        UniqueInt.writeUniqueIntegers(output_file_path, unique_integers)

    @staticmethod
    def findUniqueIntegers(input_file_path):
        """
        Reads the input file and finds the unique integers.
        
        Args:
            input_file_path (str): The path to the input file.
        
        Returns:
            list: A list of unique integers.
        """
        unique_integers = []
        current_size = 0
        with open(input_file_path, 'r') as input_file:
            while True:
                integer = UniqueInt.readNextItemFromFile(input_file)
                if integer is None:
                    break
                if not UniqueInt.contains(unique_integers, current_size, integer):
                    unique_integers = UniqueInt.insert(unique_integers, current_size, integer)
                    current_size += 1
        return UniqueInt.sortIntegers(unique_integers)

    @staticmethod
    def contains(lst, size, item):
        """
        Checks if an item is present in a list.
        
        Args:
            lst (list): The list to search.
            size (int): The number of elements in the list.
            item: The item to search for.
        
        Returns:
            bool: True if the item is in the list, False otherwise.
        """
        for i in range(size):
            if lst[i] == item:
                return True
        return False

    @staticmethod
    def insert(lst, index, item):
        """
        Inserts an item into a list at the specified index.
        
        Args:
            lst (list): The list to insert the item into.
            index (int): The index at which to insert the item.
            item: The item to insert.
        
        Returns:
            list: The updated list with the item inserted.
        """
        new_list = [None] * (len(lst) + 1)
        for i in range(index):
            new_list[i] = lst[i]
        new_list[index] = item
        for i in range(index, len(lst)):
            new_list[i + 1] = lst[i]
        return new_list

    @staticmethod
    def sortIntegers(integers):
        """
        Sorts a list of integers in increasing order.
        
        Args:
            integers (list): A list of integers.
        
        Returns:
            list: The sorted list of integers.
        """
        n = len(integers)
        for i in range(n):
            for j in range(0, n - i - 1):
                if integers[j] > integers[j + 1]:
                    integers[j], integers[j + 1] = integers[j + 1], integers[j]
        return integers

    @staticmethod
    def writeUniqueIntegers(output_file_path, unique_integers):
        """
        Writes the unique integers to the output file.
        
        Args:
            output_file_path (str): The path to the output file.
            unique_integers (list): A list of unique integers.
        """
        with open(output_file_path, 'w') as output_file:
            for integer in unique_integers:
                output_file.write(str(integer) + '\n')

    @staticmethod
    def readNextItemFromFile(input_file_stream):
        """
        Reads the next integer from the input file stream.
        
        Args:
            input_file_stream (file): The input file stream.
        
        Returns:
            int or None: The next integer from the file, or None if the end of the file is reached.
        """
        try:
            line = input_file_stream.readline().strip()
            if line:
                return int(line)
        except ValueError:
            # Skip lines with non-integer values
            pass
        return None

# Example usage
UniqueInt.processFile('hw01/sample_inputs/sample_01.txt', 'hw01/sample_results/sample_input_01.txt_results.txt')
