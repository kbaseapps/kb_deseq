import time
import json
import os
import uuid
import errno
import subprocess
import math

from DataFileUtil.DataFileUtilClient import DataFileUtil
from Workspace.WorkspaceClient import Workspace as Workspace
from KBaseReport.KBaseReportClient import KBaseReport


def log(message, prefix_newline=False):
    """Logging function, provides a hook to suppress or redirect log messages."""
    print(('\n' if prefix_newline else '') + '{0:.2f}'.format(time.time()) + ': ' + str(message))


class DESeqUtil:

    def _validate_run_deseq2_app_params(self, params):
        """
        _validate_run_deseq2_app_params:
                validates params passed to run_deseq2_app method
        """

        log('start validating run_deseq2_app params')

        # check for required parameters
        for p in ['expressionset_ref', 'diff_expression_obj_name', 'filtered_expr_matrix',
                  'workspace_name']:
            if p not in params:
                raise ValueError('"{}" parameter is required, but missing'.format(p))

    def _mkdir_p(self, path):
        """
        _mkdir_p: make directory for given path
        """
        if not path:
            return
        try:
            os.makedirs(path)
        except OSError as exc:
            if exc.errno == errno.EEXIST and os.path.isdir(path):
                pass
            else:
                raise

    def _generate_report(self, obj_ref, workspace_name):
        """
        _generate_report: generate summary report
        """
        log('creating report')
        uuid_string = str(uuid.uuid4())
        upload_message = 'Run DESeq App Finished\n\n'

        info = self.ws.get_object_info3({"objects": [{"ref": obj_ref}]})['infos'][0]

        upload_message += "Saved Differetial Expression Object: {}\n".format(info[1])

        report_params = {
              'message': upload_message,
              'workspace_name': workspace_name,
              'report_object_name': 'kb_upload_mothods_report_' + uuid_string}

        kbase_report_client = KBaseReport(self.callback_url, token=self.token)
        output = kbase_report_client.create_extended_report(report_params)

        report_output = {'report_name': output['name'], 'report_ref': output['ref']}

        return report_output

    def _get_count_matrix_file(self, expressionset_ref):
        pass

    def _generate_diff_expression_data(self, result_directory, expressionset_ref,
                                       diff_expression_obj_name, workspace_name):

        """
        _generate_diff_expression_data: generate RNASeqDifferentialExpression object data
        """
        expression_set_data = self.ws.get_objects2({'objects':
                                                   [{'ref': expressionset_ref}]})['data'][0]['data']

        diff_expression_data = {
                'tool_used': 'DESeq2',
                'tool_version': '1.16.1',
                'expressionSet_id': expressionset_ref,
                'genome_id': expression_set_data.get('genome_id'),
                'alignmentSet_id': expression_set_data.get('alignmentSet_id'),
                'sampleset_id': expression_set_data.get('sampleset_id')
        }

        handle = self.dfu.file_to_shock({'file_path': result_directory,
                                         'pack': 'zip',
                                         'make_handle': True})['handle']
        diff_expression_data.update({'file': handle})

        sample_ids = []
        diff_expression_data.update({'sample_ids': sample_ids})

        condition = []
        diff_expression_data.update({'condition': condition})

        print diff_expression_data

        return diff_expression_data

    def _save_diff_expression(self, result_directory, expressionset_ref,
                              workspace_name, diff_expression_obj_name):
        """
        _save_diff_expression: save DifferentialExpression object to workspace
        """
        log('start saving RNASeqDifferentialExpression object')
        if isinstance(workspace_name, int) or workspace_name.isdigit():
            workspace_id = workspace_name
        else:
            workspace_id = self.dfu.ws_name_to_id(workspace_name)

        diff_expression_data = self._generate_diff_expression_data(result_directory,
                                                                   expressionset_ref,
                                                                   diff_expression_obj_name,
                                                                   workspace_name)

        object_type = 'KBaseRNASeq.RNASeqDifferentialExpression'
        save_object_params = {
            'id': workspace_id,
            'objects': [{
                            'type': object_type,
                            'data': diff_expression_data,
                            'name': diff_expression_obj_name
                        }]
        }

        dfu_oi = self.dfu.save_objects(save_object_params)[0]
        diff_expression_obj_ref = str(dfu_oi[6]) + '/' + str(dfu_oi[0]) + '/' + str(dfu_oi[4])

        return diff_expression_obj_ref

    def __init__(self, config):
        self.ws_url = config["workspace-url"]
        self.callback_url = config['SDK_CALLBACK_URL']
        self.token = config['KB_AUTH_TOKEN']
        self.shock_url = config['shock-url']
        self.dfu = DataFileUtil(self.callback_url)
        self.ws = Workspace(self.ws_url, token=self.token)
        self.scratch = config['scratch']

    def run_deseq2_app(self, params):
        """
        run_deseq2_app: run DESeq2 app
        (https://www.bioconductor.org/packages/release/bioc/vignettes/DESeq2/inst/doc/DESeq2.html)

        required params:
        expressionset_ref: ExpressionSet object reference
        diff_expression_obj_name: RNASeqDifferetialExpression object name
        filtered_expr_matrix: name of output object filtered expression matrix
        workspace_name: the name of the workspace it gets saved to

        optional params:
        fold_scale_type: one of ["linear", "log2+1", "log10+1"]
        alpha_cutoff: q value cutoff
        fold_change_cutoff: fold change cutoff
        maximum_num_genes: maximum gene numbers

        return:
        result_directory: folder path that holds all files generated by run_deseq2_app
        diff_expression_obj_ref: generated RNASeqDifferetialExpression object reference
        report_name: report name generated by KBaseReport
        report_ref: report reference generated by KBaseReport
        """
        log('--->\nrunning DESeqUtil.run_deseq2_app\n' +
            'params:\n{}'.format(json.dumps(params, indent=1)))

        self._validate_run_deseq2_app_params(params)

        result_directory = os.path.join(self.scratch, str(uuid.uuid4()))
        self._mkdir_p(result_directory)

        # input files
        expressionset_ref = params.get('expressionset_ref')
        params['count_matrix_file'] = self._get_count_matrix_file(expressionset_ref)

        diff_expression_obj_ref = self._save_diff_expression(result_directory,
                                                             expressionset_ref,
                                                             params.get('workspace_name'),
                                                             params.get('diff_expression_obj_name'))

        returnVal = {'result_directory': result_directory,
                     'diff_expression_obj_ref': diff_expression_obj_ref}

        report_output = self._generate_report(diff_expression_obj_ref, params.get('workspace_name'))
        returnVal.update(report_output)

        return returnVal
