m4_divert(-1)
m4_changecom(`///')
m4_changequote([,])

m4_define([JN_INIT], [init("$1", "$2")])

m4_define([JN_OBJ], [
lastobj = jnobj("$1", "$2")
objlist.append(lastobj)])

m4_define([JN_FIELD], [lastobj.add_field("$1", "$2", "$3")])

m4_define([JN_OUTPUT], [finish("$1")])

m4_divert(0)m4_dnl
