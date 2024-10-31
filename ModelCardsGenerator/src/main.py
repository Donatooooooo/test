from Utils.logger import Logger
from Utils.parser import parser
from Utils.exceptions import ParserError, ImpossibleIntegration
from generator import ModelCardGenerator
from mlflow.exceptions import MlflowException
import sys

def generator():
    output = Logger()
    try:
        generator = ModelCardGenerator("http://127.0.0.1:5000/")
        lineage = generator.modelLineage()

        parsedInfo = None
        try:
            parsedInfo = parser()
        except ParserError as e:
            output.error(f"Invalid file format in main.md: {str(e)}. Could not integrate")

        for model in lineage:
            generator.ModelCard(model, parsedInfo)

        output.merge(generator.getOutput())
    except MlflowException as e:
        output.error("Check provided URI: invalid format")
    except FileNotFoundError as e:
        output.error(f"Check file path, {str(e).split('] ')[1]}")
    except Exception as e:
        output.error(f"Exception caused by: {str(e)}")
    finally:
        output.display()


def integrator():
    output = Logger()
    try:
        generator = ModelCardGenerator("http://127.0.0.1:5000/")
        
        parsedInfo = parser()
        generator.forceIntegrate(parsedInfo)

        output.merge(generator.getOutput())
    except ParserError as e:
        output.error(f"Invalid file format in main.md: {str(e)}. Could not integrate")
    except ImpossibleIntegration as e:
        output.error(str(e))
    except Exception as e:
        output.error(f"Exception caused by: {str(e)}")
    finally:
        output.display()


if __name__ == "__main__":
    if sys.argv[1] == "0":
        generator()
    elif sys.argv[1] == "1":
        integrator()
    else:
        sys.exit(1)