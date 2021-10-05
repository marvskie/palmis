"""
Do not modify this file. It is generated from the Swagger specification.
"""
import json
import base64
from django.db.models import Count, F, Value
from django.contrib.auth import authenticate
from django.core import serializers
from apitools.datagenerator import DataGenerator

import exec.schemas as schemas
from oauth2_provider.models import AccessToken, Application, RefreshToken

from commons.models import Organization, Branch
from exec.models import *

class AbstractStubClass(object):
    """
    Implementations need to be derived from this class.
    """

    # get__api_v1_branch -- Synchronisation point for meld
    @staticmethod
    def get__api_v1_branch(request, *args, **kwargs):
        """
        :param request: An HttpRequest
        """
        raise NotImplementedError()

    # post__api_v1_branch -- Synchronisation point for meld
    @staticmethod
    def post__api_v1_branch(request, body, *args, **kwargs):
        """
        :param request: An HttpRequest
        :param body: A dictionary containing the parsed and validated body
        :type body: dict
        """
        raise NotImplementedError()

    # get__api_v1_branch_category_branchId -- Synchronisation point for meld
    @staticmethod
    def get__api_v1_branch_category_branchId(request, branchId, *args, **kwargs):
        """
        :param request: An HttpRequest
        :param branchId: ID of the branch to get
        :type branchId: string
        """
        raise NotImplementedError()

    # post__api_v1_branch_category_branchId -- Synchronisation point for meld
    @staticmethod
    def post__api_v1_branch_category_branchId(request, body, branchId, *args, **kwargs):
        """
        :param request: An HttpRequest
        :param body: A dictionary containing the parsed and validated body
        :type body: dict
        :param branchId: ID of the branch to get
        :type branchId: string
        """
        raise NotImplementedError()

    # get__api_v1_branch_category_files -- Synchronisation point for meld
    @staticmethod
    def get__api_v1_branch_category_files(request, branchId, categoryId, fileId=None, *args, **kwargs):
        """
        :param request: An HttpRequest
        :param branchId: ID of the branch
        :type branchId: string
        :param categoryId: ID of the category under this branch
        :type categoryId: string
        :param fileId: (optional) ID of the file to get. if no fileId is given, will return all files
        :type fileId: string
        """
        raise NotImplementedError()

    # get__api_v1_search -- Synchronisation point for meld
    @staticmethod
    def get__api_v1_search(request, q=None, *args, **kwargs):
        """
        :param request: An HttpRequest
        :param q: (optional) search string parameter.
        :type q: string
        """
        raise NotImplementedError()

    # get__api_v1_task -- Synchronisation point for meld
    @staticmethod
    def get__api_v1_task(request, *args, **kwargs):
        """
        :param request: An HttpRequest
        """
        raise NotImplementedError()

    # post__api_v1_task -- Synchronisation point for meld
    @staticmethod
    def post__api_v1_task(request, body, *args, **kwargs):
        """
        :param request: An HttpRequest
        :param body: A dictionary containing the parsed and validated body
        :type body: dict
        """
        raise NotImplementedError()

    # put__api_v1_task -- Synchronisation point for meld
    @staticmethod
    def put__api_v1_task(request, body, taskId, *args, **kwargs):
        """
        :param request: An HttpRequest
        :param body: A dictionary containing the parsed and validated body
        :type body: dict
        :param taskId: ID of the task to update
        :type taskId: string
        """
        raise NotImplementedError()

    # get__api_v1_task_branchId -- Synchronisation point for meld
    @staticmethod
    def get__api_v1_task_branchId(request, branchId, *args, **kwargs):
        """
        :param request: An HttpRequest
        :param branchId: ID of the branch to get
        :type branchId: string
        """
        raise NotImplementedError()

    # get__api_v1_task_branchId_dateString -- Synchronisation point for meld
    @staticmethod
    def get__api_v1_task_branchId_dateString(request, branchId, dateString, *args, **kwargs):
        """
        :param request: An HttpRequest
        :param branchId: ID of the branch to get
        :type branchId: string
        :param dateString: get all tasks from a branch on specific dates
        :type dateString: string
        """
        raise NotImplementedError()

    # post__api_v1_upload -- Synchronisation point for meld
    @staticmethod
    def post__api_v1_upload(request, form_data, *args, **kwargs):
        """
        :param request: An HttpRequest
        :param form_data: A dictionary containing form fields and their values. In the case where the form fields refer to uploaded files, the values will be instances of `django.core.files.uploadedfile.UploadedFile`
        :type form_data: dict
        """
        raise NotImplementedError()


class MockedStubClass(AbstractStubClass):
    """
    Provides a mocked implementation of the AbstractStubClass.
    """

    @staticmethod
    def get__api_v1_branch(request, *args, **kwargs):
        """
        :param request: An HttpRequest
        """
        auth_header = request.headers.get('Authorization')
        token = auth_header.split(' ')[1]  # Removes "Basic " to isolate credentials
        user = AccessToken.objects.get(token=token)
        print(user.user.account.role.organization.pk)
       
        qs_json = serializers.serialize('json', Organization.objects.all(), fields=('pk','name',))
        return qs_json

    @staticmethod
    def post__api_v1_branch(request, body, *args, **kwargs):
        """
        :param request: An HttpRequest
        :param body: A dictionary containing the parsed and validated body
        :type body: dict
        """
        try:
            Branch.objects.create(name=body['name'])
            return json.dumps({"message":"branch created"})
        except Exception as e:
            raise ValueError(str(e))
        
    @staticmethod
    def get__api_v1_branch_category_branchId(request, branchId, *args, **kwargs):
        """
        :param request: An HttpRequest
        :param branchId: ID of the branch to get
        :type branchId: string
        """
        cats = Category.objects.filter(branch__id=int(branchId))
        qs_json = serializers.serialize('json', cats, fields=('id','name',))
        return qs_json

    @staticmethod
    def post__api_v1_branch_category_branchId(request, body, branchId, *args, **kwargs):
        """
        :param request: An HttpRequest
        :param body: A dictionary containing the parsed and validated body
        :type body: dict
        :param branchId: ID of the branch to get
        :type branchId: string
        """
        try:
            branch = Organization.objects.get(pk=int(branchId))
            created = Category.objects.create(name=body['name'], branch=branch)
            return json.dumps({"message":"new category created", "id":created.id, "name":created.name})
        except Exception as e:
            raise ValueError(str(e))

    @staticmethod
    def get__api_v1_branch_category_files(request, branchId, categoryId, fileId=None, *args, **kwargs):
        """
        :param request: An HttpRequest
        :param branchId: ID of the branch
        :type branchId: string
        :param categoryId: ID of the category under this branch
        :type categoryId: string
        :param fileId: (optional) ID of the file to get. if no fileId is given, will return all files
        :type fileId: string
        """
        try:
            branch_files = FileAttachment.objects.filter(branch__id=int(branchId),category__id=int(categoryId)).annotate(added_field=F("uploaded_by__role__name"))
            qs_json = serializers.serialize('json',branch_files,use_natural_foreign_keys=True, use_natural_primary_keys=True)
            return qs_json
        except Exception as e:
            raise ValueError(str(e))

    @staticmethod
    def get__api_v1_search(request, q=None, *args, **kwargs):
        """
        :param request: An HttpRequest
        :param q: (optional) search string parameter.
        :type q: string
        """
        try:
            branch_files = FileAttachment.objects.filter(title__contains=q)
            qs_json = serializers.serialize('json',branch_files,use_natural_foreign_keys=True, use_natural_primary_keys=True)
            return qs_json
        except Exception as e:
            raise ValueError(str(e))
        
    @staticmethod
    def get__api_v1_task(request, *args, **kwargs):
        """
        :param request: An HttpRequest
        """
        try:
            tasks = Task.objects.all()
            qs_json = serializers.serialize('json',tasks , fields=('pk','title','due_date', 'created_by', 'assigned_to', 'barnch'))
            return qs_json
        except Exception as e:
            return json.dumps({"message":str(e)}) 

    @staticmethod
    def post__api_v1_task(request, body, *args, **kwargs):
        """
        :param request: An HttpRequest
        :param body: A dictionary containing the parsed and validated body
        :type body: dict
        """
        # try:
        #     branch = Branch.objects.get(pk=int(branchId))
        #     Task.objects.create(title=body['title'], branch=branch)
        #     return json.dumps({"message":"new category created"})
        # except Exception as e:
        #     return json.dumps({"message":str(e)})
        pass
    @staticmethod
    def put__api_v1_task(request, body, taskId, *args, **kwargs):
        """
        :param request: An HttpRequest
        :param body: A dictionary containing the parsed and validated body
        :type body: dict
        :param taskId: ID of the task to update
        :type taskId: string
        """
        
        return MockedStubClass.GENERATOR.random_value(response_schema)

    @staticmethod
    def get__api_v1_task_branchId(request, branchId, *args, **kwargs):
        """
        :param request: An HttpRequest
        :param branchId: ID of the branch to get
        :type branchId: string
        """
        
        return MockedStubClass.GENERATOR.random_value(response_schema)

    @staticmethod
    def get__api_v1_task_branchId_dateString(request, branchId, dateString, *args, **kwargs):
        """
        :param request: An HttpRequest
        :param branchId: ID of the branch to get
        :type branchId: string
        :param dateString: get all tasks from a branch on specific dates
        :type dateString: string
        """
        

        return MockedStubClass.GENERATOR.random_value(response_schema)

    @staticmethod
    def post__api_v1_upload(request, form_data, *args, **kwargs):
        """
        :param request: An HttpRequest
        :param form_data: A dictionary containing form fields and their values. In the case where the form fields refer to uploaded files, the values will be instances of `django.core.files.uploadedfile.UploadedFile`
        :type form_data: dict
        """
        try:
            auth_header = request.headers.get('Authorization')
            token = auth_header.split(' ')[1]  # Removes "Basic " to isolate credentials
            
            user = AccessToken.objects.get(token=token)
            category = Category.objects.get(id=form_data['categoryId'])
        
            uploaded_by = Account.objects.get(user=user.user)
            branch = uploaded_by.role.organization

            upfile = form_data['upfile']
            uploaded = FileAttachment.objects.create(title=str(upfile), file=upfile, branch=branch, category=category, uploaded_by=uploaded_by)
        
            return json.dumps({"message":"File Uploaded", "id":uploaded.id,"title":uploaded.title, "path":uploaded.file.url})
        except Exception as e:
            raise ValueError(str(e))