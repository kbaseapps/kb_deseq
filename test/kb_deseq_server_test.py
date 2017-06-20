# -*- coding: utf-8 -*-
import unittest
import os  # noqa: F401
import json  # noqa: F401
import time
import requests  # noqa: F401
import csv

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
from kb_deseq.Utils.DESeqUtil import DESeqUtil


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

        cls.deseq_runner = DESeqUtil(cls.cfg)
        cls.prepare_data()

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'wsName'):
            cls.wsClient.delete_workspace({'workspace': cls.wsName})
            print('Test workspace was deleted')

    @classmethod
    def prepare_data(cls):
        # input_file = 'samExample.sam'
        # input_file_path = os.path.join(cls.scratch, input_file)
        # shutil.copy(os.path.join("data", input_file), input_file_path)

        cls.expressionset_ref = '15206/177/1'
        cls.expressionset_ref = '2409/141/1'

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
          'filtered_expression_matrix_name': 'filtered_expression_matrix_name',
          'workspace_name': 'workspace_name',
          'alpha_cutoff': 'alpha_cutoff',
          'fold_change_cutoff': 'fold_change_cutoff',
          'condition_labels': 'condition_labels'
        }
        with self.assertRaisesRegexp(
                    ValueError, '"expressionset_ref" parameter is required, but missing'):
            self.getImpl().run_deseq2_app(self.getContext(), invalidate_input_params)

        invalidate_input_params = {
          'expressionset_ref': 'expressionset_ref',
          'missing_diff_expression_obj_name': 'diff_expression_obj_name',
          'filtered_expression_matrix_name': 'filtered_expression_matrix_name',
          'workspace_name': 'workspace_name',
          'alpha_cutoff': 'alpha_cutoff',
          'fold_change_cutoff': 'fold_change_cutoff',
          'condition_labels': 'condition_labels'
        }
        with self.assertRaisesRegexp(
                    ValueError, '"diff_expression_obj_name" parameter is required, but missing'):
            self.getImpl().run_deseq2_app(self.getContext(), invalidate_input_params)

        invalidate_input_params = {
          'expressionset_ref': 'expressionset_ref',
          'diff_expression_obj_name': 'diff_expression_obj_name',
          'missing_filtered_expression_matrix_name': 'filtered_expression_matrix_name',
          'workspace_name': 'workspace_name',
          'alpha_cutoff': 'alpha_cutoff',
          'fold_change_cutoff': 'fold_change_cutoff',
          'condition_labels': 'condition_labels'
        }
        with self.assertRaisesRegexp(
                    ValueError, '"filtered_expression_matrix_name" parameter is required, but missing'):
            self.getImpl().run_deseq2_app(self.getContext(), invalidate_input_params)

        invalidate_input_params = {
          'expressionset_ref': 'expressionset_ref',
          'diff_expression_obj_name': 'diff_expression_obj_name',
          'filtered_expression_matrix_name': 'filtered_expression_matrix_name',
          'missing_workspace_name': 'workspace_name',
          'alpha_cutoff': 'alpha_cutoff',
          'fold_change_cutoff': 'fold_change_cutoff',
          'condition_labels': 'condition_labels'
        }
        with self.assertRaisesRegexp(
                    ValueError, '"workspace_name" parameter is required, but missing'):
            self.getImpl().run_deseq2_app(self.getContext(), invalidate_input_params)

        invalidate_input_params = {
          'expressionset_ref': 'expressionset_ref',
          'diff_expression_obj_name': 'diff_expression_obj_name',
          'filtered_expression_matrix_name': 'filtered_expression_matrix_name',
          'workspace_name': 'workspace_name',
          'missing_alpha_cutoff': 'alpha_cutoff',
          'fold_change_cutoff': 'fold_change_cutoff',
          'condition_labels': 'condition_labels'
        }
        with self.assertRaisesRegexp(
                    ValueError, '"alpha_cutoff" parameter is required, but missing'):
            self.getImpl().run_deseq2_app(self.getContext(), invalidate_input_params)

        invalidate_input_params = {
          'expressionset_ref': 'expressionset_ref',
          'diff_expression_obj_name': 'diff_expression_obj_name',
          'filtered_expression_matrix_name': 'filtered_expression_matrix_name',
          'workspace_name': 'workspace_name',
          'alpha_cutoff': 'alpha_cutoff',
          'missing_fold_change_cutoff': 'fold_change_cutoff',
          'condition_labels': 'condition_labels'
        }
        with self.assertRaisesRegexp(
                    ValueError, '"fold_change_cutoff" parameter is required, but missing'):
            self.getImpl().run_deseq2_app(self.getContext(), invalidate_input_params)

        invalidate_input_params = {
          'expressionset_ref': 'expressionset_ref',
          'diff_expression_obj_name': 'diff_expression_obj_name',
          'filtered_expression_matrix_name': 'filtered_expression_matrix_name',
          'workspace_name': 'workspace_name',
          'alpha_cutoff': 'alpha_cutoff',
          'fold_change_cutoff': 'fold_change_cutoff',
          'missing_condition_labels': 'condition_labels'
        }
        with self.assertRaisesRegexp(
                    ValueError, '"condition_labels" parameter is required, but missing'):
            self.getImpl().run_deseq2_app(self.getContext(), invalidate_input_params)

    def test_run_deseq2_app(self):

        input_params = {
            'expressionset_ref': self.expressionset_ref,
            'diff_expression_obj_name': 'MyDiffExpression',
            'filtered_expression_matrix_name': 'MyFilteredExprMatrix',
            'workspace_name': self.getWsName(),
            "alpha_cutoff": 0.05,
            "fold_change_cutoff": 1.5,
            'condition_labels': ['WT', 'hy5'],
            "fold_scale_type": 'log2',
        }

        result = self.getImpl().run_deseq2_app(self.getContext(), input_params)[0]

        self.assertTrue('result_directory' in result)
        result_files = os.listdir(result['result_directory'])
        print result_files
        expect_result_files = ['gene_count_matrix.csv', 'transcript_count_matrix.csv',
                               'deseq2_MAplot.png', 'PCA_MAplot.png',
                               'qvaluesPlot.png', 'pvaluesPlot.png',
                               'gene_results.csv',  'diff_genes.csv', 'sig_genes_results.csv',
                               'sig_genes_down_regulated.txt', 'sig_genes_up_regulated.txt']
        self.assertTrue(all(x in result_files for x in expect_result_files))
        with open(os.path.join(result['result_directory'], 'gene_count_matrix.csv'), "rb") as f:
            reader = csv.reader(f)
            columns = reader.next()[1:]
        expect_columns = ['WT_rep1_hisat2_stringtie_expression',
                          'WT_rep2_hisat2_stringtie_expression',
                          'hy5_rep1_hisat2_stringtie_expression',
                          'hy5_rep2_hisat2_stringtie_expression']
        self.assertItemsEqual(expect_columns, columns)
        self.assertTrue('diff_expression_obj_ref' in result)
        self.assertTrue('filtered_expression_matrix_ref' in result)
        self.assertTrue('report_name' in result)
        self.assertTrue('report_ref' in result)

    # def test_run_deseq2_app_partial_conditions(self):

    #     input_params = {
    #         'expressionset_ref': self.expressionset_ref,
    #         'diff_expression_obj_name': 'MyDiffExpression',
    #         'filtered_expression_matrix_name': 'MyFilteredExprMatrix',
    #         'workspace_name': self.getWsName(),
    #         'num_threads': 4,
    #         "fold_scale_type": 'log2',
    #         "alpha_cutoff": 0.5,
    #         "fold_change_cutoff": 1.5,
    #         'maximum_num_genes': 50,
    #         'condition_labels': ['hy5']
    #     }

    #     result = self.getImpl().run_deseq2_app(self.getContext(), input_params)[0]

    #     self.assertTrue('result_directory' in result)
    #     result_files = os.listdir(result['result_directory'])
    #     print result_files
    #     expect_result_files = ['gene_count_matrix.csv', 'transcript_count_matrix.csv',
    #                            'deseq2_MAplot.png', 'PCA_MAplot.png',
    #                            'qvaluesPlot.png', 'pvaluesPlot.png',
    #                            'gene_results.csv',  'diff_genes.csv', 'sig_genes_results.csv',
    #                            'sig_genes_down_regulated.txt', 'sig_genes_up_regulated.txt']
    #     self.assertTrue(all(x in result_files for x in expect_result_files))
    #     self.assertTrue('diff_expression_obj_ref' in result)
    #     self.assertTrue('filtered_expression_matrix_ref' in result)
    #     self.assertTrue('report_name' in result)
    #     self.assertTrue('report_ref' in result)
