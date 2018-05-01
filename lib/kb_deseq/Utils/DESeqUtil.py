import time
import json
import os
import uuid
import errno
import subprocess
import zipfile
import shutil
import csv
import numpy
import fileinput
import re
import itertools
import collections

from DataFileUtil.DataFileUtilClient import DataFileUtil
from Workspace.WorkspaceClient import Workspace as Workspace
from KBaseReport.KBaseReportClient import KBaseReport
from ReadsAlignmentUtils.ReadsAlignmentUtilsClient import ReadsAlignmentUtils
from DifferentialExpressionUtils.DifferentialExpressionUtilsClient import DifferentialExpressionUtils
from GenomeSearchUtil.GenomeSearchUtilClient import GenomeSearchUtil


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
        for p in ['expressionset_ref', 'differential_expression_set_suffix',
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

    def _xor(self, a, b):
        return bool(a) != bool(b)

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
                              params):
        """
        _generate_html_report: generate html summary report
        """

        log('start generating html report')
        html_report = list()

        output_directory = os.path.join(self.scratch, str(uuid.uuid4()))
        self._mkdir_p(output_directory)
        result_file_path = os.path.join(output_directory, 'report.html')

        result_directory

        result_dirs = os.listdir(result_directory)
        visualization_content = ''
        for result_dir in result_dirs:
            dispersion_plots_name = result_dir + '_dispersion_plots.png'
            dispersion_plots_display_name = '{} {} dispersion plot'.format(result_dir.split('_')[0],
                                                                           result_dir.split('_')[1])

            shutil.copy2(os.path.join(result_directory, result_dir, 'deseq2_MAplot.png'),
                         os.path.join(output_directory, dispersion_plots_name))
            visualization_content += '<div class="gallery">'
            visualization_content += '<a target="_blank" href="{}">'.format(dispersion_plots_name)
            visualization_content += '<img src="{}" '.format(dispersion_plots_name)
            visualization_content += 'alt="{}" width="600" height="400">'.format(dispersion_plots_display_name)
            visualization_content += '</a><div class="desc">{}</div></div>'.format(dispersion_plots_display_name)

            pca_plots_name = result_dir + '_PCA_MAplot.png'
            pca_plots_display_name = '{} {} PCA plot'.format(result_dir.split('_')[0],
                                                             result_dir.split('_')[1])

            shutil.copy2(os.path.join(result_directory, result_dir, 'PCA_MAplot.png'),
                         os.path.join(output_directory, pca_plots_name))
            visualization_content += '<div class="gallery">'
            visualization_content += '<a target="_blank" href="{}">'.format(pca_plots_name)
            visualization_content += '<img src="{}" '.format(pca_plots_name)
            visualization_content += 'alt="{}" width="600" height="400">'.format(pca_plots_display_name)
            visualization_content += '</a><div class="desc">{}</div></div>'.format(pca_plots_display_name)
          
        diff_expr_set_data = self.ws.get_objects2({'objects':
                                                  [{'ref': 
                                                   diff_expression_obj_ref}]})['data'][0]['data']

        items = diff_expr_set_data['items']

        # expression_ref = self.expression_set_data['items'][0]['ref']
        # expression_object = self.ws.get_objects2({'objects':
        #                                          [{'ref': expression_ref}]})['data'][0]
        # expression_data = expression_object['data']
        # genome_ref = expression_data['genome_id']
        # genome_name = self.ws.get_object_info([{"ref": genome_ref}], includeMetadata=None)[0][1]
        
        # feature_num = self.gsu.search({'ref': genome_ref})['num_found']
        # genome_features = self.gsu.search({'ref': genome_ref,
        #                                    'limit': feature_num,
        #                                    'sort_by': [['feature_id', True]]})['features']
        # feature_ids = []
        # for genome_feature in genome_features:
        #     if not re.match('.*\.\d*', genome_feature.get('feature_id')):
        #         feature_ids.append(genome_feature.get('feature_id'))
        # total_feature_num = len(feature_ids)

        overview_content = ''
        overview_content += '<br/><table><tr><th>Generated DifferentialExpressionMatrixSet'
        overview_content += ' Object</th></tr>'
        overview_content += '<tr><td>{} ({})'.format(params.get('diff_expression_obj_name'),
                                                     diff_expression_obj_ref)
        overview_content += '</td></tr></table>'

        overview_content += '<p><br/></p>'

        overview_content += '<br/><table><tr><th>Generated DifferentialExpressionMatrix'
        overview_content += ' Object</th><th></th><th></th><th></th></tr>'
        overview_content += '<tr><th>Differential Expression Matrix Name</th>'
        # overview_content += '<th>Reference Genome</th>'
        # overview_content += '<th>Reference Genome Feature Count</th>'
        overview_content += '<th>Feature Count</th>'
        overview_content += '</tr>'
        for item in items:
            diff_expr_ref = item['ref']
            diff_expr_object = self.ws.get_objects2({'objects':
                                                    [{'ref': diff_expr_ref}]})['data'][0]

            diff_expr_data = diff_expr_object['data']
            diff_expr_info = diff_expr_object['info']
            diff_expr_name = diff_expr_info[1]
            number_features = len(diff_expr_data['data']['row_ids'])

            overview_content += '<tr><td>{} ({})</td>'.format(diff_expr_name, diff_expr_ref)
            # overview_content += '<td>{} ({})</td>'.format(genome_name, genome_ref)
            # overview_content += '<td>{}</td>'.format(total_feature_num)
            overview_content += '<td>{}</td></tr>'.format(number_features)
        overview_content += '</table>'

        with open(result_file_path, 'w') as result_file:
            with open(os.path.join(os.path.dirname(__file__), 'report_template.html'),
                      'r') as report_template_file:
                report_template = report_template_file.read()
                report_template = report_template.replace('<p>Overview_Content</p>',
                                                          overview_content)
                report_template = report_template.replace('<p>Visualization_Content</p>',
                                                          visualization_content)
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

        log('start packing result files')
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
                        zip_file.write(os.path.join(root, file), 
                                       os.path.join(os.path.basename(root), file))

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
                        zip_file.write(os.path.join(root, file), 
                                       os.path.join(os.path.basename(root), file))

        output_files.append({'path': plot_file,
                             'name': os.path.basename(plot_file),
                             'label': os.path.basename(plot_file),
                             'description': 'Visualization plots by DESeq2 App'})

        return output_files

    def _generate_report(self, diff_expression_obj_ref, params, result_directory):
        """
        _generate_report: generate summary report
        """

        log('creating report')

        output_files = self._generate_output_file_list(result_directory)

        output_html_files = self._generate_html_report(result_directory,
                                                       diff_expression_obj_ref,
                                                       params)

        diff_expr_set_data = self.ws.get_objects2({'objects':
                                                  [{'ref': 
                                                   diff_expression_obj_ref}]})['data'][0]['data']

        items = diff_expr_set_data['items']

        description_set = 'DifferentialExpressionMatrixSet generated by DESeq2'
        description_object = 'DifferentialExpressionMatrix generated by DESeq2'
        objects_created = []
        objects_created.append({'ref': diff_expression_obj_ref,
                                'description': description_set})

        for item in items:
            diff_expr_ref = item['ref']
            objects_created.append({'ref': diff_expr_ref,
                                   'description': description_object})

        report_params = {'message': '',
                         'workspace_name': params.get('workspace_name'),
                         'objects_created': objects_created,
                         'file_links': output_files,
                         'html_links': output_html_files,
                         'direct_html_link_index': 0,
                         'html_window_height': 333,
                         'report_object_name': 'kb_deseq2_report_' + str(uuid.uuid4())}

        kbase_report_client = KBaseReport(self.callback_url)
        output = kbase_report_client.create_extended_report(report_params)

        report_output = {'report_name': output['name'], 'report_ref': output['ref']}

        return report_output

    def _save_count_matrix_file(self, result_directory):
        """
        _save_count_matrix_file: download gtf file for each expression
                                 run prepDE.py on them and save reault count matrix file
        """

        log('generating count matrix file')

        items = self.expression_set_data['items']

        gtf_directory = os.path.join(self.scratch, str(uuid.uuid4()))
        self._mkdir_p(gtf_directory)

        transcript_directory = os.path.join(self.scratch, str(uuid.uuid4()))
        self._mkdir_p(transcript_directory)

        for item in items:
            expression_ref = item['ref']
            expression_object = self.ws.get_objects2({'objects':
                                                     [{'ref': expression_ref}]})['data'][0]
            expression_data = expression_object['data']
            expression_info = expression_object['info']
            handle_id = expression_data.get('file').get('hid')
            expression_name = expression_info[1]

            tmp_gtf_directory = os.path.join(gtf_directory, expression_name)
            self._mkdir_p(tmp_gtf_directory)

            self.dfu.shock_to_file({'handle_id': handle_id,
                                    'file_path': tmp_gtf_directory,
                                    'unpack': 'unpack'})

            tmp_transcript_directory = os.path.join(transcript_directory, expression_name)
            self._mkdir_p(tmp_transcript_directory)

            cp_command = 'cp {} {}'.format(os.path.join(tmp_gtf_directory, 'transcripts.gtf'),
                                           tmp_transcript_directory)

            self._run_command(cp_command)

        self._run_prepDE(result_directory, transcript_directory)

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

    def _generate_diff_expression_csv(self, result_directory, alpha_cutoff, fold_change_cutoff,
                                      condition_string):
        """
        _generate_diff_expression_csv: get different expression matrix with DESeq2
        """

        result_files = os.listdir(result_directory)
        if 'gene_count_matrix.csv' not in result_files:
            error_msg = 'Missing gene_count_matrix.csv, available files: {}'.format(result_files)
            raise ValueError(error_msg)

        rcmd_list = ['Rscript', os.path.join(os.path.dirname(__file__), 'run_DESeq.R')]
        rcmd_list.extend(['--result_directory', result_directory])
        rcmd_list.extend(['--alpha_cutoff', alpha_cutoff])
        rcmd_list.extend(['--fold_change_cutoff', fold_change_cutoff])
        rcmd_list.extend(['--condition_string', condition_string])

        rcmd_str = " ".join(str(x) for x in rcmd_list)

        self._run_command(rcmd_str)

    def _get_condition_string(self, result_directory, condition_labels):
        """
        _get_condition_string: get condition string corresponding to given condition_labels
        """

        log('generating condition string')

        count_matrix_file = os.path.join(result_directory, 'gene_count_matrix.csv')
        tmp_count_matrix_file = os.path.join(result_directory, 'tmp_gene_count_matrix.csv')

        with open(count_matrix_file, "rb") as f:
            reader = csv.reader(f)
            columns = reader.next()[1:]

        condition_list = [None] * len(columns)

        items = self.expression_set_data.get('items')
        expr_name_condition_mapping = {}
        for item in items:
            expression_ref = item['ref']
            expr_object = self.ws.get_objects2({'objects':
                                               [{'ref': expression_ref}]})['data'][0]
            expr_data = expr_object['data']
            expr_info = expr_object['info']
            expr_name = expr_info[1]
            expr_condition = expr_data['condition']
            expr_name_list = expr_name_condition_mapping.get(expr_condition)
            if expr_name_list:
                expr_name_list.append(expr_name)
                expr_name_condition_mapping.update({expr_condition: expr_name_list})
            else:
                expr_name_condition_mapping.update({expr_condition: [expr_name]})

        for condition_label in condition_labels:
            if condition_label in expr_name_condition_mapping.keys():
                expression_names = expr_name_condition_mapping.get(condition_label)
                for expression_name in expression_names:
                    pos = columns.index(expression_name)
                    condition_list[pos] = condition_label
            else:
                error_msg = 'Condition: {} is not availalbe. '.format(condition_label)
                error_msg += 'Available conditions: {}'.format(expr_name_condition_mapping.keys())
                raise ValueError(error_msg)

        if None in condition_list:
            filtered_pos = [0]
            filtered_condition_list = []
            for condition in condition_list:
                if condition:
                    pos = [i + 1 for i, val in enumerate(condition_list) if val == condition]
                    filtered_pos += pos
                    filtered_condition_list.append(condition)
            filtered_pos = list(set(filtered_pos))
            with open(count_matrix_file, "rb") as source:
                rdr = csv.reader(source)
                with open(tmp_count_matrix_file, "wb") as result:
                    wtr = csv.writer(result)
                    for r in rdr:
                        wtr.writerow(tuple(list(numpy.array(r)[filtered_pos])))
            os.rename(tmp_count_matrix_file, count_matrix_file)
            condition_string = ','.join(filtered_condition_list)
        else:
            condition_string = ','.join(condition_list)

        return condition_string

    def _save_diff_expression(self, result_directory, params):
        """
        _save_diff_expression: save DifferentialExpression object to workspace
        """

        log('start saving KBaseFeatureValues.DifferentialExpressionMatrix object')

        workspace_name = params.get('workspace_name')
        diff_expression_obj_name = params.get('diff_expression_obj_name')

        destination_ref = workspace_name + '/' + diff_expression_obj_name

        result_dirs = os.listdir(result_directory)

        diff_expr_files = list()

        for result_dir in result_dirs:

            diff_expr_file = dict()
            condition_labels = result_dir.split('_')

            genes_results_filepath = os.path.join(result_directory, result_dir, 
                                                  'deseq_results.csv')

            with open(genes_results_filepath, "rb") as f:
                reader = csv.reader(f)
                columns = reader.next()[1:]

            columns[columns.index('log2FoldChange')] = 'log2_fold_change'
            columns[columns.index('pvalue')] = 'p_value'
            columns[columns.index('padj')] = 'q_value'
            for line in fileinput.input(genes_results_filepath, inplace=True):
                if fileinput.isfirstline():
                    print 'gene_id,' + ','.join(columns)
                else:
                    print line,

            reader = csv.DictReader(open(genes_results_filepath))

            diffexpr_filepath = os.path.join(result_directory, result_dir, 
                                             'differential_expression_result.csv')
            with open(diffexpr_filepath, 'w') as csvfile:
                fieldnames = ['gene_id', 'log2_fold_change', 'p_value', 'q_value']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                writer.writeheader()

                for row in reader:
                    writer.writerow({'gene_id': row.get('gene_id'), 
                                     'log2_fold_change': row.get('log2_fold_change'),
                                     'p_value': row.get('p_value'),
                                     'q_value': row.get('q_value')})

            diff_expr_file.update({'condition_mapping': 
                                   {condition_labels[0]: condition_labels[1]}})
            diff_expr_file.update({'diffexpr_filepath': diffexpr_filepath})

            diff_expr_files.append(diff_expr_file)

        expression_ref = self.expression_set_data['items'][0]['ref']
        expression_data = self.ws.get_objects2({'objects':
                                                [{'ref': expression_ref}]})['data'][0]['data']
        genome_ref = expression_data['genome_id']

        upload_diff_expr_params = {'destination_ref': destination_ref,
                                   'diffexpr_data': diff_expr_files,
                                   'tool_used': 'deseq',
                                   'tool_version': '1.16.1',
                                   'genome_ref': genome_ref}

        deu_upload_return = self.deu.save_differential_expression_matrix_set(upload_diff_expr_params)

        diff_expression_obj_ref = deu_upload_return['diffExprMatrixSet_ref']

        return diff_expression_obj_ref

    def _generate_deseq_files(self, result_directory, params):
        """
        _generate_deseq_files: generate DESeq files
        """
        gene_result_file = os.path.join(result_directory, 'gene_count_matrix.csv')
        with open(gene_result_file, "rb") as f:
            reader = csv.reader(f)
            columns = reader.next()[1:]

        for line in fileinput.input(gene_result_file, inplace=True):
            if fileinput.isfirstline():
                print 'gene_id,' + ','.join(columns)
            else:
                print line,

        condition_string = self._get_condition_string(result_directory,
                                                      params.get('condition_labels'))

        self._generate_diff_expression_csv(result_directory, params.get('alpha_cutoff'),
                                           params.get('fold_change_cutoff'), condition_string)

    def _get_condition_labels(self):
        """
        _get_condition_labels: get all possible condition label pairs
        """
        log('getting all possible condition pairs')

        items = self.expression_set_data.get('items')
        condition_replicate_name_mapping = collections.OrderedDict()
        for item in items:
            expression_ref = item['ref']
            expr_object = self.ws.get_objects2({'objects':
                                               [{'ref': expression_ref}]})['data'][0]
            expr_data = expr_object['data']
            expr_info = expr_object['info']
            expr_name = expr_info[1]
            expr_condition = expr_data['condition']
            expr_name_list = condition_replicate_name_mapping.get(expr_condition)
            if expr_name_list:
                expr_name_list.append(expr_name)
                condition_replicate_name_mapping.update({expr_condition: expr_name_list})
            else:
                condition_replicate_name_mapping.update({expr_condition: [expr_name]})

        condition_labels = condition_replicate_name_mapping.keys()

        condition_label_pairs = [list(pair) for pair in itertools.combinations(condition_labels, 
                                                                               2)]

        log('all pssible conditon pairs:\n{}'.format(condition_label_pairs))

        return condition_label_pairs, condition_labels

    def _check_input_labels(self, condition_pairs, available_condition_labels):
        """
        _check_input_labels: check input condition pairs
        """
        checked = True
        for condition_pair in condition_pairs:

            first_label = condition_pair['condition_label_1'][0].strip()
            second_label = condition_pair['condition_label_2'][0].strip()
            if first_label not in available_condition_labels:
                error_msg = 'Condition: {} is not availalbe. '.format(first_label)
                error_msg += 'Available conditions: {}'.format(available_condition_labels)
                raise ValueError(error_msg)

            if second_label not in available_condition_labels:
                error_msg = 'Condition: {} is not availalbe. '.format(second_label)
                error_msg += 'Available conditions: {}'.format(available_condition_labels)
                raise ValueError(error_msg)

            if first_label == second_label:
                raise ValueError('Input conditions are the same')

        return checked

    def __init__(self, config):
        self.ws_url = config["workspace-url"]
        self.callback_url = config['SDK_CALLBACK_URL']
        self.token = config['KB_AUTH_TOKEN']
        self.shock_url = config['shock-url']
        self.dfu = DataFileUtil(self.callback_url)
        self.rau = ReadsAlignmentUtils(self.callback_url)
        self.deu = DifferentialExpressionUtils(self.callback_url, service_ver='dev')
        self.gsu = GenomeSearchUtil(self.callback_url)
        self.ws = Workspace(self.ws_url, token=self.token)
        self.scratch = config['scratch']

    def run_deseq2_app(self, params):
        """
        run_deseq2_app: run DESeq2 app
        (https://www.bioconductor.org/packages/release/bioc/vignettes/DESeq2/inst/doc/DESeq2.html)

        required params:
            expressionset_ref: ExpressionSet object reference
            differential_expression_set_suffix: DifferentialExpressoinMatrixSet object suffix
            workspace_name: the name of the workspace it gets saved to

        optional params:
            run_all_combinations: run all paired condition combinations
            condition_labels: conditions for expression set object
            alpha_cutoff: q value cutoff
            fold_change_cutoff: fold change cutoff
            num_threads: number of threads
            fold_scale_type: one of ["linear", "log2+1", "log10+1"]

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
        expression_set_obj = self.ws.get_objects2({'objects':
                                                  [{'ref': expressionset_ref}]})['data'][0]
        self.expression_set_data = expression_set_obj['data']
        expression_set_name = expression_set_obj['info'][1]

        differential_expression_set_suffix = params.get('differential_expression_set_suffix')
        if re.match('.*_*[Ee]xpression_*[Ss]et', expression_set_name):
            diff_expression_obj_name = re.sub('_*[Ee]xpression_*[Ss]et',
                                              differential_expression_set_suffix,
                                              expression_set_name)
        else:
            diff_expression_obj_name = expression_set_name + differential_expression_set_suffix

        params['diff_expression_obj_name'] = diff_expression_obj_name

        available_condition_label_pairs, available_condition_labels = self._get_condition_labels()

        run_all_combinations = params.get('run_all_combinations')
        condition_pairs = params.get('condition_pairs')
        if not self._xor(run_all_combinations, condition_pairs):
            error_msg = "Invalid input:\nselect 'Run All Paired Condition Combinations' "
            error_msg += "or provide partial condition pairs. Don't do both"
            raise ValueError(error_msg)

        if run_all_combinations:
            condition_label_pairs = available_condition_label_pairs
        else:
            if self._check_input_labels(condition_pairs, available_condition_labels):
                condition_label_pairs = list()
                for condition_pair in condition_pairs:
                    condition_labels = [condition_pair.get('condition_label_1')[0].strip(),
                                        condition_pair.get('condition_label_2')[0].strip()]
                    condition_label_pairs.append(condition_labels)

        for condition_label_pair in condition_label_pairs:
            params['condition_labels'] = condition_label_pair

            dir_suffix = '_'.join(condition_label_pair)

            sub_result_directory = os.path.join(result_directory, dir_suffix)
            self._mkdir_p(sub_result_directory)

            # run prepDE.py and save count matrix file
            self._save_count_matrix_file(sub_result_directory)

            self._generate_deseq_files(sub_result_directory, params)

        diff_expression_obj_ref = self._save_diff_expression(result_directory,
                                                             params)

        returnVal = {'result_directory': result_directory,
                     'diff_expression_obj_ref': diff_expression_obj_ref}

        report_output = self._generate_report(diff_expression_obj_ref,
                                              params,
                                              result_directory)
        returnVal.update(report_output)

        return returnVal
