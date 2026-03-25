import csv
import subprocess
import sys


def run_script():
    result = subprocess.run([sys.executable, 'planning.py'], capture_output=True, text=True)
    assert result.returncode == 0, f"Script failed: {result.stderr}"


def read_processed():
    rows = {}
    with open('planning_processed.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows[row['Week']] = row
    return rows


def test_header():
    run_script()
    with open('planning_processed.csv', 'r') as f:
        header = f.readline().strip()
    assert header == 'Week,Essentieel,Aanbevolen,Bonus', f"Header was: {header!r}"


def test_week_1_1_essentieel():
    run_script()
    rows = read_processed()
    cell = rows['1.1']['Essentieel']
    assert 'in H0:' in cell
    assert 'in 0.E:' in cell
    assert 'in 1.1:' in cell
    assert '0.2' not in cell  # old format gone
    assert 'Exercises:' not in cell
    assert 'Chapter exercises:' not in cell


def test_week_1_2_essentieel():
    run_script()
    rows = read_processed()
    cell = rows['1.2']['Essentieel']
    # exercises like 1.1.32 -> in 1.1: 32
    assert 'in 1.1:' in cell
    # chapex like 1.1 -> in 1.E: 1
    assert 'in 1.E:' in cell


def test_week_7_2_essentieel():
    run_script()
    rows = read_processed()
    cell = rows['7.2']['Essentieel']
    # 6.2.22 -> in 6.2: 22
    assert 'in 6.2:' in cell
    assert '22' in cell
    # 10.1.5 -> in 10.1: 5
    assert 'in 10.1:' in cell
    # chapex 10.14 -> in 10.E: 14
    assert 'in 10.E:' in cell


def test_b_section():
    run_script()
    rows = read_processed()
    cell = rows['6.2']['Essentieel']
    # B.3.5 -> in B.3: 5
    assert 'in B.3:' in cell


def test_multiline_cells():
    run_script()
    rows = read_processed()
    # Cells with multiple sections should use newlines
    cell = rows['1.1']['Essentieel']
    assert '\n' in cell


if __name__ == '__main__':
    tests = [test_header, test_week_1_1_essentieel, test_week_1_2_essentieel,
             test_week_7_2_essentieel, test_b_section, test_multiline_cells]
    failed = 0
    for t in tests:
        try:
            t()
            print(f"PASS {t.__name__}")
        except AssertionError as e:
            print(f"FAIL {t.__name__}: {e}")
            failed += 1
    sys.exit(failed)
