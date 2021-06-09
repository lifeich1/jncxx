PHONY := usage
usage:
	@echo "Valid targets: $(PHONY)"

M4 := m4 -P
MKDIR := mkdir -p
PY := python3


PHONY += updatenlohmannjson
nlohmannjson_tag = v3.9.1
updatenlohmannjson: path = vendor/nlohmann_json/nlohmann/json.hpp
updatenlohmannjson: url = https://github.com/nlohmann/json/releases/download/$(nlohmannjson_tag)/json.hpp
updatenlohmannjson:
	curl -fLo $(path) --create-dirs $(url)

PHONY += jncxx
jncxx: O := out
jncxx:
	$(MKDIR) $(O)
	$(M4) py/jngen.py m4/jn.m4 input.m4 > $(O)/gen.py
	$(PY) $(O)/gen.py


.PHONY: $(PHONY)
