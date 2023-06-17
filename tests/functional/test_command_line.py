from importlib.resources import files
from unittest.mock import patch

from calcifer import runner


class Scenario:

    def __init__(self, input_lines, output_lines):
        self.input = input_lines
        self.output = output_lines

    @classmethod
    def get(cls, name):
        module_name = "tests.functional.scenarios"
        with (files(module_name) / "base.out.txt").open('r') as text_io:
            output_lines = text_io.read().split("\n")
        with (files(module_name) / f"{name}.in.txt").open('r') as text_io:
            input_lines = text_io.read().split("\n")
        with (files(module_name) / f"{name}.out.txt").open('r') as text_io:
            output_lines += text_io.read().split("\n")
        return cls(input_lines, output_lines)


def test_take_drop(capsys):
    scenario = Scenario.get('takedrop')
    input_commands = scenario.input
    expected_output = scenario.output
    with patch('builtins.input', side_effect=input_commands):
        runner.main()
    actual_output_lines = capsys.readouterr().out.split("\n")[0:-1]
    assert actual_output_lines == expected_output
