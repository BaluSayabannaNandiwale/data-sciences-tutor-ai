# data-sciences-tutor-ai
# AI Data Science Tutor

This project is an AI-powered Data Science Tutor that helps users learn and understand various data science concepts through a conversational interface. The application integrates multiple tools and visualizations to provide an interactive learning experience.

## Features

- **Conversational AI**: Powered by Google Generative AI, the tutor answers data science questions in real-time.
- **Python Code Execution**: Write, run, and get explanations for Python code snippets.
- **Data Visualizations**: Visualize data science concepts like decision trees, neural networks, and K-means clustering.
- **Comparisons**: Compare different machine learning models and algorithms.
- **Dark Mode**: Toggle between dark and light mode for a comfortable viewing experience.

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/YOUR_GITHUB_USERNAME/YOUR_REPOSITORY_NAME.git
   cd YOUR_REPOSITORY_NAME
   ```

2. **Set up a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows, use `venv\Scripts\activate`
   ```

3. **Install the required dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   - Create a `.env` file in the root directory of the project.
   - Add your Google API key to the `.env` file:
     ```
     GOOGLE_API_KEY=your_google_api_key
     ```

## Usage

1. **Run the Streamlit application**:
   ```bash
   streamlit run app.py
   ```

2. **Access the application**:
   - Open your web browser and navigate to `http://localhost:8501`.

## Project Structure

- `app.py`: The main application file.
- `components/`: Contains the sidebar and chat interface components.
- `utils/`: Utility functions and classes used in the project.
- `requirements.txt`: List of dependencies required for the project.
- `.env`: Environment variables (not included in the repository).

## Contributing

Contributions are welcome! Please follow these steps to contribute:

1. **Fork the repository**.
2. **Create a new branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes**.
4. **Commit your changes**:
   ```bash
   git commit -m "Add your commit message"
   ```
5. **Push to the branch**:
   ```bash
   git push origin feature/your-feature-name
   ```
6. **Create a Pull Request**.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [Streamlit](https://streamlit.io/)
- [Google Generative AI](https://cloud.google.com/ai)
- [Matplotlib](https://matplotlib.org/)
- [Pandas](https://pandas.pydata.org/)
