from ROOT import TFile, TTree, TH1F, TH2F, TLorentzVector, TMath, TRandom, TClonesArray, TCanvas, gROOT, TGraph, TLine, TLegend

#import ratioHistograms
import ROOT

gROOT.SetBatch(True)


f_RH_1           = TFile.Open("smallTrees/RH_had_0j_500GeV.root", "read")



f_LH_1           = TFile.Open("smallTrees/LH_had_0j_500GeV.root", "read")




RHone = f_RH_1.Get("TTree_had")

LHone = f_LH_1.Get("TTree_had")


#c1 = TCanvas()

#ROC_ratio = []

#RHoneClass = ratioHistograms.ratioHistograms(RHone, "RHone", 1)
#LHoneClass = ratioHistograms.ratioHistograms(LHone, "LHone", 0)

#RHoneClass.drawHistograms(c1)
#LHoneClass.drawHistograms(c1)

#ROC_ratio.append( (ratioHistograms.makeROC(LHoneClass.TH1F_ratio, RHoneClass.TH1F_ratio, c1, "LHone", "RHone"), "1 TeV") )


#LHoneClass.makeROC(RHoneClass, c1)


#RHfiveClass = ratioHistograms.ratioHistograms(RHfive, "RHfive", 1)
#LHfiveClass = ratioHistograms.ratioHistograms(LHfive, "LHfive", 0)

#RHfiveClass.drawHistograms(c1)
#LHfiveClass.drawHistograms(c1)
#LHfiveClass.makeROC(RHfiveClass, c1)


#ROC_ratio.append( (ratioHistograms.makeROC(LHfiveClass.TH1F_ratio, RHfiveClass.TH1F_ratio, c1, "LHfive", "RHfive"), "5 TeV") )


#ratioHistograms.ROCMGDraw(ROC_ratio, c1)



## TMVA stuff:
## http://nbviewer.jupyter.org/github/demattia/usercode/blob/master/Tutorials/InteractiveAnalysis/Notebooks/HATS_2013/TMVA.ipynb

sigCut = ROOT.TCut("RightHanded > 0.5")
bgCut = ROOT.TCut("RightHanded <= 0.5")


ROOT.TMVA.Tools.Instance()

# note that it seems to be mandatory to have an
# output file, just passing None to TMVA::Factory(..)
# does not work. Make sure you don't overwrite an
# existing file.
fout = ROOT.TFile("TMVAResults.root","RECREATE")

factory = ROOT.TMVA.Factory("TMVAClassification", fout,
                            ":".join([
                                "!V",
                                "!Silent",
                                "!Color",
                                "!DrawProgressBar",
                                "Transformations=I;D;P;G,D",
                                "AnalysisType=Classification"]
                                     ))


dataloader =  ROOT.TMVA.DataLoader("dataset")

#dataloader.AddVariable("ratiojb","F")
dataloader.AddVariable("jj_pt","F")
#dataloader.AddVariable("jj_eta","F")
#dataloader.AddVariable("jj_phi","F")

dataloader.AddVariable("bjet_pt","F")
#dataloader.AddVariable("bjet_eta","F")
#dataloader.AddVariable("bjet_phi","F")

#dataloader.AddVariable("deltaR","F")

dataloader.AddSignalTree(RHone)
dataloader.AddBackgroundTree(LHone)


dataloader.PrepareTrainingAndTestTree(sigCut,   # signal events
                                   bgCut,    # background events
                                   ":".join([
                                        "nTrain_Signal=0",
                                        "nTrain_Background=0",
                                        "SplitMode=Random",
                                        "NormMode=NumEvents",
                                        "!V"
                                       ]))



methodBDT = factory.BookMethod(dataloader, ROOT.TMVA.Types.kBDT, "BDT",
                   ":".join([
                       "!H",
                       "!V",
                       "NTrees=850",
                       "nEventsMin=150",
                       "MaxDepth=3",
                       "BoostType=AdaBoost",
                       "AdaBoostBeta=0.5",
                       "SeparationType=GiniIndex",
                       "nCuts=20",
                       "PruneMethod=NoPruning",
                       ]))


factory.TrainAllMethods()
factory.TestAllMethods()
factory.EvaluateAllMethods()
#outputFile.Close()
#ROOT.TMVA.TMVAGui(outfname)
#gApplication.Run() 




#Bundle = UntypedLabel
#
#RH_one_array = tree2array(RHone,
#	 branches=[	'Muon.PT[0]', 'Jet.PT[0]' , 
#	 			'Jet.PT[0]/(Muon.PT[0] + Jet.PT[0])'],
#    selection='Muon.PT[0] > 10',
#    start=0, stop=-1, step=1)
#
#
#RH_one_array.dtype.names = [	'muonPt', 'leadingJetPt', 
#						'ratio'  ]
#
#
#print RH_one_array
#
#standard_histograms = Select( lambda array: numpy.logical_and(array['muonPt'] > 10 ,abs(array['leadingJetPt']) > 10), Bundle(
#
#
#D1_ratio = Bin(	100, 0, 1, 
#	lambda array : (array['ratio'], Count() )),
#
#))
#
#standard_histograms.fill.numpy(RH_one_array)
#
#TH1D_ratio = standard_histograms.get("D1_ratio").plot.root("D1_ratio", "ratio")
#
#TH1D_ratio.Draw()
#c1.SaveAs("TH1D_ratio.png")#