#!/usr/bin/env python3

import os

objlist = []

NS_AB = None
NS = None

class jnfield:
    def __init__(self, typ, name, jname = None):
        self.name = name
        self.type = typ
        self.jname = jname or None

    def tune(self):
        if self.jname is None:
            t = []
            for c in self.name:
                if c.isupper():
                    t.append('_')
                t.append(c.lower())
            self.jname = ''.join(t)
        global NS_AB, NS
        if NS_AB is not None:
            self.type = self.type.replace(NS_AB + '::', NS + '::')

    def out_def(self):
        return 'std::shared_ptr<%s> %s;' % (self.type, self.name)

    def out_parse(self, obj, jobj):
        global NS
        return '%s.%s = %s::get_optional<%s>(%s, "%s");' % \
            (obj, self.name, NS, self.type, jobj, self.jname)

    def out_gen(self, obj, jobj):
        return 'if (%s.%s) %s["%s"] = %s.%s;' % \
            (obj, self.name, jobj, self.jname, obj, self.name)

class jnobj:
    def __init__(self, name, patch = None):
        self.name = name
        self.patch = patch or None
        self.fs = []

    def add_field(self, typ, name, jname = None):
        f = jnfield(typ, name, jname)
        f.tune()
        self.fs.append(f)

    def write(self, fname):
        def sa(s, inden, s1):
            s.append((' ') * inden * 4 + s1)
        s = []
        line = lambda: sa(s, 0, '')
        sa(s, 0, '#pragma once')
        line()
        sa(s, 0, '#include <nlohmann/json.hpp>')
        sa(s, 0, '#include "helper.hpp"')
        line()
        sa(s, 0, '#include <stdexcept>')
        sa(s, 0, '#include <vector>')
        sa(s, 0, '#include <string>')
        line()
        for ns in NS.split('::'):
            sa(s, 0, 'namespace %s {' % ns)
        global objlist
        for obj in objlist:
            sa(s, 0, 'struct %s;' % obj.name)
        line()
        sa(s, 0, 'struct %s {' % self.name)
        for f in self.fs:
            sa(s, 1, f.out_def())
        line()
        sa(s, 1, '%s() = default;' % self.name)
        line()
        if self.patch is not None:
            with open(self.patch, 'r') as fin:
                pat = fin.readlines()
                for p in pat:
                    s.append(p.strip('\r\n'))
        sa(s, 0, '};')
        line()
        for ns in NS.split('::'):
            sa(s, 0, '} // namespace %s' % ns)
        line()
        line()
        sa(s, 0, 'namespace nlohmann {')
        typ = '%s::%s' % (NS, self.name)
        sa(s, 1, 'void from_json(const json & j, %s & x);' % typ)
        sa(s, 1, 'void to_json(json & j, %s const & x);' % typ)
        line()
        sa(s, 1, 'inline void from_json(const json & j, %s & x) {' % typ)
        for f in self.fs:
            sa(s, 2, f.out_parse('x', 'j'))
        sa(s, 1, '}')
        line()
        sa(s, 1, 'inline void to_json(json & j, %s const & x) {' % typ)
        for f in self.fs:
            sa(s, 2, f.out_gen('x', 'j'))
        sa(s, 1, '}')
        sa(s, 0, '} // namespace nlohmann')
        with open(fname, 'w') as fout:
            for l in s:
                print(l, file=fout)



def init(ns, nsab = None):
    global NS, NS_AB
    NS, NS_AB = ns, nsab or None


def finish(outdir):
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    global objlist
    for obj in objlist:
        obj.write(os.path.join(outdir, '%s.hpp' % obj.name))
    with open(os.path.join(outdir, 'helper.hpp'), 'w') as fout:
        s = '''//  To parse this JSON data, first install
//
//      json.hpp  https://github.com/nlohmann/json
//
//  Then include this file, and then do
//
//     helper.hpp data = nlohmann::json::parse(jsonString);

#pragma once

#include <nlohmann/json.hpp>

#include <stdexcept>
#include <regex>

#include <sstream>

%s
    using nlohmann::json;

    inline json get_untyped(const json & j, const char * property) {
        if (j.find(property) != j.end()) {
            return j.at(property).get<json>();
        }
        return json();
    }

    inline json get_untyped(const json & j, std::string property) {
        return get_untyped(j, property.data());
    }

    template <typename T>
    inline std::shared_ptr<T> get_optional(const json & j, const char * property) {
        if (j.find(property) != j.end()) {
            return j.at(property).get<std::shared_ptr<T>>();
        }
        return std::shared_ptr<T>();
    }

    template <typename T>
    inline std::shared_ptr<T> get_optional(const json & j, std::string property) {
        return get_optional<T>(j, property.data());
    }
%s

#ifndef NLOHMANN_OPT_HELPER
#define NLOHMANN_OPT_HELPER
namespace nlohmann {
    template <typename T>
    struct adl_serializer<std::shared_ptr<T>> {
        static void to_json(json & j, const std::shared_ptr<T> & opt) {
            if (!opt) j = nullptr; else j = *opt;
        }

        static std::shared_ptr<T> from_json(const json & j) {
            if (j.is_null()) return std::unique_ptr<T>(); else return std::unique_ptr<T>(new T(j.get<T>()));
        }
    };
}
#endif
'''
        a, b = '', ''
        for ns in NS.split('::'):
            a += 'namespace %s {\n' % ns
            b += '} // namespace %s\n' % ns
        s = s % (a, b)
        print(s, file=fout)

