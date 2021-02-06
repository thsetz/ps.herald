from subprocess import PIPE, run
from click.testing import CliRunner
from ps.herald.ps_herald import main as herald_main
from ps.herald.ps_neelix import main as neelix_main
from ps.herald.ps_bridge import main as bridge_main


def test_ps_herald_cmdline(stage):
    runner = CliRunner()
    result = runner.invoke(herald_main, ["-x", "-d"])

    assert result.exit_code == 0
    assert "Debug mode is on" in result.output
    assert "ps_herald" in result.output
    # Test via external process
    result = run(
        ["ps_herald", "-d", "-x"],
        stdout=PIPE,
        stderr=PIPE,
        universal_newlines=True,
    )
    assert result.returncode == 0
    assert "Debug mode is on" in result.stdout
    assert "ps_herald" in result.stdout
    assert result.stderr == ""


def test_ps_bridge_cmdline(stage):
    runner = CliRunner()
    result = runner.invoke(bridge_main, ["-x", "-d"])
    assert result.exit_code == 0
    assert "Debug mode is on" in result.output
    assert "ps_bridge" in result.output
    # Test via external process
    result = run(
        ["ps_bridge", "-d", "-x"],
        stdout=PIPE,
        stderr=PIPE,
        universal_newlines=True,
    )
    assert result.returncode == 0
    assert "Debug mode is on" in result.stdout
    assert "ps_bridge" in result.stdout
    assert result.stderr == ""


def test_ps_neelix_cmdline(stage):
    runner = CliRunner()
    result = runner.invoke(neelix_main, ["-x", "-d"])
    assert result.exit_code == 0
    assert "Debug mode is on" in result.output
    assert "ps_neelix" in result.output
    # Test via external process
    result = run(
        ["ps_neelix", "-d", "-x"],
        stdout=PIPE,
        stderr=PIPE,
        universal_newlines=True,
    )
    assert result.returncode == 0
    assert "Debug mode is on" in result.stdout
    assert "ps_neelix" in result.stdout
    assert result.stderr == ""
