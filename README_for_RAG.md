# README

## Installation Instructions

To run this project successfully, you need to install the required dependencies and ensure that Microsoft C++ Build Tools are installed on your system.

### Step 1: Install Required Python Packages

Before proceeding, make sure you have Python installed (preferably Python 3.8 or later). 

Run the following command to install all necessary dependencies:

```sh
pip install -r requirements.txt
```

Alternatively, if you do not have a `requirements.txt` file, manually install the required packages by running:

```sh
pip install -r dependency.txt
```

### Step 2: Install Microsoft C++ Build Tools

For proper execution of the Retrieval-Augmented Generation (RAG) system using ChromaDB, you need to install Microsoft C++ Build Tools.

1. Download the [Microsoft Build Tools for Visual Studio](https://visualstudio.microsoft.com/visual-cpp-build-tools/).
2. Install the required components, including `MSVC v142 - VS 2019 C++ Build Tools` and `Windows 10 SDK`.
3. Restart your system after installation.

### Step 3: Running the RAG System

After installing the dependencies and Microsoft C++ Build Tools, execute the program using:

```sh
python run_rag.py
```

Alternatively, if an executable (`.exe` file) is provided, run it directly:

```sh
./run_rag.exe
```

### Notes
- Ensure all dependencies are installed properly before running the code.
- If facing issues with `pip install`, consider creating a virtual environment:
  ```sh
  python -m venv venv
  source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
  pip install -r requirements.txt
  ```
- Update `pip` and `setuptools` before installing dependencies:
  ```sh
  pip install --upgrade pip setuptools
  ```
