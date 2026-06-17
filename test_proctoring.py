from agents.proctoring_agent import (
    ProctoringAgent
)


def main():

    agent = ProctoringAgent()

    agent.start_monitoring()


if __name__ == "__main__":
    main()