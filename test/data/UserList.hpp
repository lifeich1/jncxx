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

struct UserList {
    std::shared_ptr<std::vector<my::data::User>> users;

    UserList() = default;

};

} // namespace my
} // namespace data


namespace nlohmann {
    void from_json(const json & j, my::data::UserList & x);
    void to_json(json & j, my::data::UserList const & x);

    inline void from_json(const json & j, my::data::UserList & x) {
        x.users = my::data::get_optional<std::vector<my::data::User>>(j, "users");
    }

    void to_json(json & j, my::data::UserList const & x);
        if (x.users) j["users"] = x.users;
    }
} // namespace nlohmann
