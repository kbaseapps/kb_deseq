import time
import json
import os
import uuid
import errno
import subprocess
import zipfile
import shutil

from DataFileUtil.DataFileUtilClient import DataFileUtil
from Workspace.WorkspaceClient import Workspace as Workspace
from KBaseReport.KBaseReportClient import KBaseReport
from ReadsAlignmentUtils.ReadsAlignmentUtilsClient import ReadsAlignmentUtils


def log(message, prefix_newline=False):
    """Logging function, provides a hook to suppress or redirect log messages."""
    print(('\n' if prefix_newline else '') + '{0:.2f}'.format(time.time()) + ': ' + str(message))


class DESeqUtil:

    PREPDE_TOOLKIT_PATH = '/kb/deployment/bin/prepDE'

    def _validate_run_deseq2_app_params(self, params):
        """
        _validate_run_deseq2_app_params:
                validates params passed to run_deseq2_app method
        """

        log('start validating run_deseq2_app params')

        # check for required parameters
        for p in ['expressionset_ref', 'diff_expression_obj_name',
                  'filtered_expression_matrix_name', 'workspace_name']:
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

    def _run_command(self, command):
        """
        _run_command: run command and print result
        """
        log('Start executing command:\n{}'.format(command))
        pipe = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        output = pipe.communicate()[0]
        exitCode = pipe.returncode

        if (exitCode == 0):
            log('Executed commend:\n{}\n'.format(command) +
                'Exit Code: {}\nOutput:\n{}'.format(exitCode, output))
        else:
            error_msg = 'Error running commend:\n{}\n'.format(command)
            error_msg += 'Exit Code: {}\nOutput:\n{}'.format(exitCode, output)
            raise ValueError(error_msg)

    def _generate_html_report(self, result_directory, diff_expression_obj_ref,
                              filtered_expression_matrix_ref, params):
        """
        _generate_html_report: generate html summary report
        """

        log('start generating html report')
        html_report = list()

        output_directory = os.path.join(self.scratch, str(uuid.uuid4()))
        self._mkdir_p(output_directory)
        result_file_path = os.path.join(output_directory, 'report.html')

        shutil.copy2(os.path.join(result_directory, 'deseq2_MAplot.png'),
                     os.path.join(output_directory, 'dispersion_plots.png'))
        shutil.copy2(os.path.join(result_directory, 'PCA_MAplot.png'),
                     os.path.join(output_directory, 'PCA_plots.png'))
        shutil.copy2(os.path.join(result_directory, 'pvaluesPlot.png'),
                     os.path.join(output_directory, 'pvalues_plots.png'))
        shutil.copy2(os.path.join(result_directory, 'qvaluesPlot.png'),
                     os.path.join(output_directory, 'qvalues_plots.png'))

        overview_content = ''
        overview_content += '<p>Generated Differential Expression: {}({})</p>'.format(
            params.get('diff_expression_obj_name'), diff_expression_obj_ref)
        overview_content += '<p>Generated Expression Matrix: {}({})</p>'.format(
            params.get('filtered_expression_matrix_name'), filtered_expression_matrix_ref)

        with open(result_file_path, 'w') as result_file:
            with open(os.path.join(os.path.dirname(__file__), 'report_template.html'),
                      'r') as report_template_file:
                report_template = report_template_file.read()
                report_template = report_template.replace('<p>Overview_Content</p>',
                                                          overview_content)
                result_file.write(report_template)

        report_shock_id = self.dfu.file_to_shock({'file_path': output_directory,
                                                  'pack': 'zip'})['shock_id']

        html_report.append({'shock_id': report_shock_id,
                            'name': os.path.basename(result_file_path),
                            'label': os.path.basename(result_file_path),
                            'description': 'HTML summary report for DESeq2 App'})
        return html_report

    def _generate_output_file_list(self, result_directory):
        """
        _generate_output_file_list: zip result files and generate file_links for report
        """
        log('Start packing result files')
        output_files = list()

        output_directory = os.path.join(self.scratch, str(uuid.uuid4()))
        self._mkdir_p(output_directory)
        result_file = os.path.join(output_directory, 'DESeq2_result.zip')
        plot_file = os.path.join(output_directory, 'DESeq2_plot.zip')

        with zipfile.ZipFile(result_file, 'w',
                             zipfile.ZIP_DEFLATED,
                             allowZip64=True) as zip_file:
            for root, dirs, files in os.walk(result_directory):
                for file in files:
                    if not (file.endswith('.zip') or
                            file.endswith('.png') or
                            file.endswith('.DS_Store')):
                        zip_file.write(os.path.join(root, file), file)

        output_files.append({'path': result_file,
                             'name': os.path.basename(result_file),
                             'label': os.path.basename(result_file),
                             'description': 'File(s) generated by DESeq2 App'})

        with zipfile.ZipFile(plot_file, 'w',
                             zipfile.ZIP_DEFLATED,
                             allowZip64=True) as zip_file:
            for root, dirs, files in os.walk(result_directory):
                for file in files:
                    if file.endswith('.png'):
                        zip_file.write(os.path.join(root, file), file)

        output_files.append({'path': plot_file,
                             'name': os.path.basename(plot_file),
                             'label': os.path.basename(plot_file),
                             'description': 'Visualization plots by DESeq2 App'})

        return output_files

    def _generate_report(self, diff_expression_obj_ref, filtered_expression_matrix_ref,
                         params, result_directory):
        """
        _generate_report: generate summary report
        """
        log('creating report')

        output_files = self._generate_output_file_list(result_directory)

        output_html_files = self._generate_html_report(result_directory,
                                                       diff_expression_obj_ref,
                                                       filtered_expression_matrix_ref,
                                                       params)

        report_params = {
              'message': '',
              'workspace_name': params.get('workspace_name'),
              'file_links': output_files,
              'html_links': output_html_files,
              'direct_html_link_index': 0,
              'html_window_height': 266,
              'report_object_name': 'kb_deseq2_report_' + str(uuid.uuid4())}

        kbase_report_client = KBaseReport(self.callback_url)
        output = kbase_report_client.create_extended_report(report_params)

        report_output = {'report_name': output['name'], 'report_ref': output['ref']}

        return report_output

    def _save_count_matrix_file(self, expressionset_ref, result_directory):
        """
        _save_count_matrix_file: download gtf file for each expression
                                 run prepDE.py on them and save reault count matrix file
        """
        mapped_expr_ids = self.expression_set_data.get('mapped_expression_ids')

        gtf_directory = os.path.join(self.scratch, str(uuid.uuid4()))
        self._mkdir_p(gtf_directory)

        for i in mapped_expr_ids:
            for alignment_id, expression_id in i.items():
                expression_data = self.ws.get_objects2(
                                                {'objects':
                                                 [{'ref': expression_id}]})['data'][0]['data']
                handle_id = expression_data.get('file').get('hid')
                expression_name = expression_data.get('id')

                tmp_gtf_directory = os.path.join(gtf_directory, expression_name)
                self._mkdir_p(tmp_gtf_directory)

                self.dfu.shock_to_file({'handle_id': handle_id,
                                        'file_path': tmp_gtf_directory,
                                        'unpack': 'unpack'})

        self._run_prepDE(result_directory, gtf_directory)

    def _run_prepDE(self, result_directory, input_directory):
        """
        _run_prepDE: run prepDE.py script

        ref: http://ccb.jhu.edu/software/stringtie/index.shtml?t=manual#deseq
        """
        log('generating matrix of read counts')
        command = self.PREPDE_TOOLKIT_PATH + '/prepDE.py '
        command += '-i {} '.format(input_directory)
        command += '-g {} '.format(os.path.join(result_directory, 'gene_count_matrix.csv'))
        command += '-t {} '.format(os.path.join(result_directory, 'transcript_count_matrix.csv'))

        self._run_command(command)

    def _generate_diff_expression_csv(self, result_directory, alpha_cutoff):
        """
        _generate_diff_expression_csv: get different expression matrix with DESeq2
        """
        result_files = os.listdir(result_directory)
        if 'gene_count_matrix.csv' not in result_files:
            raise ValueError('Missing gene_count_matrix.csv, available files: {}'.format(
                                                                                    result_files))

        count_matrix_file = os.path.join(result_directory, 'gene_count_matrix.csv')

        rcmd_list = ['Rscript', os.path.join(os.path.dirname(__file__), 'run_DESeq.R')]
        rcmd_list.extend(['--result_directory', result_directory])
        rcmd_list.extend(['--alpha_cutoff', alpha_cutoff])
        output_csvfile = 'gene_results.csv'
        rcmd_list.extend(['--output_csvfile', output_csvfile])
        rcmd_str = " ".join(str(x) for x in rcmd_list)

        self._run_command(rcmd_str)

    def _generate_diff_expression_data(self, result_directory, expressionset_ref,
                                       diff_expression_obj_name, workspace_name, alpha_cutoff):
        """
        _generate_diff_expression_data: generate RNASeqDifferentialExpression object data
        """

        diff_expression_data = {
                'tool_used': 'DESeq2',
                'tool_version': '1.16.1',
                'expressionSet_id': expressionset_ref,
                'genome_id': self.expression_set_data.get('genome_id'),
                'alignmentSet_id': self.expression_set_data.get('alignmentSet_id'),
                'sampleset_id': self.expression_set_data.get('sampleset_id')
        }

        self._generate_diff_expression_csv(result_directory, alpha_cutoff)

        handle = self.dfu.file_to_shock({'file_path': result_directory,
                                         'pack': 'zip',
                                         'make_handle': True})['handle']
        diff_expression_data.update({'file': handle})

        condition = []
        mapped_expr_ids = self.expression_set_data.get('mapped_expression_ids')
        for i in mapped_expr_ids:
            for alignment_id, expression_id in i.items():
                expression_data = self.ws.get_objects2(
                                                {'objects':
                                                 [{'ref': expression_id}]})['data'][0]['data']
                condition.append(expression_data.get('condition'))
        diff_expression_data.update({'condition': condition})

        return diff_expression_data

    def _generate_expression_matrix_data(self, result_directory, expressionset_ref,
                                         filtered_expression_matrix_name, workspace_name):

        """
        _generate_expression_matrix_data: generate ExpressionMatrix object data
        """

        expression_matrix_data = {
        }

        return expression_matrix_data

    def _save_diff_expression(self, result_directory, expressionset_ref,
                              workspace_name, diff_expression_obj_name, alpha_cutoff):
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
                                                                   workspace_name,
                                                                   alpha_cutoff)

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

    def _save_expression_matrix(self, result_directory, expressionset_ref,
                                workspace_name, filtered_expression_matrix_name):
        """
        _save_expression_matrix: save ExpressionMatrix object to workspace
        """
        log('start saving RNASeqDifferentialExpression object')
        if isinstance(workspace_name, int) or workspace_name.isdigit():
            workspace_id = workspace_name
        else:
            workspace_id = self.dfu.ws_name_to_id(workspace_name)

        expression_matrix_data = self._generate_expression_matrix_data(
                                                        result_directory,
                                                        expressionset_ref,
                                                        filtered_expression_matrix_name,
                                                        workspace_name)

        object_type = 'KBaseFeatureValues.ExpressionMatrix'
        save_object_params = {
            'id': workspace_id,
            'objects': [{
                            'type': object_type,
                            'data': expression_matrix_data,
                            'name': filtered_expression_matrix_name
                        }]
        }

        dfu_oi = self.dfu.save_objects(save_object_params)[0]
        filtered_expression_matrix_ref = str(dfu_oi[6]) + '/' + str(dfu_oi[0]) + '/' + str(dfu_oi[4])

        return filtered_expression_matrix_ref

    def __init__(self, config):
        self.ws_url = config["workspace-url"]
        self.callback_url = config['SDK_CALLBACK_URL']
        self.token = config['KB_AUTH_TOKEN']
        self.shock_url = config['shock-url']
        self.dfu = DataFileUtil(self.callback_url)
        self.rau = ReadsAlignmentUtils(self.callback_url)
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

        expressionset_ref = params.get('expressionset_ref')
        self.expression_set_data = self.ws.get_objects2(
                                                {'objects':
                                                 [{'ref': expressionset_ref}]})['data'][0]['data']

        # run prepDE.py and save count matrix file to result_directory
        self._save_count_matrix_file(expressionset_ref, result_directory)

        diff_expression_obj_ref = self._save_diff_expression(
                                                    result_directory,
                                                    expressionset_ref,
                                                    params.get('workspace_name'),
                                                    params.get('diff_expression_obj_name'),
                                                    params.get('alpha_cutoff'))
        filtered_expression_matrix_ref = '111/111/111'
        # filtered_expression_matrix_ref = self._save_expression_matrix(
        #                                             result_directory,
        #                                             expressionset_ref,
        #                                             params.get('workspace_name'),
        #                                             params.get('filtered_expression_matrix_name'))

        returnVal = {'result_directory': result_directory,
                     'diff_expression_obj_ref': diff_expression_obj_ref,
                     'filtered_expression_matrix_ref': filtered_expression_matrix_ref}

        report_output = self._generate_report(diff_expression_obj_ref,
                                              filtered_expression_matrix_ref,
                                              params,
                                              result_directory)
        returnVal.update(report_output)

        return returnVal
