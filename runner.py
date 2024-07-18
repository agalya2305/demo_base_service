import argparse
import logging
import os
import time

import prompts
from common.logging_util import get_std_logger, init_logging
from gen_ai.ai_bedrock_claude import AIBedrockClaude

# Get the current working directory
project_directory = os.path.abspath(os.path.dirname(__file__))
DEFAULT_LOGFILE = project_directory + "/" + "logs/server.log"
VERBOSE = True

MODEL_NAME = 'anthropic.claude-3-haiku-20240307-v1:0'
MODEL_PROVIDER = 'amazon'


class Runner:

    def __init__(self, logger):
        self.ai_bedrock_claude = AIBedrockClaude()
        self.logger = logger

    def run_app(self):
        self.logger.info("In run app")
        ai_response = self.ai_bedrock_claude.generate_text(model_id=MODEL_NAME,
                                                           prompt=prompts.prospect_report_user_prompt,
                                                           system_msg='')
        time.sleep(2)
        print(ai_response)

    @staticmethod
    def main():
        parser = argparse.ArgumentParser(description="Runner")
        parser.add_argument("--logfile", type=str, default=DEFAULT_LOGFILE, help="Path to the log file")
        parser.add_argument("--verbose", action="store_true", help="Enable verbose output", default=True)
        args = parser.parse_args()
        LOGFILE = args.logfile
        VERBOSE = args.verbose

        init_logging(log_file_path=LOGFILE, log_level=logging.INFO, verbose=VERBOSE)
        logger = get_std_logger()

        runner = Runner(logger)
        runner.run_app()
        logger.info("Runner completed")


if __name__ == '__main__':
    Runner.main()
