# soft-engg-project-jan-2025-se-Jan-15

## Project Setup (Frontend)

### To start the local server using this source code run the following commands
1. cd frontend
2. npm install (To install the node modules)
3. npm run start

## Project Setup (Backend)

To run this project successfully, you need to install the required dependencies and ensure that Microsoft C++ Build Tools are installed on your system.

### Step 1: Install Required Python Packages

Before proceeding, make sure you have Python installed (preferably Python 3.8 or later).

### Step 2: Install Microsoft C++ Build Tools

For proper execution of the Retrieval-Augmented Generation (RAG) system using ChromaDB, you need to install Microsoft C++ Build Tools.

1. Download the [Microsoft Build Tools for Visual Studio](https://visualstudio.microsoft.com/visual-cpp-build-tools/).
2. Install the required components, including `MSVC v142 - VS 2019 C++ Build Tools` and `Windows 10 SDK`.
3. Restart your system after installation.

### Step 3: Running the Backend

1. Clone the repository:
```commandline
git clone https://github.com/abhijatain/soft-engg-project-jan-2025-se-Jan-15.git
cd soft-engg-project-jan-2025-se-Jan-15
```
2. Set up a virtual environment:
```commandline
python -m venv venv
source venv/bin/activate # On Windows use venv\Scripts\activate
```
3. Install dependencies:
```commandline
pip install -r requirements.txt
```
4. Create dummy data required for the backend:
```commandline
cd backend
python dummy_data.py
```
5.Run the application:
```commandline
uvicorn app.main:app --reload
```
5. Visit `http://localhost:8000/docs` to see the Swagger UI documentation.
