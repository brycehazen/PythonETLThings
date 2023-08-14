## Creating a Standalone Executable

To make the application user-friendly and easily distributable, you can convert the Python script into a standalone .exe file using PyInstaller.

### Step-by-step Guide:

#### 1. **Install PyInstaller:**

First, install PyInstaller using pip:

    pip install pyinstaller

#### 2. **Run PyInstaller:**

Navigate to the directory containing your script (`file_processor_gui.py`) in your terminal or command prompt, then execute the following command:

    pyinstaller --onefile --windowed file_processor_gui.py

**Explanation of Parameters**:

- `--onefile`: This parameter ensures the creation of a single bundled executable.
   
- `--windowed`: This parameter prevents a terminal window from appearing when the application is run, which is particularly useful for GUI applications.

#### 3. **Locate the Executable:**

Post execution, PyInstaller will generate multiple directories. Your .exe file can be found inside the `dist` directory.

#### 4. **Distribute Your Application:**

You're now ready to distribute the generated .exe file to users. They won't need Python installed to run it.
### Notes:

- Ensure all required assets and dependencies are available or properly referenced. For example, if `RETestCases_original_v8.py` imports other libraries or files, they should be available in the directory or be included in the Python environment when running PyInstaller.

- The first time you run PyInstaller, it might take a bit longer as it collects all required files. Subsequent runs will be faster.

- The resulting .exe can be large because it bundles Python and all necessary libraries.

- If you have data files or other assets your program needs to access, you might need to adjust the way your program accesses them when it's an .exe. PyInstaller has ways to bundle these additional data files if needed.
