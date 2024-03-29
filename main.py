#------------------------------------------------------
# ---------------------- main.py -----------------------
# ------------------------------------------------------
from tabnanny import verbose
from PyQt5.QtWidgets import*
from PyQt5.uic import loadUi
import PyQt5
from matplotlib.pyplot import get
import functions
from functions import custom
import Run_Optimization
from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)
import OptimizationInputs
#Optimization Algorthms
from enumOptimizations import Optimizations

class MatplotlibWidget(QMainWindow):
    inputs = [] 
    inputs.append(OptimizationInputs.OptimizationStructure())
    inputs.append(OptimizationInputs.OptimizationStructure())
    inputs.append(OptimizationInputs.OptimizationStructure())
    inputs.append(OptimizationInputs.OptimizationSMAStructure())
    inputs.append(OptimizationInputs.OptimizationSMAStructure())
    inputs.append(OptimizationInputs.OptimizationSMAStructure())


    def __init__(self):
        
        QMainWindow.__init__(self)

        loadUi("qt_designer.ui",self)
        AddItemsToComboBox(self)
        

        self.setWindowTitle("Optimization Algorthms")
        #Set button functions
        
        self.pushButton.clicked.connect(self.Plot)
        self.infoButton.clicked.connect(self.InfoButton)
        self.inputButton.clicked.connect(self.InputButton1)
        self.inputButton_2.clicked.connect(self.InputButton2)
        self.inputButton_3.clicked.connect(self.InputButton3)

        self.functionComboBox.currentIndexChanged.connect(self.CustomFunctionSelected)
        self.functionTextbox.setVisible(False)
        self.functionLabel.setVisible(False)
        
       
        
        self.addToolBar(NavigationToolbar(self.MplWidget.canvas, self))

    def CustomFunctionSelected(self):
         if self.functionComboBox.currentIndex()==17:
            self.functionTextbox.setVisible(True)
            self.functionLabel.setVisible(True)
         else: 
            self.functionTextbox.setVisible(False)
            self.functionLabel.setVisible(False)

    def InfoButton(self):

        switcher = {
            0: 'ackleyFunctionWindow.ui',
            1: 'DixonPriceFunctionWindow.ui',
            2: 'GriewankFunctionWindow.ui',
            3: 'MichalewiczFunctionWindow.ui',
            4: 'PermFunctionWindow.ui',
            5: 'PowellFunctionWindow.ui',
            6: 'PowerSumFunctionWindow.ui',
            7: 'rastriginFunctionWindow.ui',
            8: 'rosenbrockFunctionWindow.ui',
            9: 'schwefelFunctionWindow.ui',
            10: 'sphereFunctionWindow.ui',
            11: 'sum2FunctionWindow.ui',
            12: 'tridFunctionWindow.ui',
            13: 'zakharovFunctionWindow.ui',
            14: 'ellipseFunctionWindow.ui',
            15: 'nesterovFunctionWindow.ui',
            16: 'saddleFunctionWindow.ui',
            17: ''
        }
        infowindow=switcher.get(self.functionComboBox.currentIndex(), "nothing")

        if self.functionComboBox.currentIndex()==17 : #Check if custom selected   
            return
        else: 
            self.window = PyQt5.QtWidgets.QMainWindow()
            loadUi(infowindow, self.window)           
        self.window.show()
        self.window.okButton.clicked.connect(self.AckleyInfoOkButton)          

    def Plot(self,sol):
        opt = Optimizations(self.optimizationComboBox.currentIndex())
        opt2 = Optimizations(self.optimizationComboBox_2.currentIndex())
        opt3 = Optimizations(self.optimizationComboBox_3.currentIndex())
        if self.functionTextbox.toPlainText()!="":
            functions.createFunction(str(self.functionTextbox.toPlainText()))

      
        param1 = self.functionComboBox.currentIndex(),int(self.inputs[0].MaxIter),int(self.inputs[0].dimension),int(self.inputs[0].searchAgentsNo),int(self.inputs[0].lb),int(self.inputs[0].ub)
        param2 = self.functionComboBox.currentIndex(),int(self.inputs[1].MaxIter),int(self.inputs[1].dimension),int(self.inputs[1].searchAgentsNo),int(self.inputs[1].lb),int(self.inputs[1].ub)
        param3 = self.functionComboBox.currentIndex(),int(self.inputs[2].MaxIter),int(self.inputs[2].dimension),int(self.inputs[2].searchAgentsNo),int(self.inputs[2].lb),int(self.inputs[2].ub)
        paramSMA1 = self.functionComboBox.currentIndex(), int(self.inputs[3].problem_size), self.inputs[3].verbose,int(self.inputs[3].epoch),int(self.inputs[3].pop_size),int(self.inputs[3].smalb),int(self.inputs[3].smaub)
        paramSMA2 = self.functionComboBox.currentIndex(), int(self.inputs[4].problem_size), self.inputs[4].verbose,int(self.inputs[4].epoch),int(self.inputs[4].pop_size),int(self.inputs[4].smalb),int(self.inputs[4].smaub)
        paramSMA3 = self.functionComboBox.currentIndex(), int(self.inputs[5].problem_size), self.inputs[5].verbose,int(self.inputs[5].epoch),int(self.inputs[5].pop_size),int(self.inputs[5].smalb),int(self.inputs[5].smaub)

        if self.optimizationComboBox_2.currentIndex()==15 and self.optimizationComboBox_3.currentIndex()==15 :
            #Run single
            opt = Optimizations(self.optimizationComboBox.currentIndex())
            sol = Run_Optimization.Single(opt,param1,paramSMA1)
            self.MplWidget.canvas.axes.clear()
            self.MplWidget.canvas.axes.plot(sol)
            self.MplWidget.canvas.axes.legend((opt.name, 'Best fitness'),loc='upper right')
            
        elif self.optimizationComboBox_2.currentIndex()!=15 and self.optimizationComboBox_3.currentIndex()==15 :
            #Run double first and second
            sol, sol2 = Run_Optimization.Double(opt, opt2,param1,param2,paramSMA1,paramSMA2)
            self.MplWidget.canvas.axes.clear()
            self.MplWidget.canvas.axes.plot(sol)
            self.MplWidget.canvas.axes.plot(sol2)
            self.MplWidget.canvas.axes.legend((opt.name, opt2.name),loc='upper right')
        elif self.optimizationComboBox_2.currentIndex()==15 and self.optimizationComboBox_3.currentIndex()!=15 :     
            # run double first and third
            sol, sol2 = Run_Optimization.Double(opt, opt3,param1,param3,paramSMA1,paramSMA2)
            self.MplWidget.canvas.axes.clear()
            self.MplWidget.canvas.axes.plot(sol)
            self.MplWidget.canvas.axes.plot(sol2)
            self.MplWidget.canvas.axes.legend((opt.name, opt3.name),loc='upper right')
        else:
            #run all
            sol, sol2, sol3 = Run_Optimization.Triple(opt, opt2,opt3,param1,param2,param3,paramSMA1,paramSMA2,paramSMA3)
            self.MplWidget.canvas.axes.clear()
            self.MplWidget.canvas.axes.plot(sol)
            self.MplWidget.canvas.axes.plot(sol2)
            self.MplWidget.canvas.axes.plot(sol3)
            self.MplWidget.canvas.axes.legend((opt.name, opt2.name,opt3.name),loc='upper right')
        self.MplWidget.canvas.axes.set_title('Convergence curve')
        self.MplWidget.canvas.draw()

    def InputButton(self,isSMA,input):
            if  isSMA:
                #SMA
                self.window = PyQt5.QtWidgets.QMainWindow()
                loadUi('SMA_Inputs.ui', self.window)
                self.window.show()
                self.window.smaButton.clicked.connect(lambda: self.SMAInputOkButton(input))
                #Set predefined values
                self.window.problemSizeTextBox.setText("100")
                self.window.epochTextBox.setText("10")
                self.window.popSizeTextBox.setText("50")
                self.window.lbTextBox.setText("-100")
                self.window.ubTextBox.setText("100")
            else:
                #Other Optimizations
                self.window = PyQt5.QtWidgets.QMainWindow()
                loadUi('Inputs.ui', self.window)
                self.window.show()
                self.window.hhoButton.clicked.connect(lambda: self.HHOInputOkButton(input))
                #Set predefined values
                self.window.maxIterationTextBox.setText("10")
                self.window.dimensionTextBox.setText("30")
                self.window.searchAgentsTextBox.setText("1000")
                self.window.lbTextBox.setText("-32768")
                self.window.ubTextBox.setText("32768")
    def InputButton1(self):
        isSMA = self.optimizationComboBox.currentIndex()==12
        self.InputButton(isSMA,0)
    def InputButton2(self):
        if self.optimizationComboBox_2.currentText()=="None" :
            return
        isSMA = self.optimizationComboBox_2.currentIndex()==12
        self.InputButton(isSMA,1)
    def InputButton3(self):
        if self.optimizationComboBox_3.currentText()=="None" :
            return
        isSMA = self.optimizationComboBox_3.currentIndex()==12
        self.InputButton(isSMA,2)        

            
    #HHO input window    
    def HHOInputOkButton(self,inputNumber):
        self.inputs[inputNumber].MaxIter=self.window.maxIterationTextBox.toPlainText()
        self.inputs[inputNumber].dimension=self.window.dimensionTextBox.toPlainText()
        self.inputs[inputNumber].searchAgentsNo=self.window.searchAgentsTextBox.toPlainText()
        self.inputs[inputNumber].lb=self.window.lbTextBox.toPlainText()
        self.inputs[inputNumber].ub=self.window.ubTextBox.toPlainText()
        self.window.close()
    def SMAInputOkButton(self,inputNumber):
        self.inputs[inputNumber+3].problem_size=self.window.problemSizeTextBox.toPlainText()
        self.inputs[inputNumber+3].verbose=self.window.verboseCheckBox.isChecked()
        self.inputs[inputNumber+3].epoch=self.window.epochTextBox.toPlainText()
        self.inputs[inputNumber+3].pop_size=self.window.popSizeTextBox.toPlainText()
        self.inputs[inputNumber+3].smalb=self.window.lbTextBox.toPlainText()
        self.inputs[inputNumber+3].smaub=self.window.ubTextBox.toPlainText()
        self.window.close()
    #SMA InpuWindow
    #=================
    #=================
    #=================
    #Info Ok Buttons
    def AckleyInfoOkButton(self):        
        self.window.close()
    
def AddItemsToComboBox(self):
         #Add items to functions combo Box
        self.functionComboBox.addItem('ackley')
        self.functionComboBox.addItem('dixonprice')
        self.functionComboBox.addItem('griewank')
        self.functionComboBox.addItem('michalewicz')
        self.functionComboBox.addItem('perm')
        self.functionComboBox.addItem('powell')
        self.functionComboBox.addItem('powersum')
        self.functionComboBox.addItem('rastrigin')
        self.functionComboBox.addItem('rosenbrock')
        self.functionComboBox.addItem('schwefel')
        self.functionComboBox.addItem('sphere')
        self.functionComboBox.addItem('sum2')
        self.functionComboBox.addItem('trid')
        self.functionComboBox.addItem('zakharov')
        self.functionComboBox.addItem('ellipse')
        self.functionComboBox.addItem('nesterov')
        self.functionComboBox.addItem('saddle')
        self.functionComboBox.addItem('custom')

        #Add items to optimization combo Box
        for x in range(3):
            if x==0:
                AddToOptimizationCombobox(self.optimizationComboBox)
            elif x==1:
                AddToOptimizationCombobox(self.optimizationComboBox_2)
                self.optimizationComboBox_2.addItem('None')
                self.optimizationComboBox_2.setCurrentIndex(15)
            elif x==2:
                AddToOptimizationCombobox(self.optimizationComboBox_3)
                self.optimizationComboBox_3.addItem('None')
                self.optimizationComboBox_3.setCurrentIndex(15)
                
        

def AddToOptimizationCombobox(combobox):
        combobox.addItem('BAT')
        combobox.addItem('Cuckoo Search (CS)')
        combobox.addItem('Differential evolution (DE)')
        combobox.addItem('Firefly Optimization Algorithm (FFA)')
        combobox.addItem('Genetic Algorithm (GA)')
        combobox.addItem('Grey Wolf Optimizer (GWO)')
        combobox.addItem('Harris Hawks Optimization (HHO)')
        combobox.addItem('JAYA')
        combobox.addItem('Moth-Flame Optimization (MFO)')
        combobox.addItem('Multi-Verse Optimizer (MVO)')
        combobox.addItem('Particle Swarm Optimization (PSO)')
        combobox.addItem('Sine Cosine Algorithm (SCA)')
        combobox.addItem('Slime Mould Algorithm (SMA)')
        combobox.addItem('Salp Swarm Algorithm (SSA)')
        combobox.addItem('Whale Optimization Algorithm (WOA)')   

app = QApplication([])
window = MatplotlibWidget()
window.show()
app.exec_()