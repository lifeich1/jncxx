JN_INIT([my::data], [MY])

JN_OBJ([User], [test/user_patch.hpp])
JN_FIELD([std::string], [name], [a])
JN_FIELD([int64_t], [id], [b])
JN_FIELD([int64_t], [testIdAndTest])

JN_OBJ([UserList])
JN_FIELD([std::vector<MY::User>], [users])


JN_OUTPUT([test/data])
