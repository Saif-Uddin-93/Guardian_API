# Guardian-API

![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=fff)
![AWS](https://img.shields.io/badge/AWS-%23FF9900.svg?logo=amazon-web-services&logoColor=white)
![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)

## Overview
Guardian-API is a tool designed to interact with The Guardian's API and retrieve relevant article data in JSON format. The data is then sent to an AWS SQS queue, allowing other AWS applications to consume and process the information efficiently.

[**Live Demo**](https://saif-uddin-93.github.io/Guardian_API/) *(Deployed Web Page)*
<br>

<p align="center">
  <a href="https://www.youtube.com/watch?v=c8VyVuFl_5A" target="_blank" rel="noopener noreferrer">
    <b>Video Walkthrough<b>
    <br>
    <img src="https://img.youtube.com/vi/c8VyVuFl_5A/0.jpg" alt="Video guide on project" width="600">
  </a>
</p>

---

## User Story
> **As a coding tutor,** I want to search for relevant articles from The Guardian to stay up-to-date with the latest in the software development space.

---

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [License](#license)
- [Testing](#testing)
- [Contact](#contact)

---

## Installation

To set up the project, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/saif-uddin-93/Guardian_API.git
   cd Guardian_API
   ```

2. Create Virtual Environment:
   ```bash
   python -m venv venv
   ```

3. Activate Virtual Environment (for Linux and Mac OS):
   ```bash
   source venv/bin/activate
   ```

4. Install dependencies:
   ```bash
   make requirements
   ```
   *(Ensure `make` is installed on your system to run the above command.)*

5. Install Terrform. In Ubuntu and Debian you can run the following command:
    ```bash
    sudo apt install terraform
    ```

6. Optionally, you can install AWS CLI. [Refer to the AWS documentation](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)

---

## Usage

1. Ensure your AWS credentials are set in your environment variables:
   ```bash
   export AWS_ACCESS_KEY_ID="your_access_key"
   export AWS_SECRET_ACCESS_KEY="your_secret_key"
   ```

2. Run Terraform commands from the terraform folder:
    ```bash
    terraform init
    terraform plan
    terraform apply
    ```

3. Navigate to the deployed Web Page or open the index.html file in project root folder:
   - Type in a search term and click "Search" to query the Guardian's API. You add filters to your search by clicking on "Filters".
   - Results appear at the bottom of the page.
   - Enter you AWS API ID (can be found in the [AWS console](https://eu-west-2.console.aws.amazon.com/apigateway/main/apis?region=eu-west-2))
   - Click on "send to SQS" to send the articles to an SQS queue named "guardian-queue".

---

## License
This project is licensed under the **Apache License 2.0**. See [LICENSE.txt](LICENSE.txt) for details.

For more information, visit: [Apache License 2.0](http://www.apache.org/licenses/)

---

## Testing

To run tests, use the following command from your project root folder:

```bash
pytest
```

The `pytest.ini` file includes additional configurations for test execution.

---

## Contact

For any inquiries or questions, feel free to reach out:

- **GitHub**: [@saif-uddin-93](https://github.com/saif-uddin-93)
- **Email**: _(Not available)_

---

## Future Improvements 🚀
- [ ] Complete installation and setup documentation.
- [ ] Add a video walkthrough.
- [ ] Implement advanced search filtering.
- [ ] Expand AWS integration features.

---

*README last updated: April 2025*
