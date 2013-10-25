/* These are the 5 families of data types, + a coordinate array + 2 help containers for vector and matrix */
enum GMT_enum_family {
	GMT_IS_DATASET = 0,	/* Entity is data table */
	GMT_IS_TEXTSET,		/* Entity is a Text table */
	GMT_IS_GRID,		/* Entity is a GMT grid */
	GMT_IS_CPT,		/* Entity is a CPT table */
	GMT_IS_IMAGE,		/* Entity is a 1- or 3-layer unsigned char image */
	GMT_IS_VECTOR,		/* Entity is set of user vectors */
	GMT_IS_MATRIX,		/* Entity is user matrix */
	GMT_IS_COORD};		/* Entity is a double coordinate array */


