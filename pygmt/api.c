#include <Python.h>
#include <gmt.h>
#include "capsulethunk.h"



// Set up the methods table.  Python needs this in order
// to know how to refer to the functions defined here
static PyObject *gmt_create_session ( PyObject *self, PyObject *args);
static PyObject *gmt_destroy_session ( PyObject *self, PyObject *args);
static PyObject *gmt_option ( PyObject *self, PyObject *args);
static PyObject *gmt_register_io ( PyObject *self, PyObject *args);
static PyObject *gmt_encode_id ( PyObject *self, PyObject *args);
static PyObject *gmt_retrieve_data ( PyObject *self, PyObject *args);
static PyObject *gmt_create_data ( PyObject *self, PyObject *args);
static PyObject *gmt_destroy_data ( PyObject *self, PyObject *args);
static PyObject *gmt_read_data ( PyObject *self, PyObject *args);
static PyObject *gmt_write_data ( PyObject *self, PyObject *args);
static PyObject *gmt_call_module ( PyObject *self, PyObject *args);
static PyObject *gmt_get_id ( PyObject *self, PyObject *args);


//Two basic functions that take a short python list and convert it to a
//c array of the relevant type.  Not extensively tested, as the package
//doesn't really deal much with the wesn objects
static double* double_ptr_from_list(PyObject *, double*,  unsigned int length);
static uint64_t* uint64_ptr_from_list(PyObject *, uint64_t*, unsigned int length);

void init_api(void);

static PyMethodDef _apiMethods[] = {
    {"gmt_create_session", gmt_create_session, METH_VARARGS},
    {"gmt_destroy_session", gmt_destroy_session, METH_VARARGS},
    {"gmt_option", gmt_option, METH_VARARGS},
    {"gmt_register_io", gmt_register_io, METH_VARARGS},
    {"gmt_encode_id", gmt_encode_id, METH_VARARGS},
    {"gmt_retrieve_data", gmt_retrieve_data, METH_VARARGS},
    {"gmt_create_data", gmt_create_data, METH_VARARGS},
    {"gmt_destroy_data", gmt_destroy_data, METH_VARARGS},
    {"gmt_read_data", gmt_read_data, METH_VARARGS},
    {"gmt_write_data", gmt_write_data, METH_VARARGS},
    {"gmt_call_module", gmt_call_module, METH_VARARGS},
    {"gmt_get_id", gmt_get_id, METH_VARARGS},
    {NULL, NULL}
};

void init_api()
{
    (void) Py_InitModule("_api", _apiMethods);
}


//Take a python list of doubles and turn it into a c array
//of doubles.  For use as the wesn argument in a few places
static double* double_ptr_from_list(PyObject *list, double* wesn, unsigned int length)
{
    unsigned int i, len;
    PyObject *py_float;
    if (list == Py_None) return NULL;  //return NULL if we have been passed Py_None
    if ( ! PyList_Check(list) ) return NULL;  //Or if it is not a list at all
    len = PyList_Size(list);
    if (len > length) return NULL;  //Or if it is too long
    
    //okay, do the actual work
    for (i=0; i<len; i++)
    {
        py_float = PyList_GetItem(list, i);
        wesn[i] = PyFloat_AsDouble(py_float);
    }
    return wesn;
}

//Take a python list of longs and turn it into a c array
//of longs.  Basically identical to the function above
static uint64_t* uint64_ptr_from_list(PyObject *list, uint64_t* par, unsigned int length)
{
    unsigned int i, len;
    PyObject *py_int;
    if (list == Py_None) return NULL;
    if ( ! PyList_Check(list) ) return NULL;
    len = PyList_Size(list);
    if (len > length) return NULL;
    
    for (i=0; i<len; i++)
    {
        py_int = PyList_GetItem(list, i);
        par[i] = PyInt_AsLong(py_int);
    }
    return par;
}


static PyObject *gmt_create_session ( PyObject *self, PyObject *args)
{
    char* name = NULL;
    void* API = NULL; 
    PyObject* capsule = NULL;

    //Parse the argument list
    if (!PyArg_ParseTuple(args, "s", &name)) return NULL;

    //Create the session
    API = GMT_Create_Session(name, 2, 0, NULL);
    if (!API ) return NULL;
 
    //Create and return the capsule object
    capsule = PyCapsule_New(API, NULL, NULL);
    if (!capsule ) return NULL;
    
    return Py_BuildValue("O", capsule);
} 


static PyObject *gmt_destroy_session ( PyObject *self, PyObject *args)
{
    const char* name = NULL;
    void* API = NULL; 
    PyObject* capsule = NULL;
    int ret;

    //Parse the argument list
    if (!PyArg_ParseTuple(args, "O", &capsule)) return NULL;
    if (!PyCapsule_CheckExact(capsule)) return NULL;

    //Get the GMT session pointer from the capsule object
    name = PyCapsule_GetName(capsule);
    if (!PyCapsule_IsValid(capsule, name)) return NULL;
    API = PyCapsule_GetPointer(capsule, name);
    if (!API ) return NULL;
 
    //destroy the session
    ret = GMT_Destroy_Session(API);
 
    return Py_BuildValue("i", ret);
} 


static PyObject *gmt_option ( PyObject *self, PyObject *args)
{
    const char* name = NULL;
    void* API = NULL; 
    PyObject* capsule = NULL;
    int ret;
    char* options = NULL;

    //Parse the argument list
    if (!PyArg_ParseTuple(args, "Os", &capsule, &options)) return NULL;
    if (!PyCapsule_CheckExact(capsule)) return NULL;

    //Get the GMT session pointer from the capsule object
    name = PyCapsule_GetName(capsule);
    if (!PyCapsule_IsValid(capsule, name)) return NULL;
    API = PyCapsule_GetPointer(capsule, name);
    if (!API ) return NULL;

    //Do the actual call
    ret = GMT_Option(API, options);
 
    return Py_BuildValue("i", ret);
} 

static PyObject *gmt_call_module ( PyObject *self, PyObject *args)
{
    const char* name = NULL;
    void* API = NULL; 
    PyObject* capsule = NULL;
    int mode, ret;
    PyObject* options = NULL;
    PyObject* string = NULL;
    char* module = NULL;
    char **argv_opts;
    unsigned int argc,i;

    //Parse the argument list
    if (!PyArg_ParseTuple(args, "OsiO", &capsule, &module, &mode, &options)) return NULL;
    if (!PyCapsule_CheckExact(capsule)) return NULL;

    //Get the GMT session pointer from the capsule object
    name = PyCapsule_GetName(capsule);
    if (!PyCapsule_IsValid(capsule, name)) return NULL;
    API = PyCapsule_GetPointer(capsule, name);
    if (!API ) return NULL;

    //Decide how to call based on the input options 

    if (mode == GMT_MODULE_EXIST || mode == GMT_MODULE_PURPOSE)
      ret = GMT_Call_Module(API, module, mode, '\0');
    else if (mode == GMT_MODULE_OPT) return NULL;
    else if (PyString_Check(options))
      ret = GMT_Call_Module(API, module, GMT_MODULE_CMD, PyString_AsString(options));
    else if ( PyList_Check(options) )
    {
        argc = PyList_Size(options);
        argv_opts = (char**)malloc( argc * sizeof(char*) );
        for(i=0; i<argc; ++i)
        {
            string = PyList_GetItem(options, i);
            argv_opts[i] = PyString_AsString(string);
        }
        ret = GMT_Call_Module(API, module, argc, argv_opts);
        free(argv_opts);
        
    }
    else return NULL;;
 
    return Py_BuildValue("i", ret);

} 

static PyObject *gmt_register_io ( PyObject *self, PyObject *args)
{
    const char* name = NULL;
    void* API = NULL; 
    PyObject* capsule = NULL;
    PyObject* py_ptr = NULL;
    PyObject* py_wesn = NULL;
    int id = -1;
  
    unsigned int family=0,method=0,geometry=0,direction=0;
    double wesn[4];
    void* ptr = NULL;
    

    //Parse the argument list
    if (!PyArg_ParseTuple(args, "OIIIIOO", &capsule, &family,
                          &method, &geometry, &direction,
                          &py_wesn, &py_ptr)) return NULL;
    if (!PyCapsule_CheckExact(capsule)) return NULL;

    //Get the GMT session pointer from the capsule object
    name = PyCapsule_GetName(capsule);
    if (!PyCapsule_IsValid(capsule, name)) return NULL;
    API = PyCapsule_GetPointer(capsule, name);
    if (!API ) return NULL;

    //check the type of py_ptr, and set ptr accordingly.
    //Allow it to be a string or an opaque pointer which
    //was retrieved from some other part of the code
    if (py_ptr == Py_None) ptr = NULL;
    else if (PyCapsule_CheckExact(py_ptr))
    {
        const char *tmp = NULL;
        tmp = PyCapsule_GetName(py_ptr);
        if (!PyCapsule_IsValid(py_ptr, tmp)) return NULL;
        ptr =  PyCapsule_GetPointer(py_ptr, name);
    }
    else if (PyString_Check(py_ptr))
    {
        ptr = (void*) PyString_AsString(py_ptr);
    }
    else return NULL;

    id = GMT_Register_IO(API, family, method, geometry, direction,
                          double_ptr_from_list(py_wesn, wesn, 4), ptr );
 
    return Py_BuildValue("i", id);
} 


static PyObject *gmt_encode_id ( PyObject *self, PyObject *args)
{
    const char* name = NULL;
    void* API = NULL; 
    PyObject* capsule = NULL;
    char id_str[16];
    int ret, id;

    //Parse the argument list
    if (!PyArg_ParseTuple(args, "Oi", &capsule, &id)) return NULL;
    if (!PyCapsule_CheckExact(capsule)) return NULL;

    //Get the GMT session pointer from the capsule object
    name = PyCapsule_GetName(capsule);
    if (!PyCapsule_IsValid(capsule, name)) return NULL;
    API = PyCapsule_GetPointer(capsule, name);
    if (!API ) return NULL;

    ret = GMT_Encode_ID(API, id_str, id);
    return Py_BuildValue("is", ret,id_str);
}

static PyObject *gmt_retrieve_data ( PyObject *self, PyObject *args)
{
    const char* name = NULL;
    void* API = NULL; 
    PyObject* capsule = NULL;
    int id;
    void* data;

    //Parse the argument list
    if (!PyArg_ParseTuple(args, "Oi", &capsule, &id)) return NULL;
    if (!PyCapsule_CheckExact(capsule)) return NULL;

    //Get the GMT session pointer from the capsule object
    name = PyCapsule_GetName(capsule);
    if (!PyCapsule_IsValid(capsule, name)) return NULL;
    API = PyCapsule_GetPointer(capsule, name);
    if (!API ) return NULL;

    data = GMT_Retrieve_Data(API, id);
    if (!data) return Py_None;
    return Py_BuildValue("O", PyCapsule_New(data, NULL, NULL));
}


static PyObject *gmt_create_data ( PyObject *self, PyObject *args)
{
    const char* name = NULL;
    void* API = NULL; 
    PyObject* capsule = NULL;
    PyObject* py_ptr = NULL;
    PyObject* py_par = NULL;
    PyObject* py_wesn = NULL;
    PyObject* py_inc = NULL;
  
    unsigned int family=0,geometry=0,mode=0,registration=0;
    int pad = 0;
    double wesn[4];
    uint64_t par[4];
    void* ptr = NULL;
    void* data = NULL;
    

    //Parse the argument list
    if (!PyArg_ParseTuple(args, "OIIIOOOIiO", &capsule, &family,
                          &geometry, &mode, &py_par, &py_wesn,
                          &py_inc, &registration, &pad, &py_ptr)) return NULL;
    if (!PyCapsule_CheckExact(capsule)) return NULL;

    //Get the GMT session pointer from the capsule object
    name = PyCapsule_GetName(capsule);
    if (!PyCapsule_IsValid(capsule, name)) return NULL;
    API = PyCapsule_GetPointer(capsule, name);
    if (!API ) return NULL;

    //Get the pointer from py_ptr
    if (py_ptr == Py_None) ptr = NULL; 
    else if (PyCapsule_CheckExact(py_ptr))
    {
        const char *tmp = NULL;
        tmp = PyCapsule_GetName(py_ptr);
        if (!PyCapsule_IsValid(py_ptr, tmp)) return NULL;
        ptr =  PyCapsule_GetPointer(py_ptr, name);
    }
    else return NULL;

    //The actual API call
    data = GMT_Create_Data(API, family, geometry, mode,  uint64_ptr_from_list(py_par, par, 4),
                         double_ptr_from_list(py_wesn, wesn, 4), NULL, registration, pad, ptr );

    //Return none if we failed
    if (!data) return Py_None;
    //Otherwise return the data
    return Py_BuildValue("O", PyCapsule_New(data, NULL, NULL));
} 

static PyObject *gmt_read_data ( PyObject *self, PyObject *args)
{
    const char* name = NULL;
    void* API = NULL; 
    PyObject* capsule = NULL;
    PyObject* py_ptr = NULL;
    PyObject* py_wesn = NULL;
  
    unsigned int family=0,method,geometry=0,mode=0;
    double wesn[4];
    void* ptr = NULL;
    void* data = NULL;
    char* input;
    

    //Parse the argument list
    if (!PyArg_ParseTuple(args, "OIIIIOsO", &capsule, &family,
                          &method, &geometry, &mode, &py_wesn,
                          &input, &py_ptr)) return NULL;
    if (!PyCapsule_CheckExact(capsule)) return NULL;

    //Get the GMT session pointer from the capsule object
    name = PyCapsule_GetName(capsule);
    if (!PyCapsule_IsValid(capsule, name)) return NULL;
    API = PyCapsule_GetPointer(capsule, name);
    if (!API ) return NULL;

    //Get the pointer from py_ptr
    if (py_ptr == Py_None) ptr = NULL; 
    else if (PyCapsule_CheckExact(py_ptr))
    {
        const char *tmp = NULL;
        tmp = PyCapsule_GetName(py_ptr);
        if (!PyCapsule_IsValid(py_ptr, tmp)) return NULL;
        ptr =  PyCapsule_GetPointer(py_ptr, name);
    }
    else return NULL;

    //Read the data
    data = GMT_Read_Data(API, family, method, geometry , mode, 
                         double_ptr_from_list(py_wesn, wesn, 4), input, ptr );

    //Return None if we failed
    if (!data) return Py_None;
 
    //Otherwise return the data
    return Py_BuildValue("O", PyCapsule_New(data, NULL, NULL));
} 

static PyObject *gmt_write_data ( PyObject *self, PyObject *args)
{
    const char* name = NULL;
    void* API = NULL; 
    PyObject* capsule = NULL;
    PyObject* py_ptr = NULL;
    PyObject* py_output = NULL;
    PyObject* py_wesn = NULL;
  
    unsigned int family=0,method,geometry=0,mode=0;
    double wesn[4];
    void* ptr = NULL;
    void* output = NULL;
    int ret;
    

    //Parse the argument list
    if (!PyArg_ParseTuple(args, "OIIIIOOO", &capsule, &family,
                          &method, &geometry, &mode, &py_wesn,
                          &py_output, &py_ptr)) return NULL;
    if (!PyCapsule_CheckExact(capsule)) return NULL;

    //Get the GMT session pointer from the capsule object
    name = PyCapsule_GetName(capsule);
    if (!PyCapsule_IsValid(capsule, name)) return NULL;
    API = PyCapsule_GetPointer(capsule, name);
    if (!API ) return NULL;

    //Get the pointer from py_ptr
    if (py_ptr == Py_None) ptr = NULL; 
    else if (PyCapsule_CheckExact(py_ptr))
    {
        const char *tmp = NULL;
        tmp = PyCapsule_GetName(py_ptr);
        if (!PyCapsule_IsValid(py_ptr, tmp)) return NULL;
        ptr =  PyCapsule_GetPointer(py_ptr, name);
    }
    else return NULL;

    //Get the pointer from py_output
    if (py_output == Py_None) return NULL;
    else if (PyCapsule_CheckExact(py_output))
    {
        const char *tmp = NULL;
        tmp = PyCapsule_GetName(py_output);
        if (!PyCapsule_IsValid(py_output, tmp)) return NULL;
        output =  PyCapsule_GetPointer(py_output, tmp);
    }
    else if (PyString_Check(py_output))
    {
        output = (void*) PyString_AsString(py_output);
    }
    else return NULL;


    //Read the data
    ret = GMT_Write_Data(API, family, method, geometry , mode, 
                         double_ptr_from_list(py_wesn, wesn, 4), output, ptr );

    //Otherwise return the data
    return Py_BuildValue("i", ret);
} 

static PyObject *gmt_destroy_data ( PyObject *self, PyObject *args)
{
    const char* name = NULL;
    void* API = NULL; 
    PyObject* capsule = NULL;
    PyObject* py_ptr = NULL;
    void* ptr;
    int ret;

    //Parse the argument list
    if (!PyArg_ParseTuple(args, "OO", &capsule, &py_ptr)) return NULL;
    if (!PyCapsule_CheckExact(capsule)) return NULL;

    //Get the GMT session pointer from the capsule object
    name = PyCapsule_GetName(capsule);
    if (!PyCapsule_IsValid(capsule, name)) return NULL;
    API = PyCapsule_GetPointer(capsule, name);
    if (!API ) return NULL;

    //Get the pointer from py_ptr
    if (py_ptr == Py_None) ptr = NULL; 
    else if (PyCapsule_CheckExact(py_ptr))
    {
        const char *tmp = NULL;
        tmp = PyCapsule_GetName(py_ptr);
        if (!PyCapsule_IsValid(py_ptr, tmp)) return NULL;
        ptr =  PyCapsule_GetPointer(py_ptr, name);
    }
    else return NULL;
    
    ret = GMT_Destroy_Data(API, &ptr);

    return Py_BuildValue("i", ret);
}

static PyObject *gmt_get_id ( PyObject *self, PyObject *args)
{
    const char* name = NULL;
    void* API = NULL; 
    PyObject* capsule = NULL;
    PyObject* py_ptr = NULL;
    void* ptr;
    unsigned int family =0, direction=0;
    int id;

    //Parse the argument list
    if (!PyArg_ParseTuple(args, "OIIO", &capsule, &family, &direction, &py_ptr)) return NULL;
    if (!PyCapsule_CheckExact(capsule)) return NULL;

    //Get the GMT session pointer from the capsule object
    name = PyCapsule_GetName(capsule);
    if (!PyCapsule_IsValid(capsule, name)) return NULL;
    API = PyCapsule_GetPointer(capsule, name);
    if (!API ) return NULL;

    //Get the pointer from py_ptr
    if (py_ptr == Py_None) return NULL; 
    else if (PyCapsule_CheckExact(py_ptr))
    {
        const char *tmp = NULL;
        tmp = PyCapsule_GetName(py_ptr);
        if (!PyCapsule_IsValid(py_ptr, tmp)) return NULL;
        ptr =  PyCapsule_GetPointer(py_ptr, name);
    }
    else return NULL;
    
    id = GMT_Get_ID(API, family, direction, ptr);

    return Py_BuildValue("i", id);
}

