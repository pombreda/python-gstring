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
#ifndef GSTRINGC_H_
#define GSTRINGC_H_

#define DEFAULT_GSTRING_SIZE 0
#define DEFAULT_GSTRING_TEXT ""

typedef struct {
	PyObject_HEAD
	GString *gstring;
} GStringType;

static PyTypeObject GStringPyType;

void initgstringc(void);
static int GStringType_init(GStringType *self, PyObject *args, PyObject *kwds);
static void GStringType_dealloc(PyObject *self);

static PyObject* GStringType_FromGStringType(GStringType *string_obj);
static PyObject* GStringType_FromString(const gchar *string);

static PyObject* GStringType_str(GStringType *self);
static PyObject* GStringType_assign(GStringType *self, PyObject *args, PyObject *kwds);
static PyObject* GStringType_append(register GStringType *self, register PyObject *args, register PyObject *kwds);
static PyObject* GStringType_prepend(GStringType *self, PyObject *args, PyObject *kwds);
static PyObject* GStringType_insert(GStringType *self, PyObject *args, PyObject *kwds);
static PyObject* GStringType_overwrite(GStringType *self, PyObject *args, PyObject *kwds);
static PyObject* GStringType_erase(GStringType *self, PyObject *args, PyObject *kwds);
static PyObject* GStringType_truncate(GStringType *self, PyObject *args, PyObject *kwds);
static PyObject* GStringType_set_size(GStringType *self, PyObject *args, PyObject *kwds);
static PyObject* GStringType_get_item(GStringType *self, PyObject* key);
static PyObject* GStringType_add(PyObject *self, PyObject *other);
static PyObject* GStringType_inplace_add(register PyObject *self, register PyObject *other);
static PyObject* GStringType_get_value(GStringType *self, PyObject *args, PyObject *kwds);
static PyObject* GStringType_get_allocated_len(PyObject *self, PyObject *args, PyObject* kwds);
static PyObject* GStringType_ascii_up(GStringType *self, PyObject *args, PyObject *kwds);
static PyObject* GStringType_ascii_down(GStringType *self, PyObject *args, PyObject *kwds);
static long GStringType_hash(GStringType *self);
static int GStringType_compare(GStringType *self, GStringType *other);
static int GStringType_len(GStringType *self);
static int GStringType_set_item(GStringType *self, PyObject *key, PyObject *value);


#endif /* GSTRINGC_H_ */
