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



static PyMethodDef _gmt_vectorMethods[] = {
    {"gmt_vector_from_array_list", gmt_vector_from_array_list, METH_VARARGS},
    {"free_gmt_vector", free_gmt_vector, METH_VARARGS},
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
    unsigned int n_cols;
    unsigned int n_rows;

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
    PyObject *ref;

    if (!PyArg_ParseTuple(args, "O!", &PyLong_Type, &ref)) return NULL;

    vector = (struct GMT_VECTOR *)PyLong_AsVoidPtr(ref);
    free(vector->type);
    free(vector->data);

    return Py_None;
}
