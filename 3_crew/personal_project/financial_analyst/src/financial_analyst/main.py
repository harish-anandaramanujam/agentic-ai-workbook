#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from financial_analyst.crew import FinancialAnalyst

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

def run():
    """Run the crew"""
    inputs = {
        "company": "Viasat Inc.",
    }

    crew = FinancialAnalyst().crew().kickoff(inputs=inputs)
    print(crew)

if __name__ == "__main__":
    run()