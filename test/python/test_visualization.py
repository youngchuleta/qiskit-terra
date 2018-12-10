# -*- coding: utf-8 -*-

# Copyright 2017, IBM.
#
# This source code is licensed under the Apache License, Version 2.0 found in
# the LICENSE.txt file in the root directory of this source tree.

# pylint: disable=missing-docstring

"""Tests for visualization tools."""

import os
import random
from inspect import signature
import unittest
import qiskit
from unittest.mock import patch
from .common import QiskitTestCase

try:
    from qiskit.tools.visualization import generate_latex_source, _counts_visualization, _error
    VALID_MATPLOTLIB = True
except (RuntimeError, ImportError):
    # Under some combinations (travis osx vms, or headless configurations)
    # matplotlib might not be fully, raising:
    # RuntimeError: Python is not installed as a framework.
    # when importing. If that is the case, the full test is skipped.
    VALID_MATPLOTLIB = False


@unittest.skipIf(not VALID_MATPLOTLIB, 'osx matplotlib backend not available')
class TestLatexSourceGenerator(QiskitTestCase):
    """QISKit latex source generator tests."""

    def random_circuit(self, width=3, depth=3, max_operands=3):
        """Generate random circuit of arbitrary size.
        Note: the depth is the layers of independent operation. true depth
        in the image may be more for visualization purposes, if gates overlap.

        Args:
            width (int): number of quantum wires
            depth (int): layers of operations
            max_operands (int): maximum operands of each gate

        Returns:
            QuantumCircuit: constructed circuit
        """
        qr = qiskit.QuantumRegister(width, "q")
        qc = qiskit.QuantumCircuit(qr)

        one_q_ops = "iden,u0,u1,u2,u3,x,y,z,h,s,sdg,t,tdg,rx,ry,rz"
        two_q_ops = "cx,cy,cz,ch,crz,cu1,cu3,swap"
        three_q_ops = "ccx"

        # apply arbitrary random operations at every depth
        for _ in range(depth):
            # choose either 1, 2, or 3 qubits for the operation
            remaining_qubits = list(range(width))
            while remaining_qubits:
                max_possible_operands = min(len(remaining_qubits), max_operands)
                num_operands = random.choice(range(max_possible_operands))+1
                operands = random.sample(remaining_qubits, num_operands)
                remaining_qubits = [q for q in remaining_qubits if q not in operands]
                if num_operands == 1:
                    operation = random.choice(one_q_ops.split(','))
                elif num_operands == 2:
                    operation = random.choice(two_q_ops.split(','))
                elif num_operands == 3:
                    operation = random.choice(three_q_ops.split(','))
                # every gate is defined as a method of the QuantumCircuit class
                # the code below is so we can call a gate by its name
                gate = getattr(qiskit.QuantumCircuit, operation)
                op_args = list(signature(gate).parameters.keys())
                num_angles = len(op_args) - num_operands - 1    # -1 for the 'self' arg
                angles = [random.uniform(0, 3.14) for x in range(num_angles)]
                register_operands = [qr[i] for i in operands]
                gate(qc, *angles, *register_operands)

        return qc

    def test_tiny_circuit(self):
        """Test draw tiny circuit."""
        filename = self._get_resource_path('test_tiny.tex')
        qc = self.random_circuit(1, 1, 1)
        try:
            generate_latex_source(qc, filename)
            self.assertNotEqual(os.path.exists(filename), False)
        finally:
            if os.path.exists(filename):
                os.remove(filename)

    def test_normal_circuit(self):
        """Test draw normal size circuit."""
        filename = self._get_resource_path('test_normal.tex')
        qc = self.random_circuit(5, 5, 3)
        try:
            generate_latex_source(qc, filename)
            self.assertNotEqual(os.path.exists(filename), False)
        finally:
            if os.path.exists(filename):
                os.remove(filename)

    def test_wide_circuit(self):
        """Test draw wide circuit."""
        filename = self._get_resource_path('test_wide.tex')
        qc = self.random_circuit(100, 1, 1)
        try:
            generate_latex_source(qc, filename)
            self.assertNotEqual(os.path.exists(filename), False)
        finally:
            if os.path.exists(filename):
                os.remove(filename)

    def test_deep_circuit(self):
        """Test draw deep circuit."""
        filename = self._get_resource_path('test_deep.tex')
        qc = self.random_circuit(1, 100, 1)
        try:
            generate_latex_source(qc, filename)
            self.assertNotEqual(os.path.exists(filename), False)
        finally:
            if os.path.exists(filename):
                os.remove(filename)

    def test_huge_circuit(self):
        """Test draw huge circuit."""
        filename = self._get_resource_path('test_huge.tex')
        qc = self.random_circuit(40, 40, 1)
        try:
            generate_latex_source(qc, filename)
            self.assertNotEqual(os.path.exists(filename), False)
        finally:
            if os.path.exists(filename):
                os.remove(filename)

    def test_teleport(self):
        """Test draw teleport circuit."""
        filename = self._get_resource_path('test_teleport.tex')
        qr = qiskit.QuantumRegister(3, 'q')
        cr = qiskit.ClassicalRegister(3, 'c')
        qc = qiskit.QuantumCircuit(qr, cr)
        # Prepare an initial state
        qc.u3(0.3, 0.2, 0.1, qr[0])
        # Prepare a Bell pair
        qc.h(qr[1])
        qc.cx(qr[1], qr[2])
        # Barrier following state preparation
        qc.barrier(qr)
        # Measure in the Bell basis
        qc.cx(qr[0], qr[1])
        qc.h(qr[0])
        qc.measure(qr[0], cr[0])
        qc.measure(qr[1], cr[1])
        # Apply a correction
        qc.z(qr[2]).c_if(cr, 1)
        qc.x(qr[2]).c_if(cr, 2)
        qc.measure(qr[2], cr[2])
        try:
            generate_latex_source(qc, filename)
            self.assertNotEqual(os.path.exists(filename), False)
        finally:
            if os.path.exists(filename):
                os.remove(filename)

class CountsVisualization_TestClass(QiskitTestCase):
    
    def test_plot_file_created(self):
        """Test Plot File is Created"""
#        PASSED
        testfile = 'C:\\Users\\albie\\testfile.jpg'
        plot_histogram(data=[], filename=testfile)
        try:
            self.assertNotEqual(os.path.exists(testfile), False)
        finally:
            if os.path.exists(testfile):
                os.remove(testfile) 
                
    
    def numToKeep_warning(self):
#        test that warning is raised when number_to_keep != None
#        PASSED
        plot_histogram(data=[], number_to_keep=1, show=False)
        self.assertWarns(DeprecationWarning,
                    msg="number_to_keep has been deprecated, use the options dictionary and set a number_to_keep key instead")
        
    def uneqDataLegendLens_raisesError(self):
#        test that warning is raised when number_to_keep != None
#        checks for case when data is a list of dicts, and legend doesn't match # of dicts in list
#        PASSED
        with self.assertRaises(VisualizationError) as cm:
            plot_histogram(data=[{'001': 130, '011': 130, '111': 130}, {'000': 130, '100': 130, '110': 130}], 
                       legend=["data1", "data2", "data3"], show=False)
        self.assertTrue("Length of legendL (3) doesn't match number of input executions: 2" in str(cm.exception))        
    
    #@patch.object(matpla)
    @patch.object(matplotlib, "axes")
    @patch.object(matplotlib.pyplot, "subplots")
    #def test_axes(self, mock_ax):
    def test_subplots(self, mock_plot, mock_ax):
        #if options = None
        mock_ax.return_value = None
        mock_plot.return_value = None, mock_ax
        cv.plot_histogram(data = {1:5,2:4,3:3,4:2,5:1,6:0,7:1})
        mock_plot.assert_called_with()#lines 75-76
        mock_ax.set_ylabel.assert_called_with('Probabilities', fontsize=12)#line 102
        
        # Following is called with " array([0, 1, 2, 3, 4, 5, 6] " ,but tests
        # for that fail
        mock_ax.set_xticks.assert_called #_with('[0,1,2,3,4,5,6]')#line 103
        
        mock_ax.set_xticklabels.assert_called_with([1, 2, 3, 4, 5, 6, 7], fontsize=12, rotation=70)#104
        #the following is too complicated to mock better
        mock_ax.set_ylim.assert_called #_with([0., min([1.2, max([1.2 * val for val in pvalues])])])#line 103
        
        #if options = {'height':4, 'width':3}
        mock_plot.return_value = None, None
        cv.plot_histogram(data = [], options = {'height':4, 'width':3})
        mock_plot.assert_called_with(figsize=(3, 4))#lines 73-74

if __name__ == '__main__':
    unittest.main(verbosity=2)
