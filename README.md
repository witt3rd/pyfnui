# Python Function Server Streamlit App

## Overview

This Streamlit application provides a convenient user interface for managing and interacting with a Python function server. Users can create, update, delete, and execute Python functions. The app also enables the management of function dependencies and arguments.

## Features

- **List Functions**: View a summary list of all the functions available on the server, including their names and descriptions.
- **Create Functions**: Add new Python functions by providing the function's name, code, description, package dependencies, function dependencies, and arguments.
- **Edit Functions**: Update existing functions with new code, dependencies, or argument details.
- **Delete Functions**: Remove a function from the server.
- **Execute Functions**: Run functions directly from the Streamlit app and view the output.
- **Manage Arguments**: Define and update arguments including their data types and descriptions.

## Installation

To install and run the Streamlit app locally, follow these steps:

1. Clone the repository:

   ```
   git clone <repo_url>
   cd <repo_path>
   ```

2. (Optional) Create a virtual environment and activate it:

   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the required packages:

   ```
   pip install -r requirements.txt
   ```

4. Set the server URL in the `.env` file. The `.env.example` file can be used as a template. Create a `.env` file if necessary and update the `SERVER_URL` value:

   ```
   SERVER_URL="http://localhost:8000"
   ```

5. Start the Streamlit app:
   ```
   streamlit run app.py
   ```

## Usage Instructions

Upon launching the app, you'll be presented with the following pages:

### Home Page

- You can browse through the list of Python functions available on the server.
- Select a function to view its details, edit or delete it, or execute it.

### Create/Edit Function Page

- Here, you can fill in the form to create a new function or update an existing one.
- Provide all the necessary details like function name, description, code, package dependencies, etc.

### Execute Function Page

- For the selected function, input the required arguments and press "Execute" to run the function.
- View the function's results directly on the app.

## Configuration

The app requires a `SERVER_URL` environment variable to communicate with the Python function server. Make sure this is correctly set in the `.env` file before running the app.

## Contributing

Contributions to improve this Streamlit app are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the terms of the MIT license. See the [LICENSE](LICENSE) file for details.

_Please note that the app provided is a template and might need configuring with actual server endpoints and other adjustments specific to your function server implementation._
