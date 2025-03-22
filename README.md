# OLX Price Monitor

This project is a web scraping application designed to monitor new postings and price changes for specific products on OLX. It follows clean code and clean architecture principles, ensuring maintainability and scalability.

## Features

- Scrapes product listings from OLX based on specified queries.
- Monitors price changes and new postings for specific products.
- Sends notifications for price changes or new postings.
- Modular architecture separating domain, application, and infrastructure layers.

## Project Structure

```
olx-price-monitor/
├── src/
│   ├── domain/                # Domain layer containing business logic
│   ├── application/           # Application layer handling use cases
│   ├── infrastructure/        # Infrastructure layer for data access and external services
│   ├── interfaces/            # Interfaces for CLI and API
│   └── config/                # Configuration settings
├── tests/                     # Test suite for unit and integration tests
├── scripts/                   # Scripts for running the application
├── pyproject.toml             # Project metadata and dependencies
├── poetry.lock                # Locked dependencies
├── .env.example               # Example environment variables
├── .gitignore                 # Files to ignore in version control
└── README.md                  # Project documentation
```

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd olx-price-monitor
   ```

2. Install dependencies using Poetry:
   ```
   poetry install
   ```

3. Set up environment variables by copying `.env.example` to `.env` and updating the values as needed.

## Usage

To run the price monitoring script, use the following command:
```
poetry run python scripts/run_monitor.py
```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.