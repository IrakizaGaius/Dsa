# dsa/sparse_matrix/code/src/sparse_matrix.py
"""
This module provides an implementation of a Sparse Matrix data structure
and operations such as addition, subtraction, and multiplication.
"""

class SparseMatrix:
    """
    Represents a sparse matrix, stored efficiently using a dictionary.

    Attributes:
        rows (int): The number of rows in the matrix.
        cols (int): The number of columns in the matrix.
        matrix (dict): A dictionary storing the non-zero elements of the matrix,
            where the keys are tuples of (row, column) and the values are the
            corresponding element values.
    """

    def __init__(self, matrix_file_path):
        """
        Initializes a SparseMatrix object by reading the matrix from a file.

        Args:
            matrix_file_path (str): The file path of the input matrix.

        Raises:
            ValueError: If the input file has an incorrect format.
        """
        self.rows, self.cols, self.matrix = self.read_matrix_from_file(matrix_file_path)

    def read_matrix_from_file(self, file_path):
        """
        Reads a sparse matrix from an input file and stores it in a dictionary.

        The input file format is as follows:
        rows=<number of rows>
        cols=<number of columns>
        (row, column, value)
        (row, column, value)
        ...

        Args:
            file_path (str): The file path of the input matrix.

        Returns:
            tuple: A tuple containing the number of rows, the number of columns,
                and a dictionary representing the sparse matrix.

        Raises:
            ValueError: If the input file has an incorrect format.
        """
        try:
            with open(file_path, 'r') as file:
                rows = int(file.readline().strip().split('=')[1])
                cols = int(file.readline().strip().split('=')[1])
                matrix = {}
                for line in file:
                    line = line.strip()
                    if line:
                        row, col, value = map(int, line.strip('()').split(', '))
                        matrix[(row, col)] = value
                return rows, cols, matrix
        except (IndexError, ValueError):
            raise ValueError("Input file has wrong format")

    def get_element(self, row, col):
        """
        Retrieves the value of an element in the sparse matrix.

        Args:
            row (int): The row index of the element.
            col (int): The column index of the element.

        Returns:
            int: The value of the element at the specified row and column.
                If the element is not present in the matrix, 0 is returned.
        """
        return self.matrix.get((row, col), 0)

    def set_element(self, row, col, value):
        """
        Sets the value of an element in the sparse matrix.

        Args:
            row (int): The row index of the element.
            col (int): The column index of the element.
            value (int): The new value to be set for the element.
        """
        self.matrix[(row, col)] = value

    def add(self, other):
        """
        Performs addition of two sparse matrices.

        Args:
            other (SparseMatrix): The other sparse matrix to be added.

        Returns:
            SparseMatrix: A new sparse matrix representing the sum of the two input matrices.

        Raises:
            ValueError: If the input matrices have different dimensions.
        """
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Matrices must have the same dimensions for addition")

        result = SparseMatrix(f"Dsa/sparse_matrix/sample_inputs/sample_results/result.txt")
        for (row, col), value in self.matrix.items():
            result.set_element(row, col, value)
        for (row, col), value in other.matrix.items():
            result.set_element(row, col, result.get_element(row, col) + value)
        return result

    def subtract(self, other):
        """
        Performs subtraction of two sparse matrices.

        Args:
            other (SparseMatrix): The other sparse matrix to be subtracted.

        Returns:
            SparseMatrix: A new sparse matrix representing the difference of the two input matrices.

        Raises:
            ValueError: If the input matrices have different dimensions.
        """
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Matrices must have the same dimensions for subtraction")

        result = SparseMatrix(f"Dsa/sparse_matrix/sample_inputs/sample_results/result.txt")
        for (row, col), value in self.matrix.items():
            result.set_element(row, col, value)
        for (row, col), value in other.matrix.items():
            result.set_element(row, col, result.get_element(row, col) - value)
        return result

    def multiply(self, other):
        """
        Performs multiplication of two sparse matrices.

        Args:
            other (SparseMatrix): The other sparse matrix to be multiplied.

        Returns:
            SparseMatrix: A new sparse matrix representing the product of the two input matrices.

        Raises:
            ValueError: If the number of columns in the first matrix is not equal to the
                number of rows in the second matrix.
        """
        if self.cols != other.rows:
            raise ValueError("The number of columns in the first matrix must be equal to the number of rows in the second matrix for multiplication")

        result = SparseMatrix(f"Dsa/sparse_matrix/sample_inputs/sample_results/result.txt")
        for i in range(self.rows):
            for j in range(other.cols):
                value = sum(self.get_element(i, k) * other.get_element(k, j) for k in range(self.cols))
                result.set_element(i, j, value)
        return result

if __name__ == "__main__":
    """
    The main function that allows the user to select an operation and performs it
    on the input sparse matrices.
    """
    matrix1 = SparseMatrix("Dsa/sparse_matrix/sample_inputs/easy_sample_01_1.txt")
    matrix2 = SparseMatrix("Dsa/sparse_matrix/sample_inputs/easy_sample_01_2.txt")

    print("Select an operation:")
    print("1. Addition")
    print("2. Subtraction")
    print("3. Multiplication")
    choice = int(input("Enter your choice (1-3): "))

    if choice == 1:
        result = matrix1.add(matrix2)
    elif choice == 2:
        result = matrix1.subtract(matrix2)
    elif choice == 3:
        result = matrix1.multiply(matrix2)
    else:
        print("Invalid choice!")
        exit()

    print("Result:")
    for row in range(result.rows):
        for col in range(result.cols):
            print(f"({row}, {col}, {result.get_element(row, col)})")
