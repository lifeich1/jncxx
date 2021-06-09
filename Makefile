PHONY := usage
usage:
	@echo "Valid targets: $(PHONY)"


PHONY += updatenlohmannjson
nlohmannjson_tag = v3.9.1
updatenlohmannjson: path = vendor/nlohmann_json/nlohmann/json.hpp
updatenlohmannjson: url = https://github.com/nlohmann/json/releases/download/$(nlohmannjson_tag)/json.hpp
updatenlohmannjson:
	curl -fLo $(path) --create-dirs $(url)


.PHONY: $(PHONY)
