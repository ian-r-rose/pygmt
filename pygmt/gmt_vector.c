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
#include <arrayobject.h>
#include <gmt.h>



// Set up the methods table.  Python needs this in order
// to know how to refer to the functions defined here
static PyObject *gmt_vector_from_array_list ( PyObject *self, PyObject *args);
static PyObject *free_gmt_vector ( PyObject *self, PyObject *args);

static PyObject *gmt_matrix_from_array ( PyObject *self, PyObject *args);
static PyObject *free_gmt_matrix ( PyObject *self, PyObject *args);

static PyObject *gmt_textset_from_string_list ( PyObject *self, PyObject *args);
static PyObject *free_gmt_textset ( PyObject *self, PyObject *args);

static PyMethodDef _gmt_vectorMethods[] = {
    {"gmt_vector_from_array_list", gmt_vector_from_array_list, METH_VARARGS},
    {"free_gmt_vector", free_gmt_vector, METH_VARARGS},
    {"gmt_matrix_from_array", gmt_matrix_from_array, METH_VARARGS},
    {"free_gmt_matrix", free_gmt_vector, METH_VARARGS},
    {"gmt_textset_from_string_list", gmt_textset_from_string_list, METH_VARARGS},
    {"free_gmt_textset", free_gmt_textset, METH_VARARGS},
    {NULL, NULL}
};

void init_gmt_vector()
{
    (void) Py_InitModule("_gmt_vector", _gmt_vectorMethods);
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

    PyObject* array_list;
    PyArrayObject* array;
    double *array_data;

    //Parse a list of numpy arrays
    if (!PyArg_ParseTuple(args, "O!", &PyList_Type, &array_list)) return NULL;

    //throw error if the size of the list doesn't make sense
    n_cols = PyList_Size(array_list);
    if (n_cols <=0) return NULL;
    n_rows = PyArray_DIMS((PyArrayObject *)PyList_GetItem(array_list, 0))[0];
    if (n_rows <=0) return NULL;


    //Allocate memory for the GMT_VECTOR
    struct GMT_VECTOR *vector;
    vector = (struct GMT_VECTOR *)malloc(sizeof(struct GMT_VECTOR));
    vector->type = (enum GMT_enum_type *)malloc(sizeof(enum GMT_enum_type)*n_cols);
    vector->data = (union GMT_UNIVECTOR *)malloc(sizeof(union GMT_UNIVECTOR)*n_cols);
    vector->n_columns = n_cols;
    vector->n_rows = n_rows;
    vector->alloc_mode= GMT_ALLOCATED_EXTERNALLY;

    //Loop over the columns and point each data pointer to the data
    //in the numpy array. 
    for (unsigned int i=0; i<n_cols; i++)
    {
        array = (PyArrayObject *)PyList_GetItem(array_list, i);
        array_data = (double *)PyArray_DATA(array);

        vector->data[i] = (union GMT_UNIVECTOR)array_data;
        vector->type[i] = (enum GMT_enum_type)GMT_DOUBLE;
         
        Py_INCREF( (PyObject*) array);
    }
    //Return a pointer of sorts (actually a Python Long, which
    //should be cast to a ctypes.c_void_p in python
    return Py_BuildValue("O", PyLong_FromVoidPtr( (void *)vector));
} 

//Free the memory allocated for a GMT_Vector.
//Does not free the numpy array to which it points
static PyObject *free_gmt_vector ( PyObject *self, PyObject *args)
{
    struct GMT_VECTOR *vector;
    PyObject* ref;
    PyObject* array_list;
    unsigned int n_cols;

    if (!PyArg_ParseTuple(args, "O!O!", &PyLong_Type, &ref, &PyList_Type, &array_list)) return NULL;

    n_cols = PyList_Size(array_list);
    if (n_cols <=0) return NULL;
    for (unsigned int i=0; i<n_cols; i++)
        Py_DECREF(PyList_GetItem(array_list, i));
     
    vector = (struct GMT_VECTOR *)PyLong_AsVoidPtr(ref);

    free(vector->type); vector->type = NULL;
    free(vector->data); vector->data = NULL;
    free(vector);   

    return Py_None;
}

static PyObject *gmt_textset_from_string_list ( PyObject *self, PyObject *args)
{
    unsigned long n_records;

    struct GMT_TEXTSET* set;
    struct GMT_TEXTTABLE* table;
    struct GMT_TEXTSEGMENT *segment; 
    char *record;
    PyObject* textset;
    PyObject* string_list;
    PyObject* string;

    //Parse a list of strings
    if (!PyArg_ParseTuple(args, "O!O!", &PyLong_Type, &textset, &PyList_Type, &string_list)) return NULL;

    //throw error if the size of the list doesn't make sense
    n_records = PyList_Size(string_list);
    if (n_records <=0) return NULL;

    set = (struct GMT_TEXTSET *)PyLong_AsVoidPtr(textset);
    table = set->table[0];
    segment = table->segment[0];

    //Loop over the columns and point each data pointer to the data
    //in the numpy array. 
    for (unsigned int i=0; i<n_records; i++)
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

    PyObject* string_list;
    PyObject* string;

    //Parse a list of numpy arrays
    if (!PyArg_ParseTuple(args, "O!", &PyList_Type, &string_list)) return NULL;

    //throw error if the size of the list doesn't make sense
    n_records = PyList_Size(string_list);
    if (n_records <=0) return NULL;


    //Loop over the columns and point each data pointer to the data
    //in the numpy array. 
    for (unsigned int i=0; i<n_records; i++)
    {
        string = PyList_GetItem(string_list, i);
        Py_DECREF( string );
    }
    return Py_None;
} 


static PyObject *gmt_matrix_from_array ( PyObject *self, PyObject *args)
{
    unsigned long n_cols;
    unsigned long n_rows;

    double range[6];

    PyArrayObject* array;
    double *array_data;

    //Parse a list of numpy arrays
    if (!PyArg_ParseTuple(args, "O!(dddddd)", &PyArray_Type, &array, 
                          &range[0], &range[1], &range[2], &range[3],
                          &range[4], &range[5])) return NULL;

    //throw error if the size of the list doesn't make sense
    n_rows = PyArray_DIMS(array)[0];
    n_cols = PyArray_DIMS(array)[1];
    if (n_rows <=0 || n_cols <=0) return NULL;


    //Allocate memory for the GMT_MATRIX
    struct GMT_MATRIX *matrix;
    matrix = (struct GMT_MATRIX *)malloc(sizeof(struct GMT_MATRIX));
    matrix->n_columns = n_cols;
    matrix->n_rows = n_rows;
    matrix->alloc_mode= GMT_ALLOCATED_EXTERNALLY;
    matrix->shape = 0; 
    matrix->size = sizeof(double)*n_rows*n_cols; 
    matrix->n_layers = 1.0;

    array_data = (double *)PyArray_DATA(array);

    matrix->type = (enum GMT_enum_type)GMT_DOUBLE;
    matrix->data = (union GMT_UNIVECTOR)array_data;
    for (unsigned int i=0; i<6; ++i)
        matrix->range[i] = range[i];

//    for (unsigned int i=0; i<n_rows*n_cols; ++i)
//        printf("%lf\n", matrix->data.f8[i]);
//    printf("%lf, %lf, %lf, %lf\n", matrix->range[0], matrix->range[1], matrix->range[2], matrix->range[3]);

//    printf("%i, %i\n", n_rows, n_cols);

    //Return a pointer of sorts (actually a Python Long, which
    //should be cast to a ctypes.c_void_p in python
    return Py_BuildValue("O", PyLong_FromVoidPtr( (void *)matrix));
} 

//Free the memory allocated for a GMT_Vector.
//Does not free the numpy array to which it points
static PyObject *free_gmt_matrix ( PyObject *self, PyObject *args)
{
    struct GMT_MATRIX *matrix;
    PyObject *ref;

    if (!PyArg_ParseTuple(args, "O!", &PyLong_Type, &ref)) return NULL;

    matrix = (struct GMT_MATRIX *)PyLong_AsVoidPtr(ref);
    free(matrix);

    return Py_None;
}
