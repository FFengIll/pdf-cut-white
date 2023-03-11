python cli.py -i cases/input/input.pdf -o output/output.pdf > /dev/null 2>&1
echo $? "== 0"
python cli.py -i cases/input/non_exist.pdf -o output/output.pdf > /dev/null 2>&1
echo $? "== 1"
