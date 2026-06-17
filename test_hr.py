import json

from agents.hr_agent import HRAgent


def main():

    with open(
        "data/reports/PH_ARVIND_SHARMA_report.json",
        "r",
        encoding="utf-8"
    ) as file:

        report = json.load(
            file
        )

    hr_agent = HRAgent()

    result = (
        hr_agent.generate_hr_decision(
            report
        )
    )

    print(
        "\nHR DECISION:\n"
    )

    print(result)


if __name__ == "__main__":
    main()