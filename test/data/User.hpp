#pragma once

#include <nlohmann/json.hpp>
#include "helper.hpp"

#include <stdexcept>
#include <vector>
#include <string>

namespace my {
namespace data {
struct User;
struct UserList;

struct User {
    std::shared_ptr<std::string> name;
    std::shared_ptr<int64_t> id;
    std::shared_ptr<int64_t> testIdAndTest;

    User() = default;

    explicit User(std::string const & name, int64_t id):
        name{std::make_shared<std::string>(name)},
        id{std::make_shared<int64_t>(id)} {}
};

} // namespace my
} // namespace data


namespace nlohmann {
    void from_json(const json & j, my::data::User & x);
    void to_json(json & j, my::data::User const & x);

    inline void from_json(const json & j, my::data::User & x) {
        x.name = my::data::get_optional<std::string>(j, "a");
        x.id = my::data::get_optional<int64_t>(j, "b");
        x.testIdAndTest = my::data::get_optional<int64_t>(j, "test_id_and_test");
    }

    void to_json(json & j, my::data::User const & x);
        if (x.name) j["a"] = x.name;
        if (x.id) j["b"] = x.id;
        if (x.testIdAndTest) j["test_id_and_test"] = x.testIdAndTest;
    }
} // namespace nlohmann
