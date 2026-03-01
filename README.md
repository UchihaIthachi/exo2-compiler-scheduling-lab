# Exo2 Submission Pack

Contents:
- report.md / report.pdf : write-up (Step 1–3)
- solutions/quiz*_solution.py : corrected schedules for Quiz1–3
- generate_targets.sh : generate required target C/H code using exocc
- target/ : output folder for generated code (created by generate_targets.sh)

## Generate target code (C/H)
1) Clone exo:
   git clone https://github.com/exo-lang/exo
   cd exo && git submodule update --init --recursive

2) Ensure exocc exists (pip install exo-lang OR build from source)

3) From this pack folder:
   ./generate_targets.sh /path/to/exo

Then upload:
- report.pdf
- solutions/
- target/quiz1, target/quiz2, target/quiz3
