/* Author: Christian S. Perone
 * License: LGPL
 * Email: christian.perone@gmail.com
 */

/* python-gstringc - A wrapper for GLib::GString
 * Copyright (C) 2009  Christian S. Perone
 *
 * This library is free software; you can redistribute it and/or
 * modify it under the terms of the GNU Lesser General Public
 * License as published by the Free Software Foundation; either
 * version 2 of the License, or (at your option) any later version.
 *
 * This library is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 * Lesser General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public
 * License along with this library; if not, write to the
 * Free Software Foundation, Inc., 59 Temple Place - Suite 330,
 * Boston, MA 02111-1307, USA.
 */
#include <Python.h>
#include <glib.h>

typedef struct {
	PyObject_HEAD
	GString *gstring;
} GStringType;

static PyObject *
GStringType_from_GStringType(GStringType *string_obj);

static PyObject *
GStringType_from_String(const gchar *string);

static PyTypeObject GStringPyType;

static int GStringType_init(GStringType *self, PyObject *args, PyObject *kwds)
{
	const gchar *string = NULL;
	int	  size;

	if (!PyArg_ParseTuple(args, "|si", &string, &size)) return -1;

	if(string==NULL) string = "";

	if(size>0) {
		self->gstring = g_string_sized_new(size);
		self->gstring = g_string_assign(self->gstring, string);
	} else self->gstring = g_string_new(string);

	if(self->gstring==NULL) {
		PyErr_SetString(PyExc_MemoryError, "GLib::GString cannot allocate memory for GString");
		return -1;
	}

	return 0;
}

static void
GStringType_dealloc(GStringType *self)
{
	if(self->gstring != NULL) g_string_free(self->gstring, TRUE);
	self->ob_type->tp_free((PyObject*)self);
}

static PyObject*
GStringType_str(GStringType *self)
{
	return Py_BuildValue("s", self->gstring->str);
}

static PyObject*
GStringType_assign(GStringType *self, PyObject *args, PyObject *kwds)
{
	const gchar *string;
	if(!PyArg_ParseTuple(args, "s", &string)) return NULL;
	self->gstring = g_string_assign(self->gstring, string);
	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject*
GStringType_append(GStringType *self, PyObject *args, PyObject *kwds)
{
	const gchar *string;
	if(!PyArg_ParseTuple(args, "s", &string)) return NULL;
	self->gstring = g_string_append(self->gstring, string);
	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject*
GStringType_prepend(GStringType *self, PyObject *args, PyObject *kwds)
{
	const gchar *string;
	if(!PyArg_ParseTuple(args, "s", &string)) return NULL;
	self->gstring = g_string_prepend(self->gstring, string);
	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject*
GStringType_insert(GStringType *self, PyObject *args, PyObject *kwds)
{
	const gchar *string;
	gssize size;
	if(!PyArg_ParseTuple(args, "is", &size, &string)) return NULL;
	self->gstring = g_string_insert(self->gstring, size, string);
	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject*
GStringType_overwrite(GStringType *self, PyObject *args, PyObject *kwds)
{
	const gchar *string;
	gsize size;
	if(!PyArg_ParseTuple(args, "Is", &size, &string)) return NULL;
	self->gstring = g_string_overwrite(self->gstring, size, string);
	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject*
GStringType_erase(GStringType *self, PyObject *args, PyObject *kwds)
{
	gssize pos, len;
	if(!PyArg_ParseTuple(args, "ii", &pos, &len)) return NULL;
	self->gstring = g_string_erase(self->gstring, pos, len);
	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject*
GStringType_truncate(GStringType *self, PyObject *args, PyObject *kwds)
{
	gsize len;
	if(!PyArg_ParseTuple(args, "I", &len)) return NULL;
	self->gstring = g_string_truncate(self->gstring, len);
	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject*
GStringType_set_size(GStringType *self, PyObject *args, PyObject *kwds)
{
	gsize len;
	if(!PyArg_ParseTuple(args, "I", &len)) return NULL;
	self->gstring = g_string_set_size(self->gstring, len);
	Py_INCREF(Py_None);
	return Py_None;
}

static long
GStringType_hash(GStringType *self)
{
	return g_string_hash(self->gstring);
}

static int
GStringType_compare(GStringType *self, GStringType *other)
{
	return !g_string_equal(self->gstring, other->gstring);
}

static int
GStringType_len(GStringType *self)
{
	return self->gstring->len;
}

static PyObject*
GStringType_get_item(GStringType *self, PyObject* key)
{
	long index;
	if(!PyInt_Check(key)) {
		PyErr_SetString(PyExc_IndexError, "index must be integer");
		return NULL;
	}
	index = PyInt_AsLong(key);
	if(index >= self->gstring->len)
	{
		PyErr_SetString(PyExc_IndexError, "index out of range");
		return NULL;
	}

	return Py_BuildValue("c", self->gstring->str[index]);
}

static PyObject*
GStringType_add(PyObject *self, PyObject *other)
{
	GStringType *str = NULL;

	if(PyObject_TypeCheck(other, &PyString_Type)) {
		str = (GStringType*)GStringType_from_GStringType( (GStringType*)self);
		str->gstring = g_string_append(str->gstring, PyString_AsString(other));
		return (PyObject *) str;
	}

	if(PyObject_TypeCheck(other, &GStringPyType)) {
		const gchar *st = PyString_AsString(self);
		str = (GStringType*)GStringType_from_String(st);
		str->gstring = g_string_append(str->gstring, ((GStringType*)other)->gstring->str);
		return (PyObject *) str;
	}

	Py_INCREF(Py_NotImplemented);
	return Py_NotImplemented;
}

static PyObject*
GStringType_inplace_add(PyObject *self, PyObject *other)
{
	GStringType *self_cast = (GStringType*) self;

	if(PyString_Check(other)) {
		self_cast->gstring = g_string_append(self_cast->gstring, PyString_AsString(other));
		Py_INCREF(self);
		return self;
	}

	if(PyObject_TypeCheck(other, &GStringPyType)) {
		self_cast->gstring = g_string_append(self_cast->gstring, ((GStringType*)other)->gstring->str);
		Py_INCREF(self);
		return self;
	}

	Py_INCREF(Py_NotImplemented);
	return Py_NotImplemented;
}

static PyObject*
GStringType_get_value(PyObject *self, PyObject *args, PyObject *kwds)
{
	GStringType* self_cast = (GStringType *) self;
	return Py_BuildValue("s", self_cast->gstring->str);
}

static PyObject *
GStringType_from_GStringType(GStringType *string_obj)
{
	GStringType *op;
	op = (GStringType *) PyObject_MALLOC(sizeof(GStringType));
	if (op == NULL) return PyErr_NoMemory();
	PyObject_INIT(op, &GStringPyType);
	op->gstring = g_string_new(string_obj->gstring->str);
	return (PyObject *) op;
}

static PyObject *
GStringType_from_String(const gchar *string)
{
	GStringType *op;
	op = (GStringType *) PyObject_MALLOC(sizeof(GStringType));
	if (op == NULL) return PyErr_NoMemory();
	PyObject_INIT(op, &GStringPyType);
	op->gstring = g_string_new(string);
	return (PyObject *) op;
}

static PyObject*
GStringType_get_allocated_len(PyObject *self, PyObject *args, PyObject* kwds)
{
	return Py_BuildValue("i", ((GStringType *)self)->gstring->allocated_len);
}

static int
GStringType_set_item(GStringType *self, PyObject *key, PyObject *value)
{
	glong pos = 0;

	if(!PyInt_Check(key)) {
		PyErr_SetString(PyExc_TypeError, "the key index must be integer");
		return -1;
	}
	pos = PyInt_AS_LONG(key);

	if((pos >= self->gstring->len) || (pos < 0) ) {
		PyErr_SetString(PyExc_IndexError, "index out of range");
		return -1;
	}

	if(value==NULL) {
		self->gstring =  g_string_erase(self->gstring, pos, 1);
		return 0;
	}

	if(!PyString_Check(value)) {
		PyErr_SetString(PyExc_TypeError, "the value must be a string with size 1");
		return -1;
	}

	if(PyString_Size(value)!=1) {
		PyErr_SetString(PyExc_TypeError, "the value must be a string with size 1");
		return -1;
	}
	char *str = PyString_AsString(value);
	self->gstring = g_string_overwrite(self->gstring, pos, str);
	return 0;
}


static PyMappingMethods
GStringType_MappingMethods = {
		(lenfunc) GStringType_len,
		(binaryfunc) GStringType_get_item,
		(objobjargproc) GStringType_set_item
};

static PyNumberMethods
GStringType_NumberMethods = {
	(binaryfunc) GStringType_add, /* (binaryfunc) add PyObject * (*binaryfunc)(PyObject *, PyObject *);*/
	0,
	0,
	0,
	0,
	0,
	0,
	0,
	0,
	0,
	0,
	0,
	0,
	0,
	0,
	0,
	0,
	0,
	0,
	0,
	0,
	0,
	0,
	(binaryfunc) GStringType_inplace_add, /* binaryfunc nb_inplace_add */
	0,
	0,
	0,
	0,
	0,
	0,
	0,
	0,
	0,
	0,
	0,
	0,
	0,
	0,
	0
};


static PyMethodDef
GStringType_methods[] = {
   { "assign",    (PyCFunction) GStringType_assign, METH_VARARGS,
               "Copies the bytes from a string into a GString, destroying"
               "any previous contents." },
   { "append",    (PyCFunction) GStringType_append, METH_VARARGS,
			   "Adds a string onto the end of a GString, expanding it"
			   "if necessary." },
   { "prepend",    (PyCFunction) GStringType_prepend, METH_VARARGS,
			   "Adds a string on to the start of a GString, expanding"
			   "it if necessary." },
   { "insert",    (PyCFunction) GStringType_insert, METH_VARARGS,
			   "Inserts a copy of a string into a GString, expanding"
			   "it if necessary." },
   { "overwrite",    (PyCFunction) GStringType_overwrite, METH_VARARGS,
			   "Overwrites part of a string, lengthening it if"
			   "necessary." },
   { "erase",    (PyCFunction) GStringType_erase, METH_VARARGS,
			   "Removes len bytes from a GString, starting at position pos. "
			   "The rest of the GString is shifted down to fill the gap." },
   { "truncate",    (PyCFunction) GStringType_truncate, METH_VARARGS,
	     	   "Cuts off the end of the GString, leaving the first len bytes." },
   { "set_size",    (PyCFunction) GStringType_set_size, METH_VARARGS,
			   "Sets the length of a GString. If the length is less than the"
			   "current length, the string will be truncated." },
   { "get_value",    (PyCFunction) GStringType_get_value, METH_VARARGS,
			   "Get the string in the buffer of the GString." },
   { "get_allocated_len",    (PyCFunction) GStringType_get_allocated_len, METH_VARARGS,
			   "Get the number of bytes that can be stored in the string"
			   "before it needs to be reallocated." },
			   { NULL }
};



static PyTypeObject
GStringPyType = {
   PyObject_HEAD_INIT(NULL)
   0,                         /* ob_size */
   "gstringc.GString",                 /* tp_name */
   sizeof(GStringType),       /* tp_basicsize */
   0,                         /* tp_itemsize */
   (destructor)GStringType_dealloc, /* tp_dealloc */
   0,                         /* tp_print */
   0,                         /* tp_getattr */
   0,                         /* tp_setattr */
   (cmpfunc)GStringType_compare,                         /* tp_compare */
   0,                         /* tp_repr */
   &GStringType_NumberMethods,                         /* tp_as_number */
   0,                         /* tp_as_sequence */
   &GStringType_MappingMethods,                         /* tp_as_mapping */
   (hashfunc) GStringType_hash,                         /* tp_hash */
   0,                         /* tp_call */
   (reprfunc) GStringType_str,           /* tp_str */
   0,                         /* tp_getattro */
   0,                         /* tp_setattro */
   0,                         /* tp_as_buffer */
   Py_TPFLAGS_DEFAULT | Py_TPFLAGS_CHECKTYPES | Py_TPFLAGS_HAVE_INPLACEOPS, /* tp_flags*/
   "GString object",      /* tp_doc */
   0,                         /* tp_traverse */
   0,                         /* tp_clear */
   0,                         /* tp_richcompare */
   0,                         /* tp_weaklistoffset */
   0,                         /* tp_iter */
   0,                         /* tp_iternext */
   GStringType_methods,        				  /* tp_methods */
   0,       				  /* tp_members */
   0,                         /* tp_getset */
   0,                         /* tp_base */
   0,                         /* tp_dict */
   0,                         /* tp_descr_get */
   0,                         /* tp_descr_set */
   0,                         /* tp_dictoffset */
   (initproc)GStringType_init,  /* tp_init */
   0,                         /* tp_alloc */
   0,                         /* tp_new */
};


void initgstringc(void)
{
	PyObject *mod;
    mod = Py_InitModule3("gstringc", NULL, "A GLib GString wrapper for Python.");
    if(mod==NULL) return;

    GStringPyType.tp_new = PyType_GenericNew;
	if (PyType_Ready(&GStringPyType) < 0) {
	  return;
	}
	Py_INCREF(&GStringPyType);
	PyModule_AddObject(mod, "GString", (PyObject*)&GStringPyType);

}
