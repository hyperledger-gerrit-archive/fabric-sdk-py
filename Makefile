# Run all test cases, and should be triggered by the ci
check: pep8 pylint py27 py30 py35

.PHONY: pep8
pep8:
	tox -v -epep8

.PHONY: pylint
pylint:
	set -o pipefail
	tox -v -epylint | tee pylint.txt
	set +o pipefail

.PHONY: py27
py27:
	bin_path=.tox/$venv/bin
	export PYTHON=$bin_path/python
	tox -v -e$venv

# Generate the hyperledger/fabric-sdk-py image
.PHONY: docker
docker:
	build -t hyperledger/fabric-sdk-py .
