"""
Do not modify this file. It is generated from the Swagger specification.

"""
import importlib
import logging
import json
from jsonschema import ValidationError

from django.conf import settings
from django.http import JsonResponse, HttpResponseBadRequest
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views import View

import exec.schemas as schemas
import exec.utils as utils

# Set up logging
logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger(__name__)

try:
    VALIDATE_RESPONSES = settings.SWAGGER_API_VALIDATE_RESPONSES
except AttributeError:
    VALIDATE_RESPONSES = False
LOGGER.info("Swagger API response validation is {}".format(
    "on" if VALIDATE_RESPONSES else "off"
))

# Set up the stub class. If it is not explicitly configured in the settings.py
# file of the project, we default to a mocked class.
try:
    stub_class_path = settings.STUBS_CLASS
except AttributeError:
    stub_class_path = "exec.stubs.MockedStubClass"

module_name, class_name = stub_class_path.rsplit(".", 1)
Module = importlib.import_module(module_name)
Stubs = getattr(Module, class_name)


def maybe_validate_result(result_string, schema):
    if VALIDATE_RESPONSES:
        try:
            utils.validate(json.loads(result_string, encoding="utf8"), schema)
        except ValidationError as e:
            LOGGER.error(e.message)


@method_decorator(csrf_exempt, name="dispatch")
class Branch(View):

    GET_RESPONSE_SCHEMA = json.loads("""{
    "items": {
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
    "type": "array"
}""")
    POST_RESPONSE_SCHEMA = schemas.__UNSPECIFIED__
    POST_BODY_SCHEMA = schemas.CreateBranchItem

    def get(self, request, *args, **kwargs):
        """
        :param self: A Branch instance
        :param request: An HttpRequest
        """
        try:

            result = Stubs.get__api_v1_branch(request, )

            if type(result) is tuple:
                result, headers = result
            else:
                headers = {}

            # The result may contain fields with date or datetime values that will not
            # pass JSON validation. We first create the response, and then maybe validate
            # the response content against the schema.
            response = JsonResponse(result, safe=False)

            maybe_validate_result(response.content, self.GET_RESPONSE_SCHEMA)

            for key, val in headers.items():
                response[key] = val

            return response
        except ValidationError as ve:
            return HttpResponseBadRequest("Parameter validation failed: {}".format(ve.message))
        except ValueError as ve:
            return HttpResponseBadRequest("Parameter validation failed: {}".format(ve))

    def post(self, request, *args, **kwargs):
        """
        :param self: A Branch instance
        :param request: An HttpRequest
        """
        body = utils.body_to_dict(request.body, self.POST_BODY_SCHEMA)
        if not body:
            return HttpResponseBadRequest("Body required")

        try:

            result = Stubs.post__api_v1_branch(request, body, )

            if type(result) is tuple:
                result, headers = result
            else:
                headers = {}

            # The result may contain fields with date or datetime values that will not
            # pass JSON validation. We first create the response, and then maybe validate
            # the response content against the schema.
            response = JsonResponse(result, safe=False)

            maybe_validate_result(response.content, self.POST_RESPONSE_SCHEMA)

            for key, val in headers.items():
                response[key] = val

            return response
        except ValidationError as ve:
            return HttpResponseBadRequest("Parameter validation failed: {}".format(ve.message))
        except ValueError as ve:
            return HttpResponseBadRequest("Parameter validation failed: {}".format(ve))


@method_decorator(csrf_exempt, name="dispatch")
class BranchCategoryBranchId(View):

    GET_RESPONSE_SCHEMA = json.loads("""{
    "items": {
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
        "type": "object",
        "x-scope": [
            ""
        ]
    },
    "type": "array"
}""")
    POST_RESPONSE_SCHEMA = schemas.__UNSPECIFIED__
    POST_BODY_SCHEMA = schemas.CreateCategoryItem

    def get(self, request, branchId, *args, **kwargs):
        """
        :param self: A BranchCategoryBranchId instance
        :param request: An HttpRequest
        :param branchId: string ID of the branch to get
        """
        try:

            result = Stubs.get__api_v1_branch_category_branchId(request, branchId, )

            if type(result) is tuple:
                result, headers = result
            else:
                headers = {}

            # The result may contain fields with date or datetime values that will not
            # pass JSON validation. We first create the response, and then maybe validate
            # the response content against the schema.
            response = JsonResponse(result, safe=False)

            maybe_validate_result(response.content, self.GET_RESPONSE_SCHEMA)

            for key, val in headers.items():
                response[key] = val

            return response
        except ValidationError as ve:
            return HttpResponseBadRequest("Parameter validation failed: {}".format(ve.message))
        except ValueError as ve:
            return HttpResponseBadRequest("Parameter validation failed: {}".format(ve))

    def post(self, request, branchId, *args, **kwargs):
        """
        :param self: A BranchCategoryBranchId instance
        :param request: An HttpRequest
        :param branchId: string ID of the branch to get
        """
        body = utils.body_to_dict(request.body, self.POST_BODY_SCHEMA)
        if not body:
            return HttpResponseBadRequest("Body required")

        try:

            result = Stubs.post__api_v1_branch_category_branchId(request, body, branchId, )

            if type(result) is tuple:
                result, headers = result
            else:
                headers = {}

            # The result may contain fields with date or datetime values that will not
            # pass JSON validation. We first create the response, and then maybe validate
            # the response content against the schema.
            response = JsonResponse(result, safe=False)

            maybe_validate_result(response.content, self.POST_RESPONSE_SCHEMA)

            for key, val in headers.items():
                response[key] = val

            return response
        except ValidationError as ve:
            return HttpResponseBadRequest("Parameter validation failed: {}".format(ve.message))
        except ValueError as ve:
            return HttpResponseBadRequest("Parameter validation failed: {}".format(ve))


@method_decorator(csrf_exempt, name="dispatch")
class BranchCategoryFiles(View):

    GET_RESPONSE_SCHEMA = json.loads("""{
    "items": {
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
        "type": "object",
        "x-scope": [
            ""
        ]
    },
    "type": "array"
}""")

    def get(self, request, *args, **kwargs):
        """
        :param self: A BranchCategoryFiles instance
        :param request: An HttpRequest
        """
        try:
            if "branchId" not in request.GET:
                return HttpResponseBadRequest("branchId required")

            branchId = request.GET.get("branchId")

            schema = {'type': 'string'}
            utils.validate(branchId, schema)

            if "categoryId" not in request.GET:
                return HttpResponseBadRequest("categoryId required")

            categoryId = request.GET.get("categoryId")

            schema = {'type': 'string'}
            utils.validate(categoryId, schema)


            # fileId (optional): string ID of the file to get. if no fileId is given, will return all files
            fileId = request.GET.get("fileId", None)
            if fileId is not None:
                schema = {'type': 'string'}
                utils.validate(fileId, schema)
            result = Stubs.get__api_v1_branch_category_files(request, branchId, categoryId, fileId, )

            if type(result) is tuple:
                result, headers = result
            else:
                headers = {}

            # The result may contain fields with date or datetime values that will not
            # pass JSON validation. We first create the response, and then maybe validate
            # the response content against the schema.
            response = JsonResponse(result, safe=False)

            maybe_validate_result(response.content, self.GET_RESPONSE_SCHEMA)

            for key, val in headers.items():
                response[key] = val

            return response
        except ValidationError as ve:
            return HttpResponseBadRequest("Parameter validation failed: {}".format(ve.message))
        except ValueError as ve:
            return HttpResponseBadRequest("Parameter validation failed: {}".format(ve))


@method_decorator(csrf_exempt, name="dispatch")
class Search(View):

    GET_RESPONSE_SCHEMA = json.loads("""{
    "items": {
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
        "type": "object",
        "x-scope": [
            ""
        ]
    },
    "type": "array"
}""")

    def get(self, request, *args, **kwargs):
        """
        :param self: A Search instance
        :param request: An HttpRequest
        """
        try:

            # q (optional): string search string parameter.
            q = request.GET.get("q", None)
            if q is not None:
                schema = {'type': 'string'}
                utils.validate(q, schema)
            result = Stubs.get__api_v1_search(request, q, )

            if type(result) is tuple:
                result, headers = result
            else:
                headers = {}

            # The result may contain fields with date or datetime values that will not
            # pass JSON validation. We first create the response, and then maybe validate
            # the response content against the schema.
            response = JsonResponse(result, safe=False)

            maybe_validate_result(response.content, self.GET_RESPONSE_SCHEMA)

            for key, val in headers.items():
                response[key] = val

            return response
        except ValidationError as ve:
            return HttpResponseBadRequest("Parameter validation failed: {}".format(ve.message))
        except ValueError as ve:
            return HttpResponseBadRequest("Parameter validation failed: {}".format(ve))


@method_decorator(csrf_exempt, name="dispatch")
class Task(View):

    GET_RESPONSE_SCHEMA = json.loads("""{
    "items": {
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
        "type": "object",
        "x-scope": [
            ""
        ]
    },
    "type": "array"
}""")
    POST_RESPONSE_SCHEMA = schemas.__UNSPECIFIED__
    PUT_RESPONSE_SCHEMA = schemas.__UNSPECIFIED__
    POST_BODY_SCHEMA = schemas.CreateTaskItem
    PUT_BODY_SCHEMA = schemas.UpdateTaskItem

    def get(self, request, *args, **kwargs):
        """
        :param self: A Task instance
        :param request: An HttpRequest
        """
        try:

            result = Stubs.get__api_v1_task(request, )

            if type(result) is tuple:
                result, headers = result
            else:
                headers = {}

            # The result may contain fields with date or datetime values that will not
            # pass JSON validation. We first create the response, and then maybe validate
            # the response content against the schema.
            response = JsonResponse(result, safe=False)

            maybe_validate_result(response.content, self.GET_RESPONSE_SCHEMA)

            for key, val in headers.items():
                response[key] = val

            return response
        except ValidationError as ve:
            return HttpResponseBadRequest("Parameter validation failed: {}".format(ve.message))
        except ValueError as ve:
            return HttpResponseBadRequest("Parameter validation failed: {}".format(ve))

    def post(self, request, *args, **kwargs):
        """
        :param self: A Task instance
        :param request: An HttpRequest
        """
        body = utils.body_to_dict(request.body, self.POST_BODY_SCHEMA)
        if not body:
            return HttpResponseBadRequest("Body required")

        try:

            result = Stubs.post__api_v1_task(request, body, )

            if type(result) is tuple:
                result, headers = result
            else:
                headers = {}

            # The result may contain fields with date or datetime values that will not
            # pass JSON validation. We first create the response, and then maybe validate
            # the response content against the schema.
            response = JsonResponse(result, safe=False)

            maybe_validate_result(response.content, self.POST_RESPONSE_SCHEMA)

            for key, val in headers.items():
                response[key] = val

            return response
        except ValidationError as ve:
            return HttpResponseBadRequest("Parameter validation failed: {}".format(ve.message))
        except ValueError as ve:
            return HttpResponseBadRequest("Parameter validation failed: {}".format(ve))

    def put(self, request, *args, **kwargs):
        """
        :param self: A Task instance
        :param request: An HttpRequest
        """
        body = utils.body_to_dict(request.body, self.PUT_BODY_SCHEMA)
        if not body:
            return HttpResponseBadRequest("Body required")

        try:
            if "taskId" not in request.GET:
                return HttpResponseBadRequest("taskId required")

            taskId = request.GET.get("taskId")

            schema = {'type': 'string'}
            utils.validate(taskId, schema)


            result = Stubs.put__api_v1_task(request, body, taskId, )

            if type(result) is tuple:
                result, headers = result
            else:
                headers = {}

            # The result may contain fields with date or datetime values that will not
            # pass JSON validation. We first create the response, and then maybe validate
            # the response content against the schema.
            response = JsonResponse(result, safe=False)

            maybe_validate_result(response.content, self.PUT_RESPONSE_SCHEMA)

            for key, val in headers.items():
                response[key] = val

            return response
        except ValidationError as ve:
            return HttpResponseBadRequest("Parameter validation failed: {}".format(ve.message))
        except ValueError as ve:
            return HttpResponseBadRequest("Parameter validation failed: {}".format(ve))


@method_decorator(csrf_exempt, name="dispatch")
class TaskBranchId(View):

    GET_RESPONSE_SCHEMA = json.loads("""{
    "items": {
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
        "type": "object",
        "x-scope": [
            ""
        ]
    },
    "type": "array"
}""")

    def get(self, request, branchId, *args, **kwargs):
        """
        :param self: A TaskBranchId instance
        :param request: An HttpRequest
        :param branchId: string ID of the branch to get
        """
        try:

            result = Stubs.get__api_v1_task_branchId(request, branchId, )

            if type(result) is tuple:
                result, headers = result
            else:
                headers = {}

            # The result may contain fields with date or datetime values that will not
            # pass JSON validation. We first create the response, and then maybe validate
            # the response content against the schema.
            response = JsonResponse(result, safe=False)

            maybe_validate_result(response.content, self.GET_RESPONSE_SCHEMA)

            for key, val in headers.items():
                response[key] = val

            return response
        except ValidationError as ve:
            return HttpResponseBadRequest("Parameter validation failed: {}".format(ve.message))
        except ValueError as ve:
            return HttpResponseBadRequest("Parameter validation failed: {}".format(ve))


@method_decorator(csrf_exempt, name="dispatch")
class TaskBranchIdDateString(View):

    GET_RESPONSE_SCHEMA = json.loads("""{
    "items": {
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
        "type": "object",
        "x-scope": [
            ""
        ]
    },
    "type": "array"
}""")

    def get(self, request, branchId, dateString, *args, **kwargs):
        """
        :param self: A TaskBranchIdDateString instance
        :param request: An HttpRequest
        :param branchId: string ID of the branch to get
        :param dateString: string get all tasks from a branch on specific dates
        """
        try:

            result = Stubs.get__api_v1_task_branchId_dateString(request, branchId, dateString, )

            if type(result) is tuple:
                result, headers = result
            else:
                headers = {}

            # The result may contain fields with date or datetime values that will not
            # pass JSON validation. We first create the response, and then maybe validate
            # the response content against the schema.
            response = JsonResponse(result, safe=False)

            maybe_validate_result(response.content, self.GET_RESPONSE_SCHEMA)

            for key, val in headers.items():
                response[key] = val

            return response
        except ValidationError as ve:
            return HttpResponseBadRequest("Parameter validation failed: {}".format(ve.message))
        except ValueError as ve:
            return HttpResponseBadRequest("Parameter validation failed: {}".format(ve))


@method_decorator(csrf_exempt, name="dispatch")
class Upload(View):

    POST_RESPONSE_SCHEMA = schemas.__UNSPECIFIED__

    def post(self, request, *args, **kwargs):
        """
        :param self: A Upload instance
        :param request: An HttpRequest
        """
        try:

            form_data = {}
            upfile = request.FILES.get("upfile", None)
            form_data["upfile"] = upfile
            categoryId = request.POST.get("categoryId", None)
            # if not categoryId:
            #     return HttpResponseBadRequest("Formdata field 'categoryId' required.")
            form_data["categoryId"] = categoryId
            result = Stubs.post__api_v1_upload(request, form_data, )

            if type(result) is tuple:
                result, headers = result
            else:
                headers = {}

            # The result may contain fields with date or datetime values that will not
            # pass JSON validation. We first create the response, and then maybe validate
            # the response content against the schema.
            response = JsonResponse(result, safe=False)

            maybe_validate_result(response.content, self.POST_RESPONSE_SCHEMA)

            for key, val in headers.items():
                response[key] = val

            return response
        except ValidationError as ve:
            return HttpResponseBadRequest("Parameter validation failed: {}".format(ve.message))
        except ValueError as ve:
            return HttpResponseBadRequest("Parameter validation failed: {}".format(ve))


class __SWAGGER_SPEC__(View):

    def get(self, request, *args, **kwargs):
        spec = json.loads("""{
    "basePath": "/api/v1",
    "definitions": {
        "BranchItem": {
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
        },
        "CategoryItem": {
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
        },
        "CreateBranchItem": {
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
        },
        "CreateCategoryItem": {
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
        },
        "CreateTaskItem": {
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
        },
        "FileItem": {
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
        },
        "SearchItem": {
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
        },
        "TaskItem": {
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
        },
        "UpdateTaskItem": {
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
    },
    "host": "virtserver.swaggerhub.com",
    "info": {
        "contact": {
            "email": "you@your-company.com"
        },
        "description": "This is a simple API",
        "license": {
            "name": "Apache 2.0",
            "url": "http://www.apache.org/licenses/LICENSE-2.0.html"
        },
        "title": "Simple Inventory API",
        "version": "1.0.0"
    },
    "paths": {
        "/branch": {
            "get": {
                "description": "get branch based on roles. defaults to getting all branches\\n",
                "parameters": [],
                "produces": [
                    "application/json"
                ],
                "responses": {
                    "200": {
                        "description": "branch details and categories",
                        "schema": {
                            "items": {
                                "$ref": "#/definitions/BranchItem",
                                "x-scope": [
                                    ""
                                ]
                            },
                            "type": "array"
                        }
                    },
                    "400": {
                        "description": "bad input parameter"
                    }
                },
                "summary": "get branch details based on roles",
                "tags": [
                    "Branch"
                ]
            },
            "post": {
                "consumes": [
                    "application/json"
                ],
                "description": "Adds a new branch",
                "parameters": [
                    {
                        "description": "Branch item to add",
                        "in": "body",
                        "name": "name",
                        "required": false,
                        "schema": {
                            "$ref": "#/definitions/CreateBranchItem",
                            "x-scope": [
                                ""
                            ]
                        }
                    }
                ],
                "produces": [
                    "application/json"
                ],
                "responses": {
                    "201": {
                        "description": "item created"
                    },
                    "400": {
                        "description": "invalid input, object invalid"
                    },
                    "409": {
                        "description": "an existing item already exists"
                    }
                },
                "summary": "add a new branch",
                "tags": [
                    "Branch"
                ]
            }
        },
        "/branch/category/files": {
            "get": {
                "description": "get files from this category under a branch\\n",
                "parameters": [
                    {
                        "description": "ID of the branch",
                        "in": "query",
                        "name": "branchId",
                        "required": true,
                        "type": "string"
                    },
                    {
                        "description": "ID of the category under this branch",
                        "in": "query",
                        "name": "categoryId",
                        "required": true,
                        "type": "string"
                    },
                    {
                        "description": "ID of the file to get. if no fileId is given, will return all files",
                        "in": "query",
                        "name": "fileId",
                        "required": false,
                        "type": "string"
                    }
                ],
                "produces": [
                    "application/json"
                ],
                "responses": {
                    "200": {
                        "description": "search results matching criteria",
                        "schema": {
                            "items": {
                                "$ref": "#/definitions/FileItem",
                                "x-scope": [
                                    ""
                                ]
                            },
                            "type": "array"
                        }
                    },
                    "400": {
                        "description": "bad input parameter"
                    }
                },
                "summary": "get files under this category from this branch",
                "tags": [
                    "Branch"
                ]
            }
        },
        "/branch/category/{branchId}": {
            "get": {
                "description": "get categories from this branch\\n",
                "parameters": [
                    {
                        "description": "ID of the branch to get",
                        "in": "path",
                        "name": "branchId",
                        "required": true,
                        "type": "string"
                    }
                ],
                "produces": [
                    "application/json"
                ],
                "responses": {
                    "200": {
                        "description": "search results matching criteria",
                        "schema": {
                            "items": {
                                "$ref": "#/definitions/CategoryItem",
                                "x-scope": [
                                    ""
                                ]
                            },
                            "type": "array"
                        }
                    },
                    "400": {
                        "description": "bad input parameter"
                    }
                },
                "summary": "get categories from this branch",
                "tags": [
                    "Branch"
                ]
            },
            "post": {
                "consumes": [
                    "application/json"
                ],
                "description": "Adds a category to the branch",
                "parameters": [
                    {
                        "description": "ID of the branch to get",
                        "in": "path",
                        "name": "branchId",
                        "required": true,
                        "type": "string"
                    },
                    {
                        "description": "Category item to add",
                        "in": "body",
                        "name": "name",
                        "required": false,
                        "schema": {
                            "$ref": "#/definitions/CreateCategoryItem",
                            "x-scope": [
                                ""
                            ]
                        }
                    }
                ],
                "produces": [
                    "application/json"
                ],
                "responses": {
                    "201": {
                        "description": "item created"
                    },
                    "400": {
                        "description": "invalid input, object invalid"
                    },
                    "409": {
                        "description": "an existing item already exists"
                    }
                },
                "summary": "add a new branch category",
                "tags": [
                    "Branch"
                ]
            }
        },
        "/search": {
            "get": {
                "description": "search for files, messages and tasks given parameter\\n",
                "parameters": [
                    {
                        "description": "search string parameter.",
                        "in": "query",
                        "name": "q",
                        "required": false,
                        "type": "string"
                    }
                ],
                "produces": [
                    "application/json"
                ],
                "responses": {
                    "200": {
                        "description": "search results matching criteria",
                        "schema": {
                            "items": {
                                "$ref": "#/definitions/SearchItem",
                                "x-scope": [
                                    ""
                                ]
                            },
                            "type": "array"
                        }
                    },
                    "400": {
                        "description": "failed to search"
                    }
                },
                "summary": "Searches Tasks, Messages and Files.",
                "tags": [
                    "Misc"
                ]
            }
        },
        "/task": {
            "get": {
                "description": "get all tasks permitted by this user's role\\n",
                "parameters": [],
                "produces": [
                    "application/json"
                ],
                "responses": {
                    "200": {
                        "description": "list of tasks",
                        "schema": {
                            "items": {
                                "$ref": "#/definitions/TaskItem",
                                "x-scope": [
                                    ""
                                ]
                            },
                            "type": "array"
                        }
                    },
                    "400": {
                        "description": "bad input parameter"
                    }
                },
                "summary": "get all tasks",
                "tags": [
                    "Task"
                ]
            },
            "post": {
                "consumes": [
                    "application/json"
                ],
                "description": "Adds a new task",
                "parameters": [
                    {
                        "description": "Task item to add",
                        "in": "body",
                        "name": "name",
                        "required": false,
                        "schema": {
                            "$ref": "#/definitions/CreateTaskItem",
                            "x-scope": [
                                ""
                            ]
                        }
                    }
                ],
                "produces": [
                    "application/json"
                ],
                "responses": {
                    "201": {
                        "description": "item created"
                    },
                    "400": {
                        "description": "invalid input, object invalid"
                    },
                    "409": {
                        "description": "an existing item already exists"
                    }
                },
                "summary": "add a new task",
                "tags": [
                    "Task"
                ]
            },
            "put": {
                "consumes": [
                    "application/json"
                ],
                "description": "update a task",
                "parameters": [
                    {
                        "description": "ID of the task to update",
                        "in": "query",
                        "name": "taskId",
                        "required": true,
                        "type": "string"
                    },
                    {
                        "description": "task details to update",
                        "in": "body",
                        "name": "updateTaskBody",
                        "required": false,
                        "schema": {
                            "$ref": "#/definitions/UpdateTaskItem",
                            "x-scope": [
                                ""
                            ]
                        }
                    }
                ],
                "produces": [
                    "application/json"
                ],
                "responses": {
                    "201": {
                        "description": "item updated"
                    },
                    "400": {
                        "description": "invalid input, object invalid"
                    },
                    "409": {
                        "description": "an existing item already exists"
                    }
                },
                "summary": "update a task",
                "tags": [
                    "Task"
                ]
            }
        },
        "/task/{branchId}": {
            "get": {
                "description": "get tasks from this branch\\n",
                "parameters": [
                    {
                        "description": "ID of the branch to get",
                        "in": "path",
                        "name": "branchId",
                        "required": true,
                        "type": "string"
                    }
                ],
                "produces": [
                    "application/json"
                ],
                "responses": {
                    "200": {
                        "description": "search results matching criteria",
                        "schema": {
                            "items": {
                                "$ref": "#/definitions/TaskItem",
                                "x-scope": [
                                    ""
                                ]
                            },
                            "type": "array"
                        }
                    },
                    "400": {
                        "description": "bad input parameter"
                    }
                },
                "summary": "get tasks from this branch",
                "tags": [
                    "Task"
                ]
            }
        },
        "/task/{branchId}/{dateString}": {
            "get": {
                "description": "get tasks from this branch\\n",
                "parameters": [
                    {
                        "description": "ID of the branch to get",
                        "in": "path",
                        "name": "branchId",
                        "required": true,
                        "type": "string"
                    },
                    {
                        "description": "get all tasks from a branch on specific dates",
                        "format": "dd-mm-yyyy",
                        "in": "path",
                        "name": "dateString",
                        "required": true,
                        "type": "string"
                    }
                ],
                "produces": [
                    "application/json"
                ],
                "responses": {
                    "200": {
                        "description": "list of tasks matching criteria",
                        "schema": {
                            "items": {
                                "$ref": "#/definitions/TaskItem",
                                "x-scope": [
                                    ""
                                ]
                            },
                            "type": "array"
                        }
                    },
                    "400": {
                        "description": "bad input parameter"
                    }
                },
                "summary": "get tasks from this branch",
                "tags": [
                    "Task"
                ]
            }
        },
        "/upload": {
            "post": {
                "consumes": [
                    "multipart/form-data"
                ],
                "parameters": [
                    {
                        "description": "The file to upload.",
                        "in": "formData",
                        "name": "upfile",
                        "required": false,
                        "type": "file"
                    },
                    {
                        "description": "category under which this file belongs.",
                        "in": "formData",
                        "name": "categoryId",
                        "required": true,
                        "type": "string"
                    }
                ],
                "responses": {
                    "200": {
                        "description": "file upload success"
                    },
                    "400": {
                        "description": "failed to upload file"
                    }
                },
                "summary": "Uploads a file.",
                "tags": [
                    "Misc"
                ]
            }
        }
    },
    "schemes": [
        "http"
    ],
    "swagger": "2.0",
    "tags": [
        {
            "description": "Other operations API",
            "name": "Misc"
        },
        {
            "description": "Branch details",
            "name": "Branch"
        },
        {
            "description": "Task API",
            "name": "Task"
        }
    ]
}""")
        # Mod spec to point to demo application
        spec["basePath"] = "/api/v1"
        spec["host"] = "localhost:8000"
        # Add basic auth as a security definition
        security_definitions = spec.get("securityDefinitions", {})
        security_definitions["basic_auth"] = {"type": "basic"}
        spec["securityDefinitions"] = security_definitions
        return JsonResponse(spec)


# ---------------------- DJANGO REST ------------

from rest_framework.decorators import api_view, permission_classes,authentication_classes

from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone

from exec.models import FileComment, FileAttachment, Task
from exec.serializers import FileCommentSerializer, TaskSerializer
from commons.models import Account


@api_view(["GET"])
@csrf_exempt
@permission_classes([IsAuthenticated])
def get_comments(request, file_id):
    comments = FileComment.objects.filter(commented_file__id=file_id).order_by('created_at')
    
    serializer = FileCommentSerializer(comments, many=True)
    return JsonResponse({'comments': serializer.data}, safe=False, status=status.HTTP_200_OK)

@api_view(["POST"])
@csrf_exempt
@permission_classes([IsAuthenticated])
def add_comment(request):
    
    payload = request.data
    user = request.user
    try:
        comment = FileComment.objects.create(
            text=payload["text"],
            commented_file=FileAttachment.objects.get(id=payload["file_id"]),
            created_by=Account.objects.get(user=user)
        )
        serializer = FileCommentSerializer(comment)
        return JsonResponse({'comment': serializer.data}, safe=False, status=status.HTTP_201_CREATED)
    except ObjectDoesNotExist as e:
        return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)
    except Exception:
        return JsonResponse({'error': 'Something terrible went wrong'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

from rest_framework.authentication import SessionAuthentication, BasicAuthentication

class CsrfExemptSessionAuthentication(SessionAuthentication):
    """
    SessionAuthentication scheme used by DRF. DRF's SessionAuthentication uses
    Django's session framework for authentication which requires CSRF to be
    checked. In this case we are going to disable CSRF tokens for the API.
    """

    def enforce_csrf(self, request):
        return

@api_view(["GET", "POST"])
@authentication_classes([])
@permission_classes([])
def get_tasks(request):
    
    # data = [
    #     {
    #         "id": 1,
    #         "Subject": "test",
    #         "StartTime": timezone.now(),
    #         "EndTime": timezone.now()
    #     }
    # ]
    # return JsonResponse(data, safe=False, status=status.HTTP_200_OK)
    payload = request.data
    end_date = payload.get('EndDate', timezone.now())
    start_date = payload.get('StartDate', timezone.now())

    tasks = Task.objects.filter(end_time__lte=end_date, start_time__gte=start_date)
    
    serializer = TaskSerializer(tasks, many=True)
    return JsonResponse({"tasks":serializer.data}, safe=False, status=status.HTTP_200_OK)


import json

@api_view(["POST"])
@authentication_classes([])
@permission_classes([])
def add_task(request):
    user = request.headers['Authorization']
    print(user)
    payload = request.data
    if payload['action'] == 'batch' or payload['action'] == 'insert':
        try:
            if len(payload['added']) > 0 :
                task = Task.objects.create(
                    custom_id=payload["added"][0].get('Id',-1),
                    title=payload["added"][0].get('Subject',''),
                    description=payload["added"][0].get('Description',''),
                    location=payload["added"][0].get('Location',''),
                    start_time=payload["added"][0].get('StartTime',timezone.now()),
                    end_time=payload["added"][0].get('EndTime',timezone.now()),
                    created_by=Account.objects.get(user=user)
                )
                serializer = TaskSerializer(task)
                return JsonResponse({'task': serializer.data}, safe=False, status=status.HTTP_201_CREATED)
            if len(payload['changed']) > 0 :
                task = Task.objects.get(custom_id=payload["changed"][0]['Id'])
                if(task):
                    task.title=payload["changed"][0].get('Subject','')
                    task.description=payload["changed"][0].get('Description','')
                    task.location=payload["changed"][0].get('Location','')
                    task.start_time=payload["changed"][0].get('StartTime',timezone.now())
                    task.end_time=payload["changed"][0].get('EndTime',timezone.now())
                    task.save()
                serializer = TaskSerializer(task)
                return JsonResponse({'task': serializer.data}, safe=False, status=status.HTTP_200_OK)
        except ObjectDoesNotExist as e:
            return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return JsonResponse({'error': 'Something terrible went wrong'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
    