"""
Do not modify this file. It is generated from the Swagger specification.

Container module for JSONSchema definitions.
This does not include inlined definitions.

The pretty-printing functionality provided by the json module is superior to
what is provided by pformat, hence the use of json.loads().
"""
import json

# When no schema is provided in the definition, we use an empty schema
__UNSPECIFIED__ = {}

BranchItem = json.loads("""
{
    "properties": {
        "id": {
            "example": "d290f1ee-6c54-4b01-90e6-d701748f0851",
            "format": "uuid",
            "type": "string"
        },
        "name": {
            "example": "PPB",
            "type": "string"
        },
        "releaseDate": {
            "example": "2016-08-29T09:12:33.001Z",
            "format": "date-time",
            "type": "string"
        }
    },
    "required": [
        "id",
        "name"
    ],
    "type": "object"
}
""")

CategoryItem = json.loads("""
{
    "properties": {
        "branch": {
            "properties": {
                "id": {
                    "example": "d290f1ee-6c54-4b01-90e6-d701748f0851",
                    "format": "uuid",
                    "type": "string"
                },
                "name": {
                    "example": "PPB",
                    "type": "string"
                },
                "releaseDate": {
                    "example": "2016-08-29T09:12:33.001Z",
                    "format": "date-time",
                    "type": "string"
                }
            },
            "required": [
                "id",
                "name"
            ],
            "type": "object",
            "x-scope": [
                ""
            ]
        },
        "createdDate": {
            "example": "2016-08-29T09:12:33.001Z",
            "format": "date-time",
            "type": "string"
        },
        "id": {
            "example": "d290f1ee-6c54-4b01-90e6-d701748f0851",
            "format": "uuid",
            "type": "string"
        },
        "name": {
            "example": "Category Name",
            "type": "string"
        }
    },
    "required": [
        "id",
        "name"
    ],
    "type": "object"
}
""")

CreateBranchItem = json.loads("""
{
    "properties": {
        "name": {
            "example": "PPB",
            "type": "string"
        }
    },
    "required": [
        "name"
    ],
    "type": "object"
}
""")

CreateCategoryItem = json.loads("""
{
    "properties": {
        "name": {
            "example": "Category Name",
            "type": "string"
        }
    },
    "required": [
        "name"
    ],
    "type": "object"
}
""")

CreateTaskItem = json.loads("""
{
    "properties": {
        "assignedTo": {
            "example": "title/position",
            "type": "string"
        },
        "dueDate": {
            "example": "dd-mm-yyyy:hh-mm-ss",
            "type": "string"
        },
        "title": {
            "example": "Deploy and test",
            "type": "string"
        }
    },
    "required": [
        "assignedTo",
        "dueDate",
        "title"
    ],
    "type": "object"
}
""")

FileItem = json.loads("""
{
    "properties": {
        "category": {
            "properties": {
                "id": {
                    "example": "d290f1ee-6c54-4b01-90e6-d701748f0851",
                    "format": "uuid",
                    "type": "string"
                },
                "name": {
                    "example": "PPB",
                    "type": "string"
                },
                "releaseDate": {
                    "example": "2016-08-29T09:12:33.001Z",
                    "format": "date-time",
                    "type": "string"
                }
            },
            "required": [
                "id",
                "name"
            ],
            "type": "object",
            "x-scope": [
                ""
            ]
        },
        "createdDate": {
            "example": "2016-08-29T09:12:33.001Z",
            "format": "date-time",
            "type": "string"
        },
        "filename": {
            "example": "File Name",
            "type": "string"
        },
        "id": {
            "example": "d290f1ee-6c54-4b01-90e6-d701748f0851",
            "format": "uuid",
            "type": "string"
        },
        "title": {
            "example": "Title",
            "type": "string"
        },
        "uploadedBy": {
            "example": "Title/Position",
            "type": "string"
        }
    },
    "required": [
        "id"
    ],
    "type": "object"
}
""")

SearchItem = json.loads("""
{
    "properties": {
        "data": {
            "example": {},
            "properties": {},
            "type": "object"
        },
        "objectType": {
            "example": "Task | Message | File",
            "type": "string"
        }
    },
    "type": "object"
}
""")

TaskItem = json.loads("""
{
    "properties": {
        "assignedTo": {
            "example": "title/position",
            "type": "string"
        },
        "branch": {
            "properties": {
                "id": {
                    "example": "d290f1ee-6c54-4b01-90e6-d701748f0851",
                    "format": "uuid",
                    "type": "string"
                },
                "name": {
                    "example": "PPB",
                    "type": "string"
                },
                "releaseDate": {
                    "example": "2016-08-29T09:12:33.001Z",
                    "format": "date-time",
                    "type": "string"
                }
            },
            "required": [
                "id",
                "name"
            ],
            "type": "object",
            "x-scope": [
                ""
            ]
        },
        "createdBy": {
            "example": "title/position",
            "type": "string"
        },
        "createdDate": {
            "example": "2016-08-29T09:12:33.001Z",
            "format": "date-time",
            "type": "string"
        },
        "dueDate": {
            "example": "2016-08-29T09:12:33.001Z",
            "format": "date-time",
            "type": "string"
        },
        "id": {
            "example": "d290f1ee-6c54-4b01-90e6-d701748f0851",
            "format": "uuid",
            "type": "string"
        },
        "title": {
            "example": "PPB",
            "type": "string"
        },
        "updatedDate": {
            "example": "2016-08-29T09:12:33.001Z",
            "format": "date-time",
            "type": "string"
        }
    },
    "type": "object"
}
""")

UpdateTaskItem = json.loads("""
{
    "properties": {
        "assignedTo": {
            "example": "title/position",
            "type": "string"
        },
        "dueDate": {
            "example": "dd-mm-yyyy:hh-mm-ss",
            "type": "string"
        },
        "title": {
            "example": "Deploy and test",
            "type": "string"
        }
    },
    "type": "object"
}
""")

