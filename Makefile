venv = venv
mypy = $(venv)/bin/python3
pybin != realpath `command -v python`
version != basename $(pybin)
pip = $(venv)/bin/pip

output += $(wildcard $(venv))
output += $(wildcard *.pdf)
output += $(wildcard *.gv)
output += $(wildcard __pycache__)

trans ?= -ci b

batch_images = $(wildcard images/*)
output_images = $(patsubst images/%, output/%, $(batch_images) )

help: .git/info/exclude ## Print the help message
	@awk 'BEGIN {FS = ":.*?## "} /^[0-9a-zA-Z._-]+:.*?## / {printf "\033[36m%s\033[0m : %s\n", $$1, $$2}' $(MAKEFILE_LIST) | \
		sort | \
		column -s ':' -t

out: run

$(pip):
	$(pybin) -m venv $(venv)

$(mypy): $(pip)

$(venv)/lib/$(version)/site-packages/: requirements.txt $(mypy)
	$(pip) install -r $<

ignore_file != dir .git/info/exclude || echo .gitignore

$(ignore_file): $(output)
	echo $^ | tr ' ' '\n' > $@

.PHONY: run
run: $(venv)/lib/$(version)/site-packages/ $(ignore_file) ## Run pixeldition (to check it works)
	$(mypy) pixeldition/main.py

%/:
	mkdir $@

.PHONY: batch
batch: $(output_images) ## Batch process all images in images/ with $(trans) argument

output/%: images/% | output/
	$(mypy) pixeldition/main.py $< $(trans) -o $@

clean:
	$(RM) -r $(output)


