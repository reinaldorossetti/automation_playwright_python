# Web Automation and E2E Testing with Python & Playwright

This repository provides a comprehensive suite of scripts for web automation and end-to-end (E2E) testing using Python with the powerful Playwright framework. The examples range from basic browser navigation to advanced scenarios like handling authentication, managing downloads, and using asynchronous operations.

## 🎭 What is Playwright?

Playwright is a modern open-source framework developed by Microsoft for reliable browser automation. It stands out for its ability to control the latest browser engines, its robust auto-waiting mechanism that eliminates flaky tests, and its excellent debugging tools.

### Key Features

*   **Cross-Browser Compatibility**: Automate and test across all modern rendering engines: Chromium (Google Chrome, Microsoft Edge), WebKit (Apple Safari), and Mozilla Firefox.
*   **Auto-Waits**: Playwright automatically waits for elements to be actionable before performing actions. This eliminates the primary cause of flaky tests.
*   **Powerful Tooling**: Comes with exceptional tools like **Codegen** to generate tests by recording your actions, and the **Playwright Trace Viewer**, which provides a detailed, step-by-step trace of your test execution, including DOM snapshots, network requests, and console logs.
*   **Browser Contexts**: Create isolated, incognito-like browser sessions within a single browser instance. This is perfect for running parallel, independent tests.
*   **Network Interception**: Mock and modify network traffic to test edge cases without depending on a live backend.

## 🚀 Getting Started

Follow these instructions to set up the project and run the scripts on your local machine.

### Prerequisites

*   Python 3.11.1 or higher installed on your system. You can download it from the [official Python website](https://www.python.org/downloads/).
*   `pip` (Python package installer)

### Installation

1.  **Clone the repository:**
    ```sh
    git clone <YOUR_REPOSITORY_URL>
    cd automation_playwright_python
    ```

2.  **Create and activate a virtual environment (recommended):**
    ```sh
    # On Windows
    python -m venv venv
    .\venv\Scripts\activate

    # On macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install Python dependencies:**
    The [requirements.txt](requirements.txt) file contains all the necessary Python libraries, including `playwright` and `pytest-playwright`.
    ```sh
    pip install -r requirements.txt
    ```

4.  **Install Playwright browsers:**
    This command downloads the browser binaries for Chromium, Firefox, and WebKit.
    ```sh
    playwright install
    playwright install-deps
    ```

## ✅ Running Tests with Pytest

This project uses `pytest` and the `pytest-playwright` plugin for a seamless testing experience.

*   **Run all tests:**
    This command will discover and run all tests in the project headlessly.
    ```sh
    pytest
    ```

*   **Run tests in a specific browser:**
    ```sh
    pytest --browser chromium
    # or 
    --browser firefox
    --browser webkit
    --browser-channel msedge
    --browser-channel chrome
    ```

*   **Run tests in headed mode (to watch the browser):**
    ```sh
    pytest --headed
    PWDEBUG=1 pytest -s -v tests\\test_expect_samples.py --browser-channel msedge --browser chromium
    pytest -s -v tests\\test_expect_samples.py
    ```

*   **View test execution traces:**
    The `pytest-playwright` plugin automatically generates a trace for failed tests. You can view it with this command:
    ```sh
    playwright show-trace trace.zip
    ```

## � Handling Waits in Playwright

Playwright's robust waiting mechanisms are a cornerstone of its reliability, virtually eliminating flaky tests. It handles waiting in several ways:

### 1. Auto-Waiting

Playwright automatically waits for elements to be ready before interacting with them. For example, when you call `page.get_by_role("button").click()`, Playwright performs a series of checks to ensure the button is:

*   Attached to the DOM
*   Visible
*   Stable (not animating)
*   Enabled and able to receive events

This built-in behavior means you rarely need to add explicit waits in your scripts.

### 2. Navigation Waits

When navigating with `page.goto()`, you can specify when the navigation is considered complete using the `wait_until` option. This is crucial for synchronizing your script with the page's load state.

*   **`load`** (default): Waits for the `load` event.
*   **`domcontentloaded`**: Waits for the `DOMContentLoaded` event.
*   **`networkidle`**: Waits until there are no more network connections for 500 ms.
*   **`commit`**: Waits until a response is received from the server.

**Exemplo:** Veja o script **scripts/26-navigation-wait-until.py** para uma demonstração prática.

### 3. Explicit and Custom Waits

For dynamic web applications where content is loaded via AJAX, you might need to wait for a specific condition to be met.

*   **Wait for an element**: You can explicitly wait for an element to appear in the DOM.
    ```python
    # Wait for the first element matching the locator to be attached
    page.locator("td.film-title").first.wait_for()
    ```
    > Veja um exemplo em **scripts/27-custom-wait.py**.

*   **Wait for an event**: Playwright can wait for specific events to occur, such as a file download.
    ```python
    with page.expect_download() as download_info:
        page.get_by_role("link", name="Download free").click()
    download = download_info.value
    download.save_as("image.jpg")
    ```
    > Este padrão é demonstrado em **scripts/30-download.py**.

## �📜 Script Descriptions

The `scripts/` directory contains various examples demonstrating specific Playwright features:

*   **[scripts/26-navigation-wait-until.py](scripts/26-navigation-wait-until.py)**: Demonstrates different `wait_until` strategies (`load`, `domcontentloaded`, `networkidle`) for page navigation.
*   **[scripts/27-custom-wait.py](scripts/27-custom-wait.py)**: Shows how to implement custom waits for dynamic elements, which is essential for modern web apps with AJAX-loaded content.
*   **[scripts/30-download.py](scripts/30-download.py)**: Illustrates how to handle file downloads by listening for the `download` event.
*   **[scripts/32-async-playwright.py](scripts/32-async-playwright.py)**: Presents the usage of Playwright's asynchronous API with Python's `asyncio` for non-blocking operations.
*   **[scripts/34-app.py](scripts/34-app.py)**: A script to automate logging into a Google account and saving the authentication state (cookies, local storage) to a JSON file.
    > **⚠️ Note:** You must replace `YOUR_EMAIL` and `YOUR_PASSWORD` with your credentials and create the `playwright/.auth` directory before running.
*   **playwright_persistent_concurrency.py**: Shows how to run multiple asynchronous tasks in the same browser context, using a persistent context to maintain state across sessions.
*   **[scripts/40-check_mail.py](scripts/40-check_mail.py)**: Demonstrates how to use the saved authentication state from `34-app.py` to access an authenticated page (Gmail) and perform actions like checking for new emails.

## 📄 License

This project is licensed under the Apache 2.0 License - see the [LICENSE](LICENSE) file for details.