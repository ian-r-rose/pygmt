/*               gmt_vector.c
 * A small bit of C code for wrapping the gmt types
 * GMT_VECTOR and GMT_MATRIX.  An attempt was made
 * to do this via the standard ctypes module, but
 * it had to make a lot of assumptions about memory
 * layout and potentially compiler specific stuff.
 * It seemed safer to do some of the low-level API
 * manipulation from a compiled C code.           */


//numpy throws stupid warning if using the dev version
#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION

#include <Python.h>
#include <numpy/arrayobject.h>
#include <gmt.h>
#include "capsulethunk.h"



// Set up the methods table.  Python needs this in order
// to know how to refer to the functions defined here
static PyObject *gmt_vector_from_array_list ( PyObject *self, PyObject *args);
static PyObject *free_gmt_vector ( PyObject *self, PyObject *args);

static PyObject *gmt_textset_from_string_list ( PyObject *self, PyObject *args);
static PyObject *free_gmt_textset ( PyObject *self, PyObject *args);

void init_gmt_structs(void);

static PyMethodDef _gmt_structsMethods[] = {
    {"gmt_vector_from_array_list", gmt_vector_from_array_list, METH_VARARGS},
    {"free_gmt_vector", free_gmt_vector, METH_VARARGS},
    {"gmt_textset_from_string_list", gmt_textset_from_string_list, METH_VARARGS},
    {"free_gmt_textset", free_gmt_textset, METH_VARARGS},
    {NULL, NULL}
};

void init_gmt_structs()
{
    (void) Py_InitModule("_gmt_structs", _gmt_structsMethods);
    import_array();
}


//Given a python list of 1D numpy vectors, create a GMT_Vector object,
//which stores the shape of each vector and pointers to the start
//of the data block.  Does NOT do much checking of lengths and types,
//instead this should be done in a light python wrapper of this function
static PyObject *gmt_vector_from_array_list ( PyObject *self, PyObject *args)
{
    unsigned long n_cols;
    unsigned long n_rows;

    PyObject* py_vec;
    PyObject* array_list;
    PyArrayObject* array;
    double *array_data;
    unsigned int i;

    //Parse a list of numpy arrays
    if (!PyArg_ParseTuple(args, "OO!", &py_vec, &PyList_Type, &array_list)) return NULL;

    //throw error if the size of the list doesn't make sense
    n_cols = PyList_Size(array_list);
    if (n_cols <=0) return NULL;
    n_rows = PyArray_DIMS((PyArrayObject *)PyList_GetItem(array_list, 0))[0];
    if (n_rows <=0) return NULL;


    //Allocate memory for the GMT_VECTOR
    struct GMT_VECTOR *vector = (struct GMT_VECTOR*) PyCapsule_GetPointer(py_vec, NULL);
    vector->n_columns = n_cols;
    vector->n_rows = n_rows;
    vector->alloc_mode= GMT_ALLOCATED_EXTERNALLY;

    //Loop over the columns and point each data pointer to the data
    //in the numpy array. 
    for (i=0; i<n_cols; i++)
    {
        array = (PyArrayObject *)PyList_GetItem(array_list, i);
        array_data = (double *)PyArray_DATA(array);

        vector->data[i] = (union GMT_UNIVECTOR)array_data;
        vector->type[i] = (enum GMT_enum_type)GMT_DOUBLE;
         
        Py_INCREF( (PyObject*) array);
    }
    
    return Py_None;
} 

//Free the memory allocated for a GMT_Vector.
//Does not free the numpy array to which it points
static PyObject *free_gmt_vector ( PyObject *self, PyObject *args)
{
    PyObject* array_list;
    PyObject* array;
    PyObject* py_vec;
    unsigned int n_cols;
    unsigned int i;

    if (!PyArg_ParseTuple(args, "OO!", &py_vec, &PyList_Type, &array_list)) return NULL;

    struct GMT_VECTOR *vector = (struct GMT_VECTOR*) PyCapsule_GetPointer(py_vec, NULL);

    n_cols = PyList_Size(array_list);
    if (n_cols <=0) return NULL;
    for (i=0; i<n_cols; i++)
    {
        vector->data[i] = (union GMT_UNIVECTOR)(double*) NULL;
        array = PyList_GetItem(array_list, i);
        Py_DECREF(array);
    } 
    return Py_None;
}

static PyObject *gmt_textset_from_string_list ( PyObject *self, PyObject *args)
{
    unsigned long n_records;

    struct GMT_TEXTSET* set;
    struct GMT_TEXTTABLE* table;
    struct GMT_TEXTSEGMENT *segment; 
    PyObject* textset;
    PyObject* string_list;
    PyObject* string;
    unsigned int i;

    //Parse a list of strings
    if (!PyArg_ParseTuple(args, "OO!", &textset, &PyList_Type, &string_list)) return NULL;

    //throw error if the size of the list doesn't make sense
    n_records = PyList_Size(string_list);
    if (n_records <=0) return NULL;

    set = (struct GMT_TEXTSET *)PyCapsule_GetPointer(textset, NULL);
    table = set->table[0];
    segment = table->segment[0];

    //Loop over the columns and point each data pointer to the data
    //in the numpy array. 
    for (i=0; i<n_records; i++)
    {
        string = PyList_GetItem(string_list, i);
        segment->record[i] = PyString_AsString(string);
        segment->n_rows = n_records;

        Py_INCREF( string );
    }
    return Py_None;
} 

static PyObject *free_gmt_textset ( PyObject *self, PyObject *args)
{
    unsigned long n_records;

    PyObject* textset;
    PyObject* string_list;
    PyObject* string;
    unsigned int i;

    struct GMT_TEXTSET* set;
    struct GMT_TEXTTABLE* table;
    struct GMT_TEXTSEGMENT *segment; 

    //Parse a list of numpy arrays
    if (!PyArg_ParseTuple(args, "OO!", &textset, &PyList_Type, &string_list)) return NULL;

    n_records = PyList_Size(string_list);

    set = (struct GMT_TEXTSET *)PyCapsule_GetPointer(textset, NULL);
    table = set->table[0];
    segment = table->segment[0];


    //Loop over the columns and point each data pointer to the data
    //in the numpy array. 
    for (i=0; i<n_records; i++)
    {
        segment->record[i] = NULL;
        string = PyList_GetItem(string_list, i);
        Py_DECREF( string );
    }
    return Py_None;
} 

