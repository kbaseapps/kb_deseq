# -*- coding: utf-8 -*-
import unittest
import os  # noqa: F401
import json  # noqa: F401
import time
import requests  # noqa: F401

from os import environ
try:
    from ConfigParser import ConfigParser  # py2
except:
    from configparser import ConfigParser  # py3

from pprint import pprint  # noqa: F401

from biokbase.workspace.client import Workspace as workspaceService
from kb_deseq.kb_deseqImpl import kb_deseq
from kb_deseq.kb_deseqServer import MethodContext
from kb_deseq.authclient import KBaseAuth as _KBaseAuth


class kb_deseqTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        token = environ.get('KB_AUTH_TOKEN', None)
        config_file = environ.get('KB_DEPLOYMENT_CONFIG', None)
        cls.cfg = {}
        config = ConfigParser()
        config.read(config_file)
        for nameval in config.items('kb_deseq'):
            cls.cfg[nameval[0]] = nameval[1]
        # Getting username from Auth profile for token
        authServiceUrl = cls.cfg['auth-service-url']
        auth_client = _KBaseAuth(authServiceUrl)
        user_id = auth_client.get_user(token)
        # WARNING: don't call any logging methods on the context object,
        # it'll result in a NoneType error
        cls.ctx = MethodContext(None)
        cls.ctx.update({'token': token,
                        'user_id': user_id,
                        'provenance': [
                            {'service': 'kb_deseq',
                             'method': 'please_never_use_it_in_production',
                             'method_params': []
                             }],
                        'authenticated': 1})
        cls.wsURL = cls.cfg['workspace-url']
        cls.wsClient = workspaceService(cls.wsURL)
        cls.serviceImpl = kb_deseq(cls.cfg)
        cls.scratch = cls.cfg['scratch']
        cls.callback_url = os.environ['SDK_CALLBACK_URL']

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'wsName'):
            cls.wsClient.delete_workspace({'workspace': cls.wsName})
            print('Test workspace was deleted')

    def getWsClient(self):
        return self.__class__.wsClient

    def getWsName(self):
        if hasattr(self.__class__, 'wsName'):
            return self.__class__.wsName
        suffix = int(time.time() * 1000)
        wsName = "test_kb_deseq_" + str(suffix)
        ret = self.getWsClient().create_workspace({'workspace': wsName})  # noqa
        self.__class__.wsName = wsName
        return wsName

    def getImpl(self):
        return self.__class__.serviceImpl

    def getContext(self):
        return self.__class__.ctx

    def test_bad_run_deseq2_app_params(self):
        invalidate_input_params = {
          'missing_expressionset_ref': 'expressionset_ref',
          'diff_expression_obj_name': 'diff_expression_obj_name',
          'filtered_expr_matrix': 'filtered_expr_matrix',
          'workspace_name': 'workspace_name'
        }
        with self.assertRaisesRegexp(
                    ValueError, '"expressionset_ref" parameter is required, but missing'):
            self.getImpl().run_deseq2_app(self.getContext(), invalidate_input_params)

        invalidate_input_params = {
          'expressionset_ref': 'expressionset_ref',
          'missing_diff_expression_obj_name': 'diff_expression_obj_name',
          'filtered_expr_matrix': 'filtered_expr_matrix',
          'workspace_name': 'workspace_name'
        }
        with self.assertRaisesRegexp(
                    ValueError, '"diff_expression_obj_name" parameter is required, but missing'):
            self.getImpl().run_deseq2_app(self.getContext(), invalidate_input_params)

        invalidate_input_params = {
          'expressionset_ref': 'expressionset_ref',
          'diff_expression_obj_name': 'diff_expression_obj_name',
          'missing_filtered_expr_matrix': 'filtered_expr_matrix',
          'workspace_name': 'workspace_name'
        }
        with self.assertRaisesRegexp(
                    ValueError, '"filtered_expr_matrix" parameter is required, but missing'):
            self.getImpl().run_deseq2_app(self.getContext(), invalidate_input_params)

        invalidate_input_params = {
          'expressionset_ref': 'expressionset_ref',
          'diff_expression_obj_name': 'diff_expression_obj_name',
          'filtered_expr_matrix': 'filtered_expr_matrix',
          'missing_workspace_name': 'workspace_name'
        }
        with self.assertRaisesRegexp(
                    ValueError, '"workspace_name" parameter is required, but missing'):
            self.getImpl().run_deseq2_app(self.getContext(), invalidate_input_params)
