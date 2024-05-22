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

    def __init__(self, matrix_file_path=None, rows=None, cols=None):
        """
        Initializes a SparseMatrix object. If matrix_file_path is provided, it reads the matrix from the file.
        If rows and cols are provided, it initializes an empty matrix with given dimensions.

        Args:
            matrix_file_path (str): The file path of the input matrix (optional).
            rows (int): The number of rows in the matrix (optional).
            cols (int): The number of columns in the matrix (optional).

        Raises:
            ValueError: If the input file has an incorrect format.
        """
        if matrix_file_path:
            self.rows, self.cols, self.matrix = self.read_matrix_from_file(matrix_file_path)
        elif rows is not None and cols is not None:
            self.rows = rows
            self.cols = cols
            self.matrix = {}
        else:
            raise ValueError("Either matrix_file_path or both rows and cols must be provided")

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
        if value != 0:
            self.matrix[(row, col)] = value
        elif (row, col) in self.matrix:
            del self.matrix[(row, col)]

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

        result = SparseMatrix(rows=self.rows, cols=self.cols)
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

        result = SparseMatrix(rows=self.rows, cols=self.cols)
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
            raise ValueError("The number of columns in the first matrix must be equal to "
                             "the number of rows in the second matrix for multiplication")

        result = SparseMatrix(rows=self.rows, cols=other.cols)
        for i in range(self.rows):
            for j in range(other.cols):
                value = sum(self.get_element(i, k) * other.get_element(k, j) for k in range(self.cols))
                if value != 0:
                    result.set_element(i, j, value)
        return result

    def write_matrix_to_file(self, file_path):
        """
        Writes the sparse matrix to a file in the specified format.

        Args:
            file_path (str): The file path where the matrix will be written.
        """
        with open(file_path, 'w') as file:
            file.write(f"rows={self.rows}\n")
            file.write(f"cols={self.cols}\n")
            for (row, col), value in sorted(self.matrix.items()):
                file.write(f"({row}, {col}, {value})\n")


if __name__ == "__main__":
    """
    The main function that allows the user to select an operation and performs it
    on the input sparse matrices.
    """
    matrix1 = SparseMatrix("sparse_matrix/sample_inputs/easy_sample_01_1.txt")
    matrix2 = SparseMatrix("sparse_matrix/sample_inputs/easy_sample_01_2.txt")

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

    result_file_path = "sparse_matrix/sample_results/result.txt"
    result.write_matrix_to_file(result_file_path)
    print(f"Result written to {result_file_path}")
