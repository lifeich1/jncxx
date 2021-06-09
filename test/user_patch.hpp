    explicit User(std::string const & name, int64_t id):
        name{std::make_shared<std::string>(name)},
        id{std::make_shared<int64_t>(id)} {}
