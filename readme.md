# project scripts

> To be used as a git submodule with Makefile commands for each project repository.

## Makefile

```make
BOM_PATH?=_data/bill_of_materials.csv
KICAD_XML?=hardware/Palm.xml

install:
	echo "Installing git-secrets from awslabs..."
	brew install git-secrets
	echo "Adding git-secrets config..."
	cat scripts/git-secrets >> .git/config
	echo "Installing pre-commit hook"
	touch .git/hooks/pre-commit || exit
	echo "Making pre-commit hook executable"
	chmod u+x .git/hooks/pre-commit

bom:
	rm -f $(BOM_PATH)
	python scripts/bom.py $(KICAD_XML) $(BOM_PATH)
	node scripts/bom_info.js
```
