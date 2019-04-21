from threading import Semaphore
from functools import partial
import numpy as np
import subprocess
import time
import re

import xml.etree.ElementTree as ET
from openvas_lib import VulnscanManager, VulnscanException

from server import scanFuncs, scanDetailsFuncs # import database
# from database.scan import scanFuncs

class Quantifier:
    def __init__(self, targets, importance, scan_name):
        self.targets = targets
        self.importance = importance
        self.target_details = {}
        self.scan_name = scan_name
        self._scan = scanFuncs()
        self._scan_details = scanDetailsFuncs()

    def status(self, i):
        print(str(i) + "%")

    def get_details(self, result, target):
        # Use regex to find the cvss scores in the file
        cvss_pattern = '(CVSS:)\s(\d.\d*)'
        cve_pattern = '(CVE:)\s(.*)?(CVE-\d\d\d\d-\d\d\d\d)'
        host_delimeter = '(Port Summary for Host)\s(%s)' % target
        stop_delimeter = '(Port Summary for Host)\s(.*)'
        issue_pattern = '(Issue:)(.*)'
        summary_start_pattern = '(Summary:)(.*)'
        summary_end_pattern = '(Vulnerability Detection Result:)(.*)'
        nvt_pattern = '((NVT:)\s\s\s\s(.*))'

        new_dict = {}
        scores = []
        nvt = []
        start = False
        summary_start = False
        summary = ""

        self.target_details[target] = []

        for line in result:
            match = re.search(host_delimeter, line)
            if match:
                start = True
                continue
            
            match = re.search(stop_delimeter, line)
            if match:
                if(start == True):
                    break
            
            # Host delimeter
            if(start == True):
                match = re.search(cvss_pattern, line)
                if match:
                    scores.append(float(match.groups()[1]))

                match = re.search(nvt_pattern, line)
                if match:
                    nvt.append(match.groups()[2])
                    
                match = re.search(summary_start_pattern, line)
                if match:
                    if(scores[len(scores)-1] >= 4.0):
                        summary_start = True
                        if(bool(new_dict)):
                            new_dict['host'] = target
                            new_dict['scan_id'] = self.scan_id
                            self.target_details[target].append(new_dict)
                        new_dict = {}
                        continue
    
                if summary_start:
                    match = re.search(summary_end_pattern, line)
                    if match:
                        new_dict['nvt'] = nvt[len(scores)-1]
                        new_dict['score'] = scores[len(scores)-1]
                        new_dict['summary'] = summary
                        summary = ""
                        summary_start = False
                        continue

                if(summary_start):
                    summary += line
                    continue

                match = re.search(cve_pattern, line)
                if match:
                    if(scores[len(scores)-1] >= 4.0):
                        new_dict['link'] = 'https://nvd.nist.gov/vuln/detail/%s' % match.groups()[2]
        
        self.target_details[target] = sorted(self.target_details[target], key=lambda k: k['score'], reverse=True)

        return(scores)

    def math_model_1(self, cvss_scores):
        # Convert array to numpy for efficient array manipulation
        cvss_scores = np.array(cvss_scores)

        # First Equation
        # Replace all cvss scores that are greater than or equal to 10 with 9.99
        cvss_scores[cvss_scores >= 10] = 9.99
        cvss_scores = (cvss_scores/10)
        cvss_scores = (1 - cvss_scores)
        
        # Second equation
        pi_notation = 1
        for score in cvss_scores:
            pi_notation = pi_notation * score
        
        # Third equation
        target_score = 1 - pi_notation
        target_score = 10 * target_score

        print("Total CVSS score for target: %f" % target_score)
        return(target_score)

    def math_model_2(self, targets_scores, importance):
        # Convert array to numpy for efficient array manipulation
        targets_scores = np.array(targets_scores)

        # First Equation
        targets_scores = (targets_scores/10.00)
        targets_scores = (1 - targets_scores)

        # Second equation
        pi_notation = 1
        for i in range(0, len(targets_scores)):
            pi_notation = pi_notation * (targets_scores[i]**importance[i])
        
        # Third equation
        weighted_score = 1 - pi_notation
        weighted_score = 10 * weighted_score

        return(weighted_score)

    def parse_result(self, scan_id):
        print("Parsing results for scan id %s\n" % scan_id)
        
        # Get scan details
        command = "omp -u david -w password admin -iX \'<get_tasks task_id=\"%s\" details=\"1\"/>\'" % scan_id
        result = str(subprocess.check_output(['bash', '-c', command]))

        # From scan details, Get report id
        root = ET.fromstring(result)
        for type_tag in root.findall('task/first_report/report'):
            report_id = type_tag.get('id')

        print("Report id: %s" % report_id)

        # Store contents of result file in result.txt FOR TESTING PURPOSES ONLY REMOVE ON FINAL OUPUT
        command = "omp --username david --password password -R  %s -f a3810a62-1f62-11e1-9219-406186ea4fc5 > %s.txt" % (report_id, (self.scan_name+self.scan_id))
        result = str(subprocess.check_output(['bash', '-c', command]))

        command = "omp --username david --password password -R %s -f a3810a62-1f62-11e1-9219-406186ea4fc5" % report_id
        result = str(subprocess.check_output(['bash', '-c', command]))
        result = result.split("\n")


        print("Results Parsed.\n")
        return(result)

    def scan(self, input_targets):
        print("SCANNING TARGET NETWORK")

        # Merge targets into one string separated by comma
        targets = ""
        for i in range(0, len(input_targets)-1):
            targets += input_targets[i] + ", "
        targets += input_targets[len(input_targets)-1]

        sem = Semaphore(0)
        manager = VulnscanManager("localhost", "david", "password")

        scan_id, target_id = manager.launch_scan(targets,
                            profile = "Full and fast",
                            callback_end = partial(lambda x: x.release(), sem),
                            callback_progress = self.status)
        # Wait
        sem.acquire()

        self.scan_id = scan_id
        result = self.parse_result(self.scan_id)
        
        # TEST CASE
        # self.scan_id = "df1296a7-bac5-49da-bda7-69ac74459bdd"
        # result = self.parse_result("df1296a7-bac5-49da-bda7-69ac74459bdd")

        return(result)

    def quantify_targets(self): 
        targets_weighted_scores = []
        # Scan targets and output result file 
        result = self.scan(self.targets)

        # Add Scan to database
        self._scan.addScan({
            'scan_id': self.scan_id,
            'scan_name': self.scan_name
        })
        
        for target in self.targets:
            # Get all the top cve's found and their summary/information
            target_scores = self.get_details(result, target)
            # Apply mathematical model to the target's cvss scores
            targets_weighted_scores.append(self.math_model_1(target_scores))

        # Apply 2nd Mathematical model for all tagets to output single scalar value
        self.quantified_score = self.math_model_2(targets_weighted_scores, self.importance)
        print("Quantified Security score for the network is: %f" % self.quantified_score)


def testCase():
    input_targets = ["192.168.100.12", "192.168.100.11", "127.0.0.1"]
    importance = [0.4, 0.4, 0.4] #SCALING 0.4 0.8 1.2 1.6 2.0

    quantifier = Quantifier(input_targets, importance, "scanSample@")

    quantifier.quantify_targets()

    for target in input_targets:
        for detail in (quantifier.target_details[target]):
            if 'link' in detail:
                quantifier._scan_details.addScan({
                    'scan_id': detail['scan_id'],
                    'host': detail['host'],
                    'nvt': detail['nvt'],
                    'score': detail['score'],
                    'summary': detail['summary'],
                    'link': detail['link']
                })
            else:
                quantifier._scan_details.addScan({
                    'scan_id': detail['scan_id'],
                    'host': detail['host'],
                    'nvt': detail['nvt'],
                    'score': detail['score'],
                    'summary': detail['summary']
                })

    # quantifier._scan.getScans()

    # quantifier._scan.deleteScan('df1296a7-bac5-49da-bda7-69ac74459bdd')
    
    # quantifier._scan_details.getScans()
    # quantifier._scan.getScans()

testCase()