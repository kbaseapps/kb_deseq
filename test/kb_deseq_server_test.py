# -*- coding: utf-8 -*-
import unittest
import os  # noqa: F401
import json  # noqa: F401
import time
import requests  # noqa: F401
import csv
import shutil

from os import environ
try:
    from ConfigParser import ConfigParser  # py2
except:
    from configparser import ConfigParser  # py3

from pprint import pprint  # noqa: F401

from biokbase.workspace.client import Workspace as workspaceService
from Workspace.WorkspaceClient import Workspace as Workspace
from kb_deseq.kb_deseqImpl import kb_deseq
from kb_deseq.kb_deseqServer import MethodContext
from kb_deseq.authclient import KBaseAuth as _KBaseAuth
from kb_deseq.Utils.DESeqUtil import DESeqUtil
from GenomeFileUtil.GenomeFileUtilClient import GenomeFileUtil
from ReadsUtils.ReadsUtilsClient import ReadsUtils
from ReadsAlignmentUtils.ReadsAlignmentUtilsClient import ReadsAlignmentUtils
from DataFileUtil.DataFileUtilClient import DataFileUtil
from kb_stringtie.kb_stringtieClient import kb_stringtie


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
        cls.ws = Workspace(cls.wsURL, token=token)
        cls.serviceImpl = kb_deseq(cls.cfg)
        cls.scratch = cls.cfg['scratch']
        cls.callback_url = os.environ['SDK_CALLBACK_URL']

        cls.gfu = GenomeFileUtil(cls.callback_url)
        cls.dfu = DataFileUtil(cls.callback_url)
        cls.ru = ReadsUtils(cls.callback_url)
        cls.rau = ReadsAlignmentUtils(cls.callback_url, service_ver='dev')
        cls.stringtie = kb_stringtie(cls.callback_url, service_ver='dev')

        cls.deseq_runner = DESeqUtil(cls.cfg)

        suffix = int(time.time() * 1000)
        cls.wsName = "test_kb_stringtie_" + str(suffix)
        cls.wsClient.create_workspace({'workspace': cls.wsName})

        cls.prepare_data()

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'wsName'):
            cls.wsClient.delete_workspace({'workspace': cls.wsName})
            print('Test workspace was deleted')

    @classmethod
    def prepare_data(cls):
        # # upload genome object
        # genbank_file_name = 'minimal.gbff'
        # genbank_file_path = os.path.join(cls.scratch, genbank_file_name)
        # shutil.copy(os.path.join('data', genbank_file_name), genbank_file_path)

        # genome_object_name = 'test_Genome'
        # cls.genome_ref = cls.gfu.genbank_to_genome({'file': {'path': genbank_file_path},
        #                                             'workspace_name': cls.wsName,
        #                                             'genome_name': genome_object_name
        #                                             })['genome_ref']

        # # upload reads object
        # reads_file_name = 'SE_reads.fastq'
        # reads_file_path = os.path.join(cls.scratch, reads_file_name)
        # shutil.copy(os.path.join('data', reads_file_name), reads_file_path)

        # reads_object_name_1 = 'test_Reads_1'
        # cls.reads_ref_1 = cls.ru.upload_reads({'fwd_file': reads_file_path,
        #                                        'wsname': cls.wsName,
        #                                        'sequencing_tech': 'Unknown',
        #                                        'interleaved': 0,
        #                                        'name': reads_object_name_1
        #                                        })['obj_ref']

        # reads_object_name_2 = 'test_Reads_2'
        # cls.reads_ref_2 = cls.ru.upload_reads({'fwd_file': reads_file_path,
        #                                        'wsname': cls.wsName,
        #                                        'sequencing_tech': 'Unknown',
        #                                        'interleaved': 0,
        #                                        'name': reads_object_name_2
        #                                        })['obj_ref']

        # reads_object_name_3 = 'test_Reads_3'
        # cls.reads_ref_3 = cls.ru.upload_reads({'fwd_file': reads_file_path,
        #                                        'wsname': cls.wsName,
        #                                        'sequencing_tech': 'Unknown',
        #                                        'interleaved': 0,
        #                                        'name': reads_object_name_3
        #                                        })['obj_ref']

        # # upload alignment object
        # alignment_file_name = 'accepted_hits.bam'
        # # alignment_file_name = 'Ath_WT_R1.fastq.sorted.bam'
        # alignment_file_path = os.path.join(cls.scratch, alignment_file_name)
        # shutil.copy(os.path.join('data', alignment_file_name), alignment_file_path)

        # alignment_object_name_1 = 'test_Alignment_1'
        # cls.condition_1 = 'test_condition_1'
        # cls.alignment_ref_1 = cls.rau.upload_alignment(
        #                            {'file_path': alignment_file_path,
        #                             'destination_ref': cls.wsName + '/' + alignment_object_name_1,
        #                             'read_library_ref': cls.reads_ref_1,
        #                             'condition':  cls.condition_1,
        #                             'library_type': 'single_end',
        #                             'assembly_or_genome_ref': cls.genome_ref
        #                             })['obj_ref']

        # alignment_object_name_2 = 'test_Alignment_2'
        # cls.condition_2 = 'test_condition_2'
        # cls.alignment_ref_2 = cls.rau.upload_alignment(
        #                            {'file_path': alignment_file_path,
        #                             'destination_ref': cls.wsName + '/' + alignment_object_name_2,
        #                             'read_library_ref': cls.reads_ref_2,
        #                             'condition':  cls.condition_2,
        #                             'library_type': 'single_end',
        #                             'assembly_or_genome_ref': cls.genome_ref
        #                             })['obj_ref']

        # alignment_object_name_3 = 'test_Alignment_3'
        # cls.condition_3 = 'test_condition_3'
        # cls.alignment_ref_3 = cls.rau.upload_alignment(
        #                            {'file_path': alignment_file_path,
        #                             'destination_ref': cls.wsName + '/' + alignment_object_name_3,
        #                             'read_library_ref': cls.reads_ref_3,
        #                             'condition':  cls.condition_3,
        #                             'library_type': 'single_end',
        #                             'assembly_or_genome_ref': cls.genome_ref,
        #                             'library_type': 'single_end'
        #                             })['obj_ref']

        # # upload sample_set object
        # workspace_id = cls.dfu.ws_name_to_id(cls.wsName)
        # sample_set_object_name = 'test_Sample_Set'
        # sample_set_data = {
        #             'sampleset_id': sample_set_object_name,
        #             'sampleset_desc': 'test sampleset object',
        #             'Library_type': 'SingleEnd',
        #             'condition': [cls.condition_1, cls.condition_2, cls.condition_3],
        #             'domain': 'Unknown',
        #             'num_samples': 3,
        #             'platform': 'Unknown'}
        # save_object_params = {
        #     'id': workspace_id,
        #     'objects': [{
        #                     'type': 'KBaseRNASeq.RNASeqSampleSet',
        #                     'data': sample_set_data,
        #                     'name': sample_set_object_name
        #                 }]
        # }

        # dfu_oi = cls.dfu.save_objects(save_object_params)[0]
        # cls.sample_set_ref = str(dfu_oi[6]) + '/' + str(dfu_oi[0]) + '/' + str(dfu_oi[4])

        # # upload alignment_set object
        # object_type = 'KBaseRNASeq.RNASeqAlignmentSet'
        # alignment_set_object_name = 'test_Alignment_Set'
        # alignment_set_data = {
        #             'genome_id': cls.genome_ref,
        #             'read_sample_ids': [reads_object_name_1,
        #                                 reads_object_name_2,
        #                                 reads_object_name_3],
        #             'mapped_rnaseq_alignments': [{reads_object_name_1: alignment_object_name_1},
        #                                          {reads_object_name_2: alignment_object_name_2},
        #                                          {reads_object_name_3: alignment_object_name_3}],
        #             'mapped_alignments_ids': [{reads_object_name_1: cls.alignment_ref_1},
        #                                       {reads_object_name_2: cls.alignment_ref_2},
        #                                       {reads_object_name_3: cls.alignment_ref_3}],
        #             'sample_alignments': [cls.alignment_ref_1,
        #                                   cls.alignment_ref_2,
        #                                   cls.alignment_ref_3],
        #             'sampleset_id': cls.sample_set_ref}
        # save_object_params = {
        #     'id': workspace_id,
        #     'objects': [{
        #                     'type': object_type,
        #                     'data': alignment_set_data,
        #                     'name': alignment_set_object_name
        #                 }]
        # }

        # dfu_oi = cls.dfu.save_objects(save_object_params)[0]
        # cls.alignment_set_ref = str(dfu_oi[6]) + '/' + str(dfu_oi[0]) + '/' + str(dfu_oi[4])

        # # upload expression_set object
        # cls.expressionset_ref = cls.stringtie.run_stringtie_app(
        #                                 {'alignment_object_ref': cls.alignment_set_ref,
        #                                  'workspace_name': cls.wsName,
        #                                  "min_read_coverage": 2.5,
        #                                  "junction_base": 10,
        #                                  "num_threads": 3,
        #                                  "min_isoform_abundance": 0.1,
        #                                  "min_length": 200,
        #                                  "skip_reads_with_no_ref": 1,
        #                                  "merge": 0,
        #                                  "junction_coverage": 1,
        #                                  "ballgown_mode": 1,
        #                                  "min_locus_gap_sep_value": 50,
        #                                  "disable_trimming": 1})['expression_obj_ref']

        cls.expressionset_ref = '15206/242/1'
        cls.condition_1 = 'WT'
        cls.condition_2 = 'hy5'

    def getWsClient(self):
        return self.__class__.wsClient

    def getWsName(self):
        return self.__class__.wsName

    def getImpl(self):
        return self.__class__.serviceImpl

    def getContext(self):
        return self.__class__.ctx

    # def test_bad_run_deseq2_app_params(self):
    #     invalidate_input_params = {
    #       'missing_expressionset_ref': 'expressionset_ref',
    #       'diff_expression_obj_name': 'diff_expression_obj_name',
    #       'workspace_name': 'workspace_name',
    #       'alpha_cutoff': 'alpha_cutoff',
    #       'fold_change_cutoff': 'fold_change_cutoff',
    #       'condition_labels': 'condition_labels'
    #     }
    #     with self.assertRaisesRegexp(
    #                 ValueError, '"expressionset_ref" parameter is required, but missing'):
    #         self.getImpl().run_deseq2_app(self.getContext(), invalidate_input_params)

    #     invalidate_input_params = {
    #       'expressionset_ref': 'expressionset_ref',
    #       'missing_diff_expression_obj_name': 'diff_expression_obj_name',
    #       'workspace_name': 'workspace_name',
    #       'alpha_cutoff': 'alpha_cutoff',
    #       'fold_change_cutoff': 'fold_change_cutoff',
    #       'condition_labels': 'condition_labels'
    #     }
    #     with self.assertRaisesRegexp(
    #                 ValueError, '"diff_expression_obj_name" parameter is required, but missing'):
    #         self.getImpl().run_deseq2_app(self.getContext(), invalidate_input_params)

    #     invalidate_input_params = {
    #       'expressionset_ref': 'expressionset_ref',
    #       'diff_expression_obj_name': 'diff_expression_obj_name',
    #       'missing_workspace_name': 'workspace_name',
    #       'alpha_cutoff': 'alpha_cutoff',
    #       'fold_change_cutoff': 'fold_change_cutoff',
    #       'condition_labels': 'condition_labels'
    #     }
    #     with self.assertRaisesRegexp(
    #                 ValueError, '"workspace_name" parameter is required, but missing'):
    #         self.getImpl().run_deseq2_app(self.getContext(), invalidate_input_params)

    #     invalidate_input_params = {
    #       'expressionset_ref': 'expressionset_ref',
    #       'diff_expression_obj_name': 'diff_expression_obj_name',
    #       'workspace_name': 'workspace_name',
    #       'missing_alpha_cutoff': 'alpha_cutoff',
    #       'fold_change_cutoff': 'fold_change_cutoff',
    #       'condition_labels': 'condition_labels'
    #     }
    #     with self.assertRaisesRegexp(
    #                 ValueError, '"alpha_cutoff" parameter is required, but missing'):
    #         self.getImpl().run_deseq2_app(self.getContext(), invalidate_input_params)

    #     invalidate_input_params = {
    #       'expressionset_ref': 'expressionset_ref',
    #       'diff_expression_obj_name': 'diff_expression_obj_name',
    #       'workspace_name': 'workspace_name',
    #       'alpha_cutoff': 'alpha_cutoff',
    #       'missing_fold_change_cutoff': 'fold_change_cutoff',
    #       'condition_labels': 'condition_labels'
    #     }
    #     with self.assertRaisesRegexp(
    #                 ValueError, '"fold_change_cutoff" parameter is required, but missing'):
    #         self.getImpl().run_deseq2_app(self.getContext(), invalidate_input_params)

    #     invalidate_input_params = {
    #       'expressionset_ref': 'expressionset_ref',
    #       'diff_expression_obj_name': 'diff_expression_obj_name',
    #       'workspace_name': 'workspace_name',
    #       'alpha_cutoff': 'alpha_cutoff',
    #       'fold_change_cutoff': 'fold_change_cutoff',
    #       'missing_condition_labels': 'condition_labels'
    #     }
    #     with self.assertRaisesRegexp(
    #                 ValueError, '"condition_labels" parameter is required, but missing'):
    #         self.getImpl().run_deseq2_app(self.getContext(), invalidate_input_params)

    # def test_run_deseq2_app(self):

    #     input_params = {
    #         'expressionset_ref': self.expressionset_ref,
    #         'diff_expression_obj_name': 'MyDiffExpression',
    #         'workspace_name': self.getWsName(),
    #         "alpha_cutoff": 0.05,
    #         "fold_change_cutoff": 1.5,
    #         'condition_labels': [self.condition_1, self.condition_2, self.condition_3],
    #         "fold_scale_type": 'log2'
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
    #     with open(os.path.join(result['result_directory'], 'gene_count_matrix.csv'), "rb") as f:
    #         reader = csv.reader(f)
    #         columns = reader.next()[1:]
    #     expect_columns = ['test_stringtie_expression_1',
    #                       'test_stringtie_expression_2',
    #                       'test_stringtie_expression_3']
    #     self.assertItemsEqual(expect_columns, columns)
    #     self.assertTrue('diff_expression_obj_ref' in result)
    #     diff_expression_data = self.ws.get_objects2({
    #                 'objects': [{'ref': result.get('diff_expression_obj_ref')}]})['data'][0]['data']
    #     print diff_expression_data
    #     self.assertTrue('report_name' in result)
    #     self.assertTrue('report_ref' in result)

    def test_run_deseq2_app_partial_conditions(self):

        input_params = {
            'expressionset_ref': self.expressionset_ref,
            'diff_expression_obj_name': 'MyDiffExpression',
            'workspace_name': self.getWsName(),
            "alpha_cutoff": 1,
            "fold_change_cutoff": 0,
            'condition_labels': [self.condition_1, self.condition_2],
            "fold_scale_type": 'log2'
        }

        result = self.getImpl().run_deseq2_app(self.getContext(), input_params)[0]

        self.assertTrue('result_directory' in result)
        result_files = os.listdir(result['result_directory'])
        print result_files
        expect_result_files = ['gene_count_matrix.csv', 'transcript_count_matrix.csv',
                               'deseq2_MAplot.png', 'PCA_MAplot.png',
                               'qvaluesPlot.png', 'pvaluesPlot.png',
                               'gene_results.csv', 'diff_genes.csv', 'sig_genes_results.csv',
                               'sig_genes_down_regulated.txt', 'sig_genes_up_regulated.txt']
        self.assertTrue(all(x in result_files for x in expect_result_files))
        with open(os.path.join(result['result_directory'], 'gene_count_matrix.csv'), "rb") as f:
            reader = csv.reader(f)
            columns = reader.next()[1:]
        # expect_columns = ['test_stringtie_expression_1',
        #                   'test_stringtie_expression_2']
        # self.assertItemsEqual(expect_columns, columns)

        self.assertTrue('diff_expression_obj_ref' in result)
        diff_expr_obj_ref = result.get('diff_expression_obj_ref')
        diff_expr_data = self.ws.get_objects2({'objects': 
                                              [{'ref': diff_expr_obj_ref}]})['data'][0]['data']
        # print diff_expr_data
        self.assertTrue('report_name' in result)
        self.assertTrue('report_ref' in result)
