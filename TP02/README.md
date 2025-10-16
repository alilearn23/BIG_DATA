# Efficiently Processing and Analyzing Big Data in Python

This project demonstrates and compares three effective methods for handling large datasets (Big Data) that cannot be loaded directly into RAM using Python libraries. The code uses a large dataset as a practical example to show the differences in performance and memory consumption.

## 🎯 The Problem

When trying to read a multi-gigabyte CSV file using the standard `pd.read_csv()` command, we often encounter a `MemoryError` because `pandas` attempts to load the entire file into memory at once. This code reviews practical solutions to this problem.

## 🚀 Methods Used

Three different techniques for processing large files were compared:

### 1. Reading in Chunks with `pandas`
- **Concept**: Instead of reading the entire file, we read it in smaller, fixed-size pieces (chunks), for example, 100,000 rows at a time.
- **Advantages**: Very low memory consumption, as only the current chunk is held in memory.
- **Result in Code**: Processing the file took `~86.53` seconds.

### 2. Using the `Dask` Library
- **Concept**: Dask is a parallel computing library that divides large data into partitions and processes them in parallel. Dask features "Lazy Evaluation," meaning it doesn't execute operations until the final result is requested.
- **Advantages**: Faster than the traditional chunking method thanks to parallel processing, and its API is very similar to `pandas`.
- **Result in Code**: Processing the file took `~58.10` seconds.

### 3. Converting to Parquet Format
- **Concept**: This is a two-step process:
    1.  **Conversion (One-time)**: Read the large CSV file and convert it to the `Parquet` format, which is a columnar storage format optimized for fast reading and analysis.
    2.  **Fast Reading**: Read the resulting Parquet file extremely quickly in subsequent uses.
- **Advantages**: Incredible read speeds after the initial conversion, making it ideal if you plan to analyze the same data repeatedly.
- **Result in Code**:
    - The conversion from CSV to Parquet took about `209.52` seconds.
    - Reading the entire Parquet file took only `41.24` seconds!

## 🔧 How to Run the Code (Explaining the Token Concept)

To run this code successfully, you must set up your Kaggle API credentials to allow the script to download the dataset.

### What is a Kaggle Token?
A Kaggle token is your personal API key, consisting of a **username** and a **secret key**. This token allows external applications (like this script) to securely and programmatically access your Kaggle account and download datasets.

### Setup Steps:
1.  **Get Your Token**:
    * Go to the [Kaggle](https://www.kaggle.com) website.
    * Log in to your account, then go to your `Account` settings page.
    * In the `API` section, click the `Create New Token` button.
    * A file named `kaggle.json` will be downloaded to your computer.

2.  **Use the Token in the Code**:
    * Open the `kaggle.json` file you downloaded with any text editor. Inside, you will find your username and key, like this:
      ```json
      {"username":"YOUR_KAGGLE_USERNAME","key":"YOUR_KAGGLE_KEY"}
      ```
    * In the first cell of the Jupyter Notebook (`big-data.ipynb`), replace the placeholder values:
      ```python
      # Set environment variables using the secrets you added
      os.environ['KAGGLE_USERNAME'] = 'YOUR_KAGGLE_USERNAME' # Replace with your username
      os.environ['KAGGLE_KEY'] = 'YOUR_KAGGLE_KEY' # Replace with your API key
      ```
      - Put your username from the `json` file in place of `'YOUR_KAGGLE_USERNAME'`.
      - Put your key from the `json` file in place of `'YOUR_KAGGLE_KEY'`.

3.  **Install Required Libraries**:
    ```bash
    pip install pandas dask pyarrow kaggle
    ```

4.  **Run the Code**: After setting up the token and installing the libraries, you can run the notebook cells in order.

## 📊 Summary of Results

| Method | Processing/Read Time | Notes |
| :--- | :--- | :--- |
| **Pandas (Chunks)** | ~86.5 seconds | Low memory usage, suitable for one-time processing. |
| **Dask** | ~58.1 seconds | Fast performance and a good balance between speed and ease of use. |
| **Parquet (Read)** | 41.2 seconds | The fastest by far for reading, but requires an initial conversion step. |

**Conclusion**: If you need to analyze large datasets repeatedly, investing the time to convert them to the `Parquet` format is the most efficient long-term solution. For quick, one-off processing, `Dask` offers an excellent alternative.