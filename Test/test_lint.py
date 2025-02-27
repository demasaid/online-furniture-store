import subprocess

def test_code_style():
    """Ensure code follows PEP8 and linting rules"""
    result = subprocess.run(["ruff", "check", "app/"], capture_output=True, text=True)
    assert result.returncode == 0, f"Linting issues:\n{result.stdout}"
