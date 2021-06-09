#include "data/User.hpp"
#include "data/UserList.hpp"

#include <iostream>

int main() {
    my::data::User u{"john", 117};
    std::string s;

    {
        nlohmann::json j;
        nlohmann::to_json(j, u);

        s = j.dump();
        std::cout << s << std::endl;
    }

    {
        auto j = nlohmann::json::parse(s);
        auto u = j.get<my::data::User>();

        my::data::UserList ul;
        ul.users = std::make_shared<decltype(ul.users)::element_type>();
        ul.users->emplace_back(u);

        nlohmann::json j2;
        nlohmann::to_json(j2, ul);
        std::cout << j2.dump() << std::endl;
    }


    return 0;
}
